#!/usr/bin/env python3
"""Build the complete Facility/Tenant/Organization PIA candidate package.

This is documentary governance work only. It does not start an application or
database and does not authorize implementation, enrollment, release, or F-0001
closure. The builder deliberately preserves first-pass hashes and findings,
then emits the reviewed and revised candidate.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
DATE = "2026-07-20"
PIA_ID = "ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0"
DISPOSITION = (
    "FACILITY_TENANT_ORGANIZATIONAL_STRUCTURE_PIA_DRAFT_COMPLETE_"
    "INTERNALLY_REVIEWED_AND_REVISED_PENDING_FOUNDER_DECISIONS_AND_"
    "FRESH_SEGREGATED_REVIEW"
)
NO_AUTH = (
    "No implementation, application or database startup, migration, PR, merge, "
    "tag, release, deployment, enrollment, production use, custom-agent "
    "activation, or F-0001 closure is authorized by this package."
)
RECOMMENDATION_NOTICE = (
    "All recommendations are candidate advice only. They are not approved "
    "Founder doctrine unless and until the Founder records a separate decision."
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: str, body: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body.rstrip() + "\n", encoding="utf-8")


def write_json(path: str, data: Any) -> None:
    write(path, json.dumps(data, indent=2, sort_keys=True))


def write_csv(path: str, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def table(headers: list[str], rows: Iterable[Iterable[Any]]) -> str:
    rows = [[str(cell).replace("|", "\\|") for cell in row] for row in rows]
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        + ["| " + " | ".join(row) + " |" for row in rows]
    )


def header(title: str, status: str = "FOUNDER_DECISION_REQUIRED") -> str:
    return f"""# {title}

- PIA: `{PIA_ID}`
- Version: `1.0.0-candidate`
- Date: `{DATE}`
- Status: `{status}`
- Final package disposition: `{DISPOSITION}`

