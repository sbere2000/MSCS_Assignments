# Task Scheduler Project
Final Group Project for Algorithms and Data Structures (MSCS-532-M80), Fall 2025  
Bereket Gebremariam, Sachin Karki, 
Satish Penmatsa  
University of the Cumberlands – Kentucky

## Overview
This project implements a task scheduler using a priority queue (min-heap) and hash table. Tasks are prioritized by:
1. Earliest deadline (YYYY-MM-DD string).
2. Higher urgency (integer).
3. Lower task ID (for tie-breaking).

## Files
- `TaskScheduler_final.py`: Core logic with `Task` and `TaskScheduler` classes.
- `test_TaskScheduler.py`: Test script with CLI for adding, finding, and viewing tasks.

## Requirements
- Python 3.x
- `psutil` library (`pip install psutil`)

## Usage
Run the program via command line:

1. **Run Tests** (adds tasks, finds a task, shows next task, completes tasks):
   ```bash
   python test_TaskScheduler.py test