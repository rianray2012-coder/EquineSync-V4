from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
PKG = ROOT / "governance/implementation/code-guides/drafting/CGP-006/SOLO_FOUNDER_COMPENSATING_ASSURANCE_PROFILE_AND_STAGE_24_READINESS_REBASE_V1"
VALIDATOR_PATH = PKG / "validators/validate_solo_founder_assurance_stage24_readiness.py"
spec = importlib.util.spec_from_file_location("stage24_validator", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class SoloFounderStage24ReadinessValidatorTests(unittest.TestCase):
    def copy_pkg(self):
        tmp = Path(tempfile.mkdtemp())
        target = tmp / "pkg"
        shutil.copytree(PKG, target)
        self.addCleanup(shutil.rmtree, tmp)
        return target

    def assert_fails(self, pkg, text):
        with self.assertRaises(validator.ValidationError) as ctx:
            validator.validate(ROOT, package_override=pkg, enforce_git_paths=False)
        self.assertIn(text, str(ctx.exception))

    def read_csv_rows(self, path):
        with path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def write_csv_rows(self, path, rows):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def refresh_copy_manifests(self, pkg):
        def digest(path):
            import hashlib
            data = path.read_bytes()
            return hashlib.sha256(data).hexdigest(), len(data)

        manifest = json.loads((pkg / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        for entry in manifest["files"]:
            sha, size = digest(pkg / entry["path"])
            entry["sha256"] = sha
            entry["byte_length"] = size
        (pkg / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        lines = []
        for path in sorted(pkg.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(pkg).as_posix()
            if rel == "CHECKSUM_MANIFEST.sha256":
                continue
            sha, _ = digest(path)
            lines.append(f"{sha}  {rel}")
        (pkg / "CHECKSUM_MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def test_positive_package_validates(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["guide_count"], 4)
        self.assertEqual(result["approved_disposition_source_count"], 4)
        self.assertEqual(result["residual_risk_rows"], 12)
        self.assertEqual(result["residual_risk_decision_rows"], 12)

    def test_candidate_profile_exact_bytes_preserved(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["adopted_profile_byte_length"], len((PKG / validator.ADOPTED_PROFILE).read_bytes()))

    def test_altered_candidate_profile_fails(self):
        pkg = self.copy_pkg()
        path = pkg / validator.CANDIDATE_PROFILE["path"]
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.assert_fails(pkg, "candidate profile hash mismatch")

    def test_adopted_profile_required_tokens_present(self):
        text = (PKG / validator.ADOPTED_PROFILE).read_text(encoding="utf-8")
        self.assertIn("FOUNDER_ADOPTED", text)
        self.assertIn("PROFILE_ADOPTED_PENDING_EFFECTIVE_EVENT", text)
        self.assertIn(validator.EFFECTIVE_EVENT, text)
        self.assertNotIn("FOUNDER_ADOPTION_CANDIDATE_ONLY", text)

    def test_missing_adopted_profile_fails(self):
        pkg = self.copy_pkg()
        (pkg / validator.ADOPTED_PROFILE).unlink()
        self.assert_fails(pkg, "required file missing")

    def test_adopted_profile_candidate_status_fails(self):
        pkg = self.copy_pkg()
        path = pkg / validator.ADOPTED_PROFILE
        path.write_text(path.read_text(encoding="utf-8") + "\nFOUNDER_ADOPTION_CANDIDATE_ONLY\n", encoding="utf-8")
        self.assert_fails(pkg, "adopted profile still marked candidate-only")

    def test_exact_approved_disposition_source_bytes_pass(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["approved_disposition_source_count"], 4)

    def test_altered_approved_disposition_source_hash_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_DISPOSITION_SOLO_FOUNDER_PROFILE_AND_LIMITED_STAGE_24_ACTIVATION_2026-07-30.md"
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.assert_fails(pkg, "approved source hash mismatch")

    def test_missing_approved_disposition_source_fails(self):
        pkg = self.copy_pkg()
        (pkg / "FOUNDER_STAGE_24_ACTIVATION_SCOPE_RECORD_2026-07-30.md").unlink()
        self.assert_fails(pkg, "required file missing")

    def test_exact_approved_tooling_source_bytes_still_pass(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["approved_tooling_source_count"], 7)

    def test_residual_risk_decisions_all_accepted(self):
        rows = self.read_csv_rows(PKG / "SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_REGISTER.csv")
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(row["founder_acceptance_status"] == validator.RISK_DECISION for row in rows))

    def test_pending_residual_risk_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_REGISTER.csv"
        rows = self.read_csv_rows(path)
        rows[0]["founder_acceptance_status"] = "PENDING_FOUNDER_DECISION"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "Founder residual risk decision incomplete")

    def test_missing_residual_risk_decision_row_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_DECISION_REGISTER_STAGE24.csv"
        rows = self.read_csv_rows(path)[:-1]
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "residual risk decision companion register mismatch")

    def test_residual_risk_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "SOLO_FOUNDER_ASSURANCE_RESIDUAL_RISK_DECISION_REGISTER_STAGE24.csv"
        rows = self.read_csv_rows(path)
        rows[0]["risk_closure_status"] = "CLOSED"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "residual risk companion marks risk closed")

    def test_scope_matrix_pending_effective_event(self):
        rows = self.read_csv_rows(PKG / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv")
        approved = {"PLANNING_REFERENCE", "IMPLEMENTATION_CONTROL", "PULL_REQUEST_REVIEW"}
        for row in rows:
            self.assertEqual(row["activation_state_after_package"], validator.NOT_ACTIVE_PENDING_CUSTODY)
            if row["scope"] in approved:
                self.assertEqual(row["recommended_posture"], "APPROVED_PENDING_EFFECTIVE_EVENT")
                self.assertEqual(row["effective_date_recommendation"], validator.EFFECTIVE_EVENT)

    def test_scope_marked_active_before_custody_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["activation_state_after_package"] = "ACTIVE"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "activates a guide before custody")

    def test_merge_gate_approval_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv"
        rows = self.read_csv_rows(path)
        row = next(row for row in rows if row["scope"] == "MERGE_GATE")
        row["recommended_posture"] = "APPROVED_PENDING_EFFECTIVE_EVENT"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "deferred scope not deferred")

    def test_missing_effective_event_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["effective_date_recommendation"] = "NONE"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "approved scope missing custody effective event")

    def test_readiness_rows_remain_not_active_pending_custody(self):
        rows = self.read_csv_rows(PKG / "WAVE_1_STAGE_24_READINESS_MATRIX.csv")
        self.assertTrue(all(row["activation_state_after_package"] == validator.NOT_ACTIVE_PENDING_CUSTODY for row in rows))

    def test_open_p0_or_p1_with_ready_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "WAVE_1_STAGE_24_READINESS_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["open_p0_count"] = "1"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "ready result paired with open P0 or P1")

    def test_silent_finding_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "WAVE_1_FINDING_TREATMENT_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["proposed_disposition"] = "CLOSED"
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "silent finding closure")

    def test_silent_warning_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv"
        rows = self.read_csv_rows(path)
        for row in rows:
            if row["record_type"] == "RETAINED_WARNING":
                row["proposed_treatment"] = "CLOSED"
                break
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "silent warning closure")

    def test_gap_0004_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv"
        rows = self.read_csv_rows(path)
        for row in rows:
            if row["source_id"] == "CGP005-TA-APP-GAP-0004":
                row["proposed_treatment"] = "CLOSED"
                break
        self.write_csv_rows(path, rows)
        self.assert_fails(pkg, "GAP-0004 closure")

    def test_implementation_mapping_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nREPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AUTHORIZED\n", encoding="utf-8")
        self.assert_fails(pkg, "prohibited authority")

    def test_implementation_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nIMPLEMENTATION_AUTHORIZED\n", encoding="utf-8")
        self.assert_fails(pkg, "prohibited authority")

    def test_external_tool_setup_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nEXTERNAL_TOOL_SETUP_AUTHORIZED\n", encoding="utf-8")
        self.assert_fails(pkg, "prohibited authority")

    def test_pilot_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nPILOT_AUTHORIZED\n", encoding="utf-8")
        self.assert_fails(pkg, "prohibited authority")

    def test_independent_review_claim_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "VALIDATION_REPORT.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nINDEPENDENT_HUMAN_TECHNICAL_REVIEW_PERFORMED\n", encoding="utf-8")
        self.assert_fails(pkg, "prohibited authority")

    def test_package_manifest_hash_mismatch_fails(self):
        pkg = self.copy_pkg()
        manifest = json.loads((pkg / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        manifest["files"][0]["sha256"] = "0" * 64
        (pkg / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.assert_fails(pkg, "package manifest hash mismatch")

    def test_checksum_mismatch_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "CHECKSUM_MANIFEST.sha256"
        lines = path.read_text(encoding="utf-8").splitlines()
        lines[0] = "0" * 64 + lines[0][64:]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assert_fails(pkg, "checksum mismatch")

    def test_source_freeze_missing_adopted_profile_fails(self):
        pkg = self.copy_pkg()
        manifest_path = pkg / "SOURCE_FREEZE_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["sources"] = [entry for entry in manifest["sources"] if entry.get("source_id") != "SFCA-SRC-0062"]
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        self.assert_fails(pkg, "source freeze missing adopted profile")

    def test_source_ledger_missing_adopted_profile_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "SOURCE_SHA256SUMS.txt"
        lines = [line for line in path.read_text(encoding="utf-8").splitlines() if not line.endswith(validator.ADOPTED_PROFILE)]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.refresh_copy_manifests(pkg)
        self.assert_fails(pkg, "source SHA-256 ledger missing adopted profile")

    def test_authority_matrix_adopted_profile_status_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "SOURCE_AUTHORITY_MATRIX.csv"
        rows = self.read_csv_rows(path)
        for row in rows:
            if row["source_id"] == "SFCA-SRC-0062":
                row["source_status"] = "candidate"
                break
        self.write_csv_rows(path, rows)
        self.refresh_copy_manifests(pkg)
        self.assert_fails(pkg, "authority matrix adopted profile status mismatch")

    def test_missing_phase_a_statement_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text(encoding="utf-8").replace("CUSTODY_PR_REQUIRED_BEFORE_ACTIVATION_EFFECTIVE", ""), encoding="utf-8")
        self.assert_fails(pkg, "required Phase A statement")

    def test_unauthorized_canonical_file_change_fails(self):
        with self.assertRaises(validator.ValidationError):
            validator.check_authorized_paths(["governance/implementation/code-guides/PROGRAM_STATUS.md"])

if __name__ == "__main__":
    unittest.main()
