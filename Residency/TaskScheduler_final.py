"""
Final Group Project - Core Logic
Bereket Gebremariam, Sachin Karki, Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80) - Full Term
University of the Cumberland – Kentucky
"""

class Task:
    """Represents a single task with its attributes."""
    def __init__(self, task_id, description, deadline, urgency):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.urgency = urgency

    def __str__(self):
        return f"Task ID: {self.task_id}, Description: {self.description}, Deadline: {self.deadline}, Urgency: {self.urgency}"

    def __lt__(self, other):
        # Comparison logic: earliest deadline first, then highest urgency (descending)
        return (self.deadline, -self.urgency) < (other.deadline, -other.urgency)

class TaskScheduler:
    """
    A Task Scheduler that uses a Hash Table (Python dict) for O(1) task metadata access
    and, ideally, a Priority Queue (Heap) for efficient O(log n) prioritization.
    
    NOTE: The current implementation uses simple O(n log n) list sorting for prioritization 
    instead of a true Priority Queue (Heap).
    """
    def __init__(self):
        # The Hash Table (Python dictionary): Maps task_id (Key) to Task object (Value)
        self.tasks = {}

    def add_task(self, task_id, description, deadline, urgency):
        """Add a task to the scheduler. O(1) Hash Table Insert."""
        if task_id in self.tasks:
            raise ValueError(f"Task ID {task_id} already exists")
        task = Task(task_id, description, deadline, urgency)
        self.tasks[task_id] = task

    def get_next_task(self):
        """Return the highest-priority task. Currently O(n log n) due to sorting."""
        if not self.tasks:
            raise IndexError("No tasks available")
        # Sorts by deadline then urgency
        next_task = sorted(self.tasks.values(), key=lambda x: (x.deadline, -x.urgency))[0]
        return next_task

    def complete_task(self):
        """Remove and return the highest-priority task. O(n log n) total."""
        if not self.tasks:
            raise IndexError("No tasks available")
        next_task = self.get_next_task()
        del self.tasks[next_task.task_id] # O(1) deletion
        return next_task

    def find_task(self, task_id):
        """Retrieve a task by ID. O(1) Hash Table Lookup."""
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
        return self.tasks[task_id]

    def is_empty(self):
        """Checks if the scheduler has any tasks."""
        return len(self.tasks) == 0