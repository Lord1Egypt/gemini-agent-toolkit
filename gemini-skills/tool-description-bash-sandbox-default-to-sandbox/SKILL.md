---
name: 'Tool Description: Bash (sandbox — default to sandbox)'
description: Default to sandbox; only bypass when user asks or evidence of sandbox restriction
ccVersion: 2.1.53
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

You should always default to running commands within the sandbox. Do NOT attempt to set `dangerouslyDisableSandbox: true` unless: