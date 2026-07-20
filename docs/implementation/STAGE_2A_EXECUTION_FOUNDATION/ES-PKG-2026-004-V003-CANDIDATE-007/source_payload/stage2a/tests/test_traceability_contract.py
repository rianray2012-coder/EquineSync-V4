from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import traceability_contract as contract
from validate_stage2a_package import (
    csv_parity_errors,
    load_source_module,
    process_evidence_errors,
    provider_evidence_errors,
    record_check,
    traceability_errors,
)


class TraceabilityContractTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        source_paths: set[str] = set()
        for _number, _controls, sources, implementations, _tests, _evidence in contract.REQUIREMENT_SPECS:
            source_paths.update(sources); source_paths.update(implementations)
        source_paths.update(path for _identity, path in contract.TEST_SPECS.values())
        self.source_by_path = {path: contract.source_evidence_id(path) for path in sorted(source_paths)}
        self.source_register = {"sources": [
            {"path": path, "evidence_id": evidence_id} for path, evidence_id in self.source_by_path.items()
        ]}
        for path in self.source_by_path:
            target = self.root / "source_payload" / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("\n".join([
                "def test_independent_semantic_projection_rejects_over_redaction(): pass",
                "def test_process_identity_fails_closed_on_command_or_group_conflict(): pass",
                "def test_provider_events_are_process_bound_hash_chained_and_attributable(): pass",
                "def test_combined_bogus_output_mapping_is_rejected(): pass",
            ]) + "\n", encoding="utf-8")
        for name in contract.OUTPUT_REQUIREMENT_MAP:
            (self.root / name).write_text("\n", encoding="utf-8")
        foundation_checks = sorted({
            identity.split(":", 1)[1].split(".", 1)[0]
            for identity, _path in contract.TEST_SPECS.values()
            if identity.startswith("FOUNDATION_VALIDATION.check:")
        })
        (self.root / "STAGE2A_FOUNDATION_VALIDATION.json").write_text(json.dumps({
            "checks": [{"check": name, "status": "PASS"} for name in foundation_checks]
        }), encoding="utf-8")
        (self.root / "STAGE2A_VALIDATION_COMMAND_REGISTER.json").write_text(json.dumps({
            "commands": [{"command_id": f"S2A-CMD-{number:03d}"} for number in range(1, 8)]
        }), encoding="utf-8")
        self.tests = contract.test_rows(self.source_by_path)
        self.requirements = contract.requirement_rows(contract.GAP_TITLES, self.source_by_path)
        self.findings = contract.finding_rows()
        self.trace = contract.output_rows(sorted(contract.OUTPUT_REQUIREMENT_MAP), self.requirements, self.source_by_path)
        self.test_register = {"tests": deepcopy(self.tests)}
        self.requirement_matrix = {"requirements": deepcopy(self.requirements)}
        self.finding_matrix = {"findings": deepcopy(self.findings)}
        self.trace_register = {"outputs": deepcopy(self.trace)}
        self._write_csvs()

    def tearDown(self):
        self.temporary.cleanup()

    def _write_csvs(self):
        with (self.root / "STAGE2A_TEST_CONTROL_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(self.tests[0])); writer.writeheader(); writer.writerows(self.tests)
        requirement_rows = [{
            "requirement_id": row["requirement_id"], "gap_id": row["gap_id"],
            "control_ids": "|".join(row["control_ids"]), "source_evidence_ids": "|".join(row["source_evidence_ids"]),
            "implementation_artifacts": "|".join(row["implementation_artifacts"]), "test_ids": "|".join(row["test_ids"]),
            "evidence_artifacts": "|".join(row["evidence_artifacts"]), "status": row["status"],
        } for row in self.requirements]
        with (self.root / "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(requirement_rows[0])); writer.writeheader(); writer.writerows(requirement_rows)
        finding_rows = [{
            "finding_id": row["finding_id"], "blocker_classification": row["blocker_classification"],
            "requirement_ids": "|".join(row["requirement_ids"]), "remediation_artifacts": "|".join(row["remediation_artifacts"]),
            "test_ids": "|".join(row["test_ids"]), "evidence_artifacts": "|".join(row["evidence_artifacts"]),
            "status": row["status"], "self_closed": row["self_closed"],
        } for row in self.findings]
        with (self.root / "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(finding_rows[0])); writer.writeheader(); writer.writerows(finding_rows)

    def errors(self, tests=None, requirements=None, findings=None, trace=None):
        return traceability_errors(
            self.root, self.source_register,
            tests or self.test_register, requirements or self.requirement_matrix,
            findings or self.finding_matrix, trace or self.trace_register, contract,
        )

    def test_canonical_relationships_pass(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(csv_parity_errors(self.root, self.tests, self.requirements, self.findings), [])

    def test_requirement_mutations_are_rejected(self):
        for field, value in (("gap_id", "S2-GAP-001"), ("control_ids", ["BOGUS-CONTROL"]), ("test_ids", ["S2A-TEST-TOOLCHAIN"]), ("status", "CLOSED")):
            mutated = deepcopy(self.requirement_matrix); mutated["requirements"][8][field] = value
            with self.subTest(field=field): self.assertTrue(self.errors(requirements=mutated))

    def test_test_and_finding_mutations_are_rejected(self):
        tests = deepcopy(self.test_register); tests["tests"][0]["executable_identity"] = "BOGUS"
        self.assertTrue(self.errors(tests=tests))
        findings = deepcopy(self.finding_matrix); findings["findings"][0]["self_closed"] = True
        self.assertTrue(self.errors(findings=findings))
        findings = deepcopy(self.finding_matrix); findings["findings"][2]["requirement_ids"] = ["S2A-REQ-001"]
        self.assertTrue(self.errors(findings=findings))

    def test_combined_bogus_output_mapping_is_rejected(self):
        mutated = deepcopy(self.trace_register)
        row = next(row for row in mutated["outputs"] if row["output"] == "PROVIDER_DENIAL_REGISTER.json")
        row.update({
            "control_ids": ["BOGUS-CONTROL"], "gap_ids": ["S2-GAP-001"],
            "finding_ids": ["BOGUS-FINDING"], "test_ids": ["S2A-TEST-TOOLCHAIN"],
            "artifact_role": "BOGUS", "mapping_rationale": "arbitrary", "verification_rule": "nonempty",
        })
        self.assertTrue(self.errors(trace=mutated))

    def test_each_output_relationship_field_is_contract_enforced(self):
        fields = {
            "mapping_id": "S2A-MAP-BOGUS", "source_evidence_ids": [next(iter(self.source_by_path.values()))],
            "implementation_artifacts": [next(iter(self.source_by_path))], "evidence_artifacts": ["ASSURANCE_STATEMENT.md"],
        }
        for field, value in fields.items():
            mutated = deepcopy(self.trace_register); mutated["outputs"][0][field] = value
            with self.subTest(field=field): self.assertTrue(self.errors(trace=mutated))

    def test_csv_parity_mutation_is_rejected(self):
        path = self.root / "STAGE2A_TEST_CONTROL_REGISTER.csv"
        path.write_text(path.read_text().replace("S2A-TEST-CONTROLLED-SHUTDOWN", "S2A-TEST-BOGUS", 1), encoding="utf-8")
        self.assertTrue(csv_parity_errors(self.root, self.tests, self.requirements, self.findings))

    def test_duplicate_validation_identifier_hard_fails(self):
        checks: list[dict[str, object]] = []; seen: set[str] = set()
        record_check(checks, seen, "MV-X", True, {})
        with self.assertRaisesRegex(RuntimeError, "duplicate validation check identifier"):
            record_check(checks, seen, "MV-X", True, {})

    def test_detached_source_module_load_is_read_only(self):
        module_path = self.root / "detached_module.py"
        module_path.write_text("VALUE = 1\n", encoding="utf-8")
        module = load_source_module(module_path, "stage2a_test_detached_module")
        self.assertEqual(module.VALUE, 1)
        self.assertFalse((self.root / "__pycache__").exists())

    def test_packaged_provider_and_process_evidence_mutations_fail_closed(self):
        repo = Path(__file__).resolve().parents[2]
        candidate = repo / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-006"
        foundation = json.loads((candidate / "STAGE2A_FOUNDATION_VALIDATION.json").read_text(encoding="utf-8"))
        source = json.loads((candidate / "STAGE2A_SOURCE_EVIDENCE_REGISTER.json").read_text(encoding="utf-8"))
        source_paths = {row["path"] for row in source["sources"]}
        source_ids = {row["evidence_id"] for row in source["sources"]}
        registry_path = repo / "stage2a/provider-capability-registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry_sha = __import__("hashlib").sha256(registry_path.read_bytes()).hexdigest()
        checks = {row["check"]: row for row in foundation["checks"]}
        provider = checks["provider_denial"]["detail"]
        ledger = foundation["artifacts"]["application_network_guard"]
        self.assertEqual(provider_evidence_errors(
            ledger, registry, registry_sha, provider["register"],
            provider["provider_guard_proof"], source_paths, source_ids,
        ), [])
        emptied = deepcopy(ledger)
        emptied["provider_events"] = []
        emptied["event_count"] = 0
        emptied["event_chain_sha256"] = "0" * 64
        self.assertTrue(provider_evidence_errors(
            emptied, registry, registry_sha, provider["register"],
            provider["provider_guard_proof"], source_paths, source_ids,
        ))
        process_detail = checks["process_identity"]["detail"]
        shutdown_detail = checks["controlled_shutdown"]["detail"]
        self.assertEqual(process_evidence_errors(foundation, process_detail, shutdown_detail), [])
        for field, value in (("command_line_sha256", "0" * 64), ("working_directory", "REPOSITORY_ROOT")):
            mutated = deepcopy(process_detail)
            mutated["api_identity"][field] = value
            with self.subTest(field=field):
                self.assertTrue(process_evidence_errors(foundation, mutated, shutdown_detail))


if __name__ == "__main__":
    unittest.main()
