---
name: pydantic-settings
description: Managing environment variables, validating system configurations, and parsing .env configurations using Pydantic Settings.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Pydantic Settings

## Overview
Pydantic Settings provides configuration management using Pydantic models, automatically parsing environment vars.

## When to Use This Skill
Use to load and enforce system configuration parameters strictly inside backend servers.

## Quick Start (with runnable code examples)

```python
from pydantic_settings import BaseSettings

class ServerSettings(BaseSettings):
    bot_token: str
    db_port: int = 5432
    
    class Config:
        env_file = ".env"

# Auto-loads from system variables or .env
settings = ServerSettings()
print("Port:", settings.db_port)
```

## Advanced Usage
Implement nested configuration schemas, validate settings values, and handle variable overrides during unit testing runs.

## Key References
- [Pydantic Settings Docs](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

## Dependencies
- pydantic-settings>=2.0.0
