"""Billing seat-type classification helpers for Phase 15R-E.

This module is read-only. It does not mutate users, subscriptions, Stripe,
Apple, or entitlement rows. It prepares the canonical seat vocabulary that a
later approved migration can write.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping


BILLING_SEAT_TYPES = (
    "owner_manager",
    "staff",
    "helper_family",
    "client_owner_portal",
    "lesson_participant",
    "platform_admin",
    "none",
)

ACCOUNT_ORIGINS = (
    "self_subscribed",
    "invited_by_barn",
    "invited_by_trainer",
    "platform_created",
)

PORTAL_ACCESS_STATUSES = ("active", "invited", "disabled")

# Keep this local so the read-only dry-run helper does not import FastAPI via
# core.permissions. Source-of-truth parity is pinned in tests.
PLATFORM_BILLING_ROLES = {
    "super_admin",
    "platform_admin",
    "support_admin",
    "billing_admin",
    "read_only_auditor",
}
OWNER_MANAGER_ROLES = {"admin", "barn_manager", "barn_owner"}
STAFF_ROLES = {"trainer", "groom", "working_student", "veterinarian", "farrier", "service_provider"}
CLIENT_OWNER_ROLES = {"horse_owner", "parent"}
LESSON_PARTICIPANT_ROLES = {"rider"}


def _clean(value: Any) -> str:
    return (str(value or "")).strip().lower()


def _valid(value: Any, allowed: tuple[str, ...] | set[str]) -> bool:
    return _clean(value) in set(allowed)


def _record_ref(user: Mapping[str, Any]) -> str:
    return str(user.get("id") or user.get("email") or "(unknown)")


def classify_billing_seat(user: Mapping[str, Any]) -> dict[str, Any]:
    """Return the future billing seat fields for a user row.

    Existing valid fields win. Otherwise the function derives a conservative
    preview from platform_role, account_origin, and role.
    """
    explicit_seat = _clean(user.get("billing_seat_type"))
    if explicit_seat in BILLING_SEAT_TYPES:
        origin = _clean(user.get("account_origin"))
        status = _clean(user.get("portal_access_status"))
        companion_issues = []
        if not _valid(origin, ACCOUNT_ORIGINS):
            companion_issues.append({
                "kind": "missing_or_invalid_account_origin",
                "message": f"{origin or 'missing'} is not a known account_origin.",
            })
        if not _valid(status, PORTAL_ACCESS_STATUSES):
            companion_issues.append({
                "kind": "missing_or_invalid_portal_access_status",
                "message": f"{status or 'missing'} is not a known portal_access_status.",
            })
        return {
            "billing_seat_type": explicit_seat,
            "account_origin": origin or None,
            "portal_access_status": status or None,
            "source": "explicit",
            "needs_review": bool(companion_issues),
            "companion_issues": companion_issues,
        }

    role = _clean(user.get("role"))
    platform_role = _clean(user.get("platform_role"))
    account_origin = _clean(user.get("account_origin"))
    portal_status = _clean(user.get("portal_access_status"))

    if platform_role in PLATFORM_BILLING_ROLES:
        seat = "platform_admin"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else "platform_created"
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else "active"
        needs_review = False
    elif role in OWNER_MANAGER_ROLES:
        seat = "owner_manager"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else "platform_created"
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else "active"
        needs_review = False
    elif role in STAFF_ROLES:
        seat = "staff"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else "platform_created"
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else "active"
        needs_review = role in {"trainer", "service_provider"}
    elif role in CLIENT_OWNER_ROLES:
        if account_origin == "self_subscribed":
            seat = "owner_manager"
            origin = "self_subscribed"
        else:
            seat = "client_owner_portal"
            origin = account_origin if account_origin in {"invited_by_barn", "invited_by_trainer"} else "invited_by_barn"
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else "active"
        needs_review = account_origin not in {"self_subscribed", "invited_by_barn", "invited_by_trainer"}
    elif role in LESSON_PARTICIPANT_ROLES:
        seat = "lesson_participant"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else "invited_by_barn"
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else "active"
        needs_review = False
    elif role:
        seat = "none"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else None
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else None
        needs_review = True
    else:
        seat = "none"
        origin = account_origin if _valid(account_origin, ACCOUNT_ORIGINS) else None
        status = portal_status if _valid(portal_status, PORTAL_ACCESS_STATUSES) else None
        needs_review = True

    return {
        "billing_seat_type": seat,
        "account_origin": origin,
        "portal_access_status": status,
        "source": "derived",
        "needs_review": needs_review,
        "companion_issues": [],
    }


def build_billing_seat_dry_run(users: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    rows = []
    issues = []
    counts = Counter()
    source_counts = Counter()

    for user in users:
        projected = classify_billing_seat(user)
        seat = projected["billing_seat_type"]
        source = projected["source"]
        counts[seat] += 1
        source_counts[source] += 1
        record = {
            "user_id": user.get("id"),
            "email": user.get("email"),
            "role": user.get("role"),
            "platform_role": user.get("platform_role"),
            **projected,
        }
        rows.append(record)

        if projected["needs_review"]:
            issues.append({
                "severity": "warning",
                "kind": "seat_type_needs_review",
                "record": _record_ref(user),
                "message": f"{user.get('role') or 'missing role'} projected to {seat}; review before migration.",
            })
        for issue in projected.get("companion_issues") or []:
            issues.append({
                "severity": "warning",
                "kind": issue["kind"],
                "record": _record_ref(user),
                "message": issue["message"],
            })
        if user.get("billing_seat_type") and source == "derived":
            issues.append({
                "severity": "warning",
                "kind": "invalid_existing_billing_seat_type",
                "record": _record_ref(user),
                "message": f"{user.get('billing_seat_type')} is not a known billing_seat_type.",
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_counts": {"users": len(rows)},
        "seat_counts": dict(sorted(counts.items())),
        "projection_source_counts": dict(sorted(source_counts.items())),
        "issue_counts": dict(sorted(Counter(issue["severity"] for issue in issues).items())),
        "issues": issues,
        "preview_rows": rows,
        "cleanup_checklist": build_cleanup_checklist(rows, issues),
    }


def build_cleanup_checklist(
    preview_rows: Iterable[Mapping[str, Any]],
    issues: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Group dry-run issues into founder-actionable cleanup items."""
    rows_by_ref = {
        str(row.get("user_id") or row.get("email") or "(unknown)"): row
        for row in preview_rows
    }
    grouped: dict[str, dict[str, Any]] = {}
    for issue in issues:
        record = str(issue.get("record") or "(unknown)")
        row = rows_by_ref.get(record, {})
        item = grouped.setdefault(record, {
            "record": record,
            "email": row.get("email"),
            "role": row.get("role"),
            "platform_role": row.get("platform_role"),
            "suggested_billing_seat_type": row.get("billing_seat_type"),
            "suggested_account_origin": row.get("account_origin"),
            "suggested_portal_access_status": row.get("portal_access_status"),
            "issue_kinds": [],
            "action": "review_before_migration",
        })
        kind = issue.get("kind")
        if kind and kind not in item["issue_kinds"]:
            item["issue_kinds"].append(kind)

    def sort_key(item: Mapping[str, Any]) -> tuple[str, str]:
        return (str(item.get("email") or ""), str(item.get("record") or ""))

    return sorted(grouped.values(), key=sort_key)


