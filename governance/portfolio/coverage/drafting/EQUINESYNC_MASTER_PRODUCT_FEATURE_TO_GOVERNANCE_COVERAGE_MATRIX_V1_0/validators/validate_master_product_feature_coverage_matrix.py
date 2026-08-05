#!/usr/bin/env python3
"""Deterministic validator for the EquineSync master feature-to-governance matrix revision."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict, deque
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
REPO = PACKAGE.parents[4]
ARTIFACT_ID = "EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0"
CSV_PATH = PACKAGE / f"{ARTIFACT_ID}.csv"
JSON_PATH = PACKAGE / f"{ARTIFACT_ID}.json"
SOURCE_PATH = PACKAGE / "SOURCE_AND_AUTHORITY_REGISTER.csv"
PIA_PATH = PACKAGE / "PIA_FEATURE_COVERAGE_SUMMARY.csv"
GOV_PATH = PACKAGE / "GOVERNANCE_ARTIFACT_INVENTORY.csv"
DECISION_PATH = PACKAGE / "PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv"
GAP_PATH = PACKAGE / "NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv"
QUEUE_PATH = PACKAGE / "PRIORITIZED_WORK_QUEUES.csv"
DASHBOARD_PATH = PACKAGE / "DASHBOARD_SUMMARY.json"
METRICS_PATH = PACKAGE / "PACKAGE_METRICS.json"
DEPENDENCY_PATH = PACKAGE / "DEPENDENCY_REGISTER.csv"
CONFLICT_PATH = PACKAGE / "DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv"
MANIFEST_PATH = PACKAGE / "PACKAGE_MANIFEST.json"
CHECKSUM_PATH = PACKAGE / "CHECKSUMS.sha256"
BASELINE_REF = "1eb384d80daa700ba2e71ee42872cc9bba926332"

AUTHORIZED_PREFIX = "governance/portfolio/coverage/drafting/EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0/"
PROHIBITED_PREFIXES = ("backend/", "frontend/", "docs/", ".github/", "governance/pia/", "governance/implementation/", "outputs/", "test_reports/", "tests/")

AUTHORITY = "DOCUMENTARY_COVERAGE_ANALYSIS_ONLY_NO_ADOPTION_IMPLEMENTATION_DEPLOYMENT_PILOT_OR_PRODUCTION_AUTHORITY"
AUTHORITY_STATEMENTS = {
    "NO_GOVERNANCE_ARTIFACT_ADOPTED",
    "NO_NEW_PIA_APPROVED",
    "NO_PIA_SUPPLEMENT_APPROVED",
    "NO_CODE_GUIDE_ACTIVATED",
    "NO_ADR_ADOPTED",
    "NO_OPERATING_STANDARD_ADOPTED",
    "NO_RUNBOOK_ADOPTED",
    "NO_APPLICATION_CODE_MODIFIED",
    "NO_SCHEMA_MODIFIED",
    "NO_MIGRATION_CREATED_OR_RUN",
    "NO_PROVIDER_CONFIGURATION_MODIFIED",
    "NO_DEPLOYMENT_AUTHORIZED",
    "NO_STAGING_ACTIVATION_AUTHORIZED",
    "NO_PILOT_ACTIVATION_AUTHORIZED",
    "NO_PRODUCTION_ACTIVATION_AUTHORIZED",
    "NO_PROTECTED_BRANCH_DIRECT_MUTATION",
    "NO_MERGE_AUTHORIZED",
    "NO_RUNTIME_VERIFICATION_CLAIM_WITHOUT_EVIDENCE",
}

ALLOWED_COVERAGE = {
    "FULLY_COVERED", "COVERED_WITH_RETAINED_GAP", "PARTIALLY_COVERED", "CONFLICTING_GOVERNANCE",
    "SOURCE_IDENTITY_UNRESOLVED", "NO_CLEAR_GOVERNANCE_OWNER", "NEW_PIA_CANDIDATE",
    "PIA_SUPPLEMENT_CANDIDATE", "CODE_GUIDE_GAP", "ADR_GAP", "OPERATING_STANDARD_GAP",
    "REGISTER_GAP", "RUNBOOK_GAP", "IMPLEMENTATION_ONLY_GAP", "TESTING_ONLY_GAP",
    "EVIDENCE_ONLY_GAP", "OPERATIONS_ONLY_GAP", "DEFERRED_CAPABILITY", "OUT_OF_SCOPE",
}
ALLOWED_LAYER = {"NOT_APPLICABLE", "NOT_IDENTIFIED", "GAP", "CANDIDATE", "PARTIAL", "COVERED_WITH_RETAINED_GAP", "COVERED", "ADOPTED_NOT_ACTIVE", "ACTIVE"}
ALLOWED_IMPL = {"NOT_DESIGNED", "DOCUMENTED_ONLY", "NOT_FOUND", "PARTIAL_IMPLEMENTATION", "IMPLEMENTED_UNVERIFIED", "REPOSITORY_VERIFIED", "TEST_VERIFIED", "RUNTIME_VERIFIED", "FOUNDER_VERIFIED", "DEPRECATED", "REMOVED"}
ALLOWED_FOUNDER = {"NOT_REQUIRED", "NOT_IDENTIFIED", "PENDING", "APPROVED_DOCUMENTARY_ONLY", "APPROVED_WITH_MODIFICATION", "DEFERRED", "REJECTED", "SUPERSEDED", "ADOPTED", "ACTIVE"}
ALLOWED_RISK_SEVERITY = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_RISK_LIKELIHOOD = {"RARE", "UNLIKELY", "POSSIBLE", "LIKELY"}
ALLOWED_PRIORITY = {"P0", "P1", "P2", "P3"}
ALLOWED_READINESS_BAND = {"CRITICAL_GOVERNANCE_GAP", "LOW_READINESS", "PARTIAL_READINESS", "HIGH_READINESS_WITH_RETAINED_GAPS", "GOVERNANCE_READY"}
ALLOWED_DEP_CONFIDENCE = {"CONFIRMED", "STRONGLY_INFERRED", "PRELIMINARY", "UNVERIFIED"}
ALLOWED_MVP = {"MVP_REQUIRED", "MVP_SUPPORTING", "POST_MVP", "FUTURE", "UNDETERMINED"}
ALLOWED_RELEASE = {"PILOT", "BETA", "GENERAL_AVAILABILITY", "PHASE_2", "FUTURE", "UNASSIGNED"}
ALLOWED_EFFORT = {"XS", "S", "M", "L", "XL", "UNKNOWN"}
ALLOWED_OWNER = {"FOUNDER", "GOVERNANCE", "PRODUCT", "ARCHITECTURE", "ENGINEERING", "SECURITY", "PRIVACY", "OPERATIONS", "QUALITY_ASSURANCE", "LEGAL_COMPLIANCE", "UNASSIGNED"}
ALLOWED_ACTION = {"NO_ACTION_REQUIRED", "VERIFY_REPOSITORY_IMPLEMENTATION", "VERIFY_RUNTIME_BEHAVIOR", "DRAFT_PIA_SUPPLEMENT", "DRAFT_NEW_PIA", "DRAFT_CODE_GUIDE", "DRAFT_ADR", "DRAFT_OPERATING_STANDARD", "DRAFT_RUNBOOK", "RESOLVE_AUTHORITY_CONFLICT", "RESOLVE_DUPLICATE_FEATURE", "CLARIFY_PRODUCT_REQUIREMENT", "DEFER_TO_FUTURE_RELEASE"}
ALLOWED_CHANGE = {"NEW", "UNCHANGED", "RECLASSIFIED", "EXPANDED", "MERGED", "SPLIT", "DEPRECATED", "REMOVED", "RESOLVED"}
SEVERITY_WEIGHT = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
LIKELIHOOD_WEIGHT = {"RARE": 1, "UNLIKELY": 2, "POSSIBLE": 3, "LIKELY": 4}
LAYER_WEIGHTS = {
    "PIA_COVERAGE_STATE": 30,
    "CODE_GUIDE_COVERAGE_STATE": 15,
    "ADR_COVERAGE_STATE": 10,
    "OPERATING_STANDARD_COVERAGE_STATE": 10,
    "RUNBOOK_COVERAGE_STATE": 8,
    "AI_GOVERNANCE_COVERAGE_STATE": 7,
    "SAFEGUARDING_COVERAGE_STATE": 8,
    "PRIVACY_COVERAGE_STATE": 8,
    "REPORTING_COVERAGE_STATE": 4,
}
STATE_FACTOR = {"NOT_APPLICABLE": 1.0, "COVERED": 1.0, "COVERED_WITH_RETAINED_GAP": 0.78, "PARTIAL": 0.55, "CANDIDATE": 0.35, "GAP": 0.12, "NOT_IDENTIFIED": 0.0, "ADOPTED_NOT_ACTIVE": 0.9, "ACTIVE": 1.0}
STATE_CAP = {"FULLY_COVERED": 94, "COVERED_WITH_RETAINED_GAP": 86, "PIA_SUPPLEMENT_CANDIDATE": 74, "CODE_GUIDE_GAP": 68, "ADR_GAP": 66, "OPERATING_STANDARD_GAP": 64, "RUNBOOK_GAP": 64, "NEW_PIA_CANDIDATE": 49}
LAYER_COLUMNS = list(LAYER_WEIGHTS)
REQUIRED_COLUMNS = [
    "Feature ID", "Feature name", "Product domain", "Affected personas", "Governing PIA",
    "Applicable Code Guides", "Current implementation status", "Governance coverage state",
    "Final disposition", "Source IDs", "PIA_COVERAGE_STATE", "CODE_GUIDE_COVERAGE_STATE",
    "ADR_COVERAGE_STATE", "OPERATING_STANDARD_COVERAGE_STATE", "RUNBOOK_COVERAGE_STATE",
    "AI_GOVERNANCE_COVERAGE_STATE", "SAFEGUARDING_COVERAGE_STATE", "PRIVACY_COVERAGE_STATE",
    "REPORTING_COVERAGE_STATE", "GOVERNANCE_READINESS_SCORE", "GOVERNANCE_READINESS_BAND",
    "RISK_SEVERITY", "RISK_LIKELIHOOD", "RISK_SCORE", "DELIVERY_PRIORITY", "GOVERNANCE_PRIORITY",
    "VERIFICATION_PRIORITY", "DEPENDS_ON_FEATURE_IDS", "BLOCKED_BY_FEATURE_IDS", "BLOCKS_FEATURE_IDS",
    "GOVERNANCE_DEPENDENCIES", "IMPLEMENTATION_DEPENDENCIES", "DEPENDENCY_BASIS",
    "DEPENDENCY_CONFIDENCE", "IMPLEMENTATION_STATE", "IMPLEMENTATION_EVIDENCE_PATHS",
    "IMPLEMENTATION_EVIDENCE_TYPE", "IMPLEMENTATION_EVIDENCE_COMMIT", "IMPLEMENTATION_EVIDENCE_PR",
    "IMPLEMENTATION_EVIDENCE_CONFIDENCE", "REPOSITORY_VERIFICATION_STATE", "RUNTIME_VERIFICATION_STATE",
    "TEST_EVIDENCE", "VERIFICATION_NOTES", "ORIGIN_DOCUMENT", "ORIGIN_SECTION", "ORIGIN_REQUIREMENT_ID",
    "GOVERNANCE_AUTHORITY_SOURCE", "FOUNDER_DECISION_ID", "FOUNDER_DECISION_STATE",
    "FOUNDER_DECISION_DATE", "FOUNDER_DECISION_SOURCE_PATH", "AUTHORITY_NOTES", "BUSINESS_VALUE",
    "BUSINESS_VALUE_RATIONALE", "MVP_CLASSIFICATION", "RELEASE_TARGET", "RELEASE_PLANNING_BASIS",
    "REVENUE_RELEVANCE", "OPERATIONAL_RELEVANCE", "SAFETY_RELEVANCE",
    "CUSTOMER_EXPERIENCE_RELEVANCE", "EFFORT_ESTIMATE", "EFFORT_CONFIDENCE",
    "PRIMARY_GAP_OWNER", "SECONDARY_GAP_OWNER", "RECOMMENDED_NEXT_ACTION", "ACTION_ARTIFACT_TYPE",
    "ACTION_DEPENDENCIES", "ACTION_PRIORITY", "ACTION_STATUS", "GAP_OWNER_EXPLANATION",
    "SECONDARY_DOMAINS", "CROSS_CUTTING_CONCERNS", "AI_INVOLVEMENT", "AI_DECISION_IMPACT",
    "MINOR_USER_IMPACT", "GUARDIAN_WORKFLOW_IMPACT", "SAFEGUARDING_RELEVANCE",
    "EQUINE_HEALTH_RELEVANCE", "FINANCIAL_DATA_RELEVANCE", "PERSONAL_DATA_RELEVANCE",
    "SENSITIVE_DOCUMENT_RELEVANCE", "INCIDENT_OR_EMERGENCY_RELEVANCE", "FIRST_INTRODUCED_VERSION",
    "LAST_REVIEWED_VERSION", "LAST_CHANGED_VERSION", "CHANGE_TYPE", "CHANGE_NOTES",
    "SUPERSEDES_FEATURE_ID", "SUPERSEDED_BY_FEATURE_ID",
    "RISK_RATIONALE", "EVIDENCE_LIMITATION_NOTES", "IMPLEMENTATION_EVIDENCE_TIER",
    "PERSONA_ASSIGNMENT_RATIONALE", "PARENT_PIA_SOURCE_STATE", "SOURCE_TRACEABILITY_STATE",
    "PACKAGE_CONTEXT_SOURCES", "DEPENDENCY_TYPE", "PARENT_FEATURE_ID_TYPE",
    "FEATURE_NAME_DISAMBIGUATION",
]
PATH_PATTERN = re.compile(r"^[A-Za-z0-9_./@+-]+$")
TEMPLATE_DESCRIPTION = re.compile(r"^Atomic coverage row for .+ within .+\.$")
FIELD_DICTIONARY_PATH = PACKAGE / "FIELD_DICTIONARY.csv"
DOMAIN_ALLOWED_PIAS = {
    "Administration, support, security, and operations": {"PIA-05", "PIA-02"},
    "Artificial intelligence": {"PIA-05", "PIA-07", "PIA-09", "PIA-10"},
    "Care operations": {"PIA-07", "PIA-04", "PIA-06"},
    "Communications and Owner Portal": {"PIA-10", "PIA-03"},
    "Developer platform and extensibility": {"NO_CURRENT_PIA_OWNER_IDENTIFIED"},
    "Documents, agreements, and electronic signatures": {"PIA-10", "PIA-03"},
    "Facility, barn, business, and physical operations": {"PIA-02"},
    "Financial operations": {"PIA-09"},
    "Horse identity and lifecycle": {"PIA-04", "PIA-03"},
    "Identity and access": {"PIA-01", "PIA-03"},
    "Incidents, emergency, welfare, and biosecurity": {"PIA-07", "PIA-02", "PIA-08"},
    "Integrations and external providers": {"PIA-09", "PIA-10", "PIA-06"},
    "Inventory and assets": {"PIA-07", "PIA-02"},
    "Lessons, training, riders, and guardians": {"PIA-08", "PIA-03", "PIA-06"},
    "Marketplace, provider network, and community": {"NO_CURRENT_PIA_OWNER_IDENTIFIED"},
    "Media, files, and digital assets": {"PIA-10", "PIA-04", "PIA-07"},
    "Mobile, offline, and synchronization": {"PIA-06", "PIA-07", "PIA-04", "PIA-03"},
    "Platform and shell": {"PIA-05"},
    "Relationships and guardianship": {"PIA-03", "PIA-01", "PIA-08"},
    "Reporting and analytics": {"PIA-05", "PIA-09", "PIA-07"},
    "Shows, events, travel, and transport": {"PIA-08", "PIA-06", "PIA-03"},
    "Tasks, calendar, scheduling, and notifications": {"PIA-06"},
}


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_semis(value: str) -> list[str]:
    return [part.strip() for part in (value or "").split(";") if part.strip()]


def readiness_score(row: dict[str, str]) -> int:
    score = int(round(sum(LAYER_WEIGHTS[field] * STATE_FACTOR[row[field]] for field in LAYER_WEIGHTS)))
    return min(score, STATE_CAP[row["Governance coverage state"]])


def readiness_band(score: int) -> str:
    if score <= 24:
        return "CRITICAL_GOVERNANCE_GAP"
    if score <= 49:
        return "LOW_READINESS"
    if score <= 74:
        return "PARTIAL_READINESS"
    if score <= 89:
        return "HIGH_READINESS_WITH_RETAINED_GAPS"
    return "GOVERNANCE_READY"


def expected_governance_state(row: dict[str, str]) -> str:
    action = row["ACTION_ARTIFACT_TYPE"]
    if action == "NEW_PIA" and row["PIA_COVERAGE_STATE"] in {"NOT_IDENTIFIED", "CANDIDATE"}:
        return "NEW_PIA_CANDIDATE"
    if action == "PIA_SUPPLEMENT" and row["PIA_COVERAGE_STATE"] == "PARTIAL":
        return "PIA_SUPPLEMENT_CANDIDATE"
    if row["CODE_GUIDE_COVERAGE_STATE"] == "GAP":
        return "CODE_GUIDE_GAP"
    if row["ADR_COVERAGE_STATE"] == "GAP":
        return "ADR_GAP"
    if row["OPERATING_STANDARD_COVERAGE_STATE"] == "GAP":
        return "OPERATING_STANDARD_GAP"
    if row["RUNBOOK_COVERAGE_STATE"] == "GAP":
        return "RUNBOOK_GAP"
    if action == "NO_NEW_ARTIFACT" and int(row["GOVERNANCE_READINESS_SCORE"]) >= 90:
        return "FULLY_COVERED"
    if action == "IMPLEMENTATION_VERIFICATION":
        return "COVERED_WITH_RETAINED_GAP"
    return row["Governance coverage state"]


def expected_queues(row: dict[str, str]) -> set[str]:
    queues = set()
    if row["FOUNDER_DECISION_STATE"] == "PENDING":
        queues.add("FOUNDER_DECISION_QUEUE")
    if row["Governance coverage state"] == "PIA_SUPPLEMENT_CANDIDATE":
        queues.add("PIA_SUPPLEMENT_QUEUE")
    if row["Governance coverage state"] == "NEW_PIA_CANDIDATE":
        queues.add("NEW_PIA_QUEUE")
    if row["CODE_GUIDE_COVERAGE_STATE"] == "GAP":
        queues.add("CODE_GUIDE_QUEUE")
    if row["ADR_COVERAGE_STATE"] == "GAP":
        queues.add("ADR_QUEUE")
    if row["OPERATING_STANDARD_COVERAGE_STATE"] == "GAP":
        queues.add("OPERATING_STANDARD_QUEUE")
    if row["RUNBOOK_COVERAGE_STATE"] == "GAP":
        queues.add("RUNBOOK_QUEUE")
    if row["IMPLEMENTATION_STATE"] in {"DOCUMENTED_ONLY", "NOT_FOUND", "PARTIAL_IMPLEMENTATION", "IMPLEMENTED_UNVERIFIED"}:
        queues.add("IMPLEMENTATION_VERIFICATION_QUEUE")
    if row["RUNTIME_VERIFICATION_STATE"] == "RUNTIME_VERIFICATION_NOT_PERFORMED" and row["IMPLEMENTATION_STATE"] in {"PARTIAL_IMPLEMENTATION", "IMPLEMENTED_UNVERIFIED"}:
        queues.add("RUNTIME_VERIFICATION_QUEUE")
    if row["Governance coverage state"] == "COVERED_WITH_RETAINED_GAP":
        queues.add("RETAINED_GAP_REREVIEW_QUEUE")
    return queues


def has_dependency_cycle(deps: dict[str, list[str]]) -> bool:
    indegree = {node: 0 for node in deps}
    children = defaultdict(list)
    for node, upstreams in deps.items():
        for dep in upstreams:
            if dep not in deps:
                continue
            indegree[node] += 1
            children[dep].append(node)
    q = deque([node for node, degree in indegree.items() if degree == 0])
    seen = 0
    while q:
        node = q.popleft()
        seen += 1
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                q.append(child)
    return seen != len(deps)


def validate_payload(csv_rows, json_obj, sources, pia_rows, gov_rows, decisions, gaps, queues, dashboard, metrics, dependency_rows, conflict_rows):
    errors = []
    json_rows = json_obj.get("features", [])
    if len(csv_rows) != len(json_rows):
        errors.append(f"CSV/JSON row count mismatch: {len(csv_rows)} != {len(json_rows)}")
    if csv_rows != json_rows:
        errors.append("CSV and JSON feature rows do not agree exactly")
    ids = [r.get("Feature ID", "") for r in csv_rows]
    id_set = set(ids)
    if len(ids) != len(id_set):
        errors.append("Duplicate Feature ID present")
    source_ids = {r["source_id"] for r in sources}
    pia_ids = {r["pia_id"] for r in pia_rows}
    gov_ids = {r["artifact_id"] for r in gov_rows}
    queue_keys = {(q["queue_name"], q["feature_id"]) for q in queues}
    deps = {}
    for row in csv_rows:
        rid = row.get("Feature ID", "<missing>")
        for col in REQUIRED_COLUMNS:
            if col not in row:
                errors.append(f"{rid}: required column {col} missing")
            elif not row.get(col) and col not in {"DEPENDS_ON_FEATURE_IDS", "BLOCKED_BY_FEATURE_IDS", "BLOCKS_FEATURE_IDS", "IMPLEMENTATION_EVIDENCE_PATHS"}:
                errors.append(f"{rid}: required column {col} is blank")
        if row.get("Governance coverage state") not in ALLOWED_COVERAGE:
            errors.append(f"{rid}: invalid coverage state {row.get('Governance coverage state')}")
        for field in LAYER_COLUMNS:
            if row.get(field) not in ALLOWED_LAYER:
                errors.append(f"{rid}: invalid layer state {field}={row.get(field)}")
            if row.get(field) == "ACTIVE":
                errors.append(f"{rid}: active-governance claim without activation evidence in {field}")
        if row.get("IMPLEMENTATION_STATE") not in ALLOWED_IMPL:
            errors.append(f"{rid}: invalid implementation state {row.get('IMPLEMENTATION_STATE')}")
        if row.get("FOUNDER_DECISION_STATE") not in ALLOWED_FOUNDER:
            errors.append(f"{rid}: invalid Founder decision state {row.get('FOUNDER_DECISION_STATE')}")
        if row.get("RISK_SEVERITY") not in ALLOWED_RISK_SEVERITY:
            errors.append(f"{rid}: invalid risk severity {row.get('RISK_SEVERITY')}")
        if row.get("RISK_LIKELIHOOD") not in ALLOWED_RISK_LIKELIHOOD:
            errors.append(f"{rid}: invalid risk likelihood {row.get('RISK_LIKELIHOOD')}")
        for field in ["DELIVERY_PRIORITY", "GOVERNANCE_PRIORITY", "VERIFICATION_PRIORITY", "ACTION_PRIORITY"]:
            if row.get(field) not in ALLOWED_PRIORITY:
                errors.append(f"{rid}: invalid priority {field}={row.get(field)}")
        if row.get("GOVERNANCE_READINESS_BAND") not in ALLOWED_READINESS_BAND:
            errors.append(f"{rid}: invalid readiness band {row.get('GOVERNANCE_READINESS_BAND')}")
        if row.get("DEPENDENCY_CONFIDENCE") not in ALLOWED_DEP_CONFIDENCE:
            errors.append(f"{rid}: invalid dependency confidence {row.get('DEPENDENCY_CONFIDENCE')}")
        if row.get("MVP_CLASSIFICATION") not in ALLOWED_MVP:
            errors.append(f"{rid}: invalid MVP classification {row.get('MVP_CLASSIFICATION')}")
        if row.get("RELEASE_TARGET") not in ALLOWED_RELEASE:
            errors.append(f"{rid}: invalid release target {row.get('RELEASE_TARGET')}")
        if row.get("EFFORT_ESTIMATE") not in ALLOWED_EFFORT:
            errors.append(f"{rid}: invalid effort estimate {row.get('EFFORT_ESTIMATE')}")
        for field in ["PRIMARY_GAP_OWNER", "SECONDARY_GAP_OWNER"]:
            if row.get(field) not in ALLOWED_OWNER:
                errors.append(f"{rid}: invalid owner {field}={row.get(field)}")
        if row.get("RECOMMENDED_NEXT_ACTION") not in ALLOWED_ACTION:
            errors.append(f"{rid}: invalid recommended action {row.get('RECOMMENDED_NEXT_ACTION')}")
        if row.get("CHANGE_TYPE") not in ALLOWED_CHANGE:
            errors.append(f"{rid}: invalid change type {row.get('CHANGE_TYPE')}")
        expected_risk = SEVERITY_WEIGHT.get(row.get("RISK_SEVERITY"), 0) * LIKELIHOOD_WEIGHT.get(row.get("RISK_LIKELIHOOD"), 0)
        if str(expected_risk) != row.get("RISK_SCORE"):
            errors.append(f"{rid}: inconsistent risk score {row.get('RISK_SCORE')} != {expected_risk}")
        try:
            expected_score = readiness_score(row)
            if int(row["GOVERNANCE_READINESS_SCORE"]) != expected_score:
                errors.append(f"{rid}: inconsistent readiness score {row.get('GOVERNANCE_READINESS_SCORE')} != {expected_score}")
            if row["GOVERNANCE_READINESS_BAND"] != readiness_band(expected_score):
                errors.append(f"{rid}: inconsistent readiness band {row.get('GOVERNANCE_READINESS_BAND')}")
        except Exception as exc:
            errors.append(f"{rid}: readiness calculation failed: {exc}")
        if expected_governance_state(row) != row.get("Governance coverage state"):
            errors.append(f"{rid}: governance state is not derivable from layer fields")
        if row.get("Governance coverage state") == "FULLY_COVERED":
            if int(row.get("GOVERNANCE_READINESS_SCORE", "0")) < 90:
                errors.append(f"{rid}: FULLY_COVERED row below governance-ready threshold")
            if any(row[field] == "GAP" for field in LAYER_COLUMNS):
                errors.append(f"{rid}: FULLY_COVERED row has mandatory gap layer")
            if row.get("Gap severity") in {"P0", "P1"}:
                errors.append(f"{rid}: FULLY_COVERED row retains P0/P1 gap")
        if row.get("GOVERNANCE_READINESS_BAND") == "GOVERNANCE_READY" and row.get("Governance coverage state") != "FULLY_COVERED":
            errors.append(f"{rid}: GOVERNANCE_READY row is not FULLY_COVERED")
        if TEMPLATE_DESCRIPTION.match(row.get("Feature or workflow description", "")):
            errors.append(f"{rid}: templated feature description retained")
        if row.get("Governance coverage state") == "FULLY_COVERED" and row.get("IMPLEMENTATION_EVIDENCE_TIER") not in {"CODE_INSPECTED", "TEST_EXECUTED", "RUNTIME_VERIFIED"}:
            errors.append(f"{rid}: FULLY_COVERED overstates unverified evidence tier")
        if row.get("IMPLEMENTATION_STATE") == "NOT_FOUND" and row.get("IMPLEMENTATION_EVIDENCE_PATHS"):
            errors.append(f"{rid}: NOT_FOUND row has implementation evidence paths")
        for path in split_semis(row.get("IMPLEMENTATION_EVIDENCE_PATHS", "")):
            if not PATH_PATTERN.match(path):
                errors.append(f"{rid}: non-path token in IMPLEMENTATION_EVIDENCE_PATHS")
        if row.get("IMPLEMENTATION_EVIDENCE_TIER") == "KEYWORD_MATCH_ONLY" and "keyword" not in row.get("EVIDENCE_LIMITATION_NOTES", "").lower():
            errors.append(f"{rid}: keyword-match tier lacks limitation note")
        if not row.get("RISK_RATIONALE") or "UNCALIBRATED_PLANNING_ONLY" not in row.get("RISK_RATIONALE"):
            errors.append(f"{rid}: missing risk rationale or planning-only calibration")
        if not row.get("PERSONA_ASSIGNMENT_RATIONALE") or "Primary=" not in row.get("PERSONA_ASSIGNMENT_RATIONALE"):
            errors.append(f"{rid}: missing persona assignment rationale")
        if row.get("DEPENDENCY_BASIS") == row.get("DEPENDENCY_CONFIDENCE"):
            errors.append(f"{rid}: dependency basis repeats confidence enum")
        if row.get("Parent feature ID") and row.get("Parent feature ID") not in id_set and row.get("PARENT_FEATURE_ID_TYPE") != "TAXONOMY_ONLY_PARENT":
            errors.append(f"{rid}: parent feature id unresolved without taxonomy-only designation")
        if row.get("Governance coverage state") != "FULLY_COVERED" and row.get("PRIMARY_GAP_OWNER") == "UNASSIGNED" and "UNASSIGNED" not in row.get("GAP_OWNER_EXPLANATION", ""):
            errors.append(f"{rid}: unresolved gap lacks assigned owner or UNASSIGNED explanation")
        if row.get("FOUNDER_DECISION_STATE") in {"APPROVED_DOCUMENTARY_ONLY", "APPROVED_WITH_MODIFICATION", "ADOPTED", "ACTIVE"}:
            if not row.get("FOUNDER_DECISION_SOURCE_PATH") or row.get("FOUNDER_DECISION_DATE") in {"", "NOT_DECIDED"}:
                errors.append(f"{rid}: unsupported Founder approval/adoption claim")
        if row.get("IMPLEMENTATION_STATE") == "REPOSITORY_VERIFIED" and row.get("REPOSITORY_VERIFICATION_STATE") != "REPOSITORY_VERIFIED":
            errors.append(f"{rid}: unsupported implementation verification claim")
        if row.get("IMPLEMENTATION_STATE") == "TEST_VERIFIED" and "TEST_VERIFIED" not in row.get("TEST_EVIDENCE", ""):
            errors.append(f"{rid}: unsupported implementation verification claim")
        if row.get("IMPLEMENTATION_STATE") == "RUNTIME_VERIFIED" and row.get("RUNTIME_VERIFICATION_STATE") != "RUNTIME_VERIFIED":
            errors.append(f"{rid}: unsupported implementation verification claim")
        if row.get("IMPLEMENTATION_STATE") == "FOUNDER_VERIFIED" and row.get("FOUNDER_DECISION_STATE") not in {"APPROVED_DOCUMENTARY_ONLY", "APPROVED_WITH_MODIFICATION", "ADOPTED", "ACTIVE"}:
            errors.append(f"{rid}: unsupported implementation verification claim")
        if row.get("RUNTIME_VERIFICATION_STATE") != "RUNTIME_VERIFICATION_NOT_PERFORMED":
            if "RUNTIME_VERIFIED" not in row.get("TEST_EVIDENCE", ""):
                errors.append(f"{rid}: runtime-verification claim without runtime evidence")
        if row.get("RELEASE_TARGET") != "UNASSIGNED" and ("planning" not in row.get("RELEASE_PLANNING_BASIS", "").lower() or "no adopted release authority" not in row.get("RELEASE_PLANNING_BASIS", "").lower()):
            errors.append(f"{rid}: release-target claim without source or planning disclaimer")
        for sid in split_semis(row.get("Source IDs", "")):
            if sid not in source_ids:
                errors.append(f"{rid}: source id {sid} missing from source register")
        if not row.get("ORIGIN_DOCUMENT") or not row.get("GOVERNANCE_AUTHORITY_SOURCE"):
            errors.append(f"{rid}: missing source authority traceability")
        for pia in [p for p in split_semis(row.get("Governing PIA", "")) if p.startswith("PIA-")]:
            if pia not in pia_ids:
                errors.append(f"{rid}: PIA reference {pia} missing from PIA summary")
            allowed = DOMAIN_ALLOWED_PIAS.get(row.get("Product domain"), set())
            if allowed and pia not in allowed:
                errors.append(f"{rid}: PIA reference {pia} not in declared domain-owner set for {row.get('Product domain')}")
        for guide in [g for g in split_semis(row.get("Applicable Code Guides", "")) if g.startswith("ES-CG-")]:
            if guide not in gov_ids:
                errors.append(f"{rid}: Code Guide reference {guide} missing from governance inventory")
        deps[rid] = split_semis(row.get("DEPENDS_ON_FEATURE_IDS", ""))
        for dep in deps[rid]:
            if dep not in id_set:
                errors.append(f"{rid}: invalid feature dependency {dep}")
            if dep == rid:
                errors.append(f"{rid}: self-dependency is not allowed")
        for queue in expected_queues(row):
            if (queue, rid) not in queue_keys:
                errors.append(f"{rid}: missing derived queue row {queue}")
    for q in queues:
        fid = q.get("feature_id")
        if fid not in id_set:
            errors.append(f"queue row not present in matrix: {fid}")
            continue
        row = next(r for r in csv_rows if r["Feature ID"] == fid)
        if q["queue_name"] != "CONFLICT_RESOLUTION_QUEUE" and q["queue_name"] not in expected_queues(row):
            errors.append(f"{fid}: queue row {q['queue_name']} not derivable from matrix")
        if q["queue_name"] == "CONFLICT_RESOLUTION_QUEUE" and "atomic conflict" not in q.get("rationale", "").lower():
            errors.append(f"{fid}: conflict queue row lacks atomic conflict derivation")
    if has_dependency_cycle(deps):
        errors.append("circular dependency without explanation")
    if len({r.get("ORIGIN_DOCUMENT", "") for r in csv_rows}) < len({r.get("Product domain", "") for r in csv_rows}):
        errors.append("origin document traceability is not domain-specific")
    total = len(csv_rows)
    for key, values in metrics.get("counts", {}).items():
        if key == "product_domains":
            actual = Counter(r["Product domain"] for r in csv_rows)
        elif key == "governance_state":
            actual = Counter(r["Governance coverage state"] for r in csv_rows)
        elif key == "implementation_state":
            actual = Counter(r["IMPLEMENTATION_STATE"] for r in csv_rows)
        elif key == "risk_severity":
            actual = Counter(r["RISK_SEVERITY"] for r in csv_rows)
        elif key == "readiness_band":
            actual = Counter(r["GOVERNANCE_READINESS_BAND"] for r in csv_rows)
        elif key == "gap_owner":
            actual = Counter(r["PRIMARY_GAP_OWNER"] for r in csv_rows)
        elif key == "release_target":
            actual = Counter(r["RELEASE_TARGET"] for r in csv_rows)
        elif key == "personas":
            actual = Counter()
            for row in csv_rows:
                for persona in split_semis(row["Affected personas"]):
                    actual[persona] += 1
        else:
            continue
        expected = {k: v["rows"] for k, v in values.items()}
        if dict(actual) != expected:
            errors.append(f"metrics count mismatch for {key}")
        for k, v in values.items():
            actual_pct = f"{actual[k] / total * 100:.1f}%"
            if v["percent"] != actual_pct:
                errors.append(f"metrics percentage mismatch for {key}:{k}")
    dash_counts = dashboard.get("counts", {})
    checks = {
        "governance_state": Counter(r["Governance coverage state"] for r in csv_rows),
        "implementation_state": Counter(r["IMPLEMENTATION_STATE"] for r in csv_rows),
        "risk_severity": Counter(r["RISK_SEVERITY"] for r in csv_rows),
        "readiness_band": Counter(r["GOVERNANCE_READINESS_BAND"] for r in csv_rows),
        "release_target": Counter(r["RELEASE_TARGET"] for r in csv_rows),
        "gap_owner": Counter(r["PRIMARY_GAP_OWNER"] for r in csv_rows),
        "queue": Counter(q["queue_name"] for q in queues),
    }
    for key, actual in checks.items():
        if dict(actual) != dash_counts.get(key):
            errors.append(f"dashboard count mismatch for {key}")
    if dashboard.get("row_count") != total:
        errors.append("dashboard row_count mismatch")
    conflict_features = set()
    for conflict in conflict_rows:
        for fid in split_semis(conflict.get("AFFECTED_FEATURE_IDS", "")):
            if fid and fid not in id_set:
                errors.append(f"conflict register references missing feature {fid}")
            conflict_features.add(fid)
        if len(split_semis(conflict.get("AFFECTED_FEATURE_IDS", ""))) > 1:
            errors.append(f"{conflict.get('conflict_id', '<conflict>')}: conflict row is not atomic")
        for field in ["CONFLICT_TYPE", "CONFLICT_SEVERITY", "AFFECTED_FEATURE_IDS", "AFFECTED_ARTIFACTS", "PROPOSED_RESOLUTION", "RESOLUTION_AUTHORITY_REQUIRED", "CONFLICT_STATUS"]:
            if not conflict.get(field):
                errors.append(f"{conflict.get('conflict_id', '<conflict>')}: missing {field}")
    try:
        dictionary_rows = read_csv(FIELD_DICTIONARY_PATH)
        by_field = {row["field_name"]: row for row in dictionary_rows}
        for field in REQUIRED_COLUMNS:
            if field not in by_field:
                errors.append(f"field dictionary missing required field {field}")
                continue
            entry = by_field[field]
            if entry.get("description", "").startswith("Matrix field retained or added"):
                errors.append(f"field dictionary retains boilerplate for {field}")
            for required in ["data_type", "allowed_values_or_format", "owning_role", "derivation_method", "null_blank_handling", "maintenance_trigger", "field_authority_class"]:
                if not entry.get(required):
                    errors.append(f"field dictionary missing {required} for {field}")
    except Exception as exc:
        errors.append(f"field dictionary validation failed: {exc}")
    return errors


def validate_manifest_and_checksums():
    errors = []
    actual = sorted(str(p.relative_to(PACKAGE)) for p in PACKAGE.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_paths = sorted(entry["path"] for entry in manifest["files"])
    if manifest_paths != actual:
        errors.append("PACKAGE_MANIFEST.json does not cover exactly every package file")
    checksum_entries = {}
    for line in CHECKSUM_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        h, path = line.split("  ", 1)
        checksum_entries[path] = h
    for entry in manifest["files"]:
        path = entry["path"]
        p = PACKAGE / path
        if not p.exists():
            errors.append(f"manifest path missing: {path}")
            continue
        data = p.read_bytes()
        if path == "CHECKSUMS.sha256":
            if entry["sha256"] != "LEDGER_SELF_REFERENCE_EXCLUDED":
                errors.append("CHECKSUMS.sha256 manifest entry must exclude self hash")
            continue
        if path == "PACKAGE_MANIFEST.json":
            if entry["sha256"] != "MANIFEST_SELF_REFERENCE_EXCLUDED":
                errors.append("PACKAGE_MANIFEST.json manifest entry must exclude self hash")
            continue
        if entry["byte_length"] != len(data):
            errors.append(f"manifest byte length mismatch: {path}")
        actual_hash = hashlib.sha256(data).hexdigest()
        if entry["sha256"] != actual_hash:
            errors.append(f"manifest sha mismatch: {path}")
        if checksum_entries.get(path) != actual_hash:
            errors.append(f"checksum mismatch: {path}")
    if "CHECKSUMS.sha256" in checksum_entries:
        errors.append("CHECKSUMS.sha256 must not self-reference")
    if "PACKAGE_MANIFEST.json" in checksum_entries:
        errors.append("PACKAGE_MANIFEST.json must not self-reference")
    return errors


def validate_authorized_paths():
    errors = []
    try:
        subprocess.run(["git", "rev-parse", "--verify", BASELINE_REF], cwd=REPO, check=True, capture_output=True, text=True, timeout=5)
    except Exception as exc:
        return [f"authorized-path verification blocked: baseline ref unavailable or unverifiable: {exc}"]
    try:
        status = subprocess.run(["git", "status", "--porcelain=v1", "--untracked-files=all", "--", AUTHORIZED_PREFIX], cwd=REPO, check=True, capture_output=True, text=True, timeout=30)
        changed = []
        for line in status.stdout.splitlines():
            if not line.strip():
                continue
            path = line[3:].strip()
            if " -> " in path:
                path = path.split(" -> ", 1)[1].strip()
            changed.append(path)
    except Exception as exc:
        return [f"authorized-path verification blocked: unable to enumerate changed paths: {exc}"]
    for path in changed:
        if not path.startswith(AUTHORIZED_PREFIX):
            errors.append(f"changed path outside authorized package: {path}")
        if path.startswith(PROHIBITED_PREFIXES) and not path.startswith(AUTHORIZED_PREFIX):
            errors.append(f"prohibited application/schema/config/provider/deployment path changed: {path}")
    return errors


def validate_authority_disclaimers():
    errors = []
    text = ""
    for name in [
        f"{ARTIFACT_ID}.md",
        "COVERAGE_ANALYSIS_AND_RECOMMENDATIONS_REPORT.md",
        "README_FIRST.md",
        "DOCUMENTARY_VALIDATION_REPORT.json",
        "GOVERNANCE_LAYER_AND_READINESS_METHODOLOGY.md",
        "IMPLEMENTATION_VERIFICATION_METHODOLOGY.md",
        "RISK_PRIORITY_METHODOLOGY.md",
    ]:
        text += (PACKAGE / name).read_text(encoding="utf-8") + "\n"
    if AUTHORITY not in text:
        errors.append("primary authority statement missing")
    for statement in AUTHORITY_STATEMENTS:
        if statement not in text:
            errors.append(f"authority disclaimer missing: {statement}")
    return errors


def load_payload():
    csv_rows = read_csv(CSV_PATH)
    json_obj = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    sources = read_csv(SOURCE_PATH)
    pia_rows = read_csv(PIA_PATH)
    gov_rows = read_csv(GOV_PATH)
    decisions = read_csv(DECISION_PATH)
    gaps = read_csv(GAP_PATH)
    queues = read_csv(QUEUE_PATH)
    dashboard = json.loads(DASHBOARD_PATH.read_text(encoding="utf-8"))
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    dependency_rows = read_csv(DEPENDENCY_PATH)
    conflict_rows = read_csv(CONFLICT_PATH)
    return csv_rows, json_obj, sources, pia_rows, gov_rows, decisions, gaps, queues, dashboard, metrics, dependency_rows, conflict_rows


def main() -> int:
    errors = []
    errors.extend(validate_payload(*load_payload()))
    errors.extend(validate_manifest_and_checksums())
    errors.extend(validate_authorized_paths())
    errors.extend(validate_authority_disclaimers())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    csv_rows, _, sources, *_ = load_payload()
    print("DOCUMENTARY_VALIDATION_PASS")
    print(f"feature_rows={len(csv_rows)}")
    print(f"source_rows={len(sources)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
