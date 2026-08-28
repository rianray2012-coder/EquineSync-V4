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
    ]:
        assert f'"{lane}"' in source


def test_ai_reviewer_checklist_has_stable_test_ids():
    source = _source()

    assert 'data-testid="ai-draft-review-checklist"' in source
    assert "data-testid={`ai-draft-review-check-${item.toLowerCase()" in source
    for checklist_item in [
        "Confirm the source belongs to the current barn or user context.",
        "Edit or reject uncertain line items, names, quantities, dates, and prices.",
        "Treat health scores and service suggestions as decision support only.",
        "Save final records only from the correct destination workflow.",
    ]:
        assert f'"{checklist_item}"' in source


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
