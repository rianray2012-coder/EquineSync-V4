"""tests/test_horse_ledger_1i.py - HorseOps-1I mobile polish contracts.

1I is a frontend-only mobile field-readiness pass. These tests pin the
phone-sized layout contracts that are easy to regress in source: 44px-friendly
controls, stacked narrow rows, long-id wrapping, and approved admin palette.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_care_ledger_form_primitives_keep_mobile_tap_targets():
    src = _read("frontend/src/pages/CareLedgerTab.jsx")
    assert "min-h-11 w-full bg-equine-black/60 border border-equine-silver/15 rounded px-3 py-2" in src
    assert "flex min-h-11 items-center justify-between" in src
    assert "min-h-11 min-w-11 rounded-full" in src
    assert "min-h-10 text-[11px] tracking-[0.14em]" in src


def test_daily_check_rows_stack_on_mobile_and_keep_amend_tappable():
    src = _read("frontend/src/pages/CareLedgerTab.jsx")
    assert "flex flex-col sm:flex-row sm:items-center sm:justify-between" in src
    assert "flex flex-wrap items-center gap-2 sm:gap-3" in src
    assert "basis-full sm:basis-auto" in src
    assert "self-start sm:self-auto min-h-11" in src


def test_owner_request_rows_stack_and_primary_button_is_tappable():
    src = _read("frontend/src/pages/OwnerCareLedger.jsx")
    assert "min-h-11 w-full sm:w-auto" in src
    assert "flex flex-col sm:flex-row sm:items-center sm:justify-between" in src
    assert "text-equine-silver/85 break-words" in src
    assert "owner-request-draft-restored" in src


def test_admin_horse_drawer_wraps_long_values_and_uses_mobile_severity_grid():
    src = _read("frontend/src/pages/admin/AdminHorses.jsx")
    assert "admin-horses-mobile-cards" in src
    assert "break-all" in src
    assert "grid grid-cols-1 sm:grid-cols-3" in src
    assert "pb-[calc(1.25rem+env(safe-area-inset-bottom))]" in src


def test_admin_horses_stays_on_approved_palette():
    src = _read("frontend/src/pages/admin/AdminHorses.jsx")
    forbidden = re.compile(
        r"\b(?:bg|text|border)-(?:red|amber|green|yellow|blue|indigo|violet|"
        r"purple|pink|rose|teal|cyan|emerald|lime|orange|sky|fuchsia)-\d+"
    )
    assert not forbidden.search(src)

