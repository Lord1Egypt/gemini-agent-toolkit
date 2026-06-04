---
name: linux-bash-scripting
description: Writing automation scripts, file directory operations, and loop controls in Linux Bash shell.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Linux Bash Scripting

## Overview
Bash is a Unix shell and command language that automates command sequences.

## When to Use This Skill
Use to automate local directory backups, deployment cycles, dependency setups, and batch actions.

## Quick Start (with runnable code examples)

```python
#!/bin/bash
# Loop through all files in a folder and list names
for file in /home/lordegypt/TelegramBOTS/*; do
    if [ -d "$file" ]; then
        echo "Bot Folder: $(basename "$file")"
    fi
done
```

## Advanced Usage
Manage process exits, write trap commands for code cleanups, parse script flags (`getopts`), and perform stream manipulations (`sed`/`awk`).

## Key References
- [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/)

## Dependencies
- Bash Shell