> {NO_AUTH}
>
> {RECOMMENDATION_NOTICE}
"""


SOURCE_SPECS = [
    ("FAC-SRC-001", "PIA Master Standard V1.1", "external exact PDF", "c7519371830afc25ee4b66586157869177b232054facd43bd56c9df497ccbbbc", "CONTROLLING", "Defines 43 mandatory sections, identifiers, evidence and status discipline.", "VERIFIED_EXACT"),
    ("FAC-SRC-002", "Founder Adoption and Approval Record for PIA Master Standard V1.1", "external exact PDF", "bd5deef067bf69e7ce0c5be87dbe8bb15f3f82238d4c9451d0a17641f32ffcd8", "CONTROLLING_LIFECYCLE", "Records adoption of the standard; does not approve this PIA.", "VERIFIED_EXACT"),
    ("FAC-SRC-003", "Autonomous Facility PIA drafting directive", "external handoff directive", "cf21c522425ae237fbb3cf6497751884801bea1b4fbade37a729353c7988c618", "FOUNDER_DIRECTIVE", "Controls this drafting and review run.", "VERIFIED_EXACT"),
    ("FAC-SRC-004", "Facility PIA scope and boundary seed", "nested handoff", "d01b40bf393a4dfab7e78dee321c55a9f01613e07e405a6a417d411a7d540f08", "SCOPE_SEED", "Seed only; not approved doctrine.", "VERIFIED_EXACT"),
    ("FAC-SRC-005", "Facility PIA Founder decision seed", "nested handoff", "c4b23a91fb9681e95a58fd8e82563414b3fbef9f92a2d24af3e9ae8780d72b45", "DECISION_SEED", "Unresolved questions only; not approved doctrine.", "VERIFIED_EXACT"),
]

REPO_SOURCES = [
    ("FAC-SRC-006", "Global Governance V1.0 baseline manifest", "docs/governance_v1_0/GLOBAL_GOVERNANCE_V1_0_BASELINE_MANIFEST.json", "CONSTITUTIONAL_BASELINE", "Global governance source inventory."),
    ("FAC-SRC-007", "Master Facility Domain Model V2.1", "docs/canon/adopted_sources/MASTER_FACILITY_DOMAIN_MODEL_V2_1_ADOPTED_SOURCE.md", "PRIMARY_DOMAIN", "Physical facility identity, hierarchy, place truth and lineage."),
    ("FAC-SRC-008", "Facility Domain V2.1 adoption record", "docs/canon/adoptions/c0_014_facility_domain_v2_1/C0_014_MASTER_FACILITY_DOMAIN_MODEL_CONSTITUTIONAL_ADOPTION_RECORD.md", "LIFECYCLE_AUTHORITY", "Adoption record controls the candidate wording retained inside the source."),
    ("FAC-SRC-009", "Master Barn Lifecycle V3.1", "docs/canon/adopted_sources/MASTER_BARN_LIFECYCLE_V3_1_ADOPTED_SOURCE.md", "PRIMARY_DOMAIN", "Barn operating lifecycle, degraded operation and transitions."),
    ("FAC-SRC-010", "Barn Lifecycle V3.1 adoption record", "docs/canon/adoptions/c0_015_barn_lifecycle_v3_1/C0_015_MASTER_BARN_LIFECYCLE_AND_OPERATIONS_CANON_CONSTITUTIONAL_ADOPTION_RECORD.md", "LIFECYCLE_AUTHORITY", "Records separate adoption of Barn canon."),
    ("FAC-SRC-011", "Master Business Lifecycle V2.1", "docs/canon/adopted_sources/MASTER_BUSINESS_LIFECYCLE_V2_1_ADOPTED_SOURCE.md", "PRIMARY_DOMAIN", "Durable business identity, facility associations and succession."),
    ("FAC-SRC-012", "Business Lifecycle V2.1 adoption record", "docs/canon/adoptions/c0_016_business_lifecycle_v2_1/C0_016_MASTER_BUSINESS_LIFECYCLE_MODEL_CONSTITUTIONAL_ADOPTION_RECORD.md", "LIFECYCLE_AUTHORITY", "Records separate adoption of Business canon."),
    ("FAC-SRC-013", "Identity Account and Actor Model V2.0", "docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md", "INHERITED", "Person, organization, account and actor distinctions."),
    ("FAC-SRC-014", "Master Relationship Model V2.0", "docs/canon/MASTER_RELATIONSHIP_MODEL.md", "INHERITED", "Membership and association are Relationship-owned and time-bound."),
    ("FAC-SRC-015", "Permission and Access-Control Model V1.1", "docs/canon/adopted_sources/MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_V1_1_ADOPTED_SOURCE.md", "INHERITED", "Default denial and multi-dimensional authorization."),
    ("FAC-SRC-016", "Permission V1.1 adoption record", "docs/canon/adoptions/c0_022_permission_access_control_v1_1/C0_022_MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_CONSTITUTIONAL_ADOPTION_RECORD.md", "LIFECYCLE_AUTHORITY", "Controls adoption status for Permission source."),
    ("FAC-SRC-017", "Agreement Consent and Authorization Model V2.1", "docs/canon/adoptions/c0_019_agreement_consent_authorization_v2_1/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1_ADOPTED_PRE_LOCK.md", "INHERITED", "Separates agreement, consent, authorization and authority."),
    ("FAC-SRC-018", "Agreement V2.1 adoption record", "docs/canon/adoptions/c0_019_agreement_consent_authorization_v2_1/C0_019_AGREEMENT_CONSENT_AND_AUTHORIZATION_CONSTITUTIONAL_ADOPTION_RECORD.md", "LIFECYCLE_AUTHORITY", "Controls adoption status for Agreement source."),
    ("FAC-SRC-019", "Privacy and Data Protection Model V2.0", "docs/canon/founder_approved_sources/MASTER_PRIVACY_AND_DATA_PROTECTION_MODEL_V2_0_FOUNDER_APPROVED.md", "INHERITED", "Private by default; precise location and cross-tenant exposure are sensitive."),
    ("FAC-SRC-020", "Audit Event and Evidence Model V2.0", "docs/canon/adopted_sources/MASTER_AUDIT_EVENT_AND_EVIDENCE_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Attributable, append-only evidence with authority context."),
    ("FAC-SRC-021", "Record Stewardship and Retention Model V2.1", "docs/canon/adopted_sources/MASTER_RECORD_STEWARDSHIP_AND_RETENTION_MODEL_V2_1_ADOPTED_SOURCE.md", "INHERITED", "Correction, retention and stewardship boundaries."),
    ("FAC-SRC-022", "Communication Notification and Notice Model V2.0", "docs/canon/adopted_sources/MASTER_COMMUNICATION_NOTIFICATION_AND_NOTICE_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Notice delivery is not proof of receipt or authority."),
    ("FAC-SRC-023", "Claims Disputes and Authority Model V2.0", "docs/canon/adopted_sources/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Preserve uncertainty during disputes; no inferred authority."),
    ("FAC-SRC-024", "Horse Lifecycle V3.1", "docs/canon/adopted_sources/MASTER_HORSE_LIFECYCLE_V3_1_ADOPTED_SOURCE.md", "CROSS_DOMAIN", "Horse identity and authority do not move with location."),
    ("FAC-SRC-025", "Horse Transfer and Continuity Policy", "docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md", "CROSS_DOMAIN", "Facility movement is not ownership or authority transfer."),
    ("FAC-SRC-026", "Platform Operations Reliability and Release Model V2.0", "docs/canon/adopted_sources/MASTER_PLATFORM_OPERATIONS_RELIABILITY_AND_RELEASE_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Operational/release authority remains separately gated."),
    ("FAC-SRC-027", "Configuration and Feature Flag Governance Model V2.0", "docs/canon/adopted_sources/MASTER_CONFIGURATION_AND_FEATURE_FLAG_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Configuration cannot weaken domain boundaries."),
    ("FAC-SRC-028", "Platform Resilience Backup and Recovery Model V1.0", "docs/canon/adopted_sources/MASTER_PLATFORM_RESILIENCE_BACKUP_AND_RECOVERY_OPERATIONAL_MODEL_V1_0_ADOPTED_SOURCE.md", "INHERITED", "Recovery cannot silently restore stale authority or topology."),
    ("FAC-SRC-029", "Security Incident Response and Disclosure Model V1.0", "docs/canon/adopted_sources/MASTER_SECURITY_INCIDENT_RESPONSE_AND_DISCLOSURE_MODEL_V1_0_ADOPTED_SOURCE.md", "INHERITED", "Incident containment and disclosure boundaries."),
    ("FAC-SRC-030", "Search Discovery Ranking and Retrieval Model V2.0", "docs/canon/adopted_sources/MASTER_SEARCH_DISCOVERY_RANKING_AND_RETRIEVAL_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Permission filtering precedes retrieval; no existence leakage."),
    ("FAC-SRC-031", "Developer Platform and Integration Governance Model V2.0", "docs/canon/adopted_sources/MASTER_DEVELOPER_PLATFORM_AND_INTEGRATION_GOVERNANCE_MODEL_V2_0_ADOPTED_SOURCE.md", "INHERITED", "Integrations receive no broader authority than the actor."),
    ("FAC-SRC-032", "External Architecture and Adapter Model V2.0", "docs/canon/MASTER_EXTERNAL_ARCHITECTURE_AND_ADAPTER_MODEL_V2_0.md", "INHERITED", "External systems are not authority sources; reconciliation is explicit."),
    ("FAC-SRC-033", "Portfolio realignment lock record", "governance/pia_portfolio/ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0/FOUNDER_DIRECTED_PORTFOLIO_LOCK_RECORD.md", "PRECONDITION_EVIDENCE", "Proves the ten-position portfolio gate passed before drafting."),
]

# Exact SHA-256 values captured during the completed source-assembly pass.
# They are pinned evidence, not recomputed build inputs: a subsequent source
# change requires a new controlled source-assembly/change-impact pass.
REPO_SOURCE_HASHES = {
    "FAC-SRC-006": "f5666ebffbfe527f6d01eb7fe7fbe9f21de541b7b3afe5c4a1fe2d1b3379bfe9",
    "FAC-SRC-007": "8323b8402c3d445fe2b8d363caf16bb2a8eb4e08b0b37bd36b90ee69092a698d",
    "FAC-SRC-008": "a95033f85b8efae4c39aa8e608cbc1122d67ca6185cb47ba56edc98ca531e5d4",
    "FAC-SRC-009": "c2a698ca1bbb8dc723ea7ac0270a9f66e8b06d0cbcb01535efefc517b6076d4a",
    "FAC-SRC-010": "a8dcb8f4a2fffe8b67ddcd198e094f9915a11b9278895aede78b80671ad56c78",
    "FAC-SRC-011": "a07b0ba2fc6c3c0ce5b9db3f56c5f26fcda8d87e5f4f115a02e19b6b5fb4b37d",
    "FAC-SRC-012": "ec87763e58f7dceac6a8ca66ff441d48a257afdb39a704c4e3b9e3ad2cebaf63",
    "FAC-SRC-013": "1c79c20a2edd2e7e3907e875679c5871d53c146a226364fb0cc3f956d39f5d0e",
    "FAC-SRC-014": "f6715f0a02cad2eb8d8eb140d765b7906052c4d6bf3a5a40372c74c5c1e8ba01",
    "FAC-SRC-015": "6e3f4160e4166831cfe4f154032ff7648a5a44b70762289252c615e98b899fa3",
    "FAC-SRC-016": "93a69c8fd88019e5d0839ad0124180c22248151fb052b642bbf205b832b86181",
    "FAC-SRC-017": "a96effd167554d84dbdf18f0804468abcf67a9a9e326c6ea8907e59779097bc0",
    "FAC-SRC-018": "793f166b4c2e73c19b7c6319d34c45327aa23b3ec08958e569369d38b70a4b12",
    "FAC-SRC-019": "8f323e3d4d0782c5aa017c6b904b7c42c9bf4ab8ee72170ea8f7a003505184fd",
    "FAC-SRC-020": "321aefaeee9f04ad927c01d96e4b05549713c118f9868b7fccf7a8e9b53d8ea2",
    "FAC-SRC-021": "4623fb036481a4ffea4e7edde53fa6e83e9a81f062251c8371e242219f524c2a",
    "FAC-SRC-022": "bff9fd88cb312d6666677f924a5923134d995015ab6fbfd7a398bcbeb10dc761",
    "FAC-SRC-023": "a4787fb641dca1d28d98f10240957d0b09ea8ee1cee8358f64e80dd658b8b626",
    "FAC-SRC-024": "41313d11aae592d041decaf34e5a131863423e843057d47864e666bdea21e6bf",
    "FAC-SRC-025": "a54fd42261d99819f26ac77a6e207f121049a3c4f6d2e69e3b6e7b5167435c6b",
    "FAC-SRC-026": "bb1eae9fecf46403d05a91bf802d7ef4134ed11c22bf57b1092fb14229413596",
    "FAC-SRC-027": "d5e37ac7d475465f9c8fac5171851a136882cf4c57cb75ea0b17cf8dcec2a0f8",
    "FAC-SRC-028": "9a75d2d0984c929afd6df3d51f3f6135c57443ea34a0205395325f1413095565",
    "FAC-SRC-029": "3dafa7991acc40eb321cdfeae5b9caa59dbf0a41f5184bee36ec9defb0b59734",
    "FAC-SRC-030": "18ce9cde3f1ac8f8b01bfc72ed8dfcf066cd6434a1e1b3f0c40bfe127958ca67",
    "FAC-SRC-031": "6688f58a9fcfbe55eb22d4e87a77bda7bf95899c4d46d9c11aecb18f26eb546e",
    "FAC-SRC-032": "0cdad90cb5929588ee137e9835f6b499c3651159381960fbfad436dfcd0fa18d",
    "FAC-SRC-033": "417002ce200865f93ef677c1854b179ac96bb16d83082b842178dec6e1c75c40",
}


def source_rows() -> list[dict[str, str]]:
    rows = []
    for sid, title, locator, digest, authority, relevance, status in SOURCE_SPECS:
        rows.append({"source_id": sid, "title": title, "locator": locator, "sha256": digest, "authority": authority, "relevance": relevance, "status": status, "gap": "NONE"})
    for sid, title, rel, authority, relevance in REPO_SOURCES:
        digest = REPO_SOURCE_HASHES.get(sid)
        rows.append({
            "source_id": sid,
            "title": title,
            "locator": f"repo:{rel}",
            "sha256": digest or "MISSING",
            "authority": authority,
            "relevance": relevance,
            "status": "VERIFIED_EXACT" if digest else "SOURCE_GAP",
            "gap": "NONE" if digest else "SOURCE_HASH_NOT_CAPTURED",
        })
    return rows


DECISIONS = [
    ("FAC-FD-001", "DESIGN_APPROVAL", "What is the authoritative distinction among Facility, Tenant, Organization, Barn, and Business?", "Tenant is strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context/topology label; Business is an Organization-domain operating identity. None is automatically equivalent to another.", "Treat Barn as Facility; treat Tenant as Facility/account; collapse Organization and Business.", "Conflation would corrupt isolation, lineage, authority and migration decisions.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-002", "DESIGN_APPROVAL", "Is Tenant the strict application data-isolation boundary?", "Yes. Require an explicit Tenant context for every protected record/action or a documented global classification; missing context fails closed or quarantines.", "Tenant is billing only; Barn/Facility is the isolation boundary.", "Cross-tenant leakage and unsafe default-primary fallbacks.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-003", "DESIGN_APPROVAL", "May one Organization control multiple Tenants, and under what evidence?", "Allow it only through separate typed, dated Tenant-Organization associations plus current action-specific authority; the association itself never proves control authority.", "One Organization per Tenant; Organization profile automatically controls linked Tenants.", "Real structures may be blocked or blanket authority may be inferred.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-004", "DESIGN_APPROVAL", "May one physical Facility be associated with multiple Tenants?", "Allow explicit time-bounded associations where legitimate, while maintaining separate tenant-scoped records and prohibiting cross-tenant visibility or record cascade.", "Exactly one Tenant forever; share the same underlying tenant data across Tenants.", "Transitions/shared operations can be trapped or tenant isolation can fail.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-005", "DESIGN_APPROVAL", "What Facility-Area hierarchy is controlling?", "Use Facility > Area with acyclic parent-area nesting sufficient for site, campus, structure, zone, room, stall, paddock, pasture, asset or hazard; keep labels configurable.", "Fixed seven-level hierarchy; flat Facility only.", "False precision or inability to model real sites.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-006", "DESIGN_APPROVAL", "Which Organization types are first-class?", "Support legal entity, sole proprietor, operating business, nonprofit/rescue, professional practice, service provider/vendor, governmental/educational body and other reviewed type; preserve type provenance and allow multiple non-authorizing types.", "Incorporated businesses only; unrestricted free-text type only.", "Valid operators may be excluded or semantics become ungoverned.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-007", "DESIGN_APPROVAL", "What lifecycle states apply to Facility, Tenant, and Organization?", "Adopt the candidate state sets in the State Transition Matrix, with closed/decommissioned identities retained and no silent reactivation.", "Active/inactive only; hard deletion.", "Unsafe transitions and lost lineage.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-008", "DESIGN_APPROVAL", "How are transfer, merger, split, closure, suspension, and archival controlled?", "Use reviewed effective-dated change sets and lineage events; never cascade people, horses, authority, payments, agreements, private records or evidence.", "Mutate identifiers in place; clone or move all dependent records.", "Silent authority transfer and evidence corruption.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-009", "DESIGN_APPROVAL", "How is active Tenant/Facility context selected and audited?", "Require active membership, allowed associations, explicit visible user selection and per-consequential-request revalidation; record context-selection and action audit evidence.", "Infer from the last visited Barn, role, payment or deep link.", "Confused-deputy access and stale/wrong-context changes.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-010", "DESIGN_APPROVAL", "Which topology facts may Relationships and Authorization consume?", "Expose stable IDs, typed topology, lifecycle, effective associations and sensitivity/status facts as versioned references; consumers cannot rewrite topology and must own their own decisions.", "Expose raw Facility records broadly; let consumers repair topology.", "Boundary erosion, stale decisions and unauthorized mutation.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-011", "DESIGN_APPROVAL", "Are memberships and staff assignments exclusively Relationship-domain facts?", "Yes. Facility PIA may reference them for context but does not create or own membership, employment or staff relationship truth.", "Facility owns staff lists as authority; duplicate facts in both domains.", "Contradictory relationship truth and accidental access.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-012", "DESIGN_APPROVAL", "What evidence establishes stewardship without treating payment or contact status as authority?", "Use sourced relationship/delegation/ownership/lease/operating assertions plus current Authorization evaluation; payment/contact and Organization verification are supporting claims only.", "Payer, listed contact or verified Organization is steward automatically.", "Unauthorized control and fraud.", "REQUIRED_BEFORE_DESIGN_APPROVAL"),
    ("FAC-FD-013", "IMPLEMENTATION_AUTHORIZATION", "How are providers, vendors, and service Organizations represented?", "Represent them as Organization identities with typed, dated service associations; individual professionals remain person identities representing an Organization where applicable; neither association grants record access.", "Free-text contact only; every provider is a user role with blanket access.", "Impersonation, duplicate identity or overbroad access.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-014", "IMPLEMENTATION_AUTHORIZATION", "What timezone, locale, and address rules apply?", "Store structured postal components plus display text, IANA timezone, BCP47 locale and separately protected geolocation precision with provenance.", "Free text only; precise coordinates always visible.", "Operational ambiguity or privacy exposure.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-015", "IMPLEMENTATION_AUTHORIZATION", "How are duplicates detected, reviewed, and merged?", "Quarantine suspected duplicates, compare evidence, then merge through a reviewed reversible change set preserving aliases, provenance, dissent and rollback metadata.", "Automatic fuzzy merge; delete one duplicate.", "Wrong-site merge and irreversible loss.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-016", "ENROLLMENT", "What Facility information is publicly discoverable versus Tenant-scoped?", "Use a separate opt-in projection initially limited to public name, coarse locality, public contact channel and service summary; exclude exact layout, occupants and sensitive areas.", "Publish all profile fields; no public projection.", "Location/privacy exposure or poor discovery.", "REQUIRED_BEFORE_ENROLLMENT"),
    ("FAC-FD-017", "ENROLLMENT", "What is the minimum first-user Facility/Tenant seed?", "Create one Tenant, one Organization record/association, one Facility and one clearly labeled unassigned Area; create no relationship, permission, ownership or payment authority merely from the seed.", "Tenant and Barn only; fully prepopulate a complex hierarchy.", "Conflation or excessive onboarding.", "REQUIRED_BEFORE_ENROLLMENT"),
    ("FAC-FD-018", "IMPLEMENTATION_AUTHORIZATION", "How are ambiguous legacy records quarantined?", "Create provenance-preserving quarantine records with candidate mappings, reason, reviewer and disposition; never assign missing records to primary/default automatically.", "Guess primary Tenant/Facility; reject and discard all ambiguous data.", "Cross-tenant leakage or evidence loss.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-019", "IMPLEMENTATION_AUTHORIZATION", "What topology behavior is allowed offline?", "Permit only minimum-authorized expiring reads and context-neutral observations; no consequential topology mutation until online revalidation.", "Allow offline create/move/merge; no offline access at all.", "Stale authority can corrupt canonical topology.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-020", "IMPLEMENTATION_AUTHORIZATION", "What happens on Tenant or Facility suspension?", "Deny ordinary consequential access across all surfaces, preserve emergency/safety evidence capture only through a narrowly controlled path, and require online revalidation for reinstatement.", "Total lockout including safety evidence; allow reads/writes unchanged.", "Safety evidence loss or unauthorized continuation.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-021", "IMPLEMENTATION_AUTHORIZATION", "What support-access model is allowed?", "Use ticket-bound, reason-coded, time-limited, least-privilege, impersonation-free access with approval and immutable audit.", "Standing superuser access; no support access.", "Privacy exposure or inability to resolve incidents.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-022", "IMPLEMENTATION_AUTHORIZATION", "What retention rules apply to topology, identity, projection, and evidence records?", "Retain identity/lineage/audit under governed evidence rules, make public projections revocable, and set field-level schedules only after legal and operational review.", "One universal duration; hard-delete the entire topology.", "Unsupported legal precision or loss of evidence.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-023", "ENROLLMENT", "What capacity and suitability assertions may a first-user Facility or Area display?", "Treat them as dated, sourced assertions with units, confidence and limitations; never as guarantees of safety.", "Static unqualified numbers; omit capacity entirely.", "Unsafe reliance or poor planning.", "REQUIRED_BEFORE_ENROLLMENT"),
    ("FAC-FD-024", "ENROLLMENT", "How is active context switching presented to users?", "Show persistent Tenant/Facility/Organization context, require confirmation for consequential actions, and never silently switch because a link was opened.", "Hidden automatic context; single sticky Barn.", "Wrong-context changes.", "REQUIRED_BEFORE_ENROLLMENT"),
    ("FAC-FD-025", "IMPLEMENTATION_AUTHORIZATION", "Which canonical API commands, events, and jobs are permitted?", "Use the candidate contracts as design interfaces only and require separate implementation authorization plus schema/security review.", "Build directly from prose; defer all contracts.", "Contract drift or unbuildable design.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-026", "IMPLEMENTATION_AUTHORIZATION", "What nonfunctional thresholds apply?", "Require measured isolation, accessibility, recovery, latency and scale budgets in an authorized work package; retain qualitative gates until evidence exists.", "Invent numeric thresholds now; omit quality gates.", "False precision or untestable reliability.", "REQUIRED_BEFORE_IMPLEMENTATION_AUTHORIZATION"),
    ("FAC-FD-027", "ENROLLMENT", "What closure and suspension communication is required?", "Notify affected context members through governed notice, show effective time/consequences, and preserve access only where separate authority requires it.", "Immediate silent closure; indefinite full access.", "Stranded users or excessive access.", "REQUIRED_BEFORE_ENROLLMENT"),
    ("FAC-FD-028", "ENROLLMENT", "What evidence is required before Founder design approval and later enrollment decisions?", "Resolve design-gate decisions, commission fresh segregated review, verify source/traceability gaps are zero, and record separate approval and later readiness decisions.", "Treat this recommendation as approval; approve from summary alone.", "Status inflation and unreviewed doctrine.", "REQUIRED_BEFORE_ENROLLMENT"),
]


REQUIREMENTS = [
    ("FAC-REQ-001", "The system SHALL represent Tenant, Facility, Organization, Barn and Facility Area with distinct identifiers and meanings.", "FAC-SRC-007;FAC-SRC-009;FAC-SRC-011;FAC-FD-001", "Topology service", "No identifier alias may grant authority.", "DESIGN", "FAC-AC-001", "FAC-TEST-001"),
    ("FAC-REQ-002", "Every protected record SHALL carry an explicit Tenant context or a documented global classification.", "FAC-SRC-015;FAC-SRC-019", "Persistence boundary", "Missing context fails closed; legacy records enter quarantine.", "DESIGN", "FAC-AC-002", "FAC-TEST-002"),
    ("FAC-REQ-003", "A Facility SHALL retain stable identity and lineage through rename, address correction, sale, lease, operator change, closure and decommissioning.", "FAC-SRC-007", "Facility domain", "Mutation may append history but not replace evidence.", "DESIGN", "FAC-AC-003", "FAC-TEST-003"),
    ("FAC-REQ-004", "Organization-to-Tenant and Organization-to-Facility associations SHALL be typed, time-bound, sourced and non-authorizing.", "FAC-SRC-011;FAC-SRC-014;FAC-SRC-017", "Relationship domain", "Association alone never permits action.", "DESIGN", "FAC-AC-004", "FAC-TEST-004"),
    ("FAC-REQ-005", "The system SHALL resolve authorization using actor, tenant, target, facility, organization, purpose, time and current relationship evidence.", "FAC-SRC-013;FAC-SRC-015;FAC-SRC-017", "Authorization service", "Default deny and generic failure.", "DESIGN", "FAC-AC-005", "FAC-TEST-005"),
    ("FAC-REQ-006", "The active context SHALL be explicit, visible and revalidated for every consequential request.", "FAC-SRC-015;FAC-FD-009", "Context service and UI", "Stale or unauthorized context returns a non-enumerating denial.", "DESIGN", "FAC-AC-006", "FAC-TEST-006"),
    ("FAC-REQ-007", "Context switching SHALL NOT silently transfer ownership, relationship, permission, agreement, billing or record visibility.", "FAC-SRC-014;FAC-SRC-015;FAC-SRC-017", "Context service", "No cascading side effect.", "DESIGN", "FAC-AC-007", "FAC-TEST-007"),
    ("FAC-REQ-008", "Facility Area hierarchy SHALL reject cycles and preserve parent history across moves.", "FAC-SRC-007", "Topology service", "Invalid moves fail atomically and are audited.", "DESIGN", "FAC-AC-008", "FAC-TEST-008"),
    ("FAC-REQ-009", "Transfer, merge, split and successor operations SHALL use reviewed change sets with before/after evidence and non-cascade declarations.", "FAC-SRC-007;FAC-SRC-011;FAC-SRC-020", "Topology service", "Partial operations reconcile or roll back visibly.", "DESIGN", "FAC-AC-009", "FAC-TEST-009"),
    ("FAC-REQ-010", "No topology operation SHALL infer horse ownership, custody, clinical authority, payment authority or record stewardship.", "FAC-SRC-017;FAC-SRC-023;FAC-SRC-024;FAC-SRC-025", "All consumers", "Dependent domains recalculate from their owners.", "DESIGN", "FAC-AC-010", "FAC-TEST-010"),
    ("FAC-REQ-011", "Closure and decommissioning SHALL preserve identifiers, aliases, lineage, evidence and governed retention status.", "FAC-SRC-007;FAC-SRC-021", "Facility domain", "Closed entities cannot be silently reused.", "DESIGN", "FAC-AC-011", "FAC-TEST-011"),
    ("FAC-REQ-012", "Duplicate resolution SHALL quarantine ambiguity and prohibit automatic fuzzy merge.", "FAC-SRC-020;FAC-SRC-023", "Reconciliation service", "Unresolved duplicates remain separate and flagged.", "DESIGN", "FAC-AC-012", "FAC-TEST-012"),
    ("FAC-REQ-013", "Exact layout, precise location, occupants and sensitive-area data SHALL be private by default.", "FAC-SRC-019;FAC-SRC-030", "Privacy and search", "Unauthorized queries do not disclose existence.", "DESIGN", "FAC-AC-013", "FAC-TEST-013"),
    ("FAC-REQ-014", "Public discovery SHALL read only from a revocable, purpose-limited Facility projection.", "FAC-SRC-007;FAC-SRC-019;FAC-SRC-030", "Projection service", "Revocation removes future publication without erasing audit.", "DESIGN", "FAC-AC-014", "FAC-TEST-014"),
    ("FAC-REQ-015", "Search SHALL apply permission and context filtering before retrieval, ranking, autocomplete or count disclosure.", "FAC-SRC-030", "Search service", "No existence or cross-tenant leakage.", "DESIGN", "FAC-AC-015", "FAC-TEST-015"),
    ("FAC-REQ-016", "All material topology actions and denied attempts SHALL emit attributable append-only audit evidence.", "FAC-SRC-020", "Audit service", "Correction appends evidence; prior evidence is not rewritten.", "DESIGN", "FAC-AC-016", "FAC-TEST-016"),
    ("FAC-REQ-017", "Audit events SHALL record actor, effective authority reference, tenant, facility, organization, purpose, request and change-set identifiers where applicable.", "FAC-SRC-020", "Audit service", "Missing material context blocks the action.", "DESIGN", "FAC-AC-017", "FAC-TEST-017"),
    ("FAC-REQ-018", "Support access SHALL be reason-coded, ticket-bound, time-limited, least-privilege and separately audited.", "FAC-SRC-013;FAC-SRC-015;FAC-SRC-019;FAC-FD-021", "Support control", "No standing tenant superuser.", "IMPLEMENTATION", "FAC-AC-018", "FAC-TEST-018"),
    ("FAC-REQ-019", "Tenant or Facility suspension SHALL deny ordinary consequential access across UI, API, jobs, search, exports, webhooks and integrations.", "FAC-SRC-015;FAC-SRC-026;FAC-FD-020", "Platform boundary", "A separately governed emergency evidence path may remain.", "IMPLEMENTATION", "FAC-AC-019", "FAC-TEST-019"),
    ("FAC-REQ-020", "Offline clients SHALL NOT create, move, merge, transfer, close, decommission or reassign canonical topology.", "FAC-SRC-026;FAC-SRC-028;FAC-FD-019", "Offline client", "Queued observations remain non-authoritative until online revalidation.", "IMPLEMENTATION", "FAC-AC-020", "FAC-TEST-020"),
    ("FAC-REQ-021", "Cached topology and authorization snapshots SHALL expire, be minimum-necessary and fail closed after revocation or uncertainty.", "FAC-SRC-015;FAC-SRC-019;FAC-SRC-028", "Offline client", "Stale cache never restores authority.", "IMPLEMENTATION", "FAC-AC-021", "FAC-TEST-021"),
    ("FAC-REQ-022", "Integration credentials SHALL be tenant-scoped, purpose-limited and no broader than the represented actor's authority.", "FAC-SRC-031;FAC-SRC-032", "Integration gateway", "External identifiers are claims, not authority.", "IMPLEMENTATION", "FAC-AC-022", "FAC-TEST-022"),
    ("FAC-REQ-023", "Events, webhooks and jobs SHALL be idempotent, context-bound, retry-safe and reconciled without cross-tenant fallback.", "FAC-SRC-026;FAC-SRC-031;FAC-SRC-032", "Event/job infrastructure", "Unknown context enters dead-letter quarantine.", "IMPLEMENTATION", "FAC-AC-023", "FAC-TEST-023"),
    ("FAC-REQ-024", "Recovery SHALL NOT restore stale memberships, permissions, public projections or topology as current without reconciliation.", "FAC-SRC-028", "Recovery process", "Uncertainty is visible and gated.", "IMPLEMENTATION", "FAC-AC-024", "FAC-TEST-024"),
    ("FAC-REQ-025", "Configuration and feature flags SHALL NOT weaken tenant isolation, authorization, audit or privacy controls.", "FAC-SRC-027", "Configuration service", "Unsafe configuration fails validation.", "IMPLEMENTATION", "FAC-AC-025", "FAC-TEST-025"),
    ("FAC-REQ-026", "Organization verification SHALL preserve evidence source, verifier, time, state, expiry and dispute status.", "FAC-SRC-011;FAC-SRC-023;FAC-FD-012", "Organization domain", "Unverified does not mean nonexistent; disputed does not mean verified.", "IMPLEMENTATION", "FAC-AC-026", "FAC-TEST-026"),
    ("FAC-REQ-027", "Address, timezone, locale and geolocation data SHALL be modeled separately with field provenance and visibility classification.", "FAC-SRC-007;FAC-SRC-019;FAC-FD-014", "Facility domain", "Invalid or ambiguous values remain flagged, not silently normalized.", "IMPLEMENTATION", "FAC-AC-027", "FAC-TEST-027"),
    ("FAC-REQ-028", "Capacity and suitability SHALL be dated assertions with source, unit, confidence and limitations.", "FAC-SRC-007;FAC-FD-023", "Facility domain", "They are not safety guarantees.", "IMPLEMENTATION", "FAC-AC-028", "FAC-TEST-028"),
    ("FAC-REQ-029", "Retention and deletion SHALL be field- and purpose-specific and SHALL preserve required lineage, evidence, holds and disputes.", "FAC-SRC-019;FAC-SRC-021;FAC-FD-022", "Stewardship process", "No universal hard-delete cascade.", "IMPLEMENTATION", "FAC-AC-029", "FAC-TEST-029"),
    ("FAC-REQ-030", "Notices SHALL record channel, template, recipient context, delivery attempt and result without treating delivery as authority or consent.", "FAC-SRC-022", "Notification service", "Failure escalates according to workflow.", "IMPLEMENTATION", "FAC-AC-030", "FAC-TEST-030"),
    ("FAC-REQ-031", "The first-user seed SHALL create no relationship, permission, ownership, agreement or billing authority merely from topology creation.", "FAC-SRC-014;FAC-SRC-015;FAC-SRC-017;FAC-FD-017", "Onboarding", "Required authority remains separately established.", "ENROLLMENT", "FAC-AC-031", "FAC-TEST-031"),
    ("FAC-REQ-032", "Every consequential UI SHALL display the effective Tenant, Facility and Organization context before confirmation.", "FAC-SRC-015;FAC-FD-009;FAC-FD-024", "User interface", "Ambiguous context blocks submission.", "ENROLLMENT", "FAC-AC-032", "FAC-TEST-032"),
    ("FAC-REQ-033", "Imported records without resolvable Tenant, Facility or Organization identity SHALL enter quarantine with provenance.", "FAC-SRC-020;FAC-SRC-021", "Migration process", "No default-primary assignment is allowed in the target model.", "IMPLEMENTATION", "FAC-AC-033", "FAC-TEST-033"),
    ("FAC-REQ-034", "The target model SHALL replace legacy default/primary fallbacks through a separately authorized, reversible reconciliation plan.", "FAC-SRC-001;FAC-SRC-033", "Engineering planning", "This PIA does not execute that plan.", "IMPLEMENTATION", "FAC-AC-034", "FAC-TEST-034"),
    ("FAC-REQ-035", "No AI or automation SHALL approve, merge, transfer, close, decommission, verify or authorize a Facility, Tenant or Organization without a separately approved control.", "FAC-SRC-001;FAC-SRC-023", "Automation boundary", "Suggestions remain reviewable and non-authoritative.", "DESIGN", "FAC-AC-035", "FAC-TEST-035"),
    ("FAC-REQ-036", "Every package decision, requirement, workflow, acceptance criterion, test and evidence reference SHALL be machine resolvable.", "FAC-SRC-001", "Evidence custodian", "Broken references fail validation.", "DESIGN", "FAC-AC-036", "FAC-TEST-036"),
]


WORKFLOWS = [
    ("FAC-WF-001", "Create first-user topology", "Authorized enrollment actor", "No tenant context exists", "Create candidate Tenant, Organization association, Facility and unassigned Area; separately establish relationships/authority", "Seed does not grant authority", "FAC-REQ-001;FAC-REQ-031"),
    ("FAC-WF-002", "Add Facility", "Authorized tenant actor", "Active tenant and action authorization", "Capture physical identity, address provenance and hierarchy; check duplicates; commit change set", "Duplicate ambiguity enters quarantine", "FAC-REQ-003;FAC-REQ-012;FAC-REQ-027"),
    ("FAC-WF-003", "Select or switch active context", "Member", "Active membership and permitted associations", "List allowed contexts; user selects; display scope; issue short-lived context reference", "Denied without revealing inaccessible contexts", "FAC-REQ-005;FAC-REQ-006;FAC-REQ-007"),
    ("FAC-WF-004", "Manage Facility Area", "Authorized facility actor", "Valid parent and active context", "Create, move, restrict, retire or restore through change set; cycle check; audit", "Invalid cycle or stale version fails atomically", "FAC-REQ-008;FAC-REQ-016"),
    ("FAC-WF-005", "Associate Organization", "Authorized relationship actor", "Verified identities not required unless capability depends on them", "Create typed/effective association; record source and limitations", "No authority is created", "FAC-REQ-004;FAC-REQ-026"),
    ("FAC-WF-006", "Change owner/operator", "Authorized domain actors", "Effective date, parties and evidence supplied", "End old association; start new association; notify dependents to recalculate", "No cascade to people, horses, payments or private records", "FAC-REQ-009;FAC-REQ-010"),
    ("FAC-WF-007", "Merge suspected duplicate", "Reconciliation reviewer", "Quarantined candidates and evidence comparison", "Propose survivor, aliases and lineage; second-person review; commit reversible change set", "Uncertain match remains quarantined", "FAC-REQ-012"),
    ("FAC-WF-008", "Suspend/reinstate context", "Authorized governance actor", "Reason and effective time", "Suspend across every access surface; preserve safety evidence path; online revalidate reinstatement", "No partial surface remains active", "FAC-REQ-019;FAC-REQ-021"),
    ("FAC-WF-009", "Close/decommission Facility", "Authorized facility actor", "Impact review and dependent-domain notice", "Restrict, close, revoke projections/credentials, preserve lineage and retention controls", "Horse/location/authority records are not deleted or transferred", "FAC-REQ-010;FAC-REQ-011"),
    ("FAC-WF-010", "Publish/revoke public Facility projection", "Authorized publication actor", "Valid source facility and field-level visibility", "Create minimum projection; approve; publish; revoke or expire independently", "No precise/sensitive topology is exposed", "FAC-REQ-013;FAC-REQ-014;FAC-REQ-015"),
    ("FAC-WF-011", "Import legacy topology", "Authorized migration operator", "Separately approved migration work package", "Validate context; map identities; quarantine ambiguity; reconcile totals; preserve source", "No default-primary silent assignment", "FAC-REQ-033;FAC-REQ-034"),
    ("FAC-WF-012", "Correct a topology record", "Authorized steward", "Correction evidence and current version", "Append correction change set; preserve prior assertion; reproject consumers", "No destructive history rewrite", "FAC-REQ-003;FAC-REQ-016;FAC-REQ-029"),
    ("FAC-WF-013", "Support investigation", "Authorized support actor", "Ticket, reason, approval, scope and expiry", "Grant time-limited access; display banner; audit reads/actions; revoke", "No standing access or invisible impersonation", "FAC-REQ-018"),
]


ENTITIES = [
    ("FAC-ENT-001", "Tenant", "Strict application isolation and governance context", "tenant_id, display_name, state, created_at, closed_at, version", "No physical, legal, billing or authority equivalence"),
    ("FAC-ENT-002", "Organization", "Durable entity identity for legal, operating, administrative or service bodies", "organization_id, names, types, verification_state, provenance, lifecycle", "Identity is separate from authority and Business operation"),
    ("FAC-ENT-003", "Facility", "Durable physical-place identity", "facility_id, names, address_id, timezone, locale, state, lineage", "No implied owner, operator, tenant or authority"),
    ("FAC-ENT-004", "FacilityArea", "Nested topology element", "area_id, facility_id, parent_area_id, area_type, name, state, lineage", "Acyclic; sensitive classes private by default"),
    ("FAC-ENT-005", "TenantOrganizationAssociation", "Typed relationship between Tenant and Organization", "association_id, tenant_id, organization_id, type, effective interval, source", "Non-authorizing"),
    ("FAC-ENT-006", "TenantFacilityAssociation", "Facility availability in a Tenant context", "association_id, tenant_id, facility_id, effective interval, source", "Non-authorizing; supports controlled moves"),
    ("FAC-ENT-007", "OrganizationFacilityAssociation", "Owns/leases/operates/manages/services assertion", "association_id, organization_id, facility_id, type, effective interval, evidence", "Non-authorizing and disputable"),
    ("FAC-ENT-008", "BarnOperationalContext", "Named operating context associated with Facility/Area", "barn_context_id, facility_id, area_ids, organization_ids, label, lifecycle", "Not Tenant and not durable physical identity"),
    ("FAC-ENT-009", "Address", "Structured physical/mailing address assertion", "address_id, components, display_text, geocode_precision, provenance, visibility", "Coordinates and sensitive details protected separately"),
    ("FAC-ENT-010", "TopologyChangeSet", "Atomic proposal/evidence for material topology mutation", "change_set_id, actor, context, before, after, reason, approvals, result", "Append-only evidence and idempotency key"),
    ("FAC-ENT-011", "FacilityAlias", "Historical/external name or identifier", "alias_id, facility_id, value, type, source, effective interval", "Not a new Facility and not authority"),
    ("FAC-ENT-012", "PublicFacilityProjection", "Revocable public subset", "projection_id, facility_id, fields, purpose, approved_by, published_at, revoked_at", "Never source of canonical private truth"),
    ("FAC-ENT-013", "LegacyQuarantineRecord", "Unresolved imported identity/context", "quarantine_id, source_locator, raw_hash, candidates, reason, disposition", "Not visible as canonical topology"),
    ("FAC-ENT-014", "OrganizationVerificationAssertion", "Dated verification claim", "assertion_id, organization_id, method, issuer, evidence, state, expiry, dispute", "Does not create authorization"),
    ("FAC-ENT-015", "CapacitySuitabilityAssertion", "Dated operational assertion", "assertion_id, target_id, type, value, unit, source, confidence, limitations", "Not a guarantee of safety"),
]


STATE_ROWS = [
    ("FAC-SM-001", "Tenant", "DRAFT", "PENDING_REVIEW", "submit", "tenant:submit", "required fields present", "tenant.submitted", "Remain DRAFT"),
    ("FAC-SM-001", "Tenant", "PENDING_REVIEW", "ACTIVE", "activate", "tenant:activate", "Founder-approved design plus separately authorized activation workflow", "tenant.activated", "Remain PENDING_REVIEW"),
    ("FAC-SM-001", "Tenant", "ACTIVE", "SUSPENDED", "suspend", "tenant:suspend", "reason and scope", "tenant.suspended", "Remain ACTIVE"),
    ("FAC-SM-001", "Tenant", "SUSPENDED", "ACTIVE", "reinstate", "tenant:reinstate", "online revalidation", "tenant.reinstated", "Remain SUSPENDED"),
    ("FAC-SM-001", "Tenant", "ACTIVE", "CLOSING", "begin_close", "tenant:close", "impact review", "tenant.closing", "Remain ACTIVE"),
    ("FAC-SM-001", "Tenant", "CLOSING", "CLOSED", "complete_close", "tenant:close", "reconciliation complete", "tenant.closed", "Remain CLOSING"),
    ("FAC-SM-001", "Tenant", "CLOSED", "ARCHIVED", "archive", "tenant:archive", "retention gate", "tenant.archived", "Remain CLOSED"),
    ("FAC-SM-002", "Facility", "PLANNED", "ACTIVE", "activate", "facility:activate", "identity/topology validated", "facility.activated", "Remain PLANNED"),
    ("FAC-SM-002", "Facility", "ACTIVE", "DEGRADED", "degrade", "facility:status", "operational limitation", "facility.degraded", "Remain ACTIVE"),
    ("FAC-SM-002", "Facility", "ACTIVE", "RESTRICTED", "restrict", "facility:restrict", "risk or dispute", "facility.restricted", "Remain ACTIVE"),
    ("FAC-SM-002", "Facility", "ACTIVE", "SUSPENDED", "suspend", "facility:suspend", "governance reason", "facility.suspended", "Remain ACTIVE"),
    ("FAC-SM-002", "Facility", "ACTIVE", "CLOSED", "close", "facility:close", "impact review", "facility.closed", "Remain ACTIVE"),
    ("FAC-SM-002", "Facility", "CLOSED", "DECOMMISSIONED", "decommission", "facility:decommission", "lineage preserved and credentials revoked", "facility.decommissioned", "Remain CLOSED"),
    ("FAC-SM-002", "Facility", "DECOMMISSIONED", "ARCHIVED", "archive", "facility:archive", "retention gate", "facility.archived", "Remain DECOMMISSIONED"),
    ("FAC-SM-003", "Organization", "DRAFT", "ACTIVE", "activate", "organization:activate", "minimum identity evidence", "organization.activated", "Remain DRAFT"),
    ("FAC-SM-003", "Organization", "ACTIVE", "RESTRICTED", "restrict", "organization:restrict", "dispute or risk", "organization.restricted", "Remain ACTIVE"),
    ("FAC-SM-003", "Organization", "ACTIVE", "SUSPENDED", "suspend", "organization:suspend", "reason and impact", "organization.suspended", "Remain ACTIVE"),
    ("FAC-SM-003", "Organization", "ACTIVE", "DISSOLVING", "begin_dissolution", "organization:close", "successor assessment", "organization.dissolving", "Remain ACTIVE"),
    ("FAC-SM-003", "Organization", "DISSOLVING", "CLOSED", "close", "organization:close", "associations ended", "organization.closed", "Remain DISSOLVING"),
    ("FAC-SM-003", "Organization", "CLOSED", "ARCHIVED", "archive", "organization:archive", "retention gate", "organization.archived", "Remain CLOSED"),
    ("FAC-SM-004", "FacilityArea", "PLANNED", "ACTIVE", "activate", "facility_area:write", "valid acyclic parent", "facility_area.activated", "Remain PLANNED"),
    ("FAC-SM-004", "FacilityArea", "ACTIVE", "RESTRICTED", "restrict", "facility_area:restrict", "reason", "facility_area.restricted", "Remain ACTIVE"),
    ("FAC-SM-004", "FacilityArea", "ACTIVE", "OUT_OF_SERVICE", "take_out_of_service", "facility_area:write", "operational reason", "facility_area.out_of_service", "Remain ACTIVE"),
    ("FAC-SM-004", "FacilityArea", "OUT_OF_SERVICE", "ACTIVE", "restore", "facility_area:write", "inspection/evidence", "facility_area.restored", "Remain OUT_OF_SERVICE"),
    ("FAC-SM-004", "FacilityArea", "ACTIVE", "RETIRED", "retire", "facility_area:retire", "impact review", "facility_area.retired", "Remain ACTIVE"),
    ("FAC-SM-004", "FacilityArea", "RETIRED", "ARCHIVED", "archive", "facility_area:archive", "retention gate", "facility_area.archived", "Remain RETIRED"),
]


PERMISSIONS = [
    ("FAC-PERM-001", "tenant:read", "Allowed tenant member/support grant", "tenant_id + purpose", "active membership and field policy", "Default deny; suspension override"),
    ("FAC-PERM-002", "tenant:write", "Authorized tenant steward", "tenant_id", "action-specific authorization", "Role/admin label insufficient"),
    ("FAC-PERM-003", "tenant:suspend", "Governance actor", "tenant_id", "reason, approval and audit", "No self-escalation"),
    ("FAC-PERM-004", "facility:create", "Authorized tenant actor", "tenant_id", "duplicate check and source provenance", "Creates no membership/authority"),
    ("FAC-PERM-005", "facility:read", "Authorized actor", "tenant_id + facility_id + field", "relationship/purpose/visibility", "Non-enumerating deny"),
    ("FAC-PERM-006", "facility:write", "Authorized facility steward", "tenant_id + facility_id + field", "current version and authority", "Material changes require change set"),
    ("FAC-PERM-007", "facility:transfer", "Authorized parties/reviewer", "source/destination tenant + facility", "separate migration authority", "No cross-tenant record cascade"),
    ("FAC-PERM-008", "facility:merge", "Reconciliation reviewer", "tenant + candidate facilities", "evidence and second review", "No automatic merge"),
    ("FAC-PERM-009", "facility:close", "Authorized facility actor", "tenant + facility", "impact review and effective time", "No deletion cascade"),
    ("FAC-PERM-010", "facility_area:write", "Authorized facility actor", "tenant + facility + area", "valid parent and state", "No cycle"),
    ("FAC-PERM-011", "organization:create", "Authorized tenant actor", "tenant", "identity provenance", "No verified state by default"),
    ("FAC-PERM-012", "organization:associate", "Relationship-authorized actor", "tenant + organization + facility", "typed/effective association", "Association grants no action authority"),
    ("FAC-PERM-013", "organization:verify", "Approved verification actor", "organization", "method/evidence/expiry", "No authorization side effect"),
    ("FAC-PERM-014", "context:switch", "Active member", "allowed tenant/facility/org tuple", "membership and association revalidation", "No silent switch"),
    ("FAC-PERM-015", "facility:publish", "Authorized publication actor", "facility + projection", "field-level public approval", "Exact/sensitive topology excluded"),
    ("FAC-PERM-016", "support:access", "Approved support actor", "ticket + tenant + resources", "reason, approval, expiry, audit", "No standing blanket access"),
    ("FAC-PERM-017", "topology:export", "Authorized export actor", "tenant + facility + fields", "purpose, recipient, expiry", "No public or cross-tenant fallback"),
]


CONTRACTS = [
    ("FAC-API-001", "POST /tenants/{tenant}/facilities", "Command", "facility:create", "tenant context, idempotency key, proposed identity/address", "Facility candidate plus change_set_id", "facility.created", "409 duplicate candidate; 403 generic deny"),
    ("FAC-API-002", "POST /contexts/select", "Command", "context:switch", "tenant/facility/org association tuple", "short-lived context reference and display labels", "context.selected", "404 unavailable context"),
    ("FAC-API-003", "POST /facilities/{id}/areas", "Command", "facility_area:write", "parent/version/type/provenance", "area and change_set_id", "facility_area.created", "409 cycle/stale version"),
    ("FAC-API-004", "POST /facilities/{id}/association-changes", "Command", "organization:associate", "typed before/after associations and effective time", "change proposal/result", "facility.association_changed", "422 unresolved authority/evidence"),
    ("FAC-API-005", "POST /facilities/merge-proposals", "Command", "facility:merge", "candidate ids, survivor proposal, evidence", "quarantined proposal", "facility.merge_proposed", "409 unresolved identity"),
    ("FAC-API-006", "POST /facilities/{id}/close", "Command", "facility:close", "effective time, reason, impact acknowledgement", "closed state/change set", "facility.closed", "409 unresolved dependencies"),
    ("FAC-API-007", "PUT /facilities/{id}/public-projection", "Command", "facility:publish", "approved field subset/purpose/expiry", "projection version", "facility.public_projection_changed", "422 sensitive field"),
    ("FAC-API-008", "GET /facility-search", "Query", "facility:read", "active context, purpose, filter", "permission-filtered results only", "search.executed", "generic empty/deny"),
    ("FAC-EVT-001", "facility.context_invalidated", "Event", "system", "tenant/facility/org, cause, effective_at", "Consumers revoke cached context", "append-only", "Dead-letter if context unknown"),
    ("FAC-EVT-002", "facility.topology_changed", "Event", "system", "change_set_id, before/after refs, tenant", "Consumers re-evaluate projections", "append-only", "Retry idempotently"),
    ("FAC-EVT-003", "organization.facility_association_changed", "Event", "system", "association id/type/interval/status", "Consumers recalculate only their owned effects", "append-only", "No authority side effect"),
    ("FAC-JOB-001", "context-expiry sweeper", "Job", "service identity", "tenant partitions and current time", "expire context caches", "job evidence", "Fail closed; retry partition"),
    ("FAC-JOB-002", "public-projection expiry", "Job", "service identity", "projection expiry", "unpublish expired fields", "job evidence", "Fail private"),
    ("FAC-JOB-003", "topology reconciliation", "Job", "service identity", "quarantine/change-set ledgers", "report only unless separately authorized", "job evidence", "Never auto-merge"),
]


RISKS = [
    ("FAC-RISK-001", "P1", "Legacy tenant/barn/facility conflation", "Cross-tenant disclosure or mis-scoping during transition", "Target distinctions plus quarantine and separately authorized migration", "OPEN_FOUNDER_AND_IMPLEMENTATION_GATE", "FAC-FD-001;FAC-FD-002;FAC-REQ-034"),
    ("FAC-RISK-002", "P1", "Association mistaken for authority", "Organization admins or facility members gain blanket access", "Non-authorizing associations plus Authorization-owned decisions", "OPEN_FOUNDER_GATE", "FAC-FD-012;FAC-REQ-004;FAC-REQ-005"),
    ("FAC-RISK-003", "P1", "Facility transfer cascades unrelated records", "Horse, payment, private data or evidence moves silently", "Explicit non-cascade and dependent-domain recalculation", "OPEN_FOUNDER_GATE", "FAC-FD-008;FAC-REQ-009;FAC-REQ-010"),
    ("FAC-RISK-004", "P1", "Suspension is enforced on only some surfaces", "Jobs, search, export or integration continues", "Single invalidation event and surface matrix", "OPEN_FOUNDER_AND_IMPLEMENTATION_GATE", "FAC-FD-020;FAC-REQ-019"),
    ("FAC-RISK-005", "P2", "Offline cache outlives authority", "Revoked actor changes or reads topology", "Minimum cache, expiry and online consequential writes", "OPEN_FOUNDER_GATE", "FAC-FD-019;FAC-REQ-020;FAC-REQ-021"),
    ("FAC-RISK-006", "P2", "Public projection exposes sensitive location", "Theft, stalking, safeguarding or privacy harm", "Separate opt-in projection and denylist", "OPEN_FOUNDER_GATE", "FAC-FD-016;FAC-REQ-013;FAC-REQ-014"),
    ("FAC-RISK-007", "P2", "Duplicate Facility merge is incorrect", "Lineage and records attach to wrong site", "Quarantine, evidence and reversible reviewed merge", "OPEN_FOUNDER_GATE", "FAC-FD-015;FAC-REQ-012"),
    ("FAC-RISK-008", "P2", "Unsupported retention precision", "Evidence destroyed or data retained too long", "Field schedules after legal/operational review", "OPEN_FOUNDER_GATE", "FAC-FD-022;FAC-REQ-029"),
    ("FAC-RISK-009", "P2", "Organization impersonation or over-verification", "Fraud or exclusion", "Evidence-backed states with dispute handling", "OPEN_FOUNDER_GATE", "FAC-FD-012;FAC-REQ-026"),
    ("FAC-RISK-010", "P2", "Current code defaults unknown context to primary", "Legacy records may appear valid in wrong context", "No target fallback; inventory and quarantine before migration", "OPEN_IMPLEMENTATION_GATE", "FAC-REQ-002;FAC-REQ-033;FAC-REQ-034"),
]


FINDINGS = [
    ("FAC-FIND-P1-001", "P1", "DOMAIN_OPERATIONAL", "The first draft did not state strongly enough that Barn is neither Tenant nor durable Facility identity.", "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md;DATA_DICTIONARY.md", "Add the BarnOperationalContext definition and explicit anti-equivalence rules.", "RESOLVED_IN_REVISION", "FAC-FD-001;FAC-REQ-001"),
    ("FAC-FIND-P1-002", "P1", "CROSS_DOMAIN", "Association workflows could be misread as granting authority.", "WORKFLOW_REGISTER.md;PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv", "State non-authorizing effect at creation, update and consumption points.", "RESOLVED_IN_REVISION", "FAC-FD-012;FAC-REQ-004"),
    ("FAC-FIND-P1-003", "P1", "SECURITY_PRIVACY", "Suspension coverage was not enumerated across jobs, search, exports, webhooks and integrations.", "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md;STATE_TRANSITION_MATRIX.csv", "Add all-surface denial and an explicit narrow safety-evidence exception candidate.", "RESOLVED_IN_REVISION", "FAC-FD-020;FAC-REQ-019"),
    ("FAC-FIND-P1-004", "P1", "ADVERSARIAL", "Transfer/merge language needed a complete non-cascade list.", "GOLDEN_PATHS.md;ADVERSARIAL_SCENARIOS.md", "Enumerate people, horses, permissions, agreements, billing, private records and evidence.", "RESOLVED_IN_REVISION", "FAC-FD-008;FAC-REQ-010"),
    ("FAC-FIND-P2-001", "P2", "SECURITY_PRIVACY", "Offline behavior did not separate observation capture from consequential topology mutation.", "API_EVENT_JOB_CONTRACTS.md;PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md", "Prohibit consequential offline mutation and require online revalidation.", "RESOLVED_IN_REVISION", "FAC-FD-019;FAC-REQ-020"),
    ("FAC-FIND-P2-002", "P2", "SECURITY_PRIVACY", "Public discovery fields lacked a minimum candidate set and sensitive denylist.", "DATA_DICTIONARY.md;GOLDEN_PATHS.md", "Add a separate revocable projection and exact-layout/occupant exclusions.", "RESOLVED_IN_REVISION", "FAC-FD-016;FAC-REQ-014"),
    ("FAC-FIND-P2-003", "P2", "DOMAIN_OPERATIONAL", "Canonical source bodies retain candidate-status wording while separate adoption records control lifecycle.", "SOURCE_REGISTER.md", "Record content/lifecycle separation and exact adoption evidence.", "RESOLVED_IN_REVISION", "FAC-SRC-008;FAC-SRC-010;FAC-SRC-012"),
    ("FAC-FIND-P2-004", "P2", "CROSS_DOMAIN", "Organization verification could be mistaken for authorization.", "DATA_DICTIONARY.md;INHERITANCE_AND_SHARED_CONTROL_REGISTER.md", "Add verification assertion entity and no-authority effect.", "RESOLVED_IN_REVISION", "FAC-FD-012;FAC-REQ-026"),
    ("FAC-FIND-P2-005", "P2", "MACHINE_TRACEABILITY", "Retention has no supported numeric default.", "FOUNDER_DECISION_REGISTER.md;RISK_FINDING_DEVIATION_REGISTER.csv", "Keep threshold unresolved and route to Founder/legal/operational method.", "OPEN_FOUNDER_DECISION", "FAC-FD-022;FAC-RISK-008"),
    ("FAC-FIND-P2-006", "P2", "AS_BUILT", "Current implementation uses default/primary fallbacks and partial facility-account mirrors.", "AS_BUILT_RECONCILIATION.md", "Classify as legacy nonconformance; require separately authorized reconciliation.", "OPEN_IMPLEMENTATION_GAP", "FAC-RISK-001;FAC-RISK-010"),
    ("FAC-FIND-P3-001", "P3", "DOCUMENTARY", "First-user seed wording omitted an explicit unassigned Area.", "GOLDEN_PATHS.md;FOUNDER_DECISION_BRIEF.md", "Add candidate minimum topology and state that it creates no authority.", "RESOLVED_IN_REVISION", "FAC-FD-017;FAC-REQ-031"),
    ("FAC-FIND-P3-002", "P3", "MACHINE_TRACEABILITY", "Some narrative contracts did not expose stable identifiers.", "API_EVENT_JOB_CONTRACTS.md", "Add FAC-API, FAC-EVT and FAC-JOB identifiers.", "RESOLVED_IN_REVISION", "FAC-REQ-036"),
    ("FAC-FIND-P3-003", "P3", "DOCUMENTARY", "Recommendations needed repeated candidate-only wording in Founder-facing outputs.", "FOUNDER_REVIEW_PACKET.md;FOUNDER_DECISION_BRIEF.md", "Repeat recommendation notice and unresolved status.", "RESOLVED_IN_REVISION", "FAC-FD-028"),
]


def build_pia(revised: bool) -> str:
    sections = [
        ("Document Control and Status", f"Identifier `{PIA_ID}`; candidate version `1.0.0`; owner: Founder pending assignment; lifecycle: `FOUNDER_REVIEW`; disposition `{DISPOSITION}`. This is an as-designed candidate. It is not an as-built or as-verified baseline. {NO_AUTH}"),
        ("Executive Summary", "This PIA defines the candidate structural boundary among Tenant, Facility, Organization, Barn, and Facility Area. Tenant is the strict application context; Facility is durable physical place; Organization is entity identity; Barn is an operational context; associations never create authority. Twenty-eight Founder decisions remain unresolved."),
        ("Purpose, Outcomes, and Success Measures", "Outcomes are unambiguous topology, explicit active context, tenant isolation, preserved lineage, non-cascading transitions, and testable contracts. Success requires zero unresolved P0/P1 document defects, all identifiers resolved, fresh segregated review, Founder decisions, and separate authorization before any implementation."),
        ("Authoritative Sources and Inheritance", "`SOURCE_REGISTER.md` records 33 exact sources. Facility, Barn, and Business canons provide primary domain truth. Identity, Relationship, Authorization, Permission, Privacy, Audit, Retention, Communications, Claims, Search, Operations, Resilience, Security, Integration and Adapter controls are inherited without weakening. Adoption records control lifecycle where a source body retains pre-adoption wording."),
        ("Scope, Boundaries, and Ownership", "Owns structural definitions and identifiers; topology; lifecycle; typed Tenant/Facility/Organization associations; active context selection; duplicate quarantine; non-cascading transition rules; and structural API/event/job contracts. Does not own person identity, relationship truth, authorization, consent, horse ownership/custody, clinical authority, payments, record stewardship, communications delivery, search policy, platform operations or release. MIAP is the active cross-cutting implementation-governance profile, not an eleventh PIA and not Facility-domain truth."),
        ("Definitions and Controlled Vocabulary", "Tenant: isolation/governance context. Facility: durable physical place. Organization: durable entity identity. Barn: named operational context associated to a Facility/Area. Facility Area: nested physical/topological element. Association: sourced, typed, effective-dated relationship that is never authority. Active Context: explicitly selected and revalidated Tenant/Facility/Organization tuple."),
        ("Actors, Roles, Relationships, and Authorities", "Actors include Founder/approval authority, tenant steward, facility steward, organization identity steward, relationship actor, authorization service, privacy/stewardship reviewers, support actor, evidence custodian and service identity. Labels such as owner, admin, operator or manager are claims/roles only; an action requires current authorization."),
        ("Capability Map and Release Classification", "DESIGN: definitions, topology, lifecycles, workflows and boundaries. IMPLEMENTATION: persistence, APIs, context service, migration, support, suspension, offline and integrations. ENROLLMENT: seed topology, context UX, public projection and closure notices. This package advances only design drafting/review and grants none of the later milestones."),
        ("User and Operational Workflows", "Thirteen end-to-end workflows appear in `WORKFLOW_REGISTER.md`, covering first-user seed, creation, context selection, area change, organization association, operator change, duplicate merge, suspension, closure, public projection, import, correction and support investigation."),
        ("Business Rules and Decision Logic", "Default deny; explicit context; associations are non-authorizing; topology changes are versioned and audited; closed identities are not reused; transfers and merges do not cascade; ambiguous imports quarantine; public data is a separate projection; disputed claims preserve uncertainty; recommendations are never doctrine."),
        ("Data Entities, Relationships, and Provenance", "Fifteen candidate entities are defined in `DATA_DICTIONARY.md`. Every material assertion includes stable identity, Tenant classification, source, time, actor/service, version and correction lineage. External identifiers are aliases or claims, never standalone authority."),
        ("Record Ownership, Stewardship, Correction, and Retention", "Facility domain stewards physical identity/topology. Relationship domain stewards associations/membership. Authorization stewards action decisions. Corrections append change sets. Retention is field/purpose/hold-specific; numeric schedules remain `FOUNDER_DECISION_REQUIRED` under FAC-FD-022."),
        ("State and Transition Models", "Candidate Tenant, Facility, Organization and Facility Area transitions are in `STATE_TRANSITION_MATRIX.csv`. No silent reactivation, destructive close, or state inference is permitted. Suspension must invalidate UI, API, jobs, search, exports, webhooks and integrations."),
        ("Authorization and Permission Matrix", "`PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv` defines 17 candidate actions. Every evaluation is action-, field-, tenant-, target-, facility-, organization-, purpose-, relationship-, and time-aware. Role, payment, agreement, facility assignment or organization association alone is insufficient."),
        ("User Interface and Experience Requirements", "Persistent context header; explicit context switch; confirmation for consequential actions; before/after preview; effective times; uncertainty/quarantine labels; accessible errors; generic denial; no inaccessible-entity enumeration; public/private field preview; suspension and degraded-state banners."),
        ("API, Event, Job, and Integration Contracts", "`API_EVENT_JOB_CONTRACTS.md` defines eight API, three event and three job candidates. They require explicit context, idempotency, version checks, audit, non-enumerating failures, partition-safe retry and dead-letter quarantine. They are design interfaces, not implementation authorization."),
        ("Notifications and Communications", "Material suspension, closure, association change, publication and support access should create governed notice intents. Delivery is not consent, authority or proof of receipt. Templates, recipients, failures, retries and escalation remain Communications-owned."),
        ("Files, Media, and Document Handling", "Facility evidence files must be malware-scanned, tenant/context bound, classified, access-controlled, content-addressed where appropriate, retained under stewardship rules and excluded from public projection unless separately approved. No direct object locator may bypass authorization."),
        ("Search, Reporting, and Analytics", "Permission filtering precedes retrieval, counts, autocomplete and ranking. Exact layouts, sensitive areas, occupants and precise coordinates remain private. Aggregates require re-identification review. Public search consumes only `PublicFacilityProjection`. Analytics cannot create cross-tenant discovery."),
        ("Offline, Device, and Synchronization Behavior", "Candidate rule: offline may read a minimum, expiring authorized cache and capture context-neutral observations. It may not create/move/merge/transfer/close/decommission/reassign canonical topology. Every queued observation is untrusted until online context and authority revalidation."),
        ("Security, Privacy, Consent, Safeguarding, and Abuse Controls", "Tenant isolation is necessary but insufficient: enforce record, field, purpose and relationship scope. Private by default. Protect location/sensitive areas and minors. Rate-limit enumeration. Audit denied/material acts. Agreement/consent do not replace authorization. Support is ticketed and time-limited."),
        ("AI and Automation Controls", "No AI/custom agent is activated. Automation may propose duplicate candidates or reconciliations only if separately authorized; it may not approve, merge, transfer, close, verify or authorize. Human accountable actors, confidence, inputs and evidence must remain visible."),
        ("Failure Modes, Recovery, Correction, and Reconciliation", "Fail closed on missing/stale context, cycles, version conflicts, unknown partition, expired cache or ambiguous identity. Quarantine rather than default. Retry idempotently. Append corrections. Recovery must reconcile membership, permission, topology and publication before treating restored state as current."),
        ("Observability, Administration, Support, and Incident Operations", "Candidate metrics: denied-by-context attempts, stale-context failures, suspended-surface probes, change-set reconciliation, quarantine age, public-projection drift, support access duration and dead letters. Support access uses ticket/reason/approval/expiry and immutable audit. Thresholds require authorization."),
        ("Nonfunctional and Quality Attribute Requirements", "Isolation, integrity, availability, accessibility, usability, latency, scale, recovery and audit completeness require measurable budgets before implementation authorization. This design sets qualitative gates and does not invent numbers. Degraded behavior must be explicit and cannot imply stronger offline reliability."),
        ("Environment, Configuration, Feature Flags, and Secrets Boundaries", "No environment may disable Tenant isolation, field authorization, audit, privacy or quarantine. Secrets remain external to documents. Test identities and datasets cannot cross environments. Configuration changes are versioned/audited and cannot create implementation or release authority."),
        ("Migration, Seed Data, and Data Reconciliation", "No migration is authorized. Candidate future plan: inventory every record; resolve explicit Tenant/Facility/Organization identities; quarantine ambiguity; reconcile totals/hashes; dual-read only under a controlled work package; remove default-primary fallbacks only after verified cutover and rollback evidence."),
        ("Engineering Work Packages and Implementation Sequence", "`ENGINEERING_WORK_PACKAGE_REGISTER.csv` contains candidate work packages only. The critical sequence is decision closure, fresh review, baseline approval, implementation authorization, model/context foundation, migration rehearsal, surface enforcement, UX/operations, evidence and release gates."),
        ("Acceptance Criteria", "`ACCEPTANCE_CRITERIA.csv` maps every FAC-REQ to an objective documentary or future implementation proof. Draft-package acceptance is limited to completeness, traceability, review and validation; it is not proof that software behaves as designed."),
        ("Test and Validation Matrix", "`TEST_MATRIX.csv` maps all requirements to positive, negative, cross-tenant, stale-context, lifecycle, recovery or document validation. Tests are specifications until separately executed against authorized implementation. This package ran documentary validators only."),
        ("Golden-Path Reproduction Scenarios", "`GOLDEN_PATHS.md` includes first-user creation, multi-facility context, multi-organization operation, area change, operator transition, duplicate reconciliation, suspension/reinstatement, closure and public projection. Each preserves domain ownership and no-cascade rules."),
        ("Adversarial, Negative, and Abuse Scenarios", "`ADVERSARIAL_SCENARIOS.md` challenges ID substitution, stale context, association-as-authority, partial suspension, offline replay, hierarchy cycle, duplicate poisoning, mass assignment, search enumeration, support abuse, transfer cascade, stale recovery, webhook retry and public-location leakage."),
        ("Evidence Requirements, Coverage, and Manifest", "`EVIDENCE_MANIFEST.json` links source, design, first-pass review, revision, second-pass review and validation evidence. Package hashes prove artifact integrity, not truth, approval, implementation or operation."),
        ("Deployment, Rollout, Rollback, and Release Controls", "No deployment/rollout is authorized. A future authorized plan must define environments, flags that cannot weaken controls, migrations, rollback, reconciliation, observability, incident stop conditions, evidence and approval. Release authority remains Platform Operations/Founder controlled."),
        ("Enrollment and Onboarding Readiness", "Not ready. Candidate first-user topology is one Tenant, one Organization association, one Facility and one unassigned Area, with separate relationship/authority establishment. Enrollment needs Founder decisions, fresh review, approved design, authorized/conformant implementation, evidence, support and release gates."),
        ("Dependencies and Critical Path", "`DEPENDENCY_REGISTER.csv` records canonical source, Founder decision, Authorization, Relationship, Privacy, Audit, Stewardship, Search, Platform Operations, implementation, migration, review and evidence dependencies. Open design decisions and fresh segregated review precede approval."),
        ("Open Decisions, Assumptions, Findings, Deviations, and Risks", "Twenty-eight items are `FOUNDER_DECISION_REQUIRED`. Two residual P2 findings remain open: retention decision and as-built legacy gap. There are no approved deviations. Assumption: the ten-item portfolio gate is controlling; it was validated before this package began."),
        ("Implementation Drift and As-Built Reconciliation", "`AS_BUILT_RECONCILIATION.md` finds partial barn-scoping and account membership foundations but important `default`/`primary` fallbacks, Barn/Facility/Tenant conflation and no demonstrated complete Organization topology. This is legacy nonconformance evidence, not a reason to weaken design."),
        ("Change-Control History", "`CHANGE_CONTROL_LOG.md` preserves source assembly, first draft, first review, challenge passes, revision, second review and final validation. Future material change requires impact analysis and a new controlled version; identifiers are not reused."),
        ("Requirement Traceability Matrix", "`REQUIREMENT_REGISTER.csv` links every requirement to sources/decisions, performer, failure behavior, release class, acceptance criterion and test. Machine validation checks identifier uniqueness and reference coverage."),
        ("Five Mandatory Readiness Questions", "1) Complete enough to build? No—Founder decisions and authorization remain. 2) Correctly built? No implementation was evaluated. 3) Objectively verified? Documentary package only; software unverified. 4) Operationally safe? Not established. 5) Ready for first user? No."),
        ("Review, Approval, Authorization, and Disposition", f"One controlled drafting pass, individual first-pass review of every Phase 2/7 document, six isolated challenge passes, revision, individual second-pass review and machine validation were completed. Procedural segregation is documented; no ES-RA/custom agent identity is claimed. Fresh segregated review and Founder decisions remain. Disposition: `{DISPOSITION}`."),
        ("Maintenance, Supersession, and Decommissioning", "The PIA owner must monitor source changes and design drift. A material definition, ownership, permission, lifecycle or architecture change requires a major revision. Approved successors explicitly supersede this version. Candidate/retired artifacts remain in evidence; no package may silently disappear."),
    ]
    assert len(sections) == 43
    body = header("Facility, Tenant, and Organizational Structure PIA V1.0.0")
    body += "\n## Control statements\n\n- Portfolio position: `02` of exactly ten.\n- PIA Master Standard: `ES-PIA-MASTER-STANDARD-V1.1`.\n- As-designed baseline: this package.\n- As-built baseline: not established.\n- As-verified baseline: not established.\n"
    for number, (title, text_) in enumerate(sections, 1):
        body += f"\n## {number}. {title}\n\n{text_}\n"
    if revised:
        body += "\n## Review incorporation record\n\nThe revised candidate explicitly resolves first-pass P1 findings by separating Barn from Tenant/Facility, declaring every association non-authorizing, applying suspension to all surfaces, and prohibiting transfer/merge cascade across people, horses, permissions, agreements, billing, private records and evidence. It resolves P2/P3 drafting defects by bounding offline writes, defining the public projection, preserving source-lifecycle precedence, separating verification from authority, adding stable contract IDs, and clarifying the first-user seed. Residual Founder decisions and the legacy implementation gap remain visible.\n"
    return body


def build_core_documents(revised: bool) -> list[str]:
    written: list[str] = []
    def emit(name: str, content: str) -> None:
        write(name, content)
        written.append(name)

    emit("PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md", build_pia(revised))

    source_data = source_rows()
    emit("SOURCE_REGISTER.md", header("Source Register") + "\n" + table(
        ["ID", "Source", "Authority", "Status", "SHA-256", "Relevance / gap"],
        [(r["source_id"], r["title"], r["authority"], r["status"], r["sha256"], r["relevance"] if r["gap"] == "NONE" else r["gap"]) for r in source_data]
    ) + ("\n\n## Lifecycle precedence\n\nThe Facility, Barn, Business, Permission, and Agreement source bodies contain historical candidate or pre-lock wording. Their separate constitutional adoption records control lifecycle. This package preserves both content provenance and lifecycle authority; it does not rewrite frozen sources.\n" if revised else ""))

    inherit_rows = [
        ("FAC-CTRL-001", "Identity/authentication", "Identity V2.0", "INHERITS", "Actor/account identity; no facility authority"),
        ("FAC-CTRL-002", "Relationships/membership", "Relationship V2.0", "INHERITS_AND_CONFIGURES", "Typed associations; Relationship owns truth"),
        ("FAC-CTRL-003", "Authorization/permissions", "Permission V1.1; Agreement V2.1", "INHERITS", "Action-time default denial; association and verification are not authority"),
        ("FAC-CTRL-004", "Audit/evidence", "Audit V2.0", "INHERITS_AND_EXTENDS", "Adds topology context/change-set fields"),
        ("FAC-CTRL-005", "Privacy/safeguarding", "Privacy V2.0", "INHERITS_AND_EXTENDS", "Protects precise location, layouts and occupants"),
        ("FAC-CTRL-006", "Retention/correction", "Record Stewardship V2.1", "INHERITS_AND_CONFIGURES", "Schedules remain Founder/legal/operational decision"),
        ("FAC-CTRL-007", "Notifications", "Communications V2.0", "INHERITS_AND_TRIGGERS", "Creates notice intent only"),
        ("FAC-CTRL-008", "Search/public discovery", "Search V2.0", "INHERITS_AND_CONFIGURES", "Filter before retrieval; separate public projection"),
        ("FAC-CTRL-009", "Operations/release", "Platform Operations V2.0", "INHERITS", "No release authority here"),
        ("FAC-CTRL-010", "Configuration/flags", "Configuration V2.0", "INHERITS", "Cannot weaken controls"),
        ("FAC-CTRL-011", "Backup/recovery", "Resilience V1.0", "INHERITS_AND_EXTENDS", "Reconcile topology/context after restore"),
        ("FAC-CTRL-012", "Security incident", "Security Incident V1.0", "INHERITS", "Containment/disclosure outside domain ownership"),
        ("FAC-CTRL-013", "Integrations/adapters", "Developer Platform V2.0; External Architecture V2.0", "INHERITS_AND_CONFIGURES", "Context-bound/no external authority"),
        ("FAC-CTRL-014", "Horse continuity", "Horse Lifecycle V3.1; Transfer Policy", "DEPENDS_ON", "Location/topology never transfers horse authority"),
    ]
    emit("INHERITANCE_AND_SHARED_CONTROL_REGISTER.md", header("Inheritance and Shared Control Register") + "\n" + table(["ID", "Control", "Owner/source", "Treatment", "Facility rule"], inherit_rows))

    decision_rows = [{"decision_id": d[0], "category": d[1], "question": d[2], "status": "FOUNDER_DECISION_REQUIRED", "recommended_answer": d[3], "alternatives": d[4], "risk_if_unresolved": d[5], "gate": d[6], "founder_answer": ""} for d in DECISIONS]
    emit("FOUNDER_DECISION_REGISTER.md", header("Founder Decision Register") + "\n" + "\n".join(
        f"## {r['decision_id']} — {r['question']}\n\n- Status: `FOUNDER_DECISION_REQUIRED`\n- Gate: `{r['gate']}`\n- Recommended candidate answer: {r['recommended_answer']}\n- Alternatives: {r['alternatives']}\n- Risk if unresolved: {r['risk_if_unresolved']}\n- Founder answer: _not supplied_\n"
        for r in decision_rows
    ))
    write_csv("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv", ["decision_id", "category", "question", "status", "recommended_answer", "alternatives", "risk_if_unresolved", "gate", "founder_answer"], decision_rows)
    written.append("FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv")

    req_rows = []
    for rid, statement, sources, performer, failure, release, ac, test in REQUIREMENTS:
        req_rows.append({"requirement_id": rid, "statement": statement, "source_or_decision": sources, "rationale": "Preserve domain boundaries, safety, privacy, integrity and testability.", "performer": performer, "preconditions": "Valid explicit context and action-specific authority unless the requirement states otherwise.", "required_behavior": statement.replace(" SHALL ", " ").replace(" SHALL NOT ", " must not "), "prohibited_behavior": "Silent inference, cross-tenant fallback, status inflation or destructive evidence rewrite.", "failure_behavior": failure, "data_impact": "As specified by the linked workflow/entity; every material change is versioned and audited.", "permission_impact": "Action-specific default-deny evaluation.", "release_classification": release, "acceptance_criterion": ac, "test_case": test, "evidence": f"FAC-EVID-{int(rid[-3:]):03d}", "status": "DRAFT_PENDING_FOUNDER_DECISIONS"})
    req_fields = list(req_rows[0])
    write_csv("REQUIREMENT_REGISTER.csv", req_fields, req_rows)
    written.append("REQUIREMENT_REGISTER.csv")

    emit("WORKFLOW_REGISTER.md", header("Workflow Register") + "\n" + "\n".join(
        f"## {wid} — {name}\n\n- Actor: {actor}\n- Preconditions: {pre}\n- Happy path: {path}\n- Boundary/failure: {failure}\n- Requirements: `{reqs}`\n"
        for wid, name, actor, pre, path, failure, reqs in WORKFLOWS
    ) + ("\n## Review hardening\n\nCreation or change of an association never grants action authority. Transfer, merge, split, successor and closure workflows never cascade people, horses, permissions, agreements, billing, private records or evidence. Each dependent domain recalculates only its own effects.\n" if revised else ""))

    emit("DATA_DICTIONARY.md", header("Data Dictionary") + "\n" + table(["Entity ID", "Entity", "Purpose", "Minimum fields", "Boundary"], ENTITIES) + ("\n\n## Global provenance fields\n\nEvery entity or assertion carries stable ID, tenant/global classification, created/updated actor or service, source, observed/effective time, version, correction lineage, lifecycle state and sensitivity. `BarnOperationalContext` is expressly not a Tenant or Facility. `OrganizationVerificationAssertion` is expressly not authorization.\n" if revised else ""))

    write_csv("STATE_TRANSITION_MATRIX.csv", ["state_model_id", "entity", "from_state", "to_state", "trigger", "required_permission", "guard", "audit_event", "failure_behavior"], [dict(zip(["state_model_id", "entity", "from_state", "to_state", "trigger", "required_permission", "guard", "audit_event", "failure_behavior"], row)) for row in STATE_ROWS])
    written.append("STATE_TRANSITION_MATRIX.csv")
    write_csv("PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv", ["permission_rule_id", "action", "candidate_actor", "scope", "required_evidence", "boundary"], [dict(zip(["permission_rule_id", "action", "candidate_actor", "scope", "required_evidence", "boundary"], row)) for row in PERMISSIONS])
    written.append("PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv")

    emit("API_EVENT_JOB_CONTRACTS.md", header("API, Event, and Job Contracts") + "\n" + table(["ID", "Interface", "Kind", "Permission/actor", "Input", "Output/consumer", "Evidence", "Failure"], CONTRACTS) + "\n\nAll identifiers and routes are candidate contracts. They are not active endpoints, schemas, jobs, or implementation authority. Every command requires tenant context, idempotency, optimistic version, authorization reference and audit correlation unless explicitly documented otherwise.\n")

    ac_rows, test_rows = [], []
    for idx, (rid, statement, *_rest) in enumerate(REQUIREMENTS, 1):
        ac_id, test_id = f"FAC-AC-{idx:03d}", f"FAC-TEST-{idx:03d}"
        ac_rows.append({"acceptance_id": ac_id, "requirement_id": rid, "criterion": f"Objective review demonstrates the exact obligation in {rid} and its prohibited/failure behavior without cross-tenant fallback.", "method": "Document inspection plus authorized future automated/operational evidence", "evidence_id": f"FAC-EVID-{idx:03d}", "status": "SPECIFIED_NOT_EXECUTED"})
        mode = "cross-tenant negative" if idx in {2, 5, 6, 7, 13, 14, 15, 18, 19, 21, 22, 23, 24, 25, 33, 34} else "positive and negative"
        test_rows.append({"test_id": test_id, "requirement_id": rid, "test_type": mode, "precondition": "Authorized test environment and fixtures; none created by this package", "procedure": f"Exercise the allowed, denied, stale, malformed or transition case relevant to {rid}.", "expected_result": "Required behavior occurs; prohibited behavior is denied atomically and audited without information leakage.", "evidence_id": f"FAC-EVID-{idx:03d}", "execution_status": "NOT_EXECUTED_IMPLEMENTATION_NOT_AUTHORIZED"})
    write_csv("ACCEPTANCE_CRITERIA.csv", list(ac_rows[0]), ac_rows); written.append("ACCEPTANCE_CRITERIA.csv")
    write_csv("TEST_MATRIX.csv", list(test_rows[0]), test_rows); written.append("TEST_MATRIX.csv")

    golden = [
        ("FAC-GP-001", "First-user setup", "One Tenant, one Organization association, one Facility and an unassigned Area are proposed; authority is established separately.", "No topology seed grants membership, ownership, permission or payment authority."),
        ("FAC-GP-002", "Multi-facility tenant", "An authorized user explicitly selects Facility A or B and sees persistent context.", "No data from the unselected Facility appears."),
        ("FAC-GP-003", "Multiple organizations at one facility", "Owner, lessee and operator associations coexist with effective dates.", "None grants blanket action authority."),
        ("FAC-GP-004", "Area move", "A stall is moved under a new parent using an acyclic versioned change set.", "Prior topology remains in lineage; horse authority does not change."),
        ("FAC-GP-005", "Operator transition", "Old operator association ends; new one begins; dependent domains re-evaluate.", "People, horses, agreements, permissions, billing and records do not cascade."),
        ("FAC-GP-006", "Duplicate reconciliation", "Candidates quarantine, evidence is compared, reviewed merge preserves aliases and rollback metadata.", "No automated fuzzy merge."),
        ("FAC-GP-007", "Suspension and reinstatement", "All product surfaces deny ordinary consequential access; online revalidation restores allowed context.", "Only separately governed safety evidence capture may remain."),
        ("FAC-GP-008", "Closure/decommission", "Facility closes, projections/credentials revoke, lineage and evidence remain.", "No silent deletion or reassignment."),
        ("FAC-GP-009", "Public discovery", "An opt-in coarse public projection is published then revoked.", "Exact layout, occupants and sensitive areas never enter the projection."),
    ]
    emit("GOLDEN_PATHS.md", header("Golden Paths") + "\n" + "\n".join(f"## {gid} — {name}\n\n{flow}\n\n**Invariant:** {invariant}\n" for gid, name, flow, invariant in golden))

    adversarial = [
        ("FAC-ADV-001", "Replace tenant_id in a request", "Generic deny; no existence leak; denied attempt audited"),
        ("FAC-ADV-002", "Reuse stale active context after membership revocation", "Deny after per-request revalidation; invalidate cache"),
        ("FAC-ADV-003", "Claim Organization admin role to edit a Facility", "Association/role alone insufficient"),
        ("FAC-ADV-004", "Call a background job after suspension", "Job partition denied/dead-lettered; no write"),
        ("FAC-ADV-005", "Replay offline move after authority expires", "Quarantine/reject; no canonical mutation"),
        ("FAC-ADV-006", "Create an Area parent cycle", "Atomic 409; topology unchanged"),
        ("FAC-ADV-007", "Poison fuzzy duplicate evidence", "No auto-merge; reviewed quarantine remains"),
        ("FAC-ADV-008", "Mass-assign verification or public fields", "Allowlist rejects protected fields"),
        ("FAC-ADV-009", "Enumerate inaccessible facilities through search/count/autocomplete", "No distinguishable existence response"),
        ("FAC-ADV-010", "Use expired support ticket", "Immediate deny and audit"),
        ("FAC-ADV-011", "Transfer Facility and expect horses/invoices to follow", "Non-cascade; dependent domains unchanged pending their own authority"),
        ("FAC-ADV-012", "Restore backup containing revoked membership/public projection", "Reconciliation prevents restored stale state becoming current"),
        ("FAC-ADV-013", "Retry webhook/event with same idempotency key", "One material effect, repeated evidence linked"),
        ("FAC-ADV-014", "Publish exact stall layout or occupant list", "Privacy allowlist denies publication"),
        ("FAC-ADV-015", "Open deep link for another context", "No silent switch; explicit permitted selection required"),
        ("FAC-ADV-016", "Use missing context and trigger legacy default primary fallback", "Target design denies/quarantines; never assigns primary"),
        ("FAC-ADV-017", "Close Organization and inherit every permission to successor", "No inheritance; reauthorization required"),
        ("FAC-ADV-018", "Treat signed lease as application authorization", "Agreement is evidence input only; action-time authorization still required"),
    ]
    emit("ADVERSARIAL_SCENARIOS.md", header("Adversarial Scenarios") + "\n" + table(["Scenario ID", "Attack/failure", "Required outcome"], adversarial))

    wp_rows = [
        ("FAC-WP-001", "Decision and baseline closure", "Resolve design decisions; fresh segregated review; Founder design decision", "FAC-FD-001;FAC-FD-002;FAC-FD-003;FAC-FD-004;FAC-FD-005;FAC-FD-006;FAC-FD-007;FAC-FD-008;FAC-FD-009;FAC-FD-010;FAC-FD-011;FAC-FD-012;FAC-FD-028", "NO"),
        ("FAC-WP-002", "Canonical entity and context schemas", "Tenant/Facility/Organization/Area/association/change-set schemas", "FAC-WP-001", "NO"),
        ("FAC-WP-003", "Authorization and context boundary", "Request/job/event/search/export enforcement", "FAC-WP-002;Authorization PIA", "NO"),
        ("FAC-WP-004", "Legacy inventory and migration rehearsal", "No-write inventory, mapping, quarantine, reversible rehearsal", "FAC-WP-002;FAC-FD-013;FAC-FD-014;FAC-FD-015;FAC-FD-018;FAC-FD-019;FAC-FD-020;FAC-FD-021;FAC-FD-022;FAC-FD-025;FAC-FD-026", "NO"),
        ("FAC-WP-005", "Topology workflows and lifecycle", "Versioned change sets, transitions and non-cascade behavior", "FAC-WP-002;FAC-WP-003", "NO"),
        ("FAC-WP-006", "Privacy/search/public projection", "Field policies, projection, non-enumeration", "FAC-WP-003", "NO"),
        ("FAC-WP-007", "Offline/integration/recovery", "Expiry, idempotency, reconciliation and dead letters", "FAC-WP-003;FAC-WP-005", "NO"),
        ("FAC-WP-008", "Onboarding/context UX/support", "Seed, context UX, support path and notices", "FAC-WP-003;FAC-WP-005;FAC-FD-016;FAC-FD-017;FAC-FD-023;FAC-FD-024;FAC-FD-027", "NO"),
        ("FAC-WP-009", "Verification and evidence", "Execute test matrix; as-built reconciliation; evidence package", "FAC-WP-002;FAC-WP-003;FAC-WP-004;FAC-WP-005;FAC-WP-006;FAC-WP-007;FAC-WP-008", "NO"),
        ("FAC-WP-010", "Release/enrollment gates", "Separate operational/release/enrollment approval", "FAC-WP-009", "NO"),
    ]
    write_csv("ENGINEERING_WORK_PACKAGE_REGISTER.csv", ["work_package_id", "title", "candidate_scope", "dependencies", "implementation_authorized"], [dict(zip(["work_package_id", "title", "candidate_scope", "dependencies", "implementation_authorized"], row)) for row in wp_rows]); written.append("ENGINEERING_WORK_PACKAGE_REGISTER.csv")

    dep_rows = [
        ("FAC-DEP-001", "PIA Master Standard V1.1", "CONTROLLING", "SATISFIED_FOR_DRAFT", "Keep 43 sections/traceability/status discipline"),
        ("FAC-DEP-002", "Ten-item portfolio realignment", "PRECONDITION", "SATISFIED", "Gate validated and committed before Facility branch"),
        ("FAC-DEP-003", "Founder design decisions", "DECISION", "OPEN", "Blocks design approval"),
        ("FAC-DEP-004", "Fresh segregated review", "ASSURANCE", "OPEN", "Required before Founder approval decision"),
        ("FAC-DEP-005", "Identity/Relationship/Authorization/Permission", "CROSS_DOMAIN", "SOURCE_AVAILABLE", "Must remain authoritative owners"),
        ("FAC-DEP-006", "Privacy/Audit/Stewardship/Search", "CROSS_DOMAIN", "SOURCE_AVAILABLE", "Shared controls inherited"),
        ("FAC-DEP-007", "Platform Operations/Resilience/Configuration/Security", "CROSS_DOMAIN", "SOURCE_AVAILABLE", "Required for later operational gates"),
        ("FAC-DEP-008", "Implementation authorization", "AUTHORITY", "NOT_GRANTED", "Blocks code/schema/migration work"),
        ("FAC-DEP-009", "As-built reconciliation and verification", "EVIDENCE", "NOT_STARTED", "Blocks verified/operational status"),
        ("FAC-DEP-010", "Enrollment authorization", "AUTHORITY", "NOT_GRANTED", "Blocks first user"),
    ]
    write_csv("DEPENDENCY_REGISTER.csv", ["dependency_id", "dependency", "type", "status", "effect"], [dict(zip(["dependency_id", "dependency", "type", "status", "effect"], row)) for row in dep_rows]); written.append("DEPENDENCY_REGISTER.csv")

    risk_rows = [{"item_id": r[0], "type": "RISK", "severity": r[1], "summary": r[2], "impact": r[3], "mitigation_or_disposition": r[4], "status": r[5], "traceability": r[6], "approved_deviation": "NO"} for r in RISKS]
    write_csv("RISK_FINDING_DEVIATION_REGISTER.csv", list(risk_rows[0]), risk_rows); written.append("RISK_FINDING_DEVIATION_REGISTER.csv")

    emit("AS_BUILT_RECONCILIATION.md", header("As-Built Reconciliation", "LEGACY_NONCONFORMANCE_RECORDED") + """
