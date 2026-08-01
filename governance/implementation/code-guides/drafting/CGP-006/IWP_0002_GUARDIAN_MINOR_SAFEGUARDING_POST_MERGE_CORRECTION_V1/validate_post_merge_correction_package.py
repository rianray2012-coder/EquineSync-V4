#!/usr/bin/env python3
"""Validate the CGP-006 IWP-0002 post-merge correction evidence package."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]

PACKAGE_ID = "CGP006-IWP0002-GUARDIAN-MINOR-SAFEGUARDING-POST-MERGE-CORRECTION-V1"
BASELINE = "12d5ae6faf3627bb0786af46de953fda808d7156"
DIRECTIVE_SHA = "094c39e51535f6f6dd4d3d4db370ad0485c490a308925848d6435513fc7047cd"

REQUIRED_FILES = {
    "README.md",
    "SOURCE_BASELINE_AND_DRIFT_RECORD.json",
    "FOUNDER_CORRECTIVE_AUTHORITY_RECORD.md",
    "POST_MERGE_FINDINGS_SOURCE_REGISTER.md",
    "AUTHORIZED_CORRECTIVE_PATHS.csv",
    "LEGACY_LINK_EXPANSION_CORRECTION_RECORD.md",
    "STATE_TOKEN_PROPAGATION_CORRECTION_RECORD.md",
    "FOCUSED_TEST_RESULTS.csv",
    "PRIOR_SAFEGUARD_REGRESSION_RESULTS.csv",
    "POSITIVE_CONTROL_RESULTS.csv",
    "CHANGE_AWARE_BYPASS_REVIEW.md",
    "REVIEW_FINDINGS_AND_DISPOSITION.csv",
    "VALIDATION_REPORT.md",
    "AUTHORIZED_PATH_REPORT.md",
    "ROLLBACK_AND_SUSPENSION_RECORD.md",
    "DIRECTIVE_EXECUTION_RECORD.md",
    "PACKAGE_MANIFEST.json",
    "CHECKSUM_MANIFEST.sha256",
    "validate_post_merge_correction_package.py",
    "test_validate_post_merge_correction_package.py",
}

AUTHORIZED_PREFIX = (
    "governance/implementation/code-guides/drafting/CGP-006/"
    "IWP_0002_GUARDIAN_MINOR_SAFEGUARDING_POST_MERGE_CORRECTION_V1/"
)

AUTHORIZED_PATHS = {
    "backend/core/minor_safety.py",
    "backend/core/minor_communication.py",
    "backend/routes/billing.py",
    "backend/routes/recurring_charges.py",
    "backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def digest(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def read_csv(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_text(path: Path, snippets: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            fail(f"{path.name} missing snippet: {snippet}")
    return text


def validate_package_files() -> None:
    found = {path.name for path in ROOT.iterdir() if path.is_file()}
    missing = REQUIRED_FILES - found
    if missing:
        fail(f"missing package files: {sorted(missing)}")

    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("package_id") != PACKAGE_ID:
        fail("unexpected package_id")
    if manifest.get("branch_baseline") != BASELINE:
        fail("unexpected branch baseline")
    expected_manifested = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file() and path.name not in {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256"}
    )
    if sorted(manifest.get("files", {}).keys()) != expected_manifested:
        fail("manifest file list mismatch")
    for name, meta in manifest["files"].items():
        sha, size = digest(ROOT / name)
        if sha != meta.get("sha256") or size != meta.get("bytes"):
            fail(f"manifest digest mismatch: {name}")

    checksum_lines = [
        line
        for line in (ROOT / "CHECKSUM_MANIFEST.sha256").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected_checksum_names = sorted(
        path.name for path in ROOT.iterdir() if path.is_file() and path.name != "CHECKSUM_MANIFEST.sha256"
    )
    actual_names: list[str] = []
    for line in checksum_lines:
        try:
            sha, name = line.split("  ", 1)
        except ValueError:
            fail(f"bad checksum line: {line}")
        actual_names.append(name)
        actual_sha, _ = digest(ROOT / name)
        if sha != actual_sha:
            fail(f"checksum digest mismatch: {name}")
    if sorted(actual_names) != expected_checksum_names:
        fail("checksum file list mismatch")


def validate_source_and_authority() -> None:
    record = json.loads((ROOT / "SOURCE_BASELINE_AND_DRIFT_RECORD.json").read_text(encoding="utf-8"))
    if record.get("package_id") != PACKAGE_ID:
        fail("source record package_id mismatch")
    if record.get("directive_identity", {}).get("sha256") != DIRECTIVE_SHA:
        fail("directive sha mismatch")
    if record.get("protected_head_refresh", {}).get("current_protected_head") != BASELINE:
        fail("current protected head mismatch")
    if record.get("protected_head_refresh", {}).get("drift_from_directive_head", {}).get("affected_product_or_test_paths_changed") is not False:
        fail("affected product path drift not cleared")
    require_text(
        ROOT / "FOUNDER_CORRECTIVE_AUTHORITY_RECORD.md",
        [
            DIRECTIVE_SHA,
            "No product code on PR #72",
            "No premature PR #71 thread resolution",
        ],
    )


def validate_authorized_paths() -> None:
    rows = read_csv("AUTHORIZED_CORRECTIVE_PATHS.csv")
    paths = {row["path"] for row in rows}
    for path in AUTHORIZED_PATHS:
        if path not in paths:
            fail(f"missing authorized path row: {path}")
    if f"{AUTHORIZED_PREFIX}**" not in paths:
        fail("missing package wildcard authorization")

    report = (ROOT / "AUTHORIZED_PATH_REPORT.md").read_text(encoding="utf-8")
    if "Status: `PASS`" not in report or "Unauthorized paths: `NONE`" not in report:
        fail("authorized path report does not pass")


def validate_implementation_snippets() -> None:
    minor_safety = (REPO / "backend/core/minor_safety.py").read_text(encoding="utf-8")
    minor_communication = (REPO / "backend/core/minor_communication.py").read_text(encoding="utf-8")
    billing = (REPO / "backend/routes/billing.py").read_text(encoding="utf-8")
    recurring = (REPO / "backend/routes/recurring_charges.py").read_text(encoding="utf-8")
    tests = (REPO / "backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py").read_text(encoding="utf-8")

    for snippet in [
        "def guardian_link_barn_proven",
        "async def load_verified_guardian_linked_students",
        '("migration_verified_barn_id", "legacy_barn_id")',
        "verified_barns == {active_barn}",
    ]:
        if snippet not in minor_safety:
            fail(f"minor_safety missing {snippet}")

    for name, text in {
        "minor_communication": minor_communication,
        "billing": billing,
        "recurring": recurring,
    }.items():
        if "load_verified_guardian_linked_students" not in text:
            fail(f"{name} does not use shared Guardian-link helper")
        if '{"barn_id": barn_id, "guardian_user_id": owner_id, "status": "active"}' in text:
            fail(f"{name} retained exact-barn-only owner Guardian-link query")

    for snippet in [
        'action == "invoice.pay" and not expected_state_token',
        "__missing_guardian_guard_state_token__",
    ]:
        if snippet not in billing:
            fail(f"billing missing {snippet}")

    for snippet in [
        "gate = await _payment_gate",
        '"guardian_guard_state_token": gate.get("state_token")',
        "if not gate:",
        "rc_update[key] = rc[key]",
    ]:
        if snippet not in recurring:
            fail(f"recurring missing {snippet}")

    for test_id in range(55, 60):
        if f"test_gms_t_{test_id:03d}" not in tests:
            fail(f"missing GMS-T-{test_id:03d} test")


def validate_results_records() -> None:
    focused = read_csv("FOCUSED_TEST_RESULTS.csv")
    if len(focused) < 15 or any(row["result"] != "PASS" for row in focused):
        fail("focused results are incomplete or non-passing")
    required = {
        "LEGACY_LINK_CONTRADICTORY_PROVENANCE_EXCLUDED",
        "MESSAGING_EXPANSION_INCLUDES_VERIFIED_LEGACY_LINK",
        "PAYMENT_EXPANSION_INCLUDES_VERIFIED_LEGACY_LINK",
        "MATERIALIZED_INVOICE_COPIES_REFRESHED_STATE_TOKEN",
        "LEGACY_INVOICE_WITHOUT_TOKEN_FAILS_CLOSED_OR_REAUTHORIZES_EXPLICITLY",
    }
    found = {row["requirement"] for row in focused}
    if not required <= found:
        fail(f"focused results missing requirements: {sorted(required - found)}")

    prior = read_csv("PRIOR_SAFEGUARD_REGRESSION_RESULTS.csv")
    if not any(row["test_scope"] == "PRIOR_PR_71_GUARDIAN_MINOR_CASES_GMS_T_001_THROUGH_GMS_T_054" and row["result"] == "PASS" for row in prior):
        fail("prior PR #71 safeguard rerun not recorded")
    if not any(row["test_scope"] == "CORRECTIVE_FULL_FOCUSED_SET_GMS_T_001_THROUGH_GMS_T_059" and row["result"] == "PASS" for row in prior):
        fail("full focused direct run not recorded")

    positives = read_csv("POSITIVE_CONTROL_RESULTS.csv")
    if len(positives) < 6 or any(row["result"] != "PASS" for row in positives):
        fail("positive controls incomplete or non-passing")

    dispositions = read_csv("REVIEW_FINDINGS_AND_DISPOSITION.csv")
    if {row["finding_id"] for row in dispositions} != {"PR71-POST-MERGE-001", "PR71-POST-MERGE-002"}:
        fail("review finding IDs mismatch")
    if any(row["status"] != "CORRECTED_PENDING_CORRECTIVE_PR_REVIEW_AND_PROTECTED_MERGE" for row in dispositions):
        fail("review finding disposition status mismatch")


def validate_boundary_records() -> None:
    require_text(
        ROOT / "CHANGE_AWARE_BYPASS_REVIEW.md",
        [
            "missing-barn legacy Guardian link",
            "materialized recurring invoices",
            "GitHub checks and review",
        ],
    )
    require_text(
        ROOT / "ROLLBACK_AND_SUSPENSION_RECORD.md",
        [
            "NO_RUNTIME_ACTIVATION_PERFORMED",
            "No provider call",
            "No direct protected push",
        ],
    )
    require_text(
        ROOT / "DIRECTIVE_EXECUTION_RECORD.md",
        [
            "PHASE_A_CORRECTIVE_IMPLEMENTATION_READY_FOR_DRAFT_PR",
            "No closure registers were updated in Phase A.",
        ],
    )


def main() -> None:
    validate_package_files()
    validate_source_and_authority()
    validate_authorized_paths()
    validate_implementation_snippets()
    validate_results_records()
    validate_boundary_records()
    print("PASS post-merge correction package")


if __name__ == "__main__":
    main()
