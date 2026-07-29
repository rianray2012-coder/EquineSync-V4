#!/usr/bin/env python3
"""Validate the CGP-006 Wave 1 V1.1 adoption authority reconciliation package.

Version: 1.0.0
Owner: Codex
Reliability state: SHADOW_VALIDATION
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PACKAGE_REL = Path("governance/implementation/code-guides/drafting/CGP-006/WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION")
ROOT_REL = Path("governance/implementation/code-guides")
START_HEAD = "513458bd9f0f6b321407720d35521b239cdedb85"
PR42_HEAD = "83d8e3af9afa50a55af4b679016c2568c6d3c61d"
PR42_MERGE = "db4984ee8781534c8ad8731f89c7a882013cb592"
AUTHORITY_ID = "CGP-V11-AUTH-0005"
AFFECTED = {"ES-CG-00", "ES-CG-01", "ES-CG-10", "ES-CG-13"}
REQUIRED = [
    "README.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "FOUNDER_ADOPTION_AUTHORITY_DISPOSITION.md",
    "PR_42_HISTORICAL_AUTHORITY_ANALYSIS.md",
    "V1_1_ADOPTION_STATE_RECONCILIATION.md",
    "AUTHORITY_PRECEDENCE_AND_NON_RETROACTIVITY_RULE.md",
    "GUIDE_ADOPTION_STATE_MATRIX.csv",
    "ADOPTION_ASSERTION_INVENTORY.csv",
    "CURRENT_STATUS_CHANGE_REPORT.md",
    "HISTORICAL_RECORD_PRESERVATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "AUTHORITY_BOUNDARY_REPORT.md",
    "SOURCE_REGISTER.md",
    "VALIDATION_REPORT.md",
    "REVIEW_DISPOSITION.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validators/validate_adoption_authority_reconciliation.py",
    "tests/test_adoption_authority_reconciliation.py",
]
CLOSING = [
    "PROGRAM_PLAN_V1_1_CONTROLLING",
    "PR_42_HISTORICAL_CONDITIONAL_ADOPTION_PRESERVED",
    "PR_42_CONDITIONAL_ADOPTION_NOT_CARRIED_FORWARD_AS_V1_1_STAGE_22_ADOPTION",
    "CURRENT_WAVE_1_V1_1_ADOPTION_STATE_NOT_ADOPTED",
    "V1_1_LIFECYCLE_COMPLETION_REQUIRED_BEFORE_NEW_ADOPTION_DISPOSITION",
    "NO_RETROACTIVE_INVALIDATION_OF_PR_42",
    "GUIDE_ACTIVATION_NOT_AUTHORIZED",
    "NO_ACTIVATION_EFFECTIVE_DATE_ESTABLISHED",
    "REPOSITORY_SPECIFIC_IMPLEMENTATION_MAPPING_NOT_AUTHORIZED",
    "IMPLEMENTATION_NOT_AUTHORIZED",
    "DEPLOYMENT_NOT_AUTHORIZED",
    "PILOT_AND_PRODUCTION_USE_NOT_AUTHORIZED",
    "GAP_0004_REMAINS_OPEN",
    "RETAINED_WARNINGS_REMAIN_OPEN",
    "ACTIVATION_BLOCKERS_REMAIN_OPEN",
    "NO_ADOPTED_OR_CANDIDATE_GUIDE_BYTES_CHANGED",
    "NO_V1_1_LIFECYCLE_STATE_ADVANCEMENT_OCCURRED",
    "NO_RUNTIME_IMPLEMENTATION_OCCURRED",
    "CGP_007_NOT_AUTHORIZED",
]
SEARCH_TERMS = [
    "CONDITIONALLY_ADOPTED",
    "CONDITIONALLY_ADOPTED_PENDING_PROTECTED_INTEGRATION",
    "CONDITIONALLY_ADOPTED_AND_PROTECTEDLY_MERGED_NOT_ACTIVATED",
    "CONDITIONAL_PORTFOLIO_ADOPTION",
    "NOT_ADOPTED",
    "ADOPTED",
    "CGP006-W1-CAR-0001",
    "PR #42",
    "db4984ee8781534c8ad8731f89c7a882013cb592",
]
EXCLUDED_INVENTORY_FILES = {
    "ADOPTION_ASSERTION_INVENTORY.csv",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
}
PROHIBITED_PR42_TREATMENTS = [
    "PR_42_VOID",
    "PR_42_INVALID",
    "PR_42_REVOKED_AB_INITIO",
    "PR_42_UNAUTHORIZED_WHEN_ISSUED",
    "PR_42_ERASED",
    "PR_42_NEVER_EFFECTIVE",
    "PR #42 is void",
    "PR #42 is invalid",
    "PR #42 was unauthorized",
]
STAGE22_CLAIMS = [
    "PR_42_CONDITIONAL_ADOPTION_SATISFIES_V1_1_STAGE_22",
    "PR #42 satisfies V1.1 Stage 22",
    "PR #42 completed V1.1 Stage 22",
]


def repo_root() -> Path:
    return Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_files(package: Path, *, include_package_manifest: bool, include_checksum_manifest: bool) -> list[Path]:
    excluded = set()
    if not include_package_manifest:
        excluded.add("PACKAGE_MANIFEST.json")
    if not include_checksum_manifest:
        excluded.add("CHECKSUM_MANIFEST.sha256")
    return sorted(
        p
        for p in package.rglob("*")
        if p.is_file()
        and p.name not in excluded
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def changed_paths(repo: Path) -> list[str]:
    tracked = subprocess.check_output(["git", "diff", "--name-only", START_HEAD, "--"], cwd=repo, text=True).splitlines()
    untracked = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], cwd=repo, text=True).splitlines()
    return sorted(set(tracked + untracked))


def assert_required_files(package: Path) -> None:
    missing = [name for name in REQUIRED if not (package / name).is_file()]
    if missing:
        raise AssertionError(f"Missing reconciliation package files: {missing}")


def assert_closing_statements(package: Path, repo: Path) -> None:
    for rel in [
        package / "README.md",
        package / "FOUNDER_ADOPTION_AUTHORITY_DISPOSITION.md",
        package / "REVIEW_DISPOSITION.md",
        repo / ROOT_REL / "PROGRAM_STATUS.md",
        repo / ROOT_REL / "README.md",
    ]:
        text = rel.read_text(encoding="utf-8")
        missing = [item for item in CLOSING if item not in text]
        if missing:
            raise AssertionError(f"{rel} missing closing statements: {missing}")


def assert_pr42_lineage(repo: Path, package: Path) -> None:
    for commit in [PR42_HEAD, PR42_MERGE, START_HEAD]:
        subprocess.check_call(["git", "cat-file", "-e", f"{commit}^{{commit}}"], cwd=repo)
    for rel in ["DIRECTIVE_EXECUTION_RECORD.md", "FOUNDER_ADOPTION_AUTHORITY_DISPOSITION.md", "PR_42_HISTORICAL_AUTHORITY_ANALYSIS.md"]:
        text = (package / rel).read_text(encoding="utf-8")
        for token in [PR42_HEAD, PR42_MERGE, "CGP006-W1-CAR-0001"]:
            if token not in text:
                raise AssertionError(f"{rel} missing PR #42 lineage token {token}")


def assert_affected_tracker_states(rows: list[dict[str, str]]) -> None:
    by_id = {row.get("record_id"): row for row in rows}
    missing = sorted(AFFECTED - set(by_id))
    if missing:
        raise AssertionError(f"Affected guide tracker rows missing: {missing}")
    for guide in AFFECTED:
        row = by_id[guide]
        if row.get("adoption_state") != "NOT_ADOPTED":
            raise AssertionError(f"{guide} adoption_state is not NOT_ADOPTED: {row.get('adoption_state')}")
        combined = " ".join(row.values())
        if "CGP-007" in combined and "NOT_ISSUED" not in combined and "NOT_AUTHORIZED" not in combined:
            raise AssertionError(f"{guide} tracker row implies CGP-007 authority")


def assert_activation_states(rows: list[dict[str, str]]) -> None:
    by_id = {row.get("guide_id"): row for row in rows}
    missing = sorted(AFFECTED - set(by_id))
    if missing:
        raise AssertionError(f"Affected activation rows missing: {missing}")
    for guide in AFFECTED:
        row = by_id[guide]
        if row.get("activation_state") != "NOT_ACTIVE":
            raise AssertionError(f"{guide} activation_state is not NOT_ACTIVE: {row.get('activation_state')}")
        if row.get("effective_date") not in {"NONE", ""}:
            raise AssertionError(f"{guide} activation effective date introduced: {row.get('effective_date')}")
        if row.get("authority") != "GUIDE_ACTIVATION_NOT_AUTHORIZED":
            raise AssertionError(f"{guide} activation authority changed: {row.get('authority')}")


def assert_authority_register(rows: list[dict[str, str]]) -> None:
    matches = [row for row in rows if row.get("authority_id") == AUTHORITY_ID]
    if len(matches) != 1:
        raise AssertionError(f"Expected one {AUTHORITY_ID} row, found {len(matches)}")
    row = matches[0]
    if row.get("authority_type") != "ADOPTION_AUTHORITY_RECONCILIATION":
        raise AssertionError("Authority row has wrong authority_type")
    if row.get("status") not in {"APPROVED_PENDING_PROTECTED_INTEGRATION_AND_CUSTODY", "CUSTODY_COMPLETE_CONTROLLING"}:
        raise AssertionError(f"Authority row has invalid status: {row.get('status')}")
    prohibited = row.get("prohibited_effects", "")
    for token in ["Guide-content change", "adoption", "activation", "implementation mapping", "implementation", "deployment", "runtime evidence", "CGP-007"]:
        if token not in prohibited:
            raise AssertionError(f"Authority row missing prohibited effect: {token}")


def assert_no_prohibited_pr42_treatment(texts: list[str]) -> None:
    joined = "\n".join(texts)
    hits = [term for term in PROHIBITED_PR42_TREATMENTS if term in joined]
    if hits:
        raise AssertionError(f"Prohibited PR #42 treatment found: {hits}")


def assert_no_stage22_claim(texts: list[str]) -> None:
    joined = "\n".join(texts)
    hits = [term for term in STAGE22_CLAIMS if term in joined]
    if hits:
        raise AssertionError(f"PR #42 incorrectly claimed as V1.1 Stage 22 evidence: {hits}")


def assert_gap_warning_blocker_cgp007_open(texts: list[str]) -> None:
    joined = "\n".join(texts)
    prohibited = [
        "GAP_0004_CLOSED",
        "CGP005-TA-APP-GAP-0004,CLOSED",
        "RETAINED_WARNINGS_CLOSED",
        "CGP006-CLF-0001,CLOSED",
        "ACTIVATION_BLOCKERS_CLOSED",
        "CGP_007_ISSUED",
        "CGP-007 issued",
    ]
    hits = [term for term in prohibited if term in joined]
    if hits:
        raise AssertionError(f"Prohibited closure or issuance found: {hits}")


def assert_changed_paths_authorized(paths: list[str]) -> None:
    outside = [path for path in paths if not path.startswith(ROOT_REL.as_posix() + "/")]
    if outside:
        raise AssertionError(f"Changed paths outside authorized root: {outside}")
    historical = [
        path for path in paths
        if "WAVE_1_ADOPTION_READINESS_REVIEW_V1" in path
        or path.endswith("CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT.md")
        or path.endswith("CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION.md")
    ]
    if historical:
        raise AssertionError(f"Historical PR #42 files changed: {historical}")
    guide_changes = [path for path in paths if path.startswith((ROOT_REL / "guides").as_posix() + "/")]
    if guide_changes:
        raise AssertionError(f"Adopted or candidate guide bytes changed: {guide_changes}")
    source_changes = [path for path in paths if path.startswith((ROOT_REL / "source-accession").as_posix() + "/") or path.startswith((ROOT_REL / "source-freeze").as_posix() + "/")]
    if source_changes:
        raise AssertionError(f"Approved source or source-freeze bytes changed: {source_changes}")


def matching_terms(line: str) -> list[str]:
    normalized = line.replace("`", "")
    found = []
    for term in SEARCH_TERMS:
        if term == "PR #42":
            if "PR #42" in normalized:
                found.append(term)
        elif term in line:
            found.append(term)
    return found


def classify(rel: str, line: str) -> str:
    if "WAVE_1_V1_1_ADOPTION_AUTHORITY_RECONCILIATION" in rel:
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if rel in {"governance/implementation/code-guides/PROGRAM_STATUS.md", "governance/implementation/code-guides/README.md"}:
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if "/registers/CODE_GUIDE_AUTHORITY_REGISTER.csv" in rel or "/registers/CODE_GUIDE_PROGRAM_TRACKER.csv" in rel or "/registers/GUIDE_ACTIVATION_REGISTER.csv" in rel or "/registers/CODE_GUIDE_VERSION_REGISTER.csv" in rel or "/registers/GUIDE_SUPERSESSION_REGISTER.csv" in rel:
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if "CGP_006_WAVE_1_CONDITIONAL_ADOPTION_CUSTODY_RECEIPT" in rel or "CGP_006_WAVE_1_CONDITIONAL_ADOPTION_METADATA_RECONCILIATION" in rel:
        return "HISTORICAL_CUSTODY_RECORD_PRESERVE"
    if "WAVE_1_ADOPTION_READINESS_REVIEW_V1" in rel:
        if any(token in line for token in ["CONDITIONALLY_ADOPTED", "CONDITIONAL_PORTFOLIO_ADOPTION", "CGP006-W1-CAR-0001"]):
            return "HISTORICAL_PRE_V1_1_AUTHORITY_PRESERVE"
        return "HISTORICAL_PR_EVIDENCE_PRESERVE"
    if "CODE_GUIDE_PROGRAM_V1_1_POST_CUSTODY_CLOSEOUT_AND_STATUS_RECONCILIATION/STALE_STATUS_ASSERTION_INVENTORY.csv" in rel:
        return "HISTORICAL_PR_EVIDENCE_PRESERVE"
    if "/receipts/" in rel:
        return "HISTORICAL_CUSTODY_RECORD_PRESERVE"
    if "/program-plan/" in rel:
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if "/guides/" in rel and ("NOT_ADOPTED" in line or "NOT_ACTIVE" in line):
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if any(guide in line for guide in AFFECTED) and ("NOT_ADOPTED" in line or "NOT_ACTIVE" in line):
        return "CURRENT_V1_1_STATUS_CONTROLLING"
    if "PR #42" in line.replace("`", "") or PR42_MERGE in line or PR42_HEAD in line or "CGP006-W1-CAR-0001" in line:
        return "HISTORICAL_PR_EVIDENCE_PRESERVE"
    return "OUT_OF_SCOPE_CONTEXT_ONLY"


def compute_assertion_inventory(repo: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    root = repo / ROOT_REL
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if path.name in EXCLUDED_INVENTORY_FILES and PACKAGE_REL.as_posix() in path.as_posix():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = path.relative_to(repo).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            terms = matching_terms(line)
            if not terms:
                continue
            rows.append({
                "path": rel,
                "line": str(number),
                "matched_terms": ";".join(terms),
                "assertion_excerpt": line[:500],
                "classification": classify(rel, line),
                "rationale": "Classified by authority-reconciliation validator from path and assertion context.",
            })
    return rows


def assert_assertion_inventory(repo: Path, package: Path) -> None:
    actual = compute_assertion_inventory(repo)
    with (package / "ADOPTION_ASSERTION_INVENTORY.csv").open(newline="", encoding="utf-8") as handle:
        recorded = list(csv.DictReader(handle))
    actual_keys = {(r["path"], r["line"], r["matched_terms"], r["classification"]) for r in actual}
    recorded_keys = {(r["path"], r["line"], r["matched_terms"], r["classification"]) for r in recorded}
    if actual_keys != recorded_keys:
        missing = sorted(actual_keys - recorded_keys)[:10]
        extra = sorted(recorded_keys - actual_keys)[:10]
        raise AssertionError(f"Assertion inventory mismatch; missing={missing} extra={extra}")
    if not recorded:
        raise AssertionError("Assertion inventory is empty")
    if any(r["classification"] == "AMBIGUOUS_REQUIRES_MANUAL_REVIEW" for r in recorded):
        raise AssertionError("Assertion inventory contains ambiguous rows")
    for required in ["HISTORICAL_PRE_V1_1_AUTHORITY_PRESERVE", "HISTORICAL_PR_EVIDENCE_PRESERVE", "HISTORICAL_CUSTODY_RECORD_PRESERVE", "CURRENT_V1_1_STATUS_CONTROLLING"]:
        if not any(r["classification"] == required for r in recorded):
            raise AssertionError(f"Assertion inventory lacks classification {required}")


def assert_manifest_and_checksums(package: Path) -> None:
    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    expected = [
        p.relative_to(package).as_posix()
        for p in package_files(package, include_package_manifest=False, include_checksum_manifest=False)
    ]
    if [entry["path"] for entry in manifest["files"]] != expected:
        raise AssertionError("Package manifest path mismatch")
    for entry in manifest["files"]:
        if sha(package / entry["path"]) != entry["sha256"]:
            raise AssertionError(f"Package manifest checksum mismatch: {entry['path']}")
    lines = [line.strip() for line in (package / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if line.strip()]
    entries = {}
    for line in lines:
        parts = line.split("  ", 1)
        if len(parts) != 2:
            raise AssertionError(f"Malformed checksum manifest line: {line}")
        entries[parts[1]] = parts[0]
    expected_paths = [
        p.relative_to(package).as_posix()
        for p in package_files(package, include_package_manifest=True, include_checksum_manifest=False)
    ]
    if sorted(entries) != expected_paths:
        raise AssertionError("Checksum manifest path mismatch")
    for rel, digest in entries.items():
        if sha(package / rel) != digest:
            raise AssertionError(f"Checksum manifest digest mismatch: {rel}")


def validate() -> None:
    repo = repo_root()
    package = repo / PACKAGE_REL
    assert_required_files(package)
    assert_closing_statements(package, repo)
    assert_pr42_lineage(repo, package)
    assert_affected_tracker_states(read_csv(repo / ROOT_REL / "registers/CODE_GUIDE_PROGRAM_TRACKER.csv"))
    assert_activation_states(read_csv(repo / ROOT_REL / "registers/GUIDE_ACTIVATION_REGISTER.csv"))
    assert_authority_register(read_csv(repo / ROOT_REL / "registers/CODE_GUIDE_AUTHORITY_REGISTER.csv"))
    texts = []
    for rel in ["PROGRAM_STATUS.md", "README.md"]:
        texts.append((repo / ROOT_REL / rel).read_text(encoding="utf-8"))
    for path in package.rglob("*.md"):
        texts.append(path.read_text(encoding="utf-8"))
    assert_no_prohibited_pr42_treatment(texts)
    assert_no_stage22_claim(texts)
    assert_gap_warning_blocker_cgp007_open(texts)
    assert_changed_paths_authorized(changed_paths(repo))
    assert_assertion_inventory(repo, package)
    assert_manifest_and_checksums(package)
    print("Adoption authority reconciliation package validation passed.")


if __name__ == "__main__":
    try:
        validate()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
