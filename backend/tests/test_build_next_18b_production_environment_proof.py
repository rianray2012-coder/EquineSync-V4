"""Build-Next-18B production environment proof tests.

BN18B is evidence-only. It may perform public GET probes, but it must not
mutate providers, MongoDB, users, billing, UAT accounts, or founder-acceptance
state. Operator-only proof remains represented as supplied/missing labels.
"""
from __future__ import annotations

import pathlib

from core.production_environment_proof import (
    DEFAULT_API_BASE_URL,
    DEFAULT_FRONTEND_URL,
    build_production_environment_proof,
    render_production_environment_proof_markdown,
)


ROOT = pathlib.Path(__file__).resolve().parents[2]
HEALTH_URL = f"{DEFAULT_API_BASE_URL}/api/health"
READY_URL = f"{DEFAULT_API_BASE_URL}/api/health/ready"


def _operator_env() -> dict[str, str]:
    return {
        "BN18B_DATABASE_LABEL": "MongoDB Atlas / Equine Sync / EsProduction / ES_Members",
        "BN18B_VERCEL_DEPLOY_MARKER": "Vercel production deploy marker present",
        "BN18B_RENDER_DEPLOY_MARKER": "Render production deploy marker present",
        "BN18B_ROLLBACK_EVIDENCE": "Vercel and Render rollback controls visible",
        "BN18B_BACKUP_EVIDENCE": "Atlas backup policy visible",
        "BN18B_MONITORING_EVIDENCE": "Render logs and Vercel deployment logs visible",
        "BN18B_STARTUP_LOG_EVIDENCE": "startup complete log shows background loops",
    }


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


def test_full_public_and_operator_evidence_can_pass():
    report = build_production_environment_proof(_operator_env(), fetcher=_fetcher)

    assert report["overall_status"] == "pass"
    assert report["issue_counts"] == {}
    assert {row["area"]: row["status"] for row in report["rows"]} == {
        "frontend": "pass",
        "backend": "pass",
        "database": "pass",
        "email": "pass",
        "runtime": "pass",
        "seed_safety": "pass",
        "operator_evidence": "pass",
    }
    assert report["backend_health"]["environment"] == "production"
    assert report["backend_health"]["database"] == "connected"
    assert report["source_seed_safety"]["production_auto_seed_fail_closed"] is True
    assert report["source_seed_safety"]["production_seed_route_fail_closed"] is True


def test_missing_operator_evidence_is_warning_not_auto_passed():
    report = build_production_environment_proof({}, fetcher=_fetcher)

    assert report["overall_status"] == "attention"
    assert report["issue_counts"]["warning"] == 7
    assert report["operator_evidence"] == {
        "database_label": "missing",
        "vercel_deploy_marker": "missing",
        "render_deploy_marker": "missing",
        "rollback_evidence": "missing",
        "backup_evidence": "missing",
        "monitoring_evidence": "missing",
        "startup_log_evidence": "missing",
    }


def test_health_unreachable_is_blocker():
    def fetcher(url: str):
        if url == HEALTH_URL:
            return {
                "ok": False,
                "status_code": None,
                "headers": {},
                "body_bytes": 0,
                "json": None,
                "error": "URLError: SSL handshake failed",
            }
        return _fetcher(url)

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    rows = {row["area"]: row["status"] for row in report["rows"]}
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert "health_unreachable" in kinds
    assert "database_unverified" in kinds
    assert "email_posture_unverified" in kinds
    assert "runtime_seed_flags_unverified" in kinds
    assert rows["backend"] == "blocked"
    assert rows["database"] == "blocked"
    assert rows["email"] == "blocked"
    assert rows["seed_safety"] == "blocked"


def test_degraded_database_and_unsafe_seed_flags_are_blockers():
    def fetcher(url: str):
        result = dict(_fetcher(url))
        if url == HEALTH_URL:
            body = dict(result["json"])
            body["status"] = "degraded"
            body["database"] = "unreachable"
            body["dependencies"] = dict(body["dependencies"])
            body["dependencies"]["auto_seed_enabled"] = True
            body["dependencies"]["seed_route_enabled"] = True
            result["json"] = body
        return result

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert "health_status_not_ok" in kinds
    assert "database_not_connected" in kinds
    assert "auto_seed_enabled" in kinds
    assert "seed_route_enabled" in kinds


