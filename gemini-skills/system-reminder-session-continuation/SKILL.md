---
name: 'System Reminder: Session continuation'
description: Notification that session continues from another machine
ccVersion: 2.1.18
variables:
  - GET_CWD_FN
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

This session is being continued from another machine. Application state may have changed. The updated working directory is ${GET_CWD_FN()}