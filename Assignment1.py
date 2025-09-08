def insertion_sort_decreasing(arr):
    """
    Sorts an array in monotonically decreasing order using the Insertion Sort algorithm.

    Args:
        arr: A list of comparable elements.
    """
    # Iterate from the second element to the end of the array
    for i in range(1, len(arr)):
        # Select the current element to be inserted
        key = arr[i]
        
        # Start comparing with the element to the left of the current element
        j = i - 1
        
        # Shift elements of the sorted portion that are smaller than the key
        # to the right to make space for the key
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1
        
        # Insert the key into its correct position
        arr[j + 1] = key
    
    return arr

# Example Usage
my_list = [12, 11, 13, 5, 6]
sorted_list = insertion_sort_decreasing(my_list)
print(f"Original list: [12, 11, 13, 5, 6]")
print(f"Sorted list (decreasing): {sorted_list}")

# Expected Output: [13, 12, 11, 6, 5]