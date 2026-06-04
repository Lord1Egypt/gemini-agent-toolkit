---
name: cryptography-api
description: Symmetric/asymmetric encryption, hashing, password salting, and message verification via cryptography library.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Cryptography Api

## Overview
Cryptography is a package which provides cryptographic recipes and primitives to Python developers.

## When to Use This Skill
Use to secure sensitive passwords, encrypt files, or verify integrity signatures locally.

## Quick Start (with runnable code examples)

```python
from cryptography.fernet import Fernet

# Generate key and encrypt
key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"Secret payload message")
print("Encrypted:", token)

# Decrypt
decrypted = f.decrypt(token)
print("Decrypted:", decrypted)
```

## Advanced Usage
Implement RSA public/private key pairs, PBKDF2 password derivation hashing, and AES-GCM primitives.

## Key References
- [Cryptography Docs](https://cryptography.io/)

## Dependencies
- cryptography>=41.0.0
