#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
VALIDATOR = ROOT / "governance/implementation/code-guides/drafting/CGP-006/CODE_GUIDE_PROGRAM_V1_1_POST_CUSTODY_CLOSEOUT_AND_STATUS_RECONCILIATION/validators/validate_post_custody_closeout.py"
spec = importlib.util.spec_from_file_location("post_custody_closeout_validator", VALIDATOR)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)

class PostCustodyCloseoutTests(unittest.TestCase):
    def test_closeout_package_validates(self) -> None:
        validator.validate()

    def test_checksum_manifest_lists_package_manifest(self) -> None:
        package = validator.repo_root() / validator.PACKAGE_REL
        checksum_manifest = package / "CHECKSUM_MANIFEST.sha256"
        entries = {
            line.split("  ", 1)[1]
            for line in checksum_manifest.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        self.assertIn("PACKAGE_MANIFEST.json", entries)

if __name__ == "__main__":
    unittest.main()
