#!/usr/bin/env bash
set -euo pipefail

# Change into the repository root so relative paths resolve consistently.
cd "$(cd "$(dirname "$0")" && pwd)/.."

# pytest is baked into the environment image (environment/Dockerfile).
pytest tests/test_outputs.py -rA --ctrf=./ctrf.json
RESULT=$?

mkdir -p /app
if [ "$RESULT" -eq 0 ]; then
  echo 1 > /app/reward.txt
else
  echo 0 > /app/reward.txt
fi

exit "$RESULT"
