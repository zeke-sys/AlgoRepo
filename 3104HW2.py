#Function sorts an array in place and returns only the number of direct comparisons (is a[i] > a[j]) made

def mergesort(a):
    if len(a) <= 1:
        return 0  # No comparisons needed for arrays of length 0 or 1

    mid = len(a) // 2
    left = a[:mid]
    right = a[mid:]

    count = mergesort(left) + mergesort(right) # Count comparisons in recursive calls

    i = j = k = 0

    while i < len(left) and j < len(right):
        count += 1  # Comparison made here
        if left[i] <= right[j]: # Stable sort
            a[k] = left[i] # Take from left
            i += 1
        else:
            a[k] = right[j] # Take from right
            j += 1
        k += 1

    while i < len(left): # Copy any remaining elements from left
        a[k] = left[i]
        i += 1
        k += 1

    while j < len(right): # Copy any remaining elements from right
        a[k] = right[j]
        j += 1
        k += 1

    return count
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [38, 27, 43, 3, 9, 82, 10]
#print(mergesort(arr)) #Output: Number of comparisons made

#Function returns the index of fixed point if it exists, otherwise -1 given sorted array of distinct integers
# A[i] is a fixed point if A[i] = i
# Algorithm must run theta(log(n))
def find_fixed_point(a):
    left, right = 0, len(a) - 1 # Binary search initialization

    while left <= right:
        mid = (left + right) // 2 # Find mid index
        if a[mid] == mid:
            return mid
        elif a[mid] < mid: # Search in the right half
            left = mid + 1
        else:
            right = mid - 1 # Search in the left half

    return -1
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [-10, -5, 0, 3, 7]
#print(find_fixed_point(arr)) #Output: 3


# Function returns the index of fixed point if it exists, otherwise -1 given array of distinct natural numbers
# algorithm must be as efficient as possible
def find_fixed_point_natural(a):
    left, right = 0, len(a) - 1 # Binary search initialization

    while left <= right:
        mid = left + (right - left) // 2 # Find mid index
        if a[mid] == mid:
            return mid
        elif a[mid] < mid: # Search in the right half
            left = mid + 1
        else:
            right = mid - 1 # Search in the left half

    return -1
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [0, 2, 5, 8, 17]
print(find_fixed_point_natural(arr)) #Output: 0
arr = [-10, -5, 3, 4, 7, 9, 20, 50, 100]
print(find_fixed_point_natural(arr)) #Output: -1
arr = [-10, -5, 0, 3, 7]
print(find_fixed_point_natural(arr)) #Output: 3
