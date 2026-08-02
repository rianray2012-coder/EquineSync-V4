# EquineSync Tier 1 RR2 — Cursor Outside Review Findings

| Field | Value |
|---|---|
| Review type | Independent Cursor outside documentary review of Second Draft reviewer package |
| Reviewer | Cursor Cloud Agent (`cursor-grok-4.5-high`) |
| Review date | 2026-08-02 |
| Package ZIP SHA-256 | `909ba841a1b488ae61a370d74182a5841901a0b061accc568c3d609c3d8a4433` — **VERIFIED** against sidecar |
| Package size | 2,586,324 bytes |
| Independent package-only validator | `PASS`, failures `0` (212 checks) — see `INDEPENDENT_VALIDATION_RERUN.json` |
| Prior external review | Perplexity standards benchmark (F-01…F-28) embedded in package `EXTERNAL_REVIEW/` |
| Package claim | Blocking minimum F-01–F-07, F-10, F-15 remediated |

**Authority boundary of this review.** Documentary only. No adoption, activation, implementation, production, merge, or certification authority is created or implied.

---

## 1. Executive Conclusion

The Second Draft is a **material improvement** over the first external-review target on several previously blocking defects: requirement rows are retagged as `SOURCE_TEXT_CANDIDATE`; Founder dispositions are uniformly `NO_DISPOSITION_SELECTED`; invalid-state rules are failure-capable and mutation-tested for at least RULE-01; source duplicate FKs are populated; lifecycle vocabulary now includes `REJECTED` / `REMEDIATION_REQUIRED` / `DRAFT_UNMERGED` / `BLOCKED_EVIDENCE_REQUIRED`; coverage metrics publish `verified_coverage = 0.0`; and the package-only validator re-run on these exact bytes passes.

It is **not** yet an honest remediation of F-02, and several other remediations are thin, self-satisfying, or internally inconsistent.

The single highest-severity residual is that Document 10 still ships **19 byte-identical templates** once the H1 title and `Template name:` line are excluded. The package marks F-02 `REMEDIATED`, and the validator only checks that template *names* are unique. That is the same class of defect the first external review called material: a control asserted as remediated while the underlying instrument set remains a single file with renamed titles.

Second-order residuals that block safe Founder directional review of FD-T1R2-001 and of the remediation narrative:

- FD-T1R2-001 still asks Founder to approve an **eleven-state** vocabulary while the shared standard and matrix are **13-state**.
- Per-document validators/tests restored for F-16 are presence stubs (artifact-count / subprocess smoke), not document-specific controls.
- Invented ownership appointments do not fail any ownership semantic check; only checksum/manifest integrity fails if bytes change.
- Findings register rows remain largely boilerplate across severity rationale / impact / mitigation.
- `FOUNDER_APPROVAL_EVIDENCE_PRESENT` remains on 170 source rows after F-20 “relabelling.”
- PR #83 body still declares archive SHA `aa61978c…` while the branch ZIP bytes are `909ba841…`.

**Final disposition: `REVISION_REQUIRED`.**

---

## 2. What Improved (Independent Confirmation)

| Prior finding | Second Draft observation | Confirmed? |
|---|---|---|
| F-01 normative requirements | 96/96 `SOURCE_TEXT_CANDIDATE`; `source_text_candidate_state=NOT_ACCEPTED_AS_REQUIREMENT`; `verification_method=NOT_PERFORMED` | YES |
| F-03 non-failing checks | Mutation of disposition and ACTIVE+NOT_ADOPTED produced `FAIL` with failure-capable checks | YES (for tested paths) |
| F-04 unimplemented invalid rules | All 12 rules marked `ENFORCED_BY_VALIDATOR` / `failure_capable=YES`; RULE-01 failed under mutation | YES |
| F-07 off-enum dispositions | All five `NO_DISPOSITION_SELECTED`; `authority_granted=NONE_BY_THIS_PACKAGE` | YES |
| F-08/F-09 recommendations & question drift | `recommended_option=NO_RECOMMENDATION_SELECTED`; packet/register questions match each other | PARTIAL — both still say “eleven-state” while model is 13-state |
| F-10 blank duplicate FK | 0 blank; 2816 `NO_DUPLICATE_CLUSTER`; cluster FKs resolve | YES |
| F-11 dashboard arithmetic | `exact_duplicate_clusters=68`, `redundant_exact_duplicate_copies=77`, `unique_source_identities=2884` | YES |
| F-14 test_id overclaim | `test_id` empty where assertion not verified | YES |
| F-15 no reject/remediation states | 13 states, 169 matrix rows, permitted reject/remediation exits from `FOUNDER_REVIEW_READY` | YES |
| F-19 divergent versions on byte-identical clusters | 0 residual clusters found | YES |
| Integrity checksums | Independent re-hash of all `CHECKSUMS.sha256` entries: 221 OK / 0 FAIL | YES |

