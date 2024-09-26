# Demo program to measure execution time of a Python function
import time

def timer(func):
    """Function decorator to measure execution time of functions."""
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time
        print(f'Starting execution of {func.__name__}')
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # End time
        execution_time = end_time - start_time  # Calculate execution time
        print(f'{func.__name__} executed in: {execution_time} seconds')
        return result
    return wrapper

# - The timer decorator is used to measure and print the execution time of any function it decorates.
