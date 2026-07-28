#!/usr/bin/env python3
"""Package test for CGP-006 Wave 1 activation-readiness planning."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


sys.dont_write_bytecode = True

REPO = Path(__file__).resolve().parents[7]
VALIDATOR = REPO / "governance/implementation/code-guides/drafting/CGP-006/WAVE_1_ACTIVATION_AND_EVIDENCE_PLANNING/validators/validate_activation_readiness_package.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_activation_readiness_package", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load validator module.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_validator()
    result = module.validate(REPO, require_draft_pr=False)
    if result.ok:
        print("cgp006-wave1-activation-readiness-tests: PASS")
        return 0
    print("cgp006-wave1-activation-readiness-tests: FAIL")
    for issue in result.issues:
        print(f"{issue['rule']}: {issue['path']}: {issue['message']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
