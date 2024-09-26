from src.analysis.analyzer import timer
#import random

@timer
def linear_search(arr, target):
    """
    Perform a linear search for the target in the given array.

    Parameters:
    arr (list): The list to search through.
    target: The value to search for.

    Returns:
    int: The index of the target if found, otherwise -1.
    """
    # Iterate over the array using enumerate to get both index and value
    for index, value in enumerate(arr):
        # Check if the current value matches the target
        if value == target:
            # If a match is found, return the index
            return index
    # If the target is not found in the array, return -1
    return -1


#test code:
#arr = [random.randint(0, 675) for _ in range(10000)]
#target = 56
#linear_search(arr, target)