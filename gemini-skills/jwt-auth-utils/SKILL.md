---
name: jwt-auth-utils
description: Generating, signing, and validating JSON Web Tokens (JWT) for secure REST APIs and user sessions.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Jwt Auth Utils

## Overview
JWT is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties.

## When to Use This Skill
Use to implement token-based session validation in stateless web APIs.

## Quick Start (with runnable code examples)

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super-secret"

# Create a token
payload = {"user_id": 5814716109, "exp": datetime.now(timezone.utc) + timedelta(hours=1)}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Token:", token)

# Decode a token
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print("Decoded User ID:", decoded["user_id"])
```

## Advanced Usage
Manage token expiration exceptions, refresh token rotation, and RS256 asymmetric signatures.

## Key References
- [PyJWT documentation](https://pyjwt.readthedocs.io/)

## Dependencies
- PyJWT>=2.8.0
