#!/usr/bin/env python3
"""Read-only machine validation for the Stage 2A successor package."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.util
import importlib.metadata
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker

PACKAGE_ID = "ES-PKG-2026-004-V003"
CANDIDATE_ID = "ES-PKG-2026-004-V003-CANDIDATE-007"
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
SENSITIVE_KEY = r"(?:authorization|access_token|client_secret|password|api_key|api-key|token|secret|credential|bearer)"
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


def load_source_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    prior_dont_write_bytecode = sys.dont_write_bytecode
    try:
        # Detached package validation is read-only. Dynamic imports must not add
        # __pycache__ files to the package they are validating.
        sys.dont_write_bytecode = True
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = prior_dont_write_bytecode
    return module


def record_check(checks: list[dict[str, object]], seen: set[str], identifier: str, passed: bool, detail: object) -> None:
    if identifier in seen:
        raise RuntimeError(f"duplicate validation check identifier: {identifier}")
    seen.add(identifier)
    checks.append({"check_id": identifier, "status": "PASS" if passed else "FAIL", "detail": detail})


def provider_evidence_errors(
    ledger: dict[str, object], registry: dict[str, object], registry_sha256: str,
    provider_rows: list[dict[str, object]], proof: dict[str, object],
    source_paths: set[str], source_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    expected = {row["provider_id"]: row for row in registry.get("providers", []) if isinstance(row, dict) and row.get("provider_id")}
    events = ledger.get("provider_events", []) if isinstance(ledger.get("provider_events"), list) else []
    attempts = ledger.get("attempts", []) if isinstance(ledger.get("attempts"), list) else []
    if ledger.get("schema_version") != "2.0" or ledger.get("guard") != "STAGE2A_APPLICATION_NETWORK_GUARD" or ledger.get("installed") is not True:
        errors.append("provider guard identity invalid")
    if ledger.get("provider_registry_sha256") != registry_sha256:
        errors.append("provider registry hash mismatch")
    if ledger.get("approved_endpoints") != ["LOOPBACK_API_8019", "LOOPBACK_MONGODB_27029"]:
        errors.append("approved endpoint boundary mismatch")
    if attempts or ledger.get("provider_or_external_attempt_count") != 0 or ledger.get("unapproved_attempt_count") != 0:
        errors.append("provider or external attempts must remain zero")
    ordered = sorted(events + attempts, key=lambda event: int(event.get("sequence", -1)) if isinstance(event, dict) else -1)
    previous = "0" * 64
    for sequence, event in enumerate(ordered, 1):
        if not isinstance(event, dict):
            errors.append(f"invalid provider event at sequence {sequence}")
            continue
        core = dict(event)
        recorded_hash = core.pop("event_sha256", "")
        if event.get("sequence") != sequence or event.get("previous_event_sha256") != previous:
            errors.append(f"provider event sequence or predecessor mismatch at {sequence}")
        if hashlib.sha256(canonical(core)).hexdigest() != recorded_hash:
            errors.append(f"provider event hash mismatch at {sequence}")
        previous = str(recorded_hash)
    if ledger.get("event_count") != len(ordered) or ledger.get("event_chain_sha256") != previous:
        errors.append("provider event count or chain head mismatch")
    actual: dict[str, dict[str, object]] = {}
    for event in events:
        if not isinstance(event, dict):
            continue
        provider_id = str(event.get("provider_id"))
        if provider_id in actual:
            errors.append(f"duplicate provider event {provider_id}")
        actual[provider_id] = event
    if set(actual) != set(expected):
        errors.append("provider event coverage mismatch")
    rows_by_id: dict[str, dict[str, object]] = {}
    for row in provider_rows:
        provider_id = str(row.get("provider_id"))
        if provider_id in rows_by_id:
            errors.append(f"duplicate provider outcome row {provider_id}")
        rows_by_id[provider_id] = row
    if set(rows_by_id) != set(expected):
        errors.append("provider outcome coverage mismatch")
    event_keys = {
        "schema_version", "guard_session_id", "sequence", "utc", "api_pid",
        "api_process_group_id", "launch_nonce_sha256", "event_type", "provider_id",
        "provider", "boundary_id", "source_path", "source_symbol", "source_evidence_id",
        "required_configuration_names", "present_configuration_names",
        "missing_configuration_names", "configuration_state", "integration_state",
        "boundary_state", "attempt_state", "reason_code", "attempted", "succeeded",
        "failed", "skipped", "timed_out", "unavailable", "values_recorded",
        "previous_event_sha256", "event_sha256",
    }
    for provider_id, spec in expected.items():
        event = actual.get(provider_id, {})
        row = rows_by_id.get(provider_id, {})
        state = spec.get("unconfigured_state")
        source_id = "S2A-SRC-" + hashlib.sha256(str(spec.get("source_path")).encode()).hexdigest()[:12].upper()
        expected_event_type = "PREREQUISITE_EVALUATED" if spec.get("integration_state") == "PRESENT" else "INTEGRATION_ABSENCE_ATTESTED"
        expected_boundary = "NOT_EXERCISED_NO_TRIGGER" if spec.get("integration_state") == "PRESENT" else "NO_RUNTIME_BOUNDARY"
        counts = {
            "attempted": 0, "succeeded": 0, "failed": 0, "timed_out": 0,
            "skipped": 1 if str(state).startswith("SKIPPED_") else 0,
            "unavailable": 1 if str(state).startswith("UNAVAILABLE_") else 0,
        }
        if set(event) != event_keys:
            errors.append(f"{provider_id} provider event schema mismatch")
        for event_key, ledger_key in (("guard_session_id", "guard_session_id"), ("api_pid", "api_pid"), ("api_process_group_id", "api_process_group_id"), ("launch_nonce_sha256", "launch_nonce_sha256")):
            if event.get(event_key) != ledger.get(ledger_key):
                errors.append(f"{provider_id} provider event process binding mismatch")
        try:
            stamp = dt.datetime.fromisoformat(str(event.get("utc")))
            if stamp.tzinfo is None or stamp.utcoffset() != dt.timedelta(0):
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{provider_id} provider event timestamp invalid")
        expected_fields = {
            "provider": spec.get("provider"), "boundary_id": spec.get("boundary_id"),
            "source_path": spec.get("source_path"), "source_symbol": spec.get("source_symbol"),
            "source_evidence_id": source_id, "required_configuration_names": spec.get("required_configuration_names"),
            "present_configuration_names": [], "missing_configuration_names": sorted(spec.get("required_configuration_names", [])),
            "configuration_state": "NOT_CONFIGURED", "integration_state": spec.get("integration_state"),
            "boundary_state": expected_boundary, "attempt_state": state, "reason_code": spec.get("reason_code"),
            "event_type": expected_event_type, "values_recorded": False,
        } | counts
        if any(event.get(field) != value for field, value in expected_fields.items()):
            errors.append(f"{provider_id} provider event semantics mismatch")
        if spec.get("source_path") not in source_paths or source_id not in source_ids:
            errors.append(f"{provider_id} provider source traceability mismatch")
        expected_row = {
            "provider": spec.get("provider"), "boundary_id": spec.get("boundary_id"),
            "source_path": spec.get("source_path"), "source_symbol": spec.get("source_symbol"),
            "source_evidence_id": source_id, "configuration_names": spec.get("required_configuration_names"),
            "configured": False, "integration_state": spec.get("integration_state"), "state": state,
            "attempt_count": 0, "attempted_count": 0, "succeeded_count": 0,
            "failed_count": 0, "skipped_count": counts["skipped"], "timed_out_count": 0,
            "unavailable_count": counts["unavailable"], "event_sequence": event.get("sequence"),
            "event_sha256": event.get("event_sha256"), "guard_session_id": ledger.get("guard_session_id"),
            "measurement_basis": "PROCESS_BOUND_HASH_CHAINED_RUNTIME_CAPABILITY_EVENT",
            "global_unapproved_attempt_count": 0,
        }
        if any(row.get(field) != value for field, value in expected_row.items()):
            errors.append(f"{provider_id} provider outcome derivation mismatch")
    expected_proof = {
        "guard_session_id": ledger.get("guard_session_id"), "api_pid": ledger.get("api_pid"),
        "api_process_group_id": ledger.get("api_process_group_id"),
        "launch_nonce_sha256": ledger.get("launch_nonce_sha256"),
        "provider_registry_sha256": registry_sha256, "provider_event_count": len(events),
        "network_attempt_event_count": 0, "unattributed_attempt_count": 0,
        "event_chain_sha256": ledger.get("event_chain_sha256"), "event_chain_valid": True,
        "process_identity_bound": True,
    }
    if any(proof.get(field) != value for field, value in expected_proof.items()):
        errors.append("provider guard proof mismatch")
    return errors


def process_evidence_errors(foundation: dict[str, object], process_detail: dict[str, object], shutdown_detail: dict[str, object]) -> list[str]:
    errors: list[str] = []
    identities = (("mongo", 27029), ("api", 8019))
    expected_commands = {
        "mongo": "mongod --dbpath REPOSITORY_ROOT/stage2a/.runtime/mongo --port 27029 --bind_ip 127.0.0.1 --nounixsocket --quiet",
        "api": "REPOSITORY_ROOT/stage2a/.venv/bin/python -m uvicorn full_application_profile:app --app-dir REPOSITORY_ROOT/stage2a --host 127.0.0.1 --port 8019 --log-level warning --no-access-log",
    }
    try:
        started = dt.datetime.fromisoformat(str(foundation.get("started_utc")))
        ended = dt.datetime.fromisoformat(str(foundation.get("ended_utc")))
    except (TypeError, ValueError):
        started = ended = None
        errors.append("foundation chronology invalid for process evidence")
    for kind, port in identities:
        row = process_detail.get(f"{kind}_identity") if isinstance(process_detail, dict) else None
        if not isinstance(row, dict):
            errors.append(f"missing {kind} process identity")
            continue
        command = expected_commands[kind]
        packaged_hash = hashlib.sha256(command.encode()).hexdigest()
        required = {
            "kind": kind, "owner": PACKAGE_ID, "controlled_port": port,
            "working_directory": "REPOSITORY_ROOT/stage2a", "runtime": "REPOSITORY_ROOT/stage2a/.runtime",
            "observed_command_line": command, "command_display": command,
            "packaged_command_line_sha256": packaged_hash,
            "command_line_hash_basis": "FULL_OBSERVED_COMMAND_BEFORE_LOCAL_PATH_PREFIX_REDACTION",
            "parent_pid_policy": "CREATION_PARENT_OR_INIT_REPARENT_ONLY",
        }
        if any(row.get(field) != value for field, value in required.items()):
            errors.append(f"{kind} packaged process identity semantics mismatch")
        if row.get("pid") != row.get("process_group_id") or not isinstance(row.get("pid"), int) or not isinstance(row.get("parent_pid"), int):
            errors.append(f"{kind} PID or process-group identity invalid")
        if process_detail.get(f"{kind}_pid") != row.get("pid") or process_detail.get(f"{kind}_listener_identity_verified") is not True or process_detail.get(f"{kind}_foreign_listener_pid") is not None or process_detail.get(f"{kind}_port_open") is not True:
            errors.append(f"{kind} listener attribution mismatch")
        if not SHA_RE.fullmatch(str(row.get("command_line_sha256", ""))) or row.get("command_line_sha256") == "0" * 64 or not SHA_RE.fullmatch(str(row.get("launch_nonce_sha256", ""))):
            errors.append(f"{kind} command or nonce hash invalid")
        executable = str(row.get("executable_path", ""))
        if (kind == "mongo" and not executable.endswith("/mongod")) or (kind == "api" and executable != "PYTHON_RUNTIME/bin/python3.11"):
            errors.append(f"{kind} executable identity invalid")
        try:
            stamp = dt.datetime.fromisoformat(str(row.get("identity_recorded_utc")))
            if stamp.tzinfo is None or stamp.utcoffset() != dt.timedelta(0) or (started and ended and not started <= stamp <= ended):
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{kind} identity timestamp invalid")
        if row.get("path_redaction") != {"policy": "LOCAL_PATH_PREFIX_TO_STABLE_ALIAS", "meaning_preserved": True, "stable_aliases": ["REPOSITORY_ROOT", "PYTHON_RUNTIME", "LOCAL_USER_HOME"]}:
            errors.append(f"{kind} path-redaction semantics mismatch")
    processes = shutdown_detail.get("processes", []) if isinstance(shutdown_detail, dict) else []
    if shutdown_detail.get("status") != "STOPPED" or shutdown_detail.get("api_alive") is not False or shutdown_detail.get("mongo_alive") is not False or shutdown_detail.get("pid_files_absent") is not True or shutdown_detail.get("ports_closed") is not True:
        errors.append("controlled shutdown summary mismatch")
    if len(processes) != 2 or {row.get("kind") for row in processes if isinstance(row, dict)} != {"api", "mongo"}:
        errors.append("controlled shutdown process coverage mismatch")
    for row in processes:
        if not isinstance(row, dict) or row.get("pid") != row.get("process_group_id") or row.get("command_identity_verified") is not True or row.get("controlled_port_attribution") != "LISTENER_PID_MATCHED" or row.get("forced") is not False or row.get("port_closed") is not True or row.get("status") != "STOPPED":
            errors.append(f"invalid controlled shutdown process row {row.get('kind') if isinstance(row, dict) else 'UNKNOWN'}")
    return errors


def semantic_record_errors(root: Path, record: dict[str, object], projector=None) -> list[str]:
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
    streams: dict[str, str] = {}
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
        streams[stream] = content
        if sha(path) != hashes.get(stream):
            errors.append(f"{stream} hash mismatch")
        quoted_sensitive = any(match.group("value") != "<REDACTED>" for match in SENSITIVE_QUOTED_ASSIGNMENT.finditer(content))
        unquoted_sensitive = any(
            match.group("value").strip() != "<REDACTED>"
            and not ("authorization" in match.group("prefix").lower() and match.group("value").strip() == "Bearer <REDACTED>")
            for match in SENSITIVE_ASSIGNMENT.finditer(content)
        )
        if quoted_sensitive or unquoted_sensitive or KNOWN_SECRET_VALUE.search(content):
            errors.append(f"{stream} contains unredacted sensitive data")
    combined = streams.get("stdout", "") + streams.get("stderr", "")
    required_meaning = record.get("required_meaning") if isinstance(record.get("required_meaning"), list) else []
    lines = set(combined.splitlines())
    if not required_meaning or any(str(marker) not in lines for marker in required_meaning):
        errors.append("required exact-line meaning absent after redaction")
    redaction = record.get("redaction_evidence") if isinstance(record.get("redaction_evidence"), dict) else {}
    exact_matches = {str(marker): str(marker) in lines for marker in required_meaning}
    after_projection = projector(streams.get("stdout", ""), streams.get("stderr", ""), sanitized=True) if projector else None
    if (
        redaction.get("meaning_preserved") is not True
        or redaction.get("unredacted_sensitive_match_count") != 0
        or redaction.get("semantic_projection_sha256_before") != redaction.get("semantic_projection_sha256_after")
        or after_projection is None
        or redaction.get("semantic_projection_sha256_after") != after_projection.sha256
        or redaction.get("sensitive_slot_count_before") != after_projection.sensitive_slot_count
        or redaction.get("placeholder_slot_count_after") != after_projection.placeholder_slot_count
        or redaction.get("sensitive_class_counts_before") != after_projection.sensitive_class_counts
        or redaction.get("unexpected_redaction_placeholder_count") != after_projection.unexpected_placeholder_count
        or redaction.get("over_redaction_detected") is not False
        or redaction.get("required_exact_line_matches") != exact_matches
    ):
        errors.append("redaction projection or exact-line meaning enforcement failed")
    core = dict(record)
    recorded = core.pop("record_content_sha256", "")
    if hashlib.sha256(canonical(core)).hexdigest() != recorded:
        errors.append("record content hash mismatch")
    return errors


def traceability_errors(
    root: Path,
    source_register: dict[str, object],
    test_register: dict[str, object],
    requirement_matrix: dict[str, object],
    finding_matrix: dict[str, object],
    trace: dict[str, object],
    contract,
) -> list[str]:
    """Require exact canonical relationships, not merely existing identifiers."""
    errors: list[str] = []
    sources = source_register.get("sources", []) if isinstance(source_register, dict) else []
    source_by_path = {str(row.get("path")): str(row.get("evidence_id")) for row in sources}
    if len(source_by_path) != len(sources):
        errors.append("source register path duplication prevents canonical derivation")
    try:
        expected_tests = contract.test_rows(source_by_path)
        expected_requirements = contract.requirement_rows(contract.GAP_TITLES, source_by_path)
        expected_findings = contract.finding_rows()
        top_level = {path.name for path in root.iterdir() if path.is_file()}
        top_level |= {name for name in ("DRAFT_REVIEW_SHA256SUMS.txt", "DRAFT_REVIEW_SNAPSHOT_RECORD.json", "DRAFT_REVIEW_SNAPSHOT_RECORD.md") if name not in top_level}
        expected_outputs = contract.output_rows(sorted(top_level), expected_requirements, source_by_path)
    except (KeyError, RuntimeError) as exc:
        return [f"canonical relationship derivation failed: {exc}"]
    actual_tests = test_register.get("tests", []) if isinstance(test_register, dict) else []
    actual_requirements = requirement_matrix.get("requirements", []) if isinstance(requirement_matrix, dict) else []
    actual_findings = finding_matrix.get("findings", []) if isinstance(finding_matrix, dict) else []
    actual_outputs = trace.get("outputs", []) if isinstance(trace, dict) else []
    for label, actual, expected in (
        ("test register", actual_tests, expected_tests),
        ("requirement matrix", actual_requirements, expected_requirements),
        ("finding matrix", actual_findings, expected_findings),
        ("output trace", actual_outputs, expected_outputs),
    ):
        if actual != expected:
            errors.append(f"{label} differs from exact source-controlled contract")
    foundation = json.loads((root / "STAGE2A_FOUNDATION_VALIDATION.json").read_text(encoding="utf-8")) if (root / "STAGE2A_FOUNDATION_VALIDATION.json").is_file() else {}
    foundation_checks = {str(row.get("check")) for row in foundation.get("checks", [])} if isinstance(foundation, dict) else set()
    command_register = json.loads((root / "STAGE2A_VALIDATION_COMMAND_REGISTER.json").read_text(encoding="utf-8")) if (root / "STAGE2A_VALIDATION_COMMAND_REGISTER.json").is_file() else {}
    command_ids = {str(row.get("command_id")) for row in command_register.get("commands", [])} if isinstance(command_register, dict) else set()
    package_checks = {
        "MV-001-runtime-root-resolution", "MV-011A-specific-traceability",
    }
    for row in expected_tests:
        identity = str(row["executable_identity"])
        implementation = root / "source_payload" / str(row["implementation_path"])
        if not implementation.is_file():
            errors.append(f"registered executable source missing: {row['test_id']}")
        if identity.startswith("FOUNDATION_VALIDATION.check:"):
            check_name = identity.split(":", 1)[1].split(".", 1)[0]
            if check_name not in foundation_checks:
                errors.append(f"foundation executable identity unresolved: {row['test_id']}")
        elif identity.startswith("STAGE2A_VALIDATION_COMMAND_REGISTER:"):
            if identity.split(":", 1)[1] not in command_ids:
                errors.append(f"command executable identity unresolved: {row['test_id']}")
        elif identity.startswith("PACKAGE_VALIDATOR.check:"):
            if identity.split(":", 1)[1] not in package_checks:
                errors.append(f"package-validator identity unresolved: {row['test_id']}")
        elif identity.startswith("unittest:"):
            method = identity.rsplit(".", 1)[-1]
            if implementation.is_file() and f"def {method}(" not in implementation.read_text(encoding="utf-8"):
                errors.append(f"unittest executable identity unresolved: {row['test_id']}")
    return errors


def csv_parity_errors(root: Path, tests: list[dict[str, object]], requirements: list[dict[str, object]], findings: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    def rows(name: str) -> list[dict[str, str]]:
        with (root / name).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))
    expected_tests = [{key: str(value) for key, value in row.items()} for row in tests]
    expected_requirements = [{
        "requirement_id": str(row["requirement_id"]), "gap_id": str(row["gap_id"]),
        "control_ids": "|".join(row["control_ids"]), "source_evidence_ids": "|".join(row["source_evidence_ids"]),
        "implementation_artifacts": "|".join(row["implementation_artifacts"]), "test_ids": "|".join(row["test_ids"]),
        "evidence_artifacts": "|".join(row["evidence_artifacts"]), "status": str(row["status"]),
    } for row in requirements]
    expected_findings = [{
        "finding_id": str(row["finding_id"]), "blocker_classification": str(row["blocker_classification"]),
        "requirement_ids": "|".join(row["requirement_ids"]), "remediation_artifacts": "|".join(row["remediation_artifacts"]),
        "test_ids": "|".join(row["test_ids"]), "evidence_artifacts": "|".join(row["evidence_artifacts"]),
        "status": str(row["status"]), "self_closed": str(row["self_closed"]),
    } for row in findings]
    for name, expected in (
        ("STAGE2A_TEST_CONTROL_REGISTER.csv", expected_tests),
        ("STAGE2A_REQUIREMENT_TRACEABILITY_MATRIX.csv", expected_requirements),
        ("STAGE2A_FINDING_TO_REMEDIATION_MATRIX.csv", expected_findings),
    ):
        try:
            if rows(name) != expected:
                errors.append(f"JSON/CSV parity mismatch: {name}")
        except (FileNotFoundError, csv.Error) as exc:
            errors.append(f"CSV parity unavailable: {name}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--phase", choices=("assembly", "candidate", "final"), default="candidate")
    args = parser.parse_args()
    root = args.package.resolve()
    repo = locate_repository(Path(__file__))
    detached_package_mode = repo is None
    source_root = (root / "source_payload/stage2a") if detached_package_mode else (repo / "stage2a")
    contract = load_source_module(source_root / "traceability_contract.py", "stage2a_packaged_traceability_contract")
    semantic = load_source_module(source_root / "semantic_projection.py", "stage2a_packaged_semantic_projection")
    checks: list[dict[str, object]] = []
    seen_check_ids: set[str] = set()

    def ck(identifier: str, passed: bool, detail: object) -> None:
        record_check(checks, seen_check_ids, identifier, passed, detail)

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

    active_files = [
        name for name in files
        if not name.startswith("source_payload/")
        and name != "validate_stage2a_package.py"
        and (root / name).stat().st_size < 5_000_000
    ]
    joined = "\n".join((root / name).read_text(encoding="utf-8", errors="replace") for name in active_files)
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
    secret_hits: list[str] = []
    for name in files:
        text = (root / name).read_text(encoding="utf-8", errors="replace")
        if KNOWN_SECRET_VALUE.search(text):
            secret_hits.append(name)
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", text):
            secret_hits.append(name)
    ck("MV-010-secret-values", not secret_hits, {"files_with_plausible_secret_values": sorted(set(secret_hits)), "names_only_allowed": True})

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
    trace_errors: list[str] = traceability_errors(
        root, source, test_register, requirement_matrix, finding_matrix, trace, contract
    )
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
    trace_errors.extend(csv_parity_errors(root, test_rows, requirements, findings))
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
            evidence_errors.extend(f"{name}: {message}" for message in semantic_record_errors(root, record, semantic.project_outputs))
    else:
        evidence_errors.append("missing schema")
    ck("MV-016-evidence-semantics", not evidence_errors, {"errors": evidence_errors})

    foundation_checks = {row.get("check"): row for row in foundation.get("checks", [])} if isinstance(foundation, dict) else {}
    provider_detail = foundation_checks.get("provider_denial", {}).get("detail", {})
    provider_rows = provider_detail.get("register", []) if isinstance(provider_detail, dict) else []
    provider_proof = provider_detail.get("provider_guard_proof", {}) if isinstance(provider_detail, dict) else {}
    artifacts = foundation.get("artifacts", {}) if isinstance(foundation, dict) else {}
    ledger = artifacts.get("application_network_guard", {}) if isinstance(artifacts, dict) else {}
    measurement = artifacts.get("provider_measurement", {}) if isinstance(artifacts, dict) else {}
    measurement_ledger = measurement.get("network_guard", {}) if isinstance(measurement, dict) else {}
    registry_path = (root / "source_payload/stage2a/provider-capability-registry.json") if detached_package_mode else (repo / "stage2a/provider-capability-registry.json")
    provider_errors: list[str] = []
    if not isinstance(ledger, dict) or not isinstance(measurement_ledger, dict) or ledger != measurement_ledger:
        provider_errors.append("provider ledger copies missing or inconsistent")
    if not registry_path.is_file():
        provider_errors.append("provider registry source unavailable")
        registry = {}
        registry_sha256 = ""
    else:
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry_sha256 = sha(registry_path)
    if isinstance(ledger, dict) and isinstance(registry, dict):
        provider_errors.extend(provider_evidence_errors(ledger, registry, registry_sha256, provider_rows, provider_proof, source_paths, source_ids))
    provider_ok = not provider_errors
    startup_detail = foundation_checks.get("startup_side_effect_inventory", {}).get("detail", {})
    outcomes = startup_detail.get("attempt_outcomes", {}) if isinstance(startup_detail, dict) else {}
    startup_ok = (
        set(outcomes) >= {"attempted", "succeeded", "failed", "skipped", "timed_out", "unavailable"}
        and outcomes.get("attempted") == outcomes.get("succeeded") + outcomes.get("failed") + outcomes.get("timed_out") + outcomes.get("unavailable")
        and outcomes.get("arithmetic_valid") is True
        and outcomes.get("measurement_contract", {}).get("one_terminal_state_per_attempt") is True
        and outcomes.get("measurement_contract", {}).get("unique_attempt_identifiers") is True
        and startup_detail.get("oracle_match") is True
        and startup_detail.get("network_guard", {}).get("provider_or_external_attempt_count") == 0
        and len(outcomes.get("events", [])) >= 4
        and all(event.get("state") and event.get("utc_start") and event.get("utc_end") and sum(int(event.get(state, 0)) for state in ("succeeded", "failed", "timed_out", "unavailable", "skipped")) == 1 for event in outcomes.get("events", []))
    )
    ck("MV-016A-provider-startup-measurement", provider_ok and startup_ok, {
        "provider_rows": len(provider_rows), "provider_states_valid": provider_ok, "provider_guard_proof": provider_proof,
        "provider_semantic_errors": provider_errors,
        "startup_attempt_outcomes": outcomes, "startup_measurement_valid": startup_ok,
    })

    process_detail = foundation_checks.get("process_identity", {}).get("detail", {})
    shutdown_detail = foundation_checks.get("controlled_shutdown", {}).get("detail", {})
    process_errors = process_evidence_errors(foundation, process_detail, shutdown_detail)
    ck("MV-016B-process-identity", not process_errors, {
        "startup_and_termination_identity_valid": not process_errors,
        "semantic_errors": process_errors, "foreign_process_policy": "FAIL_CLOSED",
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
        manifest_detail = {"manifest": "DEFERRED_UNTIL_ASSEMBLY_VALIDATION_MATRIX_IS_RECORDED", "rows": 0, "errors": []}
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
        manifest_detail = {"manifest": manifest_name, "rows": manifest_rows, "errors": manifest_errors}
    if args.phase != "assembly":
        manifest_detail = {"manifest": manifest_name, "rows": manifest_rows, "errors": manifest_errors}
    ck("MV-019-checksum-reconciliation", not manifest_errors, manifest_detail)

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
