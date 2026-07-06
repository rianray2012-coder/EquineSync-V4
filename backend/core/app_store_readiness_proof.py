from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ReadinessRow:
    area: str
    key: str
    label: str
    status: str
    evidence: str
    launch_gate: str
    founder_decision: str


OFFICIAL_POLICY_REFERENCES: tuple[dict[str, str], ...] = (
    {
        "owner": "Apple",
        "topic": "App privacy details",
        "url": "https://developer.apple.com/app-store/app-privacy-details/",
        "gate": "App Store privacy labels must be completed from actual data collection and sharing practices.",
    },
    {
        "owner": "Apple",
        "topic": "Account deletion",
        "url": "https://developer.apple.com/support/offering-account-deletion-in-your-app/",
        "gate": "Apps with account creation must let users initiate account deletion in the app.",
    },
    {
        "owner": "Apple",
        "topic": "App review readiness",
        "url": "https://developer.apple.com/distribute/app-review/",
        "gate": "Support and privacy links must be functional before review submission.",
    },
    {
        "owner": "Google",
        "topic": "Data safety",
        "url": "https://support.google.com/googleplay/android-developer/answer/10787469",
        "gate": "Play Console Data safety answers must match actual collection, sharing, and security practices.",
    },
    {
        "owner": "Google",
        "topic": "Payments policy",
        "url": "https://support.google.com/googleplay/android-developer/answer/9858738",
        "gate": "Play-distributed apps accepting payment for in-app features or services must use Google Play billing unless an exception applies.",
    },
    {
        "owner": "Google",
        "topic": "Restricted app access and review prep",
        "url": "https://support.google.com/googleplay/android-developer/answer/9859455",
        "gate": "Restricted app areas need access instructions, target audience details, privacy policy, and content rating inputs.",
    },
)


STORE_METADATA_FIELDS: tuple[dict[str, str], ...] = (
    {"field": "App name", "current_value": "Equine-Sync / EquineSync", "status": "needs_founder_final"},
    {"field": "Subtitle / short description", "current_value": "Not finalized for store listing.", "status": "missing"},
    {"field": "Long description", "current_value": "No app-store listing copy bundle found.", "status": "missing"},
    {"field": "Category", "current_value": "Likely Business/Productivity; founder/legal must confirm.", "status": "missing"},
    {"field": "Age rating / target audience", "current_value": "Minor and guardian workflows exist; store rating answers not prepared.", "status": "missing"},
    {"field": "Support URL", "current_value": "No public support URL found in source.", "status": "missing"},
    {"field": "Marketing URL", "current_value": "No store-ready marketing URL record found in source.", "status": "missing"},
    {"field": "Privacy policy URL", "current_value": "No public privacy policy URL found in source.", "status": "missing"},
    {"field": "Terms URL", "current_value": "No public terms URL found in source.", "status": "missing"},
    {"field": "Account deletion URL/path", "current_value": "No account deletion route or URL found in source.", "status": "missing"},
    {"field": "Bundle identifiers", "current_value": "Apple product IDs exist for billing planning; no native bundle ID evidence found.", "status": "missing"},
    {"field": "Review/demo accounts", "current_value": "No BN18E review-account package generated; no UAT mutation allowed.", "status": "missing"},
    {"field": "Screenshots", "current_value": "UAT/mobile screenshots exist, but no store-device screenshot set found.", "status": "partial"},
    {"field": "Release owner", "current_value": "No named App Store Connect / Play Console release owner found.", "status": "missing"},
)


DATA_SAFETY_ROWS: tuple[dict[str, str], ...] = (
    {
        "category": "Account and identity",
        "source_basis": "Auth, invites, role routing, account membership, and admin-user surfaces.",
        "status": "requires_privacy_labeling",
    },
    {
        "category": "Facility, staff, rider, guardian, owner, and horse data",
        "source_basis": "Role-specific intake, HorseOps, owner projections, dashboards, and task workflows.",
        "status": "requires_privacy_labeling",
    },
    {
        "category": "Billing and subscription data",
        "source_basis": "Stripe-backed web subscription surfaces and admin billing surfaces.",
        "status": "requires_policy_mapping",
    },
    {
        "category": "Documents and signature workflow data",
        "source_basis": "DocuSign/document workflow planning and webhook status sync surfaces.",
        "status": "requires_privacy_labeling",
    },
    {
        "category": "Local device storage",
        "source_basis": "QuickAdd session drafts, HorseOps local drafts, and narrow task retry queue.",
        "status": "requires_disclosure",
    },
    {
        "category": "Minor / guardian handling",
        "source_basis": "Minor safety rules, guardian/student invites, and role-specific guardian surfaces.",
        "status": "requires_target_audience_review",
    },
)


