---
name: nginx-routing
description: Configuring Nginx reverse proxy routing, load balancers, rate limits, and SSL termination.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Nginx Routing

## Overview
Nginx is a web server that can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.

## When to Use This Skill
Use to expose Flask or Node.js web services securely on a public server behind a proxy.

## Quick Start (with runnable code examples)

```python
# Simple Nginx configuration block (/etc/nginx/sites-available/default)
server {
    listen 80;
    server_name my-app.domain;

    location / {
        proxy_pass http://127.0.0.1:5000; # Route to local Flask process
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Advanced Usage
Set up SSL encryption via Certbot, configure gzip response compression, and customize upstream load balancing.

## Key References
- [Nginx Official documentation](https://nginx.org/en/docs/)

## Dependencies
- Nginx Web Server
