#!/usr/bin/env python3
"""Validate Code Guide activation records for Stage 24 limited activation."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path

VERSION = "1.1.0"
OWNER = "Codex"
RELIABILITY_STATE = "SHADOW_VALIDATION"
REGISTER_REL = Path("governance/implementation/code-guides/registers/GUIDE_ACTIVATION_REGISTER.csv")
ACTIVE_GUIDES = {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"}
ALL_GUIDES = {f"ES-CG-{i:02d}" for i in range(14)}
SCOPES = ["PLANNING_REFERENCE", "IMPLEMENTATION_CONTROL", "PULL_REQUEST_REVIEW", "MERGE_GATE", "RELEASE_GATE", "OPERATIONS_REFERENCE"]
APPROVED_SCOPES = {"PLANNING_REFERENCE", "IMPLEMENTATION_CONTROL", "PULL_REQUEST_REVIEW"}
DEFERRED_SCOPES = {"MERGE_GATE", "RELEASE_GATE", "OPERATIONS_REFERENCE"}
ACTIVE_STATE = "ACTIVE_LIMITED_STAGE_24"
EFFECTIVE_EVENT = "VERIFIED_PROTECTED_MERGE_OF_THE_POST_PR_59_STAGE_24_CUSTODY_PR"
AUTHORITY = "ES-FD-CGP-006-STAGE-24-LIMITED-ACTIVATION-2026-07-30"

def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())

def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise AssertionError(f"Missing activation register: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise AssertionError("Activation register has no rows")
    required = {"guide_id", "guide_version", "activation_state", "effective_date", "authority", *SCOPES}
    missing = required - set(rows[0])
    if missing:
        raise AssertionError(f"Activation register missing columns: {sorted(missing)}")
    return rows

def validate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    guide_ids = {row.get("guide_id", "") for row in rows}
    if guide_ids != ALL_GUIDES:
        raise AssertionError(f"Guide row mismatch missing={sorted(ALL_GUIDES-guide_ids)} extra={sorted(guide_ids-ALL_GUIDES)}")
    results.append({"rule": "all 14 guides present", "status": "PASS"})
    for row in rows:
        guide = row["guide_id"]
        if guide in ACTIVE_GUIDES:
            if row.get("activation_state") != ACTIVE_STATE:
                raise AssertionError(f"{guide} must be {ACTIVE_STATE}")
            if row.get("guide_version") != "1.1.0":
                raise AssertionError(f"{guide} active version must be 1.1.0")
            if row.get("effective_date") != EFFECTIVE_EVENT:
                raise AssertionError(f"{guide} effective event mismatch")
            if row.get("authority") != AUTHORITY:
                raise AssertionError(f"{guide} authority mismatch")
            for scope in APPROVED_SCOPES:
                if row.get(scope) != "TRUE":
                    raise AssertionError(f"{guide}:{scope} must be TRUE")
            for scope in DEFERRED_SCOPES:
                if row.get(scope) != "FALSE":
                    raise AssertionError(f"{guide}:{scope} must remain FALSE")
        else:
            if row.get("activation_state") != "NOT_ACTIVE":
                raise AssertionError(f"{guide} must remain NOT_ACTIVE")
            if row.get("effective_date") not in {"NONE", "", "NOT_ESTABLISHED"}:
                raise AssertionError(f"{guide} inactive row has effective date")
            for scope in SCOPES:
                if row.get(scope) != "FALSE":
                    raise AssertionError(f"{guide}:{scope} must remain FALSE")
    results.append({"rule": "four Wave 1 guides active only for approved Stage 24 scopes", "status": "PASS"})
    results.append({"rule": "merge, release, and operations scopes remain inactive", "status": "PASS"})
    results.append({"rule": "all other guides remain NOT_ACTIVE", "status": "PASS"})
    return results

def validate(path: Path | None = None) -> list[dict[str, str]]:
    root = repo_root()
    return validate_rows(load_rows(path or (root / REGISTER_REL)))

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
            print(f"FAIL: {exc}")
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
