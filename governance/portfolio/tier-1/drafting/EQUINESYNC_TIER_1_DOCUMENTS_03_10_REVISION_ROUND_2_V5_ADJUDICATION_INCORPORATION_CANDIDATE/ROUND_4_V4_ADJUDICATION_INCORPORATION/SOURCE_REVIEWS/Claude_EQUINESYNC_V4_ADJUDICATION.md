# Adjudication — V4 Bounded Rereview Remediation Candidate

**Artifact:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V5_ADJUDICATION_INCORPORATION_CANDIDATE.zip`
**SHA-256:** `7070c863890cd1a6fc3938256588602d9eaf71164a3dd53ef268a931835f482a` — detached sidecar **matches**
**225 files · 185/185 checksums OK · 0 macOS metadata · predecessor `ad8805d5…` recorded in README**
**Authoritative validator:** `validate_tier1_documents_03_10_v4.py` → `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED`, 0 failures, 436 checks

`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

## 1. Handoff posture — verified

Each claim independently checked, not accepted on assertion.

| Claim | Verdict | Evidence |
|---|---|---|
| Draft PR #90 only | **VERIFIED** | Doc 09 register now carries 12 rows including PRs 83, 84, 90; validator check `doc09_includes_remediation_prs` enforces the set |
| Updated ZIP + detached checksum | **VERIFIED** | Sidecar `7070c863…` matches computed digest exactly |
| Single authoritative V4 validator | **VERIFIED** | Named in `README_FIRST.md` and enforced by `rereview_prompt_names_authoritative_v4` |
| Legacy validators non-operative | **VERIFIED** | rr2, v2, v3 all return `NON_OPERATIVE_HISTORICAL`, 0 checks, no failures. V3-01 is closed — the false `no_self_closed_findings: FAIL` can no longer be emitted |
| Structural result truthfully says closure blocked | **VERIFIED** | Headline is `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED`, driven by `open_rows`. V3-02 closed |
| Content status stays revision-required | **VERIFIED** | `PACKAGING_READY_FOR_BOUNDED_REREVIEW; CONTENT_REVISION_REQUIRED; …` — packaging and content readiness correctly decoupled |

All three V3 findings are closed. The posture is sound.

---

## 2. Document 10 (T1C-004) — **I was wrong. The finding is substantiated.**

V4's summary declines my recommended downgrade, stating that normalized-body review and the Perplexity/Cursor findings continue to support treating template purpose-specificity as unresolved. **On measurement, V4 is right and my two prior recommendations were wrong.** I had read individual templates, observed genuine Prohibited Conclusions sections and purpose-specific field schemas, and concluded purpose-specificity without measuring cross-template variance. That was a sampling error, and I am withdrawing the recommendation.

**Measurement across all 19 templates:**

| Metric | Result |
|---|---|
| Heading count | **10 in every template**, no variance |
| Byte length | 2,301–2,405 B — 4.3% spread |
| Mean pairwise Jaccard similarity (non-empty lines, 171 pairs) | **62.59%** |
| Minimum pairwise similarity | **62.50%** |
| Maximum pairwise similarity | 67.74% |
| Total range across all pairs | **5.24 points** |

A 5.24-point band across 171 pairs is the signature of one boilerplate with token substitution. Genuinely purpose-specific documents produce wide variance — a sampling record and a conflict disclosure should have little in common.

Diffing two functionally unrelated templates (`05_SAMPLING_RECORD` vs `07_CONFLICT_DISCLOSURE`) yields **5 changed lines out of ~40**: the title, the template name, one purpose sentence, the field list, and two example-row labels. Everything else is byte-identical.

**The check V4 built to answer this measures the wrong property.** `distinct_doc10_normalized_template_bodies` asserts `len(normalized) == 19` — a *uniqueness* test that fails only on byte-identical bodies. Nineteen templates differing by one word each would pass it. Its passing does not establish purpose-specificity; it establishes non-duplication.

**Adjudication: T1C-004 is SUBSTANTIATED but should be re-severitied to MEDIUM, not held at BLOCKING.** The field schemas are genuinely purpose-specific and are the load-bearing part — these templates are not interchangeable in use. The defect is narrower and more precise than "generic duplicates": **the control layer is undifferentiated**. Prohibited Conclusions, evidence-adequacy criteria, and completion-state rules are identical across all 19, when a sampling record and a conflict disclosure require materially different prohibitions and different evidence tests.

