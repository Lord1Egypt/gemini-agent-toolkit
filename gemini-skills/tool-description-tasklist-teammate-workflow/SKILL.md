---
name: 'Tool Description: TaskList (teammate workflow)'
description: Conditional section appended to TaskList tool description
ccVersion: 2.1.38
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

## Teammate Workflow

When working as a teammate:
1. After completing your current task, call TaskList to find available work
2. Look for tasks with status 'pending', no owner, and empty blockedBy
3. **Prefer tasks in ID order** (lowest ID first) when multiple tasks are available, as earlier tasks often set up context for later ones
4. Claim an available task using TaskUpdate (set `owner` to your name), or wait for leader assignment
5. If blocked, focus on unblocking tasks or notify the team lead