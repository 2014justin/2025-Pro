import math

def dewpoint_to_rh_f(T_f, Td_f):
    """
    Calculate relative humidity (%) from air temp and dew point in Fahrenheit.
    """
    
    T_c = (T_f - 32) * 5/9
    Td_c = (Td_f - 32) * 5/9
    A = 17.625
    B = 243.04
    alpha_td = (A * Td_c) / (B + Td_c) # For units to workout, B has units of °C
    alpha_t = (A * T_c) / (B + T_c) #A must be dimensionless.
    return 100 * math.exp(alpha_td - alpha_t) 

def nws_heat_index_f(T_f, Td_f):
    
    # Calculate heat index (°F) using NWS full algorithm from flowchart.
    # Inputs are Air Temp in Fahrenheit (T_f) and Dew point
    # Temperature in Fahrenheit (Td_f)
    
    # Step 1: Relative humidity
    H = dewpoint_to_rh_f(T_f, Td_f) 
    # Input Temperature in Fahrenheit (T_f) 

    # Flowchart step 1
    if T_f <= 40:
        return T_f, H  # HI = air temp directly

    # Step 2: Simple formula A
    A = -10.3 + 1.1 * T_f + 0.047 * H
    if A < 79:
        return A, H

    # Step 3: Rothfusz regression (B)
    B = (-42.379 + 2.04901523 * T_f + 10.14333127 * H
         - 0.22475541 * T_f * H - 6.83783e-3 * T_f**2
         - 5.481717e-2 * H**2 + 1.22874e-3 * T_f**2 * H
         + 8.5282e-4 * T_f * H**2 - 1.99e-6 * T_f**2 * H**2)

    # Step 4: Adjustments
    # If you're in a desert climate, the algorithm will likely use this
    # equation.
    if H <= 13 and 80 <= T_f <= 112:
        adj = ((13 - H) / 4) * math.sqrt((17 - abs(T_f - 95)) / 17)
        B -= adj #adjust the heat index downwards in hot desert climates
    elif H > 85 and 80 <= T_f <= 87:
        B += 0.02 * (H - 85) * (87 - T_f)

    return B, H

if __name__ == "__main__":
    print("NWS Heat Index Calculator (°F inputs) — type 'q' to quit.\n")
    
    while True:
        temp_input = input("Enter air temperature (°F) or 'q' to quit: ").strip().lower()
        if temp_input in ("q", "quit"):
            print("Goodbye!")
            break
        
        dew_input = input("Enter dew point temperature (°F): ").strip().lower()
        if dew_input in ("q", "quit"):
            print("Goodbye!")
            break
        
        try:
            T_f = float(temp_input)
            Td_f = float(dew_input)
        except ValueError:
            print("Invalid number entered. Try again.\n")
            continue
        
        HI_f, RH = nws_heat_index_f(T_f, Td_f)
        print(f"Relative Humidity: {RH:.1f}%")
        print(f"Heat Index: {HI_f:.1f}°F\n")
