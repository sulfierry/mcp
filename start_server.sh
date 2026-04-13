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
PYTHON="$VENV_DIR/bin/python3"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create venv if needed
if [[ ! -d "$VENV_DIR" ]]; then
    echo -e "${CYAN}📦 Creating virtual environment...${NC}" >&2
    python3 -m venv "$VENV_DIR"
fi

# Ensure the venv python exists
if [[ ! -x "$PYTHON" ]]; then
    echo -e "${YELLOW}⚠ Venv python not found at $PYTHON${NC}" >&2
    echo -e "${CYAN}Recreating virtual environment...${NC}" >&2
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Install deps only if missing (skip pip entirely when already installed to avoid
# IDE handshake timeout — pip check adds ~2s, import check adds ~0.1s)
if ! "$PYTHON" -c "import fastmcp, yaml" 2>/dev/null; then
    echo -e "${CYAN}📦 Installing dependencies...${NC}" >&2
    "$VENV_DIR/bin/pip" install -q -r "$SCRIPT_DIR/server/requirements.txt" >/dev/null 2>&1 || true
fi

# Parse args
TRANSPORT="stdio"
PORT=8765

if [[ "${1:-}" == "--sse" ]]; then
    TRANSPORT="sse"
    PORT="${2:-8765}"
fi

echo -e "${GREEN}🚀 Starting MCP Skills Server (${TRANSPORT})${NC}" >&2

# Run server using venv python directly (no source activate needed)
cd "$SCRIPT_DIR"
PYTHONPATH="$SCRIPT_DIR/server" exec "$PYTHON" server/mcp_skills_server.py \
    --transport "$TRANSPORT" \
    --port "$PORT"
