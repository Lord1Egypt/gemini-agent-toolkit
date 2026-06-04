---
name: image-optimization
description: Resizing, compressing formats, and applying image filters using Pillow.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Image Optimization

## Overview
Pillow is the friendly PIL fork by Alex Clark and Contributors, providing image processing routines.

## When to Use This Skill
Use to compress static user uploads, resize avatars, or convert images to WebP.

## Quick Start (with runnable code examples)

```python
from PIL import Image

def optimize_img(input_path, output_path):
    img = Image.open(input_path)
    # Compress and convert to WebP
    img.save(output_path, "WEBP", quality=80)
    print("Image compressed successfully.")
```

## Advanced Usage
Generate thumbnails while maintaining aspect ratio, apply blurring filters, extract pixel colors, and build watermarks.

## Key References
- [Pillow Documentation](https://pillow.readthedocs.io/)

## Dependencies
- pillow>=10.0.0
