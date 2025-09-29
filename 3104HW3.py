import array
import math

#Function sorts the array in place and returns the number of direct comparisons (is a[i] < a[j]) made
#by implementing quicksort

def quicksort(a):
    def partition(low, high):
        pivot = a[high]  # Choosing the last element as pivot
        i = low - 1  # Pointer for the smaller element
        count = 0  # Count of comparisons

        for j in range(low, high):
            count += 1  # Comparison made here
            if a[j] < pivot:  # Stable sort
                i += 1
                a[i], a[j] = a[j], a[i]  # Swap elements

        a[i + 1], a[high] = a[high], a[i + 1]  # Place pivot in the correct position
        return i + 1, count

    def quicksort_recursive(low, high):
        if low < high:
            pi, count = partition(low, high) # participating index and count of comparisons
            left_count = quicksort_recursive(low, pi - 1) # recur on the left side
            right_count = quicksort_recursive(pi + 1, high) # recur on the right side
            return count + left_count + right_count
        return 0

    total_count = quicksort_recursive(0, len(a) - 1)
    return total_count
    #raise NotImplementedError("Function not yet implemented")

#Quickselect with Median of 7 Medians
#first, split into n//7 lists of length 7 and sort them
#next, make a list of the medians of each of these lists
#next, use quickselect on this list of medians to find its median
#partition the original list using this median of medians as the pivot
#finally, recurse quickselect on the side containing the sought for element
def quickselect(a, j):
    n = len(a)
    if j < 0 or j > n - 1:
        return False # j is out of bounds

    def median_of_medians(arr):
        # Split arr into sublists of length 7
        sublists = [arr[i:i + 7] for i in range(0, len(arr), 7)]
        medians = []
        for sublist in sublists:
            sublist.sort()
            medians.append(sublist[len(sublist) // 2])  # Append the median
        if len(medians) <= 7:
            medians.sort()
            return medians[len(medians) // 2]  # Return the median of medians
        else:
            return median_of_medians(medians)  # Recur on the medians list

    def partition(low, high, pivot):
        pivot_index = a.index(pivot)
        a[pivot_index], a[high] = a[high], a[pivot_index]  # Move pivot to end
        store_index = low
        for i in range(low, high):
            if a[i] < pivot:
                a[store_index], a[i] = a[i], a[store_index]
                store_index += 1
        a[store_index], a[high] = a[high], a[store_index]  # Move pivot to its final place
        return store_index

    def quickselect_recursive(low, high, k):
        if low == high:
            return a[low]

        pivot = median_of_medians(a[low:high + 1]) # find a good pivot
        pivot_index = partition(low, high, pivot) # partition around the pivot

        if k == pivot_index:
            return a[k] # found the k-th smallest element
        elif k < pivot_index:
            return quickselect_recursive(low, pivot_index - 1, k) # search in the left side
        else:
            return quickselect_recursive(pivot_index + 1, high, k) # search in the right side

    return quickselect_recursive(0, n - 1, n - j) # return the n-j-th smallest (0-based index) element
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [3, 6, 2, 7, 5, 14]
print(quicksort(arr)) #Output: Number of comparisons made
print(arr) #Output: [2, 3, 5, 6, 7, 14]
print(quickselect(arr, 2)) #Output: 5 (the 3rd smallest element) #Output: 3