---
name: 'System Reminder: File opened in IDE'
description: Notification that user opened a file in IDE
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

The user opened the file ${ATTACHMENT_OBJECT.filename} in the IDE. This may or may not be related to the current task.