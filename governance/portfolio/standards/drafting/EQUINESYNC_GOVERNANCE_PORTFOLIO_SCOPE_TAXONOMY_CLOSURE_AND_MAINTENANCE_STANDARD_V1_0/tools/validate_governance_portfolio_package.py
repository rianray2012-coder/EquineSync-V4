#!/usr/bin/env python3
"""Round 2 validator entrypoint."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import round2_package


if __name__ == "__main__":
    if "--package-dir" in sys.argv:
        idx = sys.argv.index("--package-dir")
        if idx + 1 < len(sys.argv):
            round2_package.PACKAGE_DIR = Path(sys.argv[idx + 1]).resolve()
    raise SystemExit(round2_package.validate_package(round2_package.PACKAGE_DIR))
