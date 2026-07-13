"""Verify repository CI workflows preserve the ordinary-test no-egress contract."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"
REQUIRED_SCRUBBED = (
    "STRIPE_API_KEY", "STRIPE_WEBHOOK_SECRET", "DOCUSIGN_ACCESS_TOKEN",
    "DOCUSIGN_CLIENT_SECRET", "DOCUSIGN_PRIVATE_KEY", "DOCUSIGN_PRIVATE_KEY_PATH",
    "DOCUSIGN_WEBHOOK_SECRET",
    "RESEND_API_KEY", "SENDGRID_API_KEY", "TWILIO_AUTH_TOKEN", "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", "GOOGLE_CLIENT_SECRET",
    "MICROSOFT_CLIENT_SECRET", "FIREBASE_PRIVATE_KEY", "SENTRY_AUTH_TOKEN",
)
UNAPPROVED_RUN_TOKENS = (
    "curl ", "wget ", "npm publish", "yarn publish", "vercel deploy",
    "render deploy", "gh api", "docker push", "kubectl apply",
)


def validate_workflows(root: Path = WORKFLOWS) -> list[str]:
    errors: list[str] = []
    files = sorted([*root.glob("*.yml"), *root.glob("*.yaml")])
    if not files:
        return ["no CI workflows found"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            rel = path.name
        if "contents: read" not in text:
            errors.append(f"{rel}: missing least-privilege contents: read")
        if re.search(r"permissions:\s*(?:write-all|read-all)", text):
            errors.append(f"{rel}: broad workflow permissions are prohibited")
        if "${{ secrets." in text:
            errors.append(f"{rel}: ordinary CI must not reference repository secrets")
        if "pull_request_target:" in text:
            errors.append(f"{rel}: pull_request_target is prohibited for ordinary CI")
        if re.search(r"ALLOW_SANDBOX_PROVIDER_TESTS:\s*['\"]?(?:1|true|yes|on)", text, re.I):
            errors.append(f"{rel}: sandbox provider opt-in is prohibited in ordinary CI")
        for variable in REQUIRED_SCRUBBED:
            if not re.search(rf"^\s+{re.escape(variable)}:\s*(?:['\"]{{2}})?\s*$", text, re.M):
                errors.append(f"{rel}: {variable} must be explicitly scrubbed")
        lowered = text.lower()
        for token in UNAPPROVED_RUN_TOKENS:
            if token in lowered and f"ci-egress-authorized: {token.strip()}" not in lowered:
                errors.append(f"{rel}: unapproved network-capable command: {token.strip()}")
        if "backend/tests/ci_no_egress" not in text:
            errors.append(f"{rel}: process-wide no-egress guard is not enabled")
        if "unshare --net" not in text:
            errors.append(f"{rel}: kernel network-namespace proof is missing")
        for action in re.findall(r"^\s*-\s+uses:\s*([^\s#]+)", text, re.M):
            if not action.startswith(("actions/checkout@", "actions/setup-python@")):
                errors.append(f"{rel}: action is not on the bootstrap allowlist: {action}")
    return errors


def main() -> int:
    errors = validate_workflows()
    if errors:
        print("CI egress policy: FAILED")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    count = len([*WORKFLOWS.glob("*.yml"), *WORKFLOWS.glob("*.yaml")])
    print(f"CI egress policy: PASS ({count} workflows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
