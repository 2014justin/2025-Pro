import os
import time

# The following code will benchmark the external
# SSD harddrive 'Q Drive' by writing and reading a file.
# The path according to the terminal is:
# /Volumes/Q Drive

TEST_FILE = "/Volumes/Q Drive/testfile.bin" # Points to the external SSD.
FILE_SIZE_MB = 4096 / 2 # Size of the test file in MB (2GB)
CHUNK_SIZE = 4 * 1024 * 1024 # Chunk size 

def write_test():
    print("Starting write test...")
    data = os.urandom(CHUNK_SIZE)
    total_bytes = FILE_SIZE_MB * 1024 * 1024
    written = 0
    start = time.time()

    with open(TEST_FILE, "wb") as f:
        while written < total_bytes:
            f.write(data)
            written += len(data)

    end = time.time()
    elapsed = end - start
    throughput = (total_bytes / (1024 * 1024)) / elapsed
    print(f"Write speed: {throughput:.2f} MB/s")

def read_test():
    print("Starting read test...")
    total_bytes = FILE_SIZE_MB * 1024 * 1024
    read = 0
    start = time.time()

    with open(TEST_FILE, "rb") as f:
        while read < total_bytes:
            f.read(CHUNK_SIZE)
            read += CHUNK_SIZE

    end = time.time()
    elapsed = end - start
    throughput = (total_bytes / (1024 * 1024)) / elapsed
    print(f"Read speed: {throughput:.2f} MB/s")

if __name__ == "__main__":
    write_test()
    read_test()
    os.remove(TEST_FILE)  # Clean up the test file after testing