---
name: playwright-browser
description: Automated headless web browser testing, page interactions, screenshot capture, and web scraping.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Playwright Browser

## Overview
Playwright is a modern framework for Web Testing and Automation, supporting Chromium, Firefox, and WebKit.

## When to Use This Skill
Use to scrape dynamic single-page javascript apps, capture screenshots, or run automated integration tests.

## Quick Start (with runnable code examples)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://github.com/Lord1Egypt")
    print("Page Title:", page.title())
    page.screenshot(path="github_profile.png")
    browser.close()
```

## Advanced Usage
Intercept API network requests, mock geolocation, fill forms, and simulate drag-and-drop actions.

## Key References
- [Playwright Python Docs](https://playwright.dev/python/)

## Dependencies
- playwright>=1.40.0