---

## 3. Severity-Ranked Findings (Cursor Outside Review)

Severity: **S1** material — undermines remediation or assurance claims; **S2** significant contradiction / unsupported inference; **S3** moderate defensibility weakness; **S4** minor clarity.

### S1 — Material

#### C-OR-01 · F-02 remediation is false: 19 templates remain one file under title/name normalization

**Artifacts:** `10_CLOSING_AUDIT_PROTOCOL/templates/*.md`; `EXTERNAL_REVIEW/EXTERNAL_REVIEW_FINDING_DISPOSITION_REGISTER.csv` row F-02 (`REMEDIATED`); validator check `review_template_count_and_distinct_names`.

**Evidence:** Normalised hashing that excludes only the H1 title line and the `Template name:` line collapses **19/19** templates to one SHA-256 prefix `6b48ae34e0f59f08`. Section headers are identical across all 19 (`Document Control` … `Sign-Off Fields`). A Reopening Notice and an Internal Documentary Review Plan differ only by display name.

**Effect:** Document 10 still does not deliver distinct closing instruments. The disposition register overstates remediation. The validator cannot detect this class of regression because it checks name uniqueness only.

**Minimal correction:** Author purpose-specific required fields per template (or reduce to the number of genuinely distinct instruments), and add a validator check that normalised template bodies are not identical.

---

### S2 — Significant

#### C-OR-02 · FD-T1R2-001 asks for an eleven-state vocabulary; package defines thirteen states

**Artifacts:** `FOUNDER_DECISION_PACKET.md` / `.csv`; `05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv`; `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md`; `LIFECYCLE_TRANSITION_MATRIX.csv` (13 states / 169 rows).

**Evidence:** Decision text: “approve the **eleven-state** lifecycle vocabulary…”. Shared standard enumerates 13 states including `REMEDIATION_REQUIRED` and `REJECTED` added to remediate F-15. Validator enforces `states=13`.

**Effect:** Founder cannot safely answer FD-001 as written. Approving “eleven-state” would contradict the remediated model; approving the actual model would answer a different question than the instruments record.

**Minimal correction:** Make question text byte-identical to the live vocabulary count and enumerate the states, or freeze the model back to eleven with an explicit delta — do not leave both.

#### C-OR-03 · Per-document validators/tests are presence stubs (F-16 thinly closed)

**Artifacts:** `0N_*/validators/validate_document_0N_rr2.py`; `0N_*/tests/test_document_0N_rr2_validator.py`; validator check `per_document_validator_test:*`.

**Evidence:** Each per-doc validator only lists `*.csv|*.json|*.md` in the document directory and exits 0 if any exist. Tests only assert the subprocess exit code is 0. Package validator only checks that the files exist.

**Effect:** Round 2 claims restoration of per-document validation capability, but the restored artifacts cannot detect document-local schema, enum, or referential defects.

**Minimal correction:** Either implement document-specific assertions, or relabel these artifacts as `PRESENCE_SMOKE_ONLY` and stop counting them as remediation of F-16.

#### C-OR-04 · Ownership semantic checks do not detect invented appointments

**Artifacts:** `VALIDATION/validate_tier1_documents_03_10_rr2.py` (`ownership_gap_effect_present`, `review_calendar_not_operative_pending_appointment`); `07_OWNERSHIP_STEWARDSHIP_REVIEW/*`.

**Evidence:** Mutation set `accountable_function` / `appointment_evidence` / vacancy state to invented filled values. Ownership semantic checks still `PASS`. Failures observed were checksum/manifest integrity only.

**Effect:** The package can represent appointed ownership without Founder evidence and still pass semantic ownership validation after manifests are regenerated.

**Minimal correction:** Fail when appointment/acceptance evidence is non-`NOT_RECORDED` absent a Founder decision row with authority, or require vacancy_state to remain vacant while package authority is `NOT_ADOPTED`.

#### C-OR-05 · Findings register remains mostly boilerplate (F-12 partial)

**Artifacts:** `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv` (9 rows).

