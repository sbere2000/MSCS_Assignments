"""
Final Group Project - Test Class
Bereket Gebremariam, Sachin Karki
Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80) - Full Term
University of the Cumberland – Kentucky

This is the test class which will be used to run the program.
"""

from TaskScheduler_final import TaskScheduler

def demonstrate_task_scheduler():
    scheduler = TaskScheduler()

    # Test Case 1: Add tasks
    print("Test Case 1: Adding tasks")
    # Note: I'm converting the deadline to a string to match the original main.py implementation, 
    # but the test file used a string, so I'll keep it as provided.
    scheduler.add_task(1, "Complete report", "2025-10-28", 2)
    scheduler.add_task(2, "Attend meeting", "2025-10-27", 1) # Highest priority (earliest date)
    scheduler.add_task(3, "Update database", "2025-10-28", 3) # Higher urgency than task 1 for date tie
    print("Tasks added successfully")

    # Test Case 2: Retrieve highest-priority task
    print("\nTest Case 2: Retrieving highest-priority task")
    task = scheduler.get_next_task() # Should be Task 2
    print(f"Highest-priority task: {task}")

    # Test Case 3: Find task by ID
    print("\nTest Case 3: Finding task by ID")
    task = scheduler.find_task(1)
    print(f"Found task: {task}")
    try:
        scheduler.find_task(999)
    except ValueError as e:
        print(f"Error: {e}")

    # Test Case 4: Complete task
    print("\nTest Case 4: Completing tasks")
    while not scheduler.is_empty():
        task = scheduler.complete_task()
        print(f"Completed: {task}")
        # Order should be: Task 2, Task 3, Task 1

    # Test Case 5: Edge case - Empty priority list
    print("\nTest Case 5: Empty priority list handling")
    try:
        scheduler.get_next_task()
    except IndexError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    demonstrate_task_scheduler()