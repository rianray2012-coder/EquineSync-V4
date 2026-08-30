from pathlib import Path


AI_AUTOMATION = Path(__file__).resolve().parents[2] / "frontend" / "src" / "pages" / "AiAutomation.jsx"
PRIMITIVES = Path(__file__).resolve().parents[2] / "frontend" / "src" / "components" / "Primitives.jsx"


def _source() -> str:
    return AI_AUTOMATION.read_text()


def test_ai_reviewer_lanes_have_stable_test_ids():
    source = _source()

    assert "data-testid={`ai-draft-review-lane-${lane.toLowerCase().replace(/[^a-z]+/g, \"-\")}`}" in source
    for lane in [
        "Invoices",
        "Service notes",
        "Ride data",
        "Scheduling notes",
        "Voice transcripts",
        "Photo inventory",
        "Health observations",
    ]:
        assert f'"{lane}"' in source


def test_ai_reviewer_checklist_has_stable_test_ids():
    source = _source()

    assert 'data-testid="ai-draft-review-checklist"' in source
    assert "data-testid={`ai-draft-review-check-${item.toLowerCase()" in source
    for checklist_item in [
        "Confirm the source belongs to the current barn or user context.",
        "Edit or reject uncertain line items, names, quantities, dates, and prices.",
        "Treat health scores and service suggestions as draft decision support only.",
        "Do not use AI health drafts as diagnosis, treatment, medication, emergency triage, or provider-message instructions.",
        "Use official save only for Founder-approved inventory and work-ticket lanes.",
    ]:
        assert f'"{checklist_item}"' in source


def test_health_observation_reviewer_has_draft_only_clinical_boundary_hooks():
    source = _source()

    assert '["health_observation", "Health observation"]' in source
    assert "Organize draft health observations and a review-only health score candidate" in source
    assert 'data-testid={`ai-health-draft-only-boundary-${job.id}`}' in source
    assert 'data-testid={`ai-health-no-diagnosis-boundary-${job.id}`}' in source
    assert 'data-testid={`ai-health-score-candidate-${job.id}`}' in source
    assert 'data-testid={`ai-health-score-save-gated-${job.id}`}' in source
    assert "not a diagnosis, treatment plan, medication instruction, emergency triage decision" in source
    assert "official health-score save remains separately gated" in source
    assert '"health_score"' not in source


def test_status_pill_forwards_test_hook_props():
    source = PRIMITIVES.read_text()

    assert 'dot = false, ...rest' in source
    assert '<span className={`pill ${map[tone]}`} {...rest}>' in source


def test_ai_reviewer_structured_review_sections_have_stable_test_ids():
    source = _source()

    assert 'data-testid={`ai-draft-structured-review-${job.id}`}' in source
    assert 'data-testid={`ai-draft-review-summary-${job.id}`}' in source
    assert 'data-testid={`ai-draft-missing-info-${job.id}`}' in source
    assert 'data-testid={`ai-draft-blocked-actions-${job.id}`}' in source
    assert "Draft Review Summary" in source
    assert "Missing Information" in source
    assert "Blocked Actions" in source


def test_ai_inventory_candidate_reviewer_has_human_confirmed_lane_save_hooks_and_local_actions():
    source = _source()

    assert 'data-testid={`ai-draft-inventory-candidates-${job.id}`}' in source
    assert 'data-testid={`ai-draft-inventory-no-save-${job.id}`}' in source
    assert 'data-testid={`ai-draft-inventory-candidate-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-candidate-name-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-candidate-confidence-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-candidate-disposition-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-mark-reviewed-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-mark-duplicate-${job.id}-${index}`}' in source
    assert 'data-testid={`ai-draft-inventory-mark-rejected-${job.id}-${index}`}' in source
    assert "use the explicit official-save confirmation when this lane is appropriate" in source
    assert "api.post(`/inventory" not in source


def test_ai_official_save_ui_has_explicit_human_confirmation_boundary():
    source = _source()

    assert "OFFICIAL_SAVE_LANES" in source
    assert "inventory_supply" in source
    assert "work_task_repair" in source
    assert "api.post(`/ai/draft-jobs/${job.id}/official-save`" in source
    assert 'data-testid={`ai-draft-official-save-panel-${job.id}`}' in source
    assert 'data-testid={`ai-draft-official-save-open-inventory-${job.id}`}' in source
    assert 'data-testid={`ai-draft-official-save-open-work-${job.id}`}' in source
    assert 'data-testid={`ai-draft-official-save-confirm-${job.id}`}' in source
    assert 'data-testid={`ai-draft-official-save-checkbox-${job.id}`}' in source
    assert 'data-testid={`ai-draft-official-save-confirm-submit-${job.id}`}' in source
    assert "I reviewed this AI draft, confirmed the barn context" in source
    assert "Health, billing, legal, notifications, and calendar changes remain blocked" in source
    assert "disabled={!officialSaveChecked" in source


def test_ai_reviewer_surfaces_budget_guardrail_without_private_source_details():
    source = _source()

    assert 'api.get("/ai/draft-jobs/usage-policy")' in source
    assert 'data-testid="ai-draft-budget-guardrail"' in source
    assert 'data-testid="ai-draft-budget-policy"' in source
    assert 'data-testid="ai-draft-budget-enforcement"' in source
    assert 'data-testid="ai-draft-budget-jobs"' in source
    assert 'data-testid="ai-draft-budget-tokens"' in source
    assert 'data-testid="ai-draft-budget-source-bytes"' in source
    assert "Draft extraction remains review-required, human-confirmed, and budget-gated for pilot use." in source