**Evidence:** `severity_rationale`, `impact`, `mitigation`, and `affected_actors` are identical across all 9 rows. Differentiation is limited to `record_id`, `affected_requirement_or_control`, `severity`, and short `root_cause` strings. Closure evidence is the same generic sentence for every row.

**Effect:** Register now has root_cause fields (good), but still does not contain independently usable finding narratives.

**Minimal correction:** Write finding-specific impact/rationale/mitigation/closure locators (file + row + hash), or mark rows as `REMEDIATION_TRACKING_SUMMARY` rather than closed findings.

---

### S3 — Moderate

#### C-OR-06 · `FOUNDER_APPROVAL_EVIDENCE_PRESENT` label retained on 170 source rows (F-20 incomplete)

**Artifact:** `08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` `authority_state` counts.

**Evidence:** Adoption label was renamed to `SOURCE_CONTAINS_ADOPTION_OR_LOCK_EVIDENCE_NOT_PACKAGE_ADOPTION` (598). `FOUNDER_APPROVAL_EVIDENCE_PRESENT` remains 170. Validator only bans the old adoption token.

**Minimal correction:** Rename to a historical/observed token and extend the validator denylist.

#### C-OR-07 · Inventory readiness token lags package determination

**Artifacts:** `TIER_1_DOCUMENT_INVENTORY.csv` vs `README_FIRST.md` / root `PACKAGE_MANIFEST.json`.

**Evidence:** Inventory readiness = `REVISION_ROUND_2_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW` for all 8 docs. README/manifest determination = `REVISION_ROUND_2_EXTERNAL_REVIEW_REMEDIATED_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW`.

**Minimal correction:** Align inventory tokens to the package determination or record an explicit supersession note per row.

#### C-OR-08 · Unresolved-issue register conflates remediated and open items

**Artifact:** `UNRESOLVED_ISSUE_REGISTER.csv` (28 rows).

**Evidence:** Every external finding F-01…F-28 is classified `REMEDIATED_OR_TRACKED_PER_EXTERNAL_REVIEW_DISPOSITION_REGISTER`, including items the disposition register marks `REMEDIATED` and items marked `TRACKED_NONBLOCKING`. A remediated item is not an unresolved issue.

**Minimal correction:** Split into remediations-complete vs still-open POA&M rows; keep only open/tracked items in the unresolved register.

#### C-OR-09 · PR #83 body archive SHA does not match branch ZIP bytes

**Artifacts:** PR #83 body (`aa61978cf952a6b93abcb20c009ce28d862734258e7aae7a4a2b12788563545f`); branch file `governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V1.zip` SHA `909ba841…`.

**Evidence:** `git show origin/codex/tier-1-documents-03-10-revision-round-2:...V1.zip | sha256sum` = `909ba841…`, matching the uploaded Second Draft.

**Minimal correction:** Update PR authentication section to the live archive hash/byte length, or attach a successor PR for the remediated archive.

#### C-OR-10 · Manifest-of-manifests intentionally excludes root integrity files; outer ZIP still not self-authenticated inside package

**Artifacts:** `MANIFEST_OF_MANIFESTS.csv`; root `PACKAGE_MANIFEST.json` `root_manifest_binding_limitation`; `00_PROGRAM_CONTROL/ROUND_2_PACKAGE_ZIP_RECORD.json`.

**Evidence:** Limitation is disclosed (good). Residual risk from F-05/F-28 remains: final archive authenticity depends on external hash (this review used the upload sidecar). Tracked, not newly introduced.

**Minimal correction:** Keep as tracked non-blocking with Founder-visible limitation; publish sidecar hash beside every distribution copy (already done for this upload).

#### C-OR-11 · `discovery_method` remains `NOT_PERFORMED` for all 96 candidates

**Artifact:** `03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv`.

**Evidence:** F-01 remediation retagged types and added 29148 check columns (all `NOT_PERFORMED`), but did not record the actual discovery method previously criticized (“keyword scan”).

**Minimal correction:** Populate `discovery_method` with the true method and keep `verification_method=NOT_PERFORMED`.

---

### S4 — Minor

#### C-OR-12 · Delta report repeats the External Review Remediation Delta heading three times

**Artifact:** `REVISION_ROUND_2_DELTA_REPORT.md`.

#### C-OR-13 · Validation remains single-host / unsigned (F-28 tracked)

