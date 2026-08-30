"""Private-app premium polish regression checks.

These source checks keep the PP-1/PP-2 pass focused on user-visible polish:
role dashboards should read like product surfaces, support inputs should remain
legible on light cards, and gated owner routing must stay gated.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend" / "src"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_owner_dashboard_uses_premium_pending_connection_copy_without_route():
    src = _read(FRONTEND / "features" / "dashboards" / "PersonalDashboard.jsx")

    assert 'primary: { label: "Facility Connection Pending", to: null }' in src
    assert "Owner Portal Pending" not in src
    assert 'to: "/owner-portal"' not in src
    assert "Open Owner Portal" not in src


def test_private_dashboard_empty_states_are_role_specific_not_placeholder_notes():
    sources = [
        _read(FRONTEND / "features" / "dashboards" / "TrainerDashboard.jsx"),
        _read(FRONTEND / "features" / "dashboards" / "ServiceProviderDashboard.jsx"),
        _read(FRONTEND / "components" / "today" / "TodayGroup.jsx"),
    ]
    text = "\n".join(sources)

    for expected in [
        "Lessons assigned to you will appear here with rider, horse, time, and focus notes.",
        "Active horse goals and progression plans will appear here once assigned.",
        "Facility-approved horse access will appear here with only the context needed for care.",
        "Visit notes you author will appear here for facility review and follow-up.",
        "No tasks in this group right now.",
    ]:
        assert expected in text

    for drift in [
        "No trainer-linked lessons scheduled.",
        "No trainer-linked training logs yet.",
        "No grant-scoped vet records yet.",
        "Nothing here. A quiet stretch.",
    ]:
        assert drift not in text


def test_support_form_uses_light_legible_private_app_fields():
    src = _read(FRONTEND / "pages" / "Support.jsx")

    assert "const fieldClass =" in src
    assert "bg-white" in src
    assert "text-equine-ink" in src
    assert "placeholder:text-equine-inkSoft" in src
    assert "bg-equine-navy/50" not in src
    assert "placeholder:text-equine-platinum/35" not in src

