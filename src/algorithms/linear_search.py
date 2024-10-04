def linear_search(arr, target):
    """
    Perform a linear search on the given array to find the target value.

    Parameters:
    arr (list): The list in which to search for the target.
    target: The value to search for in the list.

    Yields:
    tuple: The current state of the array and the index being checked.
           If the target is found, it yields the index of the target.
           If the target is not found, it yields (-1, -1).
    """
    # Iterate through each index in the array
    for i in range(len(arr)):
        # Yield the current state of the array and the current index
        yield arr, i, arr[i] == target  # Current state: index being checked and found status
        
        # Check if the current element matches the target
        if arr[i] == target:
            # If found, yield the current state and the index of the found target
            yield arr, i, True  # Found: return True to indicate target is present
            return  # Exit the function since the target has been found
    
    # If the loop completes without finding the target, yield not found state
    yield arr, -1, False  # Not found: return False to indicate target is absent

    """
    Theoretical Complexity of Linear Search Algorithm:

    1. Time Complexity:
       - Best Case: O(1) - This occurs when the target element is found at the first index of the array.
       - Average Case: O(n) - On average, the algorithm will need to check half of the elements in the array to find the target.
       - Worst Case: O(n) - This occurs when the target element is not present in the array, requiring the algorithm to check all n elements.

    2. Space Complexity:
       - O(1) - Linear search is an in-place algorithm, meaning it requires a constant amount of additional space regardless of the input size.

    Overall, linear search is simple and effective for small or unsorted datasets, but it becomes inefficient for large datasets compared to more advanced search algorithms like binary search.
    """
