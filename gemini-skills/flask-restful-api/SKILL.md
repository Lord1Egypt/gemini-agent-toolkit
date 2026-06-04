---
name: flask-restful-api
description: Structuring clean, resource-based HTTP REST endpoints using Flask and Flask-RESTful routing.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Flask Restful Api

## Overview
Flask-RESTful is an extension for Flask that adds support for quickly building REST APIs.

## When to Use This Skill
Use to build multi-endpoint, structured web interfaces with clean Python class routing.

## Quick Start (with runnable code examples)

```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
```

## Advanced Usage
Integrate argument parser (reqparse), custom field marshals, and JWT validation middlewares.

## Key References
- [Flask-RESTful Docs](https://flask-restful.readthedocs.io/)

## Dependencies
- Flask-RESTful>=0.3.10
