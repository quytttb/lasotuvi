#!/bin/bash
# Start LasoTuVi FastAPI server

echo "🚀 Starting LasoTuVi API server..."

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Set PYTHONPATH to include the project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run uvicorn with auto-reload from project root
cd "$SCRIPT_DIR" && uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Alternative: Run with more verbose logging
# uvicorn api.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