**Sufficient remediation:** author template-specific Prohibited Conclusions and evidence-adequacy criteria for each of the 19; replace the uniqueness check with a similarity ceiling (fail if any pair exceeds ~45% Jaccard on normalized bodies); retain the existing `doc10_template_body_collapse` fixture and add one proving the similarity ceiling can fail.

---

## 3. Document 03 (T1C-006) — real progress, **not sufficient for closure**

V4 performed the quarantine: 51 of 96 rows are now `REJECTED_SOURCE_FRAGMENT_NOT_REQUIREMENT`, with a dedicated `NON_REQUIREMENT_SOURCE_FRAGMENT_QUARANTINE.csv` (51 rows, 6 columns) and a validator check confirming its presence. It correctly caught the two worst examples I cited: `T1R2-REQ-0002` (the JSON string literal) and `T1R2-REQ-0003` (the pipe-delimited table row). That is genuine substantive work, not a documentation gesture.

**Three reasons it cannot close:**

**(a) The quarantine keyed on syntax, not requirement quality.** Sampling the 45 surviving candidates, at least 4 of the first 6 are still fragments:

| ID | Surviving text | Why it is not a requirement |
|---|---|---|
| `T1R2-REQ-0001` | "Implement the smallest viable fix. Avoid architectural changes unless required." | AI coding-prompt instruction from `AI_CODING_PROMPTS.md` |
| `T1R2-REQ-0016` | "this document. Founder/legal or an assigned compliance owner must approve the" | Mid-sentence fragment, lowercase start, truncated both ends |
| `T1R2-REQ-0019` | "BN19 cannot close until founder accepts or defers:" | Colon-terminated lead-in to a list |
| `T1R2-REQ-0020` | "2. App Store / Google Play timing: required before public launch, deferred after" | Numbered list item, truncated |

**(b) The basis for the 51 rejections is unrecorded.** All nine ISO-29148 columns — `singular_check`, `unambiguous_check`, `verifiable_check`, `complete_check`, and the rest — remain `NOT_PERFORMED` on all 96 rows, and `discovery_method` is `NOT_PERFORMED` throughout. The quarantine register carries a single `quarantine_reason` value repeated across all 51 rows. The rejections are asserted, not evidenced, in the fields that exist for exactly this purpose.

**(c) Coverage metrics were not recomputed.** `COVERAGE_METRICS_BY_DOMAIN.csv` still reports `total_source_text_candidates=96` and `open_candidate_rows=96` in the OVERALL row, with domain rows summing to 96. Only **45** candidates remain after quarantine. The metrics now contradict the register they summarize — a defect introduced by the quarantine itself. `accepted_normative_requirements=0` and `verified_coverage=0.0` remain correct and honest.

**Sufficient remediation:** run and record the ISO-29148 checks on the surviving 45; expect further rejections; give each quarantined row a specific reason rather than one shared string; recompute all coverage metrics against the post-quarantine population; add a validator check asserting `total_source_text_candidates` equals the non-rejected row count.

---

## 4. Retained open T1C items — dispositions concurred

Nine items are retained open. All are correctly retained; none should be closed in this build.

| Item | Severity | Concurrence |
|---|---|---|
| T1C-003 residual-risk population | BLOCKING | **Correct.** Doc 06 remains 9 rows, all `finding`, zero risk/exception/waiver. `FD-T1R2-004` still asks for disposition over an empty population. Unchanged and correctly open |
| T1C-004 Doc 10 templates | BLOCKING | **Correct to retain** — see §2. Re-severity to MEDIUM |
| T1C-006 Doc 03 corpus | BLOCKING | **Correct** — see §3 |
| T1C-010 production/deployment evidence separation | HIGH | **Correct.** Documentary-only separation remains |
| T1C-013 workstream currency | MEDIUM | **Correct, and still incompletely addressed.** PRs 83/84/90 added, but no `captured_at` or as-of column exists on any of the 12 rows. Currency remains unassessable |
| T1C-014 boilerplate/content depth | MEDIUM | **Correct.** Doc 06 moved from 1 to 2 distinct `closure_evidence` values across 9 rows — marginal |
| T1C-016 principal document thinness | MEDIUM | **Correct** |
| T1C-019 Second Reviewer boundary | LOW | **Correct.** Non-assertion language holds; Doc 07 still `appointment_evidence=NOT_RECORDED` × 14 |
| T1C-020 single-platform validation | LOW | **Correct** as `RETAINED_NONBLOCKING_OPEN` |

