---
name: express-routing
description: Building Express web server endpoints, routing HTTP requests, and configuring server middlewares in Node.js.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Express Routing

## Overview
Express is a minimal and flexible Node.js web application framework that provides a robust set of features for web applications.

## When to Use This Skill
Use to implement REST API backends, route controllers, or static file servers in JavaScript.

## Quick Start (with runnable code examples)

```python
const express = require('express');
const app = express();
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Express' });
});

app.listen(3000);
```

## Advanced Usage
Formulate custom authorization middlewares, configure CORS options, and route handlers using express.Router namespaces.

## Key References
- [Express documentation](https://expressjs.com/)

## Dependencies
- express>=4.18.0
