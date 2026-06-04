---
name: cron-scheduling
description: Scheduling recurring scripts, parsing crontab syntax, and implementing scheduled background loops.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Cron Scheduling

## Overview
Cron is a time-based job scheduler in Unix-like computer operating systems.

## When to Use This Skill
Use to configure automation cron triggers, back up databases periodically, or scrape sites daily.

## Quick Start (with runnable code examples)

```python
# crontab format: * * * * * command_to_execute
# Minute Hour DayOfMonth Month DayOfWeek
# Run script every day at midnight:
# 0 0 * * * /usr/bin/python3 /home/lordegypt/script.py
```

## Advanced Usage
Use python APScheduler library to manage cron schedules dynamically inside live server processes.

## Key References
- [Crontab Guru](https://crontab.guru/)

## Dependencies
- None
