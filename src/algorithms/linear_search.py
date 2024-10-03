def linear_search(arr, target, *args):
    """
    Perform a linear search for the target in the given array.

    Parameters:
    arr (list): The list to search through.
    target: The value to search for.

    Yields:
    tuple: The array, redBar1, redBar2, blueBar1, blueBar2.

    """
    for index, value in enumerate(arr):
        if value == target:
            # If a match is found, highlight the found target
            yield arr, index, -1, index, -1  # Found target (index is blueBar1, no redBar2 or blueBar2)
            return  # Stop the search after finding the target
        else:
            # Yield the current index being checked (highlight in red)
            yield arr, index, -1, -1, -1  # Current index is redBar1, no other bars highlighted

    # If the target is not found, end the search
    yield arr, -1, -1, -1, -1  # No bars highlighted after search ends
