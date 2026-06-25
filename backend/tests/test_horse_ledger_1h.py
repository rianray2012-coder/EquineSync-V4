"""tests/test_horse_ledger_1h.py - HorseOps-1H mobile field readiness.

1H is a frontend-first hardening phase. These tests pin the source-level
contracts that matter most for review: local drafts are field-only, mobile
drawers keep safe action areas, and the admin horse directory remains
summary-only while gaining mobile cards.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _without_comments(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"//.*", "", src)


def test_horseops_draft_helper_is_local_field_only():
    src = _read("frontend/src/lib/horseOpsDrafts.js")
    assert "localStorage" in src
    assert "equinesync:horseops:draft:v1" in src
    assert "token" not in src.lower()
    assert "authorization" not in src.lower()
    assert "cookie" not in src.lower()
    assert "password" not in src.lower()


def test_staff_daily_check_drawer_persists_and_clears_local_draft():
    src = _read("frontend/src/pages/CareLedgerTab.jsx")
    assert "buildHorseOpsDraftKey" in src
    assert "daily-check-new-" in src
    assert "daily-check-amend-" in src
    assert "daily-check-draft-restored" in src
    assert "saveHorseOpsDraft(draftKey" in src
    assert "clearHorseOpsDraft(draftKey)" in src


def test_owner_request_drawer_persists_and_clears_local_draft():
    src = _read("frontend/src/pages/OwnerCareLedger.jsx")
    assert "buildHorseOpsDraftKey" in src
    assert 'form: "owner-request"' in src
    assert "owner-request-draft-restored" in src
    assert "saveHorseOpsDraft(draftKey" in src
    assert "clearHorseOpsDraft(draftKey)" in src


def test_mobile_drawers_have_safe_height_sticky_actions_and_tap_targets():
    care_src = _read("frontend/src/pages/CareLedgerTab.jsx")
    owner_src = _read("frontend/src/pages/OwnerCareLedger.jsx")
    admin_src = _read("frontend/src/pages/admin/AdminHorses.jsx")
    for src in (care_src, owner_src, admin_src):
        assert "max-h-dvh" in src
        assert "env(safe-area-inset-bottom)" in src
        assert "min-h-11" in src


def test_admin_horse_directory_has_mobile_cards_and_keeps_desktop_table():
    src = _read("frontend/src/pages/admin/AdminHorses.jsx")
    assert 'data-testid="admin-horses-mobile-cards"' in src
    assert "admin-horses-card-" in src
    assert 'className="hidden md:table w-full text-[13px]"' in src
    assert "summary-only drawer" in src


def test_owner_surface_source_does_not_render_private_ledger_terms():
    src = _without_comments(_read("frontend/src/pages/OwnerCareLedger.jsx")).lower()
    forbidden = [
        "source_check_id",
        "staff_note",
        "staff notes",
        "raw check",
        "audit_log",
        "alert internals",
        "triggers",
    ]
    for token in forbidden:
        assert token not in src


def test_admin_horses_uses_approved_palette_only():
    src = _read("frontend/src/pages/admin/AdminHorses.jsx")
    forbidden = re.compile(
        r"\b(?:bg|text|border)-(?:red|amber|green|yellow|blue|indigo|violet|"
        r"purple|pink|rose|teal|cyan|emerald|lime|orange|sky|fuchsia)-\d+"
    )
    assert not forbidden.search(src)
