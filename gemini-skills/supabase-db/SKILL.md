---
name: supabase-db
description: Interacting with Supabase databases, user authentication, and storage buckets using the Python client.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Supabase Db

## Overview
Supabase is an open-source Firebase alternative providing database, auth, file storage, and real-time listeners.

## When to Use This Skill
Use to quickly store structured relational data in PostgreSQL without maintaining a server.

## Quick Start (with runnable code examples)

```python
from supabase import create_client

url = "https://your-project.supabase.co"
key = "your-anon-key"
supabase = create_client(url, key)

# Insert a row into the profiles table
data = supabase.table("profiles").insert({"username": "Lord1Egypt"}).execute()
print(data.data)
```

## Advanced Usage
Set up row-level security (RLS) policies, storage bucket uploads, and auth flow redirects.

## Key References
- [Supabase Documentation](https://supabase.com/docs)

## Dependencies
- supabase>=2.0.0
