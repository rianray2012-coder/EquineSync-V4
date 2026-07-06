"""Build-Next-18C UAT role-refresh proof tests.

BN18C must not run role UAT while BN18B production health/readiness is blocked.
It also must not auto-pass role rows without screenshot/session evidence or
record founder acceptance.
"""
from __future__ import annotations

import pathlib

from core.production_environment_proof import (
    DEFAULT_API_BASE_URL,
    DEFAULT_FRONTEND_URL,
)
from core.uat_role_refresh_proof import (
    PNG_SIGNATURE,
    ROLE_ROWS,
    build_uat_role_refresh_report,
    render_uat_role_refresh_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
HEALTH_URL = f"{DEFAULT_API_BASE_URL}/api/health"
READY_URL = f"{DEFAULT_API_BASE_URL}/api/health/ready"
VALID_PRIVACY_SWEEP = (
    "# Privacy Sweep\n\n"
    "Verified screenshot-only evidence for TP-1 through TP-10. No staff notes, "
    "raw daily-check payloads, alert triggers, source identifiers, audit diffs, "
    "tokens, passwords, Stripe identifiers, or private fields are visible."
)


def _fetcher(url: str):
    if url == DEFAULT_FRONTEND_URL:
        return {
            "ok": True,
            "status_code": 200,
            "headers": {"server": "Vercel", "x-vercel-cache": "HIT"},
            "body_bytes": 3486,
            "json": None,
            "error": "",
        }
    if url == HEALTH_URL:
        return {
            "ok": True,
            "status_code": 200,
            "headers": {"server": "uvicorn", "content-type": "application/json"},
            "body_bytes": 300,
            "json": {
                "status": "ok",
                "service": "equinesync-api",
                "version": "0.1.0",
                "database": "connected",
                "config": {
                    "jwt_configured": True,
                    "cors_configured": True,
                    "environment": "production",
                },
                "dependencies": {
                    "mailer_configured": True,
                    "email_verification_enforced": True,
                    "rate_limiting_enabled": True,
                    "auto_seed_enabled": False,
                    "seed_route_enabled": False,
                },
            },
            "error": "",
        }
    if url == READY_URL:
        return {
            "ok": True,
            "status_code": 200,
            "headers": {"server": "uvicorn", "content-type": "application/json"},
            "body_bytes": 360,
            "json": {
                "status": "ok",
                "service": "equinesync-api",
                "database": "connected",
                "started_at": "2026-07-05T00:00:00+00:00",
                "uptime_seconds": 60.0,
                "indexes_ensured": True,
            },
            "error": "",
        }
    raise AssertionError(f"Unexpected URL fetched: {url}")


def _evidence_files(row):
    return row.get("evidence_files") or [row["screenshot"]]


def _write_valid_evidence(path: pathlib.Path) -> None:
    if path.suffix == ".md":
        path.write_text(VALID_PRIVACY_SWEEP, encoding="utf-8")
    else:
        path.write_bytes(PNG_SIGNATURE + b"valid screenshot bytes")


def test_bn18b_gate_blocker_blocks_every_role_row():
    def blocked_fetcher(url: str):
        if url in {HEALTH_URL, READY_URL}:
            return {
                "ok": False,
                "status_code": None,
                "headers": {},
                "body_bytes": 0,
                "json": None,
                "error": "URLError: SSL handshake failed",
            }
        return _fetcher(url)

    report = build_uat_role_refresh_report({}, fetcher=blocked_fetcher)

    assert report["overall_status"] == "blocked"
    assert report["gate_status"] == "blocked"
    assert report["issue_counts"]["blocker"] == 1
    assert report["gate_blocker_count"] >= 1
    assert {row["status"] for row in report["role_rows"]} == {"blocked"}
    assert all("credentialed role UAT is deferred" in row["reason"] for row in report["role_rows"])


def test_clean_gate_does_not_auto_pass_without_evidence():
    report = build_uat_role_refresh_report({}, fetcher=_fetcher)

    assert report["overall_status"] == "attention"
    assert report["gate_status"] == "pass"
    assert report["gate_blocker_count"] == 0
    assert {row["status"] for row in report["role_rows"]} == {"pending_capture"}
    assert report["issue_counts"]["warning"] == len(ROLE_ROWS)


def test_screenshot_evidence_can_prepare_rows_but_not_founder_accept(tmp_path):
    for row in ROLE_ROWS:
        for filename in _evidence_files(row):
            _write_valid_evidence(tmp_path / filename)

    report = build_uat_role_refresh_report(
        {"BN18C_SCREENSHOT_EVIDENCE_DIR": str(tmp_path)},
        fetcher=_fetcher,
    )
    markdown = render_uat_role_refresh_markdown(report)

    assert report["overall_status"] == "ready_for_founder_review"
    assert {row["status"] for row in report["role_rows"]} == {"evidence_captured"}
    assert "Founder acceptance remains separate" in markdown
    assert "founder_accepted" not in markdown


def test_placeholder_evidence_does_not_prepare_rows(tmp_path):
    for row in ROLE_ROWS:
        for filename in _evidence_files(row):
            (tmp_path / filename).write_text("placeholder", encoding="utf-8")

    report = build_uat_role_refresh_report(
        {"BN18C_SCREENSHOT_EVIDENCE_DIR": str(tmp_path)},
        fetcher=_fetcher,
    )

    assert report["overall_status"] == "attention"
    assert {row["status"] for row in report["role_rows"]} == {"pending_capture"}
    assert report["issue_counts"]["warning"] == len(ROLE_ROWS)


def test_tp2_requires_facility_admin_and_barn_owner_screenshots(tmp_path):
    for row in ROLE_ROWS:
        for filename in _evidence_files(row):
            _write_valid_evidence(tmp_path / filename)
    (tmp_path / "uat-r2b-barn-owner.png").unlink()

    report = build_uat_role_refresh_report(
        {"BN18C_SCREENSHOT_EVIDENCE_DIR": str(tmp_path)},
        fetcher=_fetcher,
    )
    tp2 = next(row for row in report["role_rows"] if row["tp_row"] == "TP-2")

    assert report["overall_status"] == "attention"
    assert tp2["status"] == "pending_capture"
    assert "uat-r2b-barn-owner.png" in tp2["reason"]


def test_role_rows_match_locked_tp_mapping():
    expected = {
        ("TP-1", "UAT-R1", "platform_admin"),
        ("TP-2", "UAT-R2a / UAT-R2b", "admin / barn_owner"),
        ("TP-3", "UAT-R3", "barn_manager"),
        ("TP-4", "UAT-R4a", "groom"),
        ("TP-5", "BN13M-T1", "trainer"),
        ("TP-6", "BN13M-W1", "working_student"),
        ("TP-7", "UAT-R5", "horse_owner"),
        ("TP-8", "UAT-R6", "parent"),
        ("TP-9", "UAT-R7", "rider"),
        ("TP-10", "UAT-R8", "standalone horse_owner"),
        ("TP-11", "Privacy exclusions", "all role rows"),
    }

    assert len(ROLE_ROWS) == 11
    assert {(row["tp_row"], row["evidence_row"], row["role"]) for row in ROLE_ROWS} == expected
    tp2 = next(row for row in ROLE_ROWS if row["tp_row"] == "TP-2")
    assert tp2["evidence_files"] == [
        "uat-r2a-facility-admin.png",
        "uat-r2b-barn-owner.png",
    ]


def test_rendered_report_does_not_include_secret_shapes_or_operator_values():
    env = {
        "STRIPE_API_KEY": "sk_live_SHOULD_NOT_RENDER",
        "MONGO_URL": "mongodb+srv://user:pass@example.invalid/db",
        "DOCUSIGN_PRIVATE_KEY": "-----BEGIN RSA PRIVATE KEY-----SHOULD_NOT_RENDER",
        "BN18B_DATABASE_LABEL": "Atlas private label should not render here",
    }
    report = build_uat_role_refresh_report(env, fetcher=_fetcher)
    markdown = render_uat_role_refresh_markdown(report)

    forbidden = [
        "sk_live_SHOULD_NOT_RENDER",
        "mongodb+srv://",
        "BEGIN RSA PRIVATE KEY",
        "Atlas private label should not render here",
        "password",
        "auth token",
        "session token",
    ]
    for fragment in forbidden:
        assert fragment not in markdown


def test_bn18c_source_does_not_call_mutating_providers_or_write_mongo():
    core_src = (ROOT / "backend" / "core" / "uat_role_refresh_proof.py").read_text()
    script_src = (ROOT / "backend" / "scripts" / "build_next_18c_uat_role_refresh.py").read_text()
    combined = core_src + "\n" + script_src

    forbidden = [
        "stripe.checkout",
        "stripe.Webhook.construct_event",
        "resend.Emails.send",
        "request_docusign_access_token",
        "create_docusign_sandbox_envelope",
        "requests.post",
        "method=\"POST\"",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
        "founder_accepted",
        "create_user",
        "seed_",
    ]
    for token in forbidden:
        assert token not in combined


def test_bn18c_script_has_no_mutating_lifecycle_flags():
    script_src = (ROOT / "backend" / "scripts" / "build_next_18c_uat_role_refresh.py").read_text()
    assert "--fail-on-blockers" in script_src
    assert "--screenshot-evidence-dir" in script_src
    for token in (
        "--send-email",
        "--create-checkout",
        "--create-envelope",
        "--replay-webhook",
        "--seed",
        "--accept",
        "--login",
    ):
        assert token not in script_src
