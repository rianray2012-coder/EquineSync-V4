#!/usr/bin/env python3
"""Finalize the R3 ES-REV-2026-022 runtime-blocked evidence package."""

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
PACKAGE = REPO / "governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE"
DISPOSITION = "FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE"
R2_COMMIT = "56b0a88722d983e05baec0d3b1ea5b7b88c24001"
R2_TREE = "a60e900c2d0eef17c1f1b8a98f01f5ff1e30647d"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name: str, body: str) -> None:
    normalized = "\n".join(line.rstrip() for line in body.strip().splitlines()) + "\n"
    (PACKAGE / name).write_text(normalized, encoding="utf-8")


final_disposition = """
# Final Structured Review Disposition

**Package:** `ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE`
**Package revision:** `1.0.1-R3`
**Review input:** byte-unchanged R2 commit `56b0a88722d983e05baec0d3b1ea5b7b88c24001`
**Review cycle:** `ES-REV-2026-022`
**Disposition:** `FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE`
**Cross-agent completion gate:** `FAIL`
**Implementation authority:** `false`
**Adopted:** `false`
**Locked:** `false`

## Outcome

The exact R2 input reproduced before the review attempt: 66 files, the expected manifest digest, all package checksums, 25/25 existing deterministic package checks, zero sealed-source modifications, 39/39 original relied-source hashes from exact Git objects, zero mandatory exact-source gaps, explicit Identity and Relationships successor segregation, and the R2 machine-readable parity correction.

The fresh structured review did not begin. The live parent runtime was unrestricted/danger-full-access equivalent with `approval_policy=never` and network enabled. Repository control requires read-only/on-request/network-disabled for documentary roles and isolated bounded workspace-write/on-request/network-disabled for writable roles. The Founder granted no broad exception. Six complete pre-spawn records were created before any role start; all six were `FAIL`, and zero formal roles started.

Therefore no valid fresh segregated, adversarial, domain, machine, evidence-custody, or synthetic documentary conclusion exists. Cross-review discrepancy reconciliation could not compare independent conclusions, and the cross-agent completion gate fails. R3 records the blocked cycle; it does not modify the R2 design content or convert the blocked review into a completed review.

## Review-function status

| Function | Run ID | Status | Formal coverage | Attestation |
| --- | --- | --- | ---: | --- |
| Segregated | ES-REV-2026-022-RA02-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Adversarial | ES-REV-2026-022-RA03-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Domain | ES-REV-2026-022-RA06-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Machine | ES-REV-2026-022-RA04-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Evidence custody | ES-REV-2026-022-RA05-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Synthetic documentary | ES-REV-2026-022-RA07-01 | NOT_STARTED_PERMISSION_CHECK_FAILED | 0% | Not issued |
| Cross-review discrepancy | ES-REV-2026-022-DISC-001 | FORMAL_RECONCILIATION_NOT_PERFORMED | 0% | Not applicable |
| Orchestrator synthesis | administrative blockage record | COMPLETED_WITH_LIMITATION | runtime block only | Not a role attestation |

## Findings

- P0: 0 open, 0 closed.
- P1: 4 open or unresolved, 0 closed.
- P2: 2 open and not freshly reassessed, 0 closed.
- P3: 1 open and not freshly reassessed, 0 closed.

Status of prior P1 findings:

- `ES-REV-2026-021-ORCH-F-0001`: `OPEN_RECURRED_IN_ES_REV_2026_022`; permission prerequisites again failed, but this time the stop occurred before spawn.
- `ES-REV-2026-021-MV-F-0001`: `REMEDIATED_UNVERIFIED`; R2 intake parity checks pass, but the formal Machine Validation role did not start.
- `ES-REV-2026-021-INH-F-0001`: `OPEN_NOT_REASSESSED_PERMISSION_BLOCKED`; this cycle did not determine whether its effect is adoption-review blocking or implementation-only.
- `ES-REV-2026-021-INH-F-0002`: `OPEN_NOT_REASSESSED_PERMISSION_BLOCKED`; this cycle did not determine its documentary boundary, and executable testing was not authorized.

Adoption-review readiness is blocked by the incomplete review and failed cross-agent completion gate. This cycle does not use the open historical findings to make a new substantive readiness determination.

## Machine evidence boundary

The final package assembly validator passes its mechanical checks, including R3 metadata parity and fail-closed permission-record parity. That root-run packaging validation is not an ES-RA-04 run, does not close `ES-REV-2026-021-MV-F-0001`, and does not establish substantive design correctness or implementation behavior.

## Required next action

Start a new review cycle in a runtime that can expose and preserve read-only/on-request/network-disabled reviewer sessions and isolated bounded workspace-write/on-request/network-disabled writable sessions. Create a complete `PASS` record before every role. Freshly run all required functions, then reconcile discrepancies and reassess every carried finding.

## Authority boundary

Implementation authority remains false. No implementation, application-code change, database or schema change, migration, application or service start, executable golden-path run, enrollment, production activity, PR, merge, tag, release, deployment, activation, adoption, lock, or unrelated-finding closure occurred or is authorized. The current Identity and Relationships successor text remains separate and is not represented as Founder-approved.
"""
write("FINAL_STRUCTURED_REVIEW_DISPOSITION.md", final_disposition)
write("REVIEW_DISPOSITION.md", final_disposition)

