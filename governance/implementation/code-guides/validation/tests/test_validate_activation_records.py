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
    fields = ["guide_id", "activation_state", *validator.SCOPES, "effective_date"]
    handle = tempfile.NamedTemporaryFile("w", newline="", delete=False)
    with handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    return Path(handle.name)


def base_rows() -> list[dict[str, str]]:
    return [
        {
            "guide_id": guide_id,
            "activation_state": "NOT_ACTIVE",
            **{scope: "FALSE" for scope in validator.SCOPES},
            "effective_date": "NONE",
        }
        for guide_id in sorted(validator.GUIDES)
    ]


class ActivationRecordValidatorTests(unittest.TestCase):
    def test_positive_fixture(self) -> None:
        results = validator.validate_rows(base_rows())
        self.assertEqual(results[-1]["status"], "PASS")

    def test_negative_active_state_rejected(self) -> None:
        rows = base_rows()
        rows[0]["activation_state"] = "ACTIVE"
        with self.assertRaises(AssertionError):
            validator.validate_rows(rows)

    def test_malformed_missing_column_rejected(self) -> None:
        with tempfile.NamedTemporaryFile("w", newline="", delete=False) as handle:
            handle.write("guide_id,activation_state\nES-CG-00,NOT_ACTIVE\n")
        with self.assertRaises(AssertionError):
            validator.load_rows(Path(handle.name))

    def test_boundary_effective_date_rejected(self) -> None:
        rows = base_rows()
        rows[0]["effective_date"] = "2026-07-28"
        with self.assertRaises(AssertionError):
            validator.validate_rows(rows)

    def test_repository_register_validates(self) -> None:
        validator.validate()


if __name__ == "__main__":
    unittest.main()
