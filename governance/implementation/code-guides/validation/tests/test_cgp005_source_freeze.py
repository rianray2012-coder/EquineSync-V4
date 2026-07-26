#!/usr/bin/env python3
"""CGP-005 source-freeze validator behavior tests."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cgp_validation as validators


CODE_GUIDE_ROOT = Path(__file__).resolve().parents[2]
BASELINE = "b" * 40
WAVE_GUIDE = ("ES-CG-00",)


class CGP005SourceFreezeValidatorTests(unittest.TestCase):
    def write_csv(self, path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def read_csv(self, path: Path) -> tuple[list[str], list[dict[str, str]]]:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return list(reader.fieldnames or []), list(reader)

    def build_fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, dict[str, Path]]:
        tmp = tempfile.TemporaryDirectory()
        repo = Path(tmp.name)
        root = repo / "governance" / "implementation" / "code-guides"
        guide_dir = root / "guides" / "ES-CG-00"
        (root / "schemas").mkdir(parents=True)
        (root / "source-freeze").mkdir()
        (root / "source-accession").mkdir()
        (guide_dir / "source-freeze").mkdir(parents=True)
        (root / "registers").mkdir()
        (repo / "docs").mkdir()
        source = repo / "docs" / "source.md"
        source.write_text("frozen source bytes\n", encoding="utf-8")
        approval = repo / "docs" / "approval.md"
        approval.write_text("approval basis\n", encoding="utf-8")
        checksum = validators.sha256_file(source)
        values = {
            "source_checksum_statuses": ["VERIFIED_FILE", "VERIFIED_DIRECTORY_AGGREGATE", "NOT_APPLICABLE", "MISSING", "UNVERIFIED", "MISMATCH"],
            "source_freeze_inclusion_categories": sorted(validators.SOURCE_FREEZE_INCLUSION_CATEGORIES),
            "source_freeze_readiness_dispositions": [
                "CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW",
                "SOURCE_FREEZE_COMPLETE_READY_FOR_CGP_006_WHEN_AUTHORIZED",
                "SOURCE_FREEZE_COMPLETE_WITH_RETAINED_NON_BLOCKING_GAPS",
                "BLOCKED_BY_SOURCE_CUSTODY",
                "BLOCKED_BY_AUTHORITY_DECISION",
                "NOT_IN_WAVE_1",
            ],
        }
        (root / "schemas" / "CODE_GUIDE_CONTROLLED_VALUES.json").write_text(json.dumps(values), encoding="utf-8")
        source_fields = validators._source_freeze_fields()
        base_row = {
            "freeze_record_id": "CGP005-RC-0001",
            "source_id": "CGSRC-TEST-0001",
            "guide_id": "WAVE_1_REFERENCE_CORPUS",
            "title": "Fixture source",
            "filename": "source.md",
            "repository_path": "docs/source.md",
            "source_class": "ADOPTED_GOVERNANCE",
            "authority_status": "CONTROLLING",
            "inclusion_category": "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE",
            "version": "1.0",
            "effective_date": "2026-07-26",
            "approval_authority": "Founder",
            "approval_record_path": "docs/approval.md",
            "repository_commit": BASELINE,
            "git_object_sha": "a" * 40,
            "git_object_type": "BLOB",
            "sha256_checksum": checksum,
            "checksum_verification_result": "VERIFIED_FILE",
            "package_checksum": "",
            "package_manifest_path": "",
            "repository_integration_receipt": "governance/implementation/code-guides/receipts/CGP_005_EXECUTION_RECEIPT.md",
            "custody_status": "REPOSITORY_NATIVE",
            "predecessor": "",
            "successor": "",
            "supersession_status": "CURRENT",
            "conflict_status": "NO_KNOWN_BLOCKING_CONFLICT",
            "reason_for_inclusion": "Fixture reference corpus row preserves exact bytes without creating normative drafting authority for the guide.",
            "authority_rationale": "The reference corpus row is discovery evidence only and is separated from the curated normative freeze.",
            "guide_requirement_area": "REFERENCE_CORPUS",
            "necessity_test": "REFERENCE_CORPUS_ONLY",
            "consequence_of_exclusion": "Removing the row would reduce traceability but would not remove normative guide authority.",
            "related_drafting_question_ids": "REFERENCE_ONLY",
            "package_level_source_could_replace": "NOT_EVALUATED_REFERENCE_ONLY",
            "cgp004_component_ids": "",
            "curation_status": "REFERENCE_CORPUS_ONLY",
            "selected_from_cgp003_mapping": "YES",
            "source_burden_treatment": "CONTROLLING_FROZEN",
            "retained_limitations": "Reference corpus only.",
        }
        guide_row = {
            **base_row,
            "freeze_record_id": "CGP005-NF-ES-CG-00-0001",
            "guide_id": "ES-CG-00",
            "inclusion_category": "CONTROLLING_FROZEN",
            "reason_for_inclusion": "ES-CG-00 requires this approved fixture authority to establish its charter boundary before drafting begins.",
            "authority_rationale": "The source has controlling fixture status and supplies authority that cannot be replaced by repository behavior.",
            "guide_requirement_area": "charter_authority",
            "necessity_test": "CONTROLLING_AUTHORITY",
            "consequence_of_exclusion": "Excluding it would remove the authority basis required to validate a guide-specific source selection.",
            "related_drafting_question_ids": "ES-CG-00-DQ-0001",
            "package_level_source_could_replace": "NO",
            "curation_status": "NORMATIVE_SELECTED",
            "source_burden_treatment": "NORMATIVE_MINIMUM_REQUIRED",
        }
        reference_register = root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REGISTER.csv"
        guide_register = guide_dir / "source-freeze" / "ES-CG-00_SOURCE_FREEZE_REGISTER.csv"
        self.write_csv(reference_register, source_fields, [base_row])
        self.write_csv(guide_register, source_fields, [guide_row])
        reference_manifest = {
            "baseline_commit": BASELINE,
            "classification": "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE",
            "directory_manifests": {},
            "sources": [{"source_id": "CGSRC-TEST-0001"}],
        }
        guide_manifest = {
            "classification": "NORMATIVE_GUIDE_SOURCE_FREEZE",
            "curation_method": "GUIDE_SPECIFIC_MINIMUM_AUTHORITY_SET",
            "sources": [{"source_id": "CGSRC-TEST-0001"}],
        }
        (root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json").write_text(json.dumps(reference_manifest), encoding="utf-8")
        (root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_REPORT.md").write_text("reference report", encoding="utf-8")
        (guide_dir / "source-freeze" / "ES-CG-00_SOURCE_FREEZE_MANIFEST.json").write_text(json.dumps(guide_manifest), encoding="utf-8")
        self.write_csv(
            root / "source-freeze" / "WAVE_1_SOURCE_FREEZE_CROSSWALK.csv",
            ["crosswalk_id", "guide_id", "source_id", "source_class", "authority_status", "inclusion_category", "mapping_type", "coverage_note", "source_freeze_record_id", "freeze_manifest_path", "readiness_effect"],
            [{"crosswalk_id": "CGP005-XW-00001", "guide_id": "ES-CG-00", "source_id": "CGSRC-TEST-0001", "source_class": "ADOPTED_GOVERNANCE", "authority_status": "CONTROLLING", "inclusion_category": "CONTROLLING_FROZEN", "mapping_type": "MANDATORY", "coverage_note": "fixture", "source_freeze_record_id": "CGP005-NF-ES-CG-00-0001", "freeze_manifest_path": "fixture", "readiness_effect": "SUPPORTS_FOUNDER_REVIEW_NOT_CGP006_READY"}],
        )
        self.write_csv(
            root / "source-freeze" / "WAVE_1_SOURCE_EXCLUSION_REGISTER.csv",
            ["exclusion_id", "guide_id", "source_id", "title", "repository_path", "authority_status", "source_class", "inclusion_category", "exclusion_reason", "required_later_action", "blocks_drafting", "blocks_adoption_or_activation"],
            [],
        )
        self.write_csv(
            root / "source-freeze" / "WAVE_1_SOURCE_CONFLICT_REGISTER.csv",
            ["conflict_id", "guide_id", "source_ids", "conflict_type", "status", "freeze_treatment", "blocks_drafting", "required_later_action", "notes"],
            [],
        )
        readiness_fields = ["guide_id", "readiness_disposition", "maturity_after_cgp005", "controlling_sources_complete", "checksums_verified", "approval_basis_identified", "supersession_treatment_complete", "exclusions_recorded", "conflicts_resolved_or_retained", "repository_evidence_baseline_recorded", "drafting_questions_identified", "blocking_findings", "decision_count", "retained_gaps", "cgp006_ready", "status", "notes"]
        self.write_csv(
            root / "source-freeze" / "WAVE_1_DRAFTING_READINESS_REGISTER.csv",
            readiness_fields,
            [{"guide_id": "ES-CG-00", "readiness_disposition": "CURATED_NORMATIVE_FREEZE_READY_FOR_FOUNDER_REVIEW", "maturity_after_cgp005": "PLANNED", "controlling_sources_complete": "YES", "checksums_verified": "YES", "approval_basis_identified": "YES", "supersession_treatment_complete": "YES", "exclusions_recorded": "YES", "conflicts_resolved_or_retained": "YES", "repository_evidence_baseline_recorded": "YES", "drafting_questions_identified": "YES", "blocking_findings": "CGP005-F-0001", "decision_count": "0", "retained_gaps": "CGP005-F-0001", "cgp006_ready": "NO", "status": "REVISION_RETURNED_PENDING_FOUNDER_REVIEW", "notes": "fixture"}],
        )
        self.write_csv(
            root / "source-freeze" / "WAVE_1_REPOSITORY_EVIDENCE_BASELINE.csv",
            ["baseline_id", "guide_id", "cgp004_component_id", "repository_path", "evidence_source_ids", "evidence_class", "baseline_commit", "git_object_sha", "git_object_type", "sha256_checksum", "checksum_verification_result", "authority_treatment", "selected_for", "retained_limitations"],
            [{"baseline_id": "CGP005-REPOBASE-0001", "guide_id": "ES-CG-00", "cgp004_component_id": "CODE_GUIDE_PROGRAM_EVIDENCE", "repository_path": "docs/source.md", "evidence_source_ids": "CGSRC-TEST-0001", "evidence_class": "REPOSITORY_EVIDENCE", "baseline_commit": BASELINE, "git_object_sha": "a" * 40, "git_object_type": "BLOB", "sha256_checksum": checksum, "checksum_verification_result": "VERIFIED_FILE", "authority_treatment": "IMPLEMENTATION_EVIDENCE_ONLY", "selected_for": "fixture", "retained_limitations": "fixture"}],
        )
        for suffix in [
            "SOURCE_FREEZE_REPORT",
            "DRAFTING_READINESS_REPORT",
            "NORMATIVE_SOURCE_SELECTION_REPORT",
            "SOURCE_BURDEN_SUMMARY",
            "PACKAGE_VS_CHILD_TREATMENT_REPORT",
            "REFERENCE_CORPUS_RECONCILIATION",
        ]:
            (guide_dir / "source-freeze" / f"ES-CG-00_{suffix}.md").write_text("fixture report", encoding="utf-8")
        (guide_dir / "source-freeze" / "ES-CG-00_SOURCE_EXCLUSION_REGISTER.csv").write_text("exclusion_id,guide_id,source_id,title,repository_path,authority_status,source_class,inclusion_category,exclusion_reason,required_later_action,blocks_drafting,blocks_adoption_or_activation\n", encoding="utf-8")
        self.write_csv(
            guide_dir / "ES-CG-00_DRAFTING_QUESTION_INVENTORY.csv",
            ["question_id", "guide_id", "question_domain", "question_text", "required_for_drafting", "answer_status", "authority_basis", "blocked_by", "required_next_prompt", "notes"],
            [{"question_id": "ES-CG-00-DQ-0001", "guide_id": "ES-CG-00", "question_domain": "fixture", "question_text": "What later drafting issue remains?", "required_for_drafting": "YES", "answer_status": "UNANSWERED", "authority_basis": "CGP-005 records only.", "blocked_by": "CGP-006_NOT_ISSUED", "required_next_prompt": "CGP-006_OR_LATER", "notes": "fixture"}],
        )
        self.write_csv(
            root / "source-accession" / "MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv",
            ["mapping_id", "source_id", "guide_id", "mapping_type", "authority_status", "coverage_note", "gap_references"],
            [
                {"mapping_id": "CGMAP-0001", "source_id": "CGSRC-TEST-0001", "guide_id": "ES-CG-00", "mapping_type": "MANDATORY", "authority_status": "CONTROLLING", "coverage_note": "fixture", "gap_references": ""},
                {"mapping_id": "CGMAP-0002", "source_id": "CGSRC-TEST-0002", "guide_id": "ES-CG-00", "mapping_type": "SUPPORTING", "authority_status": "SUPPORTING", "coverage_note": "fixture unselected candidate", "gap_references": ""},
            ],
        )
        (guide_dir / "README.md").write_text("Current maturity state: `PLANNED`\nActivation state: `NOT_ACTIVE`\n", encoding="utf-8")
        self.write_csv(
            root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv",
            ["record_id", "record_type", "guide_id", "maturity_state", "prompt_status", "adoption_state", "accession_state"],
            [
                {"record_id": "ES-CG-00", "record_type": "GUIDE", "guide_id": "ES-CG-00", "maturity_state": "PLANNED", "prompt_status": "REVISION_REQUIRED", "adoption_state": "NOT_ADOPTED", "accession_state": "NOT_ACCESSIONED"},
                {"record_id": "CGP-006", "record_type": "PROGRAM_PROMPT", "guide_id": "", "maturity_state": "PLANNED", "prompt_status": "NOT_ISSUED", "adoption_state": "NOT_ADOPTED", "accession_state": "NOT_ACCESSIONED"},
            ],
        )
        return tmp, root, {"reference_register": reference_register, "guide_register": guide_register, "reference_manifest": root / "source-freeze" / "WAVE_1_REFERENCE_CORPUS_MANIFEST.json", "guide_manifest": guide_dir / "source-freeze" / "ES-CG-00_SOURCE_FREEZE_MANIFEST.json", "conflict": root / "source-freeze" / "WAVE_1_SOURCE_CONFLICT_REGISTER.csv", "exclusion": root / "source-freeze" / "WAVE_1_SOURCE_EXCLUSION_REGISTER.csv", "readiness": root / "source-freeze" / "WAVE_1_DRAFTING_READINESS_REGISTER.csv", "evidence": root / "source-freeze" / "WAVE_1_REPOSITORY_EVIDENCE_BASELINE.csv", "questions": guide_dir / "ES-CG-00_DRAFTING_QUESTION_INVENTORY.csv", "tracker": root / "registers" / "CODE_GUIDE_PROGRAM_TRACKER.csv"}

    def rewrite_source_registers(self, paths: dict[str, Path], mutate) -> None:
        for key in ["reference_register", "guide_register"]:
            fields, rows = self.read_csv(paths[key])
            mutate(rows)
            self.write_csv(paths[key], fields, rows)

    def assert_issue(self, result: validators.ValidationResult, code: str) -> None:
        self.assertEqual(result.status, "FAIL", result.to_dict())
        self.assertTrue(any(issue.code == code for issue in result.issues), result.to_dict())

    def test_current_cgp005_artifacts_validate(self):
        self.assertEqual(validators.validate_source_freeze(CODE_GUIDE_ROOT).status, "PASS")
        self.assertEqual(validators.validate_wave_1_drafting_readiness(CODE_GUIDE_ROOT).status, "PASS")

    def test_valid_minimal_source_freeze_passes(self):
        tmp, root, _ = self.build_fixture()
        with tmp:
            self.assertEqual(validators.validate_source_freeze(root, WAVE_GUIDE).status, "PASS")
            self.assertEqual(validators.validate_wave_1_drafting_readiness(root, WAVE_GUIDE).status, "PASS")

    def test_missing_checksum_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            self.rewrite_source_registers(paths, lambda rows: rows[0].update({"sha256_checksum": ""}))
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "missing_sha256_checksum")

    def test_incorrect_checksum_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            self.rewrite_source_registers(paths, lambda rows: rows[0].update({"sha256_checksum": "0" * 64}))
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "checksum_mismatch")

    def test_directory_only_controlling_reference_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            source_dir = root.parents[2] / "docs" / "source-dir"
            source_dir.mkdir()
            (source_dir / "a.md").write_text("directory source\n", encoding="utf-8")
            checksum = validators._sha256_tree_for(root.parents[2], "docs/source-dir")
            def mutate(rows: list[dict[str, str]]) -> None:
                rows[0].update({"repository_path": "docs/source-dir", "sha256_checksum": checksum, "checksum_verification_result": "VERIFIED_DIRECTORY_AGGREGATE", "git_object_type": "TREE", "package_manifest_path": ""})
            self.rewrite_source_registers(paths, mutate)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "directory_only_controlling_reference")

    def test_controlling_without_approval_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            self.rewrite_source_registers(paths, lambda rows: rows[0].update({"approval_record_path": ""}))
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "controlling_source_without_approval_record_path")

    def test_non_authority_sources_marked_controlling_fail(self):
        for source_class in ["REPOSITORY_EVIDENCE", "HISTORICAL_PREDECESSOR", "PROPOSED_NOT_ADOPTED"]:
            with self.subTest(source_class=source_class):
                tmp, root, paths = self.build_fixture()
                with tmp:
                    self.rewrite_source_registers(paths, lambda rows: rows[0].update({"source_class": source_class}))
                    self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "non_authority_marked_controlling")

    def test_duplicate_inconsistent_bytes_fail(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["reference_register"])
            duplicate = {**rows[0], "freeze_record_id": "CGP005-RC-0002", "sha256_checksum": "1" * 64}
            rows.append(duplicate)
            self.write_csv(paths["reference_register"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "duplicate_inconsistent_source")

    def test_manifest_omission_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            payload = json.loads(paths["reference_manifest"].read_text(encoding="utf-8"))
            payload["sources"] = []
            paths["reference_manifest"].write_text(json.dumps(payload), encoding="utf-8")
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "manifest_omission")

    def test_unresolved_conflict_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            self.write_csv(
                paths["conflict"],
                ["conflict_id", "guide_id", "source_ids", "conflict_type", "status", "freeze_treatment", "blocks_drafting", "required_later_action", "notes"],
                [{"conflict_id": "CGCON-9999", "guide_id": "ES-CG-00", "source_ids": "CGSRC-TEST-0001", "conflict_type": "AUTHORITY_AMBIGUITY", "status": "OPEN", "freeze_treatment": "fixture", "blocks_drafting": "YES", "required_later_action": "fixture", "notes": "fixture"}],
            )
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "unresolved_source_conflict")

    def test_excluded_source_without_rationale_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            self.write_csv(
                paths["exclusion"],
                ["exclusion_id", "guide_id", "source_id", "title", "repository_path", "authority_status", "source_class", "inclusion_category", "exclusion_reason", "required_later_action", "blocks_drafting", "blocks_adoption_or_activation"],
                [{"exclusion_id": "CGP005-EXCL-9999", "guide_id": "ES-CG-00", "source_id": "CGSRC-TEST-0001", "title": "fixture", "repository_path": "docs/source.md", "authority_status": "PROPOSED", "source_class": "PROPOSED_NOT_ADOPTED", "inclusion_category": "EXCLUDED_PROPOSED", "exclusion_reason": "", "required_later_action": "fixture", "blocks_drafting": "NO", "blocks_adoption_or_activation": "YES"}],
            )
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "missing_exclusion_rationale")

    def test_stale_baseline_commit_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["evidence"])
            rows[0]["baseline_commit"] = "c" * 40
            self.write_csv(paths["evidence"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "stale_baseline_commit")

    def test_bulk_source_map_passthrough_manifest_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            payload = json.loads(paths["guide_manifest"].read_text(encoding="utf-8"))
            payload["curation_method"] = "CGP003_MAPPING_PASSTHROUGH"
            paths["guide_manifest"].write_text(json.dumps(payload), encoding="utf-8")
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "bulk_source_map_passthrough")

    def test_boilerplate_inclusion_rationale_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["guide_register"])
            rows[0]["reason_for_inclusion"] = "mapped to guide"
            self.write_csv(paths["guide_register"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "generic_inclusion_rationale")

    def test_irrelevant_implementation_evidence_without_component_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["guide_register"])
            rows[0].update({"source_class": "REPOSITORY_EVIDENCE", "inclusion_category": "IMPLEMENTATION_EVIDENCE_FROZEN", "authority_status": "SUPPORTING", "necessity_test": "NECESSARY_IMPLEMENTATION_EVIDENCE", "cgp004_component_ids": ""})
            self.write_csv(paths["guide_register"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "implementation_evidence_without_component")

    def test_unnecessary_package_child_promotion_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["guide_register"])
            rows[0]["package_level_source_could_replace"] = "YES"
            self.write_csv(paths["guide_register"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "unnecessary_package_child_promotion")

    def test_reference_corpus_in_normative_freeze_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["guide_register"])
            rows[0]["inclusion_category"] = "REFERENCE_CORPUS_INDEXED_NOT_NORMATIVE"
            self.write_csv(paths["guide_register"], fields, rows)
            self.assert_issue(validators.validate_source_freeze(root, WAVE_GUIDE), "reference_corpus_treated_as_normative")

    def test_missing_drafting_question_inventory_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            paths["questions"].unlink()
            self.assert_issue(validators.validate_wave_1_drafting_readiness(root, WAVE_GUIDE), "missing_drafting_question_inventory")

    def test_source_frozen_maturity_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["readiness"])
            rows[0].update({"maturity_after_cgp005": "SOURCE_FROZEN", "cgp006_ready": "YES"})
            self.write_csv(paths["readiness"], fields, rows)
            fields, tracker = self.read_csv(paths["tracker"])
            tracker[0]["maturity_state"] = "SOURCE_FROZEN"
            self.write_csv(paths["tracker"], fields, tracker)
            self.assert_issue(validators.validate_wave_1_drafting_readiness(root, WAVE_GUIDE), "premature_source_frozen_maturity")

    def test_source_frozen_missing_artifact_fails(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["readiness"])
            rows[0]["maturity_after_cgp005"] = "SOURCE_FROZEN"
            self.write_csv(paths["readiness"], fields, rows)
            (root / "guides" / "ES-CG-00" / "source-freeze" / "ES-CG-00_SOURCE_FREEZE_MANIFEST.json").unlink()
            self.assert_issue(validators.validate_wave_1_drafting_readiness(root, WAVE_GUIDE), "source_frozen_missing_artifact")

    def test_blocked_by_custody_readiness_is_consistent_when_not_cgp006_ready(self):
        tmp, root, paths = self.build_fixture()
        with tmp:
            fields, rows = self.read_csv(paths["readiness"])
            rows[0].update({"readiness_disposition": "BLOCKED_BY_SOURCE_CUSTODY", "maturity_after_cgp005": "PLANNED", "blocking_findings": "1", "cgp006_ready": "NO", "status": "BLOCKED"})
            self.write_csv(paths["readiness"], fields, rows)
            result = validators.validate_wave_1_drafting_readiness(root, WAVE_GUIDE)
            self.assertEqual(result.status, "PASS", result.to_dict())


if __name__ == "__main__":
    unittest.main()
