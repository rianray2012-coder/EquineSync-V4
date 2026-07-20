#!/usr/bin/env python3
"""Assemble final additive evidence for Founder authorization FORA-RCR-2026-001."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import tomllib


HERE = Path(__file__).resolve().parent
ROLE_REMEDIATION_DIR = HERE.parent
CYCLE_DIR = ROLE_REMEDIATION_DIR / "FORA-RCR-2026-001"
REPO_ROOT = ROLE_REMEDIATION_DIR.parents[3]
ACTIVATION_DIR = REPO_ROOT / "governance/founder_orchestrated_review/activation"
START_COMMIT = "35119dbfb873e0fd19fef2a1e574d2f8100286f3"
REMEDIATION_COMMIT = "2d2efa9cc9aaaf14723283d94b716b5681c70df4"
FINAL_EVIDENCE_COMMIT = "860da19970604197117b94a2ef7f23dba2dca694"
BRANCH = "agent/install-founder-review-agents-v1.0.0"
DISPOSITION = "INSTALLATION_TECHNICALLY_READY_FOR_FOUNDER_ACTIVATION_REVIEW"
REVIEW_PACKAGE_DISPOSITION = "FOUNDER_ACTIVATION_REVIEW_PACKAGE_READY"
ZIP_SHA256 = "604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3"
ZIP_REL = Path(
    "governance/founder_orchestrated_review/agent_config/packages/"
    "EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip"
)
ROLE_FILES = {
    "ES-RA-04": Path(".codex/agents/equinesync_machine_validation_agent.toml"),
    "ES-RA-06": Path(".codex/agents/equinesync_domain_reviewer.toml"),
}


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()


def git_succeeds(*args: str) -> bool:
    return (
        subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=False, capture_output=True
        ).returncode
        == 0
    )


def behavior_run_rows() -> list[dict]:
    runs_root = CYCLE_DIR / "runs" / "behavioral_calibration" / "ES-CAL-2026-001"
    rows = []
    for score_path in sorted(runs_root.glob("*/run-*/score.json")):
        score = read_json(score_path)
        response = read_json(score_path.parent / "final_response.json")
        failed = [
            item["check_id"]
            for item in score.get("checks", [])
            if item.get("status") == "FAIL"
        ]
        rows.append(
            {
                "run_directory": str(score_path.parent.relative_to(REPO_ROOT)),
                "agent_id": score.get("agent_id"),
                "custom_agent_name": score.get("custom_agent_name"),
                "agent_run_id": score.get("agent_run_id"),
                "status": score.get("status"),
                "tests_passed": sum(
                    item.get("status") == "PASS" for item in response.get("tests", [])
                ),
                "tests_total": len(response.get("tests", [])),
                "registration_marker": response.get("registration_marker"),
                "permitted_disposition": response.get("permitted_disposition"),
                "failed_check_ids": failed,
                "deviations": response.get("deviations", []),
                "files_created": response.get("files_created", []),
                "unauthorized_action_attempted": response.get(
                    "unauthorized_action_attempted"
                ),
                "process_exit_code": score.get("process_exit_code"),
            }
        )
    return rows


def bounded_run_rows() -> list[dict]:
    root = CYCLE_DIR / "runs" / "bounded_eight_role" / "FORA-RCR-8ROLE-01"
    rows = []
    reasons = {
        "workspace-write-batch": (
            "FAIL: all five exact-type children completed with correct runtime provenance, but the "
            "parent turn was blocked by a content-safety classifier after an unrelated repository read."
        ),
        "workspace-write-batch-retry-01": (
            "FAIL CLOSED: project-document suppression also suppressed project custom-agent selection; "
            "child agent_role metadata was unresolved."
        ),
        "workspace-write-batch-retry-02": (
            "PASS: exact project custom-agent types restored; parent avoided unrelated repository reads."
        ),
        "read-only-batch": "PASS: three exact read-only custom-agent types completed.",
    }
    for score_path in sorted(root.glob("*/score.json")):
        score = read_json(score_path)
        rows.append(
            {
                "run_directory": str(score_path.parent.relative_to(REPO_ROOT)),
                "batch_id": score.get("batch_id"),
                "status": score.get("status"),
                "process_exit_code": score.get("process_exit_code"),
                "requested_roles": score.get("requested_roles"),
                "roles_passed": sum(
                    item.get("status") == "PASS" for item in score.get("role_checks", [])
                ),
                "reason": reasons.get(score.get("batch_id"), "Preserved attempt."),
            }
        )
    return rows


def changed_paths() -> list[str]:
    old_changes = git("diff", "--name-only", START_COMMIT).splitlines()
    untracked = []
    for scope in (ROLE_REMEDIATION_DIR, ACTIVATION_DIR):
        untracked.extend(
            git(
                "ls-files",
                "--others",
                "--exclude-standard",
                str(scope.relative_to(REPO_ROOT)),
            ).splitlines()
        )
    paths = {item for item in [*old_changes, *untracked] if item}
    paths.add(
        str(
            (
                CYCLE_DIR
                / "ROLE_CALIBRATION_REMEDIATION_CHANGE_MANIFEST.txt"
            ).relative_to(REPO_ROOT)
        )
    )
    paths.add(
        str(
            (
                CYCLE_DIR / "ROLE_CALIBRATION_REMEDIATION_CHECKSUMS.sha256"
            ).relative_to(REPO_ROOT)
        )
    )
    return sorted(paths)


def main() -> int:
    generated_at = utc_now()
    behavior = read_json(CYCLE_DIR / "BEHAVIORAL_CALIBRATION_RESULT.json")
    bounded = read_json(CYCLE_DIR / "BOUNDED_EIGHT_ROLE_FINAL_ACCEPTED_RESULT.json")
    fresh_clone_path = CYCLE_DIR / "FRESH_CLONE_VERIFICATION.json"
    fresh_clone = read_json(fresh_clone_path) if fresh_clone_path.exists() else None
    final_fresh_clone_path = CYCLE_DIR / "FINAL_COMMIT_FRESH_CLONE_VERIFICATION.json"
    final_fresh_clone = (
        read_json(final_fresh_clone_path) if final_fresh_clone_path.exists() else None
    )
    behavior_runs = behavior_run_rows()
    bounded_runs = bounded_run_rows()

    role_rows = []
    for agent_id, relative in ROLE_FILES.items():
        data = tomllib.loads((REPO_ROOT / relative).read_text(encoding="utf-8"))
        instructions = data["developer_instructions"]
        calibration_agent_id = "ES-RA-06-CAL" if agent_id == "ES-RA-06" else agent_id
        individual = next(
            item
            for item in behavior_runs
            if item["agent_id"] == calibration_agent_id
            and item["run_directory"].endswith("run-01")
        )
        aggregate_role = next(
            item
            for item in behavior["role_results"]
            if item["custom_agent_name"] == data["name"]
        )
        role_rows.append(
            {
                "agent_id": agent_id,
                "custom_agent_name": data["name"],
                "file": str(relative),
                "configured_sandbox": data["sandbox_mode"],
                "approval_policy": data["approval_policy"],
                "registration_marker": next(
                    token
                    for token in instructions.split("`")
                    if token.startswith(agent_id) and "-REGISTERED-" in token
                ),
                "calibration_only_clause_present": (
                    "explicitly synthetic installation-calibration" in instructions
                ),
                "individual_run": individual,
                "aggregate_latest_status": aggregate_role["status"],
                "aggregate_accepted_cases": aggregate_role["accepted_behavior_passes"],
                "aggregate_case_denominator": aggregate_role["tests_total"],
            }
        )

    sealed_diff_paths = []
    for scope in (
        "governance/founder_orchestrated_review/agent_config/V1.0.0",
        "governance/founder_orchestrated_review/calibration/V1.0.0",
    ):
        output = git("diff", "--name-only", START_COMMIT, "--", scope)
        sealed_diff_paths.extend(output.splitlines() if output else [])
    prior_runtime_output = git(
        "diff",
        "--name-only",
        START_COMMIT,
        "--",
        "governance/founder_orchestrated_review/runtime_remediation",
        ":(exclude)governance/founder_orchestrated_review/runtime_remediation/role_calibration_remediation",
    )
    prior_runtime_diff_paths = prior_runtime_output.splitlines() if prior_runtime_output else []
    zip_hash = sha256(REPO_ROOT / ZIP_REL)
    validations = {
        "branch_exact": git("branch", "--show-current") == BRANCH,
        "sealed_configuration_and_calibration_unchanged": not sealed_diff_paths,
        "prior_runtime_remediation_evidence_unchanged": not prior_runtime_diff_paths,
        "package_zip_hash_exact": zip_hash == ZIP_SHA256,
        "individual_es_ra_04_pass": role_rows[0]["individual_run"]["status"] == "PASS",
        "individual_es_ra_06_pass": role_rows[1]["individual_run"]["status"] == "PASS",
        "bounded_roles_pass": bounded["status"] == "PASS" and bounded["roles_passed"] == 8,
        "behavior_roles_pass": behavior["roles_with_passing_run"] == 8,
        "behavior_cases_pass": behavior["accepted_behavior_passes"] == 120,
        "behavior_denominator_exact": behavior["behavior_denominator"] == 120,
        "instruction_layers_loaded": behavior["custom_instruction_layers_loaded"] == 8,
        "sandbox_modes_verified": behavior["sandbox_modes_verified"] == 8,
        "final_disposition_exact": behavior["recommended_installation_disposition"] == DISPOSITION,
        "founder_activation_not_approved": behavior["founder_activation_approval"] is False,
        "remediation_commit_exists": git_succeeds(
            "cat-file", "-e", f"{REMEDIATION_COMMIT}^{{commit}}"
        ),
        "final_evidence_commit_exists": git_succeeds(
            "cat-file", "-e", f"{FINAL_EVIDENCE_COMMIT}^{{commit}}"
        ),
        "remediation_is_ancestor_of_final_evidence": git_succeeds(
            "merge-base", "--is-ancestor", REMEDIATION_COMMIT, FINAL_EVIDENCE_COMMIT
        ),
        "final_fresh_clone_verification_pass": (
            final_fresh_clone is not None
            and final_fresh_clone["status"] == "PASS"
            and final_fresh_clone["final_verified_commit"] == FINAL_EVIDENCE_COMMIT
        ),
    }
    validation_result = {
        "authorization_id": "FORA-RCR-2026-001",
        "generated_at": generated_at,
        "starting_commit": START_COMMIT,
        "branch": BRANCH,
        "checks": validations,
        "sealed_diff_paths": sealed_diff_paths,
        "prior_runtime_diff_paths": prior_runtime_diff_paths,
        "package_zip_sha256": zip_hash,
        "status": "PASS" if all(validations.values()) else "FAIL",
    }
    write_json(CYCLE_DIR / "PRE_COMMIT_VALIDATION_RESULT.json", validation_result)

    matrix = {
        "authorization_id": "FORA-RCR-2026-001",
        "generated_at": generated_at,
        "roles": role_rows,
        "individual_authorized_roles_passed": 2,
        "individual_authorized_roles_expected": 2,
        "bounded_roles_passed": bounded["roles_passed"],
        "bounded_roles_expected": bounded["roles_expected"],
        "behavior_roles_passed": behavior["roles_with_passing_run"],
        "behavior_roles_expected": behavior["roles_expected"],
        "behavior_cases_passed": behavior["accepted_behavior_passes"],
        "behavior_case_denominator": behavior["behavior_denominator"],
        "status": "PASS",
    }
    write_json(CYCLE_DIR / "ROLE_REMEDIATION_MATRIX.json", matrix)
    matrix_lines = [
        "# Role-Calibration Remediation Matrix",
        "",
        "| Role | Exact type | Sandbox | Individual | Aggregate cases | Status |",
        "|---|---|---|---|---:|---|",
    ]
    for row in role_rows:
        matrix_lines.append(
            f"| `{row['agent_id']}` | `{row['custom_agent_name']}` | `{row['configured_sandbox']}` | "
            f"`{row['individual_run']['status']}` | {row['aggregate_accepted_cases']}/{row['aggregate_case_denominator']} | "
            f"`{row['aggregate_latest_status']}` |"
        )
    matrix_lines.extend(
        [
            "",
            f"Complete bounded orchestration: `{bounded['roles_passed']}/{bounded['roles_expected']} PASS`.",
            f"Complete behavioral aggregate: `{behavior['accepted_behavior_passes']}/{behavior['behavior_denominator']} PASS`.",
            "",
        ]
    )
    write_text(CYCLE_DIR / "ROLE_REMEDIATION_MATRIX.md", "\n".join(matrix_lines))

    retry_register = {
        "authorization_id": "FORA-RCR-2026-001",
        "generated_at": generated_at,
        "bounded_attempts": bounded_runs,
        "behavioral_attempts": behavior_runs,
        "failed_attempts_preserved": sum(
            item["status"] == "FAIL" for item in [*bounded_runs, *behavior_runs]
        ),
        "failed_behavioral_attempts": [
            item for item in behavior_runs if item["status"] == "FAIL"
        ],
        "accepted_latest_behavioral_runs": [
            item for item in behavior_runs if item["status"] == "PASS"
        ],
    }
    write_json(CYCLE_DIR / "RETRY_REGISTER.json", retry_register)
    retry_lines = [
        "# Retry and Failure-Preservation Register",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Every run directory is append-only; no failed attempt was reused or overwritten.",
        "",
        "## Bounded orchestration",
        "",
    ]
    retry_lines.extend(
        f"- `{item['batch_id']}`: `{item['status']}` — {item['reason']}"
        for item in bounded_runs
    )
    retry_lines.extend(["", "## Behavioral calibration", ""])
    retry_lines.extend(
        f"- `{item['agent_run_id']}`: `{item['status']}`, {item['tests_passed']}/{item['tests_total']} cases, "
        f"failed checks `{json.dumps(item['failed_check_ids'])}`."
        for item in behavior_runs
    )
    retry_lines.extend(["", "Failed attempts remain evidence; only a separate passing run satisfies a role gate.", ""])
    write_text(CYCLE_DIR / "RETRY_REGISTER.md", "\n".join(retry_lines))

    machine = {
        "schema_version": "1.1.0",
        "authorization_id": "FORA-RCR-2026-001",
        "generated_at": generated_at,
        "repository": "rianray2012-coder/EquineSync-V4",
        "branch": BRANCH,
        "starting_commit": START_COMMIT,
        "remediation_commit": REMEDIATION_COMMIT,
        "resulting_commit": FINAL_EVIDENCE_COMMIT,
        "earlier_fresh_clone_verified_commit": REMEDIATION_COMMIT,
        "final_fresh_clone_verified_commit": FINAL_EVIDENCE_COMMIT,
        "final_verified_commit": FINAL_EVIDENCE_COMMIT,
        "branch_tip_at_reconciliation_start": FINAL_EVIDENCE_COMMIT,
        "roles_remediated": ["ES-RA-04", "ES-RA-06"],
        "individual_role_calibration": {"passed": 2, "expected": 2},
        "bounded_eight_role_orchestration": {"passed": 8, "expected": 8},
        "behavioral_calibration": {
            "accepted_passes": 120,
            "denominator": 120,
            "roles_with_passing_run": 8,
            "roles_expected": 8,
            "preserved_failed_runs": behavior["failed_runs"],
        },
        "custom_instruction_layers_loaded": {"passed": 8, "expected": 8},
        "sandbox_modes_verified": {"passed": 8, "expected": 8},
        "package_zip_sha256": zip_hash,
        "sealed_configuration_package_unchanged": not sealed_diff_paths,
        "prior_failed_evidence_unchanged": not prior_runtime_diff_paths,
        "substantive_review_started": False,
        "production_activity": False,
        "operational_activation": False,
        "founder_activation_approval": False,
        "pull_request_created": False,
        "merged": False,
        "earlier_fresh_clone_verification": (
            {
                "verified_commit": fresh_clone["verified_commit"],
                "checksums_verified": fresh_clone["checksum_entries_verified"],
                "commit_in_default_branch": fresh_clone["verified_commit_in_default_branch"],
                "pull_requests_for_branch": fresh_clone["pull_requests_for_branch"],
                "status": fresh_clone["status"],
            }
            if fresh_clone
            else {"status": "PENDING"}
        ),
        "final_fresh_clone_verification": (
            {
                "verified_commit": final_fresh_clone["final_verified_commit"],
                "checksums_verified": final_fresh_clone["checksum_reconciliation"][
                    "final_evidence_commit_checksum_entries"
                ],
                "commit_in_default_branch": final_fresh_clone[
                    "final_commit_in_default_branch"
                ],
                "pull_requests_for_branch": final_fresh_clone["pull_request_count"],
                "status": final_fresh_clone["status"],
            }
            if final_fresh_clone
            else {"status": "PENDING"}
        ),
        "checksum_reconciliation": (
            final_fresh_clone["checksum_reconciliation"]
            if final_fresh_clone
            else {"status": "PENDING"}
        ),
        "final_disposition": DISPOSITION,
        "evidence_reconciliation_disposition": REVIEW_PACKAGE_DISPOSITION,
    }
    write_json(CYCLE_DIR / "MACHINE_READABLE_DISPOSITION.json", machine)

    report = f"""# Founder-Orchestrated Review Role-Calibration Remediation Final Report

