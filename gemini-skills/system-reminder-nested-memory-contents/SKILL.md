---
name: 'System Reminder: Nested memory contents'
description: Contents of a nested memory file
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Contents of ${ATTACHMENT_OBJECT.content.path}:

${ATTACHMENT_OBJECT.content.content}