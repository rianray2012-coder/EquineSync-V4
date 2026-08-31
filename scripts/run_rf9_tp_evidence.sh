#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="$REPO_ROOT/backend/.venv/bin/python"

SELECTORS=(
  "backend/tests/test_rf9_trainer_operating_center.py"
  "backend/tests/test_build_next_13g_trainer_intake_shell.py"
  "backend/tests/test_tp3_trainer_client_lesson_owner_summary.py"
)

if [[ ! -x "$PYTHON" ]]; then
  cat >&2 <<EOF
RF9/TP evidence runner requires the project backend virtualenv:
  $PYTHON

Create it from the repository root with:
  python3.12 -m venv backend/.venv
  backend/.venv/bin/python -m pip install -r backend/requirements.txt
  backend/.venv/bin/python -m pip install -r backend/requirements-dev.txt
EOF
  exit 2
fi

cd "$REPO_ROOT"

echo "RF9/TP evidence interpreter: $PYTHON"
echo "Collecting RF9/TP selected suite..."
"$PYTHON" -m pytest --collect-only -q "${SELECTORS[@]}"

echo
echo "Running RF9/TP selected suite..."
"$PYTHON" -m pytest -q "${SELECTORS[@]}"