**Evidence:** Embedded validation reports are macOS/Python 3.14.6; this review re-ran on Linux in cloud and also `PASS`. Still no signature/container digest. Agree with tracked non-blocking disposition.

---

## 4. Remediation Claim Audit (F-01…F-28)

| ID | Package disposition | Cursor confirmation | Notes |
|---|---|---|---|
| F-01 | REMEDIATED | CONFIRM | Type retag holds |
| F-02 | REMEDIATED | **REJECT** | See C-OR-01 |
| F-03 | REMEDIATED | CONFIRM | Failure-capable paths observed |
| F-04 | REMEDIATED | CONFIRM | Rules enforced under mutation for tested rule |
| F-05 | REMEDIATED_WITH_…_LIMITATION | CONFIRM_WITH_LIMITATION | C-OR-10 |
| F-06 | REMEDIATED_WITH_…_DISCLOSURE | CONFIRM_WITH_LIMITATION | Reports regenerated; still first-party |
| F-07 | REMEDIATED | CONFIRM | |
| F-08 | REMEDIATED | CONFIRM | |
| F-09 | REMEDIATED | PARTIAL | Questions aligned to each other but stale vs 13-state model (C-OR-02) |
| F-10 | REMEDIATED | CONFIRM | |
| F-11 | REMEDIATED | CONFIRM | |
| F-12 | REMEDIATED | PARTIAL | C-OR-05 |
| F-13 | REMEDIATED | CONFIRM | coverage metrics rewritten |
| F-14 | REMEDIATED | CONFIRM | |
| F-15 | REMEDIATED | CONFIRM | introduces C-OR-02 inconsistency |
| F-16 | REMEDIATED | **REJECT / THIN** | C-OR-03 |
| F-17 | REMEDIATED | CONFIRM | confidence `NOT_SCORED` |
| F-18 | TRACKED_NONBLOCKING | AGREE | still undeclared versions |
| F-19 | TRACKED_NONBLOCKING | CONFIRM_FIXED_OR_ABSENT | 0 divergent clusters found now |
| F-20 | REMEDIATED_BY_RELABELLING | PARTIAL | C-OR-06 |
| F-21 | REMEDIATED | CONFIRM | calendar `NOT_OPERATIVE_PENDING_APPOINTMENT` |
| F-22 | REMEDIATED | PARTIAL | count expanded but conflated (C-OR-08) |
| F-23 | REMEDIATED | PARTIAL | matrix text may differ; templates still structurally identical |
| F-24 | REMEDIATED | CONFIRM | packet consequences no longer pre-recommend options |
| F-25 | REMEDIATED | CONFIRM | review_thread_state / ci_failure_analysis populated |
| F-26 | REMEDIATED_AS_NOT_ESTABLISHED_FIELDS | CONFIRM | fields present as NOT_ESTABLISHED |
| F-27 | REMEDIATED | CONFIRM_PARTIAL | narratives improved; still thin |
| F-28 | TRACKED_NONBLOCKING | AGREE | C-OR-13 |

---

## 5. Founder Decision Readiness

| Decision | Safe to present now? | Blocker |
|---|---|---|
| FD-T1R2-001 | **NO** | C-OR-02 eleven vs thirteen |
| FD-T1R2-002 | YES, as vacancy acknowledgement only | C-OR-04 weakens future appointment evidence |
| FD-T1R2-003 | YES, as directional frame only | none material from this review |
| FD-T1R2-004 | **NO** until findings narratives are real | C-OR-05 |
| FD-T1R2-005 | YES, as non-authorizing sequencing frame | none material |

---

## 6. Recommended Blocking Minimum Before Next Founder Pass

1. Fix C-OR-01 (distinct templates + validator normalised-body check).
2. Fix C-OR-02 (FD-001 question ↔ 13-state vocabulary).
3. Fix or honestly downgrade C-OR-03 (per-doc validators).
4. Update PR #83 authentication SHA to `909ba841…` (C-OR-09).
5. Re-run package-only and repository-aware validators; replace validation evidence; refresh manifests/checksums/MoM.

Non-blocking but should remain visible: C-OR-04…C-OR-08, C-OR-10, C-OR-11, C-OR-12, C-OR-13.

---

## 7. Final Disposition

`REVISION_REQUIRED`

Rationale: one previously material finding (F-02) remains unremediated despite a `REMEDIATED` disposition; Founder decision FD-001 is not decision-ready; restored per-document validation is not substantive. The broader Round 2 architecture and authority-boundary discipline remain defensible and improved.
