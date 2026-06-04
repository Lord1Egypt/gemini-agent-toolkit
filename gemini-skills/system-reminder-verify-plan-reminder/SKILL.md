---
name: 'System Reminder: Verify plan reminder'
description: Reminder to verify completed plan
ccVersion: 2.1.18
variables:
  - TASK_TOOL_NAME
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

You have completed implementing the plan. Please call the "" tool directly (NOT the ${TASK_TOOL_NAME} tool or an agent) to verify that all plan items were completed correctly.