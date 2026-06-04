---
name: mongodb-db
description: Connecting, querying, updating, and aggregating document-based records in MongoDB.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Mongodb Db

## Overview
MongoDB is a source-available cross-platform document-oriented database program classified as a NoSQL database.

## When to Use This Skill
Use when storing unstructured or dynamic JSON-like records that require complex nested schemas.

## Quick Start (with runnable code examples)

```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.test_database
collection = db.test_collection

# Insert and find
post_id = collection.insert_one({"author": "Lord1Egypt", "text": "Post text"}).inserted_id
print("Inserted ID:", post_id)
print(collection.find_one({"author": "Lord1Egypt"}))
```

## Advanced Usage
Execute aggregation pipelines, manage document indexing, and handle connection pool timeouts.

## Key References
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

## Dependencies
- pymongo>=4.0.0
