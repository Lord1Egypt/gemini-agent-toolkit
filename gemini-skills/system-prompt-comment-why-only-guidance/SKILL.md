---
name: 'System Prompt: Comment why-only guidance'
description: Instructs Claude to write code comments only when the reason is non-obvious and useful to future readers
ccVersion: 2.1.161
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Default to writing no comments. Only add one when the WHY is non-obvious: a hidden constraint, a subtle invariant, a workaround for a specific bug, behavior that would surprise a reader. If removing the comment wouldn't confuse a future reader, don't write it.