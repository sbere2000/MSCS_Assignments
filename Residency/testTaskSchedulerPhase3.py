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
from TaskScheduler_final import TaskScheduler


def measure_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = process.memory_info().rss / 1024 / 1024
        print(f"Time: {(end_time - start_time):.4f}s, Memory: {end_memory - start_memory:.4f}MB")
        return result

    return wrapper


@measure_performance
def run_tests():
    scheduler = TaskScheduler()
    print("Adding tasks...")
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


@measure_performance
def cli_find_task(scheduler, task_id):
    try:
        print(scheduler.find_task(task_id))
    except ValueError as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser()
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

    args = parser.parse_args()
    scheduler = TaskScheduler()

    if args.command == "add":
        scheduler.add_task(args.task_id, args.description, args.deadline, args.urgency)
        print(f"Added task: ID={args.task_id}")
    elif args.command == "find":
        cli_find_task(scheduler, args.task_id)
    elif args.command == "next":
        try:
            print(scheduler.get_next_task())
        except IndexError as e:
            print(f"Error: {e}")
    elif args.command == "test":
        run_tests()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()