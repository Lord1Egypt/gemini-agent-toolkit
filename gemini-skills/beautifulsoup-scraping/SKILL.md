---
name: beautifulsoup-scraping
description: Parsing HTML web structures, searching tags, and extracting text using BeautifulSoup4.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Beautifulsoup Scraping

## Overview
BeautifulSoup parses raw HTML and XML pages, providing intuitive DOM tree search systems.

## When to Use This Skill
Use to parse data out of static web pages or crawled page sources.

## Quick Start (with runnable code examples)

```python
from bs4 import BeautifulSoup
import requests

r = requests.get("https://example.com")
soup = BeautifulSoup(r.content, "html.parser")

# Find the primary heading element
heading = soup.find("h1").text
print("Heading Text:", heading)
```

## Advanced Usage
Search elements using regex patterns, navigate sibling tag nodes, extract attributes, and clean HTML bodies.

## Key References
- [BeautifulSoup4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Dependencies
- beautifulsoup4>=4.12.0, lxml>=4.9.0
