"""Build-Next-18B production environment proof.

Generates a scrubbed launch-trust report from public production probes and
operator-supplied evidence labels. It does not mutate providers, MongoDB,
users, billing, webhooks, documents, UAT accounts, or acceptance rows.

Usage:
    cd <repo-root>
    ./.venv/bin/python -m backend.scripts.build_next_18b_production_environment_proof
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
    build_production_environment_proof,
    render_production_environment_proof_markdown,
)


DEFAULT_OUTPUT = ROOT / "outputs" / "bn18b_production_environment_proof_report.md"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate the Build-Next-18B production environment proof report."
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
        "--database-label",
        default=None,
        help="Sanitized database identity label. Do not pass a MongoDB URI.",
    )
    parser.add_argument(
        "--vercel-deploy-marker",
        default=None,
        help="Operator-provided Vercel deploy marker or commit label.",
    )
    parser.add_argument(
        "--render-deploy-marker",
        default=None,
        help="Operator-provided Render deploy marker or commit label.",
    )
    parser.add_argument(
        "--rollback-evidence",
        default=None,
        help="Operator-provided rollback evidence label.",
    )
    parser.add_argument(
        "--backup-evidence",
        default=None,
        help="Operator-provided backup evidence label.",
    )
    parser.add_argument(
        "--monitoring-evidence",
        default=None,
        help="Operator-provided monitoring/log evidence label.",
    )
    parser.add_argument(
        "--startup-log-evidence",
        default=None,
        help="Operator-provided startup-log evidence label for background loops.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Markdown output path. Default: outputs/bn18b_production_environment_proof_report.md",
    )
    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help="Exit 2 when production environment blockers are present. Default writes evidence and exits 0.",
    )
    return parser.parse_args()


def _apply_optional_env(name: str, value: str | None) -> None:
    if value is not None:
        os.environ[name] = value


def main() -> int:
    args = _parse_args()
    _apply_optional_env("BN18B_FRONTEND_URL", args.frontend_url)
    _apply_optional_env("BN18B_API_BASE_URL", args.api_base_url)
    _apply_optional_env("BN18B_DATABASE_LABEL", args.database_label)
    _apply_optional_env("BN18B_VERCEL_DEPLOY_MARKER", args.vercel_deploy_marker)
    _apply_optional_env("BN18B_RENDER_DEPLOY_MARKER", args.render_deploy_marker)
    _apply_optional_env("BN18B_ROLLBACK_EVIDENCE", args.rollback_evidence)
    _apply_optional_env("BN18B_BACKUP_EVIDENCE", args.backup_evidence)
    _apply_optional_env("BN18B_MONITORING_EVIDENCE", args.monitoring_evidence)
    _apply_optional_env("BN18B_STARTUP_LOG_EVIDENCE", args.startup_log_evidence)

    report = build_production_environment_proof(os.environ)
    markdown = render_production_environment_proof_markdown(report)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")

    issue_counts = report.get("issue_counts") or {}
    print(f"Build-Next-18B production environment proof written: {out}")
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
