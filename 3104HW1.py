#Function takes an array a and swaps a[i] with a[j] in place

def swap(a, i, j):
    #temp = a[i]
    #a[i] = a[j]
    #a[j] = temp
    a[i], a[j] = a[j], a[i]  # Pythonic way to swap
    return a #returns the modified array
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [1, 2, 3, 4]
print(swap(arr, 0, 2)) #Output: [3, 2, 1, 4]


#insert_into (a, j) inserts j into the correct position given a sorted array a and a number j
#then it will fix the sorting of a using only swap() calls
#lastly insert returns the number of times swap() is called
def insert_into(a, j):
    count = 0
    a.append(j)  # Add j to the end of the array
    i = len(a) - 1  # Start from the last element
    while i > 0 and a[i-1] > a[i]:
        swap(a, i-1, i)  # Swap the elements
        count += 1
        i -= 1
    return count
    #raise NotImplementedError("Function not yet implemented")

#Example usage:
arr = [1, 3, 5, 7]
print(insert_into(arr, 4)) #Output: 2
print(arr) #Output: [1, 3, 4, 5, 7]
