import random

def counting_sort(arr, exp, *args):
    """
    A function to perform counting sort on the array based on the digit represented by exp.
    
    Parameters:
    arr (list): The list to be sorted.
    exp (int): The exponent representing the current digit place (1 for units, 10 for tens, etc.).
    
    Yield:
    list: Array sorted at current index.
    
    Returns:
    list: The sorted list based on the current digit.
    """
    n = len(arr)  # Get the length of the input array
    output = [0] * n  # Output array to hold sorted values
    count = [0] * 10  # Count array for digits 0-9

    # Count occurrences of each digit in the current place value
    for i in range(n):
        index = (arr[i] // exp) % 10  # Get the digit at the current place value
        count[index] += 1  # Increment the count for this digit
        yield arr, i, None, None, None

    # Change count[i] so that it contains the actual position of this digit in output[]
    for i in range(1, 10):
        count[i] += count[i - 1]  # Cumulative count

    # Build the output array by placing elements in their correct position
    for i in range(n - 1, -1, -1):  # Traverse the input array in reverse
        index = (arr[i] // exp) % 10  # Get the digit at the current place value
        output[count[index] - 1] = arr[i]  # Place the element in the output array
        count[index] -= 1  # Decrement the count for this digit
        yield arr, i, count[index], None, None

    # Copy the output array to arr[], so that arr[] now contains sorted numbers
    for i in range(n):
        arr[i] = output[i]  # Update the original array with sorted values
        yield arr, i, count[index], None, None

    #return arr  # Return the partially sorted array
    yield arr, i, None, None, None # Yield array at current index

def radix_sort(arr, *args):
    """
    Sorts the given array in ascending order using the radix sort algorithm.

    Parameters:
    arr (list): The list to be sorted.

    Yield:
    list: Array sorted at current index.
    
    Returns:
    list: The sorted list.
    """
    # Find the maximum number to know the number of digits
    max_num = max(arr)  # Get the maximum value in the array

    # Apply counting sort to sort elements based on place value
    exp = 1  # Start with the least significant digit
    while max_num // exp > 0:  # Continue until we have processed all digits
        yield from counting_sort(arr, exp)  # Sort the array based on the current digit
        exp *= 10  # Move to the next digit place (units to tens to hundreds, etc.)

    #return arr  # Return the fully sorted array
    yield arr, None, None, None, None # Final yield of sorted array

    """
    Theoretical Complexity of Radix Sort Algorithm:

    1. Time Complexity:
       - Best Case: O(nk) - The best case occurs when the input array is uniformly distributed across the range of digits. The algorithm will still need to process each digit of each number, leading to a linear relationship with respect to the number of elements (n) and the number of digits (k).
       - Average Case: O(nk) - On average, the time complexity remains O(nk) as the algorithm processes each digit of each number, regardless of the distribution of the input.
       - Worst Case: O(nk) - The worst case also results in O(nk) time complexity, as the algorithm must still process all digits of all numbers in the array.

    2. Space Complexity:
       - O(n + k) - The space complexity is determined by the output array and the count array used for counting occurrences of each digit. The output array requires O(n) space, while the count array requires O(k) space, where k is the range of the digit values (0-9 for decimal numbers).

    Overall, radix sort is efficient for sorting large datasets of integers or strings, especially when the number of digits (k) is significantly smaller than the number of elements (n). Its linear time complexity makes it suitable for specific applications where the input size is large and the range of values is limited.
    """
