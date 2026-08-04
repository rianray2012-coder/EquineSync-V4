# EquineSync Tier 1 Documents 03–10 — V2 Remediation Candidate Review

**Package:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V2_OUTSIDE_REVIEW_REMEDIATION_CANDIDATE`
**Reviewed:** 2026-08-04 (America/Chicago)
**Baseline:** V1 package + my Round-2 outside review (findings P-01…P-09 + FD-001 consistency item)
**Reviewer:** Perplexity Computer — machine-assisted independent documentary review. Not an accredited certification body under ISO/IEC 17021-1:2015, not a licensed CPA firm, not a third-party conformity assessment body. Second-party documentary review under ISO/IEC 17000:2020 cl. 4.4; not an audit under ISO 19011:2018 cl. 3.1.

**Authority boundary preserved and not displaced by this review:**
`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

## Disposition

**`REVISION_REQUIRED`**

This agrees with the package's own self-declared status (`REVISION_REQUIRED_PENDING_BOUNDED_INDEPENDENT_CLOSURE_REREVIEW`), but for a materially different and more serious reason than the package records: **V2 introduces a regression that breaks the package integrity chain**, and the new V2 validator does not detect it.

V2 moved **forward on honesty** and **backward on integrity**.

---

## What V2 genuinely improved

These are real and should be retained.

