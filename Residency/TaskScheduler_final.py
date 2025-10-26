"""
Final Group Project - Core Logic (Heap + Hash Table)
Bereket Gebremariam, Sachin Karki
Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80) - Full Term
University of the Cumberlands – Kentucky

This is the main class with Priority Queue and Hash Table Implementation.
"""

import heapq

class Task:
    """Represents a single task with its attributes."""
    def __init__(self, task_id, description, deadline, urgency):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline  # ISO string "YYYY-MM-DD" works lexicographically
        self.urgency = urgency

    def __str__(self):
        return (
            f"Task ID: {self.task_id}, Description: {self.description}, "
            f"Deadline: {self.deadline}, Urgency: {self.urgency}"
        )


class TaskScheduler:
    """
    Task Scheduler using:
    - Hash Table (dict) for O(1) task metadata access by task_id
    - Priority Queue (min-heap) for O(log n) prioritization by (deadline, -urgency, task_id)

    Priority rule:
      1) Earliest deadline first
      2) If tie, higher urgency first
      3) If tie, lower task_id first (to stabilize ordering)
    """

    def __init__(self):
        self.tasks = {}   # task_id -> Task
        self.heap = []    # list of tuples: (deadline, -urgency, task_id)

    def _push(self, task):
        """Push a task's priority key into the heap."""
        heapq.heappush(self.heap, (task.deadline, -task.urgency, task.task_id))

    def _purge_stale(self):
        """
        Remove heap entries that refer to tasks no longer present in self.tasks.
        Returns the top valid heap entry or None if heap has no valid entries.
        """
        while self.heap:
            deadline, neg_urgency, task_id = self.heap[0]
            if task_id in self.tasks:
                return (deadline, neg_urgency, task_id)
            # Stale entry—pop and continue
            heapq.heappop(self.heap)
        return None

    def add_task(self, task_id, description, deadline, urgency):
        """Add a task to both the dict and the heap. O(1) dict + O(log n) heap."""
        if task_id in self.tasks:
            raise ValueError(f"Task ID {task_id} already exists")
        task = Task(task_id, description, deadline, urgency)
        self.tasks[task_id] = task
        self._push(task)

    def get_next_task(self):
        """
        Peek the highest-priority task without removing it.
        O(1) amortized after purging stale entries.
        """
        top = self._purge_stale()
        if top is None:
            raise IndexError("No tasks available")
        _, _, task_id = top
        return self.tasks[task_id]

    def complete_task(self):
        """
        Remove and return the highest-priority task.
        O(log n) due to heap pop, with lazy deletion handling.
        """
        top = self._purge_stale()
        if top is None:
            raise IndexError("No tasks available")
        heapq.heappop(self.heap)  # remove the valid top
        _, _, task_id = top
        task = self.tasks.pop(task_id)  # O(1) dict deletion
        return task

    def find_task(self, task_id):
        """Retrieve a task by ID. O(1)."""
        if task_id not in self.tasks:
            raise ValueError(f"Task ID {task_id} not found")
        return self.tasks[task_id]

    def is_empty(self):
        """
        True if there are no tasks left (ignores stale heap entries).
        """
        # Quick check: if dict is empty, we are empty.
        if not self.tasks:
            return True
        # Otherwise check if any valid heap entry exists.
        return self._purge_stale() is None