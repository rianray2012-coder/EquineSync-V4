"""Read-only UAT role-refresh proof helpers for Build-Next-18C.

BN18C refreshes role-based UAT only after the production environment gate is
clean. This helper intentionally performs public GET probes only through the
BN18B production proof helper and never mutates users, sessions, providers,
MongoDB, founder-acceptance state, or product behavior.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from core.production_environment_proof import (
    DEFAULT_API_BASE_URL,
    DEFAULT_FRONTEND_URL,
    Fetcher,
    build_production_environment_proof,
    fetch_public_url,
)


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"
TEXT_EVIDENCE_MIN_CHARS = 80
TEXT_EVIDENCE_MIN_WORDS = 10
PLACEHOLDER_TEXT = {"placeholder", "todo", "tbd", "n/a", "na", "test"}


ROLE_ROWS: list[dict[str, Any]] = [
    {
        "tp_row": "TP-1",
        "evidence_row": "UAT-R1",
        "role": "platform_admin",
        "expected_surface": "Admin Portal dashboard",
        "screenshot": "uat-r1-platform-admin.png",
    },
    {
        "tp_row": "TP-2",
        "evidence_row": "UAT-R2a / UAT-R2b",
        "role": "admin / barn_owner",
        "expected_surface": "facility dashboard and barn-owner facility dashboard",
        "screenshot": "uat-r2a-facility-admin.png, uat-r2b-barn-owner.png",
        "evidence_files": [
            "uat-r2a-facility-admin.png",
            "uat-r2b-barn-owner.png",
        ],
    },
    {
        "tp_row": "TP-3",
        "evidence_row": "UAT-R3",
        "role": "barn_manager",
        "expected_surface": "manager facility dashboard",
        "screenshot": "uat-r3-barn-manager.png",
    },
    {
        "tp_row": "TP-4",
        "evidence_row": "UAT-R4a",
        "role": "groom",
        "expected_surface": "staff Today's Pulse / Operational Pulse",
        "screenshot": "uat-r4a-groom.png",
    },
    {
        "tp_row": "TP-5",
        "evidence_row": "BN13M-T1",
        "role": "trainer",
        "expected_surface": "trainer facility dashboard or trainer-safe role home",
        "screenshot": "bn13m-t1-trainer.png",
    },
    {
        "tp_row": "TP-6",
        "evidence_row": "BN13M-W1",
        "role": "working_student",
        "expected_surface": "staff Today's Pulse / working-student-safe role home",
        "screenshot": "bn13m-w1-working-student.png",
    },
    {
        "tp_row": "TP-7",
        "evidence_row": "UAT-R5",
        "role": "horse_owner",
        "expected_surface": "owner portal for linked horse",
        "screenshot": "uat-r5-horse-owner.png",
    },
    {
        "tp_row": "TP-8",
        "evidence_row": "UAT-R6",
        "role": "parent",
        "expected_surface": "guardian / minor rider dashboard",
        "screenshot": "uat-r6-guardian-parent.png",
    },
    {
        "tp_row": "TP-9",
        "evidence_row": "UAT-R7",
        "role": "rider",
        "expected_surface": "rider / lesson participant dashboard",
        "screenshot": "uat-r7-rider.png",
    },
    {
        "tp_row": "TP-10",
        "evidence_row": "UAT-R8",
        "role": "standalone horse_owner",
        "expected_surface": "standalone individual owner dashboard",
        "screenshot": "uat-r8-individual-owner.png",
    },
    {
        "tp_row": "TP-11",
        "evidence_row": "Privacy exclusions",
        "role": "all role rows",
        "expected_surface": "screenshot-only privacy sweep",
        "screenshot": "privacy-sweep.md",
    },
]


def _issue_counts(issues: list[Mapping[str, str]]) -> dict[str, int]:
    return dict(sorted(Counter(issue["severity"] for issue in issues).items()))


def _blocking_issues(proof: Mapping[str, Any]) -> list[Mapping[str, str]]:
    return [
        issue
        for issue in proof.get("issues") or []
        if issue.get("severity") == "blocker"
    ]


def _evidence_files(row: Mapping[str, Any]) -> tuple[str, ...]:
    files = row.get("evidence_files")
    if files:
        return tuple(str(file) for file in files)
    return (str(row["screenshot"]),)


def _valid_image_evidence(path: Path) -> bool:
    if not path.is_file():
        return False
    suffix = path.suffix.lower()
    try:
        head = path.read_bytes()[:16]
    except OSError:
        return False
    if suffix == ".png":
        return path.stat().st_size > len(PNG_SIGNATURE) and head.startswith(PNG_SIGNATURE)
    if suffix in {".jpg", ".jpeg"}:
        return path.stat().st_size > len(JPEG_SIGNATURE) and head.startswith(JPEG_SIGNATURE)
    return False


def _valid_text_evidence(path: Path) -> bool:
    if not path.is_file() or path.suffix.lower() != ".md":
        return False
    try:
        text = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        text = path.read_text(errors="ignore").strip()
    except OSError:
        return False
    normalized = text.lower().strip()
    if normalized in PLACEHOLDER_TEXT:
        return False
    return (
        len(text) >= TEXT_EVIDENCE_MIN_CHARS
        and len(text.split()) >= TEXT_EVIDENCE_MIN_WORDS
    )


def _invalid_evidence_files(evidence_dir: str | None, row: Mapping[str, Any]) -> list[str]:
    if not evidence_dir:
        return list(_evidence_files(row))
    invalid: list[str] = []
    for filename in _evidence_files(row):
        path = Path(evidence_dir) / filename
        suffix = path.suffix.lower()
        valid = (
            _valid_text_evidence(path)
            if suffix == ".md"
            else _valid_image_evidence(path)
        )
        if not valid:
            invalid.append(filename)
    return invalid


def _role_status(
    *,
    gate_blocked: bool,
    row: Mapping[str, Any],
    evidence_dir: str | None,
) -> tuple[str, str]:
    if gate_blocked:
        return (
            "blocked",
            "BN18B production API health/readiness gate is not clean; credentialed role UAT is deferred.",
        )

    invalid_files = _invalid_evidence_files(evidence_dir, row)
    if not invalid_files:
        return (
            "evidence_captured",
            "Required screenshot/privacy evidence is present and file signatures validate. Founder acceptance remains separate.",
        )

    return (
        "pending_capture",
        "Production gate is clean, but required BN18C evidence is missing or invalid: "
        + ", ".join(invalid_files),
    )


def build_uat_role_refresh_report(
    env: Mapping[str, str],
    *,
    fetcher: Fetcher = fetch_public_url,
) -> dict[str, Any]:
    """Build the BN18C role-refresh report.

    The report never claims role UAT passed unless the production gate is clean
    and screenshot evidence is present. Even then, founder acceptance remains
    out of scope.
    """
    production_proof = build_production_environment_proof(env, fetcher=fetcher)
    blockers = _blocking_issues(production_proof)
    gate_blocked = bool(blockers)
    evidence_dir = (env.get("BN18C_SCREENSHOT_EVIDENCE_DIR") or "").strip() or None

    role_rows: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []
    if gate_blocked:
        issues.append({
            "severity": "blocker",
            "area": "production_gate",
            "kind": "bn18b_gate_blocked",
            "message": "BN18C cannot run credentialed role UAT until production API health/readiness proof is clean.",
        })

    for row in ROLE_ROWS:
        status, reason = _role_status(
            gate_blocked=gate_blocked,
            row=row,
            evidence_dir=evidence_dir,
        )
        if status == "pending_capture":
            issues.append({
                "severity": "warning",
                "area": "role_evidence",
                "kind": "screenshot_evidence_missing",
                "message": f"{row['tp_row']} screenshot/privacy evidence is missing or invalid.",
            })
        role_rows.append({
            "tp_row": row["tp_row"],
            "evidence_row": row["evidence_row"],
            "role": row["role"],
            "expected_surface": row["expected_surface"],
            "screenshot": row["screenshot"],
            "evidence_files": ", ".join(_evidence_files(row)),
            "status": status,
            "reason": reason,
        })

    if gate_blocked:
        overall = "blocked"
        gate_status = "blocked"
    elif any(row["status"] == "pending_capture" for row in role_rows):
        overall = "attention"
        gate_status = "pass"
    else:
        overall = "ready_for_founder_review"
        gate_status = "pass"

    if gate_blocked:
        deferred = [
            "No role login/session UAT is attempted while production health/readiness is blocked.",
            "No screenshots are required or captured while the BN18B hard gate is blocked.",
            "No provider dashboard, Stripe, Resend, DocuSign, MongoDB, Vercel, Render, or Atlas mutation is performed.",
            "No UAT account, credential, session, founder-acceptance, billing, webhook, document, owner-visibility, product behavior, or Admin Portal capability is changed.",
            "Founder acceptance remains a later explicit BN19 action.",
        ]
    else:
        deferred = [
            "Screenshot evidence is local review evidence only; this proof does not create or replay browser sessions.",
            "No provider dashboard, Stripe, Resend, DocuSign, MongoDB, Vercel, Render, or Atlas mutation is performed.",
            "No UAT account, credential, session, founder-acceptance, billing, webhook, document, owner-visibility, product behavior, or Admin Portal capability is changed.",
            "Founder acceptance remains a later explicit BN19 action.",
        ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "phase": "Build-Next-18C",
        "scope": "read_only_uat_role_refresh_preflight",
        "overall_status": overall,
        "frontend_url": production_proof.get("frontend_url") or DEFAULT_FRONTEND_URL,
        "api_base_url": production_proof.get("api_base_url") or DEFAULT_API_BASE_URL,
        "gate_status": gate_status,
        "gate_blocker_count": len(blockers),
        "issue_counts": _issue_counts(issues),
        "issues": issues,
        "production_gate": {
            "frontend_ok": (production_proof.get("frontend") or {}).get("ok"),
            "health_ok": (production_proof.get("backend_health") or {}).get("ok"),
            "health_error": (production_proof.get("backend_health") or {}).get("error"),
            "readiness_ok": (production_proof.get("readiness") or {}).get("ok"),
            "readiness_error": (production_proof.get("readiness") or {}).get("error"),
            "database": (production_proof.get("backend_health") or {}).get("database"),
            "environment": (production_proof.get("backend_health") or {}).get("environment"),
            "indexes_ensured": (production_proof.get("readiness") or {}).get("indexes_ensured"),
        },
        "production_gate_blockers": [
            {
                "area": issue.get("area", ""),
                "kind": issue.get("kind", ""),
                "message": issue.get("message", ""),
            }
            for issue in blockers
        ],
        "role_rows": role_rows,
        "deferred": deferred,
    }


def render_uat_role_refresh_markdown(report: Mapping[str, Any]) -> str:
    """Render a scrubbed BN18C role-refresh report."""
    lines = [
        "# Build-Next-18C UAT Role Refresh",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only UAT role-refresh preflight for TP-1 through TP-11. This report depends on the BN18B production API health/readiness gate and does not create sessions, mutate data, or mark founder acceptance.",
        "",
        "## Overall",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Overall status | {report.get('overall_status')} |",
        f"| Gate status | {report.get('gate_status')} |",
        f"| Gate blocker count | {report.get('gate_blocker_count')} |",
        f"| Frontend URL | {report.get('frontend_url')} |",
        f"| API base URL | {report.get('api_base_url')} |",
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | --- |",
    ]

    issue_counts = report.get("issue_counts") or {}
    if issue_counts:
        for severity, count in issue_counts.items():
            lines.append(f"| {severity} | {count} |")
    else:
        lines.append("| blocker | 0 |")
        lines.append("| warning | 0 |")

    lines.extend([
        "",
        "## Production Gate",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ])
    for key, value in (report.get("production_gate") or {}).items():
        lines.append(f"| {key} | {value} |")

    lines.extend([
        "",
        "## Production Gate Blockers",
        "",
        "| Area | Kind | Message |",
        "| --- | --- | --- |",
    ])
    blockers = report.get("production_gate_blockers") or []
    if blockers:
        for issue in blockers:
            lines.append(f"| {issue['area']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | No production-gate blockers found. |")

    lines.extend([
        "",
        "## Role Rows",
        "",
        "| TP row | Evidence row | Role | Expected surface | Evidence files | Status | Reason |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ])
    for row in report.get("role_rows") or []:
        lines.append(
            f"| {row['tp_row']} | {row['evidence_row']} | {row['role']} | "
            f"{row['expected_surface']} | {row['evidence_files']} | "
            f"{row['status']} | {row['reason']} |"
        )

    lines.extend([
        "",
        "## Issues",
        "",
        "| Severity | Area | Kind | Message |",
        "| --- | --- | --- | --- |",
    ])
    issues = report.get("issues") or []
    if issues:
        for issue in issues:
            lines.append(f"| {issue['severity']} | {issue['area']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend(["", "## Deferred By Design", ""])
    for item in report.get("deferred") or []:
        lines.append(f"- {item}")

    if report.get("overall_status") == "ready_for_founder_review":
        acceptance = (
            "BN18C does not mark any row founder-accepted. Evidence-captured "
            "rows still require explicit founder review."
        )
    else:
        acceptance = (
            "BN18C does not mark any row founder-accepted. If the gate is "
            "blocked, all role rows remain blocked. If the gate later passes, "
            "role rows still require screenshot/session evidence and explicit "
            "founder review."
        )

    lines.extend([
        "",
        "## Secret Safety",
        "",
        "This report renders public URLs, status booleans, role labels, expected surface names, and blocker reasons only.",
        "It must not contain login secrets, authentication material, API keys, webhook secrets, private keys, MongoDB connection strings, provider payloads, raw owner/staff/private data, or founder-acceptance credentials.",
        "",
        "## Acceptance Boundary",
        "",
        acceptance,
        "",
    ])
    return "\n".join(lines)