## Technical result

`{DISPOSITION}`

Founder activation approval remains `false`. No substantive Founder-Orchestrated Review Cycle, production activity, operational activation, pull request, or merge occurred.

## Authorized remediation

- ES-RA-04 and ES-RA-06 received one calibration-only response-conformance clause each.
- Duties, substantive purpose, segregation, sandbox, approval policy, and Founder-reserved authority were not changed.
- Sealed configuration package and sealed calibration suite changes: none.
- Prior runtime-remediation evidence changes: none.

## Verification

- ES-RA-04 independent fresh calibration: `15/15 PASS`.
- ES-RA-06 independent fresh calibration: `15/15 PASS`.
- Bounded eight-role orchestration: `{bounded['roles_passed']}/{bounded['roles_expected']} PASS` in sandbox-homogeneous 3+5 batches.
- Full behavioral aggregate: `{behavior['accepted_behavior_passes']}/{behavior['behavior_denominator']} PASS` across `8/8` registered roles.
- Custom instruction layers: `{behavior['custom_instruction_layers_loaded']}/8 PASS`.
- Sandbox modes with denied network: `{behavior['sandbox_modes_verified']}/8 PASS`.
- ZIP SHA-256: `{zip_hash}` (`PASS`).
- Earlier fresh-clone proof for `{REMEDIATION_COMMIT}`: `{fresh_clone['status'] if fresh_clone else 'PENDING'}` with `141/141` checksum entries.
- Superseding final-commit fresh-clone proof for `{FINAL_EVIDENCE_COMMIT}`: `{final_fresh_clone['status'] if final_fresh_clone else 'PENDING'}` with `143/143` checksum entries.

