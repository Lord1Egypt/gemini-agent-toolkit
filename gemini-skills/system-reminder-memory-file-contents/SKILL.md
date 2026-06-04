---
name: 'System Reminder: Memory file contents'
description: Contents of a memory file by path
ccVersion: 2.1.79
variables:
  - MEMORY_ITEM
  - MEMORY_TYPE_DESCRIPTION
  - MEMORY_CONTENT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Contents of ${MEMORY_ITEM.path}${MEMORY_TYPE_DESCRIPTION}:

${MEMORY_CONTENT}