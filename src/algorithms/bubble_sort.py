#from src.analysis.analyzer import timer
#import random

#@timer
def bubble_sort(arr, *args):
    """
    Sorts the given array in ascending order using the bubble sort algorithm.

    Parameters:
    arr (list): The list to be sorted.
    
    Yields:
    tuple: Contains the list and index of each bar which are then highlighted to then be swapped

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
                yield arr, j, j+1, -1, -1 # Yield current state of array and index of swapped bars
    yield arr, -1, -1, -1, -1 # End of yield
    #return arr  # Return the fully sorted array

    """
    Theoretical Complexity of Bubble Sort Algorithm:

    1. Time Complexity:
       - Best Case: O(n) - This occurs when the array is already sorted. The algorithm will make a single pass through the array to confirm that no swaps are needed.
       - Average Case: O(n^2) - On average, the algorithm will need to perform n/2 comparisons for each of the n elements, leading to a quadratic time complexity.
       - Worst Case: O(n^2) - This occurs when the array is sorted in reverse order. The algorithm will need to make n passes through the array, with each pass requiring n comparisons.

    2. Space Complexity:
       - O(1) - Bubble sort is an in-place sorting algorithm, meaning it requires a constant amount of additional space regardless of the input size.

    Overall, bubble sort is not efficient for large datasets and is primarily used for educational purposes to illustrate the concept of sorting algorithms.
    """
