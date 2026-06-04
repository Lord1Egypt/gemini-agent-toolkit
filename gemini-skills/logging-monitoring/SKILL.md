---
name: logging-monitoring
description: Configuring Python logging library, formatting streams, and managing rotating logs.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Logging Monitoring

## Overview
Logging provides diagnostic tracking systems in software, helping debug runtime issues without cluttering stdout.

## When to Use This Skill
Use to log request statuses, background operations, and track crashes systematically inside files.

## Quick Start (with runnable code examples)

```python
import logging
from logging.handlers import RotatingFileHandler

# Set up log formatter
log_fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set up rotating log files (max 1MB, keeping 3 backups)
handler = RotatingFileHandler("app.log", maxBytes=1000000, backupCount=3)
handler.setFormatter(log_fmt)

logger = logging.getLogger("AppLogger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.info("Application successfully initialized.")
```

## Advanced Usage
Set up multi-logger inheritance tree, log exception traces automatically using `logger.exception()`, and configure central diagnostic systems.

## Key References
- [Python logging documentation](https://docs.python.org/3/library/logging.html)

## Dependencies
- Python Standard Library
