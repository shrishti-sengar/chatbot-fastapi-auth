#!/usr/bin/env bash
set -e

echo "Running DB init..."
python -m app.init_db

# exec the container CMD (this replaces the shell process)
exec "$@"
