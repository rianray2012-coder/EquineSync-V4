# EquineSync Tier 1 Documents 03–10 — Revision Round 2 V4 Bounded Re-Review
## Independent Adjudication of Remediation Sufficiency

**Reviewer self-identification (mandatory):** Perplexity Computer — machine-assisted independent documentary review. Not an accredited certification body under ISO/IEC 17021-1:2015, not a licensed CPA firm, not a third-party conformity assessment body. Second-party documentary review under ISO/IEC 17000:2020 cl. 4.4; not an audit under ISO 19011:2018 cl. 3.1.

**Authority boundary (preserved):** `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

**Package:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V5_ADJUDICATION_INCORPORATION_CANDIDATE.zip`
**Detached checksum:** `7070c863890cd1a6fc3938256588602d9eaf71164a3dd53ef268a931835f482a` — **independently recomputed and matched byte-exact.** Archive 2,763,428 bytes; 225 files extracted.

---

## 1. Disposition

| Surface | Disposition |
|---|---|
| Packaging, custody, validator architecture | `READY_WITH_NONBLOCKING_REVISIONS` |
| Doc10 (Closing Audit Protocol) | `READY_WITH_NONBLOCKING_REVISIONS` |
| Doc03 (Implementation Traceability) | `REVISION_REQUIRED` |
| Doc04 lifecycle rule content | `REVISION_REQUIRED` (new finding V4-01) |
| **Overall package** | **`REVISION_REQUIRED`** |

The overall disposition matches the package's own declared status. V4 does not overclaim. This is the second consecutive round in which the package's self-assessment is corroborated rather than corrected downward.

---

## 2. Handoff posture — all six claims verified TRUE

| Claim | Verdict | Evidence |
|---|---|---|
| Draft PR #90 only | **TRUE** | 11 references to PR #90 as current carrier; all 29 PR #83 references appear only in delta reports, custody records, and prior-round source reviews — historical context, not current handoff |
| Updated ZIP + detached checksum | **TRUE** | Recomputed SHA-256 matches the `.sha256` sidecar exactly |
| Single authoritative V4 validator | **TRUE** | `validate_tier1_documents_03_10_v4.py` runs 436 checks, 0 failures |
| Legacy validators non-operative | **TRUE (minor residual)** | RR2/V2/V3 reduced to ~569-byte stubs emitting `NON_OPERATIVE_HISTORICAL` and redirecting to V4 |
| Structural result truthfully says substantive closure blocked | **TRUE** | Returns `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED` |
| Content status stays revision-required | **TRUE** | `package_status` carries `CONTENT_REVISION_REQUIRED` plus the full boundary string |

**Validator consolidation did not lose coverage — this was my primary risk going in.** Collapsing four validators into one could silently have dropped the RR2 integrity suite. It did not: V4 carries 185 root-manifest hash/byte-length bindings, 185 root-checksum bindings, and 38 manifest-of-manifests checks (408 of 436), i.e. it absorbed and exceeded RR2's 260 checks, then added the distinct-value guards.

**Nonblocking residual (V4-02, S3):** the legacy stubs exit with return code 0. A non-operative validator wired into CI would register as a pass. Recommend `sys.exit(2)`.

---

## 3. Doc10 — SUFFICIENT. Recommend accepting T1C-004.

Doc10 was the longest-standing unremediated defect in this program (P-04/F-02, open since Round 2 V1, falsely claimed closed in V2, correctly retracted to `NOT_REMEDIATED_RETAINED_OPEN` in V3). **V4 genuinely fixes it.**

**P-04 — templates.** 19 templates, 45 lines each, **19 distinct normalized bodies** (previously 1). Section-level analysis:

| Section | Distinct/19 | Assessment |
|---|---|---|
| Purpose | 19/19 | Purpose-specific |
| Required Evidence Fields | 19/19 | Purpose-specific |
| Mandatory Evidence Table | 19/19 | Purpose-specific |
| Scope Boundary | 1/19 | Correctly uniform |
| Prohibited Conclusions | 1/19 | Correctly uniform |
| Collection Method | 1/19 | **Residual** |
| Required Determinations | 1/19 | **Residual** |
| Completion Fields | 1/19 | **Residual** |

The field sets are semantically correct, not decorative. `SOURCE_MANIFEST` requires `source_id, repository_path, sha256, byte_length, git_blob, controlling_version, custody_state`. `SAMPLING_RECORD` requires `population_definition, sample_size, selection_method, selected_row_ids, exceptions_found, residual_limitation`. `REVIEWER_INDEPENDENCE_DISCLOSURE` requires `relationship_to_founder, financial_interest, prior_authoring` — genuine impartiality thinking consistent with ISO/IEC 17021-1:2015 cl. 5.2. `POST_MERGE_CUSTODY_RECEIPT` requires `merge_commit, protected_branch, post_merge_sha`. Each set is what that record type would actually need.

