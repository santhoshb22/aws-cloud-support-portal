#!/usr/bin/env bash
# Minimal user-space launcher for an already-cloned project on Linux.
# Run from the repository root. This script does not create AWS resources.
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install it using your OS package manager." >&2
  exit 1
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

export APP_ENV="${APP_ENV:-local}"
export AWS_REGION="${AWS_REGION:-ap-south-1}"
export PORT="${PORT:-5000}"

echo "Starting Cloud Support Portal on port ${PORT} (APP_ENV=${APP_ENV})"
exec gunicorn --bind "0.0.0.0:${PORT}" --workers 2 --access-logfile - --error-logfile - app:app
