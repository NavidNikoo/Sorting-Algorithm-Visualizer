#from src.analysis.analyzer import timer
import random

#@timer
def merge_sort(arr, *args):
    """
    Sorts the given array in ascending order using the merge sort algorithm.

    Parameters:
    arr (list): The list to be sorted.
    
    Yield:
    tuple: The array and index will be merged

    Returns:
    list: The fully sorted list.
    """
    # Check if the array has more than one element
    if len(arr) > 1:
        # Find the middle index to split the array
        mid = len(arr) // 2
        # Divide the array into two halves
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively sort both halves
        yield from merge_sort(left_half)
        yield from merge_sort(right_half)

        # Initialize pointers for left_half, right_half, and the main array
        i = j = k = 0

        # Merge the sorted halves back into the original array
        while i < len(left_half) and j < len(right_half):
            # Compare elements from both halves and place the smaller one in the main array
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1  # Move to the next element in left_half
            else:
                arr[k] = right_half[j]
                j += 1  # Move to the next element in right_half
            k += 1  # Move to the next position in the main array
            yield arr, k, i, j, -1 # Highlight the merge

        # If there are remaining elements in left_half, add them to the main array
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
            yield arr, k, i, -1, -1 # Highlight the rest of the left half

        # If there are remaining elements in right_half, add them to the main array
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
            yield arr, k, -1, j, -1 # Highlight the rest of the right half

    yield arr,  -1, -1, -1, -1 # Sorting has finished
    #return arr  # Return the fully sorted array

arr = [random.randint(0, 100) for i in range(100)]
merge_sort(arr)