Uniform Scope Boundary and Prohibited Conclusions are correct — boundary language *should* be invariant. The residual is that **Collection Method is identical across all 19**, which is substantively wrong: collecting a sampling record is not the same activity as collecting an accession receipt. Same for Required Determinations and Completion Fields. This is nonblocking.

**P-07 — audit requirements matrix.** `required_evidence` is now **19 distinct after prefix-stripping** (was 1). Critically, the entries are keyed to the same per-template field lists, so matrix and templates are mutually consistent rather than independently invented.

**Adjudication on T1C-004** (`VALID_OPEN_RETAINED_PENDING_INDEPENDENT_DOC10_ADJUDICATION`, mapped from T1R2-EXT-F-02): **the underlying defect is remediated.** I recommend moving it to `REMEDIATED_PENDING_REREVIEW` with the three-section boilerplate residual recorded as a new nonblocking item. The package correctly declined to self-close this and routed it to independent adjudication — that is the right control behavior.

---

## 4. Doc03 — PARTIALLY SUFFICIENT. T1C-006 correctly stays open.

**What V4 genuinely did:** added `NON_REQUIREMENT_SOURCE_FRAGMENT_QUARANTINE.csv` and reclassified **51 of 96 rows** as `REJECTED_SOURCE_FRAGMENT_NOT_REQUIREMENT`. The quarantine carries per-row `source_path`, `source_locator` (line numbers), verbatim `fragment_text`, and `quarantine_reason`. Spot-checking confirms these are correctly rejected — JSON string literals (`"message": "User lacks required permissions."`) and markdown table rows (`Native iOS project | Missing | ...`) that were never requirements. **This is real analytic work, not uniquification.** It is the first per-row judgment applied to Doc03 in four rounds.

**What remains unremediated.** All ten ISO/IEC/IEEE 29148:2018 cl. 5.2.4 characteristic checks — `necessary`, `appropriate`, `unambiguous`, `complete`, `singular`, `feasible`, `verifiable`, `correct`, `conforming` — remain `NOT_PERFORMED` across **96/96** rows. Also `NOT_PERFORMED`/`NOT_ESTABLISHED`: `discovery_method`, `parent_requirement_id`, `bidirectional_trace_state`, `verified_coverage_state`, `verification_method`. Execution evidence is `NOT_EXECUTED` across all 96.

**Adjudication:** Doc03 is now an **honestly labeled quarantined candidate-fragment inventory**. It is **not** a requirements traceability register and cannot be accepted as satisfying ISO/IEC/IEEE 29148:2018 traceability or the bidirectional trace expectation in ISO/IEC/IEEE 15288:2015 cl. 6.4.3. The remaining 45 rows are correctly marked `NOT_ACCEPTED_AS_REQUIREMENT` — no overclaim anywhere. **P-01 / T1C-006 must stay open.** Retaining it as `VALID_OPEN_RETAINED` is correct.

---

## 5. NEW FINDING V4-01 (S2) — lifecycle rules are mechanically uniquified

**This is the one place V4 regressed to the program's historical failure pattern, and it passed validation because the control I recommended was gameable.**

`LIFECYCLE_TRANSITION_MATRIX.csv` reports 169 distinct values across all five rule columns (previously 1). Inspection shows distinctness is manufactured by prefixing the transition name to an invariant suffix:

```
CANDIDATE_TO_CANDIDATE_REVERSAL_REQUIRES_EXPLICIT_RESCISSION_OR_REMEDIATION_EVIDENCE
REMEDIATION_REQUIRED_TO_DRAFT_UNMERGED_REVERSAL_REQUIRES_EXPLICIT_RESCISSION_OR_REMEDIATION_EVIDENCE
SUSPENDED_TO_REMEDIATION_REQUIRED_REVERSAL_REQUIRES_EXPLICIT_RESCISSION_OR_REMEDIATION_EVIDENCE
```

Strip `{START}_TO_{END}_` and all 169 collapse to one string per column. This is structurally identical to the F-23 audit-matrix defect (`"Evidence specific to <NAME>:"` + constant) that this program has now committed three times.

It is also semantically vacuous in places: `CANDIDATE -> CANDIDATE` is marked `permitted=NO` yet still carries reversal, suspension, supersession, reactivation, and archival rules. A prohibited self-transition has no reversal semantics.

**I own part of this.** My recommended control — assert `distinct_values > 1` — is satisfied cosmetically by row-key interpolation. The package applied the stronger form correctly to the audit matrix (`distinct_audit_required_evidence_prefix_stripped`) but not to the lifecycle columns.

**Required fix:** extend prefix-stripped normalization to all five lifecycle rule columns, matching the audit-matrix check. Normalize by removing any leading substring derived from that row's own key values before counting distinct. Then author genuine per-transition rules, or collapse to a documented rule-class table where one rule legitimately governs many transitions — the latter is acceptable and honest.

---

## 6. Pending-remediated findings — which can be accepted