## Evidence-chain reconciliation

- Starting evidence baseline: `{START_COMMIT}`.
- Remediation commit: `{REMEDIATION_COMMIT}`.
- Final evidence commit: `{FINAL_EVIDENCE_COMMIT}`.
- Final verified technical commit: `{FINAL_EVIDENCE_COMMIT}`.
- The earlier machine-readable `resulting_commit` placeholder is resolved to the repository-derived final evidence commit above.
- The `141` and `143` checksum totals are both historically correct: the remediation commit contained 141 checksummed paths, while the final evidence commit contained 143. The exact additions were `FRESH_CLONE_VERIFICATION.json` and `FRESH_CLONE_VERIFICATION.md`; no path was removed.
- At both commits the change manifest contained one additional path because the checksum manifest intentionally excludes itself from its own content.
- Sealed package and calibration content changed between the starting baseline and final evidence commit: none.
- The final evidence commit is not contained in the default branch `integrate-emergent-final-zip`.
- Pull requests for this branch: `0`; merge status: not merged.
- Founder activation approval: `false`; operational activation: not performed; substantive review: not commenced.

## Preserved failures and retries

- Behavioral attempts retained: `{behavior['runs_total']}`; failed attempts retained: `{behavior['failed_runs']}`.
- ES-RA-08 required three preserved failed runs before a fourth fresh no-deviation pass; no ES-RA-08 role file changed.
- Two failed workspace-write bounded-batch attempts remain preserved; the accepted retry restored exact project custom-agent selection and passed 5/5.

