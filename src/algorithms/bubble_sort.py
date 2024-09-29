#from src.analysis.analyzer import timer
#import random

#@timer
def bubble_sort(arr, *args):
    """
    Sorts the given array in ascending order using the bubble sort algorithm.

    Parameters:
    arr (list): The list to be sorted.

    Returns:
    list: The fully sorted list.
    """
    n = len(arr)  # Get the number of elements in the array
    # Outer loop to traverse through all elements in the array
    for i in range(n):
        # Inner loop to compare adjacent elements
        for j in range(0, n-i-1):
            # If the current element is greater than the next element, swap them
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]  # Swap the elements
    return arr  # Return the fully sorted array


#test code
#arr = [random.randint(0, 675) for _ in range(10000)]
#bubble_sort(arr)