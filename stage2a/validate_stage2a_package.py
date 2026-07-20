#!/usr/bin/env python3
"""Read-only machine validation for the Stage 2A successor package."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

import jsonschema
from jsonschema import Draft202012Validator, FormatChecker

PACKAGE_ID = "ES-PKG-2026-004-V003"
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
    "STAGE2A_VALIDATION_COMMAND_REGISTER.json", "STAGE2A_ENVIRONMENT_CONTRACT.json",
    "STAGE2A_RUNTIME_TOOLCHAIN_CONTRACT.json", "PROVIDER_DENIAL_REGISTER.json",
    "PROVIDER_DENIAL_REGISTER.csv", "STAGE2A_FIXTURE_FOUNDATION.json",
    "EXECUTION_EVIDENCE_SCHEMA.json", "CLEANUP_VALIDATION_REPORT.json",
    "ROLLBACK_REHEARSAL_REPORT.json", "STARTUP_SIDE_EFFECT_INVENTORY.json",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--phase", choices=("candidate", "final"), default="candidate")
    args = parser.parse_args()
    root = args.package.resolve()
    repo = Path(__file__).resolve().parents[1]
    checks: list[dict[str, object]] = []

    def ck(identifier: str, passed: bool, detail: object) -> None:
        checks.append({"check_id": identifier, "status": "PASS" if passed else "FAIL", "detail": detail})

    ck("MV-001-runtime", sys.version.split()[0] == "3.11.11" and jsonschema.__version__ == "4.26.0", {
        "python": sys.version.split()[0], "jsonschema": jsonschema.__version__,
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
        if name in {"SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json", "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.md", "validate_stage2a_package.py"}:
            continue
        text = (root / name).read_text(encoding="utf-8", errors="ignore")
        if "/Users/" in text or "/private/tmp/" in text:
            absolute_hits.append(name)
    ck("MV-009-local-path-boundary", not absolute_hits, {"unexpected_absolute_path_files": absolute_hits, "controlled_event_exemption": "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE"})
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
        candidate = repo / path
        if not candidate.is_file() or sha(candidate) != row.get("sha256"):
            source_errors.append(f"source hash mismatch {path}")
        if path.startswith("stage2a/"):
            try:
                blob = git(repo, "rev-parse", f"HEAD:{path}")
            except Exception:
                blob = ""
            if blob != row.get("git_blob"):
                source_errors.append(f"source blob mismatch {path}")
    ck("MV-011-source-register", not source_errors and bool(source_ids), {"rows": len(source_ids), "errors": source_errors})

    baseline_result = subprocess.run(["git", "cat-file", "-e", f"{BASELINE}^{{commit}}"], cwd=repo, capture_output=True)
    ck("MV-012-git-anchors", git(repo, "branch", "--show-current") == BRANCH and baseline_result.returncode == 0, {
        "branch": git(repo, "branch", "--show-current"), "head": git(repo, "rev-parse", "HEAD"), "start": START, "baseline": BASELINE,
    })
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
            core = dict(record); recorded = core.pop("record_content_sha256", "")
            actual = hashlib.sha256((json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()).hexdigest()
            if recorded != actual:
                evidence_errors.append(f"{name}: record hash mismatch")
    else:
        evidence_errors.append("missing schema")
    ck("MV-016-evidence-semantics", not evidence_errors, {"errors": evidence_errors})

    residue = json_objects.get("SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE.json", {})
    residue_ok = isinstance(residue, dict) and residue.get("event_classification") == "SEGREGATED_REVIEW_TEMPORARY_PROCESS_RESIDUE" and residue.get("termination", {}).get("scope") == "ONLY_VERIFIED_PROCESS_GROUP_62766" and residue.get("causal_relationship_to_runtime_limitation") == "NOT_ESTABLISHED_DO_NOT_CONFLATE"
    ck("MV-017-residue-provenance", residue_ok, residue)
    selector = json_objects.get("RUNTIME_AGENT_TYPE_SELECTOR_UNAVAILABLE.json", {})
    ck("MV-018-runtime-selector-limitation", isinstance(selector, dict) and selector.get("status") == "OPEN_BLOCKING_RUNTIME_LIMITATION" and selector.get("direct_evidence_of_resolution") is False, selector)

    manifest_name = "SUCCESSOR_PACKAGE_SHA256SUMS.txt" if args.phase == "final" else "DRAFT_REVIEW_SHA256SUMS.txt"
    manifest_errors: list[str] = []
    manifest_rows = 0
    if (root / manifest_name).is_file():
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