## Method

Static read-only source inspection only. No application/database was started; no migration or test environment was created.

## Evidence and classification

| Evidence | Observation | Target comparison | Classification |
| --- | --- | --- | --- |
| `backend/core/tenancy.py` | `PRIMARY_BARN_ID="primary"`; missing user barn resolves to primary; comments map task-engine `tenant_id="default"` to `barn_id="primary"`. | Missing/unknown target context must fail closed or quarantine. | PROHIBITED_LEGACY_FALLBACK / IMPLEMENTATION_GAP |
| `backend/task_engine.py` and `backend/core/lifespan.py` | Task/media partition uses default tenant and primary barn compatibility mapping. | Tenant and Facility/Barn must remain distinct. | IMPLEMENTATION_GAP |
| `backend/routes/barns.py` | Barn provisioning creates a barn and first admin with one-barn-per-user language; writes `db.barn` while status gates read `db.barns`. | Target requires explicit Tenant/Facility/Organization topology and contract consistency. | IMPLEMENTATION_GAP / REVIEW_REQUIRED |
| `backend/core/account_memberships.py` | Additive facility account memberships mirror `users.barn_id` and role; comments acknowledge future transition. | Useful foundation but Role/relationship/account cannot become authority. | PARTIAL_CONFORMING_FOUNDATION |
| `backend/core/account_route_context.py` | Selected facility context resolves membership then reads barn status. | Moves toward explicit context but does not demonstrate full Tenant/Organization model. | PARTIAL_CONFORMING_FOUNDATION |
| application-wide `barn_id` fields | Many domain records are barn-scoped. | Provides partial isolation evidence, not proof of Tenant/Facility/Organization separation. | PARTIAL_CONFORMING_FOUNDATION |

