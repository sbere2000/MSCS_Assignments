# Bereket Gebremariam
# Optimization Technique and Implementation
# Oct 25, 2025

import numpy as np
import timeit
from collections import namedtuple

# --- Data Size ---
N = 10**6  # 1 million particles

# --- 1. UNOPTIMIZED: Array of Structures (AOS) ---
# Use a namedtuple to simulate a standard Python object/struct
Particle = namedtuple('Particle', ['x', 'y', 'z'])

# Create a list of 1 million Python objects
particles_aos = [
    Particle(x=np.random.rand(), y=np.random.rand(), z=np.random.rand())
    for _ in range(N)
]

def process_aos(data):
    """
    Simulates a memory-bound operation: summing all X-coordinates.
    Requires iterating through a list of scattered objects.
    """
    total_x = 0.0
    for p in data:
        # Accessing p.x involves multiple memory jumps (pointer chasing)
        total_x += p.x
    return total_x

# --- 2. OPTIMIZED: Structure of Arrays (SOA) ---
# Use separate, contiguous NumPy arrays for each field
particles_soa_x = np.array([p.x for p in particles_aos], dtype=np.float64)
particles_soa_y = np.array([p.y for p in particles_aos], dtype=np.float64)
particles_soa_z = np.array([p.z for p in particles_aos], dtype=np.float64)

def process_soa(data_x):
    """
    Simulates the same memory-bound operation.
    Leverages NumPy's contiguous array and vectorization.
    """
    # NumPy sum is implemented in fast, compiled C code and accesses
    # memory contiguously, maximizing cache hits.
    return np.sum(data_x)

# --- Performance Measurement ---
# Number of runs to average
runs = 5

time_aos = timeit.timeit(lambda: process_aos(particles_aos), number=runs) / runs
time_soa = timeit.timeit(lambda: process_soa(particles_soa_x), number=runs) / runs

# --- Results ---
print(f"--- Data Processing for N={N} Particles ---")
print(f"1. AOS (Pure Python): {time_aos:.6f} seconds (Average of {runs} runs)")
print(f"2. SOA (NumPy Optimized): {time_soa:.6f} seconds (Average of {runs} runs)")
print(f"Observed Speedup: {time_aos / time_soa:.2f}X")