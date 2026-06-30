"""Build-Next-12 launch closure evidence checks.

This phase may record sanitized live deployment facts, but it must not convert
the app into launch-approved status until role and provider proof are complete.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_12_CLOSURE_README.md"
STATUS = ROOT / "docs/BUILD_NEXT_12_CURRENT_INPUTS_STATUS.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn12_closure_artifacts_exist_and_are_nonempty():
    for path in (README, STATUS):
        assert path.exists(), str(path)
        assert path.stat().st_size > 500, str(path)


def test_bn12_records_current_live_urls_and_email_configured():
    text = f"{_read(README)}\n{_read(STATUS)}"

    assert "https://app.equine-sync.com" in text
    assert "https://equine-sync-api.onrender.com" in text
    assert "MongoDB Atlas / Equine Sync / EsProduction / ES_Members" in text
    assert "Vercel Production Deploy / 06.30.2026 / commit `5aeea66` / status Ready" in text
    assert "Email/mailer: configured" in text
    assert "mailer_configured=true" in text
    assert "RESEND_API_KEY configured: yes" in text
    assert "RESEND_FROM verified sender: yes" in text


def test_bn12_keeps_launch_blocked_until_role_and_provider_proof():
    text = f"{_read(README)}\n{_read(STATUS)}".lower()

    assert "not launch-clearing" in text
    assert "`blocked`" in text
    assert "role-account proof" in text
    assert "controlled live-safe stripe proof" in text
    assert "docusign disposable signer/webhook proof" in text
    assert "public launch blocked" in text
    assert "launch approved" not in text
    assert "pilot approved" not in text
    assert "ready for unrestricted launch" not in text


def test_bn12_secret_shapes_are_not_recorded():
    text = f"{_read(README)}\n{_read(STATUS)}"
    forbidden = [
        "sk" + "_live_",
        "sk" + "_test_",
        "rk" + "_live_",
        "rk" + "_test_",
        "re" + "_",
        "wh" + "sec_",
        "-----" + "BEGIN",
        "Authorization" + ": Bearer",
        "DOCUSIGN" + "_PRIVATE_KEY=",
        "DOCUSIGN" + "_WEBHOOK_SECRET=",
        "STRIPE" + "_API_KEY=",
        "JWT" + "_SECRET=",
        "mongodb" + "+srv://",
        "password" + ":",
    ]
    for fragment in forbidden:
        assert fragment not in text


def test_bn12_role_rows_remain_pending_for_official_evidence():
    text = _read(STATUS)

    for row in ("UAT-R1", "UAT-R2", "UAT-R3", "UAT-R4", "UAT-R5", "UAT-R6", "UAT-R7", "UAT-R8"):
        assert row in text
    assert "account exists and can sign in" in text
    assert "Do not paste passwords or tokens" in text
