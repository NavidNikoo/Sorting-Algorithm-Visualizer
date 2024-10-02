def linear_search(arr, target, *args):
    """
    Perform a linear search for the target in the given array.

    Parameters:
    arr (list): The list to search through.
    target: The value to search for.

    Yields:
    tuple: The array, the index of the current value being compared, 
           and the index of the found target (or -1 if not found).

    """
    # Iterate over the array using enumerate to get both index and value
    for index, value in enumerate(arr):
        # Check if the current value matches the target
        if value == target:
            # If a match is found, highlight the found target
            yield arr, index, index  # Highlight the found target in green
            return
        else:
            # Yield the current index being checked (highlight in red)
            yield arr, index, -1  # Highlight current index

    # If the target is not found, end the search
    yield arr, -1, -1  # End search if no target is found
