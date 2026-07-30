# EquineSync Multi-Agent and Assurance Tooling Intent

**Document ID:** `ES-MAATI-2026-07-30`
**Version:** `1.0.0`
**Document Type:** Founder-Approved Tooling Intent
**Document Status:** `FOUNDER_APPROVED`
**Founder Approval Date:** `2026-07-30`
**Approval Method:** `EXPLICIT_WRITTEN_FOUNDER_INSTRUCTION_IN_CHATGPT_CONVERSATION`
**Repository Effect:** `FOUNDER_APPROVED_PENDING_PROTECTED_REPOSITORY_INTEGRATION`
**Repository:** `rianray2012-coder/EquineSync-V4`
**Applicable Program:** EquineSync Code Implementation Guide Program
**Controlling Program Plan:** `ES-CODE-GUIDE-CREATION-REVIEW-ASSURANCE-PLAN-V1.1`
**Controlling Founder Determination:** `ES-FD-SOLO-FOUNDER-COMPENSATING-ASSURANCE-2026-07-29`

---

## 1. Purpose

This document records the Founder's present intention to use a layered combination of machine-assisted review agents, deterministic analysis tools, executable tests, and controlled implementation agents during future repository mapping, implementation, verification, staging, pilot, and release work.

This tooling intent supplements the Solo-Founder Compensating Assurance Model. It does not replace exact-byte source control, Founder authority, protected repository controls, objective evidence, lifecycle-specific authorization, deterministic testing, residual-risk treatment, or truthful disclosure of non-independence.

The availability, licensing, configuration, or continued existence of a named product is not a prerequisite to limited Stage 24 activation.

---

## 2. Non-Vendor-Locked Role Categories

The following role categories control even if a named product is unavailable, renamed, discontinued, replaced, or not licensed:

1. `PRIMARY_IMPLEMENTATION_AGENT`
2. `SECURITY_REVIEW_AGENT`
3. `SECOND_MODEL_PULL_REQUEST_REVIEWER`
4. `READ_ONLY_SPECIALIST_REVIEW_AGENT`
5. `DETERMINISTIC_BROWSER_TEST_FRAMEWORK`
6. `DETERMINISTIC_STATIC_SECURITY_ANALYZER`
7. `BOUNDED_PARALLEL_IMPLEMENTATION_AGENT`
8. `OPTIONAL_PULL_REQUEST_REVIEW_AGENT`
9. `DEFERRED_HIGHER_RISK_REMOTE_IMPLEMENTATION_AGENT`

A replacement tool may not receive authority broader than the assigned role category without separate Founder approval.

---

## 3. Presently Intended Tooling Portfolio

### 3.1 OpenAI Codex

**Role:** `PRIMARY_IMPLEMENTATION_AGENT`

Codex may serve as the primary repository-analysis, implementation, testing, remediation, and documentary-evidence agent when separately authorized for the applicable workstream.

This intent does not itself authorize Codex to perform repository-specific implementation mapping, modify application code, modify schemas or migrations, modify CI or infrastructure, deploy, activate providers, enroll users, operate a pilot, or merge its own work.

### 3.2 Codex Security

**Role:** `SECURITY_REVIEW_AGENT`

Codex Security is intended to support repository-wide security review, threat modeling, vulnerability discovery, vulnerability validation, attack-path analysis, security-diff review, and proposed remediation review.

Its output is machine-assisted security evidence and does not constitute an independent human security audit or third-party certification.

### 3.3 GitHub Copilot Code Review

**Role:** `SECOND_MODEL_PULL_REQUEST_REVIEWER`

GitHub Copilot Code Review is intended to provide a second-model review of applicable pull requests.

Copilot findings remain advisory until validated against source code, reachable execution paths, deterministic tests, runtime reproduction, static-analysis evidence, or other objective evidence.

### 3.4 Claude Code Read-Only Specialist Agents

**Role:** `READ_ONLY_SPECIALIST_REVIEW_AGENT`

Claude Code read-only specialist agents are intended for isolated reviews of:

1. architecture and module boundaries;
2. authentication, authorization, tenancy, and facility isolation;
3. guardian and minor safeguarding;
4. database, state, and migration safety;
5. test quality and evidence sufficiency;
6. accessibility and human factors;
7. failure recovery and operational resilience;
8. equine-domain and barn-workflow practicality.

