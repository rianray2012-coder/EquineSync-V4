#!/usr/bin/env python3
"""Create fresh ES-REV-2026-022 role outputs after the fail-closed permission gate."""

from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
PACKAGE = REPO / "governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE"
CYCLE = REPO / "governance/founder_orchestrated_review/review_cycles/ES-REV-2026-022"
COMMIT = "56b0a88722d983e05baec0d3b1ea5b7b88c24001"
TREE = "a60e900c2d0eef17c1f1b8a98f01f5ff1e30647d"


def write(name: str, body: str) -> None:
    normalized = "\n".join(line.rstrip() for line in body.strip().splitlines()) + "\n"
    (PACKAGE / name).write_text(normalized, encoding="utf-8")


write(
    "REVIEW_AUTHORIZATION.md",
    f"""
# Founder Review Authorization — ES-REV-2026-022

**Review cycle:** `ES-REV-2026-022`  
**Authorized by:** Rian Ray, Founder and Program Owner  
**Authorization date:** `2026-07-21`  
**Fresh-review directive SHA-256:** `7c49bf8157d8c3bf3966d1669a3719de54bdf7ad195e1cfd5edfc94a38a529c6`  
**Exact R2 input commit:** `{COMMIT}`  
**Exact R2 input tree:** `{TREE}`  
**R2 input manifest SHA-256:** `fc9ea834472aa603ebebe099b2270a091ce8af72a736bb6183a2066e42c81527`

The Founder authorized an attempt at a fresh documentary structured review of the byte-unchanged `1.0.1-R2` Facility PIA candidate. The authorization requires a complete `PASS` pre-spawn permission record before each formal role begins. It grants no broad exception to `AGENTS.md` or `RUNTIME_PERMISSION_CONTROL.md`.

The required role posture is read-only/on-request/network-disabled for documentary reviewers and isolated bounded workspace-write/on-request/network-disabled for Machine Validation, Evidence Custody, and Synthetic Documentary Specification. Production access must be absent and measurable.

The live parent posture was unrestricted/danger-full-access equivalent, `approval_policy=never`, and network-enabled. The task exposed no compliant permission transition and no reliable way to measure the effective reviewer mode without a prohibited spawn. Six of six formal-role checks therefore failed and zero roles started.

Authorized outcome under this condition: create review-cycle failure evidence and assign `FACILITY_PIA_REVIEW_BLOCKED_BY_RUNTIME_PERMISSION_FAILURE`. This authorization does not approve, adopt, lock, implement, release, deploy, activate, enroll, or start the application or any service.

Prohibited: application-code, database, schema, migration, service-start, executable-test, enrollment, production, deployment, release, PR, merge, tag, adoption, lock, unrelated-finding closure, sealed-source modification, and any representation that the Identity and Relationships successor text is Founder-approved.
""",
)

(PACKAGE / "RUNTIME_PERMISSION_RECORDS.csv").write_bytes((CYCLE / "RUNTIME_PERMISSION_RECORDS.csv").read_bytes())


def blocked_report(
    title: str,
    role: str,
    run_id: str,
    expected: str,
    denominator: str,
    procedures: str,
    next_action: str,
) -> str:
    return f"""
# {title}

**Review cycle:** `ES-REV-2026-022`  
**Agent run ID:** `{run_id}`  
**Requested role:** {role}  
**Exact R2 input commit:** `{COMMIT}`  
**Exact R2 input tree:** `{TREE}`  
**Permission record:** `RUNTIME_PERMISSION_RECORDS.csv`  
**Permission result:** `FAIL`  
**Formal run validity:** `NOT_STARTED_PERMISSION_CHECK_FAILED`  
**Role started:** `false`  
**Custom-agent execution claimed:** `false`

## Pre-spawn result

Required posture: `{expected}`. Observed parent posture: unrestricted/danger-full-access equivalent, `approval_policy=never`, network enabled. Actual reviewer mode was not observed because the role was not spawned. No Founder exception exists. The role stopped before substantive work, as the authorization requires.

## Scope denominator and accounting

Assigned population: {denominator}.

- Validly completed: 0
- Completed with limitation: 0
- Blocked/not reviewed: complete assigned population
- Formal coverage: 0%
- Sampling: none

## Procedures not performed

{procedures}

No substantive conclusion from ES-REV-2026-021 was copied or treated as evidence for this role.

## Classifications

- Completeness: `C0_NOT_STARTED`
- Reliability: `R0_UNASSESSED`
- Substantive evidence sufficiency: `E0_NO_SUPPORTING_EVIDENCE`
- Formal disposition: not issued
- Orchestration gate result: `PERMISSION_CHECK_FAILED`

## Completion Attestation

Not issued. The role did not start and no Work Completeness Ledger for substantive role procedures exists.

## What This Work Did Not Establish

This blocked role did not establish correctness, completeness, absence of findings, pass status, adoption-review readiness, implementation status, executable behavior, or external assurance.

## Required next action

{next_action}
"""


