---
name: semantic-versioning
description: Configuring release versions, package numbering schemes, and tracking dependency compatibilities.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Semantic Versioning

## Overview
Semantic Versioning (SemVer) enforces version numbers based on a MAJOR.MINOR.PATCH structure.

## When to Use This Skill
Use to manage package tag updates and coordinate dependency updates across python requirements.

## Quick Start (with runnable code examples)

```python
# SemVer layout:
# MAJOR version for incompatible API changes
# MINOR version for adding backward-compatible functionality
# PATCH version for backward-compatible bug fixes
# Example: 2.1.4 -> Next minor change -> 2.2.0
```

## Advanced Usage
Script automation hooks to auto-increment package versions using git tags or package manifests.

## Key References
- [Semantic Versioning 2.0.0](https://semver.org/)

## Dependencies
- None
