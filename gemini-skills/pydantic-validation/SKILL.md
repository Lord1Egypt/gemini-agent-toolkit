---
name: pydantic-validation
description: Data validation, data parsing, configuration management, and type coercion using Pydantic.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Pydantic Validation

## Overview
Pydantic is the most widely used data validation library for Python, enforcing type hints at runtime.

## When to Use This Skill
Use to validate configuration files, API payloads, or parse outputs from AI agents.

## Quick Start (with runnable code examples)

```python
from pydantic import BaseModel, Field, EmailStr

class UserProfile(BaseModel):
    id: int
    name: str = Field(min_length=2)
    email: EmailStr
    is_active: bool = True

user = UserProfile(id=1, name="Akim", email="akim.221992@gmail.com")
print(user.model_dump())
```

## Advanced Usage
Set up custom validators (`@field_validator`), dynamic model schemas, and base settings management.

## Key References
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Dependencies
- pydantic[email]>=2.0.0