Recording this intention does not grant Claude Code write authority.

### 3.5 Browser-Assisted Testing and Playwright

**Role:** `DETERMINISTIC_BROWSER_TEST_FRAMEWORK`

Playwright is intended as the principal repeatable browser and end-to-end product-testing framework.

Browser-assisted exploratory testing may supplement Playwright by evaluating rendered behavior, console errors, user journeys, responsive layouts, mobile-browser behavior, accessibility, failure states, and recovery behavior.

Exploratory browser review shall not replace repeatable executable testing where such testing is reasonably available.

### 3.6 GitHub CodeQL

**Role:** `DETERMINISTIC_STATIC_SECURITY_ANALYZER`

GitHub CodeQL is intended as a deterministic static-analysis and security backstop where repository ownership, licensing, language support, and configuration permit.

CodeQL results shall be reconciled with source review, agent findings, executable tests, threat models, attack-path analysis, and remediation evidence.

### 3.7 Google Jules

**Role:** `BOUNDED_PARALLEL_IMPLEMENTATION_AGENT`

Google Jules may be considered later for separately authorized, bounded, lower-risk tasks such as missing tests, fixtures, documentation, isolated defects, narrowly scoped dependency maintenance, and repetitive low-risk cleanup.

Jules shall not receive authority over identity, tenancy, authorization, safeguarding, payments, migrations, deployment, or other high-risk areas without express workstream-specific authority.

### 3.8 Cursor Bugbot

**Role:** `OPTIONAL_PULL_REQUEST_REVIEW_AGENT`

Cursor Bugbot may be used as an additional pull-request reviewer.

Bugbot findings are advisory until validated.

### 3.9 Cursor Background Agents

**Role:** `DEFERRED_HIGHER_RISK_REMOTE_IMPLEMENTATION_AGENT`

Cursor Background Agents are deferred.

They may not be used until a later Founder directive establishes repository permissions, secret-handling controls, internet-access boundaries, prompt-injection controls, data-exfiltration controls, branch restrictions, pull-request restrictions, spending limits, review requirements, rollback procedures, and revocation procedures.

---

## 4. Evidence Treatment

All external-agent and automated-tool findings shall use an allowed lifecycle state:

- `AGENT_FINDING_UNVALIDATED`
- `AGENT_FINDING_REPRODUCED`
- `AGENT_FINDING_CORROBORATED`
- `AGENT_FINDING_REJECTED_WITH_EVIDENCE`
- `AGENT_FINDING_DEFERRED`
- `AGENT_FINDING_REMEDIATED`
- `AGENT_FINDING_RETESTED`

No finding shall be treated as proven merely because an agent or scanner produced it.

No agent may serve as the sole author, reviewer, approver, and merger of the same material change.

---

## 5. Access and Repository Boundaries

Recording this tooling intent does not authorize installation of a GitHub App, modification of GitHub organization or repository settings, creation or modification of CI workflows, addition of dependencies, connection of an external service, disclosure of repository contents to a new provider, production-secret access, production-database access, direct protected-branch writes, automated merging, autonomous deployment, staging use, pilot use, or production use.

Each action requires separate applicable authority.

---

## 6. Lifecycle Use

The intended tooling portfolio shall be considered during repository-specific implementation mapping, current-state gap analysis, assurance-infrastructure planning, implementation work-package design, test-plan design, security review, remediation review, staging readiness, pilot readiness, and later merge-gate and release-gate consideration.

---

## 7. Stage 24 Effect

The presence, absence, or configuration of any named tool is not a prerequisite to the limited Stage 24 activation presently under consideration.

This document does not adopt the Solo-Founder Assurance Profile, activate a Code Guide, establish an activation effective date, authorize implementation mapping, authorize implementation, authorize tool setup, authorize vendor access, or authorize deployment or pilot use.

---

## 8. Required Disclosures

Every later workstream relying on this tooling intent shall disclose which tool or agent was used, which exact commit or source set was reviewed, the permissions available to the tool, whether the tool could write or only read, whether network access was available, whether repository secrets were available, whether findings were independently reproduced, whether the tool authored the code under review, and the limitations of the resulting assurance.

---

## 9. Continuing Statements

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
