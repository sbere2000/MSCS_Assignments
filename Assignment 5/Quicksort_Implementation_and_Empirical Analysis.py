import time
import random
import copy
import sys

# Set recursion limit high for large test cases
sys.setrecursionlimit(2000)

# --- 1. DETERMINISTIC QUICKSORT IMPLEMENTATION ---

def partition(arr, low, high):
    """
    Standard Partition function: Chooses the last element as the pivot
    and places it in its correct sorted position.
    """
    pivot = arr[high]  # Deterministic: Pivot is always the last element
    i = low - 1  # Index of smaller element

    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i = i + 1
            # Swap arr[i] and arr[j]
            arr[i], arr[j] = arr[j], arr[i]

    # Swap the pivot element with the element at i + 1
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high):
    """
    Main deterministic Quicksort function.
    """
    if low < high:
        # pi is the partitioning index, arr[pi] is now in the correct position
        pi = partition(arr, low, high)

        # Separately sort elements before partition and after partition
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

# --- 3. RANDOMIZED QUICKSORT IMPLEMENTATION ---

def randomized_partition(arr, low, high):
    """
    Randomized Partition: Selects a random element as pivot, swaps it
    with the last element, and then calls the standard partition.
    """
    # Generate a random index between low and high (inclusive)
    random_idx = random.randint(low, high)

    # Swap the chosen random element with the last element
    arr[random_idx], arr[high] = arr[high], arr[random_idx]

    # Now, use the standard partition function (which uses the last element as pivot)
    return partition(arr, low, high)

def randomized_quicksort(arr, low, high):
    """
    Main randomized Quicksort function.
    """
    if low < high:
        # pi is the partitioning index, arr[pi] is now in the correct position
        pi = randomized_partition(arr, low, high)

        # Recursively sort sub-arrays
        randomized_quicksort(arr, low, pi - 1)
        randomized_quicksort(arr, pi + 1, high)

# --- 4. EMPIRICAL ANALYSIS FUNCTIONS ---

def generate_test_arrays(n):
    """Generates test arrays for empirical analysis."""
    # Random Array
    random_array = [random.randint(0, n) for _ in range(n)]

    # Already Sorted Array (Worst Case for Deterministic)
    sorted_array = list(range(n))

    # Reverse Sorted Array (Also Worst Case for Deterministic)
    reverse_sorted_array = list(range(n, 0, -1))

    return {
        "Random Data": random_array,
        "Sorted Data": sorted_array,
        "Reverse Sorted Data": reverse_sorted_array
    }

def measure_time(sort_func, arr_original):
    """Measures the running time of a sorting function on a copy of the array."""
    # Create a deep copy to ensure the original array is not modified across tests
    arr = copy.deepcopy(arr_original)
    
    start_time = time.time()
    
    # Call the sorting function
    sort_func(arr, 0, len(arr) - 1)
    
    end_time = time.time()
    
    return (end_time - start_time) * 1000 # Return time in milliseconds (ms)

def run_empirical_analysis(sizes, num_trials=3):
    """
    Runs and prints the empirical time comparison between deterministic and randomized Quicksort.
    """
    print("\n--- Empirical Performance Comparison (Time in milliseconds) ---")
    print(f"| Input Size (n) | Data Type | Deterministic QS (avg) | Randomized QS (avg) |")
    print(f"|----------------|-----------|------------------------|---------------------|")

    for n in sizes:
        # Generate the test arrays for this size
        test_arrays = generate_test_arrays(n)

        for data_type, original_arr in test_arrays.items():
            
            # --- Measure Deterministic Quicksort ---
            det_times = []
            for _ in range(num_trials):
                det_times.append(measure_time(quicksort, original_arr))
            det_avg = sum(det_times) / num_trials

            # --- Measure Randomized Quicksort ---
            rand_times = []
            for _ in range(num_trials):
                rand_times.append(measure_time(randomized_quicksort, original_arr))
            rand_avg = sum(rand_times) / num_trials

            # Print results for the current size and data type
            print(f"| {n:<14} | {data_type:<9} | {det_avg:>20.4f} | {rand_avg:>17.4f} |")

# --- MAIN EXECUTION BLOCK ---

if __name__ == "__main__":
    # Define input sizes to test. Start smaller, scale up to demonstrate O(n^2) vs O(n log n)
    # Note: For sorted/reverse-sorted data, deterministic QS will be very fast for small n, 
    # but the time difference will dramatically increase as n grows.
    test_sizes = [5000, 10000, 20000, 40000]

    # Run the analysis
    run_empirical_analysis(test_sizes)

    # Example of a quick test to ensure correctness
    print("\n--- Correctness Test (n=10) ---")
    test_arr = [10, 7, 8, 9, 1, 5, 4, 3, 2, 6]
    test_arr_rand = copy.deepcopy(test_arr)
    
    quicksort(test_arr, 0, len(test_arr) - 1)
    print(f"Deterministic QS Result: {test_arr}")

    randomized_quicksort(test_arr_rand, 0, len(test_arr_rand) - 1)
    print(f"Randomized QS Result: {test_arr_rand}")
