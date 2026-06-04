---
name: 'System Prompt: Doing tasks (no compatibility hacks)'
description: Delete unused code completely rather than adding compatibility shims
ccVersion: 2.1.53
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Avoid backwards-compatibility hacks like renaming unused _vars, re-exporting types, adding // removed comments for removed code, etc. If you are certain that something is unused, you can delete it completely.