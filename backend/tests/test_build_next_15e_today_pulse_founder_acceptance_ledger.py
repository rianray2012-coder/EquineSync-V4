"""Build-Next-15E - Today Pulse founder acceptance ledger checks.

BN15E is an evidence/decision ledger only. It must not mark rows
founder-accepted, approve launch, or weaken the locked BN15 privacy boundary.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "BUILD_NEXT_15E_TODAYS_PULSE_FOUNDER_ACCEPTANCE_LEDGER_README.md"
LEDGER = ROOT / "outputs" / "build_next_15e_today_pulse_founder_acceptance_ledger.md"
PRD = ROOT / "memory" / "PRD.md"

ACCEPTANCE_ROWS = [f"TP-{i}" for i in range(1, 12)]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_bn15e_required_artifacts_exist_and_are_nonempty():
    for path in [README, LEDGER]:
        assert path.exists(), str(path)
        assert path.stat().st_size > 1000, str(path)


def test_bn15e_records_founder_acceptance_authority_without_auto_accepting():
    text = _read(README) + "\n" + _read(LEDGER)

    for phrase in [
        "Only Rian can mark",
        "not founder-accepted",
        "Pending explicit founder action",
        "ready_for_founder_review",
        "does not mark any row founder-accepted",
    ]:
        assert phrase in text

    ledger_table = text.split("## Acceptance Ledger", 1)[1].split("## Explicit Non-Acceptances", 1)[0]
    assert "| founder-accepted |" not in ledger_table
    assert ledger_table.count("| ready_for_founder_review |") == len(ACCEPTANCE_ROWS)


def test_bn15e_acceptance_rows_cover_all_today_pulse_role_boundaries():
    text = _read(LEDGER)

    for row in ACCEPTANCE_ROWS:
        assert f"| {row} |" in text

    for phrase in [
        "Platform admin",
        "Facility admin / barn owner",
        "Barn manager",
        "Staff/groom",
        "Trainer",
        "Working student",
        "Horse owner",
        "Guardian / parent",
        "Rider / lesson participant",
        "Standalone individual owner",
        "Privacy exclusions",
    ]:
        assert phrase in text


def test_bn15e_ties_acceptance_to_locked_evidence_chain():
    text = _read(README) + "\n" + _read(LEDGER)

    for phase in ["BN15A", "BN15C-A", "BN15C-B", "BN15C-C", "BN15D", "BN10"]:
        assert phase in text

    for artifact in [
        "BN13O screenshots",
        "BN15 focused tests",
        "BN15D screenshots/report/tests",
        "build_next_15d_today_pulse_uat_evidence",
    ]:
        assert artifact in text


def test_bn15e_keeps_launch_and_provider_acceptance_out_of_scope():
    text = _read(README) + "\n" + _read(LEDGER)

    for phrase in [
        "No public launch approval",
        "public launch",
        "first-client pilot",
        "live Stripe checkout",
        "Customer Portal",
        "Apple billing",
        "DocuSign live workflow",
        "Text/SMS notification delivery",
    ]:
        assert phrase in text

    assert "launch approved" not in text.lower()
    assert "pilot approved" not in text.lower()
    assert "Ready for unrestricted launch" not in text


def test_bn15e_preserves_privacy_and_no_behavior_change_guardrails():
    text = _read(README) + "\n" + _read(LEDGER)

    for phrase in [
        "No product behavior changes",
        "No backend route/schema/auth/permission changes",
        "No frontend behavior changes",
        "No owner projection changes",
        "No HorseOps write behavior",
        "No billing",
        "No seeded-demo, UAT-account, production-data, or credential mutation",
        "staff notes",
        "raw payloads",
        "alert triggers",
        "audit diffs",
        "provider IDs",
        "private horse records",
    ]:
        assert phrase in text


def test_bn15e_text_does_not_contain_secret_shaped_values():
    combined = "\n".join(_read(path) for path in [README, LEDGER])
    forbidden = [
        "sk" + "_live_",
        "rk" + "_live_",
        "pk" + "_live_",
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
    for needle in forbidden:
        assert needle not in combined


def test_bn15e_prd_status_records_locked():
    prd = _read(PRD)
    assert "Build-Next-15E - Today's Pulse Founder Acceptance Ledger" in prd
    assert "CODEX-APPROVED & LOCKED" in prd


def test_bn15e_lock_status_does_not_auto_accept_rows():
    text = _read(README) + "\n" + _read(LEDGER)
    normalized = " ".join(text.split())
    assert "Codex-approved & locked" in text
    assert "founder acceptance remains pending explicit founder action" in normalized
    assert "does not mean any row has been founder-accepted" in text


def test_bn15e_status_terms_are_controlled():
    text = _read(README) + "\n" + _read(LEDGER)

    for status in [
        "ready_for_founder_review",
        "founder-accepted",
        "needs_live_uat",
        "blocked",
        "deferred",
    ]:
        assert f"`{status}`" in text

    assert not re.search(r"Status\\s*:\\s*approved", text, flags=re.IGNORECASE)
