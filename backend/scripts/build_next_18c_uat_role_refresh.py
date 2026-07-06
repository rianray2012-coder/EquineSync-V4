"""Build-Next-18C UAT role-refresh proof.

Generates a scrubbed role-refresh preflight report. This script performs
public GET probes only through the BN18B production proof helper. It does not
log in, create sessions, seed accounts, mutate MongoDB, touch providers, or
mark founder acceptance.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.build_next_18c_uat_role_refresh
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

from core.production_environment_proof import (  # noqa: E402
    DEFAULT_API_BASE_URL,
    DEFAULT_FRONTEND_URL,
)
from core.uat_role_refresh_proof import (  # noqa: E402
    build_uat_role_refresh_report,
    render_uat_role_refresh_markdown,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn18c_uat_role_refresh_report.md"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Build-Next-18C UAT role-refresh preflight report."
    )
    parser.add_argument(
        "--frontend-url",
        default=None,
        help=f"Public frontend URL. Default: {DEFAULT_FRONTEND_URL}",
    )
    parser.add_argument(
        "--api-base-url",
        default=None,
        help=f"Public API base URL. Default: {DEFAULT_API_BASE_URL}",
    )
    parser.add_argument(
        "--screenshot-evidence-dir",
        default=None,
        help="Optional local screenshot evidence directory. Does not capture screenshots.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown output path. Default: outputs/bn18c_uat_role_refresh_report.md",
    )
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit 2 when BN18C blockers are present. Default writes evidence and exits 0.",
    )
    return parser.parse_args()


def _apply_optional_env(name: str, value: str | None) -> None:
    if value is not None:
        os.environ[name] = value


def main() -> int:
    args = _parse_args()
    _apply_optional_env("BN18B_FRONTEND_URL", args.frontend_url)
    _apply_optional_env("BN18B_API_BASE_URL", args.api_base_url)
    _apply_optional_env("BN18C_SCREENSHOT_EVIDENCE_DIR", args.screenshot_evidence_dir)

    report = build_uat_role_refresh_report(os.environ)
    markdown = render_uat_role_refresh_markdown(report)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")

    issue_counts = report.get("issue_counts") or {}
    print(f"Build-Next-18C UAT role-refresh report written: {out}")
    print(
        "Summary: "
        f"status={report.get('overall_status')} "
        f"blocker(s)={issue_counts.get('blocker', 0)} "
        f"warning(s)={issue_counts.get('warning', 0)}"
    )
    if args.fail_on_blockers and issue_counts.get("blocker", 0):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
