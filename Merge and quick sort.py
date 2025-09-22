import time
import sys
import random
import psutil

# Increase recursion limit for deep recursive calls
sys.setrecursionlimit(2000)

# --- MERGE SORT IMPLEMENTATION ---
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# --- QUICK SORT IMPLEMENTATION ---
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    
    pivot = arr[mid]
    arr[mid], arr[high] = arr[high], arr[mid]

    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# --- PERFORMANCE TESTING AND ANALYSIS ---
def get_memory_usage():
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)  # in MB

def run_tests(size):
    # Data Generation
    sorted_data = list(range(size))
    reverse_sorted_data = list(range(size, 0, -1))
    random_data = [random.randint(0, size) for _ in range(size)]
    
    test_data = {
        'Sorted Data': sorted_data.copy(),
        'Reverse Sorted Data': reverse_sorted_data.copy(),
        'Random Data': random_data.copy()
    }
    
    results = {}
    
    for name, data in test_data.items():
        # Test Merge Sort
        data_merge_sort = data.copy()
        start_time = time.perf_counter()
        initial_mem_merge = get_memory_usage()
        merge_sort(data_merge_sort)
        end_time = time.perf_counter()
        final_mem_merge = get_memory_usage()
        
        merge_time = (end_time - start_time) * 1000
        merge_mem = final_mem_merge - initial_mem_merge

        # Test Quick Sort
        data_quick_sort = data.copy()
        start_time = time.perf_counter()
        initial_mem_quick = get_memory_usage()
        quick_sort(data_quick_sort, 0, len(data_quick_sort) - 1)
        end_time = time.perf_counter()
        final_mem_quick = get_memory_usage()

        quick_time = (end_time - start_time) * 1000
        quick_mem = final_mem_quick - initial_mem_quick

        results[name] = {
            'Merge Sort': {'time (ms)': merge_time, 'memory (MB)': merge_mem},
            'Quick Sort': {'time (ms)': quick_time, 'memory (MB)': quick_mem}
        }
    
    return results

# Main execution block
if __name__ == "__main__":
    n = 100000  # Size of the dataset
    print(f"--- Running performance tests with a dataset size of n = {n} ---")
    performance_metrics = run_tests(n)
    
    for dataset, algos in performance_metrics.items():
        print(f"\n--- Results for {dataset} ---")
        for algo, metrics in algos.items():
            print(f"  {algo}:")
            print(f"    Execution Time: {metrics['time (ms)']:.2f} ms")
            print(f"    Memory Usage: {metrics['memory (MB)']:.2f} MB")