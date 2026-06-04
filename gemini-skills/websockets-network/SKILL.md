---
name: websockets-network
description: Asynchronous bi-directional WebSocket client and server configuration in Python.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Websockets Network

## Overview
WebSockets enable two-way interactive communication sessions between the user's browser and a server.

## When to Use This Skill
Use for live chats, real-time tickers, dashboard streaming, or prompt monitoring terminals.

## Quick Start (with runnable code examples)

```python
import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

# To execute: asyncio.run(main())
```

## Advanced Usage
Handle WebSocket ping-pong keepalives, custom header handshakes, and event connection retries.

## Key References
- [WebSockets documentation](https://websockets.readthedocs.io/)

## Dependencies
- websockets>=12.0.0
