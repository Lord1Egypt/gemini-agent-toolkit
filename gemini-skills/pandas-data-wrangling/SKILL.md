---
name: pandas-data-wrangling
description: Cleaning, filtering, merging, and aggregating massive tabular data structures using Pandas.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Pandas Data Wrangling

## Overview
Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool.

## When to Use This Skill
Use to clean messy data files, calculate data summaries, or handle tabular outputs in python tasks.

## Quick Start (with runnable code examples)

```python
import pandas as pd

# Load dataset
df = pd.DataFrame({"Name": ["Akim", "Lord"], "Score": [95, 98]})
# Filter and output
high_scores = df[df["Score"] > 96]
print(high_scores)
```

## Advanced Usage
Implement groupby pivot queries, merge databases, handle missing nan values, and export files to Excel sheets.

## Key References
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## Dependencies
- pandas>=2.0.0