---

## 5. Can any pending-remediated findings be accepted?

**Yes — seven of the eleven, on originating-reviewer concurrence.**

An important boundary first: I am the originating reviewer for the CLAUDE-sourced findings, so I can verify whether what I raised was fixed. **That is originating-reviewer concurrence, not independent closure, and I am not independent of findings I authored.** The package's rule — closure requires Second Reviewer or originating-reviewer concurrence — is satisfied for these; the Founder or Second Reviewer still acts. `second_reviewer_state` must remain `NOT_PERFORMED_NOT_FABRICATED` on all 20 rows regardless of what follows.

**Concur — acceptable for closure:**

| Item | Verified by direct measurement |
|---|---|
| **T1C-001** integrity chain | 185/185 OK; detached sidecar matches; predecessor digest and byte length in README; `MANIFEST_OF_MANIFESTS` correctly rescoped to 34 manifest artifacts |
| **T1C-002** lifecycle state count | "thirteen-state" in `…REGISTER.csv:2`, `.json:21`, `FOUNDER_DECISION_PACKET.csv:2`; fixture `decision_text_lifecycle_count_mismatch` detects the defect; external reviewer's original wording preserved unaltered |
| **T1C-007** traceability placeholders | `source_review_ids` 19 distinct across 20 rows; `evidence_locator` 20/20 distinct; duplicate-register problem resolved |
| **T1C-008** validator overstatement | Headline is now `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED`; 436 checks; legacy validators inert; two fixture suites execute and detect every planted defect |
| **T1C-009** preselected approval | `recommended_option=NO_RECOMMENDATION_SELECTED` on all five decisions; no disposition recorded anywhere |
| **T1C-015** terminology | Certification/audit/attestation prohibitions enforced; inventory readiness check blocks `READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL` |
| **T1C-017** custody disclosure | Detached checksum, predecessor digest, custody record, PR #90 identity all present |

**Do not accept — outside my origination, or verification incomplete:**

- **T1C-005** (source authority labels) and **T1C-018** (authoritative-current wording) — sourced substantially from Cursor and Perplexity. The V4 checks `candidate_paths_not_authoritative_current` and the prefix-stripping check both pass, but the originating reviewers should concur, not me.
- **T1C-011** (lifecycle transitions) — the state count is fixed, but my R2-09 (candidate-stage supersession forbidden by the matrix yet recorded as having occurred) and R2-10 (`REJECTED` terminal, no resubmission path) are folded into this item and I see no evidence either was addressed. **Recommend reopening T1C-011 or splitting the transition-completeness defects into a new item.**
- **T1C-012** (duplicate cluster referential linkage) — passes, but originated with Cursor.

**One caveat on T1C-008.** I concur it is remediated *as scoped* — the overstatement is gone and the fixtures are real. But the eight per-document validators remain 344-byte presence checks: `validate_document_03_rr2.py` still fails only if its directory contains no `.csv`, `.json`, or `.md` file. That was R2-06, and it is unaddressed. If T1C-008 is read as covering per-document validator substance, it is not remediated. Recommend recording the per-document validator defect as a separate open item rather than letting it close inside T1C-008.

---

## 6. Determination

**V4 remediations are sufficient for their stated scope — bounded packaging remediation and handoff readiness — and are not sufficient for content closure. The package's own status says exactly this, and it is accurate.**

`PACKAGING_READY_FOR_BOUNDED_REREVIEW` — **concur.** The handoff posture is correct and no longer has defects that would derail an independent engagement.

`CONTENT_REVISION_REQUIRED` — **concur.** Two blocking items (T1C-003, T1C-006) plus a re-severitied T1C-004 remain genuinely open, and three new sub-defects surfaced in this adjudication: the Doc 03 coverage-metric mismatch, the Doc 10 distinctness check measuring uniqueness rather than similarity, and the transition-completeness defects apparently lost inside T1C-011.

Recommended actions before the bounded re-review is commissioned: recompute the Doc 03 coverage metrics (§3c — an arithmetic contradiction is the kind of thing that consumes reviewer attention cheaply), re-severity T1C-004 to MEDIUM with the corrected defect statement (§2), and reopen or split T1C-011 (§5). The seven concurred items can be moved to closed-pending-Founder on this concurrence.

Nothing in this adjudication adopts, activates, authorizes implementation or production use, authorizes merge, certifies, waives, accepts risk, or records a Founder decision.
