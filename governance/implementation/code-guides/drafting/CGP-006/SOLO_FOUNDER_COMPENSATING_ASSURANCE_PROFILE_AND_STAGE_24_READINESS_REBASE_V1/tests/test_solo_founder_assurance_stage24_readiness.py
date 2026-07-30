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
        with path.open(newline="") as f:
            return list(csv.DictReader(f))

    def test_positive_package_validates(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["guide_count"], 4)
        self.assertEqual(result["finding_rows"], 6)

    def test_exact_controlling_determination_passes(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertGreaterEqual(result["source_count"], 30)

    def test_exact_adopted_guide_bytes_pass(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["readiness_rows"], 4)

    def test_exact_approved_tooling_source_bytes_pass(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["approved_tooling_source_count"], 7)

    def test_altered_approved_tooling_source_hash_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "MULTI_AGENT_AND_ASSURANCE_TOOLING_INTENT_V1_0_0.md"
        path.write_text(path.read_text() + "\n")
        self.assert_fails(pkg, "approved tooling source hash mismatch")

    def test_missing_approved_tooling_source_fails(self):
        pkg = self.copy_pkg()
        (pkg / "AGENT_FINDING_RECORD_SCHEMA_V1_0_0.md").unlink()
        self.assert_fails(pkg, "required file missing")

    def test_tooling_pending_approval_claim_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\n`TOOLING_INTENT_CANDIDATE`\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_external_tool_setup_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text() + "\nEXTERNAL_TOOL_SETUP_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_named_tools_mandatory_for_stage24_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nNAMED_TOOLS_REQUIRED_FOR_LIMITED_STAGE_24_ACTIVATION\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_cursor_background_agent_present_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nCURSOR_BACKGROUND_AGENTS_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_claude_code_write_authority_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nCLAUDE_CODE_WRITE_ACCESS_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_jules_present_implementation_authority_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nGOOGLE_JULES_PRESENT_IMPLEMENTATION_AUTHORITY\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_agent_finding_proven_without_validation_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nAGENT_FINDING_PROVEN_WITHOUT_VALIDATION\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_agent_self_approve_and_merge_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "README.md"
        path.write_text(path.read_text() + "\nAGENT_MAY_SELF_APPROVE_AND_MERGE\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_pr_ready_for_review_marker_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "DIRECTIVE_EXECUTION_RECORD.md"
        path.write_text(path.read_text() + "\nPR_59_READY_FOR_REVIEW\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_second_pr_marker_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "DIRECTIVE_EXECUTION_RECORD.md"
        path.write_text(path.read_text() + "\nSECOND_PR_OPENED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_disclosed_non_independent_review_statuses_pass(self):
        text = (PKG / "FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_RECORD.md").read_text()
        self.assertIn("FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_COMPLETE_WITH_DISCLOSED_SELF_REVIEW", text)
        self.assertIn("FOUNDER_TECHNICAL_GOVERNANCE_REVIEW_IS_NOT_INDEPENDENT", text)

    def test_implementation_evidence_assigned_later(self):
        rows = self.read_csv_rows(PKG / "WAVE_1_FINDING_TREATMENT_MATRIX.csv")
        row = next(r for r in rows if r["finding_id"] == "W1-V11-FIND-0005")
        self.assertIn("IMPLEMENTATION_EVIDENCE_REQUIRED_AFTER_AUTHORIZED_IMPLEMENTATION", row["proposed_disposition"])

    def test_runtime_evidence_assigned_later(self):
        rows = self.read_csv_rows(PKG / "WAVE_1_FINDING_TREATMENT_MATRIX.csv")
        row = next(r for r in rows if r["finding_id"] == "W1-V11-FIND-0006")
        self.assertIn("RUNTIME_EVIDENCE_REQUIRED_AFTER_AUTHORIZED_STAGING_OR_PILOT_USE", row["proposed_disposition"])

    def test_guide_specific_readiness_classification_passes(self):
        rows = self.read_csv_rows(PKG / "WAVE_1_STAGE_24_READINESS_MATRIX.csv")
        self.assertEqual({r["guide_id"] for r in rows}, {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"})
        self.assertTrue(all(r["activation_state_after_package"] == "NOT_ACTIVE" for r in rows))

    def test_limited_activation_proposals_remain_proposals_only(self):
        rows = self.read_csv_rows(PKG / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv")
        self.assertEqual(len(rows), 24)
        self.assertTrue(all(r["effective_date_recommendation"] == "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED_IN_THIS_PACKAGE" for r in rows))

    def test_all_required_disclosures_present(self):
        result = validator.validate(ROOT, enforce_git_paths=False)
        self.assertEqual(result["status"], "PASS")

    def test_package_only_path_control_passes(self):
        validator.check_authorized_paths([str(validator.PACKAGE_REL / "README.md")])

    def test_altered_determination_hash_fails(self):
        pkg = self.copy_pkg()
        manifest = json.loads((pkg / "SOURCE_FREEZE_MANIFEST.json").read_text())
        manifest["controlling_determination_sha256"] = "0" * 64
        (pkg / "SOURCE_FREEZE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        self.assert_fails(pkg, "source freeze determination hash mismatch")

    def test_altered_guide_bytes_fails(self):
        pkg = self.copy_pkg()
        manifest = json.loads((pkg / "SOURCE_FREEZE_MANIFEST.json").read_text())
        manifest["guides"][0]["sha256"] = "0" * 64
        (pkg / "SOURCE_FREEZE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        self.assert_fails(pkg, "source freeze guide identity mismatch")

    def test_independent_review_claim_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "PASS_A_AUTHORITY_AND_SOURCE_FIDELITY_REVIEW.md"
        path.write_text(path.read_text() + "\n`INDEPENDENT_HUMAN_TECHNICAL_REVIEW_PERFORMED`\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_silent_finding_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "WAVE_1_FINDING_TREATMENT_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["proposed_disposition"] = "CLOSED"
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        self.assert_fails(pkg, "silent finding closure")

    def test_silent_warning_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv"
        rows = self.read_csv_rows(path)
        for row in rows:
            if row["record_type"] == "RETAINED_WARNING":
                row["proposed_treatment"] = "CLOSED"
                break
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        self.assert_fails(pkg, "silent warning closure")

    def test_gap_0004_closure_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "RETAINED_CONDITION_WARNING_GAP_AND_BLOCKER_MATRIX.csv"
        rows = self.read_csv_rows(path)
        for row in rows:
            if row["source_id"] == "CGP005-TA-APP-GAP-0004":
                row["proposed_treatment"] = "CLOSED"
                break
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        self.assert_fails(pkg, "GAP-0004 closure")

    def test_guide_activation_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "WAVE_1_STAGE_24_READINESS_MATRIX.csv"
        text = path.read_text().replace("NOT_ACTIVE", "ANY_GUIDE_ACTIVE_STATUS", 1)
        path.write_text(text)
        self.assert_fails(pkg, "prohibited authority")

    def test_effective_date_establishment_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "PROPOSED_STAGE_24_ACTIVATION_SCOPE_MATRIX.csv"
        path.write_text(path.read_text() + "\nACTIVATION_EFFECTIVE_DATE_ESTABLISHED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_implementation_mapping_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text() + "\nREPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_implementation_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text() + "\nIMPLEMENTATION_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_deployment_or_pilot_authorization_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_STAGE_24_LIMITED_ACTIVATION_DECISION_PACKET.md"
        path.write_text(path.read_text() + "\nPILOT_AUTHORIZED\n")
        self.assert_fails(pkg, "prohibited authority")

    def test_missing_review_pass_fails(self):
        pkg = self.copy_pkg()
        (pkg / "PASS_H_ADVERSARIAL_AND_RED_TEAM_REVIEW.md").unlink()
        self.assert_fails(pkg, "required file missing")

    def test_unresolved_founder_confirmation_with_completion_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "FOUNDER_DOMAIN_OWNER_REVIEW_RECORD.md"
        path.write_text(path.read_text() + "\nFOUNDER_CONFIRMATION_REQUIRED\n")
        self.assert_fails(pkg, "domain review claims completion")

    def test_open_p0_or_p1_with_ready_fails(self):
        pkg = self.copy_pkg()
        path = pkg / "WAVE_1_STAGE_24_READINESS_MATRIX.csv"
        rows = self.read_csv_rows(path)
        rows[0]["open_p0_count"] = "1"
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys(), lineterminator="\n")
            w.writeheader(); w.writerows(rows)
        self.assert_fails(pkg, "ready result paired with open P0 or P1")

    def test_unauthorized_canonical_file_change_fails(self):
        with self.assertRaises(validator.ValidationError):
            validator.check_authorized_paths(["governance/implementation/code-guides/PROGRAM_STATUS.md"])

if __name__ == "__main__":
    unittest.main()
