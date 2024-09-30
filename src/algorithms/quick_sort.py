#from src.analysis.analyzer import timer
#import random

#@timer
def quick_sort(arr, low, high, *args):
    """
    Sorts the given array in ascending order using the quick sort algorithm.

    Parameters:
    arr (list): The list to be sorted.
    low (int): Start index of array.
    high (int): End index of array.
    
    Yield:
    tuple: Array, pivot, left pointer, right pointer

    Returns:
    list: The sorted list.
    """
    if low < high:
        pi, yield_array = yield from partition(arr, low, high) # Partition array and yield current value
        
        yield from quick_sort(arr, low, pi - 1) # Left side
        yield from quick_sort(arr, pi + 1, high) # Right side
        
        yield arr, None, None, None, None # Yield sorted array
        
def partition(arr, low, high):
    """
    Partition the array around a pivot.
    The last element is the pivot.

   Yield:
   tuple: Pivot index, array, and current index
   
    """
    pivot = arr[high] # Select last element
    i = low - 1 # Pointer for next greater element
    pivot_index = high # Track pivot index
    
    for j in range(low, high):
        yield arr, pivot_index, i, j, None # Yield current state of array
        
        if arr[j] < pivot: # Swap if current element is smaller than pivot
            i += 1
            arr[i], arr[j] = arr[j], arr[i] 

            yield arr, pivot_index, i, j, None # Yield array after swapping
            
    arr[i + 1], arr[high] = arr[high], arr[i +1] # Swap pivot element with element at i+1
    
    yield arr, pivot_index, i + 1, high, None # Yield array state after placing pivot
    
    return i + 1, arr # Return partitioning index
   
    #Old Code (Just in case we need it)
    '''# Base case: if the array has one or no elements, it is already sorted
    if len(arr) <= 1:
        #yield arr, -1, -1, -1 # Sorted
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
    '''
    
#test code:
#arr = [random.randint(0, 100) for i in range(100)]
#quick_sort(arr)
