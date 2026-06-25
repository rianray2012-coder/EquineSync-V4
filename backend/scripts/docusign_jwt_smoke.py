"""Build-Next-6D DocuSign JWT smoke test.

Backend-only verification that the sandbox integration key, API user GUID,
account id, RSA private key, and one-time consent are aligned. This script asks
DocuSign for an access token and never creates envelopes, signing URLs, provider
webhooks, or signed-document storage.

Usage:
    cd <repo-root>
    python -m backend.scripts.docusign_jwt_smoke
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import jwt
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.document_signing import (  # noqa: E402
    docusign_missing_required_env,
    load_docusign_private_key,
)

JWT_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:jwt-bearer"
DEFAULT_AUTH_SERVER = "account-d.docusign.com"


def _parse_args():
    p = argparse.ArgumentParser(description="Run a safe DocuSign sandbox JWT token smoke test.")
    p.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP timeout in seconds. Default: 15.",
    )
    return p.parse_args()


def _auth_server() -> str:
    server = (os.environ.get("DOCUSIGN_AUTH_SERVER") or DEFAULT_AUTH_SERVER).strip()
    server = server.removeprefix("https://").removeprefix("http://").strip("/")
    return server or DEFAULT_AUTH_SERVER


def _build_assertion(auth_server: str) -> str:
    now = int(time.time())
    claims = {
        "iss": os.environ["DOCUSIGN_INTEGRATION_KEY"].strip(),
        "sub": os.environ["DOCUSIGN_USER_ID"].strip(),
        "aud": auth_server,
        "iat": now,
        "exp": now + 3600,
        "scope": "signature impersonation",
    }
    private_key = load_docusign_private_key(os.environ)
    return jwt.encode(claims, private_key, algorithm="RS256")


def _account_id_verified(auth_server: str, access_token: str, timeout: int) -> bool:
    account_id = os.environ["DOCUSIGN_ACCOUNT_ID"].strip()
    response = requests.get(
        f"https://{auth_server}/oauth/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=timeout,
    )
    if response.status_code != 200:
        return False
    try:
        payload = response.json()
    except ValueError:
        return False
    return any(str(row.get("account_id") or "") == account_id for row in payload.get("accounts") or [])


def main() -> int:
    args = _parse_args()
    missing = docusign_missing_required_env(os.environ)
    if missing:
        print("DocuSign JWT smoke: configuration incomplete", file=sys.stderr)
        for key in missing:
            print(f"- missing: {key}", file=sys.stderr)
        return 2

    auth_server = _auth_server()
    token_url = f"https://{auth_server}/oauth/token"
    try:
        assertion = _build_assertion(auth_server)
        response = requests.post(
            token_url,
            data={"grant_type": JWT_GRANT_TYPE, "assertion": assertion},
            timeout=args.timeout,
        )
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print("DocuSign JWT smoke: request failed", file=sys.stderr)
        print(f"- error_type: {type(exc).__name__}", file=sys.stderr)
        return 3

    try:
        payload = response.json()
    except ValueError:
        payload = {}

    if response.status_code != 200 or not payload.get("access_token"):
        print("DocuSign JWT smoke: token request failed", file=sys.stderr)
        print(f"- status_code: {response.status_code}", file=sys.stderr)
        if payload.get("error"):
            print(f"- error: {payload.get('error')}", file=sys.stderr)
        if payload.get("error_description"):
            print(f"- error_description: {payload.get('error_description')}", file=sys.stderr)
        return 4

    access_token = payload["access_token"]
    try:
        account_verified = _account_id_verified(auth_server, access_token, args.timeout)
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print("DocuSign JWT smoke: account verification failed", file=sys.stderr)
        print(f"- error_type: {type(exc).__name__}", file=sys.stderr)
        return 5
    if not account_verified:
        print("DocuSign JWT smoke: account verification failed", file=sys.stderr)
        print("- account_id_verified: false", file=sys.stderr)
        return 6

    print("DocuSign JWT smoke: OK")
    print(f"- auth_server: {auth_server}")
    print("- access_token_received: true")
    print("- account_id_verified: true")
    print(f"- token_type: {payload.get('token_type') or 'Bearer'}")
    print(f"- expires_in: {payload.get('expires_in')}")
    print("- envelope_creation_attempted: false")
    print("- secrets_printed: false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
