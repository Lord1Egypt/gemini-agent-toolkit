---
name: 'Tool Description: Bash (sandbox — no sensitive paths)'
description: Do not suggest adding sensitive paths to sandbox allowlist
ccVersion: 2.1.53
allowed-tools: Read Write Edit Bash
license: BSD-3-Clause license
metadata:
    skill-author: Lord1Egypt
---

Do not suggest adding sensitive paths like ~/.bashrc, ~/.zshrc, ~/.ssh/*, or credential files to the sandbox allowlist.