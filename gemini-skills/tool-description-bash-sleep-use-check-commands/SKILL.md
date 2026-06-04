---
name: 'Tool Description: Bash (sleep — use check commands)'
description: Bash tool instruction: use check commands rather than sleeping when polling
ccVersion: 2.1.53
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

If you must poll an external process, use a check command (e.g. `gh run view`) rather than sleeping first.