def test_missing_runtime_seed_flags_are_blockers():
    def fetcher(url: str):
        result = dict(_fetcher(url))
        if url == HEALTH_URL:
            body = dict(result["json"])
            body["dependencies"] = dict(body["dependencies"])
            body["dependencies"].pop("auto_seed_enabled")
            body["dependencies"].pop("seed_route_enabled")
            result["json"] = body
        return result

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    rows = {row["area"]: row["status"] for row in report["rows"]}
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert rows["seed_safety"] == "blocked"
    assert "auto_seed_flag_unverified" in kinds
    assert "seed_route_flag_unverified" in kinds


def test_readiness_non_json_is_blocker():
    def fetcher(url: str):
        if url == READY_URL:
            return {
                "ok": True,
                "status_code": 200,
                "headers": {"server": "uvicorn", "content-type": "text/html"},
                "body_bytes": 42,
                "json": None,
                "error": "",
            }
        return _fetcher(url)

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    rows = {row["area"]: row["status"] for row in report["rows"]}
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert rows["runtime"] == "blocked"
    assert "ready_not_json" in kinds


def test_readiness_status_must_be_ok():
    def fetcher(url: str):
        result = dict(_fetcher(url))
        if url == READY_URL:
            body = dict(result["json"])
            body["status"] = "degraded"
            body["indexes_ensured"] = True
            result["json"] = body
        return result

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    rows = {row["area"]: row["status"] for row in report["rows"]}
    kinds = {issue["kind"] for issue in report["issues"]}

    assert report["overall_status"] == "blocked"
    assert rows["runtime"] == "blocked"
    assert "ready_status_not_ok" in kinds


def test_email_verification_not_enforced_is_warning():
    def fetcher(url: str):
        result = dict(_fetcher(url))
        if url == HEALTH_URL:
            body = dict(result["json"])
            body["dependencies"] = dict(body["dependencies"])
            body["dependencies"]["email_verification_enforced"] = False
            result["json"] = body
        return result

    report = build_production_environment_proof(_operator_env(), fetcher=fetcher)
    assert report["overall_status"] == "attention"
    assert any(issue["kind"] == "email_verification_not_enforced" for issue in report["issues"])


def test_rendered_report_does_not_include_operator_values_or_secret_shapes():
    env = _operator_env()
    env.update({
        "STRIPE_API_KEY": "sk_live_SHOULD_NOT_RENDER",
        "MONGO_URL": "mongodb+srv://user:pass@example.invalid/db",
        "DOCUSIGN_PRIVATE_KEY": "-----BEGIN RSA PRIVATE KEY-----SHOULD_NOT_RENDER",
    })
    report = build_production_environment_proof(env, fetcher=_fetcher)
    markdown = render_production_environment_proof_markdown(report)

    assert "provided" in markdown
    forbidden = [
        "sk_live_SHOULD_NOT_RENDER",
        "mongodb+srv://",
        "BEGIN RSA PRIVATE KEY",
        "Atlas backup policy visible",
        "startup complete log shows background loops",
    ]
    for fragment in forbidden:
        assert fragment not in markdown


def test_bn18b_source_does_not_call_mutating_providers_or_write_mongo():
    core_src = (ROOT / "backend" / "core" / "production_environment_proof.py").read_text()
    script_src = (ROOT / "backend" / "scripts" / "build_next_18b_production_environment_proof.py").read_text()
    combined = core_src + "\n" + script_src

    forbidden = [
        "stripe.checkout",
        "stripe.Webhook.construct_event",
        "resend.Emails.send",
        "request_docusign_access_token",
        "create_docusign_sandbox_envelope",
        "requests.post",
        "urlopen(Request(",
        "method=\"POST\"",
        "AsyncIOMotorClient",
        "insert_one",
        "update_one",
        "delete_one",
        "bulk_write",
        "founder_accepted",
    ]
    for token in forbidden:
        assert token not in combined


def test_bn18b_script_has_no_mutating_lifecycle_flags():
    script_src = (ROOT / "backend" / "scripts" / "build_next_18b_production_environment_proof.py").read_text()
    assert "--fail-on-blockers" in script_src
    assert "--database-label" in script_src
    for token in (
        "--send-email",
        "--create-checkout",
        "--create-envelope",
        "--replay-webhook",
        "--seed",
        "--accept",
    ):
        assert token not in script_src
