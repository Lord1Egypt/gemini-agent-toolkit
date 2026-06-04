---
name: security-headers
description: Implementing Content Security Policy (CSP), CORS, and essential security headers in web server responses.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Security Headers

## Overview
Security headers instruct browsers how to handle scripts, requests, and sandboxing features of your site, defending against XSS and Clickjacking.

## When to Use This Skill
Use in Flask, Express, or Next.js to secure public web pages and prevent scripting attacks.

## Quick Start (with runnable code examples)

```python
from flask import Flask, make_response

app = Flask(__name__)

@app.route("/")
def home():
    r = make_response("Secure Webpage")
    # Prevent clickjacking
    r.headers["X-Frame-Options"] = "DENY"
    # Block XSS sniffing
    r.headers["X-Content-Type-Options"] = "nosniff"
    # Control referral leakages
    r.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return r
```

## Advanced Usage
Formulate strict Content Security Policies (CSP) with script nonces, HSTS max-age, and CORS preflight routing.

## Key References
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

## Dependencies
- Flask>=3.0.0
