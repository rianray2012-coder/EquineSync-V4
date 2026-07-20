#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PY="$ROOT/stage2a/.venv/bin/python"
test -x "$PY"
cd "$ROOT/stage2a"
"$PY" -m unittest discover -s tests -p 'test_*.py'
exec env -i \
  PATH="$PATH" \
  TMPDIR="${TMPDIR:-/tmp}" \
  LANG="${LANG:-C.UTF-8}" \
  LC_ALL="${LC_ALL:-C.UTF-8}" \
  sandbox-exec -f config/loopback-only.sb "$PY" validate_foundation.py
