#!/usr/bin/env python3
"""Validate the installed EquineSync Founder-Orchestrated Review Agent system.

This validator is installation-level evidence. It deliberately lives outside the
sealed V1.0.0 configuration package and never edits package-controlled files.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import re
import subprocess
import sys
import tomllib
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import unquote, urldefrag, urlparse

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover - exercised only in a broken environment
    raise SystemExit(
        "Missing validation dependency. Install validation/requirements.txt "
        f"with the selected Python interpreter: {exc}"
    ) from exc


SCRIPT_PATH = Path(__file__).resolve()
VALIDATION_DIR = SCRIPT_PATH.parent
REPO_ROOT = SCRIPT_PATH.parents[3]
INSTALL_ROOT = REPO_ROOT / "governance/founder_orchestrated_review"
PACKAGE_ROOT = INSTALL_ROOT / "agent_config/V1.0.0"
AGENT_DIR = REPO_ROOT / ".codex/agents"
SOURCE_PACKAGE_DIR = INSTALL_ROOT / "agent_config/packages"
ZIP_NAME = "EquineSync_Founder_Orchestrated_Review_Agent_Config_Package_V1.0.0.zip"
ZIP_PATH = SOURCE_PACKAGE_DIR / ZIP_NAME
CHECKSUM_PATH = SOURCE_PACKAGE_DIR / f"{ZIP_NAME}.sha256"
EXPECTED_ZIP_SHA256 = "604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3"
EXPECTED_SOURCE_COMMIT = "a1caf346fe7b07b1be7dde12f1b805a62b2e5f9b"
EXPECTED_PACKAGE_VERSION = "1.0.0"
EXPECTED_FRAMEWORK_VERSION = "V1.3"

REPORT_PATH = VALIDATION_DIR / "INSTALLED_SYSTEM_VALIDATION_REPORT.md"
RESULT_PATH = VALIDATION_DIR / "INSTALLED_SYSTEM_VALIDATION_RESULT.json"
COMMAND_LOG_PATH = VALIDATION_DIR / "INSTALLED_SYSTEM_VALIDATION_COMMAND_LOG.txt"
DEPENDENCY_PATH = VALIDATION_DIR / "INSTALLED_SYSTEM_VALIDATION_DEPENDENCIES.json"

DIRECTIVE_PATH = PACKAGE_ROOT / "orchestration/CODEX_ORCHESTRATION_DIRECTIVE.md"
CONTRACT_PATH = PACKAGE_ROOT / "shared/COMMON_AGENT_OPERATING_CONTRACT.md"
PACKAGE_VALIDATOR_PATH = PACKAGE_ROOT / "scripts/validate_package.py"
MANIFEST_PATH = PACKAGE_ROOT / "PACKAGE_MANIFEST.json"
SCHEMA_DIR = PACKAGE_ROOT / "schemas"

REQUIRED_AGENT_FIELDS = {
    "name",
    "description",
    "developer_instructions",
    "sandbox_mode",
    "approval_policy",
}
ALLOWED_AGENT_FIELDS = set(REQUIRED_AGENT_FIELDS)

ROLE_MAP = {
    "equinesync_drafting_agent.toml": {
        "name": "equinesync_drafting_agent",
        "agent_id": "ES-RA-01",
        "prompt": "prompts/ES-RA-01_DRAFTING_AGENT.md",
        "sandbox_mode": "workspace-write",
        "registration_marker": "ES-RA-01-REGISTERED-V1.0.0",
    },
    "equinesync_segregated_review_agent.toml": {
        "name": "equinesync_segregated_review_agent",
        "agent_id": "ES-RA-02",
        "prompt": "prompts/ES-RA-02_SEGREGATED_REVIEW_AGENT.md",
        "sandbox_mode": "read-only",
        "registration_marker": "ES-RA-02-REGISTERED-V1.0.0",
    },
    "equinesync_adversarial_challenge_agent.toml": {
        "name": "equinesync_adversarial_challenge_agent",
        "agent_id": "ES-RA-03",
        "prompt": "prompts/ES-RA-03_ADVERSARIAL_CHALLENGE_AGENT.md",
        "sandbox_mode": "read-only",
        "registration_marker": "ES-RA-03-REGISTERED-V1.0.0",
    },
    "equinesync_machine_validation_agent.toml": {
        "name": "equinesync_machine_validation_agent",
        "agent_id": "ES-RA-04",
        "prompt": "prompts/ES-RA-04_MACHINE_VALIDATION_AGENT.md",
        "sandbox_mode": "workspace-write",
        "registration_marker": "ES-RA-04-REGISTERED-V1.0.0",
    },
    "equinesync_evidence_custodian.toml": {
        "name": "equinesync_evidence_custodian",
        "agent_id": "ES-RA-05",
        "prompt": "prompts/ES-RA-05_EVIDENCE_CUSTODIAN.md",
        "sandbox_mode": "workspace-write",
        "registration_marker": "ES-RA-05-REGISTERED-V1.0.0",
    },
    "equinesync_domain_reviewer.toml": {
        "name": "equinesync_domain_reviewer",
        "agent_id": "ES-RA-06",
        "prompt": "prompts/ES-RA-06_DOMAIN_REVIEWER.md",
        "sandbox_mode": "read-only",
        "registration_marker": "ES-RA-06-REGISTERED-V1.0.0",
    },
    "equinesync_synthetic_golden_path_agent.toml": {
        "name": "equinesync_synthetic_golden_path_agent",
        "agent_id": "ES-RA-07",
        "prompt": "prompts/ES-RA-07_SYNTHETIC_GOLDEN_PATH_SPECIFICATION_AGENT.md",
        "sandbox_mode": "workspace-write",
        "registration_marker": "ES-RA-07-REGISTERED-V1.0.0",
    },
    "equinesync_executable_golden_path_controller.toml": {
        "name": "equinesync_executable_golden_path_controller",
        "agent_id": "ES-RA-08",
        "prompt": "prompts/ES-RA-08_EXECUTABLE_GOLDEN_PATH_REPRODUCTION_CONTROLLER.md",
        "sandbox_mode": "workspace-write",
        "registration_marker": "ES-RA-08-REGISTERED-V1.0.0",
    },
}
RUNTIME_CANARY_FILE = "es_runtime_canary.toml"
RUNTIME_CANARY_NAME = "es_runtime_canary"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if completed.returncode == 0 else "UNAVAILABLE"


def package_version(package_name: str) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "UNAVAILABLE"


class Validation:
    def __init__(self) -> None:
        self.started_at = now_utc()
        self.checks: list[dict[str, Any]] = []
        self.commands: list[dict[str, Any]] = []
        self.limitations: list[str] = [
            "Static validation does not prove runtime custom-agent registration or role compliance.",
            "TOML sandbox defaults can be superseded by the parent session's live permission overrides.",
            "Codex workspace-write is a workspace boundary, not path-level enforcement for role-specific output directories.",
            "Cross-file consistency checks cover the installation's declared invariants; they are not a proof of every semantic relationship in the framework.",
        ]

    def check(
        self,
        check_id: str,
        title: str,
        procedure: Callable[[], Any],
        summarize: Callable[[Any], Any] | None = None,
    ) -> Any:
        try:
            evidence = procedure()
        except Exception as exc:  # noqa: BLE001 - every validation failure must be recorded
            self.checks.append(
                {
                    "check_id": check_id,
                    "title": title,
                    "status": "FAIL",
                    "detail": f"{type(exc).__name__}: {exc}",
                }
            )
            return None
        detail_value = summarize(evidence) if summarize else evidence
        self.checks.append(
            {
                "check_id": check_id,
                "title": title,
                "status": "PASS",
                "detail": (
                    detail_value
                    if isinstance(detail_value, str)
                    else json.dumps(detail_value, sort_keys=True)
                ),
            }
        )
        return evidence

    def run(self, command: list[str], cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
        self.commands.append(
            {
                "command": command,
                "cwd": str(cwd.relative_to(REPO_ROOT)) if cwd != REPO_ROOT else ".",
                "return_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }
        )
        return completed

    @property
    def failures(self) -> list[dict[str, Any]]:
        return [item for item in self.checks if item["status"] == "FAIL"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_pointer(document: Any, fragment: str) -> Any:
    if fragment in ("", "#"):
        return document
    pointer = fragment[1:] if fragment.startswith("#") else fragment
    pointer = unquote(pointer)
    if not pointer.startswith("/"):
        raise ValueError(f"Unsupported JSON Pointer fragment: {fragment}")
    current = document
    for raw_token in pointer.lstrip("/").split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        else:
            current = current[token]
    return current


def iter_refs(value: Any, location: str = "$") -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key == "$ref" and isinstance(child, str):
                found.append((child_location, child))
            found.extend(iter_refs(child, child_location))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(iter_refs(child, f"{location}[{index}]"))
    return found


def unresolved_refs(schema_path: Path, schema: dict[str, Any]) -> list[str]:
    unresolved: list[str] = []
    for location, reference in iter_refs(schema):
        try:
            target_part, fragment = urldefrag(reference)
            if not target_part:
                target_document = schema
            else:
                parsed = urlparse(target_part)
                if parsed.scheme or parsed.netloc:
                    raise ValueError("external reference is not locally sealed")
                target_path = (schema_path.parent / unquote(target_part)).resolve()
                if SCHEMA_DIR.resolve() not in target_path.parents and target_path != SCHEMA_DIR.resolve():
                    raise ValueError("reference escapes the schema directory")
                target_document = load_json(target_path)
            resolve_pointer(target_document, f"#{fragment}" if fragment else "")
        except Exception as exc:  # noqa: BLE001 - include every unresolved reference
            unresolved.append(f"{schema_path.name}:{location}: {reference}: {exc}")
    return unresolved


def check_zip_hash() -> str:
    if not ZIP_PATH.is_file():
        raise FileNotFoundError(ZIP_PATH)
    actual = sha256_file(ZIP_PATH)
    if actual != EXPECTED_ZIP_SHA256:
        raise ValueError(f"expected {EXPECTED_ZIP_SHA256}, got {actual}")
    return actual


def check_checksum_file() -> str:
    expected_line = f"{EXPECTED_ZIP_SHA256}  {ZIP_NAME}"
    lines = CHECKSUM_PATH.read_text(encoding="utf-8").splitlines()
    if lines != [expected_line]:
        raise ValueError(f"checksum file content mismatch: {lines!r}")
    return expected_line


def check_archive_install_identity() -> dict[str, Any]:
    with zipfile.ZipFile(ZIP_PATH) as archive:
        entries = [item for item in archive.infolist() if not item.is_dir()]
        if len(entries) != 67:
            raise ValueError(f"expected 67 archive files, found {len(entries)}")
        top_levels = {Path(item.filename).parts[0] for item in entries}
        if len(top_levels) != 1:
            raise ValueError(f"unexpected archive roots: {sorted(top_levels)}")
        archive_relative: set[str] = set()
        mismatches: list[str] = []
        for item in entries:
            parts = Path(item.filename).parts
            relative = Path(*parts[1:])
            relative_name = relative.as_posix()
            archive_relative.add(relative_name)
            installed_path = PACKAGE_ROOT / relative
            if not installed_path.is_file():
                mismatches.append(f"missing installed file: {relative_name}")
                continue
            archive_bytes = archive.read(item)
            installed_bytes = installed_path.read_bytes()
            if archive_bytes != installed_bytes:
                mismatches.append(
                    f"byte mismatch: {relative_name}: archive={sha256_bytes(archive_bytes)} "
                    f"installed={sha256_bytes(installed_bytes)}"
                )
        installed_relative = {
            path.relative_to(PACKAGE_ROOT).as_posix()
            for path in PACKAGE_ROOT.rglob("*")
            if path.is_file()
        }
        if archive_relative != installed_relative:
            for name in sorted(archive_relative - installed_relative):
                mismatches.append(f"archive-only file: {name}")
            for name in sorted(installed_relative - archive_relative):
                mismatches.append(f"installed-only file: {name}")
        if mismatches:
            raise ValueError("; ".join(mismatches))
    return {"file_count": len(entries), "mismatches": 0}


def parse_and_validate_agents() -> dict[str, dict[str, Any]]:
    all_files = sorted(AGENT_DIR.glob("*.toml"))
    expected_files = sorted([*ROLE_MAP, RUNTIME_CANARY_FILE])
    if [path.name for path in all_files] != expected_files:
        raise ValueError(
            f"agent file set mismatch: actual={[path.name for path in all_files]} "
            f"expected={expected_files}"
        )
    files = [AGENT_DIR / name for name in sorted(ROLE_MAP)]
    parsed: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for path in files:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        missing = REQUIRED_AGENT_FIELDS - set(data)
        unexpected = set(data) - ALLOWED_AGENT_FIELDS
        if missing or unexpected:
            raise ValueError(f"{path.name}: missing={sorted(missing)} unexpected={sorted(unexpected)}")
        if not all(isinstance(data[field], str) and data[field].strip() for field in REQUIRED_AGENT_FIELDS):
            raise TypeError(f"{path.name}: every required field must be a non-empty string")
        expected = ROLE_MAP[path.name]
        if data["name"] != expected["name"]:
            raise ValueError(f"{path.name}: name {data['name']} != {expected['name']}")
        if data["name"] in names:
            raise ValueError(f"duplicate custom-agent name: {data['name']}")
        names.add(data["name"])
        if data["sandbox_mode"] != expected["sandbox_mode"]:
            raise ValueError(
                f"{path.name}: sandbox {data['sandbox_mode']} != {expected['sandbox_mode']}"
            )
        if data["approval_policy"] != "on-request":
            raise ValueError(f"{path.name}: approval_policy must be on-request")
        instructions = data["developer_instructions"]
        if expected["registration_marker"] not in instructions:
            raise ValueError(
                f"{path.name}: missing runtime registration marker {expected['registration_marker']}"
            )
        required_refs = [
            expected["prompt"],
            "shared/COMMON_AGENT_OPERATING_CONTRACT.md",
            "orchestration/CODEX_ORCHESTRATION_DIRECTIVE.md",
        ]
        for relative_reference in required_refs:
            referenced = PACKAGE_ROOT / relative_reference
            if not referenced.is_file():
                raise FileNotFoundError(referenced)
            repository_reference = referenced.relative_to(REPO_ROOT).as_posix()
            if repository_reference not in instructions:
                raise ValueError(f"{path.name}: missing reference {repository_reference}")
        for phrase in (
            "pre-spawn permission record",
            "Founder Review Authorization",
            "frozen",
            "scope denominator",
            "Work Completeness Ledger",
            "Completion Attestation",
            "Rian Ray is the sole Founder disposition authority",
        ):
            if phrase not in instructions:
                raise ValueError(f"{path.name}: missing control phrase {phrase!r}")
        parsed[path.name] = data
    return parsed


def validate_runtime_canary() -> dict[str, Any]:
    path = AGENT_DIR / RUNTIME_CANARY_FILE
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    missing = REQUIRED_AGENT_FIELDS - set(data)
    unexpected = set(data) - ALLOWED_AGENT_FIELDS
    if missing or unexpected:
        raise ValueError(
            f"{path.name}: missing={sorted(missing)} unexpected={sorted(unexpected)}"
        )
    if data["name"] != RUNTIME_CANARY_NAME:
        raise ValueError(f"{path.name}: unexpected name {data['name']!r}")
    if data["sandbox_mode"] != "read-only":
        raise ValueError(f"{path.name}: sandbox_mode must be read-only")
    if data["approval_policy"] != "on-request":
        raise ValueError(f"{path.name}: approval_policy must be on-request")
    instructions = data["developer_instructions"]
    for phrase in (
        "temporary calibration infrastructure for runtime discovery only",
        "Return exactly ES_RUNTIME_CANARY_LOADED_V1 and no other text",
        "Do not use tools, inspect files, perform substantive work, or claim activation",
    ):
        if phrase not in instructions:
            raise ValueError(f"{path.name}: missing control phrase {phrase!r}")
    return {
        "file": path.relative_to(REPO_ROOT).as_posix(),
        "name": data["name"],
        "sandbox_mode": data["sandbox_mode"],
        "approval_policy": data["approval_policy"],
        "classification": "CALIBRATION_ONLY_NOT_A_REGISTERED_REVIEW_ROLE",
    }


def validate_schemas() -> dict[str, Any]:
    schema_files = sorted(SCHEMA_DIR.glob("*.json"))
    if len(schema_files) != 20:
        raise ValueError(f"expected 20 schemas, found {len(schema_files)}")
    unresolved: list[str] = []
    for path in schema_files:
        schema = load_json(path)
        if not isinstance(schema, dict):
            raise TypeError(f"{path.name} is not a JSON object")
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise ValueError(f"{path.name}: unexpected or missing Draft 2020-12 declaration")
        Draft202012Validator.check_schema(schema)
        unresolved.extend(unresolved_refs(path, schema))
    if unresolved:
        raise ValueError("unresolved $ref values: " + "; ".join(unresolved))
    ref_count = sum(len(iter_refs(load_json(path))) for path in schema_files)
    return {"schema_count": len(schema_files), "draft": "2020-12", "ref_count": ref_count}


def validate_instance(instance_path: Path, schema_path: Path) -> str:
    instance = load_json(instance_path)
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path))
    if errors:
        messages = [
            f"{'/'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
            for error in errors
        ]
        raise ValueError("; ".join(messages))
    return f"{instance_path.relative_to(PACKAGE_ROOT)} validates against {schema_path.name}"


def validate_all_json_examples() -> list[str]:
    mapping = {
        "EXAMPLE_REVIEW_AUTHORIZATION.json": "review_authorization.schema.json",
    }
    example_files = sorted((PACKAGE_ROOT / "examples").glob("*.json"))
    if {path.name for path in example_files} != set(mapping):
        raise ValueError(
            f"unmapped or missing JSON examples: actual={[path.name for path in example_files]} "
            f"mapped={sorted(mapping)}"
        )
    return [validate_instance(path, SCHEMA_DIR / mapping[path.name]) for path in example_files]


def validate_manifest_bytes() -> dict[str, Any]:
    manifest = load_json(MANIFEST_PATH)
    listed = {item["path"]: item for item in manifest["files"]}
    if len(listed) != 63:
        raise ValueError(f"expected 63 manifest entries, found {len(listed)}")
    mismatches: list[str] = []
    for relative, item in listed.items():
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            mismatches.append(f"missing {relative}")
            continue
        if path.stat().st_size != item["bytes"]:
            mismatches.append(f"size {relative}")
        if sha256_file(path) != item["sha256"]:
            mismatches.append(f"hash {relative}")
    if mismatches:
        raise ValueError("manifest mismatches: " + ", ".join(mismatches))
    return {"manifest_entries": len(listed), "mismatches": 0}


def extract_declared_version(path: Path, label: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"\*\*{re.escape(label)}:\*\*\s*([^\s]+)", text)
    if not match:
        raise ValueError(f"{path.relative_to(PACKAGE_ROOT)}: missing {label}")
    return match.group(1)


def validate_cross_file_consistency(agent_data: dict[str, dict[str, Any]]) -> dict[str, Any]:
    registry = load_json(PACKAGE_ROOT / "config/agent_registry.json")
    tool_policy = load_json(PACKAGE_ROOT / "config/tool_policy.json")
    review_gates = load_json(PACKAGE_ROOT / "config/review_gates.json")
    versions = load_json(PACKAGE_ROOT / "config/directive_versions.json")
    manifest = load_json(MANIFEST_PATH)

    expected_ids = {item["agent_id"] for item in ROLE_MAP.values()}
    registry_by_id = {item["agent_id"]: item for item in registry["agents"]}
    if set(registry_by_id) != expected_ids or len(registry["agents"]) != 8:
        raise ValueError("agent_registry agent IDs do not match the eight installed roles")
    if set(tool_policy["role_policies"]) != expected_ids:
        raise ValueError("tool_policy role IDs do not match the agent registry")
    defaults = tool_policy["default_rules"]
    for required_false in (
        "production_write_allowed",
        "destructive_actions_allowed",
        "secret_exposure_allowed",
        "frozen_package_mutation_allowed",
    ):
        if defaults.get(required_false) is not False:
            raise ValueError(f"tool policy must set {required_false}=false")
    if defaults.get("network_access_default") != "DENY_UNLESS_AUTHORIZED":
        raise ValueError("tool policy network default is not DENY_UNLESS_AUTHORIZED")

    unknown_gate_roles = {
        agent_id
        for gate in review_gates["gates"]
        for agent_id in gate["required_agents"]
        if agent_id not in expected_ids
    }
    if unknown_gate_roles:
        raise ValueError(f"review_gates contains unknown roles: {sorted(unknown_gate_roles)}")

    if versions["package_version"] != EXPECTED_PACKAGE_VERSION:
        raise ValueError("directive_versions package version mismatch")
    if versions["framework_version"] != EXPECTED_FRAMEWORK_VERSION:
        raise ValueError("directive_versions framework version mismatch")
    if versions["common_contract"] != extract_declared_version(CONTRACT_PATH, "Contract version"):
        raise ValueError("Common Agent Operating Contract version mismatch")
    if versions["codex_orchestration_directive"] != extract_declared_version(
        DIRECTIVE_PATH, "Directive version"
    ):
        raise ValueError("Codex orchestration directive version mismatch")

    prompt_files = {path.relative_to(PACKAGE_ROOT).as_posix() for path in (PACKAGE_ROOT / "prompts").glob("*.md")}
    expected_prompts = {item["prompt"] for item in ROLE_MAP.values()}
    if prompt_files != expected_prompts:
        raise ValueError("prompt file set does not match role map")

    for file_name, expected in ROLE_MAP.items():
        agent_id = expected["agent_id"]
        registry_item = registry_by_id[agent_id]
        if registry_item["prompt"] != expected["prompt"]:
            raise ValueError(f"{agent_id}: registry prompt mismatch")
        if registry_item["shared_contract"] != "shared/COMMON_AGENT_OPERATING_CONTRACT.md":
            raise ValueError(f"{agent_id}: registry contract mismatch")
        if registry_item.get("may_issue_final_approval") is not False:
            raise ValueError(f"{agent_id}: may_issue_final_approval must be false")
        if versions["agent_prompts"].get(agent_id) != extract_declared_version(
            PACKAGE_ROOT / expected["prompt"], "Prompt version"
        ):
            raise ValueError(f"{agent_id}: prompt version mismatch")
        if agent_data[file_name]["name"] != expected["name"]:
            raise ValueError(f"{agent_id}: TOML role mapping mismatch")

    manifest_paths = {item["path"] for item in manifest["files"]}
    actual_schema_paths = {
        path.relative_to(PACKAGE_ROOT).as_posix() for path in SCHEMA_DIR.glob("*.json")
    }
    actual_template_paths = {
        path.relative_to(PACKAGE_ROOT).as_posix()
        for path in (PACKAGE_ROOT / "templates").glob("*")
        if path.is_file()
    }
    if not actual_schema_paths <= manifest_paths:
        raise ValueError("one or more schemas are absent from PACKAGE_MANIFEST.json")
    if not actual_template_paths <= manifest_paths:
        raise ValueError("one or more templates are absent from PACKAGE_MANIFEST.json")

    return {
        "agent_ids": sorted(expected_ids),
        "gate_count": len(review_gates["gates"]),
        "prompt_count": len(prompt_files),
        "schema_count": len(actual_schema_paths),
        "template_count": len(actual_template_paths),
    }


def dependency_record() -> dict[str, Any]:
    return {
        "generated_at": now_utc(),
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "platform": platform.platform(),
        "packages": {
            "jsonschema": package_version("jsonschema"),
            "jsonschema-specifications": package_version("jsonschema-specifications"),
            "referencing": package_version("referencing"),
            "rpds-py": package_version("rpds-py"),
        },
        "tools": {
            "git": git_value("--version"),
            "codex": subprocess.run(
                ["codex", "--version"], check=False, capture_output=True, text=True
            ).stdout.strip(),
        },
    }


def write_outputs(validation: Validation) -> None:
    completed_at = now_utc()
    dependency = dependency_record()
    DEPENDENCY_PATH.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    command_lines = [
        "# Installed system validation command log",
        f"started_at={validation.started_at}",
        f"completed_at={completed_at}",
        f"validator={SCRIPT_PATH.relative_to(REPO_ROOT)}",
        f"python={sys.executable}",
        f"argv={json.dumps(sys.argv)}",
        "",
    ]
    for index, entry in enumerate(validation.commands, start=1):
        command_lines.extend(
            [
                f"## command {index}",
                f"cwd={entry['cwd']}",
                f"command={json.dumps(entry['command'])}",
                f"return_code={entry['return_code']}",
                "stdout:",
                entry["stdout"].rstrip(),
                "stderr:",
                entry["stderr"].rstrip(),
                "",
            ]
        )
    COMMAND_LOG_PATH.write_text("\n".join(command_lines).rstrip() + "\n", encoding="utf-8")

    pass_count = sum(item["status"] == "PASS" for item in validation.checks)
    fail_count = len(validation.failures)
    status = "PASS" if fail_count == 0 else "FAIL"
    result = {
        "validation_id": "ES-INSTALLED-SYSTEM-VALIDATION-V1.0.0",
        "started_at": validation.started_at,
        "completed_at": completed_at,
        "repository_commit": git_value("rev-parse", "HEAD"),
        "repository_branch": git_value("branch", "--show-current"),
        "status": status,
        "summary": {
            "checks": len(validation.checks),
            "passed": pass_count,
            "failed": fail_count,
        },
        "checks": validation.checks,
        "limitations": validation.limitations,
        "artifacts": {
            "report": REPORT_PATH.relative_to(REPO_ROOT).as_posix(),
            "result": RESULT_PATH.relative_to(REPO_ROOT).as_posix(),
            "command_log": COMMAND_LOG_PATH.relative_to(REPO_ROOT).as_posix(),
            "dependencies": DEPENDENCY_PATH.relative_to(REPO_ROOT).as_posix(),
        },
    }
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report_lines = [
        "# Installed System Validation Report",
        "",
        f"**Result:** `{status}`",
        "",
        f"**Validation ID:** `{result['validation_id']}`",
        "",
        f"**Repository branch:** `{result['repository_branch']}`",
        "",
        f"**Repository commit at validation:** `{result['repository_commit']}`",
        "",
        f"**Completed:** `{completed_at}`",
        "",
        "## Validation results",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for item in validation.checks:
        detail = item["detail"].replace("|", "\\|").replace("\n", " ")
        report_lines.append(
            f"| `{item['check_id']}` {item['title']} | `{item['status']}` | {detail} |"
        )
    report_lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Checks: {len(validation.checks)}",
            f"- Passed: {pass_count}",
            f"- Failed: {fail_count}",
            "- Draft 2020-12 metaschema validation is distinct from JSON parsing and was run with the Python `jsonschema` implementation.",
            "- Package-manifest validation and exact ZIP-to-install byte comparison are distinct checks.",
            "",
            "## Dependency and command evidence",
            "",
            f"- `{DEPENDENCY_PATH.relative_to(REPO_ROOT)}`",
            f"- `{COMMAND_LOG_PATH.relative_to(REPO_ROOT)}`",
            "",
            "## Limitations",
            "",
        ]
    )
    report_lines.extend(f"- {item}" for item in validation.limitations)
    report_lines.extend(
        [
            "",
            "## Scope statement",
            "",
            "This report validates installation structure, sealed-package integrity, JSON Schema validity, supplied examples, and declared cross-file invariants. It does not start or simulate a substantive Founder-Orchestrated Review Cycle and does not issue a Founder disposition.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(report_lines), encoding="utf-8")


def main() -> int:
    os.chdir(REPO_ROOT)
    validation = Validation()

    validation.check("SRC-001", "Source ZIP SHA-256", check_zip_hash)
    validation.check("SRC-002", "Adjacent checksum file content", check_checksum_file)

    checksum_command = validation.run(["shasum", "-a", "256", "-c", CHECKSUM_PATH.name], SOURCE_PACKAGE_DIR)
    validation.check(
        "SRC-003",
        "Adjacent checksum command",
        lambda: (
            checksum_command.stdout.strip()
            if checksum_command.returncode == 0
            else (_ for _ in ()).throw(
                ValueError(checksum_command.stderr.strip() or checksum_command.stdout.strip())
            )
        ),
    )

    package_command = validation.run([sys.executable, str(PACKAGE_VALIDATOR_PATH)])
    validation.check(
        "PKG-001",
        "Package-controlled validator",
        lambda: (
            package_command.stdout.strip()
            if package_command.returncode == 0
            else (_ for _ in ()).throw(
                ValueError(package_command.stderr.strip() or package_command.stdout.strip())
            )
        ),
    )
    validation.check("PKG-002", "ZIP-to-install exact byte identity", check_archive_install_identity)
    validation.check("PKG-003", "Manifest-listed byte identity", validate_manifest_bytes)
    validation.check(
        "PKG-004",
        "Package manifest JSON Schema validation",
        lambda: validate_instance(MANIFEST_PATH, SCHEMA_DIR / "package_manifest.schema.json"),
    )

    validation.check(
        "AGT-000",
        "Calibration-only runtime canary controls",
        validate_runtime_canary,
    )
    agent_data = validation.check(
        "AGT-001",
        "Eight registered custom-agent TOMLs and controls",
        parse_and_validate_agents,
        lambda data: {
            "agent_count": len(data),
            "names": sorted(item["name"] for item in data.values()),
            "sandbox_modes": {
                item["name"]: item["sandbox_mode"] for item in data.values()
            },
        },
    )
    validation.check(
        "AGT-002",
        "Unique custom-agent names",
        lambda: (
            "8 unique names"
            if agent_data and len({item["name"] for item in agent_data.values()}) == 8
            else (_ for _ in ()).throw(ValueError("agent parsing or uniqueness failed"))
        ),
    )

    validation.check("SCH-001", "Draft 2020-12 metaschema and $ref validation", validate_schemas)
    validation.check("SCH-002", "All supplied JSON examples", validate_all_json_examples)
    validation.check(
        "SCH-003",
        "Sample Founder Review Authorization",
        lambda: validate_instance(
            PACKAGE_ROOT / "examples/EXAMPLE_REVIEW_AUTHORIZATION.json",
            SCHEMA_DIR / "review_authorization.schema.json",
        ),
    )

    validation.check(
        "XFL-001",
        "Cross-file registry, policy, gate, version, role, prompt, schema, and template consistency",
        lambda: validate_cross_file_consistency(agent_data or {}),
    )
    validation.check(
        "CFG-001",
        "Project agent concurrency configuration",
        lambda: (
            "max_threads=6 max_depth=1"
            if tomllib.loads((REPO_ROOT / ".codex/config.toml").read_text(encoding="utf-8"))
            == {"agents": {"max_threads": 6, "max_depth": 1}}
            else (_ for _ in ()).throw(ValueError("unexpected .codex/config.toml content"))
        ),
    )
    validation.check(
        "GOV-001",
        "Source package and locked installation commit ancestry",
        lambda: (
            f"HEAD descends from {EXPECTED_SOURCE_COMMIT}"
            if subprocess.run(
                ["git", "merge-base", "--is-ancestor", EXPECTED_SOURCE_COMMIT, "HEAD"],
                cwd=REPO_ROOT,
                check=False,
            ).returncode
            == 0
            else (_ for _ in ()).throw(ValueError("installation commit is not an ancestor of HEAD"))
        ),
    )

    write_outputs(validation)
    print(f"INSTALLED SYSTEM VALIDATION {'PASSED' if not validation.failures else 'FAILED'}")
    print(f"report={REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"result={RESULT_PATH.relative_to(REPO_ROOT)}")
    return 0 if not validation.failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
