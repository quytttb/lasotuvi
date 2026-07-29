#!/bin/bash
# Start LasoTuVi FastAPI server

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -x "$SCRIPT_DIR/.venv/bin/uvicorn" ]]; then
    echo "Missing .venv. Run: python3 -m venv .venv && pip install -e '.[api]'" >&2
    exit 1
fi

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run uvicorn with auto-reload from project root
cd "$SCRIPT_DIR"
exec "$SCRIPT_DIR/.venv/bin/uvicorn" api.main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run with more verbose logging
# uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