BILLING_POLICY_ROWS: tuple[dict[str, str], ...] = (
    {
        "surface": "Current web subscription purchase",
        "current_source": "Stripe Checkout/customer portal through `/billing/subscription`.",
        "store_policy_risk": "Allowed for web launch, but native app store apps must not steer around Apple/Google purchase rules.",
        "status": "ready_for_web_only",
    },
    {
        "surface": "Apple App Store distributed iOS app",
        "current_source": "Planning docs include Apple-originated purchase concepts and product ID shapes; no native iOS/IAP implementation is present.",
        "store_policy_risk": "Blocked until Apple IAP applicability, purchase flow, entitlement reconciliation, and review notes are finalized.",
        "status": "blocked_for_app_store",
    },
    {
        "surface": "Google Play distributed Android app",
        "current_source": "No Google Play Billing implementation or Play Console policy decision record found.",
        "store_policy_risk": "Blocked until Google Play billing applicability and subscription entitlement mapping are finalized.",
        "status": "blocked_for_google_play",
    },
    {
        "surface": "Existing paid web subscribers using a future native app",
        "current_source": "No store-specific subscriber access wording found.",
        "store_policy_risk": "Requires review notes and in-app copy that avoid prohibited purchase steering.",
        "status": "decision_required",
    },
)


SCREENSHOT_REQUIREMENTS: tuple[dict[str, str], ...] = (
    {"asset": "iPhone / iPad App Store screenshots", "status": "missing", "evidence": "No native iOS project or store screenshot bundle found."},
    {"asset": "Android phone / tablet Google Play screenshots", "status": "missing", "evidence": "No Android project or Play screenshot bundle found."},
    {"asset": "Feature graphic / promotional assets", "status": "missing", "evidence": "Brand assets exist, but store promotional assets are not packaged."},
    {"asset": "Role-based review-note screenshot map", "status": "partial", "evidence": "BN18C role screenshots exist; they are not store submission screenshots."},
)


RELEASE_OWNERSHIP_ROWS: tuple[dict[str, str], ...] = (
    {"item": "Apple Developer account owner", "status": "missing", "gate": "Name the account/team owner before iOS submission."},
    {"item": "Google Play Console account owner", "status": "missing", "gate": "Name the account/team owner before Android submission."},
    {"item": "Release manager", "status": "missing", "gate": "Name who presses submit, monitors review, and handles rejection responses."},
    {"item": "Support responder", "status": "missing", "gate": "Name who monitors support contact used in store listings."},
    {"item": "Rollback/removal owner", "status": "missing", "gate": "Name who can remove, pause, or hotfix a store release."},
)


def build_app_store_readiness_proof(root: Path | str | None = None) -> dict[str, Any]:
    base = Path(root) if root is not None else ROOT
    rows = _build_readiness_rows(base)
    issues = _issues_for_rows(rows)
    issue_counts = Counter(issue["severity"] for issue in issues)
    status_counts = Counter(row.status for row in rows)
    overall_status = "blocked" if issue_counts.get("blocker", 0) else "ready"

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_status": overall_status,
        "status_counts": dict(sorted(status_counts.items())),
        "issue_counts": dict(sorted(issue_counts.items())),
        "readiness_rows": [row.__dict__ for row in rows],
        "issues": issues,
        "store_metadata_inventory": list(STORE_METADATA_FIELDS),
        "data_safety_rows": list(DATA_SAFETY_ROWS),
        "billing_policy_rows": list(BILLING_POLICY_ROWS),
        "screenshot_requirements": list(SCREENSHOT_REQUIREMENTS),
        "release_ownership_rows": list(RELEASE_OWNERSHIP_ROWS),
        "founder_decisions": _founder_decisions(),
        "policy_references": list(OFFICIAL_POLICY_REFERENCES),
        "source_scan": _source_scan_summary(base),
        "scope": {
            "behavior_changes": "none",
            "database_writes": "none",
            "network_calls": "none",
            "provider_mutations": "none",
            "uat_account_mutations": "none",
            "founder_acceptance": "not_marked_by_script",
            "app_store_submission": "not_performed",
        },
    }


