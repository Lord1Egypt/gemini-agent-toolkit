---
name: 'Agent Prompt: /rename auto-generate session name'
description: Prompt used by /rename (no args) to auto-generate a kebab-case session name from conversation context
ccVersion: 2.1.147
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Generate a short kebab-case name (2-4 words) that captures the main topic of this conversation. Use lowercase words separated by hyphens. Examples: "fix-login-bug", "add-auth-feature", "refactor-api-client", "debug-test-failures". Return JSON with a "name" field.