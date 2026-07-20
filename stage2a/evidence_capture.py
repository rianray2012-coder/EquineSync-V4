#!/usr/bin/env python3
"""Semantically constrained evidence capture for bounded foundation checks."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from lib.control import ENV_FILE, EVIDENCE, REPO, ROOT, canonical, digest, file_sha, load_env, validate_env
from semantic_projection import project_outputs, safe_projection_metadata

SCHEMA_PATH = ROOT / "execution-evidence-schema.json"
SENSITIVE_KEY = r"(?:authorization|access_token|client_secret|password|api_key|api-key|token|secret|credential|bearer)"
SENSITIVE = re.compile(rf"(?i){SENSITIVE_KEY}")
SENSITIVE_ARGUMENT_KEYS = {"authorization", "access_token", "client_secret", "password", "api_key", "api-key", "token", "secret", "credential", "bearer"}
SENSITIVE_QUOTED_ASSIGNMENT = re.compile(rf"(?i)(?P<prefix>[\"']?{SENSITIVE_KEY}[\"']?\s*[:=]\s*)(?P<quote>[\"'])(?P<value>.*?)(?P=quote)")
AUTHORIZATION_BEARER_ASSIGNMENT = re.compile(r"(?i)(?P<prefix>[\"']?authorization[\"']?\s*[:=]\s*Bearer\s+)(?P<value><REDACTED>|[^\s,;]+)")
SENSITIVE_ASSIGNMENT = re.compile(rf"(?im)(?P<prefix>(?<![A-Za-z0-9_-]){SENSITIVE_KEY}(?![A-Za-z0-9_-])\s*[:=]\s*)(?P<value>.*?)(?=\s+[A-Za-z_][A-Za-z0-9_-]*\s*[:=]|\s*$|[,;])")
BARE_BEARER = re.compile(r"(?i)(?P<prefix>(?<![A-Za-z0-9_-])Bearer\s+)(?P<value><REDACTED>|[^\s,;]+)")
KNOWN_SECRET_VALUE = re.compile(r"(?:sk_(?:live|test)_[A-Za-z0-9_-]+|whsec_[A-Za-z0-9_-]+|AKIA[A-Z0-9]{12,})")


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, text=True, capture_output=True, check=True).stdout.strip()


def _relative_or_name(value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(REPO.resolve()).as_posix()
        except ValueError:
            return path.name
    return value


def sanitize_arguments(arguments: list[str]) -> list[str]:
    sanitized: list[str] = []
    redact_next = False
    for index, raw in enumerate(arguments):
        if redact_next:
            sanitized.append("<REDACTED>")
            redact_next = False
            continue
        if raw == "-c":
            sanitized.append(raw)
            redact_next = True
            continue
        argument_key = raw.split("=", 1)[0].lstrip("-").lower()
        if raw.startswith("--") and argument_key in SENSITIVE_ARGUMENT_KEYS:
            if "=" in raw:
                sanitized.append(raw.split("=", 1)[0] + "=<REDACTED>")
            else:
                sanitized.append(raw)
                redact_next = True
            continue
        if "=" in raw and raw.split("=", 1)[0].lower() in SENSITIVE_ARGUMENT_KEYS:
            sanitized.append(raw.split("=", 1)[0] + "=<REDACTED>")
            continue
        sanitized.append(_relative_or_name(raw))
    return sanitized


def redact_output(value: str) -> tuple[str, int]:
    replacements = 0

    def quoted_assignment(match: re.Match[str]) -> str:
        nonlocal replacements
        if match.group("value") == "<REDACTED>":
            return match.group(0)
        replacements += 1
        return f"{match.group('prefix')}{match.group('quote')}<REDACTED>{match.group('quote')}"

    def assignment(match: re.Match[str]) -> str:
        nonlocal replacements
        current = match.group("value").strip()
        if current == "<REDACTED>" or (
            "authorization" in match.group("prefix").lower()
            and current == "Bearer <REDACTED>"
        ):
            return match.group(0)
        replacements += 1
        return f"{match.group('prefix')}<REDACTED>"

    value = AUTHORIZATION_BEARER_ASSIGNMENT.sub(assignment, value)
    value = SENSITIVE_QUOTED_ASSIGNMENT.sub(quoted_assignment, value)
    value = SENSITIVE_ASSIGNMENT.sub(assignment, value)
    value = BARE_BEARER.sub(assignment, value)
    value, token_count = KNOWN_SECRET_VALUE.subn("<REDACTED>", value)
    return value, replacements + token_count


def sensitive_output_matches(value: str) -> list[str]:
    matches = []
    for match in SENSITIVE_QUOTED_ASSIGNMENT.finditer(value):
        if match.group("value") != "<REDACTED>":
            matches.append("quoted_sensitive_assignment")
    for match in SENSITIVE_ASSIGNMENT.finditer(value):
        current = match.group("value").strip()
        if (
            current != "<REDACTED>"
            and not ("authorization" in match.group("prefix").lower() and current == "Bearer <REDACTED>")
        ):
            matches.append("sensitive_assignment")
    for match in AUTHORIZATION_BEARER_ASSIGNMENT.finditer(value):
        if match.group("value") != "<REDACTED>":
            matches.append("authorization_bearer")
    for match in BARE_BEARER.finditer(value):
        if match.group("value") != "<REDACTED>":
            matches.append("bare_bearer")
    if KNOWN_SECRET_VALUE.search(value):
        matches.append("known_secret_value_pattern")
    return sorted(set(matches))


def validate_record_semantics(record: dict[str, object], evidence_root: Path) -> list[str]:
    errors: list[str] = []
    expected = record.get("expected_result", {}).get("exit_status") if isinstance(record.get("expected_result"), dict) else None
    actual = record.get("actual_result", {}).get("exit_status") if isinstance(record.get("actual_result"), dict) else None
    top_level = record.get("exit_status")
    expected_result = "PASS" if actual == expected else "FAIL"
    if actual != top_level:
        errors.append("actual_result.exit_status must equal exit_status")
    if record.get("result") != expected_result:
        errors.append("result must reflect expected-versus-actual exit status")
    try:
        start = dt.datetime.fromisoformat(str(record["utc_start"]))
        end = dt.datetime.fromisoformat(str(record["utc_end"]))
        if end < start:
            errors.append("utc_end precedes utc_start")
    except (KeyError, ValueError):
        errors.append("timestamps are not comparable ISO date-times")
    streams: dict[str, str] = {}
    hashes = record.get("evidence_file_hashes") if isinstance(record.get("evidence_file_hashes"), dict) else {}
    for stream in ("stdout", "stderr"):
        location = record.get(f"{stream}_location")
        path = (evidence_root / str(location)).resolve()
        try:
            path.relative_to(evidence_root.resolve())
        except ValueError:
            errors.append(f"{stream} path escapes evidence root")
            continue
        if not path.is_file():
            errors.append(f"{stream} file missing")
            continue
        content = path.read_text(encoding="utf-8")
        streams[stream] = content
        if file_sha(path) != hashes.get(stream):
            errors.append(f"{stream} SHA-256 mismatch")
        if sensitive_output_matches(content):
            errors.append(f"{stream} contains unredacted sensitive output")
    required_meaning = record.get("required_meaning") if isinstance(record.get("required_meaning"), list) else []
    combined = streams.get("stdout", "") + streams.get("stderr", "")
    lines = set(combined.splitlines())
    if not required_meaning or any(str(marker) not in lines for marker in required_meaning):
        errors.append("required exact-line meaning is absent after redaction")
    redaction = record.get("redaction_evidence") if isinstance(record.get("redaction_evidence"), dict) else {}
    after_projection = project_outputs(streams.get("stdout", ""), streams.get("stderr", ""), sanitized=True)
    exact_matches = {str(marker): str(marker) in lines for marker in required_meaning}
    if (
        redaction.get("meaning_preserved") is not True
        or redaction.get("semantic_projection_sha256_before") != redaction.get("semantic_projection_sha256_after")
        or redaction.get("semantic_projection_sha256_after") != after_projection.sha256
        or redaction.get("sensitive_slot_count_before") != after_projection.sensitive_slot_count
        or redaction.get("placeholder_slot_count_after") != after_projection.placeholder_slot_count
        or redaction.get("sensitive_class_counts_before") != after_projection.sensitive_class_counts
        or redaction.get("unredacted_sensitive_match_count") != after_projection.unredacted_sensitive_count
        or redaction.get("unexpected_redaction_placeholder_count") != after_projection.unexpected_placeholder_count
        or redaction.get("over_redaction_detected") is not False
        or redaction.get("required_exact_line_matches") != exact_matches
    ):
        errors.append("objective redaction projection or exact-line meaning proof failed")
    core = dict(record)
    recorded_hash = core.pop("record_content_sha256", "")
    if hashlib.sha256(canonical(core)).hexdigest() != recorded_hash:
        errors.append("record content SHA-256 mismatch")
    return errors


def capture(
    run_id: str,
    command: list[str],
    expected_exit: int,
    *,
    input_paths: list[Path],
    datastore_before: str = "NOT_APPLICABLE_NO_DATASTORE_WRITE",
    datastore_after: str = "NOT_APPLICABLE_NO_DATASTORE_WRITE",
    cleanup_result: str = "PASS_NO_DATASTORE_WRITE",
    rollback_result: str = "NOT_APPLICABLE_NO_DATASTORE_WRITE",
    required_meaning: list[str],
) -> dict[str, object]:
    env = load_env()
    validate_env(env)
    start = dt.datetime.now(dt.timezone.utc)
    out_dir = EVIDENCE / "stdout"
    err_dir = EVIDENCE / "stderr"
    out_dir.mkdir(parents=True, exist_ok=True)
    err_dir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, timeout=30)
    end = dt.datetime.now(dt.timezone.utc)
    out = out_dir / f"{run_id}.txt"
    err = err_dir / f"{run_id}.txt"
    before_projection = project_outputs(proc.stdout, proc.stderr, sanitized=False)
    safe_stdout, stdout_replacements = redact_output(proc.stdout)
    safe_stderr, stderr_replacements = redact_output(proc.stderr)
    after_projection = project_outputs(safe_stdout, safe_stderr, sanitized=True)
    projected_after = safe_stdout + safe_stderr
    exact_lines = set(projected_after.splitlines())
    exact_matches = {marker: marker in exact_lines for marker in required_meaning}
    meaning_preserved = (
        before_projection.sha256 == after_projection.sha256
        and before_projection.sensitive_slot_count == after_projection.placeholder_slot_count
        and after_projection.unredacted_sensitive_count == 0
        and after_projection.unexpected_placeholder_count == 0
        and all(exact_matches.values())
    )
    if not meaning_preserved:
        raise RuntimeError(
            "independent evidence redaction projection failed: "
            + json.dumps({"before": safe_projection_metadata(before_projection), "after": safe_projection_metadata(after_projection), "required_exact_line_matches": exact_matches}, sort_keys=True)
        )
    out.write_text(safe_stdout, encoding="utf-8")
    err.write_text(safe_stderr, encoding="utf-8")
    artifacts = {_relative_or_name(str(path)): file_sha(path) for path in sorted(input_paths)}
    executable = Path(command[0])
    tool_versions = {"python": sys.version.split()[0]}
    if executable.is_file():
        tool_versions["executable_sha256"] = file_sha(executable)
    core: dict[str, object] = {
        "schema_version": "3.0",
        "package_id": "ES-PKG-2026-004-V003",
        "run_identifier": run_id,
        "command": _relative_or_name(command[0]),
        "sanitized_arguments": sanitize_arguments(command[1:]),
        "input_artifact_hashes": artifacts,
        "configuration_identity": file_sha(ENV_FILE),
        "environment_identity": digest({k: env[k] for k in sorted(env)}),
        "utc_start": start.isoformat(),
        "utc_end": end.isoformat(),
        "commit_hash": _git("rev-parse", "HEAD"),
        "tree_hash": _git("rev-parse", "HEAD^{tree}"),
        "expected_result": {"exit_status": expected_exit},
        "actual_result": {"exit_status": proc.returncode},
        "exit_status": proc.returncode,
        "stdout_location": out.relative_to(ROOT).as_posix(),
        "stderr_location": err.relative_to(ROOT).as_posix(),
        "datastore_digest_before": datastore_before,
        "datastore_digest_after": datastore_after,
        "cleanup_result": cleanup_result,
        "rollback_result": rollback_result,
        "tool_versions": tool_versions,
        "evidence_file_hashes": {"stdout": file_sha(out), "stderr": file_sha(err)},
        "redaction_status": "PASS_VALUES_REDACTED_PATHS_REPOSITORY_RELATIVE",
        "required_meaning": required_meaning,
        "redaction_evidence": {
            "policy": "SENSITIVE_ASSIGNMENTS_AND_KNOWN_SECRET_VALUE_PATTERNS_REDACTED",
            "stdout_replacements": stdout_replacements,
            "stderr_replacements": stderr_replacements,
            "unredacted_sensitive_match_count": len(sensitive_output_matches(safe_stdout + safe_stderr)),
            "projection_engine": "S2A-INDEPENDENT-SEMANTIC-PROJECTOR-V1",
            "normalization_version": "S2A-REDACTION-PROJECTION-V3",
            "semantic_projection_sha256_before": before_projection.sha256,
            "semantic_projection_sha256_after": after_projection.sha256,
            "sensitive_slot_count_before": before_projection.sensitive_slot_count,
            "placeholder_slot_count_after": after_projection.placeholder_slot_count,
            "sensitive_class_counts_before": before_projection.sensitive_class_counts,
            "unexpected_redaction_placeholder_count": after_projection.unexpected_placeholder_count,
            "over_redaction_detected": after_projection.unexpected_placeholder_count != 0 or before_projection.sha256 != after_projection.sha256,
            "required_exact_line_matches": exact_matches,
            "meaning_preserved": meaning_preserved,
        },
        "result": "PASS" if proc.returncode == expected_exit else "FAIL",
        "execution_status": "EXECUTION_NOT_AUTHORIZED",
    }
    record = core | {"record_content_sha256": hashlib.sha256(canonical(core)).hexdigest()}
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
    semantic_errors = validate_record_semantics(record, ROOT)
    if semantic_errors:
        raise RuntimeError("evidence semantic validation failed: " + "; ".join(semantic_errors))
    target = EVIDENCE / f"{run_id}.json"
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--expected-exit", type=int, required=True)
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--required-meaning", action="append", required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command or not args.input:
        raise SystemExit("command and at least one --input are required")
    print(json.dumps(capture(args.run_id, args.command, args.expected_exit, input_paths=[Path(x) for x in args.input], required_meaning=args.required_meaning), indent=2))
