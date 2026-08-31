"""Landing page guardrail for the horse ledger/passport hero message."""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LANDING = ROOT / "frontend" / "src" / "pages" / "Landing.jsx"


def test_landing_names_horse_ledger_and_passport_as_hero_item():
    text = " ".join(LANDING.read_text(encoding="utf-8").split())

    for phrase in [
        "horse ledger and horse passport",
        "lifetime record for modern horse care",
        "Horse Ledger & Passport",
        "lifelong care history",
        "the next owner is not starting from a blank page",
        "future owners are not forced to rebuild health, training, provider, and document context from a blank page",
    ]:
        assert phrase in text


def test_landing_keeps_passport_message_inside_existing_signup_boundaries():
    text = " ".join(LANDING.read_text(encoding="utf-8").split())

    for phrase in [
        "Public signup supports owners, barn operators, trainers, and service providers.",
        "Rider, guardian, and staff accounts remain invitation-based.",
    ]:
        assert phrase in text

    forbidden_claims = [
        "passport transfer is live",
        "buyer transfer is live",
        "ownership transfer is live",
        "records export is live",
        "provider access is live",
        "payments are live",
        "signatures are live",
        "multi-facility switching is live",
    ]
    for phrase in forbidden_claims:
        assert phrase not in text