write(
    "CHANGE_MANIFEST.txt",
    """
PACKAGE: ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE
REVIEW CYCLE: ES-REV-2026-022
REVISION: 1.0.1-R3
EXACT R2 INPUT COMMIT: 56b0a88722d983e05baec0d3b1ea5b7b88c24001
EXACT R2 INPUT TREE: a60e900c2d0eef17c1f1b8a98f01f5ff1e30647d
R2 INPUT MANIFEST SHA-256: fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527
DISPOSITION: FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE

R2 INPUT VERIFICATION
- Verified the exact 66-file R2 input before review-cycle output changed.
- Reproduced every R2 checksum and the 25/25 R2 package validator result.
- Reproduced 39/39 original relied-source hashes from exact commit objects.
- Confirmed zero sealed-source modifications, zero mandatory exact-source gaps, explicit Identity and Relationships separation, and R2 machine-readable correction parity.

R3 REVIEW-CYCLE EVIDENCE
- Updated REVIEW_AUTHORIZATION.md for ES-REV-2026-022.
- Replaced RUNTIME_PERMISSION_RECORDS.csv with six complete pre-spawn FAIL records created before role launch.
- Replaced all six role reports with fresh NOT_STARTED_PERMISSION_CHECK_FAILED reports; zero substantive role outputs are claimed.
- Updated discrepancy, findings, correction, traceability, scope, completeness, claim, omission, attempt, and output registers.
- Added ES_REV_2026_021_TO_ES_REV_2026_022_REVIEW_CYCLE_RECONCILIATION.md.
- Preserved every prior P1/P2/P3 finding without formal closure or fresh substantive reassessment.
- Updated machine-readable metadata and deterministic validator controls for the runtime-blocked R3 state.
- Regenerated package inventory, manifest, checksums, validation evidence, and final disposition.

DESIGN AND AUTHORITY BOUNDARY
- R3 contains review-cycle evidence only; it makes no Facility PIA design correction.
- FAC-FD-001 through FAC-FD-018 remain recorded as Founder-approved design direction only.
- Implementation authority remains false.
- No implementation, code/database/schema/migration change, startup, executable review, enrollment, production, PR, merge, tag, release, deployment, adoption, or lock occurred.
- Sealed source evidence remains unchanged.
""",
)

change_log = (PACKAGE / "CHANGE_CONTROL_LOG.md").read_text(encoding="utf-8")
marker = "## 2026-07-21 - ES-REV-2026-022 runtime-permission block"
if marker not in change_log:
    change_log = change_log.rstrip() + "\n\n" + marker + "\n\n"
    change_log += "Created complete role-specific permission records before any formal spawn. All six failed under the unrestricted/never/network-enabled parent, so no role started. Advanced review evidence from R2 to R3, preserved the exact R2 input commit, retained every historical finding without closure, and assigned `FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE`. No design, implementation, adoption, or lock authority changed.\n"
    (PACKAGE / "CHANGE_CONTROL_LOG.md").write_text(change_log, encoding="utf-8")

main_doc = PACKAGE / "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_1_FOUNDER_DECISION_INCORPORATED_REVIEW_CANDIDATE.md"
text = main_doc.read_text(encoding="utf-8").replace("**Review cycle:** `ES-REV-2026-021`", "**Review cycle:** `ES-REV-2026-022`")
if "**Package revision:**" not in text:
    text = text.replace("**Version:** `1.0.1`\n", "**Version:** `1.0.1`\n**Package revision:** `1.0.1-R3`\n")
main_doc.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")

