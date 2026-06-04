---
name: redis-caching
description: Distributed key-value caching, session storage, and rate limiting with Upstash or standard Redis.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Redis Caching

## Overview
Redis is an open-source, in-memory data store used as a database, cache, message broker, and queue.

## When to Use This Skill
Use to implement caching, rate limiters, or session persistence across serverless backend instances.

## Quick Start (with runnable code examples)

```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Set and Get cached values
r.set('user:session:100', 'active', ex=3600)
session_status = r.get('user:session:100')
print("Session status:", session_status)
```

## Advanced Usage
Implement Redis transactions, pub/sub pipelines, and complex JSON queries.

## Key References
- [Redis Python Client](https://github.com/redis/redis-py)

## Dependencies
- redis>=5.0.0
