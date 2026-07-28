#!/usr/bin/env python3
"""Validate Code Guide activation records.

Version: 1.0.0
Owner: Codex
Inputs: governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv
Reliability state: SHADOW_VALIDATION
Evaluated rules:
- activation register exists and parses;
- every guide row is present;
- every guide remains NOT_ACTIVE;
- every activation scope is FALSE;
- no activation effective date is established;
- validation fails nonzero on missing, malformed, or unsafe records.
Limitations: not a mandatory CI gate; does not authorize guide activation.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


VERSION = "1.0.0"
OWNER = "Codex"
RELIABILITY_STATE = "SHADOW_VALIDATION"
REGISTER_REL = Path("governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv")
GUIDES = {
    "ES-CG-00",
    "ES-CG-01",
    "ES-CG-02",
    "ES-CG-03",
    "ES-CG-04",
    "ES-CG-05",
    "ES-CG-06",
    "ES-CG-07",
    "ES-CG-08",
    "ES-CG-09",
    "ES-CG-10",
    "ES-CG-11",
    "ES-CG-12",
    "ES-CG-13",
}
SCOPES = [
    "PLANNING_REFERENCE",
    "IMPLEMENTATION_CONTROL",
    "PULL_REQUEST_REVIEW",
    "MERGE_GATE",
    "RELEASE_GATE",
    "OPERATIONS_REFERENCE",
]


def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"Missing activation register: {path}")
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError("Activation register has no rows")
    required_columns = {"guide_id", "activation_state", "effective_date", *SCOPES}
    missing_columns = required_columns - set(rows[0])
    if missing_columns:
        raise AssertionError(f"Activation register missing columns: {sorted(missing_columns)}")
    return rows


def validate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    guide_ids = {row.get("guide_id", "") for row in rows}
    missing_guides = sorted(GUIDES - guide_ids)
    extra_guides = sorted(guide_ids - GUIDES)
    if missing_guides or extra_guides:
        raise AssertionError(f"Guide row mismatch missing={missing_guides} extra={extra_guides}")
    results.append({"rule": "all 14 guides present", "status": "PASS"})
    active = [row["guide_id"] for row in rows if row.get("activation_state") != "NOT_ACTIVE"]
    if active:
        raise AssertionError(f"Activation state is not NOT_ACTIVE for: {active}")
    results.append({"rule": "all guides NOT_ACTIVE", "status": "PASS"})
    scope_failures = []
    for row in rows:
        for scope in SCOPES:
            if row.get(scope) != "FALSE":
                scope_failures.append(f"{row.get('guide_id')}:{scope}={row.get(scope)}")
    if scope_failures:
        raise AssertionError(f"Activation scope failures: {scope_failures}")
    results.append({"rule": "all activation scopes FALSE", "status": "PASS"})
    effective_dates = [
        f"{row.get('guide_id')}:{row.get('effective_date')}"
        for row in rows
        if row.get("effective_date") not in {"NONE", "", "NOT_ESTABLISHED"}
    ]
    if effective_dates:
        raise AssertionError(f"Activation effective dates established: {effective_dates}")
    results.append({"rule": "no activation effective date", "status": "PASS"})
    return results


def validate(path: Path | None = None) -> list[dict[str, str]]:
    root = repo_root()
    rows = load_rows(path or (root / REGISTER_REL))
    return validate_rows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--path")
    args = parser.parse_args()
    try:
        results = validate(Path(args.path) if args.path else None)
    except Exception as exc:
        if args.json:
            print(json.dumps({"status": "FAIL", "version": VERSION, "owner": OWNER, "error": str(exc)}))
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    payload = {"status": "PASS", "version": VERSION, "owner": OWNER, "reliability_state": RELIABILITY_STATE, "rules": results}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for item in results:
            print(f"{item['status']} {item['rule']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