def render_app_store_readiness_report(report: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Build-Next-18E App Store / Google Play Readiness Report",
        "",
        f"Generated at: `{report['generated_at']}`",
        "",
        "## Scope",
        "",
        "Evidence-only readiness gate for Apple App Store and Google Play launch readiness.",
        "No product behavior, route, schema, auth, permission, provider, database, UAT account, founder-acceptance, native-app, or app-store-submission changes were performed.",
        "",
        "## Overall",
        "",
        f"- Status: `{report['overall_status']}`",
        f"- Behavior changes: `{report['scope']['behavior_changes']}`",
        f"- Database writes: `{report['scope']['database_writes']}`",
        f"- Network calls: `{report['scope']['network_calls']}`",
        f"- Provider mutations: `{report['scope']['provider_mutations']}`",
        f"- UAT account mutations: `{report['scope']['uat_account_mutations']}`",
        f"- Founder acceptance: `{report['scope']['founder_acceptance']}`",
        f"- App-store submission: `{report['scope']['app_store_submission']}`",
        "",
        "## Status Summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status in ("ready", "partial", "missing", "deferred", "blocked"):
        lines.append(f"| {status} | {report['status_counts'].get(status, 0)} |")

    lines.extend([
        "",
        "## Issue Summary",
        "",
        "| Severity | Count |",
        "| --- | ---: |",
    ])
    for severity in ("blocker", "decision_required", "warning"):
        lines.append(f"| {severity} | {report['issue_counts'].get(severity, 0)} |")

    lines.extend([
        "",
        "## Readiness Checklist",
        "",
        "| Area | Item | Status | Evidence | Launch gate | Founder decision |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for row in report["readiness_rows"]:
        lines.append(
            f"| {row['area']} | {row['label']} | {row['status']} | {row['evidence']} | {row['launch_gate']} | {row['founder_decision']} |"
        )

    lines.extend([
        "",
        "## Store Metadata Inventory",
        "",
        "| Field | Current value | Status |",
        "| --- | --- | --- |",
    ])
    for row in report["store_metadata_inventory"]:
        lines.append(f"| {row['field']} | {row['current_value']} | {row['status']} |")

    lines.extend([
        "",
        "## Privacy And Data-Safety Evidence",
        "",
        "| Category | Source basis | Status |",
        "| --- | --- | --- |",
    ])
    for row in report["data_safety_rows"]:
        lines.append(f"| {row['category']} | {row['source_basis']} | {row['status']} |")

    lines.extend([
        "",
        "## Support And Account Deletion Evidence",
        "",
        f"- Public support URL: `{report['source_scan']['support_url_status']}`",
        f"- Public privacy policy URL: `{report['source_scan']['privacy_policy_status']}`",
        f"- Account deletion route or URL: `{report['source_scan']['account_deletion_status']}`",
        "- Current result: blocked for app-store submission until public support, privacy, terms, and account-deletion paths are implemented and documented.",
        "",
        "## Billing Policy Mapping",
        "",
        "| Surface | Current source | Store policy risk | Status |",
        "| --- | --- | --- | --- |",
    ])
    for row in report["billing_policy_rows"]:
        lines.append(f"| {row['surface']} | {row['current_source']} | {row['store_policy_risk']} | {row['status']} |")

    lines.extend([
        "",
        "## Screenshot And Review-Note Requirements",
        "",
        "| Asset | Status | Evidence |",
        "| --- | --- | --- |",
    ])
    for row in report["screenshot_requirements"]:
        lines.append(f"| {row['asset']} | {row['status']} | {row['evidence']} |")

    lines.extend([
        "",
        "## Release Ownership Checklist",
        "",
        "| Item | Status | Gate |",
        "| --- | --- | --- |",
    ])
    for row in report["release_ownership_rows"]:
        lines.append(f"| {row['item']} | {row['status']} | {row['gate']} |")

    lines.extend([
        "",
        "## Founder Decisions",
        "",
        "| Decision | Status | Options | Gate |",
        "| --- | --- | --- | --- |",
    ])
    for row in report["founder_decisions"]:
        lines.append(f"| {row['decision']} | {row['status']} | {row['options']} | {row['gate']} |")

    lines.extend([
        "",
        "## Official Policy References",
        "",
        "| Owner | Topic | URL | Gate |",
        "| --- | --- | --- | --- |",
    ])
    for ref in report["policy_references"]:
        lines.append(f"| {ref['owner']} | {ref['topic']} | {ref['url']} | {ref['gate']} |")

    lines.extend([
        "",
        "## Source Scan Summary",
        "",
        f"- Web manifest: `{report['source_scan']['web_manifest_status']}`",
        f"- Native iOS project: `{report['source_scan']['ios_project_status']}`",
        f"- Native Android project: `{report['source_scan']['android_project_status']}`",
        f"- Store metadata bundle: `{report['source_scan']['store_metadata_status']}`",
        f"- Store screenshot bundle: `{report['source_scan']['store_screenshot_status']}`",
        f"- Existing UAT/role screenshot evidence: `{report['source_scan']['uat_screenshot_status']}`",
        f"- Billing source mapping: `{report['source_scan']['billing_mapping_status']}`",
        f"- Minor/guardian source evidence: `{report['source_scan']['minor_guardian_status']}`",
        "",
        "## Issues",
        "",
        "| Severity | Area | Kind | Message |",
        "| --- | --- | --- | --- |",
    ])
    if report["issues"]:
        for issue in report["issues"]:
            lines.append(f"| {issue['severity']} | {issue['area']} | {issue['kind']} | {issue['message']} |")
    else:
        lines.append("| - | - | - | No issues found. |")

    lines.extend([
        "",
        "## BN18E Acceptance Boundary",
        "",
        "- BN18E may be accepted as evidence that app-store readiness is not complete yet.",
        "- BN18E must not be used as an app-store submission, a native app implementation, a privacy-label completion, or a billing-policy legal sign-off.",
        "- A web-only or PWA-assisted pilot can proceed only if founder explicitly accepts app-store distribution as deferred.",
        "- Native Apple App Store / Google Play launch remains blocked until native projects, metadata, privacy/data-safety answers, support/deletion URLs, screenshots, review notes, release ownership, and app-store billing policy are complete.",
        "",
    ])
    return "\n".join(lines)


def _build_readiness_rows(base: Path) -> list[ReadinessRow]:
    scan = _source_scan_summary(base)
    ios_project_present = scan["ios_project_status"] == "present"
    android_project_present = scan["android_project_status"] == "present"
    store_metadata_present = scan["store_metadata_status"] == "present"
    store_screenshots_present = scan["store_screenshot_status"] == "present"
    uat_screenshots_present = scan["uat_screenshot_status"] == "present"
    return [
        ReadinessRow(
            "Platform",
            "web_manifest",
            "Web manifest and installable web metadata",
            "ready" if scan["web_manifest_status"] == "present" else "missing",
            "frontend/public/manifest.json includes name, description, display, colors, and icon entries." if scan["web_manifest_status"] == "present" else "No web manifest found.",
            "Good for web/PWA-adjacent metadata only; not enough for native store submission.",
            "Founder must choose whether web/PWA-assisted launch is enough for pilot.",
        ),
        ReadinessRow(
            "Platform",
            "native_ios_project",
            "Native iOS project",
            "ready" if ios_project_present else "missing",
            "Native iOS project evidence found." if ios_project_present else "No ios directory, Xcode project, workspace, Capacitor config, or Expo config found.",
            "Required before an App Store-distributed iOS app can be built and submitted.",
            "Confirm signing, bundle identifier, build number, and release ownership." if ios_project_present else "Accept app-store iOS as deferred or authorize native wrapper/app build.",
        ),
        ReadinessRow(
            "Platform",
            "native_android_project",
            "Native Android project",
            "ready" if android_project_present else "missing",
            "Native Android project evidence found." if android_project_present else "No android directory, Gradle project, Capacitor config, or Expo config found.",
            "Required before a Google Play-distributed Android app can be built and submitted.",
            "Confirm signing, application id, versioning, and release ownership." if android_project_present else "Accept Google Play as deferred or authorize native wrapper/app build.",
        ),
        ReadinessRow(
            "Metadata",
            "store_metadata_bundle",
            "Store metadata bundle",
            "ready" if store_metadata_present else "missing",
            "Store metadata bundle evidence found." if store_metadata_present else "No App Store Connect or Google Play metadata bundle found.",
            "Required for store listing, review, category, age rating, support, and marketing copy.",
            "Founder must verify final name, positioning, categories, descriptions, and contacts." if store_metadata_present else "Founder must approve final name, positioning, categories, descriptions, and contacts.",
        ),
        ReadinessRow(
            "Privacy",
            "privacy_data_safety",
            "Privacy labels and Google Data safety answers",
            "missing",
            "Source has privacy-sensitive workflows, but no final Apple privacy label or Google Data safety worksheet.",
            "Must be completed from real data collection, sharing, retention, and security practices.",
            "Founder/legal must approve privacy and data-safety answers before submission.",
        ),
        ReadinessRow(
            "Support",
            "support_urls",
            "Support, privacy, terms, and account deletion URLs",
            "blocked",
            "No public support URL, public privacy policy URL, public terms URL, or account deletion route/URL found.",
            "Required before store submission for apps with account creation and restricted access.",
            "Founder must approve support owner and account deletion implementation path.",
        ),
        ReadinessRow(
            "Billing",
            "billing_policy_mapping",
            "Web Stripe billing versus app-store billing policy",
            "partial" if scan["billing_mapping_status"] == "partial" else "missing",
            "Repo documents web Stripe and Apple-originated purchase concepts, but no native Apple/Google billing implementation is present.",
            "Native app-store launch blocked until Apple/Google purchase rules, review notes, and entitlements are finalized.",
            "Founder must decide web-only billing for pilot versus app-store IAP implementation before native launch.",
        ),
        ReadinessRow(
            "Screenshots",
            "store_screenshots",
            "Store screenshots and review-note asset map",
            "ready" if store_screenshots_present else "partial" if uat_screenshots_present else "missing",
            "Store screenshot bundle evidence found." if store_screenshots_present else "Existing role/UAT screenshots are present, but no store-device screenshot set or store review-note bundle exists." if uat_screenshots_present else "No store screenshot bundle or UAT screenshot evidence found.",
            "Store-specific screenshots and reviewer flow notes required before submission.",
            "Founder must verify which roles and workflows appear in store screenshots." if store_screenshots_present else "Founder must approve which roles and workflows appear in store screenshots.",
        ),
        ReadinessRow(
            "Review",
            "review_accounts",
            "App-review accounts and restricted-access notes",
            "deferred",
            "BN18E does not create or mutate review accounts; no review-account package found.",
            "App reviewers need safe credentials and route notes before submission.",
            "Founder must authorize review account creation in a later, explicit gate.",
        ),
        ReadinessRow(
            "Ownership",
            "release_ownership",
            "Release ownership and escalation",
            "missing",
            "No named Apple/Google account owner, submitter, support responder, or rejection-response owner found.",
            "Release ownership must be assigned before production store launch.",
            "Founder must name release and support owners.",
        ),
    ]


def _issues_for_rows(rows: list[ReadinessRow]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for row in rows:
        if row.status in {"blocked", "missing"}:
            issues.append({
                "severity": "blocker",
                "area": row.area,
                "kind": row.key,
                "message": f"{row.label}: {row.launch_gate}",
            })
        elif row.status in {"partial", "deferred"}:
            issues.append({
                "severity": "decision_required",
                "area": row.area,
                "kind": row.key,
                "message": f"{row.label}: {row.founder_decision}",
            })
    return issues


def _founder_decisions() -> list[dict[str, str]]:
    return [
        {
            "decision": "Pilot distribution posture",
            "status": "required",
            "options": "web-only, PWA-assisted web, native app-store distributed",
            "gate": "Must be accepted before BN19 founder acceptance ledger finalizes.",
        },
        {
            "decision": "App Store / Google Play timing",
            "status": "required",
            "options": "required before public launch, deferred after web launch, deferred after first-client pilot",
            "gate": "Must resolve public launch copy and roadmap commitments.",
        },
        {
            "decision": "Billing policy route",
            "status": "required",
            "options": "web Stripe only for web launch, Apple/Google IAP for native launch, hybrid with compliant access wording",
            "gate": "Must be complete before native store submission.",
        },
        {
            "decision": "Account deletion implementation",
            "status": "required",
            "options": "self-service in-app deletion, request-to-delete plus in-app initiation, defer app stores until built",
            "gate": "Apps with account creation cannot be store-submitted without a compliant path.",
        },
        {
            "decision": "Privacy/data-safety owner",
            "status": "required",
            "options": "founder, counsel, release owner, delegated compliance owner",
            "gate": "Apple privacy labels and Google Data safety cannot be guessed.",
        },
        {
            "decision": "Store screenshot/review-note scope",
            "status": "required",
            "options": "owner-safe marketing flow, staff/manager operational flow, multi-role restricted demo flow",
            "gate": "Reviewers need safe route instructions and non-sensitive demo data.",
        },
    ]


def _source_scan_summary(base: Path) -> dict[str, str]:
    return {
        "web_manifest_status": "present" if _manifest_is_present(base) else "missing",
        "ios_project_status": "present" if _any_path(base, ("ios", "*.xcodeproj", "*.xcworkspace")) else "missing",
        "android_project_status": "present" if _any_path(base, ("android", "build.gradle", "settings.gradle")) else "missing",
        "store_metadata_status": "present" if _any_path(base, ("fastlane/metadata", "store_metadata", "docs/store_metadata")) else "missing",
        "store_screenshot_status": "present" if _any_path(base, ("fastlane/screenshots", "store_screenshots", "docs/store_screenshots")) else "missing",
        "uat_screenshot_status": "present" if (base / "outputs" / "build_next_18c_uat_role_refresh_screenshots").exists() else "missing",
        "support_url_status": _url_status(base, ("support",)),
        "privacy_policy_status": _url_status(base, ("privacy",)),
        "terms_status": _url_status(base, ("terms",)),
        "account_deletion_status": "present" if _account_deletion_path_present(base) else "missing",
        "billing_mapping_status": "partial" if _source_contains(base, ("Stripe is for web-based subscription purchases", "Apple App Store billing is for iOS-originated purchases"), all_terms=True) else "missing",
        "minor_guardian_status": "present" if _source_contains(base, ("guardian", "minor", "parent"), all_terms=True) else "missing",
    }


def _manifest_is_present(base: Path) -> bool:
    manifest = base / "frontend" / "public" / "manifest.json"
    if not manifest.exists():
        return False
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    return all(data.get(key) for key in ("name", "short_name", "icons", "display"))


def _any_path(base: Path, patterns: tuple[str, ...]) -> bool:
    for pattern in patterns:
        if "/" in pattern:
            if (base / pattern).exists():
                return True
        elif any(base.glob(pattern)):
            return True
    return False


def _url_status(base: Path, terms: tuple[str, ...]) -> str:
    url_re = re.compile(r"https?://[^\s)>\"]+", re.IGNORECASE)
    for path in _text_files(base, exclude_bn18e=True):
        for line in _read_text(path).lower().splitlines():
            if not all(term in line for term in terms):
                continue
            urls = url_re.findall(line)
            if any("equine-sync.com" in url and any(term in url for term in terms) for url in urls):
                return "present"
    return "missing"


def _account_deletion_path_present(base: Path) -> bool:
    route_re = re.compile(r"(/account[^\\s\"']*delete|/delete-account|account-deletion)", re.IGNORECASE)
    for root in ("backend", "frontend/src", "frontend/public"):
        path = base / root
        if not path.exists():
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in {".py", ".js", ".jsx", ".json", ".html"}:
                continue
            relative = str(candidate.relative_to(base))
            if (
                "app_store_readiness_proof" in relative
                or "build_next_18e_app_store_readiness_proof" in relative
                or "test_build_next_18e_app_store_readiness_proof" in relative
            ):
                continue
            if route_re.search(_read_text(candidate)):
                return True
    return False


def _source_contains(
    base: Path,
    terms: tuple[str, ...],
    *,
    all_terms: bool = False,
    exclude_bn18e: bool = False,
) -> bool:
    lowered = tuple(term.lower() for term in terms)
    for path in _text_files(base, exclude_bn18e=exclude_bn18e):
        text = _read_text(path).lower()
        if all_terms and all(term in text for term in lowered):
            return True
        if not all_terms and any(term in text for term in lowered):
            return True
    return False


def _text_files(base: Path, *, exclude_bn18e: bool) -> list[Path]:
    roots = ("backend", "docs", "frontend/public", "frontend/src", "memory")
    files: list[Path] = []
    for root in roots:
        path = base / root
        if not path.exists():
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in {".py", ".js", ".jsx", ".json", ".md", ".html"}:
                continue
            relative = str(candidate.relative_to(base))
            if exclude_bn18e and (
                "APP_STORE_PRODUCTION_READINESS" in relative
                or "app_store_readiness_proof" in relative
                or "build_next_18e_app_store_readiness_proof" in relative
                or "test_build_next_18e_app_store_readiness_proof" in relative
            ):
                continue
            files.append(candidate)
    return files


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
