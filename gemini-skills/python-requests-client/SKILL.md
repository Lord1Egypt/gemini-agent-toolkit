---
name: python-requests-client
description: Performing synchronous HTTP requests, managing sessions, passing headers, and query parameters using Requests.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Python Requests Client

## Overview
Requests is an elegant and simple HTTP library for Python, built for human beings.

## When to Use This Skill
Use to fetch API resources, query REST endpoints, or post data to webhooks.

## Quick Start (with runnable code examples)

```python
import requests

# Perform a basic request
r = requests.get("https://api.github.com/events")
print(r.status_code)
# Parse JSON directly
data = r.json()
```

## Advanced Usage
Manage session pools (`requests.Session()`), configure connection and read timeouts, handle multipart uploads, and handle SSL certificate validations.

## Key References
- [Requests documentation](https://requests.readthedocs.io/)

## Dependencies
- requests>=2.31.0
