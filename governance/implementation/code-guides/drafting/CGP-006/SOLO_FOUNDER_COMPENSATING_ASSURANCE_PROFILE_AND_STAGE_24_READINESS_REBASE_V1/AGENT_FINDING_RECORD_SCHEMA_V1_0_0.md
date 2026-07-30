# EquineSync Agent Finding Record Schema

**Document ID:** `ES-AFRS-2026-07-30`
**Version:** `1.0.0`
**Document Status:** `FOUNDER_APPROVED`
**Founder Approval Date:** `2026-07-30`
**Approval Method:** `EXPLICIT_WRITTEN_FOUNDER_INSTRUCTION_IN_CHATGPT_CONVERSATION`

---

## 1. Required Record

| Field | Required | Allowed or Expected Value |
|---|---:|---|
| `finding_id` | Yes | Stable unique identifier |
| `originating_tool` | Yes | Product or reviewer name |
| `role_category` | Yes | Approved role category |
| `review_type` | Yes | Declared review scope |
| `reviewed_repository` | Yes | `rianray2012-coder/EquineSync-V4` |
| `reviewed_commit` | Yes | Full commit SHA |
| `reviewed_branch_or_pr` | Yes | Branch or PR reference |
| `affected_file` | When applicable | Repository-relative path |
| `affected_line_or_symbol` | When applicable | Line range, function, class, route, query, schema, or workflow |
| `affected_guide_or_control` | When applicable | Guide, control, or invariant identifier |
| `title` | Yes | Concise title |
| `description` | Yes | Evidence-grounded explanation |
| `failure_or_attack_path` | Security/reliability findings | Reachable path or scenario |
| `severity` | Yes | `P0`, `P1`, `P2`, or `P3` |
| `confidence` | Yes | `HIGH`, `MEDIUM`, or `LOW` |
| `evidence` | Yes | Source, logs, test, trace, screenshot, query result, or reasoning summary |
| `reproduction_method` | When feasible | Deterministic steps or test |
| `affected_population_or_assets` | Yes | Users, facilities, horses, records, operations, or infrastructure |
| `proposed_treatment` | Yes | Remediate, defer, reject, constrain, test, or Founder decision |
| `validation_state` | Yes | Allowed lifecycle state |
| `validation_evidence` | After validation | Objective support or rejection evidence |
| `remediation_authority` | Yes | Authorized, not authorized, or pending |
| `remediation_commit` | After remediation | Full SHA |
| `retest_method` | After remediation | Exact method |
| `retest_result` | After retest | Pass, fail, partial, or blocked |
| `residual_risk` | Yes | Description or `NONE_IDENTIFIED` |
| `closure_authority` | Yes | Explicit authority |
| `status` | Yes | Current lifecycle state |

---

## 2. Minimal Template

```markdown
# Finding <ID>: <Title>

**Originating tool:**
**Role category:**
**Review type:**
**Reviewed repository:** `rianray2012-coder/EquineSync-V4`
**Reviewed commit:**
**Branch or PR:**
**Affected file:**
**Affected line or symbol:**
**Affected guide or control:**
**Severity:**
**Confidence:**
**Validation state:**

## Description

## Failure or Attack Path

## Evidence

## Reproduction Method

## Affected Population or Assets

## Proposed Treatment

## Validation Evidence

## Remediation Authority

## Remediation Commit

## Retest Method and Result

## Residual Risk

## Closure Authority
```

---

## 3. Prohibited Closure

A finding may not be closed solely because the originating agent withdrew it without evidence, another agent did not find it, the implementation agent disagreed, the build passed, the code compiled, the defect was not observed during one manual test, the feature is not live, or remediation is inconvenient.

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
