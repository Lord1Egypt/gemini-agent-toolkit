---
name: prometheus-metrics
description: Instrumenting system diagnostics, counting requests, and exporting metrics to Prometheus monitoring systems.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Prometheus Metrics

## Overview
Prometheus is a free software ecosystem for monitoring and alerting, relying on pull-based timeseries ingestion.

## When to Use This Skill
Use to track system loads, latency distributions, and error rates of running web applications.

## Quick Start (with runnable code examples)

```python
from prometheus_client import start_http_server, Counter
import time

# Create a metric to track requests
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

def process_request():
    REQUESTS.inc()

if __name__ == '__main__':
    # Start exporter server on port 8000
    start_http_server(8000)
    while True:
        process_request()
        time.sleep(1)
```

## Advanced Usage
Set up gauge metrics, summary latency buckets, custom registry setups, and alerting rules configuration.

## Key References
- [Prometheus Python Client](https://github.com/prometheus/client_python)

## Dependencies
- prometheus-client>=0.17.0
