---
name: 'System Reminder: USD budget'
description: Current USD budget statistics
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

USD budget: $${ATTACHMENT_OBJECT.used}/$${ATTACHMENT_OBJECT.total}; $${ATTACHMENT_OBJECT.remaining} remaining