#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
VALIDATOR = ROOT / "governance/implementation/code-guides/validation/validate_activation_records.py"
spec = importlib.util.spec_from_file_location("activation_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

def write_fixture(rows: list[dict[str, str]]) -> Path:
    fields = ["guide_id", "guide_version", "activation_state", *validator.SCOPES, "effective_date", "authority"]
    handle = tempfile.NamedTemporaryFile("w", newline="", delete=False)
    with handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    return Path(handle.name)

def base_rows() -> list[dict[str, str]]:
    rows = []
    for guide_id in sorted(validator.ALL_GUIDES):
        active = guide_id in validator.ACTIVE_GUIDES
        rows.append({
            "guide_id": guide_id,
            "guide_version": "1.1.0" if active else "UNADOPTED_CANDIDATE_OR_PLANNED",
            "activation_state": validator.ACTIVE_STATE if active else "NOT_ACTIVE",
            **{scope: ("TRUE" if active and scope in validator.APPROVED_SCOPES else "FALSE") for scope in validator.SCOPES},
            "effective_date": validator.EFFECTIVE_EVENT if active else "NONE",
            "authority": validator.AUTHORITY if active else "GUIDE_ACTIVATION_NOT_AUTHORIZED",
        })
    return rows

class ActivationRecordValidatorTests(unittest.TestCase):
    def test_positive_fixture(self) -> None:
        self.assertEqual(validator.validate_rows(base_rows())[-1]["status"], "PASS")

    def test_repository_register_validates(self) -> None:
        validator.validate()

    def test_inactive_guide_cannot_be_active(self) -> None:
        rows = base_rows()
        row = next(r for r in rows if r["guide_id"] == "ES-CG-02")
        row["activation_state"] = validator.ACTIVE_STATE
        with self.assertRaises(AssertionError):
            validator.validate_rows(rows)

    def test_merge_gate_rejected(self) -> None:
        rows = base_rows()
        row = next(r for r in rows if r["guide_id"] == "ES-CG-00")
        row["MERGE_GATE"] = "TRUE"
        with self.assertRaises(AssertionError):
            validator.validate_rows(rows)

    def test_missing_effective_event_rejected(self) -> None:
        rows = base_rows()
        row = next(r for r in rows if r["guide_id"] == "ES-CG-01")
        row["effective_date"] = "NONE"
        with self.assertRaises(AssertionError):
            validator.validate_rows(rows)

    def test_malformed_missing_column_rejected(self) -> None:
        with tempfile.NamedTemporaryFile("w", newline="", delete=False) as handle:
            handle.write("guide_id,activation_state\nES-CG-00,NOT_ACTIVE\n")
        with self.assertRaises(AssertionError):
            validator.load_rows(Path(handle.name))

if __name__ == "__main__":
    unittest.main()
