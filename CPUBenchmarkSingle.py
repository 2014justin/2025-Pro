import time
import math
import multiprocessing

# Run a simple benchmark that leverages multiple threads.
# Number crunching is a good way to stress the single core performance of
# Apple M4 silicon. 

def cpu_benchmark(L=5):
    # Run a Synthetic CPU Benchmark
    # Return operations per second
    start_time = time.time()
    ops = 0

    # Run until L seconds elapse
    while time.time() - start_time < L:
        # Example workload: floating-point + math ops
        for i in range(1000):
            _ = math.sqrt(i) * math.log(i+1)**2/ (math.cos(i) + 1.0000001) + math.tan(i)
            ops += 1000

    return ops


def multiprocess_benchmark(L, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(cpu_benchmark, [L]*num_processes)
    total_ops = sum(results)
    return total_ops

if __name__ == "__main__":
    L = 30 # adjustable benchmark length in seconds
    num_processes = 4 # <--- Change this value to set number of processes (cores)

    start_time = time.time()
    total_ops = multiprocess_benchmark(L, num_processes)
    elapsed = time.time() - start_time
    score = total_ops / elapsed

    print(f"Benchmark length requested: {L} sec")
    print(f"Processes used: {num_processes}")
    print(f"Actual elapsed: {elapsed:.2f} sec")
    print(f"Total operations: {total_ops:,}")
    print(f"Score: {score:,.0f} ops/sec")

