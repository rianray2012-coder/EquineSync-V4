# EquineSync Tier 1 Documents 03–10 — Consolidated Outside-Review Findings and Disposition Register

Date: 2026-08-04  
Status: `REVISION_REQUIRED`  
Authority boundary: `NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

## 1. Source reviews and version reconciliation

| Review | Reviewed target | Conclusion | Consolidation treatment |
| --- | --- | --- | --- |
| Claude | Received archive SHA-256 `909ba841a1b488ae61a370d74182a5841901a0b061accc568c3d609c3d8a4433`, 2,586,324 bytes; repository head not reviewed | `REVISION_REQUIRED` | Controlling for defects demonstrated in that archive; package-identity mismatch is independently blocking. |
| Perplexity | Later RR2/remediated documentary package described in the report | `READY_WITH_NONBLOCKING_REVISIONS` | Controls for standards benchmarking and evidence of later remediation; does not override unresolved defects found by the other reviewers. |
| Cursor | Repository commit `a1a1ff5cf056e7e78c99c4038fb8afcb95aebab7`; archive SHA-256 `aa61978cf952a6b93abcb20c009ce28d862734258e7aae7a4a2b12788563545f`, 2,545,176 bytes | `REVISION_REQUIRED` | Authenticated review baseline. Cursor expressly did not review later PR #83 tip `1c053c4a9658e5b47d0cbc0bbf4edf6a995a41e3`. |

The reports do not evaluate identical bytes. Accordingly, a finding is not closed merely because a later report describes a corrected state. The current PR tip and current packaged ZIP must first be authenticated, and each finding below must then be verified against that single target.

## 2. Consolidation rules

- Duplicate findings are merged by underlying control defect, not by wording.
- Severity uses the most protective supported classification.
- A conflicting reviewer conclusion becomes `VERIFY_CURRENT_TARGET`; it is not silently resolved in favor of readiness.
- “Already remediated” requires exact path/row evidence, a negative test where applicable, and updated manifests/checksums.
- External findings may not be self-closed without the designated Second Reviewer or the originating reviewer’s concurrence.
- Patrick K. Spoon Sr., COO, is the designated Second Reviewer for high-consequence governance actions, subject to conflict-of-interest and recusal rules.

## 3. Consolidated findings

| ID | Severity | Consolidated defect | Source findings | Disposition / required closure |
| --- | --- | --- | --- | --- |
| T1C-001 | BLOCKING | Review-target identity is inconsistent across the kit, archives, PR commits, and reports. | Claude R2-01; Cursor review identity; Perplexity package context | Authenticate one current PR commit and one generated ZIP; record SHA-256, byte length, manifest root, branch, PR, and supersession of all predecessor review targets. Stop on mismatch. |
| T1C-002 | BLOCKING | Founder decision FD-T1R2-001 may describe an thirteen-state vocabulary while the operative model contains thirteen states. | Claude R2-02; Cursor OR-010; Perplexity C-03/C-22 | Current-target verification. If present, correct every surface to thirteen and add a validator binding the decision text to the distinct-state count. |
| T1C-003 | BLOCKING | FD-T1R2-004 may ask for residual-risk disposition against an empty, incomplete, or already-remediated population. | Claude R2-03/R2-04; Cursor OR-005; Perplexity C-09/C-10 | Rebuild the decision population by row ID; preserve all external findings; distinguish finding, risk, exception, waiver, and accepted risk; do not imply acceptance where no Founder decision exists. |
| T1C-004 | BLOCKING | Document 10’s 19 closing-review templates are generic duplicates rather than purpose-specific instruments. | Cursor OR-001; Perplexity P-04/P-07/C-17/C-18; Claude’s control-quality discussion | Author purpose-specific fields, evidence requirements, exclusions, determinations, sign-off, validation rules, and prohibited conclusions for each instrument. Add normalized-content distinctness and required-field negative tests. |
| T1C-005 | BLOCKING | Source authority states may be elevated from filename/path keywords rather than authenticated approval, adoption, or lock evidence. Candidate paths may be labeled authoritative. | Cursor OR-002/OR-008; Perplexity P-06/C-14; Claude source-authority observations | Replace heuristic elevation with evidence-backed states containing locators/hashes; otherwise use documentary/context-only states. Forbid candidate-path authority unless explicit controlling evidence exists. |
| T1C-006 | BLOCKING | Document 03 includes fragments, headers, JSON, comments, and coding prompts as “atomic requirements”; coverage is computed over a low-quality candidate corpus. | Cursor OR-003/OR-012; Claude R2-08; Perplexity P-01/C-01/C-02 | Quarantine non-requirements, apply recorded ISO-style quality checks, require human acceptance for normative status, correct discovery method, and recompute all metrics from the accepted/candidate populations separately. |
| T1C-007 | HIGH | Independent findings were incompletely carried into Document 06 and may have been self-closed with boilerplate evidence and no second reviewer. | Claude R2-04/R2-05/R2-13; Perplexity C-25/C-31 | Create one authoritative findings population with source-ID crosswalk; assign per-finding status, blocking rationale, owner, next action, closure criteria, and evidence. Require Second Reviewer/originating-reviewer concurrence for closure. |
| T1C-008 | HIGH | Validator PASS is overstated: per-document checks may test presence only; advertised invalid-state, source, template, and decision controls are incomplete or unexercised. | Cursor OR-006/OR-011/OR-014; Claude R2-06/R2-07; Perplexity C-05 | Label structural checks truthfully; implement every advertised rule via explicit rule-to-function mapping; fail on unknown rules; add negative fixtures proving each control can fail. |
| T1C-009 | HIGH | Founder-decision fields and surfaces may imply a selected approval despite `NO_FOUNDER_DECISION_RECORDED`; generic consequences weaken decision quality. | Cursor OR-004/OR-017; Perplexity P-02/C-06/C-07/C-08; Claude R2-02/R2-03/R2-14 | Make CSV the source of truth; set all undecided dispositions to `NO_DISPOSITION_SELECTED`; generate prose from CSV; write decision-specific consequences and express authority not granted. |
| T1C-010 | HIGH | Evidence-state separation is incomplete where production/deployment evidence is claimed but not represented. | Cursor OR-007; Claude Document 03 assessment | Add explicit production/deployment evidence fields with non-observed defaults or narrow the narrative; validate that no evidence class is inferred from another. |
| T1C-011 | MEDIUM | Lifecycle vocabulary, transition history, and permitted transitions may conflict, including candidate supersession and rejection/resubmission. | Claude R2-09/R2-10; Cursor OR-010/OR-011; Perplexity P-05 | Reconcile all 13 states, actual supersession history, resubmission policy, and permitted transitions. Make every prohibited/permitted transition evidence- and authority-specific. |
| T1C-012 | MEDIUM | Source duplicate clusters may lack referential linkage in an earlier build; later report claims the linkage is repaired. | Cursor OR-009; Perplexity C-13 | `VERIFY_CURRENT_TARGET`: prove zero orphan cluster references and dashboard arithmetic from the current register; retain a failing orphan fixture. |
| T1C-013 | MEDIUM | Workstream/PR disposition data may be stale, self-referential, un-timestamped, or omit carrier PR #83; CI data may be opaque JSON in CSV. | Cursor OR-013; Claude R2-12/R2-16; Perplexity C-15/C-16 | Capture `as_of_utc` and base SHA, include or expressly scope out PR #83, refresh heads, normalize CI fields, qualify behind/drifted mergeability, and validate failures. |
| T1C-014 | MEDIUM | Boilerplate appears in findings rationale, consequences, lifecycle rule columns, audit evidence, unresolved issues, ownership deadlines, and remediation sections. | Claude R2-11/R2-13/R2-17; Cursor OR-005/OR-016; Perplexity P-02/P-03/P-05/P-07/P-08 | Replace with record-specific content or reference a single controlled rule where uniformity is intentional. Add duplicate-section/idempotence checks. |
| T1C-015 | MEDIUM | Certification/audit/attestation terminology may overstate documentary status in earlier builds. | Cursor OR-015; Perplexity C-24 and legal-terminology caution | `VERIFY_CURRENT_TARGET`: retain self-declaration/documentary-review wording and forbidden-term checks; do not claim certification, legal compliance, or third-party attestation. |
| T1C-016 | MEDIUM | Principal Documents 03–10 are thin pointer narratives and do not adequately explain their registers or controlled vocabularies. | Cursor OR-016; Perplexity P-08/C-26 | Expand each document with purpose, scope, definitions, controlled vocabularies, use instructions, acceptance criteria, edge cases, dependencies, and register-backed examples. |
| T1C-017 | LOW | Manifest/bootstrap exclusions and archive custody are incompletely disclosed or externally bound. | Claude R2-19; Cursor OR-018/OR-019; Perplexity C-19/C-20 | Enumerate every unbound artifact; bind all non-self-referential manifests; publish detached ZIP checksum and custody record. |
| T1C-018 | LOW | Source rows labeled “authoritative current” may lack declared versions; `implementation_use` wording invites unsafe filtering. | Claude R2-15/R2-18 | Flag unversioned-authoritative overlaps; require canonical evidence; rename to `permitted_use_class` or prefix every value with `NOT_SAFE_FOR_IMPLEMENTATION`. |
| T1C-019 | LOW | Ownership vacancies are honestly disclosed but function-specific deadlines, escalation, succession, and independence controls remain weak. | Claude R2-17; Cursor OR-020; Perplexity C-11/C-12 | Preserve vacancy honesty; differentiate criticality/deadlines; record Patrick K. Spoon Sr. only through an authorized appointment record; preserve recusal and unavailable-independence states. |
| T1C-020 | LOW | Validation is single-platform in the reviewed later package. | Perplexity P-09/C-21 | Add an independent Linux/CI reproduction record with the same authenticated target and compare results. |

## 4. Conflict resolutions

1. **Overall readiness:** `REVISION_REQUIRED` controls. Two reviewers reached that conclusion and identified defects affecting decision validity, authority classification, and substantive fitness.
2. **Templates:** Perplexity called the substantive template defect nonblocking for boundary safety; Cursor called it blocking for Document 10 fitness. It is classified BLOCKING because Documents 03–10 are being evaluated for finalization, not merely containment of authority overclaim.
3. **Validator coverage:** Perplexity reported a later build with 12 implemented predicates; Cursor and Claude found earlier/incomplete or unexercised controls. Closure requires negative-fixture proof on the authenticated current target.
4. **Duplicate-cluster linkage:** Cursor found empty foreign keys; Perplexity found complete linkage in a later build. This is `VERIFY_CURRENT_TARGET`, not an unresolved factual contradiction.
5. **Founder decisions:** Later evidence may show `NO_DISPOSITION_SELECTED`; earlier evidence shows stronger language. All current surfaces must be generated from one authoritative register and tested for consistency.

## 5. Exit criteria

The package may return for Founder documentary review only when:

1. T1C-001 through T1C-010 are closed with exact evidence and independent review.
2. Every remaining item has a truthful disposition, owner, due date, and nonblocking rationale.
3. All machine checks pass in repository and extracted-package modes, including negative fixtures.
4. A fresh independent rereview confirms the remediated current target; this is a bounded closure rereview, not an automatic new full review cycle.
5. Founder decision surfaces contain no preselected outcome and create no adoption, activation, merge, implementation, production, or certification authority.
