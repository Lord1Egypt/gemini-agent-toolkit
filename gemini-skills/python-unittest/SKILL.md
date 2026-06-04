---
name: python-unittest
description: Writing test cases, assertions, mocking API calls, and running test runner pipelines using unittest.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Python Unittest

## Overview
unittest is the built-in testing framework in Python, offering clean class-based test configurations.

## When to Use This Skill
Use to create unit tests and verify the logic correctness of your code modules.

## Quick Start (with runnable code examples)

```python
import unittest

def add_values(x, y):
    return x + y

class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add_values(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
```

## Advanced Usage
Configure test fixtures (`setUp`/`tearDown`), mock external requests using `unittest.mock.patch`, and assert custom errors.

## Key References
- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)

## Dependencies
- Python Standard Library