write(
    "SEGREGATED_REVIEW_REPORT.md",
    blocked_report(
        "Segregated Review Report",
        "ES-RA-02 Segregated Review Agent",
        "ES-REV-2026-022-RA02-01",
        "read-only/on-request/network-disabled",
        "18 Founder decisions; 55 requirements; 55 acceptance criteria; 85 test specifications; 16 focused FAC-FD-017 cases; two independent review passes",
        "Independent detection, structured coverage, omission search, source-to-provision verification, P0/P1 evidence inspection, overstatement review, self-audit, and completion attestation were not performed.",
        "Launch a fresh ES-RA-02 only after its pre-spawn record passes in a read-only/on-request/network-disabled runtime.",
    ),
)

write(
    "ADVERSARIAL_CHALLENGE_REPORT.md",
    blocked_report(
        "Adversarial Challenge Report",
        "ES-RA-03 Adversarial Challenge Agent",
        "ES-REV-2026-022-RA03-01",
        "read-only/on-request/network-disabled",
        "the complete applicable challenge inventory, including authority inference, shared-facility isolation, stale context, duplicate/merge, legacy quarantine, lifecycle, privacy, and adaptive-onboarding abuse categories",
        "Challenge-inventory initialization, negative-path analysis, bypass analysis, reproducibility records, exception-abuse review, severity assessment, and challenge reconciliation were not performed.",
        "Launch a fresh ES-RA-03 only after its pre-spawn record passes in a read-only/on-request/network-disabled runtime.",
    ),
)

write(
    "DOMAIN_REVIEW_REPORT.md",
    blocked_report(
        "Domain Review Report",
        "ES-RA-06 Facility/Tenant/Organization Domain Reviewer",
        "ES-REV-2026-022-RA06-01",
        "read-only/on-request/network-disabled",
        "Tenant, Facility, Organization, Barn, Business, membership, stewardship, relationship, authority, provider capability, and their actors, records, permissions, states, transitions, exceptions, corrections, retention, recovery, and adjacent interfaces",
        "Domain Coverage Model construction, authority-source inspection, operational-scenario analysis, cross-domain conflict review, specialist-referral assessment, and independent domain conclusions were not performed.",
        "Launch a fresh ES-RA-06 only after its pre-spawn record passes in a read-only/on-request/network-disabled runtime.",
    ),
)

write(
    "MACHINE_VALIDATION_REPORT.md",
    blocked_report(
        "Machine Validation Report",
        "ES-RA-04 Machine Validation Agent",
        "ES-REV-2026-022-RA04-01",
        "isolated bounded workspace-write/on-request/network-disabled",
        "the complete formal validation inventory for package structure, hashes, cross-format parity, requirement/acceptance/test traceability, machine-readable status, and correction re-verification",
        "No formal validation inventory was initialized; no independent command suite, repeatability test, tool-trust assessment, or separate re-performance occurred. Orchestrator intake reproduced the R2 checksums and 25/25 package checks only to establish immutable input identity. Those intake checks are not an ES-RA-04 run. Prior finding ES-REV-2026-021-MV-F-0001 therefore remains REMEDIATED_UNVERIFIED.",
        "Launch a fresh ES-RA-04 in an isolated bounded workspace-write/on-request/network-disabled environment and independently reverify the R2 correction.",
    ),
)

write(
    "EVIDENCE_CUSTODY_REPORT.md",
    blocked_report(
        "Evidence Custody Report",
        "ES-RA-05 Evidence Custodian",
        "ES-REV-2026-022-RA05-01",
        "controlled bounded workspace-write/on-request/network-disabled",
        "expected, received, missing, unused, conflicting, derivative, and relied-upon evidence inventories plus the cross-agent completion gate",
        "No formal custody inventories, evidence-reliance map, derivative-parent confirmation, broken-reference closure check, independent hash recalculation, or cross-agent completion verification occurred. Orchestrator intake reproduced the exact R2 package identity and 39/39 relied-source hashes from Git objects; that intake evidence is not an ES-RA-05 completion.",
        "Launch a fresh ES-RA-05 only after its pre-spawn record passes in a controlled bounded workspace-write/on-request/network-disabled environment.",
    ),
)

write(
    "SYNTHETIC_GOLDEN_PATH_REPORT.md",
    blocked_report(
        "Synthetic Golden Path Documentary Review Report",
        "ES-RA-07 Synthetic Golden-Path Specification Agent",
        "ES-REV-2026-022-RA07-01",
        "authorized bounded workspace-write/on-request/network-disabled; documentary only",
        "the 12 Founder-directed documentary golden paths",
        "No fresh path-by-path authority, actor, permission, state, transition, action, expected-result, oracle, evidence, cleanup, timing, or integration review occurred. Existing R2 Golden 12 materials are historical input only. No executable controller was authorized or run.",
        "Launch a fresh ES-RA-07 only after its pre-spawn record passes in a bounded workspace-write/on-request/network-disabled documentary specification environment.",
    ),
)

print("fresh blocked role outputs written")
