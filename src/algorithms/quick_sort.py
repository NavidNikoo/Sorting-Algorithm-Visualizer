def quick_sort(arr, low, high, *args):
    """
    Sorts the given array in ascending order using the quick sort algorithm.

    Parameters:
    arr (list): The list to be sorted.
    low (int): Start index of the array.
    high (int): End index of the array.
    
    Yield:
    tuple: Array, pivot, left pointer, right pointer

    Returns:
    list: The sorted list.
    """
    # Check if the current subarray has more than one element
    if low < high:
        # Partition the array and get the pivot index
        pi, yield_array = yield from partition(arr, low, high)  # Partition array and yield current value
        
        # Recursively apply quick_sort to the left subarray
        yield from quick_sort(arr, low, pi - 1)  # Sort the left side
        
        # Recursively apply quick_sort to the right subarray
        yield from quick_sort(arr, pi + 1, high)  # Sort the right side
        
        # Yield the sorted array after processing
        yield arr, None, None, None, None  # Yield sorted array
        
def partition(arr, low, high):
    """
    Partition the array around a pivot.
    The last element is the pivot.

    Yield:
    tuple: Pivot index, array, and current index
    """
    pivot = arr[high]  # Select the last element as the pivot
    i = low - 1  # Pointer for the next greater element
    pivot_index = high  # Track the pivot index
    
    # Iterate through the array to partition it
    for j in range(low, high):
        yield arr, pivot_index, i, j, None  # Yield current state of the array
        
        # If the current element is smaller than the pivot
        if arr[j] < pivot:  # Swap if current element is smaller than pivot
            i += 1  # Move the pointer for the next greater element
            arr[i], arr[j] = arr[j], arr[i]  # Swap the elements

            yield arr, pivot_index, i, j, None  # Yield array after swapping
            
    # Place the pivot element in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Swap pivot element with element at i + 1
    
    yield arr, pivot_index, i + 1, high, None  # Yield array state after placing pivot
    
    return i + 1, arr  # Return the partitioning index
    """
    Theoretical Complexity of Quick Sort Algorithm:

    1. Time Complexity:
       - Best Case: O(n log n) - This occurs when the pivot divides the array into two equal halves at each recursive step, leading to a logarithmic number of levels of recursion and linear work at each level.
       - Average Case: O(n log n) - On average, the pivot will divide the array into reasonably balanced partitions, resulting in a similar time complexity as the best case.
       - Worst Case: O(n^2) - This occurs when the pivot is the smallest or largest element in the array, leading to unbalanced partitions. In this case, the algorithm will have to make n recursive calls, each requiring O(n) time to process.

    2. Space Complexity:
       - O(log n) - This is the space complexity for the recursive stack in the best and average cases, where the depth of recursion is logarithmic. However, in the worst case, the space complexity can be O(n) due to the depth of the recursion stack.

    Overall, quick sort is an efficient sorting algorithm that performs well on average and is widely used in practice. Its in-place sorting capability and average-case performance make it a preferred choice for large datasets.
    """
