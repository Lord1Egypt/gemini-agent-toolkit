---
name: 'System Reminder: MCP resource no content'
description: Shown when MCP resource has no content
ccVersion: 2.1.18
variables:
  - ATTACHMENT_OBJECT
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

<mcp-resource server="${ATTACHMENT_OBJECT.server}" uri="${ATTACHMENT_OBJECT.uri}">(No content)</mcp-resource>