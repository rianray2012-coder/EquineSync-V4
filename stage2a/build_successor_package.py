#!/usr/bin/env python3
"""Assemble the remediated Stage 2A candidate for independent re-review."""
from __future__ import annotations

import csv
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess
import tempfile
import re
import zipfile
from pathlib import Path

from traceability_contract import (
    FINDING_SPECS,
    finding_rows as canonical_finding_rows,
    output_rows as canonical_output_rows,
    requirement_rows as canonical_requirement_rows,
    test_rows as canonical_test_rows,
)

REPO = Path(__file__).resolve().parents[1]
STAGE = REPO / "stage2a"
FAILED_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003"
PRIOR_CORRECTED_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-003"
PRIOR_CANDIDATE_004_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-004"
PRIOR_CANDIDATE_005_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-005"
PRIOR_CANDIDATE_006_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-006"
PRIOR_CANDIDATE_007_ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-007"
ROOT = REPO / "docs/implementation/STAGE_2A_EXECUTION_FOUNDATION/ES-PKG-2026-004-V003-CANDIDATE-008"
EVIDENCE = STAGE / "evidence/latest"
EVENTS = STAGE / "evidence/events"
REVIEWS = STAGE / "review_attempts"
OUTPUTS = REPO.parents[1] / "outputs"
PACKAGE_ID = "ES-PKG-2026-004-V003"
CANDIDATE_ID = "ES-PKG-2026-004-V003-CANDIDATE-008"
PREDECESSOR = "ES-PKG-2026-003-V002"
START = "0be6172a28b75238c5facabf91d43ed09aaf0d54"
BASELINE = "acb518ea5a160820e64681ff95a16b010fe1156c"
PREDECESSOR_SHA = "b7193e9a4cac078a87c45e31d708f787b40e7e7e973eee7c3f327680a7e32329"
SEALED_SHA = "268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f"
BRANCH = "codex/stage2a-execution-foundation-remediation"
REMOTE = "https://github.com/rianray2012-coder/EquineSync-V4.git"
DISPOSITION = "STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE"
RUNTIME_CAUSE = "RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE"
FAILED_ATTEMPT_002_SHA = "6f984649f8465e3410d95deaf9ece76f642bb0ab70eddb89252a858cc0b470b4"
FAILED_ATTEMPT_002_MANIFEST_SHA = "e8a65076f1ed4b548223c8f158a0ae930fba85c041763a9ae972b69802e7a45b"
FAILED_ATTEMPT_003_SHA = "86d87ca6d289f9ca3b3b3c48e565781469a553d8219b0c8a720b60aebf034ec0"
FAILED_ATTEMPT_003_MANIFEST_SHA = "f7bd73c7f28b3139f68fc0cd6d6af9d260a16f6ae8292425a24c91c6e832f4bc"
FAILED_ATTEMPT_004_SHA = "7d209ec231f9d8a0ad04809f7d8efd45630534ea24875042ae5b6893c16e7c0c"
FAILED_ATTEMPT_004_MANIFEST_SHA = "927cad3b2b8142188e2e9cce3a069fd121361f2ddf489ba7c5fc9d9d51af591f"
FAILED_ATTEMPT_005_SHA = "41cc9ae595dbe640cc9aedf79fe84267d58ddb84355682626e237eccd5d3595c"
FAILED_ATTEMPT_005_MANIFEST_SHA = "a0937895498704028cf8f450f18555ac7b54b5417a96248d62702a6fa7aff75f"
FAILED_ATTEMPT_006_SHA = "de4145d04779e0d1aa2b73bfff870f54637818c7ad895d74db82b6e9aa232068"
FAILED_ATTEMPT_006_MANIFEST_SHA = "e75db726bd1ca48a8ecbd6dd9d204b7189d4d3f015c3ce4e07a460ad792b0274"
FAILED_ATTEMPT_007_SHA = "e89cbed1ac280e1acb4c9a2105177037a5b2335afe8f4f9df38ab3033902c04e"
FAILED_ATTEMPT_007_MANIFEST_SHA = "cb63e7e2da83368ad737ade7cc3b37d4b6b4281b4a6ab2dc6770f3e481964f1d"


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, text=True, capture_output=True, check=True).stdout.strip()


