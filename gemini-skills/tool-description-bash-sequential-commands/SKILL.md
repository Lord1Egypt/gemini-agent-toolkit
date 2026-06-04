---
name: 'Tool Description: Bash (sequential commands)'
description: Bash tool instruction: chain dependent commands with &&
ccVersion: 2.1.53
variables:
  - BASH_TOOL_NAME
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

If the commands depend on each other and must run sequentially, use a single ${BASH_TOOL_NAME} call with '&&' to chain them together.