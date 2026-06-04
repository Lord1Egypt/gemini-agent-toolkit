---
name: 'Tool Description: Bash (sandbox — per-command)'
description: Treat each command individually; default to sandbox for future commands
ccVersion: 2.1.53
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Treat each command you execute with `dangerouslyDisableSandbox: true` individually. Even if you have recently run a command with this setting, you should default to running future commands within the sandbox.