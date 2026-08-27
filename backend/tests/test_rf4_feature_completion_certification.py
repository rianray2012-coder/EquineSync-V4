from __future__ import annotations

from pathlib import Path

from core.rf4_feature_completion_certification import (
    ALLOWED_CLASSIFICATIONS,
    DIRECT_SURFACE_CLASSIFICATIONS,
    FEATURE_MODULE_CLASSIFICATIONS,
    build_rf4_certification,
    render_rf4_report,
)
from routes.backlog import MODULES


ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rf4_classifies_every_feature_module_key():
    assert sorted(FEATURE_MODULE_CLASSIFICATIONS) == sorted(MODULES)
    assert set(FEATURE_MODULE_CLASSIFICATIONS.values()).issubset(ALLOWED_CLASSIFICATIONS)


def test_rf4_direct_surfaces_are_routed_and_classified():
    app_routes = _read("frontend/src/App.js")

    assert DIRECT_SURFACE_CLASSIFICATIONS
    for route, classification in DIRECT_SURFACE_CLASSIFICATIONS.items():
        assert classification in ALLOWED_CLASSIFICATIONS
        assert f'path="{route}"' in app_routes


def test_rf4_role_navigation_does_not_expose_generic_feature_shells():
    role_navigation = _read("frontend/src/lib/roleNavigation.js")

    assert "FeatureWorkspace" not in role_navigation
    assert "/mobile-readiness" not in role_navigation
    assert "/group-messaging" not in role_navigation
    assert "/ai-automation" not in role_navigation
    assert "/staff-tasks" not in role_navigation


def test_rf4_truth_labels_manifest_delivery_signature_and_mobile_readiness():
    advanced_reports = _read("frontend/src/pages/AdvancedReports.jsx")
    group_messaging = _read("frontend/src/pages/GroupMessaging.jsx")
    forms_signatures = _read("frontend/src/pages/FormsSignatures.jsx")
    integrations = _read("frontend/src/pages/Integrations.jsx")
    mobile_readiness = _read("frontend/src/pages/MobileReadiness.jsx")
    backlog = _read("backend/routes/backlog.py")

    assert "Excel manifest" in advanced_reports
    assert "PDF manifest" in advanced_reports
    assert "Export manifests:" in advanced_reports
    assert "download_format" in backlog

    assert "push-preview metadata" in group_messaging
    assert "without sending external push notifications" in group_messaging
    assert "logged locally" in group_messaging
    assert "Log locally" in group_messaging
    assert "Local communication log" in group_messaging
    assert 'delivery_status": "preview_only"' in backlog

    assert "Track local acknowledgement records" in forms_signatures
    assert "No signing link is generated" in forms_signatures
    assert "ready locally" in forms_signatures
    assert "acknowledged locally" in forms_signatures
    assert "Record acknowledgement" in forms_signatures

    assert "Credentials and native app tokens are intentionally not stored here" in integrations
    assert "Record connected" in integrations

    assert "Limited field-recovery queue shape" in mobile_readiness
    assert "Stall-card identification" in mobile_readiness
    assert "Native background sync" in backlog


def test_rf4_ai_and_staff_task_boundaries_are_certified_not_expanded():
    ai_automation = _read("frontend/src/pages/AiAutomation.jsx")
    staff_tasks = _read("frontend/src/pages/StaffTasks.jsx")

    assert "before anything is approved" in ai_automation
    assert "review-first automation item" in ai_automation
    assert "auto_apply" not in ai_automation
    assert "Task Assignments" in staff_tasks
    assert "handoff notes" in staff_tasks


def test_rf4_user_facing_phase_and_placeholder_copy_is_removed():
    admin_placeholder = _read("frontend/src/pages/admin/AdminPlaceholder.jsx")
    role_intake = _read("frontend/src/pages/RoleIntake.jsx")

    assert "access is read-only here" in admin_placeholder
    assert "Settings changes remain restricted until an approved workflow is connected" in admin_placeholder
    assert "Wires up in" not in admin_placeholder
    assert "ships the shell" not in admin_placeholder
    assert "Coming in Admin" not in admin_placeholder
    assert "Facility connection can be completed after intake" in role_intake
    assert "placeholder-only in this phase" not in role_intake


def test_rf4_report_renders_ready_without_blockers():
    report = build_rf4_certification(ROOT)
    rendered = render_rf4_report(report)

    assert report["overall_status"] == "ready"
    assert report["status_counts"].get("blocked", 0) == 0
    assert report["coverage"]["module_count"] == len(MODULES)
    assert report["module_classification_counts"]["readiness"] >= 8
    assert "RF4 Feature Completion Certification Report" in rendered
    assert "## Feature Module Inventory" in rendered
    assert "## Founder Decision Rows" in rendered
    assert "user_facing_phase_copy_removed" in rendered
    assert "RF17 remains responsible" in rendered
