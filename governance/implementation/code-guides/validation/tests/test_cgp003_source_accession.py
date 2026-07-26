#!/usr/bin/env python3
"""Unit tests for CGP-003 source-accession validation."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

VALIDATION_DIR = Path(__file__).resolve().parents[1]
CODE_GUIDE_ROOT = VALIDATION_DIR.parent
sys.path.insert(0, str(VALIDATION_DIR))

import cgp_validation as cv  # noqa: E402


def codes(result: cv.ValidationResult) -> set[str]:
    return {issue.code for issue in result.issues}


class Cgp003SourceAccessionTests(unittest.TestCase):
    def test_current_source_accession_passes(self):
        result = cv.validate_source_accession(CODE_GUIDE_ROOT)
        self.assertEqual(result.status, "PASS", result.to_dict())
        self.assertGreater(result.summary["sources_checked"], 0)
        self.assertGreater(result.summary["mappings_checked"], 0)

    def test_negative_unknown_source_mapping_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "governance" / "implementation" / "code-guides"
            (tmp_root / "schemas").mkdir(parents=True)
            (tmp_root / "guides" / "ES-CG-00").mkdir(parents=True)
            (tmp_root / "source-accession").mkdir(parents=True)
            (Path(tmp) / "source.txt").write_text("source\n", encoding="utf-8")
            (tmp_root / "guides" / "ES-CG-00" / "README.md").write_text("# Guide\n", encoding="utf-8")
            values = json.loads((CODE_GUIDE_ROOT / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").read_text(encoding="utf-8"))
            (tmp_root / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").write_text(json.dumps(values), encoding="utf-8")

            source_path = tmp_root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_REGISTER.csv"
            source_fields = [
                "source_id",
                "title",
                "filename",
                "repository_path",
                "source_class",
                "authority_status",
                "version",
                "effective_date",
                "approval_authority",
                "approval_record_path",
                "checksum",
                "checksum_verification_status",
                "exact_approved_bytes_accessioned",
                "source_format",
                "related_pias",
                "related_atlases",
                "applicable_code_guides",
                "related_controls_or_domains",
                "predecessor",
                "successor",
                "supersession_status",
                "conflicts",
                "limitations",
                "custody_status",
                "review_status",
                "originating_commit",
                "repository_integration_receipt_path",
                "notes",
            ]
            with source_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=source_fields, lineterminator="\n")
                writer.writeheader()
                writer.writerow({
                    "source_id": "CGSRC-TEST-0001",
                    "title": "Synthetic source",
                    "filename": "source.txt",
                    "repository_path": "source.txt",
                    "source_class": "REPOSITORY_EVIDENCE",
                    "authority_status": "SUPPORTING",
                    "checksum": cv.sha256_file(Path(tmp) / "source.txt"),
                    "checksum_verification_status": "VERIFIED_FILE",
                    "exact_approved_bytes_accessioned": "NOT_APPLICABLE",
                    "source_format": "TXT",
                    "applicable_code_guides": "ES-CG-00",
                    "custody_status": "REPOSITORY_NATIVE",
                    "review_status": "PENDING_REVIEW",
                })

            mapping_path = tmp_root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv"
            rows = [{
                "mapping_id": "CGMAP-0001",
                "source_id": "CGSRC-MISSING-9999",
                "guide_id": "ES-CG-00",
                "mapping_type": "SUPPORTING",
                "authority_status": "SUPPORTING",
                "coverage_note": "negative fixture",
                "gap_references": "",
            }]
            fields = list(rows[0])
            with mapping_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
                writer.writeheader()
                writer.writerows(rows)
            for name, header in {
                "MASTER_CODE_GUIDE_SOURCE_GAP_REGISTER.csv": ["gap_id", "source_id", "gap_type", "affected_source", "affected_guide_or_program_area", "risk", "required_next_action", "responsible_authority", "drafting_may_proceed", "blocks_adoption_or_activation", "status", "notes"],
                "MASTER_CODE_GUIDE_SOURCE_CONFLICT_REGISTER.csv": ["conflict_id", "source_ids", "conflict_type", "affected_area", "description", "current_treatment", "required_next_action", "status", "notes"],
                "MASTER_CODE_GUIDE_SOURCE_SUPERSESSION_REGISTER.csv": ["supersession_id", "predecessor_source_id", "successor_source_id", "supersession_status", "evidence_path", "affected_guides", "notes"],
            }.items():
                with (tmp_root / "source-accession" / name).open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.writer(handle, lineterminator="\n")
                    writer.writerow(header)
            result = cv.validate_source_accession(tmp_root)
            self.assertEqual(result.status, "FAIL")
            self.assertIn("orphan_source_mapping", codes(result))


if __name__ == "__main__":
    unittest.main()
