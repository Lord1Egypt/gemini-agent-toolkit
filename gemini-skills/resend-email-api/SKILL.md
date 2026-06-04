---
name: resend-email-api
description: Sending programmatic, HTML transactional emails with custom domains using Resend.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Resend Email Api

## Overview
Resend is the email service platform for developers, built on React Email schemas and modern API structures.

## When to Use This Skill
Use to send responsive emails with custom styling and tracking analytics from serverless functions.

## Quick Start (with runnable code examples)

```python
import requests

url = "https://api.resend.com/emails"
headers = {"Authorization": "Bearer re_..."}

data = {
    "from": "onboarding@resend.dev",
    "to": "akim.221992@gmail.com",
    "subject": "Hello from Lord1Egypt",
    "html": "<strong>Welcome onboard!</strong>"
}

r = requests.post(url, json=data, headers=headers)
print(r.json())
```

## Advanced Usage
Track email delivery status events via webhook logs, attach pdf attachments, and integrate React Email component layouts.

## Key References
- [Resend API Documentation](https://resend.com/docs)

## Dependencies
- requests>=2.28.0
