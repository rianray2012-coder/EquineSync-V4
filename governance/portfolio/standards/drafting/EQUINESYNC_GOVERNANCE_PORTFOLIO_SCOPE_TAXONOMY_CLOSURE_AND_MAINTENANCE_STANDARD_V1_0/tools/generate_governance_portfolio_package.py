#!/usr/bin/env python3
"""Round 2 generator entrypoint.

Use --write or --regenerate to mutate package files. Use --check for a
strictly read-only drift check.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import round2_package


if __name__ == "__main__":
    raise SystemExit(round2_package.main(sys.argv[1:]))
