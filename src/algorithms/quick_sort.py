from src.analysis.analyzer import timer
#import random

@timer
def quick_sort(arr):
    """
    Sorts the given array in ascending order using the quick sort algorithm.

    Parameters:
    arr (list): The list to be sorted.

    Returns:
    list: The sorted list.
    """
    # Base case: if the array has one or no elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # Choose a pivot element from the array (here we choose the middle element)
    pivot = arr[len(arr) // 2]

    # Partition the array into three lists:
    # - left: elements less than the pivot
    # - middle: elements equal to the pivot
    # - right: elements greater than the pivot
    left = [x for x in arr if x < pivot]   # Elements less than the pivot
    middle = [x for x in arr if x == pivot] # Elements equal to the pivot
    right = [x for x in arr if x > pivot]  # Elements greater than the pivot

    # Recursively apply quick_sort to the left and right partitions
    # and concatenate the results with the middle list
    return quick_sort(left) + middle + quick_sort(right)  # Return the combined sorted array

#test code:
#arr = [random.randint(0, 100) for i in range(100)]
#quick_sort(arr)
