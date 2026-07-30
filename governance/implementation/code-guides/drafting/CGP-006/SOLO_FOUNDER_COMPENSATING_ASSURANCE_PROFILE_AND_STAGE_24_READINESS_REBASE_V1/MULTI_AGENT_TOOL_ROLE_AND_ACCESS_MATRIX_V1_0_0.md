# EquineSync Multi-Agent Tool Role and Access Matrix

**Document ID:** `ES-MATRAM-2026-07-30`
**Version:** `1.0.0`
**Document Status:** `FOUNDER_APPROVED`
**Founder Approval Date:** `2026-07-30`
**Approval Method:** `EXPLICIT_WRITTEN_FOUNDER_INSTRUCTION_IN_CHATGPT_CONVERSATION`

---

## 1. Matrix

| Tool | Role Category | Present Posture | Read | Write | Permitted Future Use | Prohibited Without Later Authority |
|---|---|---|---:|---:|---|---|
| OpenAI Codex | `PRIMARY_IMPLEMENTATION_AGENT` | Existing documentary agent; implementation not authorized | Yes when authorized | Branch-only when separately authorized | Mapping, implementation, testing, remediation, evidence | Direct protected writes, self-merge, deployment, pilot operation |
| Codex Security | `SECURITY_REVIEW_AGENT` | Planned | Yes | Patch proposals only when separately authorized | Threat model, repository scan, diff scan, validation, attack paths | Independent-audit claims, autonomous merge |
| GitHub Copilot Code Review | `SECOND_MODEL_PULL_REQUEST_REVIEWER` | Planned | PR and repository context | Review comments only | Second-model PR review | Sole approval, silent closure, protected write |
| Claude Code specialist agents | `READ_ONLY_SPECIALIST_REVIEW_AGENT` | Planned read-only | Yes | No | Architecture, authorization, safeguarding, database, tests, accessibility, recovery, domain workflow | Edit, commit, push, merge, production secrets |
| Playwright | `DETERMINISTIC_BROWSER_TEST_FRAMEWORK` | Planned | Test environment | Test artifacts only | End-to-end and browser testing | Production data or destructive production tests |
| Browser-assisted testing agent | `DETERMINISTIC_BROWSER_TEST_FRAMEWORK` supplemental | Planned | Rendered test app | Test interactions only | Exploratory workflow and visual QA | Replacing required repeatable tests |
| GitHub CodeQL | `DETERMINISTIC_STATIC_SECURITY_ANALYZER` | Planned subject to eligibility | Source | Findings only | Static security analysis | Treating a pass as complete assurance |
| Google Jules | `BOUNDED_PARALLEL_IMPLEMENTATION_AGENT` | Deferred | None now | None now | Later tests, fixtures, docs, narrow low-risk tasks | High-risk identity, tenancy, minors, payments, migrations, deployment |
| Cursor Bugbot | `OPTIONAL_PULL_REQUEST_REVIEW_AGENT` | Optional planned | PR context | Comments only | Additional PR review | Sole approval, automatic merge |
| Cursor Background Agents | `DEFERRED_HIGHER_RISK_REMOTE_IMPLEMENTATION_AGENT` | Deferred | None | None | Possible later bounded implementation | Any use before secrets, network, prompt-injection, spending, rollback, and revocation controls |

---

## 2. Default Permission Principle

```text
READ_ONLY_UNLESS_SEPARATELY_AUTHORIZED
BRANCH_ONLY_WHEN_WRITE_AUTHORIZED
NO_PROTECTED_BRANCH_WRITE
NO_AUTOMATIC_MERGE
NO_PRODUCTION_SECRETS
NO_PRODUCTION_DATABASE
NO_AUTONOMOUS_DEPLOYMENT
```

---

## 3. Required Access Review

Before connecting or expanding any tool, record repository scope, permission scope, accessible data, secret exposure, network access, retention terms, billing controls, revocation procedure, Founder decision, and reassessment date.

---

## 4. Continuing Statements

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
