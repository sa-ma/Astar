import tracemalloc
import time
from functools import wraps

def track_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Start memory tracking
        tracemalloc.start()
        start_time = time.time()

        # Run the actual function
        result = func(*args, **kwargs)

        # Stop memory tracking and execution time
        current, peak = tracemalloc.get_traced_memory()
        execution_time = time.time() - start_time
        tracemalloc.stop()
        
                # Collect the results in a dictionary
        performance_metrics = {
            "execution_time": execution_time,
            "peak_memory": peak / 1024,  # Convert to KB
            "current_memory": current / 1024,  # Convert to KB
            "temporary_memory": (peak - current) / 1024  # Convert to KB
        }

        #Print or log the results
        # print(f"Function: {func.__name__}")
        # print(f"Execution Time: {execution_time:.4f} seconds")
        # print(f"Peak Memory Usage: {peak / 1024:.2f} KB")
        # print(f"Current Memory Usage: {current / 1024:.2f} KB")
        # print(f"Temporary Memory Allocated and Released: {(peak - current) / 1024:.2f} KB")
        return result, performance_metrics

    return wrapper
