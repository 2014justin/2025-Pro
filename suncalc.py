# The following script is a complete code that will take as inputs
# Latitude and time of year and give you complete information on
# Local sunrise, sunset, solar noon, and equation of time.
# automatically converting it to local time.

# The code will loop unless you type q

# It will automatically estimate your timezone offset from longitude.
# I've noticed that the results are accurate however the solar noon calculation
# may be early. For example doing Denver CO, it says the solar noon is before 12:00PM.
# Which is wrong because in reality it is closer to 1:00PM.

from math import sin, cos, tan, radians, degrees, acos, pi # We will use radians

# Define solar declination and equation of time functions.
# Intuitively, the solar declination is 23.5 deg at the summer solstice and
# -23.5 deg at the winter solstice.

def solar_declination(day_of_year: int) -> tuple: 
    B = 2 * pi * (day_of_year - 81) / 365.0
    delta_deg = 23.44 * sin(B)
    delta_rad = radians(delta_deg)
    return delta_rad, delta_deg

def equation_of_time(day_of_year: int) -> float:
    B = 2 * pi * (day_of_year - 81) / 365.0
    eot = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B)
    return eot

def daylight_duration_hours(latitude_deg: float, declination_rad: float) -> float:
    phi = radians(latitude_deg)
    cosH = -tan(phi) * tan(declination_rad)
    if cosH <= -1:
        return 24.0  # sun never sets
    elif cosH >= 1:
        return 0.0   # sun never rises
    H_rad = acos(cosH)
    daylight_hours = (2 * degrees(H_rad)) / 15.0
    return daylight_hours

def solar_noon_localtime_minutes(longitude_deg, eot_minutes, timezone_offset_hours):
    # Solar noon in minutes from midnight, adjusted by timezone offset
    solar_noon_std = 720 - (4 * longitude_deg) - eot_minutes
    return solar_noon_std + (timezone_offset_hours * 60)

def minutes_to_hhmm(minutes: float) -> str:
    minutes = minutes % 1440  # wrap around 24 hr
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    ampm = "AM" if hours < 12 else "PM"
    hours = hours % 12
    if hours == 0:
        hours = 12
    return f"{hours:02d}:{mins:02d} {ampm}"

def main():
    print("**IMPORTANT:**\n- Enter longitude positive for EAST of Greenwich, negative for WEST.")
    print("Type 'q' at any prompt to quit.\n")
    while True:
        lat_input = input("Enter latitude (degrees, north positive): ")
        if lat_input.lower() == 'q':
            print("Exiting...")
            break
        lon_input = input("Enter longitude (degrees, east positive): ")
        if lon_input.lower() == 'q':
            print("Exiting...")
            break
        day_input = input("Enter day of year (1-365): ")
        if day_input.lower() == 'q':
            print("Exiting...")
            break

        try:
            latitude = float(lat_input)
            longitude = float(lon_input)
            day_number = int(day_input)
        except ValueError:
            print("Invalid input. Please enter numeric values or 'q' to quit.\n")
            continue

        if not (1 <= day_number <= 365):
            print("Day of year must be between 1 and 365.\n")
            continue
        if not (-90 <= latitude <= 90):
            print("Latitude must be between -90 and 90 degrees.\n")
            continue
        if not (-180 <= longitude <= 180):
            print("Longitude must be between -180 and 180 degrees.\n")
            continue

        # Estimate timezone offset from longitude
        timezone_offset = round(longitude / 15)

        delta_rad, delta_deg = solar_declination(day_number)
        eot_min = equation_of_time(day_number)
        daylight_hrs = daylight_duration_hours(latitude, delta_rad)
        solar_noon_min = solar_noon_localtime_minutes(longitude, eot_min, timezone_offset)
        sunrise_min = solar_noon_min - (daylight_hrs * 60) / 2
        sunset_min = solar_noon_min + (daylight_hrs * 60) / 2

        print(f"\nResults for day {day_number} at ({latitude}°, {longitude}°):")
        print(f"Estimated timezone offset: UTC{timezone_offset:+d}")
        print(f"Declination: {delta_deg:.2f}°")
        print(f"Equation of Time: {eot_min:.2f} min")
        print(f"Daylight: {int(daylight_hrs)}h {int((daylight_hrs*60) % 60)}m")
        print(f"Sunrise: {minutes_to_hhmm(sunrise_min)}")
        print(f"Solar Noon: {minutes_to_hhmm(solar_noon_min)}")
        print(f"Sunset: {minutes_to_hhmm(sunset_min)}\n")

if __name__ == "__main__":
    main()
