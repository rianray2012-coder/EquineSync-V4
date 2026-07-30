#!/usr/bin/env python3
"""Tests for current Wave 1 custody status-table consistency."""

from __future__ import annotations

import contextlib
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parents[1]
CODE_GUIDE_ROOT = VALIDATION_DIR.parent
sys.path.insert(0, str(VALIDATION_DIR))

import cgp_validation as cv  # noqa: E402


GUIDES = ("ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13")


def result_codes(result: cv.ValidationResult) -> set[str]:
    return {issue.code for issue in result.issues}


def status_text(overrides: dict[tuple[str, str], str] | None = None) -> str:
    overrides = overrides or {}
    rows = []
    for guide in GUIDES:
        values = {
            "Stage 22 adoption": "ADOPTED",
            "Stage 23 accession": "REPOSITORY_ACCESSIONED",
            "Custody": "CUSTODY_COMPLETE",
            "Activation": "ACTIVE_LIMITED_STAGE_24",
            "Implementation mapping": "NOT_AUTHORIZED",
            "Implementation": "NOT_AUTHORIZED",
        }
        for column in values:
            values[column] = overrides.get((guide, column), values[column])
        rows.append(
            f"| `{guide}` | `{values['Stage 22 adoption']}` | `{values['Stage 23 accession']}` | "
            f"`{values['Custody']}` | `{values['Activation']}` | "
            f"`{values['Implementation mapping']}` | `{values['Implementation']}` |"
        )
    return textwrap.dedent(
        f"""\
        # Code Guide Program Status

        **Prompt status:** `{cv.WAVE_1_STAGE23_CUSTODY_COMPLETE_STATUS}`

        ## Wave 1 V1.1 Stage 22 Adoption And Stage 23 Accession Status

        | Guide | Stage 22 adoption | Stage 23 accession | Custody | Activation | Implementation mapping | Implementation |
        | --- | --- | --- | --- | --- | --- | --- |
        {rows[0]}
        {rows[1]}
        {rows[2]}
        {rows[3]}
        """
    )


@contextlib.contextmanager
def temporary_code_guide_root(program_status: str):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "governance" / "implementation" / "code-guides"
        (root / "schemas").mkdir(parents=True)
        (root / "registers").mkdir()
        (root / "drafting" / "CGP-006" / "HISTORICAL").mkdir(parents=True)
        (root / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").write_text(
            (CODE_GUIDE_ROOT / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / "CONTROLLED_VALUES.md").write_text(
            (CODE_GUIDE_ROOT / "CONTROLLED_VALUES.md").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (root / "registers" / "CODE_GUIDE_CONTROL_REGISTER.csv").write_text(
            "control_id,guide_id,title,status\n",
            encoding="utf-8",
        )
        tracker_rows = [
            "record_id,record_type,guide_id,maturity_state,adoption_state,accession_state",
            *[
                f"{guide},GUIDE,{guide},REPOSITORY_ACCESSIONED,ADOPTED,REPOSITORY_ACCESSIONED"
                for guide in GUIDES
            ],
        ]
        (root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv").write_text("\n".join(tracker_rows) + "\n", encoding="utf-8")
        (root / "PROGRAM_STATUS.md").write_text(program_status, encoding="utf-8")
        yield root


class Wave1CurrentStatusCustodyTableTests(unittest.TestCase):
    def test_current_status_table_passes_when_custody_complete(self) -> None:
        with temporary_code_guide_root(status_text()) as root:
            result = cv.validate_portfolio_consistency(root)
        self.assertEqual(result.status, "PASS")

    def test_current_status_table_fails_when_one_guide_is_pending_custody(self) -> None:
        with temporary_code_guide_root(status_text({("ES-CG-00", "Custody"): "PENDING_CUSTODY"})) as root:
            result = cv.validate_portfolio_consistency(root)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("wave1_current_status_custody_inconsistent", result_codes(result))

    def test_historical_pending_custody_record_is_ignored(self) -> None:
        with temporary_code_guide_root(status_text()) as root:
            (root / "drafting" / "CGP-006" / "HISTORICAL" / "SNAPSHOT.md").write_text(
                "Historical pre-custody record: `PENDING_CUSTODY`.\n",
                encoding="utf-8",
            )
            result = cv.validate_portfolio_consistency(root)
        self.assertEqual(result.status, "PASS")

    def test_boundary_status_changes_fail(self) -> None:
        cases = [
            ("Stage 22 adoption", "NOT_ADOPTED"),
            ("Stage 23 accession", "NOT_ACCESSIONED"),
            ("Activation", "NOT_ACTIVE"),
            ("Implementation mapping", "AUTHORIZED"),
            ("Implementation", "AUTHORIZED"),
        ]
        for column, value in cases:
            with self.subTest(column=column):
                with temporary_code_guide_root(status_text({("ES-CG-00", column): value})) as root:
                    result = cv.validate_portfolio_consistency(root)
                self.assertEqual(result.status, "FAIL")
                self.assertIn("wave1_current_status_boundary_changed", result_codes(result))

    def test_missing_current_table_fails_closed(self) -> None:
        no_table = f"# Code Guide Program Status\n\n**Prompt status:** `{cv.WAVE_1_STAGE23_CUSTODY_COMPLETE_STATUS}`\n"
        with temporary_code_guide_root(no_table) as root:
            result = cv.validate_portfolio_consistency(root)
        self.assertEqual(result.status, "FAIL")
        self.assertIn("missing_wave1_current_status_table", result_codes(result))


if __name__ == "__main__":
    unittest.main()
