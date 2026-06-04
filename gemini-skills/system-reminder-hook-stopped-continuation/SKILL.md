---
name: 'System Reminder: Hook stopped continuation'
description: Message when a hook stops continuation
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

${ATTACHMENT_OBJECT.hookName} hook stopped continuation: ${ATTACHMENT_OBJECT.message}