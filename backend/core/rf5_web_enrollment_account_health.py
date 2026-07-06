from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]

REQUIRED_ENROLLMENT_PATHS = {
    "individual_horse_owner": {
        "role": "horse_owner",
        "phase": "RF7",
        "terms": ["private land", "family", "informal care"],
    },
    "barn_facility_owner": {
        "role": "barn_owner",
        "phase": "RF5/RF12",
        "terms": ["barn managers", "Facility name", "Approximate capacity"],
    },
    "service_provider": {
        "role": "service_provider",
        "phase": "RF10",
        "terms": ["Service type", "Service area"],
    },
    "trainer": {
        "role": "trainer",
        "phase": "RF9",
        "terms": ["Specialties", "Service area"],
    },
}

MAIN_ENROLLMENT_ORDER = [
    "individual_horse_owner",
    "barn_facility_owner",
    "service_provider",
    "trainer",
]

INVITE_ONLY_PUBLIC_ROLES = ["rider", "parent", "guardian", "staff", "barn_staff"]

REQUIRED_ADMIN_PORTAL_ROUTES = [
    "users",
    "approvals",
    "facilities",
    "subscriptions",
    "billing",
    "support",
    "alerts",
    "reports",
    "integrations",
    "settings",
    "audit-logs",
]

FOUNDER_DECISIONS = [
    {
        "decision": "Accept the first public enrollment path order and labels.",
        "status": "requires founder review",
        "phase": "RF5, RF7, RF9, RF10",
        "notes": "Current order is Individual Horse Owner, Barn Owner / Manager, Service Provider, Trainer.",
    },
    {
        "decision": "Decide which critical signup fields become required by path.",
        "status": "requires founder decision",
        "phase": "RF5, RF7, RF9, RF10",
        "notes": "RF5 lists critical data without adding backend validation or deeper enrollment schemas.",
    },
    {
        "decision": "Decide whether trainer and service-provider self-signup stays review-gated.",
        "status": "requires founder decision",
        "phase": "RF9, RF10",
        "notes": "Existing signup marks trainer, barn owner, and service provider roles pending review.",
    },
    {
        "decision": "Accept rider, guardian, and staff access as invite-first with a limited-trial fallback.",
        "status": "requires founder review",
        "phase": "RF5, RF7, RF18",
        "notes": "RF5 records the fallback but does not enforce limited-trial access caps server-side.",
    },
    {
        "decision": "Accept leasee invites as owner/trainer controlled with owner oversight preserved.",
        "status": "requires founder review",
        "phase": "RF7",
        "notes": "RF5 records the leasee policy only; RF7 must implement the grant and revocation model.",
    },
    {
        "decision": "Accept admin account-health inventory as RF5 opening evidence only.",
        "status": "requires founder review",
        "phase": "RF5",
        "notes": "RF5 does not add new admin analytics, billing intervention mutations, or privacy-sensitive content inspection.",
    },
]


@dataclass(frozen=True)
class ProofRow:
    key: str
    status: str
    evidence: str
    next_action: str