decision_register = PACKAGE / "FOUNDER_DECISION_REGISTER.md"
text = decision_register.read_text(encoding="utf-8").replace("**Review cycle:** `ES-REV-2026-021`", "**Review cycle:** `ES-REV-2026-022`")
text = text.replace("Review status: fresh structured review pending at the design freeze.", "Review status: ES-REV-2026-022 blocked before all formal roles by runtime permission failure.")
decision_register.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")

golden_paths = PACKAGE / "GOLDEN_PATHS.md"
text = golden_paths.read_text(encoding="utf-8").replace(
    "**Review cycle:** `ES-REV-2026-021`",
    "**Originating cycle:** `ES-REV-2026-021`\n**ES-REV-2026-022 treatment:** `HISTORICAL_INPUT_NOT_FRESHLY_REVIEWED`",
)
golden_paths.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")

trace_path = PACKAGE / "FOUNDER_DECISION_TRACEABILITY_MATRIX.csv"
with trace_path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
fields = list(rows[0])
for row in rows:
    row["review_result_ids"] = "ES-REV-2026-021-ORCH-F-0001;ES-REV-2026-022-DISC-001;FINAL_STRUCTURED_REVIEW_DISPOSITION"
    row["implementation_authority"] = "FALSE"
with trace_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

machine_path = PACKAGE / "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json"
machine = json.loads(machine_path.read_text(encoding="utf-8"))
machine.update({
    "branch": "codex/facility-pia-r2-compliant-structured-review-v1",
    "candidate_commit": R2_COMMIT,
    "design_freeze_commit": R2_COMMIT,
    "design_freeze_tree": R2_TREE,
    "disposition": DISPOSITION,
    "package_revision": "1.0.1-R3",
    "package_run_id": "ES-PKG-2026-022-V101-R3",
    "review_cycle_id": "ES-REV-2026-022",
    "review_blocked": True,
    "review_blocker": "RUNTIME_PERMISSION_FAILURE",
    "review_complete": False,
    "custom_agent_execution_claimed": False,
    "implementation_authority": False,
    "implementation_activity": False,
    "migration_activity": False,
    "application_started": False,
    "service_started": False,
    "deployment_activity": False,
    "enrollment_or_production_activity": False,
    "adopted": False,
    "locked": False,
})
machine["review_runtime"] = {
    "parent_permission_mode": "unrestricted/danger-full-access equivalent",
    "parent_approval_policy": "never",
    "parent_network_status": "enabled",
    "exception_reference": "NONE",
    "pre_spawn_records": 6,
    "pre_spawn_pass": 0,
    "pre_spawn_fail": 6,
    "formal_roles_started": 0,
    "actual_reviewer_mode": "NOT_OBSERVED_ROLE_NOT_SPAWNED",
    "runtime_disposition": "PERMISSION_CHECK_FAILED_BEFORE_SPAWN",
}
machine_path.write_text(json.dumps(machine, indent=2, sort_keys=True) + "\n", encoding="utf-8")

