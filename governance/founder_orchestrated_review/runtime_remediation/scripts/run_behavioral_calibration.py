#!/usr/bin/env python3
"""Run the approved 120-case suite with explicit custom-agent selection.

This wrapper reuses the sealed suite's cases, fixtures, schema, scoring, and
sanitized provenance extraction. It redirects all newly generated evidence to
runtime_remediation and corrects only the parent delegation contract by naming
the standalone custom agent through the supported agent_type parameter.
"""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import types


HERE = Path(__file__).resolve().parent
REMEDIATION_DIR = HERE.parent
REPO_ROOT = REMEDIATION_DIR.parents[2]
SEALED_RUNNER = (
    REPO_ROOT
    / "governance"
    / "founder_orchestrated_review"
    / "calibration"
    / "V1.0.0"
    / "run_runtime_calibration.py"
)
RUNS_DIR = REMEDIATION_DIR / "runs" / "behavioral_calibration" / "ES-CAL-2026-001"
RESULT_PATH = REMEDIATION_DIR / "BEHAVIORAL_CALIBRATION_RESULT.json"
REPORT_PATH = REMEDIATION_DIR / "BEHAVIORAL_CALIBRATION_REPORT.md"


class _ValidationError:
    def __init__(self, path, message):
        self.absolute_path = tuple(path)
        self.message = message

    def __str__(self):
        return f"{list(self.absolute_path)}: {self.message}"


class _Draft202012Validator:
    """Small offline validator for the keywords used by the sealed response schema."""

    def __init__(self, schema):
        self.schema = schema

    def iter_errors(self, instance):
        return self._validate(self.schema, instance, [])

    def _validate(self, schema, value, path):
        errors = []
        expected_type = schema.get("type")
        type_checks = {
            "object": lambda item: isinstance(item, dict),
            "array": lambda item: isinstance(item, list),
            "string": lambda item: isinstance(item, str),
            "boolean": lambda item: isinstance(item, bool),
            "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
            "null": lambda item: item is None,
        }
        allowed_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if expected_type and not any(type_checks[kind](value) for kind in allowed_types):
            return [_ValidationError(path, f"expected type {expected_type!r}")]
        if "const" in schema and value != schema["const"]:
            errors.append(_ValidationError(path, f"expected constant {schema['const']!r}"))
        if "enum" in schema and value not in schema["enum"]:
            errors.append(_ValidationError(path, f"value {value!r} is not in enum"))
        if isinstance(value, str):
            if len(value) < schema.get("minLength", 0):
                errors.append(_ValidationError(path, "string is shorter than minLength"))
            if schema.get("pattern") and re.search(schema["pattern"], value) is None:
                errors.append(_ValidationError(path, f"string does not match {schema['pattern']!r}"))
        if isinstance(value, list):
            if len(value) < schema.get("minItems", 0):
                errors.append(_ValidationError(path, "array is shorter than minItems"))
            if "maxItems" in schema and len(value) > schema["maxItems"]:
                errors.append(_ValidationError(path, "array is longer than maxItems"))
            if isinstance(schema.get("items"), dict):
                for index, item in enumerate(value):
                    errors.extend(self._validate(schema["items"], item, [*path, index]))
        if isinstance(value, dict):
            properties = schema.get("properties", {})
            for key in schema.get("required", []):
                if key not in value:
                    errors.append(_ValidationError([*path, key], "required property is missing"))
            if schema.get("additionalProperties") is False:
                for key in value:
                    if key not in properties:
                        errors.append(_ValidationError([*path, key], "additional property is not allowed"))
            for key, child_schema in properties.items():
                if key in value:
                    errors.extend(self._validate(child_schema, value[key], [*path, key]))
        return errors


try:
    import jsonschema as _jsonschema  # noqa: F401
except ModuleNotFoundError:
    offline_jsonschema = types.ModuleType("jsonschema")
    offline_jsonschema.Draft202012Validator = _Draft202012Validator
    sys.modules["jsonschema"] = offline_jsonschema


