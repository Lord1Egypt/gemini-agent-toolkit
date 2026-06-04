---
name: sqlite-database
description: Querying, migrating, and writing relational tables inside embedded SQLite databases.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Sqlite Database

## Overview
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.

## When to Use This Skill
Use for lightweight, zero-configuration local file databases in Python scripts or small servers.

## Quick Start (with runnable code examples)

```python
import sqlite3

# Connect to local database file (or :memory:)
conn = sqlite3.connect("local_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO users (name) VALUES ('Lord1Egypt')")
conn.commit()

# Query table
cursor.execute("SELECT * FROM users")
print(cursor.fetchall())
conn.close()
```

## Advanced Usage
Perform transactional rollbacks, write triggers, use context managers, and execute vacuum operations.

## Key References
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)

## Dependencies
- Python Standard Library
