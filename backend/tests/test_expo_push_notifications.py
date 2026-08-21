from pathlib import Path

import pytest
from pydantic import ValidationError

from notifications import PUSH_PROOF_BODY, PushTokenIn, _redact_token_hash, _token_hash


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


def test_mobile_push_panel_exposes_proof_controls_without_token_body():
    src = Path(__file__).resolve().parents[2] / "mobile" / "App.tsx"
    text = src.read_text()

    assert "testID=\"push-proof-panel\"" in text
    assert "testID=\"push-register-button\"" in text
    assert "testID=\"push-proof-send-button\"" in text
    assert "testID=\"push-disable-button\"" in text
    assert "token_hash={pushTokenHash || 'not_registered'}" in text
    assert "expo_push_token" in text
