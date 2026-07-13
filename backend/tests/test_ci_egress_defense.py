from __future__ import annotations

import os
import socket
import subprocess
import sys
from pathlib import Path

import pytest

from core.provider_isolation import PROVIDER_CREDENTIAL_VARS, validate_provider_isolation
from backend.scripts.verify_ci_egress_policy import validate_workflows


ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / "backend" / "tests" / "ci_no_egress" / "sitecustomize.py"


def test_workflow_contract_is_deny_by_default():
    assert validate_workflows() == []


@pytest.mark.parametrize(
    "mutation, expected",
    [
        (lambda text: text.replace('STRIPE_API_KEY: ""', 'STRIPE_API_KEY: ${{ secrets.STRIPE_API_KEY }}'), "must not reference repository secrets"),
        (lambda text: text.replace('ALLOW_SANDBOX_PROVIDER_TESTS: "false"', 'ALLOW_SANDBOX_PROVIDER_TESTS: "true"'), "sandbox provider opt-in is prohibited"),
        (lambda text: text.replace('RESEND_API_KEY: ""', ''), "RESEND_API_KEY must be explicitly scrubbed"),
        (lambda text: text + "\n      - run: curl https://example.com\n", "unapproved network-capable command: curl"),
        (lambda text: text.replace("backend/tests/ci_no_egress", "removed/no-egress"), "process-wide no-egress guard is not enabled"),
    ],
)
def test_workflow_policy_corruption_fails_closed(tmp_path, mutation, expected):
    source = (ROOT / ".github" / "workflows" / "provider-isolation.yml").read_text()
    (tmp_path / "corrupt.yml").write_text(mutation(source))
    assert any(expected in error for error in validate_workflows(tmp_path))


def test_all_governed_provider_credentials_are_rejected_when_inherited():
    for variable in PROVIDER_CREDENTIAL_VARS:
        with pytest.raises(RuntimeError):
            validate_provider_isolation({"APP_ENV": "ci", variable: "synthetic-inherited-value"})


def test_process_guard_blocks_external_and_preserves_loopback():
    code = """
import socket
for action in (
    lambda: socket.create_connection(('203.0.113.10', 443), timeout=.01),
    lambda: socket.getaddrinfo('api.stripe.com', 443),
    lambda: socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'probe', ('203.0.113.10', 53)),
):
    try:
        action()
    except RuntimeError as exc:
        assert 'CI egress blocked' in str(exc)
    else:
        raise AssertionError('external egress was not blocked')
listener = socket.socket()
listener.bind(('127.0.0.1', 0))
listener.listen(1)
client = socket.create_connection(listener.getsockname(), timeout=1)
server, _ = listener.accept()
client.close(); server.close(); listener.close()
print('guard-pass')
"""
    result = subprocess.run(
        [sys.executable, "-c", code],
        env={**os.environ, "PYTHONPATH": str(GUARD.parent)},
        capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "guard-pass"


def test_guard_is_loaded_in_child_test_process():
    env_path = str(GUARD.parent)
    result = subprocess.run(
        [sys.executable, "-c", "import socket; socket.create_connection(('203.0.113.10', 443), .01)"],
        env={**os.environ, "PYTHONPATH": env_path}, capture_output=True, text=True, timeout=5,
    )
    assert result.returncode != 0
    assert "CI egress blocked" in result.stderr
