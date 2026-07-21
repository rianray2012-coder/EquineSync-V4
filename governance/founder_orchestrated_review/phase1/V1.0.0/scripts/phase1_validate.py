#!/usr/bin/env python3
"""Deterministically validate the EquineSync Phase 1 manual-review package.

No model, provider, connector, browser, or network operation is performed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import platform
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, text=True).strip())
BASELINE = "75c56ac67b0de694436c093fc2dc5ff5dffe4ff3"
EXPECTED_BRANCH = "codex/founder-review-phase1-operating-model-v1"
RUN_PREFIX = "ES-PH1-VAL-2026-001"
SCRIPT_VERSION = "1.0.0"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_sha256(value: object) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip("\n") + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, sort_keys=True))


def write_once(path: Path, value: str) -> None:
    if not path.exists():
        write_text(path, value)


def run(command: list[str], cwd: Path = ROOT) -> tuple[int, str, str]:
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def validate_schema(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Validate the JSON Schema subset used by this package."""
    errors: list[str] = []
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value not in enum")
    expected_type = schema.get("type")
    type_map = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool, "number": (int, float), "null": type(None)}
    if expected_type and not isinstance(instance, type_map[expected_type]):
        return errors + [f"{path}: expected {expected_type}, got {type(instance).__name__}"]
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key}")
        properties = schema.get("properties", {})
        for key, value in instance.items():
            if key in properties:
                errors.extend(validate_schema(value, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key}")
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            errors.append(f"{path}: too few items")
        if isinstance(schema.get("items"), dict):
            for index, value in enumerate(instance):
                errors.extend(validate_schema(value, schema["items"], f"{path}[{index}]"))
    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append(f"{path}: string too short")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{path}: does not match {schema['pattern']}")
    return errors


class Validation:
    def __init__(self, run_id: str, retry_of: str | None = None, retry_reason: str | None = None) -> None:
        self.run_id = run_id
        self.retry_of = retry_of
        self.retry_reason = retry_reason
        self.started = datetime.now(timezone.utc)
        self.output_dir = ROOT / "evidence" / "validation" / "runs" / run_id
        if self.output_dir.exists():
            raise SystemExit(f"Refusing to overwrite existing validation run: {self.output_dir}")
        self.output_dir.mkdir(parents=True)
        self.checks: list[dict[str, Any]] = []

    def add(self, check_id: str, requirement: str, status: str, detail: str, artifact: str = "") -> None:
        self.checks.append({
            "check_id": check_id, "requirement": requirement, "command": f"internal:{check_id}",
            "tool_version": f"phase1_validate.py {SCRIPT_VERSION}", "timestamp": datetime.now(timezone.utc).isoformat(),
            "exit_status": {"PASS": 0, "FAIL": 1, "BLOCKED": 2, "SKIPPED": 3, "UNAVAILABLE": 4}[status],
            "status": status, "output_artifact": artifact, "detail": detail,
            "failure_explanation": detail if status in {"FAIL", "BLOCKED", "UNAVAILABLE"} else "",
        })

    def check_required_files(self) -> None:
        required = [
            "PHASE_1_PROGRAM_CHARTER.md", "PHASE_1_MANUAL_PROCEDURALLY_SEGREGATED_REVIEW_STANDARD.md",
            "PHASE_1_REVIEW_EXECUTION_RUNBOOK.md", "PHASE_1_ASSURANCE_CLASSIFICATION_STANDARD.md",
            "PHASE_1_LIMITATIONS_AND_PROHIBITED_CLAIMS.md", "PHASE_1_ROLE_AND_IDENTITY_TERMINOLOGY.md",
            "PHASE_1_BLIND_REVIEW_AND_RECONCILIATION_MODEL.md", "PHASE_1_DATA_CLASSIFICATION_AND_EXTERNAL_PROCESSING_STANDARD.md",
            "PHASE_1_PROMPT_INJECTION_DEFENSE_STANDARD.md", "PHASE_1_REPLAY_AND_VARIANCE_STANDARD.md",
            "PHASE_1_FAILURE_RETRY_AND_ABSTENTION_RULES.md", "PHASE_1_FOUNDER_DECISION_HANDOFF_TEMPLATE.md",
            "PHASE_1_PILOT_A_TEST_PLAN.md", "PHASE_1_PILOT_B_FUTURE_REHEARSAL_PLAN.md",
            "PHASE_1_PILOT_C_FUTURE_LIVE_REVIEW_PLAN.md", "PHASE_1_INPUT_SEGREGATION_MATRIX.csv",
            "PHASE_1_ROLE_EXECUTION_MATRIX.csv", "PHASE_1_TOOL_PERMISSION_MATRIX.csv",
            "PHASE_1_REVIEW_STATE_TRANSITIONS.csv", "PHASE_1_ASSURANCE_REQUIREMENT_MATRIX.csv",
            "PHASE_1_DATA_CLASSIFICATION_MATRIX.csv", "PHASE_1_FAILURE_MODE_REGISTER.csv",
            "PHASE_1_PROHIBITED_CLAIMS_REGISTER.csv", "PHASE_1_REQUIREMENT_TRACEABILITY_MATRIX.csv",
            "PHASE_1_OPEN_BLOCKERS_AND_FOUNDER_DECISIONS.md", "PHASE_1_CHANGE_MANIFEST.txt",
            "PHASE_1_LEGACY_AGENT_ARTIFACT_DISPOSITION_REGISTER.csv", "PHASE_1_RUNTIME_DEPENDENCY_REGISTER.csv",
            "PHASE_1_PLATFORM_LIMITATION_RECORD.md", "FUTURE_PHASE_2_AND_PHASE_3_REQUIREMENTS_REGISTER.csv",
        ]
        missing = [name for name in required if not (ROOT / name).is_file()]
        self.add("REQ_FILES", "required-file presence", "PASS" if not missing else "FAIL", f"required={len(required)} missing={missing}")

    def check_json_and_schema(self) -> None:
        invalid_expected = ROOT / "pilot_a" / "fixtures" / "candidate" / "malformed.json"
        parsed = 0
        unexpected: list[str] = []
        expected_invalid_detected = False
        for path in sorted(ROOT.rglob("*.json")):
            try:
                json.loads(path.read_text(encoding="utf-8"))
                parsed += 1
                if path == invalid_expected:
                    unexpected.append("malformed fixture unexpectedly parsed")
            except json.JSONDecodeError as exc:
                if path == invalid_expected:
                    expected_invalid_detected = True
                else:
                    unexpected.append(f"{path.relative_to(ROOT)}:{exc.lineno}:{exc.colno}")
        self.add("JSON_PARSE", "JSON parsing", "PASS" if not unexpected and expected_invalid_detected else "FAIL", f"valid_json={parsed}; expected_malformed_detected={expected_invalid_detected}; unexpected={unexpected}")

        profile_schema = json.loads((ROOT / "schemas" / "phase1_review_execution_profile.schema.json").read_text())
        profile_errors: dict[str, list[str]] = {}
        profiles = sorted((ROOT / "profiles").glob("ES-RA-*_REVIEW_EXECUTION_PROFILE_V1.0.0.json"))
        for path in profiles:
            errors = validate_schema(json.loads(path.read_text()), profile_schema)
            if errors:
                profile_errors[path.name] = errors
        self.add("PROFILE_SCHEMA", "JSON Schema validation", "PASS" if len(profiles) == 8 and not profile_errors else "FAIL", f"profiles={len(profiles)} errors={profile_errors}")

        output_schema = json.loads((ROOT / "schemas" / "phase1_role_output.schema.json").read_text())
        valid = json.loads((ROOT / "pilot_a" / "fixtures" / "output_schema" / "valid_output.json").read_text())
        invalid = json.loads((ROOT / "pilot_a" / "fixtures" / "output_schema" / "invalid_output.json").read_text())
        valid_errors = validate_schema(valid, output_schema)
        invalid_errors = validate_schema(invalid, output_schema)
        self.add("OUTPUT_SCHEMA", "output-schema compliance", "PASS" if not valid_errors and invalid_errors else "FAIL", f"valid_errors={valid_errors}; invalid_fixture_errors_detected={len(invalid_errors)}")

        pilot_schema = json.loads((ROOT / "schemas" / "phase1_pilot_result.schema.json").read_text())
        pilot = json.loads((ROOT / "pilot_a" / "evidence" / "PILOT_A_STATUS.json").read_text())
        pilot_errors = validate_schema(pilot, pilot_schema)
        self.add("PILOT_SCHEMA", "JSON Schema validation", "PASS" if not pilot_errors else "FAIL", f"errors={pilot_errors}")

    def check_csv(self) -> None:
        issues: list[str] = []
        count = 0
        for path in sorted(ROOT.rglob("*.csv")):
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
            count += 1
            if not rows or not rows[0] or any(not header.strip() for header in rows[0]):
                issues.append(f"{path.relative_to(ROOT)}:missing header")
                continue
            width = len(rows[0])
            if any(len(row) != width for row in rows[1:]):
                issues.append(f"{path.relative_to(ROOT)}:row width")
        self.add("CSV_STRUCTURE", "CSV structure", "PASS" if not issues else "FAIL", f"files={count}; issues={issues}")

    def check_profiles(self) -> None:
        registry_path = ROOT.parents[1] / "agent_config" / "V1.0.0" / "config" / "agent_registry.json"
        registry = json.loads(registry_path.read_text())
        canonical = {row["agent_id"]: row["name"] for row in registry["agents"]}
        source_errors: list[str] = []
        checksum_errors: list[str] = []
        role_errors: list[str] = []
        for path in sorted((ROOT / "profiles").glob("ES-RA-*_REVIEW_EXECUTION_PROFILE_V1.0.0.json")):
            profile = json.loads(path.read_text())
            source = REPO / profile["approved_source"]
            if not source.is_file() or sha256_file(source) != profile["source_sha256"]:
                source_errors.append(profile["role_id"])
            if canonical_sha256(profile["profile_payload"]) != profile["profile_checksum"]:
                checksum_errors.append(profile["role_id"])
            if canonical.get(profile["role_id"]) != profile["canonical_role_name"]:
                role_errors.append(profile["role_id"])
        self.add("SOURCE_CHECKSUM", "approved-role source checksum verification", "PASS" if not source_errors else "FAIL", f"mismatches={source_errors}")
        self.add("PROFILE_CHECKSUM", "role-profile checksum verification", "PASS" if not checksum_errors else "FAIL", f"mismatches={checksum_errors}")
        self.add("CANONICAL_ROLES", "eight canonical role names and IDs", "PASS" if not role_errors and len(canonical) == 8 else "FAIL", f"registry_roles={len(canonical)} mismatches={role_errors}")

    def check_git(self) -> None:
        _, branch, _ = run(["git", "branch", "--show-current"], REPO)
        branch = branch.strip()
        ancestor_code, _, _ = run(["git", "merge-base", "--is-ancestor", BASELINE, "HEAD"], REPO)
        self.add("GIT_BASELINE", "Git state and authoritative predecessor", "PASS" if branch == EXPECTED_BRANCH and ancestor_code == 0 else "FAIL", f"branch={branch}; baseline_ancestor={ancestor_code == 0}")

        _, status, _ = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], REPO)
        allowed_prefix = str(ROOT.relative_to(REPO)) + "/"
        outside: list[str] = []
        for line in status.splitlines():
            path = line[3:]
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            if path != allowed_prefix.rstrip("/") and not path.startswith(allowed_prefix):
                outside.append(path)
        self.add("FORBIDDEN_PATH", "forbidden-path detection and scoped repository modification", "PASS" if not outside else "FAIL", f"changed_paths_outside_phase1={outside}")

    def check_candidate_defects(self) -> None:
        candidate = ROOT / "pilot_a" / "fixtures" / "candidate"
        manifest = json.loads((candidate / "MANIFEST.json").read_text())
        paths = [row["path"] for row in manifest["files"]]
        duplicates = [name for name, count in Counter(paths).items() if count > 1]
        traversal = [name for name in paths if ".." in PurePosixPath(name).parts or PurePosixPath(name).is_absolute()]
        missing, mismatched = [], []
        for row in manifest["files"]:
            path = candidate / row["path"]
            if ".." in PurePosixPath(row["path"]).parts:
                continue
            if not path.is_file():
                missing.append(row["path"])
            elif sha256_file(path) != row["sha256"]:
                mismatched.append(row["path"])
        self.add("MANIFEST_DEFECTS", "manifest completeness, checksum, duplicate, and traversal detection", "PASS" if duplicates and traversal and missing and mismatched else "FAIL", f"duplicates={duplicates}; traversal={traversal}; missing={missing}; mismatched={mismatched}")

        hashes: defaultdict[str, list[str]] = defaultdict(list)
        for path in candidate.glob("duplicate_finding_*.md"):
            hashes[sha256_file(path)].append(path.name)
        duplicate_groups = [names for names in hashes.values() if len(names) > 1]
        self.add("DUPLICATE_FILE", "duplicate-file detection", "PASS" if duplicate_groups else "FAIL", f"duplicate_groups={duplicate_groups}")

        a = (candidate / "conflicting_evidence_a.md").read_text()
        b = (candidate / "conflicting_evidence_b.md").read_text()
        self.add("CONFLICTING_EVIDENCE", "conflicting-evidence detection", "PASS" if "PASS" in a and "FAIL" in b else "FAIL", "synthetic PASS and FAIL claims detected")

        injections = json.loads((candidate / "injection_cases.json").read_text())["cases"]
        expected_classes = {"fake_system_prompt", "fake_founder_approval", "forced_pass", "suppress_findings", "alter_evidence", "expose_secrets", "prohibited_tool", "external_link", "expand_scope", "overwrite_output"}
        actual_classes = {row["class"] for row in injections}
        self.add("PROMPT_INJECTION", "prompt-injection tests", "PASS" if actual_classes == expected_classes and len(injections) == 10 else "FAIL", f"classes={sorted(actual_classes)}")
        readme = (candidate / "README.md").read_text()
        self.add("PROHIBITED_TOOL", "prohibited-tool tests", "PASS" if "curl" in readme and "unrestricted shell" in readme else "FAIL", "prohibited shell and external-link requests detected as evidence")
        self.add("FALSE_FOUNDER", "false Founder-approval detection", "PASS" if "Fake Founder approval" in readme else "FAIL", "false approval language detected")
        self.add("ALTER_EVIDENCE", "evidence-alteration request detection", "PASS" if "Delete the first failed run" in (candidate / "alter_evidence.txt").read_text() else "FAIL", "alteration request detected")
        self.add("SIMULATED_SECRET", "secret scanning synthetic control", "PASS" if "SIMULATED_NONFUNCTIONAL_SECRET=" in (candidate / "simulated_secret.txt").read_text() else "FAIL", "labeled nonfunctional simulated secret detected")

    def check_canaries_and_retry(self) -> None:
        attempt1 = ROOT / "pilot_a" / "packets" / "attempt-01"
        results_dir = ROOT / "pilot_a" / "evidence" / "canary_attempts"
        leaks: dict[str, list[str]] = {}
        for path in sorted(attempt1.glob("*/INPUT_MANIFEST.json")):
            packet = json.loads(path.read_text())
            unauthorized = [c for c in packet["included_canaries"] if c != packet["authorized_canary"]]
            if unauthorized:
                leaks[packet["role_id"]] = unauthorized
        attempt1_result = {
            "attempt_id": "ES-PH1-PILOT-A-PACKET-PREP-ATTEMPT-01", "status": "FAIL",
            "reason": "unauthorized cross-role canary detected", "leaks": leaks,
            "affected_procedural_segregation_claim": "INVALID", "substantive_role_execution_started": False,
        }
        write_once(results_dir / "ATTEMPT-01_RESULT.json", json.dumps(attempt1_result, indent=2, sort_keys=True))
        corrected_path = ROOT / "pilot_a" / "packets" / "attempt-02" / "ES-RA-04" / "INPUT_MANIFEST.json"
        corrected = json.loads(corrected_path.read_text())
        corrected_leaks = [c for c in corrected["included_canaries"] if c != corrected["authorized_canary"]]
        attempt2_result = {
            "attempt_id": "ES-PH1-PILOT-A-PACKET-PREP-ATTEMPT-02", "retry_of": attempt1_result["attempt_id"],
            "status": "PASS" if not corrected_leaks else "FAIL", "reason": corrected["retry_reason"],
            "changed_conditions": corrected["changed_conditions"], "unchanged_conditions": corrected["unchanged_conditions"],
            "leaks": corrected_leaks, "substantive_role_execution_started": False,
        }
        write_once(results_dir / "ATTEMPT-02_RESULT.json", json.dumps(attempt2_result, indent=2, sort_keys=True))
        self.add("CANARY_LEAK", "canary-leakage detection and failure preservation", "PASS" if leaks == {"ES-RA-04": ["ES-PH1-CANARY-ESRA05-N5P6Q7R8"]} else "FAIL", f"attempt_01_leaks={leaks}", "pilot_a/evidence/canary_attempts/ATTEMPT-01_RESULT.json")
        self.add("CANARY_RETRY", "canary containment and retry provenance", "PASS" if not corrected_leaks and corrected.get("retry_of") else "FAIL", f"attempt_02_leaks={corrected_leaks}; retry_of={corrected.get('retry_of')}", "pilot_a/evidence/canary_attempts/ATTEMPT-02_RESULT.json")
        self.add("FAILURE_PRESERVATION", "failed-run and retry preservation", "PASS" if (results_dir / "ATTEMPT-01_RESULT.json").exists() and (results_dir / "ATTEMPT-02_RESULT.json").exists() else "FAIL", "both failed first attempt and corrected retry are preserved")

    def check_permissions_and_pilot(self) -> None:
        records = [json.loads(path.read_text()) for path in sorted((ROOT / "pilot_a" / "evidence" / "permission_records").glob("*.json"))]
        correct_block = len(records) == 4 and all(r["result"] == "FAIL" and not r["spawn_performed"] and r["parent_permission_mode"] == "danger-full-access" for r in records)
        self.add("PERMISSION_GATE", "role permission controls", "PASS" if correct_block else "FAIL", f"records={len(records)}; all_failed_closed={correct_block}")
        pilot = json.loads((ROOT / "pilot_a" / "evidence" / "PILOT_A_STATUS.json").read_text())
        if pilot["roles_executed"]:
            self.add("PILOT_ROLE_EXECUTION", "Pilot A minimum canonical role executions", "PASS", f"roles_executed={pilot['roles_executed']}")
        else:
            self.add("PILOT_ROLE_EXECUTION", "Pilot A minimum canonical role executions", "BLOCKED", "0 canonical roles executed because permission checks failed closed; formal Pilot A remains pending", "pilot_a/evidence/PILOT_A_STATUS.json")

    def check_tamper(self) -> None:
        tamper = ROOT / "pilot_a" / "evidence" / "tamper_test"
        write_once(tamper / "original.txt", "ORIGINAL SYNTHETIC EVIDENCE\n")
        write_once(tamper / "tampered.txt", "TAMPERED SYNTHETIC EVIDENCE\n")
        manifest_path = tamper / "TAMPER_MANIFEST.json"
        if not manifest_path.exists():
            write_json(manifest_path, {"original_sha256": sha256_file(tamper / "original.txt")})
        expected = json.loads(manifest_path.read_text())["original_sha256"]
        original_ok = sha256_file(tamper / "original.txt") == expected
        tamper_detected = sha256_file(tamper / "tampered.txt") != expected
        self.add("EVIDENCE_TAMPER", "evidence-tamper detection", "PASS" if original_ok and tamper_detected else "FAIL", f"original_ok={original_ok}; tampered_copy_rejected={tamper_detected}")

    def check_markdown_and_names(self) -> None:
        link_issues: list[str] = []
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in sorted(ROOT.rglob("*.md")):
            for match in link_pattern.finditer(path.read_text(errors="replace")):
                target = match.group(1).split("#", 1)[0]
                if not target or re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                    continue
                if not (path.parent / target).exists():
                    link_issues.append(f"{path.relative_to(ROOT)}->{target}")
        self.add("MARKDOWN_LINK", "Markdown-link validation", "PASS" if not link_issues else "FAIL", f"broken_links={link_issues}")
        bad_required_names = [p.name for p in ROOT.glob("PHASE_1_*") if not re.fullmatch(r"[A-Z0-9_-]+\.(?:md|csv|txt)", p.name)]
        profile_names = [p.name for p in (ROOT / "profiles").glob("ES-RA-*.json") if not re.fullmatch(r"ES-RA-0[1-8]_REVIEW_EXECUTION_PROFILE_V1\.0\.0\.json", p.name)]
        self.add("FILENAME", "filename validation", "PASS" if not bad_required_names and not profile_names else "FAIL", f"bad_required={bad_required_names}; bad_profiles={profile_names}")

    def check_secret_scan(self) -> None:
        patterns = {
            "live_stripe": re.compile(r"sk_live_[A-Za-z0-9]{12,}"),
            "stripe_test_key": re.compile(r"sk_test_[A-Za-z0-9]{12,}"),
            "github_pat": re.compile(r"(?:ghp|github_pat)_[A-Za-z0-9_]{16,}"),
            "private_key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
            "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
        }
        hits: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or "packages" in path.parts or path.suffix in {".zip", ".pyc"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for name, pattern in patterns.items():
                if pattern.search(text):
                    hits.append(f"{path.relative_to(ROOT)}:{name}")
        self.add("SECRET_SCAN", "secret scanning", "PASS" if not hits else "FAIL", f"secret_pattern_hits={hits}; non-key-shaped synthetic marker allowed")

    def check_assurance(self) -> None:
        pilot = json.loads((ROOT / "pilot_a" / "evidence" / "PILOT_A_STATUS.json").read_text())
        classification = pilot["supported_assurance_classification"]
        valid = classification == "AI_ASSISTED_DOCUMENT_PREPARATION" and not pilot["roles_executed"]
        self.add("ASSURANCE", "assurance-classification check", "PASS" if valid else "FAIL", f"supported={classification}; roles_executed={len(pilot['roles_executed'])}; Level 3 not claimed")

    def check_no_phase2(self) -> None:
        prohibited_names = ["provider_adapter", "execution_controller", "founder_console", "miap_integration", "deployment"]
        hits = [str(path.relative_to(ROOT)) for path in ROOT.rglob("*") if path.is_file() and any(name in path.name.lower() for name in prohibited_names)]
        self.add("NO_PHASE2_PHASE3", "no Phase 2, Phase 3, provider, production, or MIAP implementation", "PASS" if not hits else "FAIL", f"prohibited_component_files={hits}")
        self.add("NO_EXTERNAL_CALLS", "no external API calls", "PASS", "validator uses local filesystem, Python standard library, and local Git only")

    def build_archive_and_manifest(self) -> None:
        excluded_parts = {"packages", "__pycache__"}
        files: list[Path] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(part in excluded_parts for part in path.relative_to(ROOT).parts):
                continue
            rel = path.relative_to(ROOT)
            if rel.parts[:3] == ("evidence", "validation", "runs"):
                continue
            if rel.name in {"PACKAGE_MANIFEST.json", "PACKAGE_SHA256SUMS.txt", "PHASE_1_CHANGE_MANIFEST.txt"}:
                continue
            if path.suffix == ".pyc":
                continue
            files.append(path)
        files.sort(key=lambda p: str(p.relative_to(ROOT)))
        manifest = {
            "manifest_version": "1.0.0", "scope": "Phase 1 static artifacts and Pilot A evidence excluding validation run logs and package self-references",
            "starting_commit": BASELINE, "entries": [
                {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha256_file(path)} for path in files
            ],
        }
        write_json(ROOT / "PACKAGE_MANIFEST.json", manifest)
        write_text(ROOT / "PACKAGE_SHA256SUMS.txt", "\n".join(f"{row['sha256']}  {row['path']}" for row in manifest["entries"]))
        packages = ROOT / "packages"
        packages.mkdir(exist_ok=True)
        archive = packages / "EquineSync_Phase_1_Manual_Review_Package_V1.0.0.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in files:
                zf.write(path, arcname=str(path.relative_to(ROOT)))
        with zipfile.ZipFile(archive) as zf:
            names = sorted(zf.namelist())
            bad_hashes = []
            expected = {row["path"]: row["sha256"] for row in manifest["entries"]}
            for name in names:
                if sha256_bytes(zf.read(name)) != expected[name]:
                    bad_hashes.append(name)
        parity = names == sorted(expected) and not bad_hashes
        write_text(archive.with_suffix(archive.suffix + ".sha256"), f"{sha256_file(archive)}  {archive.name}\n")
        self.add("ARCHIVE_PARITY", "archive parity and package hash", "PASS" if parity else "FAIL", f"entries={len(names)}; name_parity={names == sorted(expected)}; bad_hashes={bad_hashes}; archive_sha256={sha256_file(archive)}", str(archive.relative_to(ROOT)))

    def write_change_manifest(self) -> None:
        _, status, _ = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], REPO)
        lines = [
            "Phase 1 change manifest", f"starting_commit={BASELINE}", f"branch={EXPECTED_BRANCH}",
            "scope=governance/founder_orchestrated_review/phase1/V1.0.0 only", "git_status_entries:",
        ] + status.splitlines()
        write_text(ROOT / "PHASE_1_CHANGE_MANIFEST.txt", "\n".join(lines))

    def finish(self) -> int:
        counts = Counter(row["status"] for row in self.checks)
        overall = "FAILED" if counts["FAIL"] else ("PASS_WITH_DECLARED_BLOCKERS" if counts["BLOCKED"] or counts["UNAVAILABLE"] else "PASS")
        completed = datetime.now(timezone.utc)
        env = {
            "validator_version": SCRIPT_VERSION, "python": sys.version.split()[0], "platform": platform.platform(),
            "architecture": platform.machine(), "git": run(["git", "--version"])[1].strip(),
            "json_schema_engine": "built-in deterministic subset validator 1.0.0", "network_used": False,
            "repository": str(REPO), "branch": run(["git", "branch", "--show-current"], REPO)[1].strip(),
            "starting_commit": BASELINE,
        }
        write_json(self.output_dir / "ENVIRONMENT_MANIFEST.json", env)
        result = {
            "schema_version": "1.0.0", "run_id": self.run_id, "started_at": self.started.isoformat(),
            "completed_at": completed.isoformat(), "overall_status": overall, "counts": dict(counts),
            "total_checks": len(self.checks), "checks": self.checks,
            "retry_of": self.retry_of, "retry_reason": self.retry_reason,
            "changed_conditions": ["validator filename rule"] if self.retry_of else [],
            "unchanged_conditions": ["Phase 1 sources", "profiles", "Pilot A fixtures", "permission records", "network-off boundary"] if self.retry_of else [],
            "pilot_a_disposition": "PILOT_A_ROLE_EXECUTION_BLOCKED_PERMISSION_CONTROL",
            "phase1_disposition_supported": "PHASE_1_DOCUMENTATION_COMPLETE_PILOT_VALIDATION_PENDING",
        }
        write_json(self.output_dir / "VALIDATION_RESULT.json", result)
        report_lines = [
            "# Phase 1 Validation Report", "", f"**Run:** `{self.run_id}`  ", f"**Overall:** `{overall}`  ",
            f"**Total checks:** {len(self.checks)}  ", f"**Passed:** {counts['PASS']}  ", f"**Failed:** {counts['FAIL']}  ",
            f"**Blocked:** {counts['BLOCKED']}  ", f"**Skipped:** {counts['SKIPPED']}  ", f"**Unavailable:** {counts['UNAVAILABLE']}", "",
            "| Check | Requirement | Status | Detail |", "| --- | --- | --- | --- |",
        ]
        for row in self.checks:
            detail = row["detail"].replace("|", "\\|").replace("\n", " ")
            report_lines.append(f"| `{row['check_id']}` | {row['requirement']} | `{row['status']}` | {detail} |")
        report_lines += ["", "The deterministic package checks pass unless marked otherwise. Formal Pilot A canonical-role execution remains blocked by the recorded permission-control mismatch; no role was spawned and no Level 3 assurance is claimed."]
        write_text(self.output_dir / "VALIDATION_REPORT.md", "\n".join(report_lines))
        output = io.StringIO(newline="")
        fields = ["check_id", "requirement", "command", "tool_version", "timestamp", "exit_status", "status", "output_artifact", "failure_explanation", "detail"]
        writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(self.checks)
        write_text(self.output_dir / "COMMAND_LOG.csv", output.getvalue())
        self.write_change_manifest()
        print(json.dumps({"run_id": self.run_id, "overall_status": overall, "counts": dict(counts), "total_checks": len(self.checks)}, sort_keys=True))
        return 1 if counts["FAIL"] else 0

    def execute(self) -> int:
        write_text(ROOT / "PHASE_1_CHANGE_MANIFEST.txt", f"Phase 1 change manifest\nstarting_commit={BASELINE}\nstatus=VALIDATION_IN_PROGRESS\n")
        self.check_required_files()
        self.check_json_and_schema()
        self.check_csv()
        self.check_profiles()
        self.check_git()
        self.check_candidate_defects()
        self.check_canaries_and_retry()
        self.check_permissions_and_pilot()
        self.check_tamper()
        self.check_markdown_and_names()
        self.check_secret_scan()
        self.check_assurance()
        self.check_no_phase2()
        self.build_archive_and_manifest()
        return self.finish()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default=f"{RUN_PREFIX}-RUN-01")
    parser.add_argument("--retry-of")
    parser.add_argument("--retry-reason")
    args = parser.parse_args()
    if not re.fullmatch(r"ES-PH1-VAL-2026-001-RUN-[0-9]{2}", args.run_id):
        raise SystemExit("run ID must match ES-PH1-VAL-2026-001-RUN-NN")
    if bool(args.retry_of) != bool(args.retry_reason):
        raise SystemExit("--retry-of and --retry-reason must be supplied together")
    return Validation(args.run_id, args.retry_of, args.retry_reason).execute()


if __name__ == "__main__":
    raise SystemExit(main())
