---
name: performance-profiling
description: Measuring CPU performance metrics and memory bottlenecks in Python code blocks.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Performance Profiling

## Overview
Profiling calculates statistics of code execution, revealing bottleneck processes.

## When to Use This Skill
Use to analyze slow mathematical scripts, inspect pillow memory footprint, or optimize algorithms.

## Quick Start (with runnable code examples)

```python
import cProfile

def count_primes():
    primes = []
    for num in range(2, 5000):
        if all(num % i != 0 for i in range(2, int(num**0.5) + 1)):
            primes.append(num)
    return len(primes)

# Run profile statistics output
cProfile.run('count_primes()')
```

## Advanced Usage
Use `line_profiler` to trace memory and speed per script line, investigate memory leaks via `tracemalloc`, and generate flamegraphs.

## Key References
- [Python Profiling documentation](https://docs.python.org/3/library/profile.html)

## Dependencies
- Python Standard Library
