from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUPERSESSION_NOTE = ROOT / "docs" / "assurance" / "stripe_sandbox_catalog" / "PR70_CURRENT_BASE_STATIC_SUPERSESSION.md"
ENV_PLACEHOLDERS = ROOT / "docs" / "PHASE_15A_ENV_PLACEHOLDERS.md"
BILLING_PROVISIONING = ROOT / "backend" / "core" / "billing_provisioning.py"
STRIPE_CATALOG_TEST = ROOT / "backend" / "tests" / "test_phase15r_stripe_catalog.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_pr70_static_supersession_note_preserves_current_base_boundary():
    text = _read(SUPERSESSION_NOTE)

    required_fragments = [
        "PR #70 Current-Base Static Supersession",
        "PR `#70`",
        "backend/core/stripe_catalog_sync.py",
        "backend/core/stripe_config.py",
        "backend/scripts/sync_stripe_catalog.py",
        "docs/assurance/stripe_sandbox_catalog/stripe_sandbox_catalog_assurance_report.md",
        "backend/core/billing_provisioning.py",
        "backend/tests/test_phase15r_stripe_catalog.py",
        "docs/PHASE_15A_ENV_PLACEHOLDERS.md",
        "static and non-runtime only",
        "Stripe API calls",
        "Stripe live mode",
        "Stripe object mutation",
        "real payment mutation",
        "provider-live activity",
        "deployment",
        "production use",
        "public claims",
        "certification",
        "risk acceptance",
        "Gate 7 closure",
        "final package closure",
        "CONTENT_REMEDIATION_BLOCKED_RETAINED_OPEN",
    ]

    for fragment in required_fragments:
        assert fragment in text


def test_existing_static_guardrails_remain_source_visible():
    env_text = _read(ENV_PLACEHOLDERS)
    provisioning_text = _read(BILLING_PROVISIONING)
    catalog_test_text = _read(STRIPE_CATALOG_TEST)

    assert "The raw `STRIPE_API_KEY` value." in env_text
    assert "No Products/Prices are created at startup in production." in env_text
    assert "Production: STRIPE_API_KEY is required" in provisioning_text
    assert "Production startup: STRIPE_API_KEY missing" in provisioning_text
    assert "LIVE_STRIPE_PRICE_IDS" in catalog_test_text
    assert "LIVE_STRIPE_PRODUCT_IDS" in catalog_test_text
