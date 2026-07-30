# EquineSync External Agent Access Register

**Document ID:** `ES-EAAR-2026-07-30`
**Version:** `1.0.0`
**Document Status:** `FOUNDER_APPROVED_TEMPLATE`
**Founder Approval Date:** `2026-07-30`
**Approval Method:** `EXPLICIT_WRITTEN_FOUNDER_INSTRUCTION_IN_CHATGPT_CONVERSATION`
**Current Effect:** `NO_EXTERNAL_ACCESS_AUTHORIZED`

---

## 1. Access Register

| Access ID | Tool | Role | Status | Repository Scope | Read | Write | Network | Secrets | Production Data | Spending Limit | Approval | Review Date | Revocation | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `EAAR-0001` | OpenAI Codex | `PRIMARY_IMPLEMENTATION_AGENT` | `EXISTING_USE_SUBJECT_TO_WORKSTREAM_AUTHORITY` | `EquineSync-V4` | As authorized | Branch-only when authorized | Runtime-dependent | No production secrets | No | Founder-controlled | Founder | Before mapping | Revoke connector/session/token | Documentary use does not grant implementation authority |
| `EAAR-0002` | Codex Security | `SECURITY_REVIEW_AGENT` | `PLANNED_NOT_CONNECTED_BY_THIS_RECORD` | Proposed repo only | Proposed read | None by default | Provider scan environment | No | No | Founder-controlled | Pending | Before scan | Revoke GitHub App | No scan authorized here |
| `EAAR-0003` | GitHub Copilot Code Review | `SECOND_MODEL_PULL_REQUEST_REVIEWER` | `PLANNED_NOT_ENABLED_BY_THIS_RECORD` | Proposed repo | PR/repo context | Comments only | GitHub-hosted | No | No | GitHub controls | Pending | Before automatic review | Disable policy/app | Advisory only |
| `EAAR-0004` | Claude Code specialist agents | `READ_ONLY_SPECIALIST_REVIEW_AGENT` | `PLANNED_NOT_CONFIGURED_BY_THIS_RECORD` | Local clean clone | Read-only | None | Locally configured | No | No | Account controls | Pending | Before first review | Remove credentials/agents | Tool restrictions required |
| `EAAR-0005` | Playwright | `DETERMINISTIC_BROWSER_TEST_FRAMEWORK` | `PLANNED_NOT_INSTALLED_BY_THIS_RECORD` | Test environment | Test source/data | Test artifacts | Local/CI | Test-only later | No | CI controls | Pending | Before setup PR | Remove workflow/dependency | Separate authority required |
| `EAAR-0006` | GitHub CodeQL | `DETERMINISTIC_STATIC_SECURITY_ANALYZER` | `PLANNED_SUBJECT_TO_ELIGIBILITY` | Proposed repo | Source | Findings only | GitHub-hosted | No | No | GitHub plan | Pending | Before enablement | Disable scanning | Separate authority required |
| `EAAR-0007` | Google Jules | `BOUNDED_PARALLEL_IMPLEMENTATION_AGENT` | `DEFERRED` | None | None | None | Remote VM | No | No | Low limit required | Not approved | After implementation authority | Revoke GitHub App | High-risk areas prohibited |
| `EAAR-0008` | Cursor Bugbot | `OPTIONAL_PULL_REQUEST_REVIEW_AGENT` | `PLANNED_OPTIONAL_NOT_CONNECTED` | Proposed PRs | PR context | Comments only | Cursor-hosted | No | No | Cursor controls | Pending | Before connection | Revoke GitHub App | Advisory only |
| `EAAR-0009` | Cursor Background Agents | `DEFERRED_HIGHER_RISK_REMOTE_IMPLEMENTATION_AGENT` | `PROHIBITED_PENDING_LATER_CONTROLS` | None | None | None | Remote internet-connected | No | No | Limit required | Not approved | After mapping and implementation authority | Revoke app/credentials | Requires high-risk controls |

---

## 2. Allowed Status Values

- `PLANNED_NOT_CONNECTED_BY_THIS_RECORD`
- `PLANNED_NOT_ENABLED_BY_THIS_RECORD`
- `PLANNED_NOT_CONFIGURED_BY_THIS_RECORD`
- `PLANNED_NOT_INSTALLED_BY_THIS_RECORD`
- `PLANNED_SUBJECT_TO_ELIGIBILITY`
- `PLANNED_OPTIONAL_NOT_CONNECTED`
- `DEFERRED`
- `PROHIBITED_PENDING_LATER_CONTROLS`
- `APPROVED_READ_ONLY`
- `APPROVED_BRANCH_WRITE`
- `SUSPENDED`
- `REVOKED`

---

## 3. Connection Gate

No planned entry becomes approved merely because this register exists.

Before connection, the Founder shall approve the exact repository, permissions, data exposure, secrets posture, billing posture, retention posture, revocation plan, applicable workstream, allowed output, and prohibited output.

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
