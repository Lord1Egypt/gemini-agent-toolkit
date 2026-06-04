---
name: prisma-orm-db
description: Type-safe database ORM management, migrations, and CRUD operations using Prisma in Node.js or Python.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Prisma Orm Db

## Overview
Prisma is a next-generation ORM for Node.js and TypeScript, now supporting Python bindings.

## When to Use This Skill
Use to write type-safe queries, define structural database schemas, and manage schema migrations.

## Quick Start (with runnable code examples)

```python
# Prisma Schema (schema.prisma example)
# datasource db {
#   provider = "postgresql"
#   url      = env("DATABASE_URL")
# }
# model User {
#   id    Int    @id @default(autoincrement())
#   email String @unique
#   name  String?
# }
```

## Advanced Usage
Configure database relations, execute raw SQL commands, write seeding scripts, and deploy migrations.

## Key References
- [Prisma Official Documentation](https://www.prisma.io/docs)

## Dependencies
- prisma>=5.0.0