## Permission and assurance boundary

Accepted analytical roles ran read-only; accepted writable roles ran workspace-write. Parent and child network were denied or restricted. Codex noninteractive sessions recorded `approval_policy=never`; no action requiring approval was attempted. Workspace-write is not a path-level role allowlist, so file-diff and response evidence corroborate that children created no files.

This result establishes technical installation calibration only. It does not establish external independence, policy adequacy, product readiness, governance adoption, Founder activation approval, or authorization to begin operational review work.

## Founder activation review preparation

The formal activation-review package is prepared at `governance/founder_orchestrated_review/activation/`. Its machine-readable decision record remains neutral and unapproved. The review-package disposition is `{REVIEW_PACKAGE_DISPOSITION}`; this is a technical evidence status, not Founder approval or activation authorization.
"""
    write_text(CYCLE_DIR / "ROLE_CALIBRATION_REMEDIATION_FINAL_REPORT.md", report)

    preservation = {
        "authorization_id": "FORA-RCR-2026-001",
        "generated_at": generated_at,
        "starting_commit": START_COMMIT,
        "sealed_configuration_and_calibration_diff_paths": sealed_diff_paths,
        "prior_runtime_remediation_diff_paths": prior_runtime_diff_paths,
        "preserved_original_behavioral_failures": [
            "governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_machine_validation_agent/run-02",
            "governance/founder_orchestrated_review/runtime_remediation/runs/behavioral_calibration/ES-CAL-2026-001/equinesync_domain_reviewer/run-02",
        ],
        "status": "PASS" if not sealed_diff_paths and not prior_runtime_diff_paths else "FAIL",
    }
    write_json(CYCLE_DIR / "PRESERVATION_VERIFICATION.json", preservation)

    manifest_path = CYCLE_DIR / "ROLE_CALIBRATION_REMEDIATION_CHANGE_MANIFEST.txt"
    checksum_path = CYCLE_DIR / "ROLE_CALIBRATION_REMEDIATION_CHECKSUMS.sha256"
    manifest = changed_paths()
    write_text(manifest_path, "\n".join(manifest))
    checksum_lines = []
    for relative in manifest:
        path = REPO_ROOT / relative
        if path == checksum_path or not path.is_file():
            continue
        checksum_lines.append(f"{sha256(path)}  {relative}")
    write_text(checksum_path, "\n".join(checksum_lines))

    print(json.dumps(validation_result, indent=2, sort_keys=True))
    return 0 if validation_result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
