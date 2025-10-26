"""
Final Group Project - Core Logic (Heap + Hash Table)
Bereket Gebremariam, Sachin Karki
Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80)
University of the Cumberlands – Kentucky

Task Scheduler using a Priority Queue (min-heap) and Hash Table (dict).
"""

import heapq
from datetime import datetime

class Task:
    def __init__(self, task_id, description, deadline, urgency):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline  # Unix timestamp
        self.urgency = urgency
        self.is_deleted = False  # For lazy deletion

    def __str__(self):
        # Convert timestamp back to readable date for display
        return f"ID: {self.task_id}, Desc: {self.description}, Due: {datetime.fromtimestamp(self.deadline).strftime('%Y-%m-%d')}, Urg: {self.urgency}"

class TaskScheduler:
    def __init__(self):
        self.tasks = {}  # task_id -> Task
        self.heap = []   # (deadline, -urgency, task_id)

    def add_task(self, task_id, description, deadline, urgency):
        if task_id in self.tasks:
            raise ValueError("Task ID already exists")
        try:
            timestamp = datetime.strptime(deadline, "%Y-%m-%d").timestamp()
        except ValueError:
            raise ValueError("Invalid deadline format. Use YYYY-MM-DD")
        if urgency < 0:
            raise ValueError("Urgency must be non-negative")
        task = Task(task_id, description, timestamp, urgency)
        self.tasks[task_id] = task
        heapq.heappush(self.heap, (timestamp, -urgency, task_id))

    def get_next_task(self):
        while self.heap:
            timestamp, neg_urgency, task_id = self.heap[0]
            if task_id not in self.tasks or self.tasks[task_id].is_deleted:
                heapq.heappop(self.heap)  # Remove invalid entry
            else:
                return self.tasks[task_id]
        raise IndexError("No tasks available")

    def complete_task(self):
        while self.heap:
            timestamp, neg_urgency, task_id = self.heap[0]
            if task_id not in self.tasks or self.tasks[task_id].is_deleted:
                heapq.heappop(self.heap)  # Remove invalid entry
            else:
                heapq.heappop(self.heap)
                task = self.tasks.pop(task_id)
                return task
        raise IndexError("No tasks available")

    def find_task(self, task_id):
        if task_id not in self.tasks or self.tasks[task_id].is_deleted:
            raise ValueError("Task not found")
        return self.tasks[task_id]

    def update_task(self, task_id, new_deadline=None, new_urgency=None):
        if task_id not in self.tasks or self.tasks[task_id].is_deleted:
            raise ValueError("Task not found")
        task = self.tasks[task_id]
        if new_deadline:
            try:
                task.deadline = datetime.strptime(new_deadline, "%Y-%m-%d").timestamp()
            except ValueError:
                raise ValueError("Invalid deadline format. Use YYYY-MM-DD")
        if new_urgency is not None:
            if new_urgency < 0:
                raise ValueError("Urgency must be non-negative")
            task.urgency = new_urgency
        # Mark old entry as deleted and add new entry
        task.is_deleted = True
        heapq.heappush(self.heap, (task.deadline, -task.urgency, task_id))