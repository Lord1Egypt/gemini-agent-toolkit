---
name: email-delivery
description: Routing transactional user emails via SMTP, Resend, or SendGrid APIs in Python.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Email Delivery

## Overview
Email delivery APIs route transactional updates, verify accounts, or send alerts.

## When to Use This Skill
Use to notify users, send diagnostic server crash logs, or confirm actions.

## Quick Start (with runnable code examples)

```python
import smtplib
from email.mime.text import MIMEText

def send_smtp_email(to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "admin@my-app.com"
    msg['To'] = to_addr
    
    # Establish connection
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)
```

## Advanced Usage
Structure HTML layout messages, attach files, configure webhook receipt listeners, and verify domain DNS records (SPF, DKIM, DMARC).

## Key References
- [Python smtplib module](https://docs.python.org/3/library/smtplib.html)

## Dependencies
- Python Standard Library
