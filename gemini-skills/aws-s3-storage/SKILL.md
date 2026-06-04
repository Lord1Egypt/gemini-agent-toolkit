---
name: aws-s3-storage
description: Uploading, downloading, and managing static file assets in Amazon Web Services S3 Buckets using Boto3.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Aws S3 Storage

## Overview
Amazon S3 (Simple Storage Service) is an object storage service offering industry-leading scalability, data availability, security, and performance.

## When to Use This Skill
Use to store persistent user media assets, database backups, or generated PDFs securely.

## Quick Start (with runnable code examples)

```python
import boto3

s3 = boto3.client('s3')

def upload_file(file_name, bucket_name):
    # Upload local file
    s3.upload_file(file_name, bucket_name, file_name)
    print(f"Uploaded {file_name} successfully.")
```

## Advanced Usage
Create S3 Presigned URLs for secure temporary user downloads, set up bucket lifecycle policies, and manage ACL access permissions.

## Key References
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## Dependencies
- boto3>=1.28.0
