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

SCHEMA_PATH = ROOT / "execution-evidence-schema.json"
SENSITIVE = re.compile(r"(?i)(secret|token|password|api[_-]?key|credential|authorization)")


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
        if raw.startswith("--") and SENSITIVE.search(raw.split("=", 1)[0]):
            if "=" in raw:
                sanitized.append(raw.split("=", 1)[0] + "=<REDACTED>")
            else:
                sanitized.append(raw)
                redact_next = True
            continue
        if "=" in raw and SENSITIVE.search(raw.split("=", 1)[0]):
            sanitized.append(raw.split("=", 1)[0] + "=<REDACTED>")
            continue
        sanitized.append(_relative_or_name(raw))
    return sanitized


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
    out.write_text(proc.stdout, encoding="utf-8")
    err.write_text(proc.stderr, encoding="utf-8")
    artifacts = {_relative_or_name(str(path)): file_sha(path) for path in sorted(input_paths)}
    executable = Path(command[0])
    tool_versions = {"python": sys.version.split()[0]}
    if executable.is_file():
        tool_versions["executable_sha256"] = file_sha(executable)
    core: dict[str, object] = {
        "schema_version": "2.0",
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
        "result": "PASS" if proc.returncode == expected_exit else "FAIL",
        "execution_status": "EXECUTION_NOT_AUTHORIZED",
    }
    record = core | {"record_content_sha256": hashlib.sha256(canonical(core)).hexdigest()}
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
    target = EVIDENCE / f"{run_id}.json"
    target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--expected-exit", type=int, required=True)
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command or not args.input:
        raise SystemExit("command and at least one --input are required")
    print(json.dumps(capture(args.run_id, args.command, args.expected_exit, input_paths=[Path(x) for x in args.input]), indent=2))
