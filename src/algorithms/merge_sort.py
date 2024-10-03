def merge_sort(array, left, right):
    """
    Sorts a given array using the Merge Sort algorithm.

    The Merge Sort algorithm is a divide and conquer algorithm 
    that recursively divides the input list in half and sorts 
    each half before merging them back together. This process 
    is repeated until the entire list is sorted. 

    Time complexity: O(n log n).
    """
    # Check if the left index is less than the right index
    if left < right:
        # Calculate the middle index
        mid = int((left + right) / 2)
        
        # Recursively sort the left half of the array
        yield from merge_sort(array, left, mid)
        
        # Recursively sort the right half of the array
        yield from merge_sort(array, mid + 1, right)
        
        # Merge the two sorted halves
        yield from merge(array, left, mid, right)


def merge(array, left, mid, right):
    """
    Merges two sorted subarrays into a single sorted array.

    This function takes two sorted subarrays and merges them 
    into a single sorted array. The subarrays are defined by 
    the indices left, mid, and right.
    """
    # Create temporary arrays for the left and right halves
    bottom = array[left:mid + 1]  # Left sorted subarray
    top = array[mid + 1:right + 1]  # Right sorted subarray
    
    # Initialize pointers for bottom, top, and the main array
    i = 0  # Pointer for the left subarray
    j = 0  # Pointer for the right subarray
    k = left  # Pointer for the main array
    
    # Merge the two subarrays until one is exhausted
    while i < len(bottom) and j < len(top):
        # Yield the current state of the array and indices being merged
        yield array, left + i, mid + j, left, right
        
        # Compare elements from both subarrays and merge them
        if bottom[i] < top[j]:
            array[k] = bottom[i]  # Take from the left subarray
            i += 1  # Move the pointer in the left subarray
        else:
            array[k] = top[j]  # Take from the right subarray
            j += 1  # Move the pointer in the right subarray
        k += 1  # Move the pointer in the main array
    
    # Copy any remaining elements from the left subarray
    while i < len(bottom):
        array[k] = bottom[i]  # Copy remaining element
        i += 1  # Move the pointer in the left subarray
        k += 1  # Move the pointer in the main array
    
    # Copy any remaining elements from the right subarray
    while j < len(top):
        array[k] = top[j]  # Copy remaining element
        j += 1  # Move the pointer in the right subarray
        k += 1  # Move the pointer in the main array

        """
        Theoretical Complexity of Merge Sort Algorithm:

        1. Time Complexity:
           - Best Case: O(n log n) - This occurs when the array is already sorted. The algorithm still needs to divide the array and merge the subarrays, leading to a logarithmic number of divisions and linear merging.
           - Average Case: O(n log n) - On average, the algorithm will need to perform n comparisons for each of the log n levels of recursion, resulting in a time complexity of n log n.
           - Worst Case: O(n log n) - This occurs when the array is in reverse order. Similar to the average case, the algorithm will still require n comparisons for each of the log n levels of recursion.

        2. Space Complexity:
           - O(n) - Merge sort requires additional space for temporary arrays used during the merging process. The space complexity is linear because it needs to store the elements of the array being sorted.

        Overall, merge sort is an efficient and stable sorting algorithm that performs well on large datasets. Its divide-and-conquer approach allows it to maintain a consistent time complexity across different scenarios, making it a preferred choice for sorting linked lists and large arrays.
        """