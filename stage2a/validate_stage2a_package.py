#!/usr/bin/env python3
"""Read-only machine validation for the Stage 2A successor package."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker

PACKAGE_ID = "ES-PKG-2026-004-V003"
CANDIDATE_ID = "ES-PKG-2026-004-V003-CANDIDATE-004"
START = "0be6172a28b75238c5facabf91d43ed09aaf0d54"
BASELINE = "acb518ea5a160820e64681ff95a16b010fe1156c"
PREDECESSOR_SHA = "b7193e9a4cac078a87c45e31d708f787b40e7e7e973eee7c3f327680a7e32329"
BRANCH = "codex/stage2a-execution-foundation-remediation"
REQUIRED = {
    "SUCCESSOR_PACKAGE_INDEX.md", "SUCCESSOR_PACKAGE_INDEX.json",
    "PACKAGE_STATUS_RECORD.md", "PACKAGE_STATUS_RECORD.json",
    "FOUNDER_AUTHORIZATION_BOUNDARY.md", "IMMUTABLE_BASELINE_RECORD.json",
    "PREDECESSOR_REFERENCE_RECORD.json", "F0002_FOUNDER_AUTHORIZED_CLOSURE.json",
    "STAGE2A_SCOPE_REGISTER.json", "STAGE2A_CHANGE_MANIFEST.json",
    "STAGE2A_FILES_CREATED_REGISTER.json", "STAGE2A_FILES_MODIFIED_REGISTER.json",
    "STAGE2A_SOURCE_EVIDENCE_REGISTER.json", "STAGE2A_SOURCE_EVIDENCE_REGISTER.csv",
    "STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json", "STAGE2A_GAP_REMEDIATION_REPORT.json",
    "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json", "STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.csv",
    "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json", "STAGE2A_FINDING_TO_REMEDIATION_MATRIX.csv",
    "STAGE2A_TEST_CONTROL_REGISTER.json", "STAGE2A_TEST_CONTROL_REGISTER.csv",
    "CORRECTED_CANDIDATE_PROVENANCE.json", "EVIDENCE_REUSE_AND_RERUN_REGISTER.json",
    "VALIDATOR_INVOCATION_MATRIX.json",
    "STAGE2A_VALIDATION_COMMAND_REGISTER.json", "STAGE2A_ENVIRONMENT_CONTRACT.json",
    "STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT.json", "PROVIDER_DENIAL_REGISTER.json",
    "PROVIDER_DENIAL_REGISTER.csv", "STAGE2A_FIXTURE_FOUNDATION.json",
    "EXECUTION_EVIDENCE_SCHEMA.json", "CLEANUP_VALIDATION_REPORT.json",
    "ROLLBACK_REHEARSAL_REPORT.json", "STARTUP_SIDE_EFFECT_INVENTORY.json",
    "STARTUP_SIDE_EFFECT_ORACLE.json",
    "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json",
    "RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.json", "ASSURANCE_STATEMENT.md",
    "F0001_UPDATED_READINESS_DETERMINATION.json", "validate_stage2a_package.py",
}
FINAL_REQUIRED = {
    "STAGE2A_SEGREGATED_REVIEW.json", "STAGE2A_ADVERSARIAL_REVIEW.json",
    "STAGE2A_FINDINGS_REGISTER.json", "STAGE2A_FINDING_RECONCILIATION.json",
    "SUCCESSOR_PACKAGE_MACHINE_VALIDATION.json", "EXACT_FILE_INVENTORY.json",
    "SUCCESSOR_PACKAGE_MANIFEST.json", "SUCCESSOR_PACKAGE_SHA256SUMS.txt",
    "SUCCESSOR_PACKAGE_CLEAN_EXTRACTION_VERIFICATION.json",
}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
SENSITIVE_KEY = r"(?:secret|token|password|api[_-]?key|credential|authorization|bearer)"
SENSITIVE_QUOTED_ASSIGNMENT = re.compile(rf"(?i)(?P<prefix>[\"']?{SENSITIVE_KEY}[\"']?\s*[:=]\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)")
SENSITIVE_ASSIGNMENT = re.compile(rf"(?im)(?P<prefix>\b{SENSITIVE_KEY}\b\s*[:=]\s*)(?P<value>.*?)(?=\s+[A-Za-z_][A-Za-z0-9_-]*\s*[:=]|\s*$|[,;])")
KNOWN_SECRET_VALUE = re.compile(r"(?:sk_(?:live|test)_[A-Za-z0-9_-]+|whsec_[A-Za-z0-9_-]+|AKIA[A-Z0-9]{12,})")


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=False)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def locate_repository(script_path: Path) -> Path | None:
    """Resolve the repository independently of the invocation working directory."""
    resolved = script_path.resolve()
    for candidate in (resolved.parent, *resolved.parents):
        if (candidate / ".git").exists() and (candidate / "stage2a").is_dir():
            return candidate
    return None


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def semantic_record_errors(root: Path, record: dict[str, object]) -> list[str]:
    errors: list[str] = []
    expected = record.get("expected_result", {}).get("exit_status") if isinstance(record.get("expected_result"), dict) else None
    actual = record.get("actual_result", {}).get("exit_status") if isinstance(record.get("actual_result"), dict) else None
    if actual != record.get("exit_status"):
        errors.append("actual/top-level exit mismatch")
    if record.get("result") != ("PASS" if actual == expected else "FAIL"):
        errors.append("result does not match expected-versus-actual exit status")
    try:
        if dt.datetime.fromisoformat(str(record["utc_end"])) < dt.datetime.fromisoformat(str(record["utc_start"])):
            errors.append("reverse chronology")
    except (KeyError, ValueError):
        errors.append("invalid chronology")
    combined = ""
    hashes = record.get("evidence_file_hashes") if isinstance(record.get("evidence_file_hashes"), dict) else {}
    for stream in ("stdout", "stderr"):
        location = record.get(f"{stream}_location")
        path = (root / str(location)).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{stream} escapes package")
            continue
        if not path.is_file():
            errors.append(f"{stream} missing")
            continue
        content = path.read_text(encoding="utf-8")
        combined += content
        if sha(path) != hashes.get(stream):
            errors.append(f"{stream} hash mismatch")
        quoted_sensitive = any(match.group("value") != "<REDACTED>" for match in SENSITIVE_QUOTED_ASSIGNMENT.finditer(content))
        unquoted_sensitive = any(match.group("value").strip() != "<REDACTED>" for match in SENSITIVE_ASSIGNMENT.finditer(content))
        if quoted_sensitive or unquoted_sensitive or KNOWN_SECRET_VALUE.search(content):
            errors.append(f"{stream} contains unredacted sensitive data")
    required_meaning = record.get("required_meaning") if isinstance(record.get("required_meaning"), list) else []
    lines = set(combined.splitlines())
    if not required_meaning or any(str(marker) not in lines for marker in required_meaning):
        errors.append("required exact-line meaning absent after redaction")
    redaction = record.get("redaction_evidence") if isinstance(record.get("redaction_evidence"), dict) else {}
    exact_matches = {str(marker): str(marker) in lines for marker in required_meaning}
    projection = hashlib.sha256(combined.encode()).hexdigest()
    if (
        redaction.get("meaning_preserved") is not True
        or redaction.get("unredacted_sensitive_match_count") != 0
        or redaction.get("semantic_projection_sha256_before") != redaction.get("semantic_projection_sha256_after")
        or redaction.get("semantic_projection_sha256_after") != projection
        or redaction.get("required_exact_line_matches") != exact_matches
    ):
        errors.append("redaction projection or exact-line meaning enforcement failed")
    core = dict(record)
    recorded = core.pop("record_content_sha256", "")
    if hashlib.sha256(canonical(core)).hexdigest() != recorded:
        errors.append("record content hash mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--phase", choices=("assembly", "candidate", "final"), default="candidate")
    args = parser.parse_args()
    root = args.package.resolve()
    repo = locate_repository(Path(__file__))
    detached_package_mode = repo is None
    checks: list[dict[str, object]] = []

    def ck(identifier: str, passed: bool, detail: object) -> None:
        checks.append({"check_id": identifier, "status": "PASS" if passed else "FAIL", "detail": detail})

    jsonschema_version = importlib.metadata.version("jsonschema")
    context_valid = (repo is not None and (repo / ".git").exists()) or (detached_package_mode and (root / "SUCCESSOR_PACKAGE_INDEX.json").is_file())
    ck("MV-001-runtime-root-resolution", sys.version.split()[0] == "3.11.11" and jsonschema_version == "4.26.0" and context_valid, {
        "python": sys.version.split()[0], "jsonschema": jsonschema_version,
        "resolution_mode": "DETACHED_PACKAGE_SOURCE_PAYLOAD" if detached_package_mode else "REPOSITORY",
        "resolved_repository_root": repo.as_posix() if repo else None,
        "resolved_package_root": root.as_posix(), "invocation_working_directory": Path.cwd().resolve().as_posix(),
        "required_command": "stage2a/.venv/bin/python stage2a/validate_stage2a_package.py PACKAGE --phase PHASE",
    })
    files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    file_set = set(files)
    needed = REQUIRED | (FINAL_REQUIRED if args.phase == "final" else set())
    ck("MV-002-required-outputs", needed <= file_set, {"required": len(needed), "present": len(needed & file_set), "missing": sorted(needed - file_set)})
    ck("MV-003-path-safety", all(not p.is_absolute() and ".." not in p.parts for p in map(PurePosixPath, files)), {"files": len(files)})
    symlinks = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_symlink())
    folded: dict[str, list[str]] = {}
    for name in files:
        folded.setdefault(name.casefold(), []).append(name)
    collisions = [values for values in folded.values() if len(values) > 1]
    ck("MV-004-symlinks-case-collisions", not symlinks and not collisions, {"symlinks": symlinks, "case_collisions": collisions})

    json_errors: list[str] = []
    json_objects: dict[str, object] = {}
    for name in files:
        if name.endswith(".json"):
            try:
                json_objects[name] = json.loads((root / name).read_text(encoding="utf-8"))
            except Exception as exc:
                json_errors.append(f"{name}: {type(exc).__name__}")
    ck("MV-005-json-parse", not json_errors, {"parsed": len(json_objects), "errors": json_errors})

    csv_errors: list[str] = []
    csv_rows = 0
    for name in files:
        if name.endswith(".csv"):
            try:
                with (root / name).open(newline="", encoding="utf-8") as handle:
                    rows = list(csv.reader(handle))
                if not rows or any(len(row) != len(rows[0]) for row in rows):
                    raise ValueError("empty or structurally inconsistent CSV")
                csv_rows += len(rows) - 1
            except Exception as exc:
                csv_errors.append(f"{name}: {exc}")
    ck("MV-006-csv-structure", not csv_errors, {"data_rows": csv_rows, "errors": csv_errors})

    joined = "\n".join((root / name).read_text(encoding="utf-8", errors="replace") for name in files if name != "validate_stage2a_package.py" and (root / name).stat().st_size < 5_000_000)
    required_statuses = ("F0001_REMAINS_OPEN_BLOCKING", "EXECUTION_NOT_AUTHORIZED", "NOT_EXTERNALLY_ASSURED", "STAGE2A_EXECUTION_FOUNDATION_REMEDIATION_INCOMPLETE", "RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE")
    ck("MV-007-controlled-status", all(value in joined for value in required_statuses), {value: value in joined for value in required_statuses})
    prohibited = ("EXECUTION_READY", "EXECUTION_AUTHORIZED", "F0001_CLOSED", "CP3_READY_TO_EXECUTE", "PRODUCTION_READY", "EXTERNALLY_ASSURED")
    prohibited_hits = [value for value in prohibited if re.search(rf"(?<!NOT_)\b{re.escape(value)}\b", joined)]
    ck("MV-008-forbidden-status", not prohibited_hits, {"hits": prohibited_hits})

    absolute_hits = []
    for name in files:
        if name.startswith("source_payload/") or name in {"SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json", "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.md", "validate_stage2a_package.py"}:
            continue
        text = (root / name).read_text(encoding="utf-8", errors="ignore")
        if "/Users/" in text or "/private/tmp/" in text:
            absolute_hits.append(name)
    ck("MV-009-local-path-boundary", not absolute_hits, {"unexpected_absolute_path_files": absolute_hits, "controlled_exemptions": ["SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE", "immutable source_payload code and historical evidence"]})
    secret_patterns = ("sk" + "_live_", "sk" + "_test_", "wh" + "sec_", "AK" + "IA", "-----BEGIN " + "PRIVATE KEY-----")
    secret_hits = [pattern for pattern in secret_patterns if pattern in joined]
    ck("MV-010-secret-values", not secret_hits, {"pattern_hits": secret_hits, "names_only_allowed": True})

    source = json_objects.get("STAGE2A_SOURCE_EVIDENCE_REGISTER.json", {})
    source_errors: list[str] = []
    source_ids: set[str] = set()
    source_paths: set[str] = set()
    for row in source.get("sources", []) if isinstance(source, dict) else []:
        identifier, path = row.get("evidence_id"), row.get("path")
        if identifier in source_ids or path in source_paths:
            source_errors.append(f"duplicate source {identifier} {path}")
        source_ids.add(identifier); source_paths.add(path)
        candidate = (root / "source_payload" / path) if detached_package_mode else (repo / path)
        if not candidate.is_file() or sha(candidate) != row.get("sha256"):
            source_errors.append(f"source hash mismatch {path}")
        commit = row.get("git_commit")
        blob = row.get("git_blob") if detached_package_mode else git(repo, "rev-parse", f"{commit}:{path}", check=False)
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit) or not re.fullmatch(r"[0-9a-f]{40}", str(blob)) or blob != row.get("git_blob"):
            source_errors.append(f"source blob/commit mismatch {path}")
    payload_paths = sorted(path.relative_to(root / "source_payload").as_posix() for path in (root / "source_payload").rglob("*") if path.is_file()) if (root / "source_payload").is_dir() else []
    ck("MV-011-source-register", not source_errors and bool(source_ids) and set(payload_paths) == source_paths, {"rows": len(source_ids), "source_payload_rows": len(payload_paths), "mode": "DETACHED" if detached_package_mode else "REPOSITORY", "errors": source_errors})

    requirement_matrix = json_objects.get("STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.json", {})
    finding_matrix = json_objects.get("STAGE2A_FINDING_TO_REMEDIATION_MATRIX.json", {})
    trace = json_objects.get("STAGE2A_SOURCE_TO_OUTPUT_TRACEABILITY.json", {})
    test_register = json_objects.get("STAGE2A_TEST_CONTROL_REGISTER.json", {})
    trace_errors: list[str] = []
    test_rows = test_register.get("tests", []) if isinstance(test_register, dict) else []
    test_ids = {row.get("test_id") for row in test_rows}
    for row in test_rows:
        if not row.get("test_id") or not row.get("executable_identity") or not row.get("implementation_path") or row.get("implementation_path") not in source_paths:
            trace_errors.append(f"invalid executable test registration {row.get('test_id')}")
    requirements = requirement_matrix.get("requirements", []) if isinstance(requirement_matrix, dict) else []
    requirement_ids: set[str] = set()
    for row in requirements:
        identifier = row.get("requirement_id")
        if identifier in requirement_ids:
            trace_errors.append(f"duplicate requirement {identifier}")
        requirement_ids.add(identifier)
        for field in ("control_ids", "source_evidence_ids", "implementation_artifacts", "test_ids", "evidence_artifacts"):
            if not isinstance(row.get(field), list) or not row[field]:
                trace_errors.append(f"{identifier} missing specific {field}")
        if row.get("gap_id") not in {f"S2-GAP-{number:03d}" for number in range(1, 10)}:
            trace_errors.append(f"{identifier} invalid gap")
    findings = finding_matrix.get("findings", []) if isinstance(finding_matrix, dict) else []
    finding_ids: set[str] = set()
    for row in findings:
        identifier = row.get("finding_id")
        if identifier in finding_ids:
            trace_errors.append(f"duplicate finding {identifier}")
        finding_ids.add(identifier)
        for field in ("blocker_classification", "requirement_ids", "remediation_artifacts", "test_ids", "evidence_artifacts"):
            value = row.get(field)
            if not value or (field != "blocker_classification" and not isinstance(value, list)):
                trace_errors.append(f"{identifier} missing specific {field}")
        if any(test_id not in test_ids for test_id in row.get("test_ids", [])):
            trace_errors.append(f"{identifier} references unregistered executable test")
        if any(not ((root / path).is_file() or path in source_paths) for path in row.get("remediation_artifacts", [])):
            trace_errors.append(f"{identifier} references missing remediation artifact")
        if any(not (root / path).is_file() for path in row.get("evidence_artifacts", [])):
            trace_errors.append(f"{identifier} references missing evidence artifact")
    output_rows = trace.get("outputs", []) if isinstance(trace, dict) else []
    mapping_ids: set[str] = set()
    mapped_outputs: set[str] = set()
    for row in output_rows:
        mapping_id = row.get("mapping_id")
        output = row.get("output")
        if mapping_id in mapping_ids or output in mapped_outputs:
            trace_errors.append(f"duplicate trace mapping {mapping_id} {output}")
        mapping_ids.add(mapping_id); mapped_outputs.add(output)
        ids = row.get("requirement_ids", [])
        if not ids or len(ids) >= 9 or any(identifier not in requirement_ids for identifier in ids):
            trace_errors.append(f"{row.get('output')} has generic or invalid requirement mapping")
        if not row.get("source_evidence_ids") or not row.get("test_ids") or not row.get("evidence_artifacts") or not row.get("artifact_role") or not row.get("verification_rule"):
            trace_errors.append(f"{row.get('output')} lacks specific source/test/evidence mapping")
        if any(identifier not in source_ids for identifier in row.get("source_evidence_ids", [])):
            trace_errors.append(f"{output} references unknown source evidence")
        if any(identifier not in test_ids for identifier in row.get("test_ids", [])):
            trace_errors.append(f"{output} references unregistered executable test")
        if any(path not in source_paths for path in row.get("implementation_artifacts", [])):
            trace_errors.append(f"{output} references implementation outside source register")
        if any(not (root / path).is_file() for path in row.get("evidence_artifacts", [])):
            trace_errors.append(f"{output} references missing evidence artifact")
    top_level_files = {name for name in files if "/" not in name}
    assembly_future = {"DRAFT_REVIEW_SHA256SUMS.txt", "DRAFT_REVIEW_SNAPSHOT_RECORD.json", "DRAFT_REVIEW_SNAPSHOT_RECORD.md"} if args.phase == "assembly" else set()
    expected_trace_outputs = top_level_files | assembly_future
    if mapped_outputs != expected_trace_outputs:
        trace_errors.append(f"top-level trace coverage mismatch missing={sorted(expected_trace_outputs-mapped_outputs)} extra={sorted(mapped_outputs-expected_trace_outputs)}")
    ck("MV-011A-specific-traceability", len(requirements) == 9 and len(findings) >= 5 and bool(output_rows) and len(test_rows) >= 10 and not trace_errors, {
        "requirements": len(requirements), "findings": len(findings), "outputs": len(output_rows), "executable_tests": len(test_rows), "errors": trace_errors,
    })

    if detached_package_mode:
        baseline_record = json_objects.get("IMMUTABLE_BASELINE_RECORD.json", {})
        anchors_ok = isinstance(baseline_record, dict) and baseline_record.get("immutable_baseline") == BASELINE and baseline_record.get("modified") is False
        anchor_detail = {"mode": "DETACHED_PACKAGE_RECORDED_ANCHORS", "start": START, "baseline": BASELINE, "cryptographic_git_object_reverification": "REQUIRES_REPOSITORY_MODE"}
    else:
        baseline_result = subprocess.run(["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"], cwd=repo, capture_output=True)
        anchors_ok = git(repo, "branch", "--show-current") == BRANCH and baseline_result.returncode == 0
        anchor_detail = {"mode": "REPOSITORY", "branch": git(repo, "branch", "--show-current"), "head": git(repo, "rev-parse", "HEAD"), "start": START, "baseline": BASELINE}
    ck("MV-012-git-anchors", anchors_ok, anchor_detail)
    pred = json_objects.get("PREDECESSOR_REFERENCE_RECORD.json", {})
    ck("MV-013-predecessor", isinstance(pred, dict) and pred.get("archive_sha256") == PREDECESSOR_SHA and pred.get("unchanged") is True, pred)

    foundation = json_objects.get("STAGE2A_FOUNDATION_VALIDATION.json", {})
    ck("MV-014-foundation-validation", isinstance(foundation, dict) and foundation.get("validation") == "PASS" and foundation.get("pass_count") == foundation.get("check_count") and foundation.get("provider_attempt_count") == foundation.get("production_access_count") == foundation.get("live_data_access_count") == 0, {
        "validation": foundation.get("validation") if isinstance(foundation, dict) else None,
        "score": f"{foundation.get('pass_count')}/{foundation.get('check_count')}" if isinstance(foundation, dict) else None,
    })
    bootstrap = json_objects.get("BACKEND_BOOTSTRAP_VALIDATION.json", {})
    inventory = bootstrap.get("inventory", []) if isinstance(bootstrap, dict) else []
    hashes_valid = bool(inventory) and all(SHA_RE.fullmatch(str(x.get("download_artifact_sha256", ""))) and SHA_RE.fullmatch(str(x.get("metadata_sha256", ""))) for x in inventory)
    ck("MV-015-bootstrap-artifact-integrity", isinstance(bootstrap, dict) and bootstrap.get("validation") == "PASS" and hashes_valid, {"inventory_rows": len(inventory), "hashes_valid": hashes_valid})

    schema = json_objects.get("EXECUTION_EVIDENCE_SCHEMA.json")
    evidence_errors: list[str] = []
    if isinstance(schema, dict):
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for name in ("FOUNDATION_EVIDENCE_EXAMPLE_PASS.json", "FOUNDATION_EVIDENCE_EXAMPLE_INTENTIONAL_FAIL.json"):
            record = json_objects.get(name)
            if not isinstance(record, dict):
                evidence_errors.append(f"missing {name}")
                continue
            evidence_errors.extend(f"{name}: {x.message}" for x in validator.iter_errors(record))
            evidence_errors.extend(f"{name}: {message}" for message in semantic_record_errors(root, record))
    else:
        evidence_errors.append("missing schema")
    ck("MV-016-evidence-semantics", not evidence_errors, {"errors": evidence_errors})

    foundation_checks = {row.get("check"): row for row in foundation.get("checks", [])} if isinstance(foundation, dict) else {}
    provider_detail = foundation_checks.get("provider_denial", {}).get("detail", {})
    provider_rows = provider_detail.get("register", []) if isinstance(provider_detail, dict) else []
    provider_ok = bool(provider_rows) and all(
        row.get("state") == "SKIPPED_NOT_CONFIGURED"
        and row.get("attempted_count") == row.get("succeeded_count") == row.get("failed_count") == row.get("timed_out_count") == row.get("unavailable_count") == 0
        and row.get("skipped_count") == 1
        and row.get("global_unapproved_attempt_count") == 0
        and row.get("outcome_event", {}).get("provider_path_evaluated") is True
        for row in provider_rows
    )
    startup_detail = foundation_checks.get("startup_side_effect_inventory", {}).get("detail", {})
    outcomes = startup_detail.get("attempt_outcomes", {}) if isinstance(startup_detail, dict) else {}
    startup_ok = (
        set(outcomes) >= {"attempted", "succeeded", "failed", "skipped", "timed_out", "unavailable"}
        and outcomes.get("attempted") == outcomes.get("succeeded") + outcomes.get("failed") + outcomes.get("timed_out") + outcomes.get("unavailable")
        and startup_detail.get("oracle_match") is True
        and startup_detail.get("network_guard", {}).get("provider_or_external_attempt_count") == 0
        and len(outcomes.get("events", [])) >= 4
        and all(event.get("state") and event.get("utc_start") and event.get("utc_end") for event in outcomes.get("events", []))
    )
    ck("MV-016A-provider-startup-measurement", provider_ok and startup_ok, {
        "provider_rows": len(provider_rows), "provider_states_valid": provider_ok,
        "startup_attempt_outcomes": outcomes, "startup_measurement_valid": startup_ok,
    })

    process_detail = foundation_checks.get("process_identity", {}).get("detail", {})
    shutdown_detail = foundation_checks.get("controlled_shutdown", {}).get("detail", {})
    required_identity = {"pid", "process_group_id", "parent_pid", "parent_pid_policy", "executable_path", "working_directory", "controlled_port", "command_line_sha256", "observed_command_line", "command_display", "launch_nonce_sha256", "identity_recorded_utc"}
    identity_rows = [process_detail.get("mongo_identity"), process_detail.get("api_identity")]
    identity_ok = all(isinstance(row, dict) and required_identity <= set(row) and row.get("pid") == row.get("process_group_id") and SHA_RE.fullmatch(str(row.get("launch_nonce_sha256", ""))) for row in identity_rows) and process_detail.get("mongo_listener_identity_verified") is True and process_detail.get("api_listener_identity_verified") is True and process_detail.get("mongo_foreign_listener_pid") is None and process_detail.get("api_foreign_listener_pid") is None
    termination_rows = shutdown_detail.get("processes", []) if isinstance(shutdown_detail, dict) else []
    termination_ok = len(termination_rows) == 2 and all(row.get("command_identity_verified") is True and row.get("pid") == row.get("process_group_id") for row in termination_rows)
    ck("MV-016B-process-identity", identity_ok and termination_ok, {
        "identity_fields": sorted(required_identity), "startup_identity_valid": identity_ok,
        "termination_identity_valid": termination_ok, "foreign_process_policy": "FAIL_CLOSED",
    })

    provenance = json_objects.get("CORRECTED_CANDIDATE_PROVENANCE.json", {})
    reuse = json_objects.get("EVIDENCE_REUSE_AND_RERUN_REGISTER.json", {})
    blocker_results = provenance.get("blocker_results", []) if isinstance(provenance, dict) else []
    provenance_ok = (
        provenance.get("candidate_id") == CANDIDATE_ID
        and provenance.get("failed_candidate_unchanged") is True
        and len(blocker_results) == 5
        and all(row.get("status") == "REMEDIATED_PENDING_REREVIEW" for row in blocker_results)
        and isinstance(reuse, dict) and bool(reuse.get("reused_predecessor_evidence")) and bool(reuse.get("invalidated_checks")) and bool(reuse.get("rerun_checks"))
    )
    ck("MV-016C-candidate-provenance-reuse", provenance_ok, {
        "candidate_id": provenance.get("candidate_id") if isinstance(provenance, dict) else None,
        "blocker_results": len(blocker_results), "reuse_register_present": isinstance(reuse, dict),
    })

    residue = json_objects.get("SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json", {})
    residue_ok = isinstance(residue, dict) and residue.get("event_classification") == "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE" and residue.get("termination", {}).get("scope") == "ONLY_VERIFIED_PROCESS_GROUP_62766" and residue.get("causal_relationship_to_runtime_limitation") == "NOT_ESTABLISHED_DO_NOT_CONFLATE"
    ck("MV-017-residue-provenance", residue_ok, residue)
    selector = json_objects.get("RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.json", {})
    ck("MV-018-runtime-selector-limitation", isinstance(selector, dict) and selector.get("status") == "OPEN_BLOCKING_RUNTIME_LIMITATION" and selector.get("direct_evidence_of_resolution") is False, selector)

    manifest_name = "SUCCESSOR_PACKAGE_SHA256SUMS.txt" if args.phase == "final" else "DRAFT_REVIEW_SHA256SUMS.txt"
    manifest_errors: list[str] = []
    manifest_rows = 0
    if args.phase == "assembly":
        ck("MV-019-checksum-reconciliation", True, {"manifest": "DEFERRED_UNTIL_ASSEMBLY_VALIDATION_MATRIX_IS_RECORDED", "rows": 0, "errors": []})
    elif (root / manifest_name).is_file():
        for line in (root / manifest_name).read_text(encoding="utf-8").splitlines():
            expected, name = line.split("  ", 1); manifest_rows += 1
            if not SHA_RE.fullmatch(expected) or name not in file_set or sha(root / name) != expected:
                manifest_errors.append(name)
        listed = {line.split("  ", 1)[1] for line in (root / manifest_name).read_text().splitlines() if "  " in line}
        allowed_unlisted = {manifest_name, "DRAFT_REVIEW_SNAPSHOT_RECORD.json", "DRAFT_REVIEW_SNAPSHOT_RECORD.md"} if args.phase == "candidate" else {manifest_name}
        extra = sorted(file_set - listed - allowed_unlisted)
        if extra:
            manifest_errors.append("unlisted:" + ",".join(extra))
    else:
        manifest_errors.append("missing manifest")
    ck("MV-019-checksum-reconciliation", not manifest_errors, {"manifest": manifest_name, "rows": manifest_rows, "errors": manifest_errors})

    if args.phase == "final":
        exact = json_objects.get("EXACT_FILE_INVENTORY.json", {})
        exact_paths = exact.get("paths", []) if isinstance(exact, dict) else []
        ck("MV-020-exact-inventory", exact_paths == files, {"listed": len(exact_paths), "physical": len(files)})
        package_manifest = json_objects.get("SUCCESSOR_PACKAGE_MANIFEST.json", {})
        entries = package_manifest.get("entries", []) if isinstance(package_manifest, dict) else []
        paths = [x.get("path") for x in entries]
        ck("MV-021-deterministic-manifest", paths == sorted(paths) and len(paths) == len(set(paths)), {"entries": len(paths)})

    failed = [row for row in checks if row["status"] == "FAIL"]
    result = {
        "package_id": PACKAGE_ID, "phase": args.phase,
        "validation": "PASS" if not failed else "FAIL",
        "pass_count": len(checks) - len(failed), "check_count": len(checks),
        "checks": checks, "execution": "EXECUTION_NOT_AUTHORIZED",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
