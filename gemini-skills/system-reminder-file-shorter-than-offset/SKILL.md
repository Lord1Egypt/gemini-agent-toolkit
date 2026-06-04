---
name: 'System Reminder: File shorter than offset'
description: Warning when file read offset exceeds file length
ccVersion: 2.1.18
variables:
  - RESULT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

<system-reminder>Warning: the file exists but is shorter than the provided offset (${RESULT_OBJECT.file.startLine}). The file has ${RESULT_OBJECT.file.totalLines} lines.</system-reminder>