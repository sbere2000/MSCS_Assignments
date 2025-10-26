"""
Final Group Project - Test Class
Bereket Gebremariam, Sachin Karki
Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80)
University of the Cumberlands – Kentucky

Test suite for TaskScheduler with CLI support and performance metrics.
"""

import argparse
import time
import psutil
import os
import random
import matplotlib.pyplot as plt
from TaskScheduler_final import TaskScheduler

def measure_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024
        return result, (end_time - start_time), (end_memory - start_memory)
    return wrapper

@measure_performance
def run_basic_tests():
    scheduler = TaskScheduler()
    print("Adding basic tasks...")
    scheduler.add_task(1, "Report", "2025-10-28", 2)
    scheduler.add_task(2, "Meeting", "2025-10-27", 1)
    scheduler.add_task(3, "Database", "2025-10-28", 3)

    print("\nNext task:", scheduler.get_next_task())

    print("\nFinding task ID 1:")
    try:
        print(scheduler.find_task(1))
    except ValueError as e:
        print(f"Error: {e}")

    print("\nCompleting tasks:")
    while True:
        try:
            print(scheduler.complete_task())
        except IndexError:
            break
    return "Basic tests completed"

@measure_performance
def run_edge_case_tests():
    scheduler = TaskScheduler()
    print("\nTesting edge cases...")
    try:
        scheduler.add_task(1, "Invalid Deadline", "2025-13-01", 1)
    except ValueError as e:
        print(f"Expected error: {e}")
    try:
        scheduler.add_task(1, "Duplicate ID", "2025-10-28", 1)
        scheduler.add_task(1, "Duplicate ID", "2025-10-29", 2)
    except ValueError as e:
        print(f"Expected error: {e}")
    try:
        scheduler.add_task(2, "Negative Urgency", "2025-10-28", -1)
    except ValueError as e:
        print(f"Expected error: {e}")
    try:
        scheduler.find_task(999)
    except ValueError as e:
        print(f"Expected error: {e}")
    return "Edge case tests completed"

@measure_performance
def run_stress_test(num_tasks):
    scheduler = TaskScheduler()
    print(f"\nStress testing with {num_tasks} tasks...")
    for i in range(num_tasks):
        deadline = f"2025-12-{random.randint(1, 31):02d}"
        scheduler.add_task(i, f"Task {i}", deadline, random.randint(1, 10))
    completed = 0
    while scheduler.heap:
        scheduler.complete_task()
        completed += 1
        if completed % (num_tasks // 10) == 0:
            print(f"Completed {completed} tasks")
    return f"Stress test with {num_tasks} tasks completed"

@measure_performance
def cli_find_task(scheduler, task_id):
    try:
        print(scheduler.find_task(task_id))
    except ValueError as e:
        print(f"Error: {e}")
    return "Find task executed"

def plot_performance(sizes, times, memories, filename="performance.png"):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, marker='o')
    plt.xlabel("Number of Tasks")
    plt.ylabel("Time (s)")
    plt.title("Execution Time vs. Dataset Size")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, memories, marker='o')
    plt.xlabel("Number of Tasks")
    plt.ylabel("Memory Usage (MB)")
    plt.title("Memory Usage vs. Dataset Size")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Performance plot saved as {filename}")

def main():
    parser = argparse.ArgumentParser(description="Task Scheduler CLI")
    subparsers = parser.add_subparsers(dest="command")

    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--task_id", type=int, required=True)
    parser_add.add_argument("--description", type=str, required=True)
    parser_add.add_argument("--deadline", type=str, required=True)
    parser_add.add_argument("--urgency", type=int, required=True)

    parser_find = subparsers.add_parser("find")
    parser_find.add_argument("--task_id", type=int, required=True)

    subparsers.add_parser("next")
    subparsers.add_parser("test")
    subparsers.add_parser("stress")

    args = parser.parse_args()
    scheduler = TaskScheduler()

    if args.command == "add":
        try:
            scheduler.add_task(args.task_id, args.description, args.deadline, args.urgency)
            print(f"Added task: ID={args.task_id}")
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "find":
        cli_find_task(scheduler, args.task_id)
    elif args.command == "next":
        try:
            print(scheduler.get_next_task())
        except IndexError as e:
            print(f"Error: {e}")
    elif args.command == "test":
        result, time_taken, memory_used = run_basic_tests()
        print(f"{result}: Time: {time_taken:.4f}s, Memory: {memory_used:.4f}MB")
        result, time_taken, memory_used = run_edge_case_tests()
        print(f"{result}: Time: {time_taken:.4f}s, Memory: {memory_used:.4f}MB")
    elif args.command == "stress":
        sizes = [100, 1000, 10000]
        times = []
        memories = []
        for size in sizes:
            result, time_taken, memory_used = run_stress_test(size)
            print(f"{result}: Time: {time_taken:.4f}s, Memory: {memory_used:.4f}MB")
            times.append(time_taken)
            memories.append(memory_used)
        plot_performance(sizes, times, memories)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()