def render_billing_seat_markdown(report: Mapping[str, Any]) -> str:
    def table(headers: list[str], rows: list[list[Any]]) -> list[str]:
        out = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            out.append("| " + " | ".join("" if v is None else str(v) for v in row) + " |")
        return out

    lines = [
        "# Phase 15R-E Billing Seat Classification Dry-Run",
        "",
        f"Generated at: `{report.get('generated_at')}`",
        "",
        "## Scope",
        "",
        "Read-only projection of current `users` rows into future billing-seat fields.",
        "No Mongo writes, checkout changes, webhook changes, Stripe calls, Apple calls, or hard enforcement are performed.",
        "",
        "## Counts",
        "",
        *table(["Source", "Count"], [["users", report.get("source_counts", {}).get("users", 0)]]),
        "",
        "## Seat Counts",
        "",
        *table(["billing_seat_type", "count"], [[k, v] for k, v in (report.get("seat_counts") or {}).items()]),
        "",
        "## Issue Summary",
        "",
        *table(["Severity", "Count"], [[k, v] for k, v in (report.get("issue_counts") or {}).items()]),
        "",
        "## Issues",
        "",
    ]
    issues = report.get("issues") or []
    if issues:
        lines.extend(table(
            ["Severity", "Kind", "Record", "Message"],
            [[i.get("severity"), i.get("kind"), i.get("record"), i.get("message")] for i in issues],
        ))
    else:
        lines.append("No issues.")
    lines.extend([
        "",
        "## Founder Cleanup Checklist",
        "",
    ])
    checklist = report.get("cleanup_checklist") or []
    if checklist:
        lines.extend(table(
            [
                "record",
                "email",
                "role",
                "suggested_billing_seat_type",
                "suggested_account_origin",
                "suggested_portal_access_status",
                "issue_kinds",
                "action",
            ],
            [
                [
                    item.get("record"),
                    item.get("email"),
                    item.get("role"),
                    item.get("suggested_billing_seat_type"),
                    item.get("suggested_account_origin"),
                    item.get("suggested_portal_access_status"),
                    ", ".join(item.get("issue_kinds") or []),
                    item.get("action"),
                ]
                for item in checklist
            ],
        ))
    else:
        lines.append("No cleanup items.")
    lines.extend([
        "",
        "## Preview",
        "",
        *table(
            ["user_id", "email", "role", "platform_role", "billing_seat_type", "account_origin", "portal_access_status", "source", "needs_review"],
            [
                [
                    row.get("user_id"),
                    row.get("email"),
                    row.get("role"),
                    row.get("platform_role"),
                    row.get("billing_seat_type"),
                    row.get("account_origin"),
                    row.get("portal_access_status"),
                    row.get("source"),
                    row.get("needs_review"),
                ]
                for row in report.get("preview_rows", [])
            ],
        ),
        "",
        "## Deferred",
        "",
        "- No `users` rows are updated.",
        "- No hard usage enforcement is added.",
        "- No Stripe or Apple billing mutation is added.",
        "- No billing-seat UI is added.",
    ])
    return "\n".join(lines) + "\n"
