def merge_sort(array, left, right):
    """
    Sorts a given array using the Merge Sort algorithm.

    Merge Sort algorithm is a divide and conquer algorithm 
    that recursively divides the input list in half and sorts 
    each half before merging them back together. This process 
    is repeated until the entire list is sorted. 

    Time complexity: O(nlog²n).
    """
    if left < right:
        mid = int((left + right) / 2)
        yield from merge_sort(array, left, mid)
        yield from merge_sort(array, mid + 1, right)
        yield from merge(array, left, mid, right)


def merge(array, left, mid, right):
    """
    Merges two sorted arrays into a single sorted array.
    """
    bottom = array[left:mid + 1]
    top = array[mid + 1:right + 1]
    i = 0
    j = 0
    k = left
    while i < len(bottom) and j < len(top):
        # The two lines below are not part of the algorithm
        yield array, left + i, mid + j, left, right
        if bottom[i] < top[j]:
            array[k] = bottom[i]
            i += 1
        else:
            array[k] = top[j]
            j += 1
        k += 1
    while i < len(bottom):
        array[k] = bottom[i]
        i += 1
        k += 1
    while j < len(top):
        array[k] = top[j]
        j += 1
        k += 1