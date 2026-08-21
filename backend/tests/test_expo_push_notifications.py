import pytest
from pydantic import ValidationError

from notifications import (
    PUSH_PROOF_BODY,
    PushTokenIn,
    _expo_ticket_diagnostics,
    _redact_token_hash,
    _token_hash,
)


def test_expo_push_token_accepts_expo_token_and_redacts_hash():
    token = "ExpoPushToken[aaaaaaaaaaaaaaaaaaaaaa]"
    body = PushTokenIn(expo_push_token=token, platform="IOS", enabled=True)

    assert body.platform == "ios"
    assert _redact_token_hash(token) == _token_hash(token)[:12]
    assert token not in _redact_token_hash(token)


@pytest.mark.parametrize(
    "token",
    [
        "plain-token",
        "ExponentPushToken",
        "ExpoPushToken",
        "mailto:test@example.com",
    ],
)
def test_expo_push_token_rejects_non_expo_tokens(token):
    with pytest.raises(ValidationError):
        PushTokenIn(expo_push_token=token, platform="ios")


def test_founder_push_proof_copy_stays_generic():
    forbidden_fragments = [
        "diagnosis",
        "medication",
        "dose",
        "injury",
        "minor",
        "payment",
        "invoice",
        "signature",
    ]

    lowered = PUSH_PROOF_BODY.lower()
    for fragment in forbidden_fragments:
        assert fragment not in lowered
    assert "open EquineSync".lower() in lowered


def test_expo_ticket_diagnostics_keeps_only_safe_error_fields():
    ticket = {
        "status": "error",
        "message": "DeviceNotRegistered",
        "details": {
            "error": "DeviceNotRegistered",
            "expoPushToken": "ExpoPushToken[secret]",
        },
        "to": "ExpoPushToken[secret]",
    }

    diagnostics = _expo_ticket_diagnostics(ticket)

    assert diagnostics == {
        "ticket_error": "DeviceNotRegistered",
        "ticket_details_error": "DeviceNotRegistered",
    }
    assert "ExpoPushToken[secret]" not in repr(diagnostics)
