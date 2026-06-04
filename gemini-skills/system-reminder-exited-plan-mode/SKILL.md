---
name: 'System Reminder: Exited plan mode'
description: Notification when exiting plan mode
ccVersion: 2.1.105
variables:
  - CONDITIONAL_NOTE
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

## Exited Plan Mode

You have exited plan mode. You can now make edits, run tools, and take actions.${CONDITIONAL_NOTE}