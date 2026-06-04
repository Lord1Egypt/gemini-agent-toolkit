---
name: regular-expressions
description: Designing, parsing, and searching string parameters using Python regular expressions.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Regular Expressions

## Overview
Regular Expressions (Regex) define search patterns to extract or validate matching parts of texts.

## When to Use This Skill
Use to extract emails, parse URLs, clean user inputs, or extract variables from raw HTML.

## Quick Start (with runnable code examples)

```python
import re

text = "Find me at akim.221992@gmail.com and also lordegypt@github.com"
# Extract all email patterns
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
print("Emails found:", emails)
```

## Advanced Usage
Design complex regex configurations with named lookarounds, non-capturing groups, and multi-line flag patterns.

## Key References
- [Python re module documentation](https://docs.python.org/3/library/re.html)

## Dependencies
- Python Standard Library