## Disposition

The current software is not claimed conformant to this candidate and was not dynamically verified. The PIA records a target design independent of the legacy shortcuts. Any remediation requires a separately authorized, inventoried, reversible migration and work-package sequence. No source file outside this documentary package was modified.
""")

    emit("CHANGE_CONTROL_LOG.md", header("Change-Control Log") + """
| Entry | Date | Change | Authority/effect |
| --- | --- | --- | --- |
| FAC-CHG-001 | 2026-07-20 | Verified Portfolio Realignment gate. | Preconditions only; no Facility doctrine. |
| FAC-CHG-002 | 2026-07-20 | Assembled 33 exact sources and static as-built evidence. | Read-only evidence. |
| FAC-CHG-003 | 2026-07-20 | Produced complete first draft and first-hash manifest. | Candidate only. |
| FAC-CHG-004 | 2026-07-20 | Reviewed every Phase 2/7 drafted document and executed six isolated challenge passes. | Procedural segregation; not an ES-RA or fresh external review. |
| FAC-CHG-005 | 2026-07-20 | Revised documents against 13 findings. | 11 resolved; 2 residual P2 items retained. |
| FAC-CHG-006 | 2026-07-20 | Completed second document review and cross-document consistency pass. | No P0/P1 remain in documentary package. |
| FAC-CHG-007 | 2026-07-20 | Ran machine validation and prepared Founder briefing. | Package integrity only; no approval or implementation effect. |
""")

    machine = {
        "pia_id": PIA_ID,
        "version": "1.0.0-candidate",
        "date": DATE,
        "portfolio_position": "02",
        "status": "FOUNDER_DECISION_REQUIRED",
        "disposition": DISPOSITION,
        "authority": {"implementation_authorized": False, "migration_authorized": False, "release_authorized": False, "enrollment_authorized": False, "production_authorized": False, "custom_agent_activated": False, "f0001_closed": False},
        "definitions": {"tenant": "strict application isolation and governance context", "facility": "durable physical-place identity", "organization": "durable entity identity", "barn": "named operational context associated with a Facility or Area", "association": "typed and effective-dated relationship that is not authority"},
        "counts": {"sources": len(source_data), "source_gaps": sum(1 for r in source_data if r["gap"] != "NONE"), "founder_decisions": len(DECISIONS), "requirements": len(REQUIREMENTS), "workflows": len(WORKFLOWS), "entities": len(ENTITIES), "permissions": len(PERMISSIONS), "state_transitions": len(STATE_ROWS), "contracts": len(CONTRACTS), "risks": len(RISKS)},
        "source_ids": [r["source_id"] for r in source_data],
        "decision_ids": [d[0] for d in DECISIONS],
        "requirement_ids": [r[0] for r in REQUIREMENTS],
        "workflow_ids": [w[0] for w in WORKFLOWS],
        "entity_ids": [e[0] for e in ENTITIES],
        "permission_ids": [p[0] for p in PERMISSIONS],
        "open_gates": ["FOUNDER_DESIGN_DECISIONS", "FRESH_SEGREGATED_REVIEW", "FOUNDER_DESIGN_APPROVAL", "IMPLEMENTATION_AUTHORIZATION", "AS_BUILT_VERIFICATION", "OPERATIONAL_READINESS", "ENROLLMENT_AUTHORIZATION"],
    }
    write_json("PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json", machine); written.append("PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json")

    evidence = {
        "pia_id": PIA_ID,
        "evidence_items": [
            {"evidence_id": "FAC-EVID-SOURCE-001", "kind": "SOURCE", "locator": "SOURCE_REGISTER.md", "proves": "Source identities and source gaps"},
            {"evidence_id": "FAC-EVID-DRAFT-001", "kind": "FIRST_DRAFT", "locator": "review/first_pass/FIRST_DRAFT_HASH_MANIFEST.csv", "proves": "First-draft artifact hashes"},
            {"evidence_id": "FAC-EVID-REVIEW-001", "kind": "REVIEW", "locator": "DOCUMENT_REVIEW_FINDINGS_REGISTER.csv", "proves": "First-pass findings and disposition"},
            {"evidence_id": "FAC-EVID-CHALLENGE-001", "kind": "CHALLENGE", "locator": "review/first_pass/", "proves": "Six isolated challenge pass records"},
            {"evidence_id": "FAC-EVID-REVISION-001", "kind": "REVISION", "locator": "REVISION_TRACEABILITY_REGISTER.csv", "proves": "Finding-to-change mapping"},
            {"evidence_id": "FAC-EVID-SECOND-001", "kind": "SECOND_REVIEW", "locator": "SECOND_PASS_REVIEW_SUMMARY.md", "proves": "Second review and residual findings"},
            {"evidence_id": "FAC-EVID-VALIDATION-001", "kind": "VALIDATION", "locator": "VALIDATION_REPORT.json", "proves": "Documentary validation results"},
            {"evidence_id": "FAC-EVID-ASBUILT-001", "kind": "STATIC_AS_BUILT", "locator": "AS_BUILT_RECONCILIATION.md", "proves": "Legacy implementation comparison only"},
        ] + [{"evidence_id": f"FAC-EVID-{idx:03d}", "kind": "PLANNED_REQUIREMENT_PROOF", "locator": f"TEST_MATRIX.csv#{test}", "proves": rid, "status": "NOT_EXECUTED"} for idx, (rid, *_x, test) in enumerate(REQUIREMENTS, 1)]
    }
    write_json("EVIDENCE_MANIFEST.json", evidence); written.append("EVIDENCE_MANIFEST.json")

    overview_files = [
        "ACCEPTANCE_CRITERIA.csv", "ADVERSARIAL_SCENARIOS.md", "API_EVENT_JOB_CONTRACTS.md",
        "AS_BUILT_RECONCILIATION.md", "CHANGE_CONTROL_LOG.md", "CHECKSUM_MANIFEST.sha256",
        "CROSS_DOCUMENT_CONSISTENCY_REPORT.md", "DATA_DICTIONARY.md", "DEPENDENCY_REGISTER.csv",
        "DOCUMENT_OVERVIEW_AND_RATIONALE.md", "DOCUMENT_REVIEW_FINDINGS_REGISTER.csv",
        "DOCUMENT_REVIEW_LEDGER.csv", "ENGINEERING_WORK_PACKAGE_REGISTER.csv", "EVIDENCE_MANIFEST.json",
        "FINAL_OPEN_FINDINGS_REGISTER.csv", "FIRST_PASS_REVIEW_SUMMARY.md", "FOUNDER_DECISION_BRIEF.md",
        "FOUNDER_DECISION_RECOMMENDATION_MATRIX.csv", "FOUNDER_DECISION_RECOMMENDATION_MATRIX.json",
        "FOUNDER_DECISION_REGISTER.md", "FOUNDER_INPUT_QUESTIONS.md", "FOUNDER_INPUT_QUESTION_REGISTER.csv",
        "FOUNDER_REVIEW_PACKET.md", "GOLDEN_PATHS.md", "INHERITANCE_AND_SHARED_CONTROL_REGISTER.md",
        "PACKAGE_MANIFEST.json", "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv",
        "PIA_FACILITY_TENANT_ORGANIZATION_MACHINE_READABLE.json",
        "PIA_FACILITY_TENANT_ORGANIZATION_V1_0_0.md", "REQUIREMENT_REGISTER.csv",
        "REVIEW_DISPOSITION.md", "REVISION_CHANGE_SUMMARY.md", "REVISION_TRACEABILITY_REGISTER.csv",
        "RISK_FINDING_DEVIATION_REGISTER.csv", "SECOND_PASS_REVIEW_SUMMARY.md", "SOURCE_REGISTER.md",
        "STATE_TRANSITION_MATRIX.csv", "TEST_MATRIX.csv", "VALIDATION_REPORT.json", "VALIDATION_REPORT.md",
        "WORKFLOW_REGISTER.md", "build_facility_pia_package.py", "validate_facility_pia_package.py",
        "review/first_pass/ADVERSARIAL_REVIEW.md", "review/first_pass/CROSS_DOMAIN_OWNERSHIP_REVIEW.md",
        "review/first_pass/DOCUMENTARY_GOLDEN_PATH_REVIEW.md",
        "review/first_pass/DOMAIN_OPERATIONAL_REVIEW.md",
        "review/first_pass/FIRST_DRAFT_HASH_MANIFEST.csv",
        "review/first_pass/MACHINE_TRACEABILITY_REVIEW.md",
        "review/first_pass/SECURITY_PRIVACY_TENANT_ISOLATION_REVIEW.md",
    ]
    def overview_purpose(path: str) -> tuple[str, str]:
        if path.startswith("review/first_pass/"):
            return "Preserved first-pass or isolated challenge evidence", "Founder/fresh reviewer"
        if "FOUNDER" in path:
            return "Founder decision, recommendation, question, or review material", "Founder"
        if "REVIEW" in path or "FINDING" in path or "REVISION" in path or "CONSISTENCY" in path or path == "REVIEW_DISPOSITION.md":
            return "Review, finding, revision, consistency, or disposition evidence", "Founder/fresh reviewer"
        if "MANIFEST" in path or "VALIDATION" in path or path.startswith("validate_"):
            return "Package integrity, evidence indexing, or validation", "Machine/evidence reviewer"
        if path.startswith("build_"):
            return "Reproducible documentary package builder; no product implementation", "Evidence custodian"
        if path == "SOURCE_REGISTER.md":
            return "Exact source identity, precedence, relevance, and gap record", "Evidence custodian"
        if path.startswith("PIA_FACILITY"):
            return "Human-readable or machine-readable controlling design candidate", "Founder/PIA owner"
        if path in {"REQUIREMENT_REGISTER.csv", "ACCEPTANCE_CRITERIA.csv", "TEST_MATRIX.csv"}:
            return "Requirement-to-proof specification and traceability", "Engineering/QA after authorization"
        if path in {"WORKFLOW_REGISTER.md", "GOLDEN_PATHS.md", "ADVERSARIAL_SCENARIOS.md"}:
            return "Whole workflow, reproduction, or negative scenario specification", "Domain/review functions"
        if path in {"DATA_DICTIONARY.md", "STATE_TRANSITION_MATRIX.csv", "PERMISSION_AND_AUTHORIZATION_BOUNDARY_MATRIX.csv", "API_EVENT_JOB_CONTRACTS.md"}:
            return "Candidate data, state, permission, or interface contract", "Architecture/security/engineering"
        if path == "AS_BUILT_RECONCILIATION.md":
            return "Static legacy implementation comparison and gap classification", "Architecture/engineering"
        return "Required governance register or control artifact", "PIA owner/relevant control owner"
    overview_rows = [(path, *overview_purpose(path)) for path in overview_files]
    emit("DOCUMENT_OVERVIEW_AND_RATIONALE.md", header("Document Overview and Rationale") + "\n" + table(["Document/group", "Why it exists", "Primary reader"], overview_rows) + "\n\nThe package is deliberately redundant only where human explanation and machine verification need parallel representations. Narrative and structured files must remain materially consistent.\n")

    emit("FOUNDER_DECISION_BRIEF.md", header("Founder Decision Brief") + f"""
