---
name: pdf-parsing-utils
description: Extracting structured text tables and content blocks from PDF files using PyPDF or pdfplumber.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Pdf Parsing Utils

## Overview
PDF parsing translates visual PDF files into machine-readable text and clean data structures.

## When to Use This Skill
Use to parse text parameters out of uploaded financial statements or text reports.

## Quick Start (with runnable code examples)

```python
import pypdf

def extract_pdf_text(pdf_path):
    reader = pypdf.PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
```

## Advanced Usage
Extract tabular tables using pdfplumber, extract metadata headers, decrypt passwords, and manage page rotations.

## Key References
- [PyPDF Documentation](https://pypdf.readthedocs.io/)

## Dependencies
- pypdf>=3.0.0
