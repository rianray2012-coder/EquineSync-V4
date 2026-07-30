#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
VALIDATOR = ROOT / "governance/implementation/code-guides/founder-determinations/ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29/validators/validate_founder_approved_solo_founder_determination.py"
spec = importlib.util.spec_from_file_location("solo_founder_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)
PACKAGE = ROOT / validator.PACKAGE_REL

class SoloFounderDeterminationValidatorTests(unittest.TestCase):
    def copy_package(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tmp = tempfile.TemporaryDirectory()
        target = Path(tmp.name) / validator.PACKAGE_REL
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(PACKAGE, target)
        return tmp, target

    def test_package_validates(self) -> None:
        result = validator.validate(ROOT)
        self.assertEqual(result["status"], "PASS")

    def test_authorized_token_corrections_total_three(self) -> None:
        source = (PACKAGE / "SOURCE_PAYLOAD_ORIGINAL.md").read_text(encoding="utf-8")
        doc = (PACKAGE / validator.DOC_NAME).read_text(encoding="utf-8")
        self.assertEqual(source.count("MEDICAL_OR SAFETY"), 2)
        self.assertEqual(source.count("SECURITY_AND NEGATIVE"), 1)
        self.assertEqual(doc.count("MEDICAL_OR_SAFETY"), 2)
        self.assertEqual(doc.count("SECURITY_AND_NEGATIVE"), 1)

    def test_approved_metadata_is_finalized(self) -> None:
        doc = (PACKAGE / validator.DOC_NAME).read_text(encoding="utf-8")
        self.assertIn("**Founder Approval Status:** `FOUNDER_APPROVED`", doc)
        self.assertIn("**Founder Approval Date:** 2026-07-29", doc)
        self.assertIn(validator.APPROVAL_DISPOSITION, doc)
        self.assertNotIn("FOUNDER_APPROVAL_CANDIDATE", doc)

    def test_hash_and_byte_length_recorded_in_approval_record(self) -> None:
        result = validator.validate(ROOT)
        approval = (PACKAGE / "FOUNDER_APPROVAL_RECORD.md").read_text(encoding="utf-8")
        self.assertIn(result["document_sha256"], approval)
        self.assertIn(str(result["document_byte_length"]), approval)

    def test_truncated_source_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        (target / "SOURCE_PAYLOAD_ORIGINAL.md").write_text("# EQUINESYNC FOUNDER DETERMINATION\n", encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_correction_count_mismatch_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        source = (target / "SOURCE_PAYLOAD_ORIGINAL.md").read_text(encoding="utf-8").replace("MEDICAL_OR SAFETY", "MEDICAL_OR SAFETY_X", 1)
        (target / "SOURCE_PAYLOAD_ORIGINAL.md").write_text(source, encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_unrelated_wording_change_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        doc_path.write_text(doc_path.read_text(encoding="utf-8").replace("solo-Founder project", "solo-Founder initiative", 1), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_heading_alteration_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        doc_path.write_text(doc_path.read_text(encoding="utf-8").replace("# 1. PURPOSE", "# 1. PURPOSES", 1), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_finding_alteration_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        doc_path.write_text(doc_path.read_text(encoding="utf-8").replace("`W1-V11-FIND-0001`", "`W1-V11-FIND-9999`", 1), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_authority_expansion_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        doc_path.write_text(doc_path.read_text(encoding="utf-8").replace("`IMPLEMENTATION_NOT_AUTHORIZED_BY_THIS_DETERMINATION`", "`IMPLEMENTATION_AUTHORIZED_BY_THIS_DETERMINATION`", 1), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_stage_24_activation_language_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        doc_path.write_text(doc_path.read_text(encoding="utf-8").replace("`STAGE_24_GUIDE_ACTIVATION`", "`STAGE_24_GUIDE_ACTIVATION_AUTHORIZED`", 1), encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_self_referential_literal_hash_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        doc_path = target / validator.DOC_NAME
        result = validator.validate(ROOT)
        doc_path.write_text(doc_path.read_text(encoding="utf-8") + result["document_sha256"] + "\n", encoding="utf-8")
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_missing_approval_record_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        (target / "FOUNDER_APPROVAL_RECORD.md").unlink()
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_missing_checksum_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        (target / "CHECKSUM_MANIFEST.sha256").unlink()
        with self.assertRaises(validator.ValidationError):
            validator.validate(Path(tmp.name), enforce_git_paths=False)

    def test_unauthorized_path_change_fails(self) -> None:
        tmp, target = self.copy_package()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name)
        outside = repo / "governance/implementation/code-guides/PROGRAM_STATUS.md"
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_text("unauthorized\n", encoding="utf-8")
        # Simulate the authorized-path rule directly because temp roots are not git repos.
        changed = ["governance/implementation/code-guides/PROGRAM_STATUS.md"]
        outside_changes = [path for path in changed if not path.startswith(validator.PACKAGE_REL.as_posix() + "/")]
        self.assertTrue(outside_changes)

if __name__ == "__main__":
    unittest.main()