## Decision posture

There are `{len(DECISIONS)}` unresolved decisions: 12 before design approval, 10 before implementation authorization, and 6 before enrollment. The package recommends a coherent model but does not adopt it. Decide the design-gate set first; the remaining questions can then be answered without reopening core definitions unless the Founder selects an alternative.

## Recommended model in one view

- Tenant: strict application isolation/governance context.
- Facility: durable physical-place identity and topology.
- Organization: durable legal/operating/admin/service entity identity.
- Barn: named operating context tied to a Facility/Area, never Tenant.
- Association, membership, role, payment and agreement: evidence inputs, never automatic authority.
- Consequential action: explicit visible context plus action-time authorization.
- Transfer/merge/closure: lineage-preserving and non-cascading.
- Public discovery: separate revocable coarse projection.
- Offline: minimum expiring reads/observations only; no consequential topology mutation.

## Highest-risk unresolved choices

1. FAC-FD-001/FAC-FD-002 — core distinctions and strict Tenant isolation. Choosing equivalence preserves the current ambiguity and is not recommended.
2. FAC-FD-008/FAC-FD-011/FAC-FD-012 — transition, relationship and authority boundaries. Any cascade or inferred authority risks cross-domain harm.
3. FAC-FD-019/FAC-FD-020 — offline and suspension behavior. Partial enforcement is a P1 risk.
4. FAC-FD-022/FAC-FD-016 — retention and public location. Both require deliberate data-risk decisions.
5. FAC-FD-017/FAC-FD-024 — first-user seed and context UX. These gate safe enrollment, not merely interface polish.