1. **No self-closure.** All 20 consolidated findings in `OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv` are `OPEN_PENDING_SECOND_REVIEW` (19) or `RETAINED_NONBLOCKING` (1). The package does not close its own findings. This is correct behaviour under ISO/IEC 27001:2022 cl. 10.2.
2. **Refusal to fabricate the second reviewer.** All 20 rows carry `second_reviewer_state = NOT_PERFORMED_NOT_FABRICATED`, and T1C-019 explicitly records that no Patrick K. Spoon Sr. review or appointment was fabricated. This is the single best judgement call in V2.
3. **Honest self-declared disposition.** `PACKAGE_STATUS = REVISION_REQUIRED_PENDING_BOUNDED_INDEPENDENT_CLOSURE_REREVIEW`, and the validator emits `STRUCTURAL_PASS_SUBSTANTIVE_CONTROL_BLOCKED` rather than a bare `PASS`. Separating structural conformance from substantive closure is conceptually the right control.
4. **Authenticated custody record.** `00_PROGRAM_CONTROL/AUTHENTICATED_REPOSITORY_AND_PACKAGE_CUSTODY_RECORD_V2.json` carries real commit SHAs (PR #83 head `1c053c4a…`, base `1eb384d8…`), archive SHA-256, byte lengths, and a predecessor/successor table including the Cursor-reviewed `a1a1ff5c…`. This addresses review-target identity ambiguity.
5. **Two-reviewer consolidation.** 20 T1C findings with 20 distinct defect statements and 20 distinct evidence statements — genuine synthesis of my review and the Claude review, not a copy-paste.
6. **Linux/CI limitation recorded honestly** as `NOT_AVAILABLE_RETAINED_NONBLOCKING` rather than claimed.

---

## New defects introduced by V2

### N-01 — Manifest-of-manifests regression breaks the integrity chain (S1, blocking)

This is a regression of prior-round blocking finding F-05, which had been remediated in V1.

| | V1 | V2 |
|---|---|---|
| `MANIFEST_OF_MANIFESTS.csv` rows | 18 | 168 |
| Rows that are per-directory manifests/checksums | **18 of 18** | **0 of 168** |
| Path set | the 18 manifest/checksum files | **exact duplicate of `PACKAGE_MANIFEST.json`** |
| Includes itself | no (deliberately excluded, rationale disclosed) | **yes, with a stale hash** |
| Files covered by neither manifest | 2 (root manifest + root checksum) | **21** |

The file no longer performs its function. It is now a byte-for-byte duplicate of the package manifest's path set, so the 21 per-directory `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256` files, plus the root manifest and root checksum, are authenticated by nothing. It also lists itself with a hash that does not match its own current content.

**Direct evidence:** running the substantive V1 validator against the V2 package returns `status: FAIL`, 3 failures:
- `manifest_integrity:MANIFEST_OF_MANIFESTS.csv` — hash/byte check
- `manifest_of_manifests_excludes_root_self_references`
- `manifest_of_manifests:MANIFEST_OF_MANIFESTS.csv` — manifest/checksum binding

**Standard:** [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §5.2.2 authenticity, §5.2.4 integrity; [ISO 14721:2012 OAIS](https://www.iso.org/standard/57284.html) fixity information; [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) PS.3.

**Fix:** restore the V1 generation logic — `MANIFEST_OF_MANIFESTS.csv` must contain exactly the per-directory manifest and checksum files (now 21 of them, since `00_PROGRAM_CONTROL/` and `OUTSIDE_REVIEW/` were added), must exclude itself and the two root files, and must be regenerated after all other files are written.

### N-02 — Negative fixtures are inert (S1)

`VALIDATION/FIXTURES/negative/` contains 12 fixtures. **Eleven are referenced by zero Python files.** The twelfth (`decision_text_lifecycle_count_mismatch.json`) is referenced only in a file-existence check — the validator confirms the file is present, never loads or evaluates it.

A negative fixture that is never fed to the validator proves nothing. T1C-008 ("Validator PASS may be overstated") is therefore addressed by adding files that cannot demonstrate detection capability. This repeats the exact superficiality pattern of F-02/P-04.

**Standard:** [NIST SP 800-53A Rev.5](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4 — assessment procedures must produce a determination supported by evidence.

**Fix:** add a fixture-execution harness that loads each negative fixture, runs the relevant validator predicate against it, and asserts `FAIL`. Record the results in the validation report.

### N-03 — The V2 validator is far weaker than the validator it sits alongside (S2)

`validate_tier1_documents_03_10_v2.py` runs 11 checks (7 file-existence + 4 register conditions). `validate_tier1_documents_03_10_rr2.py` runs 212 checks including full manifest integrity. The V2 validator does **not** check manifest integrity at all, which is precisely why N-01 ships undetected: the new validator reports structural pass while the substantive validator reports FAIL.

**Fix:** the V2 validator should invoke or subsume the RR2 validator rather than run beside it, so that `STRUCTURAL_PASS` cannot be emitted while integrity checks fail.

### N-04 — `PER_FINDING_CLOSURE_EVIDENCE_REGISTER.csv` is a byte-identical duplicate (S2)

Both `OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv` and `OUTSIDE_REVIEW/PER_FINDING_CLOSURE_EVIDENCE_REGISTER.csv` hash to `0ec36b40bf6fab8eed4bf2d524682b324bcf9d4e48a7156bd65cec7f198e267b`. Two manifest entries, one file's content. The delta report lists them as separate deliverables ("T1C disposition and per-finding closure evidence registers").

**Fix:** either delete one, or make the closure-evidence register carry what its name promises — per-finding evidence locators (file path, row ID, SHA-256, line reference) rather than a copy of the disposition summary.

### N-05 — Source-review crosswalk is not actually populated (S2)

The `source_review_ids` column is intended to trace each T1C finding back to the reviewer(s) who raised it. All 20 rows contain the same string: `"see consolidated outside-review register source findings column"`. Traceability from my P-01…P-09 and the Claude findings into the T1C numbering is therefore not machine-checkable, and cannot be verified without manual prose reading.

**Fix:** populate with actual identifiers, e.g. `PPLX-P-04;CLAUDE-F-11`.

### N-06 — T1C-004 records a factually incorrect remediation claim (S2)

T1C-004 (`Document 10 templates may be generic duplicates`) is dispositioned `PARTIALLY_REMEDIATED` with the evidence statement: *"V1 contains purpose-specific templates from prior remediation."*

This is not correct. Independently verified in the V2 package: `10_CLOSING_AUDIT_PROTOCOL/templates/` contains 19 files, **every one exactly 43 lines**, and after stripping the title line and the `Template name:` line there is **1 distinct normalized body across all 19**. `03_SOURCE_MANIFEST.md` and `05_SAMPLING_RECORD.md` carry identical prompts under identical headings. The templates were renamed (`01_`…`19_` with purpose-specific filenames and distinct heading text), which is a presentational improvement, but the required fields are unchanged generic prose.

**Fix:** correct the evidence text and reclassify to `NOT_REMEDIATED`.

### N-07 — Data dictionaries are 100% trivially auto-generated (S3)

22 data dictionaries were added covering 338 field rows. In **338 of 338 rows (100%)**, the `definition` column is the field name with underscores replaced by spaces — e.g. field `permitted_starting_state` is defined as "permitted starting state"; field `permitted` is defined as "permitted". Six of eleven columns (`data_type`, `required_or_optional`, `permitted_values`, `null_treatment`, `source_of_truth`, `validation_rule`, `prohibited_use`, `relationship_to_other_registers`) hold a single distinct value per file.

The accompanying 22 JSON schemas declare every field as `{"type": "string"}` with `additionalProperties: true`, so they constrain nothing beyond column presence.

This gives partial credit against P-08 (thin narratives) in form but not in substance.

**Fix:** author real definitions and permitted-value enumerations for the controlled-vocabulary fields at minimum (`authority_state`, `closure_state`, `permitted`, `requirement_type`, `severity`, `record_classification`, `merge_authority_state`). Set `additionalProperties: false` and add `enum` constraints where a controlled vocabulary exists.

### N-08 — Dictionary and schema coverage is partial (S3)

22 data dictionaries and 22 schemas against 46 CSV registers on disk. The uncovered registers include several that carry controlled vocabularies.

---

## Status of my original nine findings

| Finding | V1 status | V2 status | Evidence |
|---|---|---|---|
| **P-01** `discovery_method=NOT_PERFORMED` misrepresents keyword-scan origin | Open | **Unchanged** | 96/96 rows still `NOT_PERFORMED`; no rubric column added |
| **P-02** Packet consequence columns are boilerplate | Open | **Unchanged** | All 4 `consequence_if_*` columns still 1 distinct value across 5 decisions |
| **P-03** Findings rationale/impact/mitigation boilerplate | Open | **Unchanged** | `severity_rationale`, `impact`, `mitigation` each still 1 distinct across 9 rows. (`root_cause` is 9 distinct — that was already satisfactory in V1) |
| **P-04** 19 templates structurally identical | Open | **Unchanged** | 19 files, all 43 lines, 1 distinct normalized body. Renamed only. See N-06 |
| **P-05** Lifecycle rule columns boilerplate | Open | **Unchanged** | All 5 rule columns still 1 distinct across 169 rows |
| **P-06** `FOUNDER_APPROVAL_EVIDENCE_PRESENT` lacks boundary suffix | Open | **Unchanged** | Still present on 170 rows; the paired label remains correctly suffixed |
| **P-07** Audit matrix distinct-count superficial | Open | **Unchanged** | 19 distinct raw strings, **1 distinct** after stripping the `"Evidence specific to <NAME>:"` prefix |
| **P-08** Principal doc narratives thin | Open | **Partially addressed** | Pointer files still 7–19 lines. Data dictionaries added but trivially generated — see N-07 |
| **P-09** Single-platform validation | Open (disclosed) | **Unchanged, honestly recorded** | `LINUX_CI_REPRODUCTION_RECORD.md` records `NOT_AVAILABLE_RETAINED_NONBLOCKING`. Appropriate handling |
| **FD-001** "eleven-state" vs 13-state matrix | Open | **Unchanged in operative registers** | `FOUNDER_DECISION_PACKET.csv` and `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` both still read "eleven-state"; the lifecycle matrix has 13 states. Now tracked as T1C-002, and a negative fixture is named for it, but the text was not corrected |

**Zero of the ten content items were substantively fixed.** V2 re-registered them as open findings rather than remediating them. That is defensible as a deliberate strategy — the package explicitly declines to self-close — but it means the revision work itself is still entirely outstanding.

---

## What still needs to be revised

**Blocking, must fix before any further review cycle:**

1. **Regenerate `MANIFEST_OF_MANIFESTS.csv`** to cover the 21 per-directory manifest/checksum files, exclude itself and the two root files, and regenerate last (N-01).
2. **Re-run the RR2 validator and ship a passing report**, or ship the failing report with the failure disclosed. Currently the package ships a `PASS` report generated against V1 bytes alongside V2 bytes that fail (N-01, N-03).
3. **Wire the negative fixtures into an execution harness** so each one is proven to trigger a `FAIL` (N-02).
4. **Merge the two validators** so structural pass cannot be reported while integrity checks fail (N-03).

**High priority:**

5. Correct the T1C-004 evidence statement and reclassify to `NOT_REMEDIATED` (N-06).
6. Populate `source_review_ids` with real reviewer/finding identifiers (N-05).
7. Resolve the duplicate closure-evidence register (N-04).
8. Correct "eleven-state" to "thirteen-state" in `FOUNDER_DECISION_PACKET.csv` and `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` (FD-001 / T1C-002). This is a two-cell edit.

**Content work still outstanding from Round 2 (unchanged):**

9. P-01 — set `discovery_method = KEYWORD_SCAN` and add a rubric.
10. P-02 — author per-decision consequence text for all five Founder decisions. Bounded language was supplied in Section 5 of my Round-2 review and can be pasted directly.
11. P-03 — author per-finding `severity_rationale`, `impact`, `mitigation`.
12. P-04 — author purpose-specific required fields for each of the 19 templates. A `SOURCE_MANIFEST` needs source_id / controlling_version / sha256 / byte_length / custody; a `SAMPLING_RECORD` needs population_definition / sample_size / sample_method / results / disposition. This remains the largest single item.
13. P-05 — collapse the five lifecycle rule columns to a single `rule_reference`, or populate per-transition.
14. P-06 — relabel to `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION`.
15. P-07 — author per-area required evidence, derived from the P-04 template fields once those exist.
16. N-07 — author real field definitions and enum constraints for controlled-vocabulary fields.

**Recommended sequencing:** items 1–4 first (they are mechanical and restore the integrity baseline), then 5–8 (small text corrections), then 9–11 and 14 (single-pass register edits), then 12 and 15–16 (the substantial authoring work), then 13.

---

## Observation on the pattern

Three separate remediation attempts have now produced the same signature: a defect is closed by adding *artifacts that are shaped like* the fix rather than by authoring the content the fix requires.

- F-02 → 19 templates with distinct hashes but identical bodies
- F-23 → 19 audit-requirement strings distinguished only by a name prefix
- T1C-008 → 12 negative fixtures that no code executes
- P-08 → 22 data dictionaries whose definitions restate the field names

Each passes a count-based or presence-based check and fails a content-based one. If a fourth round is generated the same way, it will likely pass whatever new structural check is written for it and still not be usable.

The most effective single control available: for every register column intended to carry per-row analysis, add a validator check asserting `distinct_values > 1` (or `> n/2`) across the population. That converts the entire class of defect into a hard validator failure and would have caught P-02, P-03, P-05, P-07, and N-07 automatically.

---

## Boundary re-statement

Nothing in this review declares adoption, activation, implementation, production authorisation, merge authorisation, certification, or legal compliance. Alignment with a standard is not certification against it. The following remain in force:

**`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`**

---

## Appendix — verification steps performed

1. Extracted V2 package: 189 files, 18 top-level directories.
2. Ran `VALIDATION/validate_tier1_documents_03_10_v2.py` → `STRUCTURAL_PASS_SUBSTANTIVE_CONTROL_BLOCKED`, 0 failures, 11 checks.
3. Ran `VALIDATION/validate_tier1_documents_03_10_rr2.py --package-root .` → **`FAIL`, 3 failures**, all manifest-of-manifests related.
4. Compared `MANIFEST_OF_MANIFESTS.csv` path set against `PACKAGE_MANIFEST.json` path set → identical (168 = 168); manifest/checksum files covered = 0. V1 equivalent: 18 rows, 18 manifest/checksum files covered.
5. Recomputed SHA-256 of every `MANIFEST_OF_MANIFESTS.csv` entry → 1 mismatch (the file's own self-reference).
6. Walked filesystem vs manifest → 21 files covered by neither manifest.
7. Grepped all Python sources for each of the 12 negative fixture filenames → 11 referenced 0 times, 1 referenced once as a path literal in an existence check.
8. Hashed both `OUTSIDE_REVIEW` registers → identical SHA-256.
9. Normalized all 19 templates (stripped title + `Template name:` lines), hashed → 1 distinct body of 19; all files exactly 43 lines; 19 distinct heading sets.
10. Counted distinct values per column across `FOUNDER_DECISION_PACKET.csv` (5 rows), findings register (9 rows), lifecycle matrix (169 rows), source register (2,961 rows), audit matrix (19 rows).
11. Prefix-stripped `AUDIT_REQUIREMENTS_MATRIX.csv` `required_evidence` → 19 raw distinct collapse to 1.
12. Compared `definition` against de-underscored `field_name` across all 338 data-dictionary rows → 338 matches.
13. Grepped the whole package for "eleven-state" / "13-state" → operative registers still read "eleven-state".
14. Read `AUTHENTICATED_REPOSITORY_AND_PACKAGE_CUSTODY_RECORD_V2.json`, `LINUX_CI_REPRODUCTION_RECORD.md`, `REVISION_ROUND_2_TO_V2_DELTA_REPORT.md`, and both T1C registers in full.
