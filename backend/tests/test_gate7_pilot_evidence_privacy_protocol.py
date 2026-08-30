from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ROOT / "docs" / "PILOT_EVIDENCE_PRIVACY_PROTOCOL.md"


def _protocol_text() -> str:
    return PROTOCOL.read_text(encoding="utf-8")


def _normalized_protocol_text() -> str:
    return re.sub(r"\s+", " ", _protocol_text())


def test_pilot_evidence_privacy_protocol_exists():
    assert PROTOCOL.exists()
    assert PROTOCOL.stat().st_size > 0


def test_protocol_carries_required_operator_sections():
    text = _protocol_text()
    required_sections = [
        "# Pilot Evidence Privacy Protocol",
        "## Evidence Owner And Access",
        "## Allowed Pilot Evidence",
        "## Prohibited Pilot Evidence",
        "## Required Redaction Rules",
        "## Storage Locations",
        "## Retention And Disposition",
        "## Support Evidence Handling",
        "## Owner Documents And Legal Evidence",
        "## Payment And Tax Evidence",
        "## Minors, Guardians, Riders, And Safety",
        "## Horse Health And Barn Operations",
        "## AI Evidence Handling",
        "## Privacy Incident Escalation",
        "## Retained Activation Stop Rules",
    ]

    for section in required_sections:
        assert section in text


def test_protocol_front_loads_gate7_privacy_decisions():
    text = _normalized_protocol_text()
    required_fragments = [
        "Raw pilot evidence may be viewed only by the founder",
        "Redacted Gate 7 evidence may be stored under `outputs/`",
        "Raw evidence must not be bundled into implementation PRs.",
        "Credential files, environment files, provider keys, and runtime secrets must remain in ignored secret locations",
        "Do not use pilot evidence for marketing, sales demos, model training, provider expansion, public launch claims, or unrelated analytics",
        "Support ticket descriptions and internal notes may contain sensitive free text.",
        "audit metadata, PR descriptions, issue titles, and public-facing evidence must stay routing-only and redacted",
        "Owner document evidence must prove owner-safe status projection without copying document contents.",
        "DocuSign sandbox proof does not authorize production envelope sending.",
        "Adobe Sign remains deferred.",
        "Pilot billing evidence must show founder-granted free/manual access and no payment collection.",
        "Evidence involving minors, guardians, riders, emergency contacts, household relationships, custody, safeguarding, or location patterns must use the minimum necessary proof.",
        "Do not include real horse medical details, owner-hidden barn notes, staff performance details, private schedules, or facility security patterns in shared evidence.",
        "`official_records_written=false`",
        "Preserve the minimum necessary evidence, redact before broad sharing, freeze the smallest unsafe workflow",
    ]

    for fragment in required_fragments:
        assert fragment in text


def test_protocol_preserves_retained_activation_stop_rules():
    text = _protocol_text()
    retained_limits = [
        "Production deployment.",
        "Customer-facing live Checkout.",
        "Live payment collection.",
        "Stripe Customer Portal activation.",
        "Live automatic tax activation.",
        "Legal signature sends.",
        "DocuSign production envelopes.",
        "Adobe Sign activation.",
        "Provider-live activation or public directory expansion.",
        "Official AI save authority.",
        "AI autonomous mutation.",
    ]

    for limit in retained_limits:
        assert limit in text


def test_protocol_does_not_contain_secret_shapes():
    text = _protocol_text()
    forbidden_patterns = [
        r"sk_(live|test)_[A-Za-z0-9]{16,}",
        r"rk_(live|test)_[A-Za-z0-9]{16,}",
        r"whsec_[A-Za-z0-9]{16,}",
        r"mongodb(\\+srv)?://",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"eyJ[A-Za-z0-9_-]{20,}\\.[A-Za-z0-9_-]{20,}\\.[A-Za-z0-9_-]{20,}",
        r"https://checkout\\.stripe\\.com/[A-Za-z0-9/_?=&.-]+",
    ]

    for pattern in forbidden_patterns:
        assert not re.search(pattern, text)
