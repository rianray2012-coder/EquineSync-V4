# EquineSync Multi-Agent Review and Finding Validation Policy

**Document ID:** `ES-MARFVP-2026-07-30`
**Version:** `1.0.0`
**Document Status:** `FOUNDER_APPROVED`
**Founder Approval Date:** `2026-07-30`
**Approval Method:** `EXPLICIT_WRITTEN_FOUNDER_INSTRUCTION_IN_CHATGPT_CONVERSATION`
**Policy Effect:** `FOUNDER_APPROVED_PENDING_PROTECTED_REPOSITORY_INTEGRATION`

---

## 1. Purpose

This policy defines how EquineSync shall use machine-assisted reviewers, deterministic scanners, executable tests, browser agents, and implementation agents without mistaking agent quantity for evidence quality.

---

## 2. Core Rules

1. Every review shall identify the exact commit, branch, guide version, source path, or frozen artifact reviewed.
2. Initial specialist reviews should be isolated from other reviewers' conclusions where reasonably practicable.
3. Every material finding shall identify a source location and an affected invariant, control, or expected behavior.
4. A speculative concern shall not be reported as a confirmed defect.
5. A scanner pass shall not be treated as proof of complete security.
6. A passing build shall not be treated as proof of correct authorization, tenancy, safeguarding, recovery, accessibility, or product usability.
7. No agent may self-approve or merge its own material implementation.
8. High-risk findings require reproduction, corroboration, or objective support before remediation priority is finalized.
9. Rejected findings require an evidence-backed rationale.
10. Remediated findings require retesting against the repaired commit.

---

## 3. Finding Lifecycle

| State | Meaning |
|---|---|
| `AGENT_FINDING_UNVALIDATED` | Reported but not independently checked against source or execution. |
| `AGENT_FINDING_REPRODUCED` | Reproduced through execution, deterministic test, or direct source proof. |
| `AGENT_FINDING_CORROBORATED` | Supported by another review path, scanner, or objective artifact. |
| `AGENT_FINDING_REJECTED_WITH_EVIDENCE` | Rejected with recorded source, test, or architectural evidence. |
| `AGENT_FINDING_DEFERRED` | Valid or plausible but assigned to a later authorized lifecycle stage. |
| `AGENT_FINDING_REMEDIATED` | A separately authorized remediation has been implemented. |
| `AGENT_FINDING_RETESTED` | Remediation was retested and the result recorded. |

Prohibited states include `AGENT_FINDING_ASSUMED_TRUE`, `AGENT_FINDING_CLOSED_BY_SILENCE`, `AGENT_FINDING_CLOSED_BY_MODEL_CONFIDENCE`, and `AGENT_FINDING_REMEDIATED_WITHOUT_RETEST`.

---

## 4. Required Finding Fields

Every material finding shall record:

1. finding ID;
2. originating tool or reviewer;
3. reviewer role category;
4. exact reviewed commit or artifact;
5. affected file and line or symbol;
6. affected guide, control, invariant, or product expectation;
7. defect or risk description;
8. reachable execution path or failure scenario;
9. severity;
10. confidence;
11. evidence;
12. reproduction method;
13. affected users, data, horses, facilities, or operations;
14. proposed treatment;
15. validation status;
16. remediation authority state;
17. retest requirement;
18. residual risk;
19. closure authority.

---

## 5. Severity

| Severity | Treatment |
|---|---|
| `P0` | Immediate stop for catastrophic or uncontrolled harm, compromise, or authority failure. |
| `P1` | Blocks the applicable readiness, activation, mapping, implementation, staging, pilot, or release decision. |
| `P2` | Material risk requiring explicit treatment and retained visibility. |
| `P3` | Improvement, warning, maintainability concern, or lower-severity defect. |

An agent may propose severity, but final lifecycle effect shall be determined through applicable governance authority and evidence.

---

## 6. High-Risk Review Requirements

Changes affecting authentication, authorization, tenancy, facility isolation, guardian or minor controls, support impersonation, private records, horse-health or care records, uploads, payments, provider callbacks, migrations, account recovery, session revocation, audit evidence, deployment, secrets, or rollback require at least two distinct review modes plus deterministic verification where feasible.

Qualifying review modes include primary implementation review, second-model PR review, specialist read-only review, security scan, static analysis, executable test, browser journey, database constraint test, and threat-model review.

---

## 7. Reviewer Separation

For a material change, the implementation agent may explain its design and evidence, another reviewer or review mode must challenge the change, the Founder remains the approval authority where required, protected integration shall follow repository controls, and the implementation agent shall not be the sole source of closure evidence.

---

## 8. Conflicting Findings

When reviewers disagree:

1. preserve both findings;
2. identify the disagreement;
3. compare exact source and assumptions;
4. attempt deterministic reproduction;
5. record the reconciliation;
6. escalate unresolved policy questions to `FOUNDER_DECISION_REQUIRED`;
7. do not average conflicting conclusions into a false compromise.

---

## 9. Tool Limitations

Every report shall disclose relevant limitations, including incomplete repository coverage, unavailable dependencies, unavailable runtime environment, missing credentials, network restrictions, synthetic-data limitations, unsupported languages, model context limitations, inaccessible production behavior, and absence of independent human review.

---

## 10. Continuing Statements

`PROGRAM_PLAN_V1_1_CONTROLLING`

`SOLO_FOUNDER_COMPENSATING_ASSURANCE_DETERMINATION_CONTROLLING`

`FOUNDER_SOLO_COMPENSATING_ASSURANCE_MODEL_APPLIES`

`EQUINESYNC_IS_A_SOLO_FOUNDER_PROJECT`

`MACHINE_ASSISTED_REVIEW_IS_NOT_INDEPENDENT_HUMAN_REVIEW`

`ALL_AGENT_FINDINGS_REQUIRE_VALIDATION`

`NO_AGENT_MAY_SELF_APPROVE_ITS_OWN_IMPLEMENTATION`

`NO_AGENT_DIRECT_PROTECTED_BRANCH_WRITE`

`MULTI_AGENT_TOOLING_INTENT_FOUNDER_APPROVED`

`NO_EXTERNAL_TOOL_SETUP_AUTHORIZED`

`IMPLEMENTATION_MAPPING_NOT_AUTHORIZED`

`IMPLEMENTATION_NOT_AUTHORIZED`

`DEPLOYMENT_NOT_AUTHORIZED`

`PILOT_NOT_AUTHORIZED`

`PRODUCTION_NOT_AUTHORIZED`
