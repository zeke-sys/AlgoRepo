import array
import math

# implementing heap
# given array a, heapify(a) will turn a into a heap
def heapify(a):
    n = len(a)

    # Function to maintain the heap property
    def sift_down(i):
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left child index
        right = 2 * i + 2  # right child index

        # If left child is larger than root
        if left < n and a[left] > a[largest]:
            largest = left

        # If right child is larger than largest so far
        if right < n and a[right] > a[largest]:
            largest = right

        # If largest is not root
        if largest != i:
            a[i], a[largest] = a[largest], a[i]  # Swap
            sift_down(largest)  # Recursively heapify the affected sub-tree

    # Build a maxheap
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i)

    return a
    #raise NotImplementedError("Function not yet implemented")

# given a heap a and index j, bubble_up will bubble the element at index j up to its correct position
def bubble_up(a, j):
    while j > 0:
        parent = (j - 1) // 2
        if a[j] > a[parent]:
            a[j], a[parent] = a[parent], a[j]
            j = parent
        else:
            break
    return a
    #raise NotImplementedError("Function not yet implemented")

# given a heap a and index j, bubble_down will move the element at index j down to its correct position
def bubble_down(a, j):
    n = len(a)
    while True:
        largest = j
        left = 2 * j + 1
        right = 2 * j + 2

        if left < n and a[left] > a[largest]:
            largest = left
        if right < n and a[right] > a[largest]:
            largest = right
        if largest != j:
            a[j], a[largest] = a[largest], a[j]
            j = largest
        else:
            break
    return a
    #raise NotImplementedError("Function not yet implemented")

# given a heap a, extract_min(a) will swap the root with the last child of the heap, then fix the heap properly
def extract_min(a):
    if len(a) == 0:
        return None  # Heap is empty

    min_elem = a[0]  # The root element
    a[0] = a[-1]  # Move the last element to root
    a.pop()  # Remove the last element

    # Function to maintain the heap property
    def sift_down(i):
        n = len(a)
        smallest = i  # Initialize smallest as root
        left = 2 * i + 1  # left child index
        right = 2 * i + 2  # right child index

        # If left child is smaller than root
        if left < n and a[left] < a[smallest]:
            smallest = left

        # If right child is smaller than smallest so far
        if right < n and a[right] < a[smallest]:
            smallest = right

        # If smallest is not root
        if smallest != i:
            a[i], a[smallest] = a[smallest], a[i]  # Swap
            sift_down(smallest)  # Recursively heapify the affected sub-tree

    sift_down(0)  # Heapify the root element
    return min_elem
    #raise NotImplementedError("Function not yet implemented")

#----------------------------------------------

#Example usage:
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
heap = heapify(arr)
print("Heapified array:", heap)  # Output: Heapified array
print("Bubble up index 5:", bubble_up(heap, 5))  # Output: Bubble up index 5
print("Bubble down index 0:", bubble_down(heap, 0))  # Output: Bubble down index 0
print("Extracted min:", extract_min(heap))  # Output: Extracted min
print("Heap after extraction:", heap)  # Output: Heap after extraction
#----------------------------------------------


# implement heapsort
# the function heapsort(a) sorts the array in place and returns the number of direct comparisons
# (is a[i] < a[j]) made
# must use heap implemenatation
def heapsort(a):
    n = len(a)
    if n <= 1:
        return 0  # No comparisons needed for arrays of length 0 or 1

    # First, build the heap
    heapify(a)

    total_count = 0

    # Function to maintain the heap property and count comparisons
    def sift_down(i, heap_size):
        nonlocal total_count
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left child index
        right = 2 * i + 2  # right child index

        # If left child is larger than root
        if left < heap_size:
            total_count += 1  # Comparison made here
            if a[left] > a[largest]:
                largest = left

        # If right child is larger than largest so far
        if right < heap_size:
            total_count += 1  # Comparison made here
            if a[right] > a[largest]:
                largest = right

        # If largest is not root
        if largest != i:
            a[i], a[largest] = a[largest], a[i]  # Swap
            sift_down(largest, heap_size)  # Recursively heapify the affected sub-tree

    # One by one extract elements from heap
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]  # Move current root to end
        sift_down(0, i)  # call sift_down on the reduced heap

    return total_count
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print("Number of comparisons in heapsort:", heapsort(arr)) #Output: Number of comparisons
print("Sorted array:", arr) #Output: Sorted array
#Output: Sorted array

# End of 3104HW4.py