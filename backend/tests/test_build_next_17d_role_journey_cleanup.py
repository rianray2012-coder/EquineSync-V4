"""Build-Next-17D - targeted role journey cleanup guards.

BN17D is a narrow cleanup phase for the findings recorded by BN17C. These
tests intentionally stay source-level: they prove direct legacy product routes
are no longer plain authenticated routes, unsafe role nav no longer links into
operational messaging, and launch-hostile copy has been removed.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"
REPORT = ROOT / "outputs" / "bn17d_role_journey_cleanup_evidence.md"
README = ROOT / "BUILD_NEXT_17D_ROLE_JOURNEY_CLEANUP_README.md"


def _read(path: Path) -> str:
    return path.read_text()


def _section(src: str, export_name: str) -> str:
    start = src.index(f"export const {export_name}")
    next_export = src.find("\nexport const ", start + 1)
    return src[start:] if next_export == -1 else src[start:next_export]


def test_bn17d_direct_legacy_product_routes_are_role_gated():
    app = _read(FRONTEND / "App.js")

    expected = {
        "/today": ("Today", "barnOperations"),
        "/horses": ("Horses", "horseDirectory"),
        "/horses/:id": ("HorseProfile", "horseDirectory"),
        "/riders": ("Riders", "facilityDirectory"),
        "/owners": ("Owners", "facilityDirectory"),
        "/lessons": ("Lessons", "trainingWorkflow"),
        "/training": ("Training", "trainingWorkflow"),
        "/health": ("Health", "careWorkflow"),
        "/stall-rest": ("Rehab", "careWorkflow"),
        "/medications": ("Medications", "careWorkflow"),
        "/turnout": ("Turnout", "careWorkflow"),
        "/feed": ("Feed", "careWorkflow"),
        "/inventory": ("Inventory", "inventoryWorkflow"),
        "/billing/success": ("SubscriptionSuccess", "checkoutReturn"),
        "/incidents": ("Incidents", "careWorkflow"),
        "/messaging": ("Messaging", "operationalMessaging"),
        "/settings": ("Settings", "accountSettings"),
    }

    assert "const BN17D_DIRECT_ROUTE_ROLES" in app
    for path, (component, role_key) in expected.items():
        gated = f'path="{path}" element={{permit(<{component} />, BN17D_DIRECT_ROUTE_ROLES.{role_key})}}'
        plain = f'path="{path}" element={{<{component} />}}'
        assert gated in app
        assert plain not in app


def test_owner_guardian_provider_nav_no_longer_links_to_operational_messaging():
    nav = _read(FRONTEND / "lib" / "roleNavigation.js")

    for export_name in [
        "OWNER_NAVIGATION",
        "INDIVIDUAL_OWNER_NAVIGATION",
        "GUARDIAN_NAVIGATION",
        "SERVICE_PROVIDER_NAVIGATION",
        "DEFAULT_NAVIGATION",
    ]:
        assert 'item("/messaging", "Messages", "messages")' not in _section(nav, export_name)

    assert 'items: [item("/admin/portal/settings", "Profile", "settings")]' in _section(nav, "PLATFORM_NAVIGATION")
    assert 'item("/messaging", "Messages", "messages")' in _section(nav, "FACILITY_ADMIN_NAVIGATION")
    assert 'item("/messaging", "Messages", "messages")' in _section(nav, "MANAGER_NAVIGATION")
    assert 'item("/messaging", "Messages", "messages")' in _section(nav, "TRAINER_NAVIGATION")
    assert 'item("/messaging", "Messages", "messages")' in _section(nav, "STAFF_NAVIGATION")


def test_bn17d_production_copy_cleanup_removes_flagged_strings():
    sources = [
        FRONTEND / "components" / "onboarding" / "StaffStep.jsx",
        FRONTEND / "components" / "NotificationPrefsCard.jsx",
        FRONTEND / "pages" / "admin" / "AdminTopbar.jsx",
        FRONTEND / "pages" / "FeatureWorkspace.jsx",
        FRONTEND / "pages" / "FormsSignatures.jsx",
    ]
    combined = "\n".join(_read(path) for path in sources)

    for forbidden in [
        "Email delivery is in dev mode",
        "backend/.env",
        "magic link",
        "push is coming soon",
        "coming in Admin-2",
        "workflow shell",
        "Live envelope sending remains gated",
        "later phase",
    ]:
        assert forbidden not in combined

    assert "Invite link available" in combined
    assert "Email delivery is not available for this invite." in combined
    assert "Additional delivery channels appear here after they are configured." in combined
    assert "Envelope sending appears only after the signature provider is enabled for this account." in combined


def test_bn17d_evidence_and_readme_record_non_expansionary_scope():
    report = _read(REPORT)
    readme = _read(README)

    for src in [report, readme]:
        assert "BN17D-ROUTE-1" in src
        assert "BN17D-COPY-1" in src
        assert "BN17D-FEATURE-1" in src
        assert "No backend route/schema/auth/permission/privacy changes." in src
        assert "No new product behavior." in src
        assert "BN18A" in src
