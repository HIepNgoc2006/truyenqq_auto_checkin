#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p logs
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.browsers"
export XDG_CACHE_HOME="$PWD/.cache"
set -a
source .env
set +a
flock -n .lock .venv/bin/python main.py >> "logs/checkin-$(date +%F).log" 2>&1
