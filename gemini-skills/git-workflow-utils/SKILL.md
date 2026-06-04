---
name: git-workflow-utils
description: Advanced git operations including branching, commits, merge conflicts, tag creation, and history manipulation.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Git Workflow Utils

## Overview
Git is a distributed version control system designed to handle everything from small to very large projects.

## When to Use This Skill
Use to script workspace updates, pull-request hooks, or resolve conflicts automatically in agent loops.

## Quick Start (with runnable code examples)

```python
# Run git commands via subprocess
import subprocess

def git_commit_and_push(message: str):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])
```

## Advanced Usage
Handle interactive rebases, git cherry-pick, merge conflict marker parsing, and submodule management.

## Key References
- [Pro Git Book](https://git-scm.com/book/en/v2)

## Dependencies
- Git CLI