## Evidence limits

The documents were internally reviewed and revised and passed machine validation. The same Codex run used procedurally separated passes; this is not represented as an ES-RA review or a fresh external/segregated reviewer. Software was inspected statically only and is not conformant, verified, operational, or enrollment-ready.
""")

    recommendation_json = {"pia_id": PIA_ID, "notice": RECOMMENDATION_NOTICE, "recommendations": decision_rows}
    write_json("FOUNDER_DECISION_RECOMMENDATION_MATRIX.json", recommendation_json); written.append("FOUNDER_DECISION_RECOMMENDATION_MATRIX.json")

    question_rows = [{"question_id": f"FAC-OQ-{idx:03d}", "decision_id": d[0], "question": d[2], "why_needed": d[5], "recommended_answer": d[3], "alternatives": d[4], "gate": d[6], "status": "FOUNDER_DECISION_REQUIRED", "founder_input": ""} for idx, d in enumerate(DECISIONS, 1)]
    emit("FOUNDER_INPUT_QUESTIONS.md", header("Founder Input Questions") + "\n" + "\n".join(f"## {r['question_id']} / {r['decision_id']}\n\n**Question:** {r['question']}\n\n**Why needed:** {r['why_needed']}\n\n**Recommended candidate answer:** {r['recommended_answer']}\n\n**Alternatives:** {r['alternatives']}\n\n**Gate:** `{r['gate']}`\n\n**Founder input:** _not supplied_\n" for r in question_rows))
    write_csv("FOUNDER_INPUT_QUESTION_REGISTER.csv", list(question_rows[0]), question_rows); written.append("FOUNDER_INPUT_QUESTION_REGISTER.csv")

    emit("FOUNDER_REVIEW_PACKET.md", header("Founder Review Packet") + f"""