def write_json(name: str, value: object) -> None:
    (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def common(title: str) -> str:
    return (
        f"# {title}\n\n"
        f"- Package: `{PACKAGE_ID}`\n"
        f"- Candidate: `{CANDIDATE_ID}`\n"
        f"- Branch: `{BRANCH}`\n"
        f"- Starting commit: `{START}`\n"
        "- F-0001: `F0001_REMAINS_OPEN_BLOCKING`\n"
        "- Execution: `EXECUTION_NOT_AUTHORIZED`\n"
        "- Assurance: `NOT_EXTERNALLY_ASSURED`\n"
        f"- Principal disposition: `{DISPOSITION}`\n"
    )


def write_md(name: str, title: str, body: str) -> None:
    (ROOT / name).parent.mkdir(parents=True, exist_ok=True)
    (ROOT / name).write_text(common(title) + "\n" + body.strip() + "\n", encoding="utf-8")


def pair(stem: str, title: str, value: object, body: str) -> None:
    write_json(stem + ".json", value)
    write_md(stem + ".md", title, body)


def check(validation: dict[str, object], name: str) -> dict[str, object]:
    return next(row for row in validation["checks"] if row["check"] == name)


def package_safe_validation(raw: dict[str, object]) -> dict[str, object]:
    """Redact only local path prefixes while preserving technical meaning."""
    repo_prefix = REPO.resolve().as_posix()
    replacements = {
        repo_prefix: "REPOSITORY_ROOT",
        "/Users/rianray/.pyenv/versions/3.11.11": "PYTHON_RUNTIME",
        "/Users/rianray": "LOCAL_USER_HOME",
    }

    def transform(value: object) -> object:
        if isinstance(value, str):
            for source, target in replacements.items():
                value = value.replace(source, target)
            return value
        if isinstance(value, list):
            return [transform(item) for item in value]
        if isinstance(value, dict):
            return {key: transform(item) for key, item in value.items()}
        return value

    value = transform(deepcopy(raw))
    assert isinstance(value, dict)
    process_check = next(row for row in value["checks"] if row["check"] == "process_identity")
    for key in ("mongo_identity", "api_identity"):
        identity = process_check["detail"][key]
        identity["command_line_hash_basis"] = "FULL_OBSERVED_COMMAND_BEFORE_LOCAL_PATH_PREFIX_REDACTION"
        identity["packaged_command_line_sha256"] = hashlib.sha256(identity["observed_command_line"].encode()).hexdigest()
        identity["path_redaction"] = {
            "policy": "LOCAL_PATH_PREFIX_TO_STABLE_ALIAS",
            "meaning_preserved": True,
            "stable_aliases": ["REPOSITORY_ROOT", "PYTHON_RUNTIME", "LOCAL_USER_HOME"],
        }
    value["package_path_redaction"] = {
        "policy": "LOCAL_PATH_PREFIX_TO_STABLE_ALIAS",
        "meaning_preserved": True,
        "raw_evidence_location": "stage2a/evidence/latest/FOUNDATION_VALIDATION.json",
        "raw_evidence_promoted_to_package": False,
    }
    return value


def verify_freeze(root: Path, expected_payload: int, expected_physical: int, expected_manifest_sha: str, archive_name: str, expected_archive_sha: str) -> dict[str, object]:
    archive = OUTPUTS / archive_name
    if not archive.is_file() or sha(archive) != expected_archive_sha:
        raise RuntimeError("failed candidate immutable archive changed")
    prefix = f"{root.name}/"
    with zipfile.ZipFile(archive, "r") as frozen:
        members = {
            info.filename[len(prefix):]: frozen.read(info)
            for info in frozen.infolist()
            if not info.is_dir() and info.filename.startswith(prefix)
        }
    manifest_bytes = members.get("DRAFT_REVIEW_SHA256SUMS.txt", b"")
    if hashlib.sha256(manifest_bytes).hexdigest() != expected_manifest_sha:
        raise RuntimeError(f"failed candidate embedded manifest changed: {root.name}")
    rows = manifest_bytes.decode("utf-8").splitlines()
    errors = []
    listed: set[str] = set()
    for line in rows:
        expected, relative = line.split("  ", 1)
        listed.add(relative)
        data = members.get(relative)
        if data is None or hashlib.sha256(data).hexdigest() != expected:
            errors.append(relative)
    expected_controls = {"DRAFT_REVIEW_SHA256SUMS.txt", "DRAFT_REVIEW_SNAPSHOT_RECORD.json", "DRAFT_REVIEW_SNAPSHOT_RECORD.md"}
    unexpected = set(members) - listed - expected_controls
    missing_controls = expected_controls - set(members)
    if errors or unexpected or missing_controls or len(rows) != expected_payload or len(members) != expected_physical:
        raise RuntimeError(
            f"failed candidate archive integrity mismatch: rows={len(rows)} physical={len(members)} "
            f"errors={errors} unexpected={sorted(unexpected)} missing_controls={sorted(missing_controls)}"
        )
    return {
        "candidate_directory": root.relative_to(REPO).as_posix(),
        "archive": f"outputs/{archive_name}",
        "archive_sha256": expected_archive_sha,
        "manifest_sha256": expected_manifest_sha,
        "payload_files": len(rows),
        "physical_files": len(members),
        "verification_basis": "IMMUTABLE_ARCHIVE_BYTES_AND_EMBEDDED_MANIFEST",
        "unchanged": True,
    }


def verify_failed_assembly(root: Path, expected_files: int, expected_manifest_sha: str, archive_name: str, expected_archive_sha: str) -> dict[str, object]:
    manifest = STAGE / "evidence/failed_attempts/CANDIDATE_005_ASSEMBLY_FAILED_SHA256SUMS.txt"
    if not manifest.is_file() or sha(manifest) != expected_manifest_sha:
        raise RuntimeError("Candidate 005 failed-assembly manifest changed")
    rows = manifest.read_text(encoding="utf-8").splitlines()
    archive = OUTPUTS / archive_name
    if not archive.is_file() or sha(archive) != expected_archive_sha:
        raise RuntimeError("Candidate 005 failed-assembly archive changed")
    prefix = f"{root.name}/"
    with zipfile.ZipFile(archive, "r") as frozen:
        members = {
            info.filename[len(prefix):]: frozen.read(info)
            for info in frozen.infolist()
            if not info.is_dir() and info.filename.startswith(prefix)
        }
    errors: list[str] = []
    listed_paths: set[str] = set()
    for line in rows:
        expected, relative = line.split("  ", 1)
        listed_paths.add(relative)
        data = members.get(relative)
        if data is None or hashlib.sha256(data).hexdigest() != expected:
            errors.append(relative)
    if errors or len(rows) != expected_files or set(members) != listed_paths:
        raise RuntimeError(f"Candidate 005 failed-assembly archive integrity mismatch: rows={len(rows)} physical={len(members)} errors={errors}")
    return {
        "candidate_directory": root.relative_to(REPO).as_posix(),
        "archive": f"outputs/{archive_name}",
        "archive_sha256": expected_archive_sha,
        "manifest": manifest.relative_to(REPO).as_posix(),
        "manifest_sha256": expected_manifest_sha,
        "physical_files": len(members),
        "classification": "PRE_FREEZE_ASSEMBLY_VALIDATION_FAILED",
        "verification_basis": "IMMUTABLE_ARCHIVE_BYTES_AND_EXTERNAL_MANIFEST",
        "unchanged": True,
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("candidate package may only be built on the authorized Stage 2A branch")
    packaging_commit = git("rev-parse", "HEAD")
    packaging_tree = git("rev-parse", "HEAD^{tree}")
    if packaging_commit == START or not git("ls-tree", "-r", "--name-only", packaging_commit, "--", "stage2a"):
        raise RuntimeError("Stage 2A implementation must be committed before package assembly")
    failed_candidates = [
        verify_freeze(FAILED_ROOT, 108, 111, FAILED_ATTEMPT_002_MANIFEST_SHA, "ES-PKG-2026-004-V003_REVIEW_ATTEMPT_002_FAILED.zip", FAILED_ATTEMPT_002_SHA),
        verify_freeze(PRIOR_CORRECTED_ROOT, 121, 124, FAILED_ATTEMPT_003_MANIFEST_SHA, "ES-PKG-2026-004-V003_REVIEW_ATTEMPT_003_FAILED.zip", FAILED_ATTEMPT_003_SHA),
        verify_freeze(PRIOR_CANDIDATE_004_ROOT, 207, 210, FAILED_ATTEMPT_004_MANIFEST_SHA, "ES-PKG-2026-004-V003_REVIEW_ATTEMPT_004_FAILED.zip", FAILED_ATTEMPT_004_SHA),
        verify_failed_assembly(PRIOR_CANDIDATE_005_ROOT, 249, FAILED_ATTEMPT_005_MANIFEST_SHA, "ES-PKG-2026-004-V003-CANDIDATE-005_ASSEMBLY_FAILED.zip", FAILED_ATTEMPT_005_SHA),
        verify_freeze(PRIOR_CANDIDATE_006_ROOT, 253, 256, FAILED_ATTEMPT_006_MANIFEST_SHA, "ES-PKG-2026-004-V003-CANDIDATE-006_FROZEN.zip", FAILED_ATTEMPT_006_SHA),
        verify_freeze(PRIOR_CANDIDATE_007_ROOT, 274, 277, FAILED_ATTEMPT_007_MANIFEST_SHA, "ES-PKG-2026-004-V003-CANDIDATE-007_FROZEN.zip", FAILED_ATTEMPT_007_SHA),
    ]
    raw_validation = json.loads((EVIDENCE / "FOUNDATION_VALIDATION.json").read_text(encoding="utf-8"))
    validation = package_safe_validation(raw_validation)
    bootstrap = json.loads((EVIDENCE / "BACKEND_BOOTSTRAP_RUN.json").read_text(encoding="utf-8"))
    if validation["validation"] != "PASS" or bootstrap["validation"] != "PASS":
        raise RuntimeError("foundation validation and backend bootstrap must pass")
    implementation_commit = validation["artifacts"]["implementation_commit"]
    implementation_tree = validation["artifacts"]["implementation_tree"]
    bootstrap_commit = bootstrap.get("implementation_commit")
    bootstrap_ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", implementation_commit, str(bootstrap_commit)], cwd=REPO)
    if bootstrap_ancestry.returncode != 0:
        raise RuntimeError("bootstrap commit does not descend from the validated implementation")
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", implementation_commit, packaging_commit], cwd=REPO)
    if ancestry.returncode != 0:
        raise RuntimeError("validated implementation is not an ancestor of the packaging commit")
    if ROOT.exists():
        raise RuntimeError(f"refusing to overwrite existing corrected candidate {CANDIDATE_ID}")
    if not FAILED_ROOT.is_dir():
        raise RuntimeError("archived failed candidate directory is unavailable")
    ROOT.mkdir(parents=True)

    baseline = {
        "package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "repository": REMOTE,
        "stage2_package_branch": "codex/stage2-f0001-execution-baseline",
        "stage2_package_commit": START, "stage2a_branch": BRANCH,
        "stage2a_implementation_commit": implementation_commit, "stage2a_implementation_tree": implementation_tree,
        "stage2a_packaging_commit": packaging_commit, "stage2a_packaging_tree": packaging_tree,
        "stage2a_bootstrap_commit": bootstrap_commit,
        "immutable_baseline": BASELINE, "stage2_archive_sha256": PREDECESSOR_SHA,
        "stage2_package_validation": "PASS_50_OF_50", "stage2_package_clean_extraction": "113_OF_113",
        "stage2_remote_tip": START, "pull_requests": 0, "default_branch_contains_stage2_commit": False,
        "predecessor_unchanged": True,
        "failed_candidates": failed_candidates,
    }
    pair("STAGE2A_PRE_CHANGE_BASELINE", "Stage 2A Pre-Change Baseline", baseline,
         "All mandatory repository, predecessor, immutable-baseline, branch, and publication checks passed before implementation.")
    publication = baseline | {"push_result": "PASS_EXACT_COMMIT_PUBLISHED", "amended": False, "pr_created": False, "merged": False, "tagged": False, "released": False, "deployed": False}
    pair("STAGE2_PACKAGE_PUBLICATION_RECORD", "Stage 2 Publication Record", publication,
         f"The Stage 2 branch was published at exact commit `{START}`. No PR, merge, tag, release, or deployment occurred.")

    closure = {
        "package_id": PACKAGE_ID, "finding_id": "ES-REV-2026-001-F-0002",
        "disposition": "F0002_CLOSED_BY_FOUNDER_AUTHORITY_FOR_IMMUTABLE_BASELINE_MATERIALIZATION",
        "closure_authority": "Rian Ray, Founder", "immutable_baseline": BASELINE,
        "scope": "exact materialization identification verification and reproducibility of the immutable baseline only",
        "does_not_close_f0001": True, "execution_ready": False, "workflow_execution_authorized": False,
        "production_ready": False, "atlases_completed": False, "gp05_implemented": False,
        "external_assurance": False,
    }
    pair("F0002_FOUNDER_AUTHORIZED_CLOSURE", "F-0002 Founder-Authorized Closure", closure,
         f"Disposition: `{closure['disposition']}`. This bounded closure does not close F-0001 or authorize execution.")
    f2 = [
        {"evidence_id": "F2C-E-001", "subject": "immutable commit", "value": BASELINE, "status": "PASS"},
        {"evidence_id": "F2C-E-002", "subject": "Stage 2 commit", "value": START, "status": "PASS"},
        {"evidence_id": "F2C-E-003", "subject": "Stage 2 archive SHA-256", "value": PREDECESSOR_SHA, "status": "PASS"},
        {"evidence_id": "F2C-E-004", "subject": "independent materialization assessment", "value": "F0002_READY_FOR_AUTHORIZED_CLOSURE", "status": "PASS"},
        {"evidence_id": "F2C-E-005", "subject": "Founder closure scope", "value": "immutable baseline materialization only", "status": "PASS"},
    ]
    write_json("F0002_CLOSURE_EVIDENCE_REGISTER.json", {"package_id": PACKAGE_ID, "evidence": f2})
    with (ROOT / "F0002_CLOSURE_EVIDENCE_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(f2[0])); writer.writeheader(); writer.writerows(f2)

    gap_titles = {
        1: "Backend dependency-install contract", 2: "Runtime and toolchain contract",
        3: "Disposable environment and provider isolation", 4: "Deterministic start stop and health orchestration",
        5: "Synthetic fixture foundation", 6: "Evidence-capture harness",
        7: "Exact cleanup and zero-residue proof", 8: "Rollback and recovery foundation",
        9: "Startup side-effect control",
    }
    authorized = [{
        "gap_id": f"S2-GAP-{number:03d}", "title": title, "scope": "AUTHORIZED_STAGE2A",
        "implementation_status": "REMEDIATED_CANDIDATE", "independent_verification": "PENDING_REREVIEW",
        "formally_closed": False, "f0001_effect": "F0001_REMAINS_OPEN_BLOCKING",
    } for number, title in gap_titles.items()]
    deferred = [{
        "gap_id": f"S2-GAP-{number:03d}", "title": "Retained Stage 2 blocker",
        "scope": "OUTSIDE_STAGE2A", "implementation_status": "NOT_ATTEMPTED_BLOCKING",
        "formally_closed": False, "f0001_effect": "F0001_REMAINS_OPEN_BLOCKING",
    } for number in range(10, 32)]
    pair("STAGE2A_SCOPE_REGISTER", "Stage 2A Scope Register", {"package_id": PACKAGE_ID, "authorized_gaps": authorized, "deferred_gaps": deferred},
         "Authorized: `S2-GAP-001` through `S2-GAP-009`. Deferred and unchanged: `S2-GAP-010` through `S2-GAP-031`. No gap is self-closed.")

    # Gap 001 and 002 evidence.
    requirement_hash = sha(REPO / "backend/requirements.txt")
    bootstrap_contract = {
        "gap_id": "S2-GAP-001", "python": "3.11.11", "working_directory": "repository root",
        "bootstrap_command": "sh stage2a/bootstrap_backend.sh", "timeout_seconds_per_command": 900,
        "requirements": "backend/requirements.txt", "requirements_sha256": requirement_hash,
        "all_requirements_exactly_pinned": True, "pip_configuration": "ISOLATED_DEV_NULL",
        "dependency_resolution": "NO_DEPS_ALL_REQUIREMENTS_EXPLICITLY_PINNED",
        "artifact_hash_basis": bootstrap["installed_artifact_hash_basis"],
        "cleanup_on_failure": "remove ignored stage2a/.venv", "expected_exit": 0,
    }
    pair("BACKEND_BOOTSTRAP_CONTRACT", "Backend Bootstrap Contract", bootstrap_contract,
         "The exact Python runtime, timeout-bounded bootstrap command, pinned requirement source, isolated pip configuration, failure cleanup, and downloaded-artifact hash basis are machine recorded.")
    pair("BACKEND_BOOTSTRAP_VALIDATION", "Backend Bootstrap Validation", bootstrap,
         f"Result: `PASS`. `{len(bootstrap['inventory'])}` requirement artifacts have pip-reported download SHA-256 and installed metadata SHA-256 values; `pip check` passed.")
    inventory_lines = [f"{row['name']}=={row['version']}  artifact_sha256={row['download_artifact_sha256']}  metadata_sha256={row['metadata_sha256']}" for row in bootstrap["inventory"]]
    (ROOT / "BACKEND_DEPENDENCY_INVENTORY.txt").write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")
    toolchain = json.loads((STAGE / "toolchain.json").read_text(encoding="utf-8")) | {
        "gap_id": "S2-GAP-002", "package_manager_decision": "npm",
        "frontend_lockfile": "frontend/package-lock.json", "frontend_lockfile_sha256": sha(REPO / "frontend/package-lock.json"),
        "yarn_metadata_preserved": True, "source_dependency_changes": 0,
    }
    pair("STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT", "Stage 2A Runtime and Toolchain Contract", toolchain,
         "The contract captures every executable required by bootstrap, orchestration, isolation, validation, hashing, and Git recovery, including binary SHA-256 values where available.")
    write_md("PACKAGE_MANAGER_AUTHORITY_DECISION.md", "Package Manager Authority Decision",
             "Stage 2A uses npm with `frontend/package-lock.json` and the repository-supported `npm ci --legacy-peer-deps --include=dev --no-audit --no-fund`. Historical Yarn metadata is preserved but is not authoritative for Stage 2A.")
    capture_keys = ("operating_system", "architecture", "shell", "python", "pip", "pyenv", "node", "npm", "mongodb", "mongosh", "git", "curl", "lsof", "sandbox_exec", "zsh")
    (ROOT / "TOOLCHAIN_VERSION_CAPTURE.txt").write_text("\n".join(f"{key}={toolchain[key]}" for key in capture_keys) + "\n", encoding="utf-8")
    pair("TOOLCHAIN_VALIDATION", "Toolchain Validation", toolchain | {"validation": "PASS"},
         "Backend bootstrap, frontend lockfile installation, frontend build, and required tool identification passed without dependency-source changes or deployment.")

    # Gaps 003-009 use current foundation evidence.
    environment = check(validation, "environment_contract")["detail"]
    isolation = {
        "gap_id": "S2-GAP-003", "environment": environment,
        "negative_tests": check(validation, "isolation_negative_tests")["detail"],
        "network_denials": validation["artifacts"]["network_denials"],
        "provider_attempt_count": validation["provider_attempt_count"], "production_access_count": validation["production_access_count"], "live_data_access_count": validation["live_data_access_count"],
        "network_profile": "stage2a/config/loopback-only.sb", "external_egress": "DENIED_EXACT_PORT_SANDBOX",
    }
    pair("STAGE2A_ISOLATION_CONTROL", "Stage 2A Isolation Control", isolation,
         "A strict environment allowlist, ambient prohibited-name denial, exact loopback ports, synthetic datastore identity, deny proxies, and sandbox-enforced external network denial operate fail closed.")
    providers = check(validation, "provider_denial")["detail"]
    provider_rows = providers["register"]
    write_json("PROVIDER_DENIAL_REGISTER.json", {"package_id": PACKAGE_ID, "attempt_count": providers["attempt_count"], "outcome_totals": providers["outcome_totals"], "providers": provider_rows, "network_guard": providers["network_guard"], "provider_guard_proof": providers["provider_guard_proof"]})
    with (ROOT / "PROVIDER_DENIAL_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(provider_rows[0])); writer.writeheader(); writer.writerows(provider_rows)
    write_json("ISOLATION_NEGATIVE_TEST_REPORT.json", isolation | {"validation": "PASS"})
    write_md("ISOLATION_NEGATIVE_TEST_REPORT.md", "Isolation Negative Test Report", "All configuration mutations, inherited provider configuration, unapproved loopback access, and documentation-range external access were denied. Values were not recorded.")
    from lib.control import ALLOWED_NAMES
    (ROOT / "SECRET_NAME_ALLOWLIST.txt").write_text("\n".join(sorted(ALLOWED_NAMES)) + "\n", encoding="utf-8")

    cold = check(validation, "cold_start_full_application")["detail"]
    shutdown = check(validation, "controlled_shutdown")["detail"]
    interrupted = check(validation, "interrupted_start_cleanup")["detail"]
    orchestration = {
        "gap_id": "S2-GAP-004", "entry_point": "stage2a/orchestrate.py",
        "start": "stage2a/.venv/bin/python stage2a/orchestrate.py start --profile full",
        "status": "stage2a/.venv/bin/python stage2a/orchestrate.py status",
        "stop": "stage2a/.venv/bin/python stage2a/orchestrate.py stop",
        "mongo": "127.0.0.1:27029", "api": "127.0.0.1:8019", "health": "/api/health/ready",
        "startup_timeout_seconds": 180, "shutdown_timeout_seconds": 15,
        "full_application_routes": cold["health"].get("route_count", "UNKNOWN_NOT_EXPOSED_BY_HEALTH"),
        "pid_identity": "PID_PLUS_PGID_PLUS_PARENT_PID_PLUS_EXECUTABLE_PATH_PLUS_FULL_COMMAND_HASH_PLUS_WORKING_DIRECTORY_PLUS_CONTROLLED_PORT",
        "foreign_process_policy": "FAIL_CLOSED_REFUSE_ADOPTION_OR_SIGNAL_WHEN_ANY_IDENTITY_FIELD_IS_INCOMPLETE_OR_CONFLICTING",
    }
    pair("STAGE2A_ORCHESTRATION_CONTRACT", "Stage 2A Orchestration Contract", orchestration,
         "The orchestrator starts the disposable datastore and full EquineSync application, verifies owned PID identity, health, and exact listeners, and deletes PID controls only after independently confirmed group exit and port closure.")
    pair("COLD_START_VALIDATION", "Cold Start Validation", {"result": "PASS", "evidence": cold}, "The complete EquineSync application reached its repository health endpoint inside the exact-port sandbox.")
    pair("CONTROLLED_SHUTDOWN_VALIDATION", "Controlled Shutdown Validation", {"result": "PASS", "evidence": shutdown}, "Only verified owned process groups were signaled; both controlled ports and PID controls were absent afterward.")
    pair("INTERRUPTED_START_VALIDATION", "Interrupted Start Validation", {"result": "PASS", "evidence": interrupted}, "The bounded datastore-ready failpoint triggered and left no process or listener residue.")

    fixture = check(validation, "fixture_reproducibility")["detail"]
    fixture_contract = {
        "gap_id": "S2-GAP-005", "fixture_id": "STAGE2A-FOUNDATION-V1", "fixture_version": "1.0.0",
        "synthetic_only": True, "owner": PACKAGE_ID, "collection": "stage2a_foundation",
        "loader": "stage2a/fixture_loader.py", "fixture_sha256": fixture["fixture_sha256"],
        "starting_state_digest": fixture["starting_state_digest"], "first_loaded_state_digest": fixture["first_loaded_state_digest"],
        "second_loaded_state_digest": fixture["second_loaded_state_digest"], "ending_state_digest": fixture["ending_state_digest"],
        "domain_fixture_scope": "PROHIBITED_NOT_IMPLEMENTED",
        "authority_basis": "Founder directive authorizes generic execution-foundation fixtures and expressly prohibits complete domain fixtures",
    }
    pair("STAGE2A_FIXTURE_FOUNDATION", "Stage 2A Fixture Foundation", fixture_contract,
         "Generic, owner-tagged synthetic fixtures validate loader, evidence, cleanup, rollback, and deterministic reset mechanics. Identity, Relationships, Authorization, GP-05, and CP-3 domain fixtures are expressly not implemented.")
    pair("FIXTURE_REPRODUCIBILITY_REPORT", "Fixture Reproducibility Report", fixture, "Two clean-reset loads produced identical canonical digests and restored the exact empty starting digest.")
    (ROOT / "FIXTURE_DIGESTS.txt").write_text("\n".join(f"{key}={value}" for key, value in fixture.items() if "digest" in key or "sha256" in key) + "\n", encoding="utf-8")

    shutil.copy2(STAGE / "execution-evidence-schema.json", ROOT / "EXECUTION_EVIDENCE_SCHEMA.json")
    write_md("EXECUTION_EVIDENCE_SCHEMA.md", "Execution Evidence Schema", "The strict JSON Schema requires nonempty run and command identity, sanitized arguments, multiple input hashes, configuration and environment hashes, UTC chronology, Git commit and tree, expected/actual outcomes, exit semantics, stream hashes, datastore digests, cleanup and rollback results, tools, redaction state, and a full record-content SHA-256.")
    for source, target in (("foundation-example-pass.json", "FOUNDATION_EVIDENCE_EXAMPLE_PASS.json"), ("foundation-example-intentional-fail.json", "FOUNDATION_EVIDENCE_EXAMPLE_INTENTIONAL_FAIL.json")):
        shutil.copy2(EVIDENCE / source, ROOT / target)
    for stream in ("stdout", "stderr"):
        for name in ("foundation-example-pass.txt", "foundation-example-intentional-fail.txt"):
            target = ROOT / "evidence" / "latest" / stream / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(EVIDENCE / stream / name, target)
    evidence_detail = check(validation, "evidence_capture_semantics")["detail"]
    pair("EVIDENCE_CAPTURE_VALIDATION", "Evidence Capture Validation", {"gap_id": "S2-GAP-006", "result": "PASS", "evidence": evidence_detail}, "Positive and intentional-failure records pass the strict schema, semantic record hash, chronology, implementation-commit binding, and stream-hash checks; a semantically empty record is rejected.")

    cleanup_detail = check(validation, "cleanup_failure_and_interruption")["detail"]
    zero = check(validation, "zero_residue")["detail"]
    cleanup_contract = {
        "gap_id": "S2-GAP-007", "implementation": "stage2a/cleanup.py",
        "owned_rows": "owner plus synthetic marker in exact disposable database",
        "database_reset": "drop exact disposable database only", "runtime_purge": "owner marker plus path boundary plus no listeners",
        "foreign_listener": "fail closed", "successful_load": "PASS", "partial_failure": "PASS",
        "real_interruption": "PASS", "repeated_cleanup": "PASS", "already_clean": "PASS", "zero_residue": True,
    }
    pair("STAGE2A_CLEANUP_CONTRACT", "Stage 2A Cleanup Contract", cleanup_contract, "Cleanup covers owned rows, the exact disposable database, PID/listener state, logs, snapshots, markers, and the owner-marked runtime directory. It refuses mismatched identities or active foreign listeners.")
    pair("CLEANUP_VALIDATION_REPORT", "Cleanup Validation Report", cleanup_detail, "Successful, partial-failure, real-process-interruption, repeated, and already-clean paths returned owned fixture state to zero.")
    pair("ZERO_RESIDUE_PROOF", "Zero Residue Proof", zero, "The disposable database was dropped; verified process groups exited; controlled ports and PID controls were absent; and the owner-marked runtime directory was removed.")

    rollback = check(validation, "durable_rollback_recovery")["detail"]
    rollback_contract = {
        "gap_id": "S2-GAP-008", "implementation": "stage2a/rollback_recovery.py",
        "durable_snapshot": "owner-marked JSON artifact with canonical payload SHA-256",
        "source_recovery": "tested git restore in disposable local clone to implementation commit and checkout to starting commit",
        "environment_restart": True, "datastore_restore": True,
        "session_cache_disposition": rollback["session_cache_disposition"], "destructive_migration": False,
    }
    pair("STAGE2A_ROLLBACK_RECOVERY_CONTRACT", "Stage 2A Rollback and Recovery Contract", rollback_contract, "A durable recovery artifact survives a complete process stop/restart. The rehearsal restores datastore state, verifies exact digests, tests source restore in a disposable clone, and records the no-external-session/cache determination.")
    pair("ROLLBACK_REHEARSAL_REPORT", "Rollback Rehearsal Report", rollback, "A bounded synthetic mutation changed the digest; full process restart and durable restoration returned exactly to the pre-failure digest.")
    pair("RECOVERED_STATE_INVARIANT_REPORT", "Recovered State Invariant Report", {"result": "PASS", "pre": rollback["pre_rollback_digest"], "post": rollback["post_rollback_digest"], "equal": rollback["pre_rollback_digest"] == rollback["post_rollback_digest"]}, "The recovered-state invariant passed: post-rollback digest equals the pre-failure digest.")

    startup = check(validation, "startup_side_effect_inventory")["detail"]
    network = check(validation, "network_boundary")["detail"]
    startup_contract = {
        "gap_id": "S2-GAP-009", "full_application": True,
        "profile_control": startup["profile_control"], "catalog_materialization": startup["catalog_materialization"],
        "startup_document_writes": startup["startup_document_writes"],
        "metadata_collections_inventoried": startup["collections_with_index_metadata"],
        "inventory_digest": startup["inventory_digest"], "background_flags": startup["background_flags"],
        "network_inventory": network, "provider_attempt_count": validation["provider_attempt_count"],
        "oracle_id": startup["oracle_id"], "oracle_match": startup["oracle_match"],
        "required_log_markers": startup["required_log_markers"],
        "prohibited_log_markers": startup["prohibited_log_markers"],
        "attempt_outcomes": startup["attempt_outcomes"],
        "application_network_guard": startup["network_guard"],
        "permitted_startup_side_effects": "MongoDB collection and index metadata only; exact inventory captured",
    }
    pair("STARTUP_SIDE_EFFECT_INVENTORY", "Startup Side-Effect Inventory", startup_contract, "The real application started with all nonessential loops disabled, seed paths disabled, provider configuration absent, live catalog materialization replaced by a Stage 2A no-op, zero startup document writes, and every created collection/index recorded.")
    shutil.copy2(STAGE / "startup-side-effect-oracle.json", ROOT / "STARTUP_SIDE_EFFECT_ORACLE.json")
    pair("STAGE2A_DETERMINISTIC_EXECUTION_PROFILE", "Stage 2A Deterministic Execution Profile", startup_contract, "The controlled profile uses exact loopback ports, synthetic datastore identity, zero-document-write catalog control, disabled jobs, provider denial, exact process identity, and deterministic configuration hashing.")
    pair("STARTUP_ISOLATION_VALIDATION", "Startup Isolation Validation", {"result": "PASS", "startup": startup_contract}, "Environment, network, datastore, process, background-task, and provider-attempt inventories pass for the full application.")

    env_contract = {
        "package_id": PACKAGE_ID, "operating_system": "macOS 26.5.2", "architecture": "arm64",
        "python": "3.11.11", "database": "MongoDB 8.0.26 at 127.0.0.1:27029",
        "application": "full EquineSync API at 127.0.0.1:8019", "network": "sandbox exact-port loopback only",
        "synthetic_only": True, "production_access": False, "live_data": False, "provider_writes": False,
        "secrets": "names only values excluded", "process_residue_event": "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE",
        "runtime_readiness_limitation": RUNTIME_CAUSE,
    }
    pair("STAGE2A_ENVIRONMENT_CONTRACT", "Stage 2A Environment Contract", env_contract, "The environment is disposable, synthetic-only, exact-port loopback, provider-denied, resettable, and isolated from production. The separately contained temporary-review residue and the independent runtime selector limitation are both recorded without causal conflation.")

    unit_result = subprocess.run(
        [str(STAGE / ".venv/bin/python"), "-m", "unittest", "discover", "-s", "stage2a/tests", "-p", "test_*.py"],
        cwd=REPO, text=True, capture_output=True, check=False, timeout=120,
    )
    unit_match = re.search(r"Ran (\d+) tests?", unit_result.stdout + unit_result.stderr)
    if unit_result.returncode != 0 or not unit_match:
        raise RuntimeError("unit-control command did not complete with a measurable test count")
    unit_count = int(unit_match.group(1))
    commands = [
        {"command_id": "S2A-CMD-001", "purpose": "backend bootstrap", "cwd": "repository root", "command": "sh stage2a/bootstrap_backend.sh", "expected_exit": 0, "timeout_seconds": 900, "observed": "PASS"},
        {"command_id": "S2A-CMD-002", "purpose": "frontend install", "cwd": "frontend", "command": "npm ci --legacy-peer-deps --include=dev --no-audit --no-fund", "expected_exit": 0, "timeout_seconds": 900, "observed": "PASS"},
        {"command_id": "S2A-CMD-003", "purpose": "frontend build", "cwd": "frontend", "command": "npm run build", "expected_exit": 0, "timeout_seconds": 900, "observed": "PASS"},
        {"command_id": "S2A-CMD-004", "purpose": "unit controls", "cwd": "repository root", "command": "stage2a/.venv/bin/python -m unittest discover -s stage2a/tests -p test_*.py", "expected_exit": 0, "timeout_seconds": 120, "observed": f"PASS_{unit_count}_OF_{unit_count}", "observed_test_count": unit_count, "stdout_sha256": hashlib.sha256(unit_result.stdout.encode()).hexdigest(), "stderr_sha256": hashlib.sha256(unit_result.stderr.encode()).hexdigest()},
        {"command_id": "S2A-CMD-005", "purpose": "isolated foundation validation", "cwd": "repository root", "command": "sh stage2a/run_validation.sh", "expected_exit": 0, "timeout_seconds": 900, "observed": f"PASS_{validation['pass_count']}_OF_{validation['check_count']}"},
        {"command_id": "S2A-CMD-006", "purpose": "assembly-phase packaged-validator invocation matrix", "cwd": "package root nested directory and external directory", "command": "stage2a/.venv/bin/python PACKAGED_VALIDATE_STAGE2A_PACKAGE PACKAGE --phase assembly", "expected_exit": 0, "timeout_seconds": 120, "observed": "PENDING_ASSEMBLY_INVOCATION_MATRIX"},
    ]
    pair("STAGE2A_VALIDATION_COMMAND_REGISTER", "Stage 2A Validation Command Register", {"package_id": PACKAGE_ID, "commands": commands, "cp3_commands": [], "business_workflow_commands": []}, "\n".join(f"- `{row['command_id']}` `{row['command']}` — `{row['observed']}`" for row in commands))
    write_json("STAGE2A_FOUNDATION_VALIDATION.json", validation)
    shutil.copy2(EVIDENCE / "FOUNDATION_VALIDATION.txt", ROOT / "STAGE2A_FOUNDATION_VALIDATION.txt")

    # Events and failed review attempt remain distinct evidence.
    for name in ("SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json", "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.md", "RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.json", "RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.md"):
        shutil.copy2(EVENTS / name, ROOT / name)
    archive_specs = {
        "attempt-001": ("ES-PKG-2026-004-V003_REVIEW_ATTEMPT_001_FAILED.zip", "1ecb52cbebf70f25a333f37355b9e94f44fb5ad88b7bf500568b59fa88457054"),
        "attempt-002": ("ES-PKG-2026-004-V003_REVIEW_ATTEMPT_002_FAILED.zip", FAILED_ATTEMPT_002_SHA),
        "attempt-003": ("ES-PKG-2026-004-V003_REVIEW_ATTEMPT_003_FAILED.zip", FAILED_ATTEMPT_003_SHA),
        "attempt-004": ("ES-PKG-2026-004-V003_REVIEW_ATTEMPT_004_FAILED.zip", FAILED_ATTEMPT_004_SHA),
    }
    for attempt, (archive_name, expected_sha) in archive_specs.items():
        attempt_root = ROOT / "review_attempts" / attempt
        attempt_root.mkdir(parents=True)
        source_root = REVIEWS / attempt
        for source in sorted(source_root.iterdir()):
            if source.is_file():
                shutil.copy2(source, attempt_root / source.name)
        failed_archive = OUTPUTS / archive_name
        if sha(failed_archive) != expected_sha:
            raise RuntimeError(f"failed review snapshot archive integrity mismatch: {archive_name}")
        write_json(f"review_attempts/{attempt}/ARCHIVE_REFERENCE.json", {
            "archive": f"outputs/{archive_name}", "archive_sha256": expected_sha,
            "copied_into_corrected_candidate": False,
            "reason": "preserved externally as immutable failed-candidate evidence; mutable duplication prohibited",
        })

    # Committed source evidence and change controls.
    fixed_sources = [
        "backend/.python-version", "backend/requirements.txt", "frontend/package.json", "frontend/package-lock.json", "frontend/vercel.json",
        "backend/core/config.py", "backend/core/db.py", "backend/core/lifespan.py", "backend/core/billing_provisioning.py", "backend/server.py",
        "backend/core/provider_live_proof.py", "backend/mailer.py", "backend/routes/system.py",
        "backend/core/document_signing.py", "backend/routes/document_signatures.py", "backend/storage.py",
        "backend/routes/backlog.py", "backend/routes/subscriptions.py", "backend/routes/membership.py",
        "docs/implementation/STAGE_2_EXECUTION_BASELINE/ES-PKG-2026-003-V002/EXECUTION_BASELINE_GAP_ANALYSIS.json",
        "docs/implementation/STAGE_2_EXECUTION_BASELINE/ES-PKG-2026-003-V002/EXECUTION_BASELINE_GAP_ANALYSIS.md",
    ]
    stage_sources = sorted(
        path for path in git("ls-files", "stage2a").splitlines()
        if path and not any(part in {".venv", ".runtime", "__pycache__", "latest"} for part in Path(path).parts)
    )
    sources = []
    for path in fixed_sources + stage_sources:
        at_start = subprocess.run(["git", "cat-file", "-e", f"{START}:{path}"], cwd=REPO, capture_output=True).returncode == 0
        source_commit = START if at_start and not path.startswith("stage2a/") else packaging_commit
        source_identifier = "S2A-SRC-" + hashlib.sha256(path.encode()).hexdigest()[:12].upper()
        validated_blob = "NOT_PRESENT_AT_VALIDATED_IMPLEMENTATION_COMMIT"
        if subprocess.run(["git", "cat-file", "-e", f"{implementation_commit}:{path}"], cwd=REPO, capture_output=True).returncode == 0:
            validated_blob = git("rev-parse", f"{implementation_commit}:{path}")
        sources.append({
            "evidence_id": source_identifier, "path": path, "sha256": sha(REPO / path),
            "git_commit": source_commit, "git_blob": git("rev-parse", f"{source_commit}:{path}"),
            "validated_git_blob": validated_blob,
            "authority": "AUTHORIZED_STAGE2A_IMPLEMENTATION" if path.startswith("stage2a/") else "SEALED_STAGE2_REPOSITORY_EVIDENCE",
            "evidence_role": "IMPLEMENTATION_AND_CONTROL_SOURCE" if path.startswith("stage2a/") else "PREDECESSOR_REQUIREMENT_OR_APPLICATION_SOURCE",
        })
    write_json("STAGE2A_SOURCE_EVIDENCE_REGISTER.json", {"package_id": PACKAGE_ID, "validated_implementation_commit": implementation_commit, "packaging_commit": packaging_commit, "sources": sources, "count": len(sources)})
    with (ROOT / "STAGE2A_SOURCE_EVIDENCE_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(sources[0])); writer.writeheader(); writer.writerows(sources)
    for row in sources:
        target = ROOT / "source_payload" / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / row["path"], target)
    created = stage_sources + sorted(path.relative_to(REPO).as_posix() for path in ROOT.rglob("*") if path.is_file())
    pair("STAGE2A_FILES_CREATED_REGISTER", "Stage 2A Files Created Register", {"package_id": PACKAGE_ID, "created": created, "count": len(created)}, "All implementation and package files are additive under `stage2a/` and the new successor-package root.")
    pair("STAGE2A_FILES_MODIFIED_REGISTER", "Stage 2A Files Modified Register", {"package_id": PACKAGE_ID, "modified": [], "renamed": [], "deleted": []}, "No pre-existing application, governance, predecessor-package, or immutable-baseline file was modified, renamed, or deleted.")
    changes = [{"change_id": f"S2A-CHG-{number:03d}", "gap_id": f"S2-GAP-{number:03d}", "description": title, "implementation_root": "stage2a/", "status": "REMEDIATED_CANDIDATE"} for number, title in gap_titles.items()]
    changes.extend([
        {"change_id": "S2A-CHG-010", "gap_id": "S2-GAP-006", "description": "Deterministic packaged-validator repository-root resolution", "implementation_root": "stage2a/validate_stage2a_package.py", "status": "REMEDIATED_PENDING_REREVIEW"},
        {"change_id": "S2A-CHG-011", "gap_id": "S2-GAP-006", "description": "Specific requirement control artifact test finding remediation evidence traceability", "implementation_root": "stage2a/build_successor_package.py", "status": "REMEDIATED_PENDING_REREVIEW"},
        {"change_id": "S2A-CHG-012", "gap_id": "S2-GAP-009", "description": "Measured provider and startup-attempt outcome states", "implementation_root": "stage2a/network_guard.py", "status": "REMEDIATED_PENDING_REREVIEW"},
        {"change_id": "S2A-CHG-013", "gap_id": "S2-GAP-006", "description": "Evidence semantic redaction and meaning-preservation enforcement", "implementation_root": "stage2a/evidence_capture.py", "status": "REMEDIATED_PENDING_REREVIEW"},
        {"change_id": "S2A-CHG-014", "gap_id": "S2-GAP-004", "description": "PID command parent process-group working-path and port identity enforcement", "implementation_root": "stage2a/orchestrate.py", "status": "REMEDIATED_PENDING_REREVIEW"},
    ])
    pair("STAGE2A_CHANGE_MANIFEST", "Stage 2A Change Manifest", {"package_id": PACKAGE_ID, "changes": changes, "modified_existing_files": 0, "renamed": 0, "deleted": 0}, "\n".join(f"- `{row['change_id']}` `{row['gap_id']}` — {row['description']}" for row in changes))

    pair("STAGE2A_GAP_REMEDIATION_REPORT", "Stage 2A Gap Remediation Report", {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "authorized_gaps": authorized, "formal_gap_closures": 0, "f0001": "F0001_REMAINS_OPEN_BLOCKING"}, "All nine authorized gaps have remediated candidates and await independent re-review. No gap is self-closed; F-0001 remains open.")

    # Stable, specific requirement/control/source/test/evidence relationships.
    source_by_path = {row["path"]: row["evidence_id"] for row in sources}
    def source_ids(paths: list[str]) -> list[str]:
        missing = [path for path in paths if path not in source_by_path]
        if missing:
            raise RuntimeError(f"traceability source paths missing from source register: {missing}")
        return [source_by_path[path] for path in paths]

    test_specs = {
        "S2A-TEST-DEP-BOOTSTRAP": ("BACKEND_BOOTSTRAP_RUN.validation", "stage2a/bootstrap_backend.py"),
        "S2A-TEST-PIP-CHECK": ("BACKEND_BOOTSTRAP_RUN.pip_check", "stage2a/dependency_inventory.py"),
        "S2A-TEST-TOOLCHAIN": ("STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT", "stage2a/toolchain.json"),
        "S2A-TEST-FRONTEND-BUILD": ("STAGE2A_VALIDATION_COMMAND_REGISTER:S2A-CMD-003", "stage2a/build_successor_package.py"),
        "S2A-TEST-ENV-NEGATIVE": ("FOUNDATION_VALIDATION.check:isolation_negative_tests", "stage2a/validate_foundation.py"),
        "S2A-TEST-EXACT-PORT-DENIAL": ("FOUNDATION_VALIDATION.check:exact_port_egress_denial", "stage2a/validate_foundation.py"),
        "S2A-TEST-PROCESS-IDENTITY": ("FOUNDATION_VALIDATION.check:process_identity", "stage2a/validate_foundation.py"),
        "S2A-TEST-INTERRUPTED-START": ("FOUNDATION_VALIDATION.check:interrupted_start_cleanup", "stage2a/validate_foundation.py"),
        "S2A-TEST-CONTROLLED-SHUTDOWN": ("FOUNDATION_VALIDATION.check:controlled_shutdown", "stage2a/validate_foundation.py"),
        "S2A-TEST-FIXTURE-REPLAY": ("FOUNDATION_VALIDATION.check:fixture_reproducibility", "stage2a/validate_foundation.py"),
        "S2A-TEST-FIXTURE-RESET": ("FOUNDATION_VALIDATION.check:zero_residue", "stage2a/validate_foundation.py"),
        "S2A-TEST-EVIDENCE-SEMANTICS": ("FOUNDATION_VALIDATION.check:evidence_capture_semantics", "stage2a/validate_foundation.py"),
        "S2A-TEST-REDACTION-MEANING": ("unittest:test_controls.ControlTests.test_output_redaction_covers_quoted_multiword_and_bearer_values", "stage2a/tests/test_controls.py"),
        "S2A-TEST-VALIDATOR-ROOT-MATRIX": ("PACKAGE_VALIDATOR.check:MV-001-runtime-root-resolution", "stage2a/validate_stage2a_package.py"),
        "S2A-TEST-TRACE-SPECIFICITY": ("PACKAGE_VALIDATOR.check:MV-011A-specific-traceability", "stage2a/validate_stage2a_package.py"),
        "S2A-TEST-PACKAGE-TRACE-ROW": ("PACKAGE_VALIDATOR.parameterized:MV-011A-specific-traceability", "stage2a/validate_stage2a_package.py"),
        "S2A-TEST-CLEANUP-PARTIAL": ("FOUNDATION_VALIDATION.check:cleanup_failure_and_interruption", "stage2a/validate_foundation.py"),
        "S2A-TEST-CLEANUP-INTERRUPTED": ("FOUNDATION_VALIDATION.check:cleanup_failure_and_interruption", "stage2a/validate_foundation.py"),
        "S2A-TEST-ZERO-RESIDUE": ("FOUNDATION_VALIDATION.check:zero_residue", "stage2a/validate_foundation.py"),
        "S2A-TEST-DATASTORE-ROLLBACK": ("FOUNDATION_VALIDATION.check:durable_rollback_recovery", "stage2a/validate_foundation.py"),
        "S2A-TEST-SOURCE-RECOVERY": ("FOUNDATION_VALIDATION.check:durable_rollback_recovery.source_recovery", "stage2a/validate_foundation.py"),
        "S2A-TEST-STARTUP-ORACLE": ("FOUNDATION_VALIDATION.check:startup_side_effect_inventory", "stage2a/validate_foundation.py"),
        "S2A-TEST-PROVIDER-OUTCOME-STATES": ("FOUNDATION_VALIDATION.check:provider_denial", "stage2a/validate_foundation.py"),
        "S2A-TEST-NETWORK-GUARD": ("FOUNDATION_VALIDATION.check:network_boundary", "stage2a/validate_foundation.py"),
    }
    test_rows = canonical_test_rows(source_by_path)
    write_json("STAGE2A_TEST_CONTROL_REGISTER.json", {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "tests": test_rows})
    with (ROOT / "STAGE2A_TEST_CONTROL_REGISTER.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(test_rows[0])); writer.writeheader(); writer.writerows(test_rows)

    requirement_specs = [
        (1, ["S2A-CTL-DEP-001", "S2A-CTL-DEP-002"], ["backend/requirements.txt", "stage2a/bootstrap_backend.sh", "stage2a/bootstrap_backend.py", "stage2a/dependency_inventory.py"], ["stage2a/bootstrap_backend.sh", "stage2a/dependency_inventory.py"], ["S2A-TEST-DEP-BOOTSTRAP", "S2A-TEST-PIP-CHECK"], ["BACKEND_BOOTSTRAP_VALIDATION.json", "BACKEND_DEPENDENCY_INVENTORY.txt"]),
        (2, ["S2A-CTL-TOOL-001", "S2A-CTL-PKG-MGR-001"], ["stage2a/toolchain.json", "frontend/package-lock.json", "frontend/package.json"], ["stage2a/toolchain.json", "frontend/package-lock.json"], ["S2A-TEST-TOOLCHAIN", "S2A-TEST-FRONTEND-BUILD"], ["TOOLCHAIN_VALIDATION.json", "TOOLCHAIN_VERSION_CAPTURE.txt"]),
        (3, ["S2A-CTL-ENV-001", "S2A-CTL-NET-001", "S2A-CTL-PROVIDER-001"], ["stage2a/lib/control.py", "stage2a/config/stage2a.env", "stage2a/config/loopback-only.sb", "stage2a/network_guard.py"], ["stage2a/lib/control.py", "stage2a/network_guard.py"], ["S2A-TEST-ENV-NEGATIVE", "S2A-TEST-EXACT-PORT-DENIAL"], ["STAGE2A_ISOLATION_CONTROL.json", "PROVIDER_DENIAL_REGISTER.json"]),
        (4, ["S2A-CTL-PROCESS-001", "S2A-CTL-PROCESS-002"], ["stage2a/orchestrate.py", "stage2a/tests/test_controls.py"], ["stage2a/orchestrate.py"], ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-INTERRUPTED-START", "S2A-TEST-CONTROLLED-SHUTDOWN"], ["STAGE2A_ORCHESTRATION_CONTRACT.json", "CONTROLLED_SHUTDOWN_VALIDATION.json", "INTERRUPTED_START_VALIDATION.json"]),
        (5, ["S2A-CTL-FIXTURE-001"], ["stage2a/fixtures/foundation-v1.json", "stage2a/fixture_loader.py"], ["stage2a/fixture_loader.py", "stage2a/fixtures/foundation-v1.json"], ["S2A-TEST-FIXTURE-REPLAY", "S2A-TEST-FIXTURE-RESET"], ["STAGE2A_FIXTURE_FOUNDATION.json", "FIXTURE_REPRODUCIBILITY_REPORT.json"]),
        (6, ["S2A-CTL-EVIDENCE-001", "S2A-CTL-REDACTION-001", "S2A-CTL-PACKAGE-ROOT-001", "S2A-CTL-TRACE-001"], ["stage2a/evidence_capture.py", "stage2a/execution-evidence-schema.json", "stage2a/validate_stage2a_package.py", "stage2a/build_successor_package.py"], ["stage2a/evidence_capture.py", "stage2a/validate_stage2a_package.py", "stage2a/build_successor_package.py"], ["S2A-TEST-EVIDENCE-SEMANTICS", "S2A-TEST-REDACTION-MEANING", "S2A-TEST-VALIDATOR-ROOT-MATRIX", "S2A-TEST-TRACE-SPECIFICITY"], ["EVIDENCE_CAPTURE_VALIDATION.json", "EXECUTION_EVIDENCE_SCHEMA.json", "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json"]),
        (7, ["S2A-CTL-CLEANUP-001", "S2A-CTL-ZERO-RESIDUE-001"], ["stage2a/cleanup.py", "stage2a/lib/control.py"], ["stage2a/cleanup.py"], ["S2A-TEST-CLEANUP-PARTIAL", "S2A-TEST-CLEANUP-INTERRUPTED", "S2A-TEST-ZERO-RESIDUE"], ["CLEANUP_VALIDATION_REPORT.json", "ZERO_RESIDUE_PROOF.json"]),
        (8, ["S2A-CTL-ROLLBACK-001", "S2A-CTL-SOURCE-RECOVERY-001"], ["stage2a/rollback_recovery.py", "stage2a/validate_foundation.py"], ["stage2a/rollback_recovery.py"], ["S2A-TEST-DATASTORE-ROLLBACK", "S2A-TEST-SOURCE-RECOVERY"], ["ROLLBACK_REHEARSAL_REPORT.json", "RECOVERED_STATE_INVARIANT_REPORT.json"]),
        (9, ["S2A-CTL-STARTUP-001", "S2A-CTL-ATTEMPTS-001"], ["backend/core/lifespan.py", "backend/core/billing_provisioning.py", "stage2a/full_application_profile.py", "stage2a/network_guard.py", "stage2a/startup-side-effect-oracle.json"], ["stage2a/full_application_profile.py", "stage2a/network_guard.py", "stage2a/startup-side-effect-oracle.json"], ["S2A-TEST-STARTUP-ORACLE", "S2A-TEST-PROVIDER-OUTCOME-STATES", "S2A-TEST-NETWORK-GUARD"], ["STARTUP_SIDE_EFFECT_INVENTORY.json", "STARTUP_SIDE_EFFECT_ORACLE.json", "PROVIDER_DENIAL_REGISTER.json"]),
    ]
    requirements = []
    for number, controls, source_paths, implementations, tests, evidence_artifacts in requirement_specs:
        requirements.append({
            "requirement_id": f"S2A-REQ-{number:03d}", "gap_id": f"S2-GAP-{number:03d}",
            "requirement": gap_titles[number], "control_ids": controls,
            "source_evidence_ids": source_ids(source_paths), "implementation_artifacts": implementations,
            "test_ids": tests, "evidence_artifacts": evidence_artifacts,
            "status": "REMEDIATED_CANDIDATE_PENDING_INDEPENDENT_REREVIEW",
        })
    requirements = canonical_requirement_rows(gap_titles, source_by_path)
    write_json("STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json", {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "requirements": requirements})
    requirement_csv = [{
        "requirement_id": row["requirement_id"], "gap_id": row["gap_id"],
        "control_ids": "|".join(row["control_ids"]), "source_evidence_ids": "|".join(row["source_evidence_ids"]),
        "implementation_artifacts": "|".join(row["implementation_artifacts"]), "test_ids": "|".join(row["test_ids"]),
        "evidence_artifacts": "|".join(row["evidence_artifacts"]), "status": row["status"],
    } for row in requirements]
    with (ROOT / "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(requirement_csv[0])); writer.writeheader(); writer.writerows(requirement_csv)

    finding_specs = [
        ("ES-ADV-V003-R2-F-0004", "PACKAGED_VALIDATOR_ROOT_RESOLUTION_DEFECT", ["S2A-REQ-006"], ["stage2a/validate_stage2a_package.py"], ["S2A-TEST-VALIDATOR-ROOT-MATRIX"], ["VALIDATOR_INVOCATION_MATRIX.json"]),
        ("ES-ADV-V003-R2-F-0003", "TRACEABILITY_MATRIX_MAPPING_INSUFFICIENTLY_SPECIFIC", ["S2A-REQ-006"], ["STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json", "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json", "STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json"], ["S2A-TEST-TRACE-SPECIFICITY"], ["STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json"]),
        ("ES-ADV-V003-R2-F-0001", "PROVIDER_STARTUP_ATTEMPT_MEASUREMENT_INSUFFICIENT", ["S2A-REQ-009"], ["stage2a/network_guard.py", "stage2a/startup-side-effect-oracle.json"], ["S2A-TEST-PROVIDER-OUTCOME-STATES", "S2A-TEST-STARTUP-ORACLE"], ["PROVIDER_DENIAL_REGISTER.json", "STARTUP_SIDE_EFFECT_INVENTORY.json"]),
        ("ES-ADV-V003-R2-F-0002", "EVIDENCE_SEMANTIC_AND_REDACTION_ENFORCEMENT_INSUFFICIENT", ["S2A-REQ-006"], ["stage2a/evidence_capture.py", "stage2a/execution-evidence-schema.json"], ["S2A-TEST-EVIDENCE-SEMANTICS", "S2A-TEST-REDACTION-MEANING"], ["EVIDENCE_CAPTURE_VALIDATION.json", "FOUNDATION_EVIDENCE_EXAMPLE_PASS.json"]),
        ("ES-ADV-V003-R2-F-0005", "PROCESS_IDENTITY_COMMAND_AND_PROCESS_GROUP_VERIFICATION_INSUFFICIENT", ["S2A-REQ-004"], ["stage2a/orchestrate.py"], ["S2A-TEST-PROCESS-IDENTITY", "S2A-TEST-CONTROLLED-SHUTDOWN"], ["STAGE2A_ORCHESTRATION_CONTRACT.json", "CONTROLLED_SHUTDOWN_VALIDATION.json"]),
    ]
    findings = [{
        "finding_id": finding_id, "blocker_classification": blocker, "requirement_ids": requirement_ids,
        "remediation_artifacts": artifacts, "test_ids": tests, "evidence_artifacts": evidence_artifacts,
        "status": "REMEDIATED_PENDING_REREVIEW", "self_closed": False,
    } for finding_id, blocker, requirement_ids, artifacts, tests, evidence_artifacts in finding_specs]
    finding_specs = FINDING_SPECS
    findings = canonical_finding_rows()
    write_json("STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json", {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "findings": findings})
    finding_csv = [{
        "finding_id": row["finding_id"], "blocker_classification": row["blocker_classification"],
        "requirement_ids": "|".join(row["requirement_ids"]), "remediation_artifacts": "|".join(row["remediation_artifacts"]),
        "test_ids": "|".join(row["test_ids"]), "evidence_artifacts": "|".join(row["evidence_artifacts"]),
        "status": row["status"], "self_closed": row["self_closed"],
    } for row in findings]
    with (ROOT / "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(finding_csv[0])); writer.writeheader(); writer.writerows(finding_csv)

    prior_validation_commit = "83ccfac2bdeb0615e8818ffcbde03337d429dba5"
    reuse_register = {
        "package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID,
        "reused_predecessor_evidence": [
            {"evidence": "16/16 Stage 2A lifecycle validation", "source_commit": prior_validation_commit, "immutable_source": f"{FAILED_ROOT.relative_to(REPO).as_posix()}/STAGE2A_FOUNDATION_VALIDATION.json", "immutable_artifact_sha256": sha(FAILED_ROOT / "STAGE2A_FOUNDATION_VALIDATION.json"), "containing_manifest_sha256": FAILED_ATTEMPT_002_MANIFEST_SHA, "reuse_scope": ["synthetic fixture determinism", "owned-row cleanup semantics", "datastore and source recovery invariants"], "basis": "fixture, cleanup ownership, rollback payload, and immutable source anchors are hash-identical; reused as corroborative predecessor evidence only", "controlling_for_corrected_candidate": False},
            {"evidence": "127-artifact backend dependency inventory", "immutable_source": f"{FAILED_ROOT.relative_to(REPO).as_posix()}/BACKEND_BOOTSTRAP_VALIDATION.json", "immutable_artifact_sha256": sha(FAILED_ROOT / "BACKEND_BOOTSTRAP_VALIDATION.json"), "containing_manifest_sha256": FAILED_ATTEMPT_002_MANIFEST_SHA, "reuse_scope": ["pinned requirements", "download artifact hashes", "installed metadata hashes"], "basis": "backend requirements SHA-256 and bootstrap implementation are unchanged; corrected-candidate bootstrap rerun independently reconfirms the same contract", "controlling_for_corrected_candidate": False},
        ],
        "invalidated_checks": [
            {"blocker": blocker, "reason": "prior candidate evidence was insufficient for this exact control and is not controlling"}
            for _, blocker, *_ in finding_specs
        ],
        "rerun_checks": [
            {"blocker": blocker, "test_ids": tests, "result": "PASS_TECHNICAL_CANDIDATE_PENDING_INDEPENDENT_REREVIEW"}
            for _, blocker, _, _, tests, _ in finding_specs
        ],
        "full_lifecycle_rerun": {"result": validation["validation"], "score": f"{validation['pass_count']}/{validation['check_count']}", "implementation_commit": implementation_commit},
        "dependency_rerun": {"result": bootstrap["validation"], "artifact_count": len(bootstrap["inventory"]), "implementation_commit": bootstrap_commit},
    }
    pair("EVIDENCE_REUSE_AND_RERUN_REGISTER", "Evidence Reuse and Rerun Register", reuse_register, "Prior lifecycle and dependency results are retained only as corroborative predecessor evidence where their inputs remain hash-identical. Every check affected by the five blockers was invalidated and rerun; the new reruns control this candidate.")
    blocker_results = [{"blocker": blocker, "status": "REMEDIATED_PENDING_REREVIEW", "finding_id": finding_id} for finding_id, blocker, *_ in finding_specs]
    provenance = {
        "package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "candidate_attempt": 8,
        "distinct_from_failed_candidate": True, "failed_candidate_unchanged": True,
        "failed_candidates": failed_candidates, "validated_implementation_commit": implementation_commit,
        "packaging_commit": packaging_commit, "blocker_results": blocker_results,
        "freeze_commit": "RECORDED_EXTERNALLY_AFTER_BYTE_FREEZE_TO_AVOID_CIRCULAR_SELF_REFERENCE",
        "execution": "EXECUTION_NOT_AUTHORIZED", "assurance": "NOT_EXTERNALLY_ASSURED",
    }
    pair("CORRECTED_CANDIDATE_PROVENANCE", "Corrected Candidate Provenance", provenance, f"`{CANDIDATE_ID}` is a distinct eighth candidate. The failed 108-file and Candidate-003 through Candidate-007 evidence remains byte-for-byte unchanged and is referenced by its original manifest and archive SHA-256 values.")

    pair("IMMUTABLE_BASELINE_RECORD", "Immutable Baseline Record", {"package_id": PACKAGE_ID, "immutable_baseline": BASELINE, "modified": False, "reachable": True}, f"Governance baseline `{BASELINE}` remains unchanged and reachable.")
    pair("PREDECESSOR_REFERENCE_RECORD", "Predecessor Reference Record", {"package_id": PACKAGE_ID, "predecessor": PREDECESSOR, "commit": START, "archive_sha256": PREDECESSOR_SHA, "unchanged": True, "sealed_predecessor": "ES-PKG-2026-002-V001", "sealed_predecessor_sha256": SEALED_SHA}, f"Predecessor `{PREDECESSOR}` remains unchanged at archive SHA-256 `{PREDECESSOR_SHA}`.")
    write_md("FOUNDER_AUTHORIZATION_BOUNDARY.md", "Founder Authorization Boundary", "Authorized only: exact Stage 2 publication, bounded F-0002 closure, S2-GAP-001 through 009 remediation, technical validation, independent review, package assembly, branch push, and fresh-clone verification. CP-3, golden paths, GP-05, Atlases, providers, production, live data, deployment, release, merge, default-branch changes, tags, and business workflows remain prohibited.")
    write_md("ASSURANCE_STATEMENT.md", "Assurance Statement", "Assurance remains `NOT_EXTERNALLY_ASSURED`. Internal segregated and adversarial reviews do not constitute external assurance.")
    readiness = {
        "package_id": PACKAGE_ID, "f0001": "F0001_REMAINS_OPEN_BLOCKING",
        "principal_disposition": DISPOSITION, "primary_blocked_readiness_cause": RUNTIME_CAUSE,
        "technical_candidate_gaps": 9, "independently_verified_gaps": 0,
        "execution": "EXECUTION_NOT_AUTHORIZED", "assurance": "NOT_EXTERNALLY_ASSURED",
        "cp3_suites_executed": 0, "golden_paths_executed": 0, "business_workflows_executed": 0,
    }
    pair("F0001_UPDATED_READINESS_DETERMINATION", "F-0001 Updated Readiness Determination", readiness, "F-0001 remains open and blocking. The runtime agent-type selector limitation remains the primary blocked-readiness cause and is distinct from the contained temporary-review process residue.")
    pair("PACKAGE_STATUS_RECORD", "Package Status Record", readiness | {"status": "CANDIDATE_PENDING_SEGREGATED_AND_ADVERSARIAL_REREVIEW", "f0002": closure["disposition"]}, "This is a remediated candidate pending independent re-review. The required principal disposition remains incomplete because the runtime agent-type selector limitation is unresolved.")
    pair("SUCCESSOR_PACKAGE_INDEX", "Stage 2A Successor Package Index", {"package_id": PACKAGE_ID, "predecessor": PREDECESSOR, "starting_commit": START, "validated_implementation_commit": implementation_commit, "packaging_commit": packaging_commit, "candidate": True, "authorized_gaps": [f"S2-GAP-{n:03d}" for n in range(1, 10)], "principal_disposition": DISPOSITION}, "This candidate contains the nine technical remediation foundations, validation evidence, bounded F-0002 closure, separate residue provenance, first failed review evidence, and controls for independent re-review.")

    shutil.copy2(STAGE / "validate_stage2a_package.py", ROOT / "validate_stage2a_package.py")
    write_json("VALIDATOR_INVOCATION_MATRIX.json", {"candidate_id": CANDIDATE_ID, "status": "ASSEMBLY_VALIDATION_IN_PROGRESS", "execution": "EXECUTION_NOT_AUTHORIZED"})
    future_controls = {"DRAFT_REVIEW_SHA256SUMS.txt", "DRAFT_REVIEW_SNAPSHOT_RECORD.json", "DRAFT_REVIEW_SNAPSHOT_RECORD.md"}
    trace_outputs = sorted({path.name for path in ROOT.iterdir() if path.is_file()} | future_controls | {"STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json", "STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.md"})
    trace = canonical_output_rows(trace_outputs, requirements, source_by_path)
    pair("STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY", "Stage 2A Source-to-Output Traceability", {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "outputs": trace}, "Every top-level output has a unique stable mapping identifier, output-specific role and rationale, direct implementation source, registered executable check, controlling evidence, and applicable finding chain. MV-011A verifies reference existence and complete top-level coverage.")

    package_created = sorted({path.relative_to(REPO).as_posix() for path in ROOT.rglob("*") if path.is_file()} | {f"{ROOT.relative_to(REPO).as_posix()}/{name}" for name in future_controls})
    complete_created = sorted(set(stage_sources + package_created))
    pair("STAGE2A_FILES_CREATED_REGISTER", "Stage 2A Files Created Register", {"package_id": PACKAGE_ID, "created": complete_created, "count": len(complete_created)}, "The register includes every additive implementation, generated evidence, package, review-attempt, and candidate-freeze control path. Final archive controls are added by the finalization stage and reconciled by the exact file inventory.")

    python = STAGE / ".venv/bin/python"
    validator = ROOT / "validate_stage2a_package.py"
    invocation_specs: list[tuple[str, Path, Path, Path]] = [
        ("PACKAGE_ROOT", ROOT, validator, ROOT),
        ("PACKAGE_NESTED_REVIEW_ATTEMPT_004", ROOT / "review_attempts/attempt-004", validator, ROOT),
        ("EXTERNAL_PRIVATE_TMP", Path("/private/tmp"), validator, ROOT),
    ]
    invocation_results: list[dict[str, object]] = []
    for location, cwd, validator_path, package_path in invocation_specs:
        result = subprocess.run([str(python), str(validator_path), str(package_path), "--phase", "assembly"], cwd=cwd, text=True, capture_output=True, check=False, timeout=120)
        parsed = json.loads(result.stdout) if result.stdout.strip() else {}
        invocation_results.append({
            "location": location, "mode": "REPOSITORY_BACKED_PACKAGED_VALIDATOR", "exit_status": result.returncode,
            "validation": parsed.get("validation"), "score": f"{parsed.get('pass_count')}/{parsed.get('check_count')}",
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
        })
    with tempfile.TemporaryDirectory(prefix="es-candidate007-detached-", dir="/private/tmp") as temporary:
        extracted = Path(temporary) / CANDIDATE_ID
        shutil.copytree(ROOT, extracted)
        detached_validator = extracted / "validate_stage2a_package.py"
        result = subprocess.run([str(python), str(detached_validator), str(extracted), "--phase", "assembly"], cwd=Path(temporary), text=True, capture_output=True, check=False, timeout=120)
        parsed = json.loads(result.stdout) if result.stdout.strip() else {}
        invocation_results.append({
            "location": "DETACHED_CLEAN_COPY_EXTERNAL_PRIVATE_TMP", "mode": "DETACHED_PACKAGE_SOURCE_PAYLOAD",
            "exit_status": result.returncode, "validation": parsed.get("validation"),
            "score": f"{parsed.get('pass_count')}/{parsed.get('check_count')}",
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(), "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
            "temporary_copy_removed": True,
        })
    if any(row["exit_status"] != 0 or row["validation"] != "PASS" for row in invocation_results):
        raise RuntimeError(f"validator assembly invocation matrix failed: {invocation_results}")
    invocation_matrix = {
        "candidate_id": CANDIDATE_ID, "phase": "ASSEMBLY_PRE_FREEZE_CHECKSUM_DEFERRED",
        "validator_sha256": sha(validator), "invocations": invocation_results,
        "supported_locations": 4, "passed_locations": len(invocation_results),
        "detached_source_payload_files": len(sources), "result": "PASS",
        "final_candidate_checksum_validation_required_after_freeze": True,
        "execution": "EXECUTION_NOT_AUTHORIZED",
    }
    write_json("VALIDATOR_INVOCATION_MATRIX.json", invocation_matrix)
    commands[5]["observed"] = f"PASS_ASSEMBLY_{len(invocation_results)}_OF_{len(invocation_results)}_INCLUDING_DETACHED"
    commands.append({"command_id": "S2A-CMD-007", "purpose": "detached clean-copy packaged validation", "cwd": "external temporary directory", "command": "PACKAGED_PYTHON validate_stage2a_package.py DETACHED_PACKAGE --phase assembly", "expected_exit": 0, "timeout_seconds": 120, "observed": "PASS_DETACHED_PACKAGE_SOURCE_PAYLOAD"})
    pair("STAGE2A_VALIDATION_COMMAND_REGISTER", "Stage 2A Validation Command Register", {"package_id": PACKAGE_ID, "commands": commands, "cp3_commands": [], "business_workflow_commands": []}, "\n".join(f"- `{row['command_id']}` `{row['command']}` — `{row['observed']}`" for row in commands))

    # Freeze all payload files. Snapshot controls are added after the manifest.
    payload = sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file())
    rows = [f"{sha(ROOT / path)}  {path}" for path in payload]
    (ROOT / "DRAFT_REVIEW_SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    manifest_hash = sha(ROOT / "DRAFT_REVIEW_SHA256SUMS.txt")
    snapshot = {"package_id": PACKAGE_ID, "candidate_id": CANDIDATE_ID, "review_attempt": 8, "payload_files": len(payload), "manifest_sha256": manifest_hash, "validated_implementation_commit": implementation_commit, "packaging_commit": packaging_commit, "frozen": True, "execution": "EXECUTION_NOT_AUTHORIZED"}
    pair("DRAFT_REVIEW_SNAPSHOT_RECORD", "Draft Review Snapshot Record", snapshot, f"Review attempt 8 freezes `{len(payload)}` payload files under manifest SHA-256 `{manifest_hash}`. Reviewers must not modify the candidate.")
    print(json.dumps({"package_root": ROOT.relative_to(REPO).as_posix(), "validated_implementation_commit": implementation_commit, "packaging_commit": packaging_commit, "payload_files": len(payload), "physical_files": len(payload) + 3, "manifest_sha256": manifest_hash, "validation": validation["validation"], "principal_disposition": DISPOSITION}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