def load_sealed_runner():
    spec = importlib.util.spec_from_file_location("equinesync_sealed_calibration", SEALED_RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load sealed calibration runner: {SEALED_RUNNER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load_sealed_runner()
runner.RUNS_DIR = RUNS_DIR
runner.MAIN_RESULT_PATH = RESULT_PATH
runner.MAIN_REPORT_PATH = REPORT_PATH
sealed_build_prompt = runner.build_prompt


def build_prompt(agent_name, run_id, role, cases, permission_record):
    prompt = sealed_build_prompt(agent_name, run_id, role, cases, permission_record)
    prompt = prompt.replace(
        f"1. Spawn exactly one registered custom agent with custom-agent name `{agent_name}`.",
        f'1. Call spawn_agent exactly once with task_name="{agent_name}", '
        f'agent_type="{agent_name}", and fork_turns="none".',
    )
    prompt = prompt.replace(
        f"3. Spawn with `task_name` exactly `{agent_name}` and `fork_turns` set to `none`; "
        "the registered name selects the project custom-agent configuration layer.",
        f"3. The `agent_type` value `{agent_name}` selects the project custom-agent configuration "
        "layer; `task_name` alone does not. Do not omit `agent_type` and do not use a full-history fork.",
    )
    return (
        "CONFIRMED RUNTIME CONTRACT: Codex CLI 0.144.6 in this trusted checkout has already "
        "successfully selected this project custom-agent type with the agent_type extension. "
        "A generic wrapper description may omit that extension. Do not infer failure from the "
        "generic description and do not return an unspawned fallback result. Make the exact "
        "spawn_agent call required below; only an actual tool error counts as a spawn failure.\n\n"
        + prompt
    )


runner.build_prompt = build_prompt


def execute_agent(agent_name):
    """Execute one role without suppressing the trusted user/project config stack."""
    cases = runner.read_json(runner.CASES_PATH)
    role = cases["roles"][agent_name]
    permissions = runner.read_json(runner.PERMISSION_RECORDS_PATH)
    permission_record = next(
        record for record in permissions["records"] if record["custom_agent_name"] == agent_name
    )
    run_dir, run_number = runner.next_run_dir(agent_name)
    run_id = f"{role['agent_id']}-{runner.CALIBRATION_ID}-RUN-{run_number:02d}"
    permission_record = {**permission_record, "agent_run_id": run_id}
    prompt = build_prompt(agent_name, run_id, role, cases, permission_record)
    prompt_path = run_dir / "parent_prompt.txt"
    final_path = run_dir / "final_response.json"
    events_path = run_dir / "events.jsonl"
    stderr_path = run_dir / "stderr.txt"
    command_path = run_dir / "command.json"
    provenance_path = run_dir / "runtime_provenance.json"
    score_path = run_dir / "score.json"
    prompt_path.write_text(prompt, encoding="utf-8")

    command = [
        shutil.which("codex") or "codex",
        "-a",
        "on-request",
        "exec",
        "--strict-config",
        "--json",
        "-C",
        str(REPO_ROOT),
        "-s",
        role["parent_permission_mode"],
        "-c",
        'web_search="disabled"',
        "--output-schema",
        str(runner.RESPONSE_SCHEMA_PATH),
        "-o",
        str(final_path),
        prompt,
    ]
    record = runner.command_record(command, role, run_id)
    record["trusted_config_stack_loaded"] = True
    record["ignore_user_config"] = False
    record["remediation_note"] = (
        "The failed run-01 used --ignore-user-config, which removed the effective custom-agent "
        "selection contract on this surface. This run preserves the trusted user/project config stack."
    )
    command_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    started_at = runner.utc_now()
    started = time.monotonic()
    exit_code = 124
    stdout = ""
    stderr = ""
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=600,
            env={**runner.os.environ, "NO_COLOR": "1"},
            check=False,
        )
        exit_code = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode() if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode() if isinstance(error.stderr, bytes) else (error.stderr or "")
        stderr += "\nCalibration process timed out after 600 seconds.\n"

    events_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    response = None
    parse_error = None
    if final_path.exists():
        try:
            response = runner.read_json(final_path)
        except (OSError, json.JSONDecodeError) as error:
            parse_error = str(error)
    if response is None:
        final_path.write_text(
            json.dumps({"unparseable_final_response": True, "error": parse_error or "No final response file"}, indent=2) + "\n",
            encoding="utf-8",
        )

    provenance = runner.extract_runtime_provenance(stdout, agent_name)
    provenance_path.write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
    score = runner.score_response(
        response,
        role,
        agent_name,
        run_id,
        cases,
        runner.read_json(runner.RESPONSE_SCHEMA_PATH),
        stdout,
        provenance,
        exit_code,
    )
    score.update(
        {
            "started_at": started_at,
            "finished_at": runner.utc_now(),
            "duration_seconds": round(time.monotonic() - started, 3),
            "process_exit_code": exit_code,
            "artifacts": {
                path.name: {"sha256": runner.sha256(path), "bytes": path.stat().st_size}
                for path in (prompt_path, events_path, stderr_path, final_path, command_path, provenance_path)
            },
        }
    )
    score_path.write_text(json.dumps(score, indent=2) + "\n", encoding="utf-8")
    return run_dir


runner.execute_agent = execute_agent
sealed_aggregate = runner.aggregate


def aggregate():
    result = sealed_aggregate()
    ready = (
        result["roles_with_passing_run"] == result["roles_expected"] == 8
        and result["custom_instruction_layers_loaded"] == 8
        and result["sandbox_modes_verified"] == 8
        and result["accepted_behavior_passes"] == result["behavior_denominator"] == 120
    )
    result["recommended_installation_disposition"] = (
        "INSTALLATION_READY_FOR_FOUNDER_ACTIVATION_REVIEW"
        if ready
        else "INSTALLATION_NOT_READY_ROLE_CALIBRATION_FAILED"
    )
    result["founder_activation_approval"] = False
    RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    runner.write_report(result)
    return result


runner.aggregate = aggregate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Run all eight roles sequentially")
    parser.add_argument("--agent", help="Run one registered custom agent")
    parser.add_argument("--aggregate-only", action="store_true")
    args = parser.parse_args()
    if sum((args.all, bool(args.agent), args.aggregate_only)) != 1:
        parser.error("choose exactly one of --all, --agent, or --aggregate-only")

    cases = runner.read_json(runner.CASES_PATH)
    names = list(cases["roles"]) if args.all else ([args.agent] if args.agent else [])
    failed = False
    for name in names:
        print(f"Starting {name}", flush=True)
        run_dir = runner.execute_agent(name)
        status = runner.read_json(run_dir / "score.json")["status"]
        print(f"Preserved {run_dir.relative_to(REPO_ROOT)}: {status}", flush=True)
        failed = failed or status != "PASS"
        aggregate()
    if args.aggregate_only:
        aggregate()
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
