#!/bin/bash
# Quiet wrapper for mcp-remote to hide transport fallback warnings from Antigravity
/home/leon/.nvm/versions/node/v20.19.4/bin/mcp-remote "http://localhost:8765/sse" 2>/dev/null