evidence_path = PACKAGE / "EVIDENCE_MANIFEST.json"
evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
evidence.update({
    "review_cycle_id": "ES-REV-2026-022",
    "review_disposition": DISPOSITION,
    "formal_review_valid": False,
    "package_revision": "1.0.1-R3",
    "sealed_source_modifications": 0,
    "implementation_authority": False,
    "implementation_activity": False,
    "adopted": False,
    "locked": False,
    "original_relied_source_count": 39,
    "original_relied_sources_verified": 39,
    "exact_review_input": {
        "commit": R2_COMMIT,
        "tree": R2_TREE,
        "file_count": 66,
        "manifest_sha256": "fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527",
        "bytes_unchanged_before_review": True,
    },
    "fresh_review_authorization": {
        "sha256": "7c49bf8157d8c3bf3966d1669a3719de54bdf7ad195e1cfd5edfc94a38a529c6",
        "preservation": "external Codex attachment; digest recorded in REVIEW_AUTHORIZATION.md",
    },
    "permission_gate": {"records": 6, "pass": 0, "fail": 6, "roles_started": 0},
})
evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_manifests() -> None:
    excluded_inventory = {"PACKAGE_FILE_INVENTORY.csv", "PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "CHECKSUM_MANIFEST.sha256"}
    inventory_paths = sorted(p for p in PACKAGE.rglob("*") if p.is_file() and p.relative_to(PACKAGE).as_posix() not in excluded_inventory)
    inventory_lines = ["path,bytes,sha256,classification,stage"]
    for path in inventory_paths:
        rel = path.relative_to(PACKAGE).as_posix()
        inventory_lines.append(f"{rel},{path.stat().st_size},{digest(path)},REVIEW_EVIDENCE_PACKAGE_ARTIFACT,REVIEW_RUNTIME_PERMISSION_BLOCKED_FINAL_R3")
    (PACKAGE / "PACKAGE_FILE_INVENTORY.csv").write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")

    old_manifest = json.loads((PACKAGE / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest_paths = sorted(p for p in PACKAGE.rglob("*") if p.is_file() and p.name not in {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "CHECKSUM_MANIFEST.sha256"})
    old_manifest.update({
        "schema_version": "1.3.0",
        "package_revision": "1.0.1-R3",
        "branch": "codex/facility-pia-r2-compliant-structured-review-v1",
        "review_cycle_id": "ES-REV-2026-022",
        "starting_commit": R2_COMMIT,
        "design_freeze_commit": R2_COMMIT,
        "design_freeze_tree": R2_TREE,
        "predecessor_commit": "a5cf78295ad43cde7f73e383b3d5e98a11000382",
        "r2_input_commit": R2_COMMIT,
        "r2_input_tree": R2_TREE,
        "r2_input_manifest_sha256": "fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527",
        "r2_input_bytes_unchanged_before_review": True,
        "disposition": DISPOSITION,
        "stage": "REVIEW_RUNTIME_PERMISSION_BLOCKED_FINAL_EVIDENCE_PACKAGE",
        "permission_control_result": "PERMISSION_CHECK_FAILED_BEFORE_SPAWN",
        "reviewer_permission_records": {"records": 6, "pass": 0, "fail": 6, "roles_started": 0},
        "formal_review_functions_completed": 0,
        "formal_review_valid": False,
        "custom_agent_execution_claimed": False,
        "sealed_source_modification_count": 0,
        "mandatory_exact_source_gap_count": 0,
        "identity_relationships_successor_founder_approved": False,
        "implementation_authority": False,
        "implementation_activity": False,
        "migration_activity": False,
        "application_or_service_started": False,
        "deployment_activity": False,
        "enrollment_or_production_activity": False,
        "pull_request_created": False,
        "merged": False,
        "tag_created": False,
        "adopted": False,
        "locked": False,
        "open_findings": {"P0": 0, "P1": 4, "P2": 2, "P3": 1},
        "corrected_unverified_findings": {"P1": 1},
        "file_count_excluding_manifest_and_checksums": len(manifest_paths),
        "files": [{"path": p.relative_to(PACKAGE).as_posix(), "bytes": p.stat().st_size, "sha256": digest(p)} for p in manifest_paths],
    })
    (PACKAGE / "PACKAGE_MANIFEST.json").write_text(json.dumps(old_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checksum_paths = sorted(p for p in PACKAGE.rglob("*") if p.is_file() and p.name not in {"CHECKSUMS.sha256", "CHECKSUM_MANIFEST.sha256"})
    sums = "".join(f"{digest(path)}  {path.relative_to(PACKAGE).as_posix()}\n" for path in checksum_paths)
    (PACKAGE / "CHECKSUMS.sha256").write_text(sums, encoding="utf-8")
    (PACKAGE / "CHECKSUM_MANIFEST.sha256").write_text(sums, encoding="utf-8")


write(
    "VALIDATION_COMMAND_LOG.txt",
    """
Review cycle: ES-REV-2026-022
Package revision: 1.0.1-R3
Run type: ORCHESTRATOR_PACKAGE_ASSEMBLY_CHECK; NOT FORMAL ES-RA-04

Immutable R2 intake:
- git rev-parse HEAD -> 56b0a88722d983e05baec0d3b1ea5b7b88c24001
- find package -type f | wc -l -> 66
- sha256 PACKAGE_MANIFEST.json -> fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527
- sha256 prior blocked ZIP -> f99bbe6de544b1bd688b0c283a75608471c499c63d6745f595f1e522756cd5a8
- shasum -a 256 -c CHECKSUMS.sha256 -> all OK
- python PIA_PACKAGE_VALIDATOR.py -> 25/25 PASSED
- 39 original relied sources verified from exact R2 Git objects -> 39/39

Preserved method correction:
- A filesystem-only relied-source check found 5/39 because the clone is sparse.
- The check was rerun against exact Git objects at the R2 commit and found 39/39.
- Sparse worktree absence was not misclassified as source provenance failure.

Permission gate:
- pre-spawn records -> 6
- PASS -> 0
- FAIL -> 6
- roles started -> 0

R3 finalization:
- python PIA_PACKAGE_VALIDATOR.py -> expected 29/29 PASSED packaging checks
- shasum -a 256 -c CHECKSUMS.sha256 -> expected all OK

Limitations:
- No formal Machine Validation Agent ran.
- No executable behavior or implementation was tested.
- A packaging-validator pass does not close ES-REV-2026-021-MV-F-0001 or establish substantive review completion.
""",
)

# Seed validation evidence, build manifests, execute the deterministic package checker, then
# replace the seed evidence and rebuild to account for its exact final bytes.
write("VALIDATION_REPORT.md", "# Validation Report\n\nPending final package assembly validation.\n")
(PACKAGE / "VALIDATION_REPORT.json").write_text(json.dumps({"status": "PENDING_FINAL_PACKAGE_ASSEMBLY"}, indent=2) + "\n", encoding="utf-8")
build_manifests()

proc = subprocess.run([sys.executable, "PIA_PACKAGE_VALIDATOR.py"], cwd=PACKAGE, text=True, capture_output=True)
if proc.returncode != 0:
    print(proc.stdout)
    print(proc.stderr, file=sys.stderr)
    raise SystemExit(proc.returncode)
validator = json.loads(proc.stdout)
validation = {
    "schema_version": "1.1.0",
    "review_cycle_id": "ES-REV-2026-022",
    "package_revision": "1.0.1-R3",
    "run_type": "ORCHESTRATOR_PACKAGE_ASSEMBLY_CHECK",
    "formal_machine_agent_run": False,
    "formal_review_completed": False,
    "permission_gate": {"records": 6, "pass": 0, "fail": 6, "roles_started": 0},
    "prior_finding": {"finding_id": "ES-REV-2026-021-MV-F-0001", "status": "REMEDIATED_UNVERIFIED"},
    "result": validator["result"],
    "checks_executed": validator["checks_executed"],
    "checks_passed": validator["checks_passed"],
    "checks_failed": validator["checks_failed"],
    "environment": validator["environment"],
    "checks": validator["checks"],
    "limitations": [
        "No formal ES-RA-04 role ran.",
        "No independent review or executable behavior was tested.",
        "Passing package checks do not establish substantive correctness or finding closure.",
    ],
}
(PACKAGE / "VALIDATION_REPORT.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
write(
    "VALIDATION_REPORT.md",
    f"""
# Validation Report

**Review cycle:** `ES-REV-2026-022`
**Package revision:** `1.0.1-R3`
**Run type:** `ORCHESTRATOR_PACKAGE_ASSEMBLY_CHECK`
**Formal ES-RA-04 run:** `false`
**Result:** `{validator['result']}`

## Results

- Checks executed: {validator['checks_executed']}
- Checks passed: {validator['checks_passed']}
- Checks failed: {validator['checks_failed']}
- Permission records: 6
- Permission checks passed: 0
- Permission checks failed: 6
- Formal roles started: 0

The deterministic checks cover file registration and hashes, checksum aliases, authorized file types, 18 decision records, 55 requirements, 55 acceptance criteria, 85 tests, 18 decision-trace rows, positive/negative/boundary design mappings, permission-matrix parity, sealed-source hashes, source-gap parity, no unresolved Founder-decision status, authority booleans, Identity and Relationships segregation, required outputs, finding severities, R3 metadata parity, fail-closed permission-record parity, blocked role-report parity, and final-disposition parity.

## Boundary

This is an orchestrator package-assembly check, not independent Machine Validation. It does not establish substantive design correctness, executable behavior, implementation coverage, adoption readiness, or closure of `ES-REV-2026-021-MV-F-0001`, which remains `REMEDIATED_UNVERIFIED`.
""",
)
build_manifests()

final_proc = subprocess.run([sys.executable, "PIA_PACKAGE_VALIDATOR.py"], cwd=PACKAGE, text=True, capture_output=True)
if final_proc.returncode != 0:
    print(final_proc.stdout)
    print(final_proc.stderr, file=sys.stderr)
    raise SystemExit(final_proc.returncode)
final = json.loads(final_proc.stdout)
if (final["checks_executed"], final["checks_passed"], final["checks_failed"]) != (
    validation["checks_executed"], validation["checks_passed"], validation["checks_failed"]
):
    raise SystemExit("final validation changed after manifest rebuild")

print(json.dumps({
    "package_files": len([p for p in PACKAGE.rglob('*') if p.is_file()]),
    "manifest_sha256": digest(PACKAGE / "PACKAGE_MANIFEST.json"),
    "checks_executed": final["checks_executed"],
    "checks_passed": final["checks_passed"],
    "checks_failed": final["checks_failed"],
    "result": final["result"],
}, indent=2))
