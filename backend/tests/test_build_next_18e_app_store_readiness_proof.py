from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from core.app_store_readiness_proof import (
    ROOT,
    build_app_store_readiness_proof,
    render_app_store_readiness_report,
)


def test_bn18e_current_repo_is_blocked_for_native_store_launch():
    report = build_app_store_readiness_proof(ROOT)
    rows = {row["key"]: row for row in report["readiness_rows"]}

    assert report["overall_status"] == "blocked"
    assert rows["web_manifest"]["status"] == "ready"
    assert rows["native_ios_project"]["status"] == "missing"
    assert rows["native_android_project"]["status"] == "missing"
    assert rows["support_urls"]["status"] == "blocked"
    assert rows["billing_policy_mapping"]["status"] == "partial"
    assert rows["review_accounts"]["status"] == "deferred"
    assert report["issue_counts"].get("blocker", 0) >= 6
    assert report["issue_counts"].get("decision_required", 0) >= 3


def test_bn18e_source_scan_records_absent_native_and_present_web_assets():
    scan = build_app_store_readiness_proof(ROOT)["source_scan"]

    assert scan["web_manifest_status"] == "present"
    assert scan["ios_project_status"] == "missing"
    assert scan["android_project_status"] == "missing"
    assert scan["store_metadata_status"] == "missing"
    assert scan["store_screenshot_status"] == "missing"
    assert scan["uat_screenshot_status"] == "present"
    assert scan["support_url_status"] == "missing"
    assert scan["privacy_policy_status"] == "missing"
    assert scan["account_deletion_status"] == "missing"
    assert scan["billing_mapping_status"] == "partial"
    assert scan["minor_guardian_status"] == "present"


def test_bn18e_readiness_rows_follow_source_scan_when_store_artifacts_exist(tmp_path):
    manifest_dir = tmp_path / "frontend" / "public"
    manifest_dir.mkdir(parents=True)
    (manifest_dir / "manifest.json").write_text(
        '{"name":"EquineSync","short_name":"ES","icons":[{"src":"icon.png"}],"display":"standalone"}',
        encoding="utf-8",
    )
    (tmp_path / "ios").mkdir()
    (tmp_path / "android").mkdir()
    (tmp_path / "fastlane" / "metadata").mkdir(parents=True)
    (tmp_path / "fastlane" / "screenshots").mkdir(parents=True)
    (tmp_path / "outputs" / "build_next_18c_uat_role_refresh_screenshots").mkdir(parents=True)

    report = build_app_store_readiness_proof(tmp_path)
    scan = report["source_scan"]
    rows = {row["key"]: row["status"] for row in report["readiness_rows"]}

    assert scan["ios_project_status"] == "present"
    assert scan["android_project_status"] == "present"
    assert scan["store_metadata_status"] == "present"
    assert scan["store_screenshot_status"] == "present"
    assert rows["native_ios_project"] == "ready"
    assert rows["native_android_project"] == "ready"
    assert rows["store_metadata_bundle"] == "ready"
    assert rows["store_screenshots"] == "ready"


def test_bn18e_report_contains_required_gate_sections_and_founder_decisions():
    report = build_app_store_readiness_proof(ROOT)
    rendered = render_app_store_readiness_report(report)

    required_sections = [
        "## Readiness Checklist",
        "## Store Metadata Inventory",
        "## Privacy And Data-Safety Evidence",
        "## Support And Account Deletion Evidence",
        "## Billing Policy Mapping",
        "## Screenshot And Review-Note Requirements",
        "## Release Ownership Checklist",
        "## Founder Decisions",
        "## Official Policy References",
        "## BN18E Acceptance Boundary",
    ]
    for section in required_sections:
        assert section in rendered

    assert "web-only, PWA-assisted web, native app-store distributed" in rendered
    assert "Google Play billing" in rendered
    assert "Apple privacy labels" in rendered
    assert "not_performed" in rendered


def test_bn18e_metadata_and_policy_tables_cover_store_requirements():
    report = build_app_store_readiness_proof(ROOT)

    metadata_fields = {row["field"] for row in report["store_metadata_inventory"]}
    assert {
        "App name",
        "Support URL",
        "Privacy policy URL",
        "Account deletion URL/path",
        "Review/demo accounts",
        "Screenshots",
        "Release owner",
    }.issubset(metadata_fields)

    billing_surfaces = {row["surface"] for row in report["billing_policy_rows"]}
    assert "Current web subscription purchase" in billing_surfaces
    assert "Apple App Store distributed iOS app" in billing_surfaces
    assert "Google Play distributed Android app" in billing_surfaces

    policy_topics = {row["topic"] for row in report["policy_references"]}
    assert "App privacy details" in policy_topics
    assert "Data safety" in policy_topics
    assert "Payments policy" in policy_topics


def test_bn18e_script_writes_report_and_fail_on_blockers_exits_two(tmp_path):
    output = tmp_path / "bn18e_report.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_18e_app_store_readiness_proof",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert "Build-Next-18E App Store / Google Play Readiness Report" in output.read_text(encoding="utf-8")
    assert "status=blocked" in result.stdout

    blocked = subprocess.run(
        [
            sys.executable,
            "-m",
            "backend.scripts.build_next_18e_app_store_readiness_proof",
            "--output",
            str(output),
            "--fail-on-blockers",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert blocked.returncode == 2
    assert "blocker(s)=" in blocked.stdout


def test_bn18e_rendered_report_has_no_secret_shapes():
    rendered = render_app_store_readiness_report(build_app_store_readiness_proof(ROOT))

    forbidden_patterns = [
        r"sk_(live|test)_[A-Za-z0-9]{16,}",
        r"rk_(live|test)_[A-Za-z0-9]{16,}",
        r"whsec_[A-Za-z0-9]{16,}",
        r"mongodb(\\+srv)?://",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, rendered)

    assert "password" not in rendered.lower()


def test_bn18e_proof_code_is_read_only():
    files = [
        ROOT / "backend/core/app_store_readiness_proof.py",
        ROOT / "backend/scripts/build_next_18e_app_store_readiness_proof.py",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in files)

    forbidden_tokens = [
        "MongoClient",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "replace_one",
        "requests.",
        "httpx.",
        "stripe.",
        "docusign",
        "AppStoreConnect",
        "googleapiclient",
        "founder_accepted",
        "seed_bn",
    ]
    for token in forbidden_tokens:
        assert token not in joined


def test_bn18e_expected_package_file_list_is_explicit():
    expected = {
        "BUILD_NEXT_18E_APP_STORE_READINESS_README.md",
        "docs/APP_STORE_PRODUCTION_READINESS.md",
        "docs/LAUNCH_TRUST_CURRENT_PLAN.md",
        "docs/LAUNCH_TRUST_MASTER_FIX_LIST.md",
        "memory/PRD.md",
        "backend/core/app_store_readiness_proof.py",
        "backend/scripts/build_next_18e_app_store_readiness_proof.py",
        "backend/tests/test_build_next_18e_app_store_readiness_proof.py",
        "outputs/bn18e_app_store_readiness_report.md",
    }

    assert len(expected) == 9
    assert all(Path(path).suffix for path in expected)