def _read(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def _contains_all(source: str, needles: Iterable[str]) -> bool:
    return all(needle in source for needle in needles)


def _status_counts(rows: Iterable[ProofRow]) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1
    return counts


def build_rf5_readiness(root: Path = ROOT) -> Dict[str, object]:
    app_routes = _read(root, "frontend/src/App.js")
    landing = _read(root, "frontend/src/pages/Landing.jsx")
    login = _read(root, "frontend/src/pages/Login.jsx")
    signup = _read(root, "frontend/src/pages/Signup.jsx")
    enrollment = _read(root, "frontend/src/pages/Enrollment.jsx")
    enrollment_paths = _read(root, "frontend/src/lib/enrollmentPaths.js")
    auth = _read(root, "backend/routes/auth.py")

    order_positions = [
        enrollment_paths.find(f'id: "{path_id}"')
        for path_id in MAIN_ENROLLMENT_ORDER
    ]
    order_ok = all(position >= 0 for position in order_positions) and order_positions == sorted(order_positions)

    missing_paths: List[str] = []
    for path_id, expected in REQUIRED_ENROLLMENT_PATHS.items():
        checks = [
            f'id: "{path_id}"',
            f'role: "{expected["role"]}"',
            f'deferredPhase: "{expected["phase"]}"',
            f'data-testid={{`enrollment-path-${{path.id}}`}}',
        ]
        checks.extend(expected["terms"])
        if not _contains_all(enrollment_paths + enrollment, checks):
            missing_paths.append(path_id)

    missing_admin_routes = [
        route for route in REQUIRED_ADMIN_PORTAL_ROUTES if f'path="{route}"' not in app_routes
    ]

    rows = [
        ProofRow(
            key="public_enrollment_route",
            status="ready" if 'path="/enroll"' in app_routes and 'import Enrollment from "./pages/Enrollment"' in app_routes else "blocked",
            evidence="`/enroll` is registered as a public route before credential collection.",
            next_action="RF18 should run end-to-end enrollment UAT across supported device sizes.",
        ),
        ProofRow(
            key="home_signup_entry_points_route_to_enrollment",
            status="ready" if 'navigate(`/enroll${query}`)' in landing and "goToEnrollment" in landing and "/signup" not in landing else "blocked",
            evidence="Landing navigation, hero, role cards, pricing CTAs, and footer Join actions route to `/enroll`.",
            next_action="Founder should approve path order and copy before broader launch.",
        ),
        ProofRow(
            key="login_signup_entry_point",
            status="ready" if 'to="/enroll"' in login and 'data-testid="login-join-link"' in login else "blocked",
            evidence="The sign-in page now gives no-account users a Join EquineSync action.",
            next_action="RF18 should test the login-to-enrollment path with analytics and support instrumentation.",
        ),
        ProofRow(
            key="required_enrollment_paths_inventory",
            status="ready" if not missing_paths and order_ok else "blocked",
            evidence=f"{len(REQUIRED_ENROLLMENT_PATHS)} required enrollment paths are declared with role mapping, critical data, and deferred phase ownership.",
            next_action="RF7/RF9/RF10 should deepen the owner, trainer, and provider workflows without changing RF5 claims.",
        ),
        ProofRow(
            key="invite_only_roles_excluded_from_public_enrollment",
            status="ready"
            if "Rider, Guardian, Or Staff?" in enrollment
            and "limited seven-day" in enrollment + enrollment_paths
            and "Rider, guardian, and staff accounts remain invitation-based" in landing
            and 'id: "rider"' not in landing
            and "facility_or_provider_contact" in signup
            and "signup-step-limited-trial" in signup
            and "signup-finish-limited-trial" in signup
            and "Continue with limited access" in signup
            and "14-day free trial" in signup.split('!enrollmentContext?.limitedAccess', 1)[-1]
            and all(f'role: "{role}"' not in enrollment_paths for role in INVITE_ONLY_PUBLIC_ROLES)
            else "blocked",
            evidence="Rider, guardian, and staff accounts are not public main enrollment paths; RF5 offers invite guidance and a separate limited individual-owner signup branch.",
            next_action="RF7/RF18 must implement and test the limited-trial/access-cap semantics before stronger claims.",
        ),
        ProofRow(
            key="signup_receives_enrollment_context",
            status="ready"
            if _contains_all(
                signup,
                [
                    "useSearchParams",
                    "ENROLLMENT_CONTEXT_BY_ID",
                    "selectedEnrollment",
                    'navigate("/enroll", { replace: true })',
                    "signup-change-role-path",
                    "signup-enrollment-context",
                    "enrollment_path",
                    'to="/enroll"',
                ],
            )
            and "pickRole" not in signup
            else "blocked",
            evidence="Signup requires enrollment context, locks the public role to the selected path, and displays a changeable enrollment context.",
            next_action="Decide which path data becomes server-validated in RF7/RF9/RF10.",
        ),
        ProofRow(
            key="leasee_invite_caveat_recorded",
            status="ready"
            if "LEASEE_INVITE_RULE" in enrollment_paths
            and "Leasee access" in enrollment
            and "horse owner or the horse's assigned trainer" in enrollment_paths
            and "not opened as a public enrollment path" in enrollment
            else "blocked",
            evidence="Leasee access is recorded as invite-only from owner or assigned trainer while preserving owner oversight.",
            next_action="RF7 must implement leasee invite/grant semantics before leasee access is claimed live.",
        ),
        ProofRow(
            key="signup_backend_contract_not_expanded",
            status="ready" if "class MarketplaceSignupBody(BaseModel)" in auth and "profile: Optional[dict]" in auth else "blocked",
            evidence="RF5 does not add signup schema or auth permission changes; extra client enrollment context remains non-authoritative evidence.",
            next_action="Backend persistence and validation for enrollment-specific data should be explicit future work.",
        ),
        ProofRow(
            key="admin_account_health_inventory",
            status="ready" if not missing_admin_routes else "blocked",
            evidence=f"{len(REQUIRED_ADMIN_PORTAL_ROUTES)} platform-admin support/account-health route surfaces are present for RF5 inventory.",
            next_action="A later RF5 pass can add privacy-scrubbed metrics without exposing sensitive free text.",
        ),
        ProofRow(
            key="later_phase_boundaries_preserved",
            status="ready"
            if _contains_all(
                enrollment + enrollment_paths,
                ["Depth continues in", "RF7", "RF9", "RF10"]
            )
            else "blocked",
            evidence="Enrollment UI names later phase ownership rather than claiming completed owner/trainer/provider depth.",
            next_action="Keep RF7/RF9/RF10/RF18 open until those workflows are implemented and tested.",
        ),
    ]

    counts = _status_counts(rows)
    return {
        "phase": "RF5",
        "title": "RF5 Web Enrollment and Account Health Opening Gate",
        "overall_status": "ready" if counts.get("blocked", 0) == 0 else "blocked",
        "status_counts": counts,
        "rows": rows,
        "missing_paths": missing_paths,
        "missing_admin_routes": missing_admin_routes,
        "founder_decisions": FOUNDER_DECISIONS,
    }


def _table(headers: List[str], rows: List[List[str]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |" for row in rows)
    return "\n".join(out)


def render_rf5_report(report: Dict[str, object]) -> str:
    rows: List[ProofRow] = report["rows"]  # type: ignore[assignment]
    founder_decisions: List[Dict[str, str]] = report["founder_decisions"]  # type: ignore[assignment]

    lines = [
        "# RF5 Web Enrollment and Account Health Opening Gate Report",
        "",
        "Phase: `RF5`",
        f"Overall status: `{report['overall_status']}`",
        "",
        "## Proof Rows",
        "",
        _table(
            ["Key", "Status", "Evidence", "Next Action"],
            [[row.key, row.status, row.evidence, row.next_action] for row in rows],
        ),
        "",
        "## Enrollment Paths",
        "",
        _table(
            ["Path", "Signup Role", "Deferred Depth Phase"],
            [
                [path_id, value["role"], value["phase"]]
                for path_id in MAIN_ENROLLMENT_ORDER
                for value in [REQUIRED_ENROLLMENT_PATHS[path_id]]
            ],
        ),
        "",
        "## Invite-Only / Limited Trial Caveats",
        "",
        "- Rider, guardian, and staff accounts are not public main enrollment paths.",
        "- Those users should normally enroll from a trainer, barn owner, barn manager, or boss invite.",
        "- RF5 records a limited seven-day individual-owner trial option when contact information for a facility, trainer, or provider is supplied.",
        "- Leasee access must be invite-only from the horse owner or assigned trainer while owner oversight remains intact.",
        "",
        "## Account-Health Inventory",
        "",
        _table(
            ["Admin Route", "RF5 Status"],
            [[f"/admin/portal/{route}", "inventory present"] for route in REQUIRED_ADMIN_PORTAL_ROUTES],
        ),
        "",
        "## Founder Decision Rows",
        "",
        _table(
            ["Decision", "Status", "Phase", "Notes"],
            [
                [
                    item["decision"],
                    item["status"],
                    item["phase"],
                    item["notes"],
                ]
                for item in founder_decisions
            ],
        ),
        "",
        "## Boundaries",
        "",
        "- RF5 adds the public web enrollment selector and routes home/login Join actions to it.",
        "- RF5 limits the main selector to four public paths: Individual Horse Owner, Barn Owner / Manager, Service Provider, and Trainer.",
        "- RF5 records account-health/admin surfaces as inventory evidence only.",
        "- RF5 does not add backend enrollment schemas, limited-trial enforcement, leasee grants, billing intervention mutations, provider grants, trainer operating workflows, owner-portal depth, or RF18 UAT acceptance.",
        "- Trainer and service-provider marketplace signup remain review-gated under the existing signup posture.",
        "",
    ]
    return "\n".join(lines)
