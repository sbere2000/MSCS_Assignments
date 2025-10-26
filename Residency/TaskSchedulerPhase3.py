"""
Final Group Project - Core Logic (Heap + Hash Table)
Bereket Gebremariam, Sachin Karki
Satish Penmatsa
2025 Fall - Algorithms and Data Structures (MSCS-532-M80)
University of the Cumberlands – Kentucky

Task Scheduler using a Priority Queue (min-heap) and Hash Table (dict).
"""

import heapq

class Task:
    def __init__(self, task_id, description, deadline, urgency):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.urgency = urgency

    def __str__(self):
        return f"ID: {self.task_id}, Desc: {self.description}, Due: {self.deadline}, Urg: {self.urgency}"

class TaskScheduler:
    def __init__(self):
        self.tasks = {}  # task_id -> Task
        self.heap = []   # (deadline, -urgency, task_id)

    def add_task(self, task_id, description, deadline, urgency):
        task = Task(task_id, description, deadline, urgency)
        self.tasks[task_id] = task
        heapq.heappush(self.heap, (deadline, -urgency, task_id))

    def get_next_task(self):
        while self.heap and self.heap[0][2] not in self.tasks:
            heapq.heappop(self.heap)
        if not self.heap:
            raise IndexError("No tasks")
        return self.tasks[self.heap[0][2]]

    def complete_task(self):
        while self.heap and self.heap[0][2] not in self.tasks:
            heapq.heappop(self.heap)
        if not self.heap:
            raise IndexError("No tasks")
        _, _, task_id = heapq.heappop(self.heap)
        return self.tasks.pop(task_id)

    def find_task(self, task_id):
        if task_id not in self.tasks:
            raise ValueError("Task not found")
        return self.tasks[task_id]