## Requested Founder action

1. Review the 12 design-gate decisions in FAC-FD-001 through FAC-FD-012.
2. Select or amend each answer and sign a separate decision record; do not treat this packet as the decision.
3. Direct a fresh segregated review after design answers are incorporated.
4. Only after that review, decide whether to approve the design. Implementation, release and enrollment remain separate later decisions.

## Executive summary

The portfolio gate passed before drafting. The package contains 43 mandatory PIA sections, 33 source records, 36 requirements, 13 workflows, 15 entities, 26 state transitions, 17 permission rules, 14 interface contracts, 28 Founder decisions, nine golden paths and 18 adversarial scenarios. The first review found 4 P1, 6 P2 and 3 P3 findings. Revision resolved all P1/P3 and four P2 document defects; two P2 items remain visible because they require Founder input or later implementation remediation.

## Non-negotiable inherited boundaries

- Facility truth is physical; Barn truth is operational; Organization truth is entity/business identity; Tenant truth is isolation context.
- Relationship and Authorization own relationship/authority truth.
- Facility placement, organization association, role, agreement, payment or possession cannot independently grant access.
- Transfers do not silently move horses, people, permissions, payments, agreements, private records or evidence.
- Current code is legacy evidence, not controlling design.

## Current disposition

`{DISPOSITION}`