Eleven T1C items carry `REMEDIATED_IN_V3_PENDING_REREVIEW`. Against my V3 verification plus this round:

**ACCEPT (9).** Manifest-of-manifests reconstruction, negative-fixture execution, validator regression guards, register de-duplication, crosswalk population, T1C-004 honest reclassification, authority-label rescoping (170/170), thirteen-state vocabulary alignment (byte-identical packet/register), and evidence-custody integrity. Each was independently reverified this round; the V4 validator's 408 integrity checks pass with 0 failures.

**ACCEPT, newly evidenced this round (3 more).**
- **P-02** — packet consequence columns: 5 distinct of 5, and substantively decision-specific. FD-T1R2-003 correctly notes candidate-path rows still need row-level evidence; FD-T1R2-005 correctly refuses to authorize protected-branch merge. Genuine.
- **P-03** — findings register: `severity_rationale`, `impact`, `mitigation` at 8 distinct of 9; `root_cause` 9 of 9. Text is real per-finding reasoning ("S1 because an unverified candidate scrape can be mistaken for accepted requirements"). Genuine. Minor: one duplicate pair remains in three columns — the `>1` threshold masks it.
- **P-04 / P-07** — per §3.

**DO NOT ACCEPT (2).** T1C-009 and T1C-011 still carry the mismatched `source_review_ids` I raised as V3-02. The remediation content is fine; the citations point to the wrong findings. Correct the mapping before closure — otherwise a re-reviewer reconciling those rows will not find the claimed source.

**CORRECTLY RETAINED OPEN (9).** T1C-003, 006, 010, 013, 014, 016, 019 as `VALID_OPEN_RETAINED`; T1C-004 pending this adjudication; T1C-020 `RETAINED_NONBLOCKING_OPEN`. All nine are properly characterized. `second_reviewer_state = NOT_PERFORMED_NOT_FABRICATED` holds across all 20 rows — the package continues to refuse to fabricate an independent reviewer.

---

## 7. Required before next round

1. **V4-01 (S2)** — prefix-stripped normalization on all five lifecycle rule columns; then author real per-transition rules or a documented rule-class table.
2. **V3-02 carryover (S2)** — fix `source_review_ids` on T1C-009 and T1C-011.
3. **V4-02 (S3)** — legacy validator stubs should exit nonzero.
4. **Doc10 residual (S3)** — differentiate Collection Method, Required Determinations, Completion Fields per template.
5. **P-01 / T1C-006** — remains the largest open item; requires executing ISO/IEC/IEEE 29148:2018 cl. 5.2.4 characteristic checks on the 45 surviving candidates.

**Generalized control, restated correctly:** for every column intended to carry per-row analysis, assert `distinct(normalize(value)) > 1`, where `normalize` strips any substring derivable from that row's own key fields. The unnormalized form is the version V4 satisfied cosmetically.

---

## 8. Assessment

V4 is the strongest round in this program. The two hardest content defects — Doc10 templates and the audit matrix — are genuinely remediated after three rounds of superficial attempts, and Doc03 received its first real per-row analytic pass. The validator consolidation increased coverage rather than laundering it, the legacy stubs are honest about their own non-authority, and the structural result truthfully reports that substantive closure remains blocked. The package routed T1C-004 to independent adjudication instead of self-closing it.

The single significant lapse is V4-01, where the lifecycle columns were made to satisfy a distinct-value check without satisfying its intent. That is worth fixing precisely because everything around it was done properly.

`UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

### Primary sources
ISO/IEC/IEEE 29148:2018 (requirements characteristics, cl. 5.2.4) — https://www.iso.org/standard/72089.html · ISO/IEC/IEEE 15288:2015 (cl. 6.4.3) — https://www.iso.org/standard/63711.html · ISO/IEC/IEEE 15289:2019 — https://www.iso.org/standard/74909.html · ISO/IEC 17000:2020 cl. 4.4 (second-party conformity assessment) — https://www.iso.org/standard/68131.html · ISO/IEC 17021-1:2015 cl. 5.2 (impartiality) — https://www.iso.org/standard/61651.html · ISO 19011:2018 cl. 3.1 — https://www.iso.org/standard/70017.html · ISO/IEC 27001:2022 cl. 10.2 (nonconformity and corrective action) — https://www.iso.org/standard/27001 · ISO 15489-1:2016 (records management) — https://www.iso.org/standard/62542.html · NIST SP 800-53 Rev. 5 Release 5.2.0 — https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final · NIST CSF 2.0 GV.RR-01/GV.RR-02 — https://doi.org/10.6028/NIST.CSWP.29 · COSO ICIF 2013 Principles 3, 5, 16, 17 — https://www.coso.org/guidance-on-ic · SLSA v1.0 — https://slsa.dev/spec/v1.0/levels · EU Regulation 2024/1689 Arts. 11, 12, 17, 18 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj

*Documentary review only. Not adoption, activation, implementation authorization, production authorization, merge authorization, certification, or a legal compliance determination.*
