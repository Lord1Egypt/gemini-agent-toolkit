---
name: 'System Reminder: Hook success'
description: Success message from a hook
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

${ATTACHMENT_OBJECT.hookName} hook success: ${ATTACHMENT_OBJECT.content}