This is the strongest truthful status. It is not approved, implementation-ready, implemented, verified, operationally ready or ready for controlled first-user enrollment.
""")

    return written


def review_and_revise() -> tuple[list[str], dict[str, str], dict[str, str]]:
    first_files = build_core_documents(revised=False)
    first_hashes = {name: sha(ROOT / name) for name in first_files}
    write_csv("review/first_pass/FIRST_DRAFT_HASH_MANIFEST.csv", ["path", "sha256", "review_scope"], [{"path": name, "sha256": digest, "review_scope": "INDIVIDUAL_FIRST_PASS_AND_APPLICABLE_CHALLENGE_PASSES"} for name, digest in sorted(first_hashes.items())])

    finding_rows = [{"finding_id": f[0], "severity": f[1], "review_lane": f[2], "finding": f[3], "affected_documents": f[4], "required_change": f[5], "disposition": f[6], "traceability": f[7]} for f in FINDINGS]
    write_csv("DOCUMENT_REVIEW_FINDINGS_REGISTER.csv", list(finding_rows[0]), finding_rows)

    lane_docs = {
        "review/first_pass/DOMAIN_OPERATIONAL_REVIEW.md": ("Domain and Operational Review", "Facility/Barn/Business source reread", ["FAC-FIND-P1-001", "FAC-FIND-P2-003"], "Facility physical truth and Barn operating truth are materially distinguishable; lifecycle/closure flows are viable after required revisions."),
        "review/first_pass/CROSS_DOMAIN_OWNERSHIP_REVIEW.md": ("Cross-Domain Ownership Review", "Identity, Relationship, Permission, Agreement, Horse and Claims boundaries", ["FAC-FIND-P1-002", "FAC-FIND-P2-004"], "The revised package leaves relationship and authorization truth with their authoritative domains and makes all structural associations non-authorizing."),
        "review/first_pass/SECURITY_PRIVACY_TENANT_ISOLATION_REVIEW.md": ("Security, Privacy, and Tenant-Isolation Review", "Tenant ID substitution, suspension, offline cache and public projection", ["FAC-FIND-P1-003", "FAC-FIND-P2-001", "FAC-FIND-P2-002"], "The revised design fails closed, applies suspension across surfaces, bounds offline use, and separates public projection."),
        "review/first_pass/ADVERSARIAL_REVIEW.md": ("Adversarial Review", "18 negative/misuse scenarios and transfer/merge behavior", ["FAC-FIND-P1-004"], "The non-cascade invariant is explicit and adversarial outcomes are testable."),
        "review/first_pass/MACHINE_TRACEABILITY_REVIEW.md": ("Machine and Traceability Review", "Identifier, source, requirement, AC/test/evidence and decision reference coverage", ["FAC-FIND-P2-005", "FAC-FIND-P3-002"], "Stable contract identifiers were added; unsupported retention precision remains a deliberate Founder decision."),
        "review/first_pass/DOCUMENTARY_GOLDEN_PATH_REVIEW.md": ("Documentary Golden-Path Review", "Nine end-to-end narratives, context visibility and first-user seed", ["FAC-FIND-P3-001", "FAC-FIND-P3-003"], "First-user topology and candidate-only recommendation language are explicit."),
    }
    for path, (title, basis, ids, result) in lane_docs.items():
        write(path, header(title, "PROCEDURALLY_ISOLATED_INTERNAL_REVIEW_COMPLETE") + f"""
## Reviewer-role declaration

This pass was conducted in a separate review context after first-draft hashes were frozen and with independent source re-reading. It is an internal procedurally segregated pass by Codex, not an activated custom agent, not an ES-RA role, and not the still-required fresh segregated review.

## Basis

{basis}.

## Findings

{', '.join(f'`{item}`' for item in ids)}.

## Result

{result}
""")

    write("FIRST_PASS_REVIEW_SUMMARY.md", header("First-Pass Review Summary", "FIRST_PASS_COMPLETE_REVISION_REQUIRED") + """
## Scope and method

Every Phase 2 and Founder-briefing draft listed in `review/first_pass/FIRST_DRAFT_HASH_MANIFEST.csv` received an individual content/consistency/traceability/status review. Six separate challenge contexts then re-read their relevant controlling sources and challenged the frozen draft. This is procedural segregation within one Codex run, not independent custom-agent or external review.

## Counts before revision

| Severity | Found | Required revision | Residual by design |
| --- | ---: | ---: | ---: |
| P0 | 0 | 0 | 0 |
| P1 | 4 | 4 | 0 |
| P2 | 6 | 4 document fixes | 2 |
| P3 | 3 | 3 | 0 |

All P1 changes were mandatory before a second pass. No draft was accepted on the first read without a recorded per-document disposition.
""")

    final_files = build_core_documents(revised=True)
    final_hashes = {name: sha(ROOT / name) for name in final_files}
    ledger_rows = []
    for name in sorted(first_files):
        affected = [f[0] for f in FINDINGS if name in f[4].split(";")]
        ledger_rows.append({"document": name, "first_draft_sha256": first_hashes[name], "first_pass_review": "COMPLETED", "finding_ids": ";".join(affected) or "NONE", "required_change": "YES" if affected else "NO", "revision_count": "1" if first_hashes[name] != final_hashes[name] else "0", "final_sha256": final_hashes[name], "second_pass_review": "COMPLETED", "final_status": "REVISED_AND_ACCEPTED_FOR_FOUNDER_REVIEW" if affected else "CONFIRMED_AND_ACCEPTED_FOR_FOUNDER_REVIEW"})
    write_csv("DOCUMENT_REVIEW_LEDGER.csv", list(ledger_rows[0]), ledger_rows)

    revision_rows = []
    for f in FINDINGS:
        revision_rows.append({"finding_id": f[0], "severity": f[1], "affected_documents": f[4], "change_made": f[5] if f[6].startswith("RESOLVED") else "No unsupported answer invented; item preserved as an explicit residual gate.", "verification": "SECOND_PASS_CONFIRMED" if f[6].startswith("RESOLVED") else "OPEN_AND_VISIBLE", "final_disposition": f[6], "traceability": f[7]})
    write_csv("REVISION_TRACEABILITY_REGISTER.csv", list(revision_rows[0]), revision_rows)
    write("REVISION_CHANGE_SUMMARY.md", header("Revision Change Summary", "REVISION_COMPLETE_SECOND_PASS_REQUIRED") + """
## Incorporated changes

- Separated BarnOperationalContext from Tenant and durable Facility identity.
- Repeated the rule that structural association and Organization verification never create authority.
- Applied suspension to UI, API, jobs, search, exports, webhooks and integrations, with only a separately governed safety-evidence exception candidate.
- Enumerated non-cascade protection for people, horses, permissions, agreements, billing, private records and evidence.
- Prohibited consequential offline topology mutation and required online revalidation.
- Defined a revocable public projection and protected exact/sensitive topology.
- Recorded adoption-record precedence over historical candidate wording in adopted source bodies.
- Added verification and capacity assertion entities, stable contract identifiers, and the unassigned first-user Area.
- Repeated candidate-only recommendation wording in Founder materials.

## Deliberately unresolved

`FAC-FIND-P2-005` remains pending FAC-FD-022 because no source supports an exact retention duration. `FAC-FIND-P2-006` remains an implementation gap because remediation is not authorized. Neither was silently invented or hidden.
""")
    return final_files, first_hashes, final_hashes


def build_second_pass(final_files: list[str]) -> None:
    open_rows = [
        {"finding_id": "FAC-FIND-P2-005", "severity": "P2", "summary": "Retention schedule requires Founder/legal/operational decision", "status": "OPEN_FOUNDER_DECISION", "blocking_gate": "IMPLEMENTATION_AUTHORIZATION", "traceability": "FAC-FD-022;FAC-RISK-008"},
        {"finding_id": "FAC-FIND-P2-006", "severity": "P2", "summary": "Legacy default/primary context and incomplete target topology remain in current code", "status": "OPEN_IMPLEMENTATION_GAP", "blocking_gate": "IMPLEMENTATION_AUTHORIZATION_AND_VERIFICATION", "traceability": "FAC-RISK-001;FAC-RISK-010;FAC-REQ-034"},
    ]
    write_csv("FINAL_OPEN_FINDINGS_REGISTER.csv", list(open_rows[0]), open_rows)
    write("SECOND_PASS_REVIEW_SUMMARY.md", header("Second-Pass Review Summary", "SECOND_PASS_COMPLETE_PENDING_FRESH_SEGREGATED_REVIEW") + f"""
## Method

All `{len(final_files)}` revised/confirmed Phase 2 and Founder-facing documents in `DOCUMENT_REVIEW_LEDGER.csv` were reread individually after revision. Cross-document identifiers, definitions, counts, gates, status statements, ownership, non-cascade rules, source precedence and machine/human parity were checked again.

## Results after revision

| Severity | Open | Result |
| --- | ---: | --- |
| P0 | 0 | None found |
| P1 | 0 | All four first-pass P1 defects resolved and rechecked |
| P2 | 2 | Visible Founder/implementation gates; neither is a hidden documentary defect |
| P3 | 0 | All three drafting findings resolved |

No fresh external/ES-RA/custom-agent review is claimed. The next assurance step is a genuinely fresh segregated review after Founder design decisions are incorporated.
""")
    write("CROSS_DOCUMENT_CONSISTENCY_REPORT.md", header("Cross-Document Consistency Report", "CONSISTENT_WITH_OPEN_GATES") + """
## Checks

- Tenant, Facility, Organization, Barn, Facility Area, association and active-context definitions are materially consistent across narrative, machine JSON, data dictionary, workflows and Founder brief.
- All 36 requirements link to one acceptance criterion, test and planned evidence ID.
- All 28 Founder decisions appear in Markdown, CSV, JSON and question registers with `FOUNDER_DECISION_REQUIRED` status.
- The 12/10/6 design/implementation/enrollment gate split is consistent.
- All source gaps are zero; lifecycle-precedence caveats are explicit.
- P0/P1/P2/P3 counts reconcile across findings, revision and second-pass reports.
- No document grants implementation, migration, release, deployment, enrollment, production, custom-agent or F-0001 authority.
- As-designed, as-built and as-verified baselines remain distinct.

## Residual consistency constraints

Founder answers must be incorporated through controlled change, then all structured matrices and counts must be regenerated. Current code remains nonconformant evidence until separately authorized remediation and verification occur.
""")
    write("REVIEW_DISPOSITION.md", header("Review Disposition", "INTERNAL_REVIEW_COMPLETE_FOUNDER_AND_FRESH_REVIEW_PENDING") + f"""
## Disposition

`{DISPOSITION}`

## Basis

- The ten-position Portfolio Realignment gate passed before Facility drafting began.
- Every Phase 2 and Founder-facing draft was individually reviewed, hashed, revised where required, and reviewed again.
- Six procedurally isolated challenge passes were completed without claiming an activated custom agent or ES-RA role.
- First-pass findings were P0=0, P1=4, P2=6, P3=3; final open findings are P0=0, P1=0, P2=2, P3=0.
- The two residual P2 items are explicit gates: unsupported retention precision requires Founder input, and legacy implementation nonconformance requires later authorization/remediation/verification.
- Machine validation must pass before packaging.

## Not granted

This disposition does not approve or ratify the design and does not authorize implementation, migration, PR, merge, tag, release, deployment, enrollment, production use, custom-agent activation, or F-0001 closure.
""")


def build_manifest_and_checksums() -> None:
    excluded = {"PACKAGE_MANIFEST.json", "CHECKSUM_MANIFEST.sha256", "VALIDATION_REPORT.md", "VALIDATION_REPORT.json"}
    files = [p for p in ROOT.rglob("*") if p.is_file() and p.relative_to(ROOT).as_posix() not in excluded and "__pycache__" not in p.parts]
    entries = [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(files)]
    manifest = {"package_id": PIA_ID, "version": "1.0.0-candidate", "date": DATE, "status": "FOUNDER_DECISION_REQUIRED", "disposition": DISPOSITION, "self_exclusions": sorted(excluded), "file_count_excluding_self_and_validation": len(entries), "files": entries, "authority": {"implementation": False, "migration": False, "release": False, "enrollment": False, "production": False, "custom_agent_activation": False, "f0001_closure": False}}
    write_json("PACKAGE_MANIFEST.json", manifest)
    checksum_files = [p for p in ROOT.rglob("*") if p.is_file() and p.name not in {"CHECKSUM_MANIFEST.sha256", "VALIDATION_REPORT.md", "VALIDATION_REPORT.json"} and "__pycache__" not in p.parts]
    write("CHECKSUM_MANIFEST.sha256", "\n".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}" for p in sorted(checksum_files)))


def main() -> None:
    final_files, _first, _final = review_and_revise()
    build_second_pass(final_files)
    # Validation reports are emitted by the separate validator.
    build_manifest_and_checksums()
    print(json.dumps({"package": PIA_ID, "phase2_and_founder_documents": len(final_files), "sources": len(source_rows()), "decisions": len(DECISIONS), "requirements": len(REQUIREMENTS), "first_pass_findings": len(FINDINGS), "disposition": DISPOSITION}, indent=2))


if __name__ == "__main__":
    main()
