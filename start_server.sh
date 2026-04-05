#!/usr/bin/env bash
# start_server.sh — One-command launcher for the MCP Skills Server
#
# Usage:
#   ./start_server.sh              # stdio mode (for Claude Desktop / Antigravity)
#   ./start_server.sh --sse        # SSE mode (HTTP on localhost:8765)
#   ./start_server.sh --sse 9000   # SSE mode on custom port
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# Create venv if needed
if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${CYAN}📦 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Activate and install deps
source "$VENV_DIR/bin/activate"
pip install -q -r "$SCRIPT_DIR/server/requirements.txt" 2>/dev/null

# Parse args
TRANSPORT="stdio"
PORT=8765

if [[ "${1:-}" == "--sse" ]]; then
    TRANSPORT="sse"
    PORT="${2:-8765}"
fi

echo -e "${GREEN}🚀 Starting MCP Skills Server (${TRANSPORT})${NC}"

# Run server
cd "$SCRIPT_DIR"
PYTHONPATH="$SCRIPT_DIR/server" python server/mcp_skills_server.py \
    --transport "$TRANSPORT" \
    --port "$PORT"
