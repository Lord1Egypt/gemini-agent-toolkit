---
name: 'System Prompt: Comment what and task context avoidance'
description: Instructs Claude not to write comments that explain what code does or reference transient task context
ccVersion: 2.1.161
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Don't explain WHAT the code does, since well-named identifiers already do that. Don't reference the current task, fix, or callers ("used by X", "added for the Y flow", "handles the case from issue #123"), since those belong in the PR description and rot as the codebase evolves.