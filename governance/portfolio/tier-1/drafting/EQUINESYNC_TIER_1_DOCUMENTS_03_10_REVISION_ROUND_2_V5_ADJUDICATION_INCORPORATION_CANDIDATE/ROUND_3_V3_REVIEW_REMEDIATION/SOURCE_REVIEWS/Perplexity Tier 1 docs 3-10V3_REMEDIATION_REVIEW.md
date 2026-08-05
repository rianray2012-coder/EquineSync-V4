# EquineSync Tier 1 Documents 03–10 — V3 Remediation Candidate Review

**Package:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V3_REVIEW_FINDINGS_REMEDIATION_CANDIDATE` (209 files)
**Reviewed:** 2026-08-04 (America/Chicago)
**Baseline:** V2 package + my V2 review (N-01…N-08) + Round-2 outside review (P-01…P-09, FD-001)
**Reviewer:** Perplexity Computer — machine-assisted independent documentary review. Not an accredited certification body under ISO/IEC 17021-1:2015, not a licensed CPA firm, not a third-party conformity assessment body. Second-party documentary review under ISO/IEC 17000:2020 cl. 4.4; not an audit under ISO 19011:2018 cl. 3.1.

**Authority boundary preserved and not displaced by this review:**
`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

## Disposition

**`REVISION_REQUIRED`** — agreeing with the package's own `REVISION_REQUIRED_PENDING_OUTSIDE_REVIEWER_REREVIEW`.

This is the first round that fixed what was flagged rather than adding artifacts shaped like fixes. **All four blocking V2 defects are genuinely remediated**, verified independently. What remains open is the original Round-2 content-authoring backlog, which the package now labels honestly rather than claiming closed.

---

## Blocking V2 defects — all fixed

### N-01 Manifest integrity regression — **FIXED**

| | V2 | V3 |
|---|---|---|
| `MANIFEST_OF_MANIFESTS.csv` rows | 168 | 34 |
| Manifest/checksum files covered | **0** | **34 of 34** |
| Duplicate of `PACKAGE_MANIFEST.json` path set | yes | no |
| Includes itself | yes, stale hash | no |
| Hash mismatches | 1 | **0** |
| Files covered by neither manifest | 21 | **2** (root manifest + root checksum — the correct, disclosed bootstrap limitation) |

**Decisive evidence:** the substantive RR2 validator, which returned `FAIL` with 3 failures against V2, now returns **`PASS`, 260 checks, 0 failures** against V3. I independently recomputed SHA-256 for all 34 manifest-of-manifests entries — zero mismatches.

### N-02 Inert negative fixtures — **FIXED, with a structural caveat**

`VALIDATION/execute_negative_fixtures_v3.py` now exists and executes all 11 fixtures, each with a real predicate evaluated against fixture content. Not hardcoded — I read all 42 lines and confirmed each `record()` call performs an actual comparison. The V3 validator refuses `PASS` if any fixture fails.

**Caveat (new finding V3-01 below):** the harness re-implements detection logic inline rather than invoking the production validator.

### N-03 Weak validator masking failures — **FIXED**

The V3 validator adds 13 targeted regression guards, each tied to a specific V3 remediation: `manifest_of_manifests_only_manifest_checksum_files`, `manifest_of_manifests_no_root_self_reference`, `no_eleven_state_wording`, `source_authority_label_scoped`, `closure_register_distinct`, `source_review_ids_populated`, `negative_fixtures_execute`, `no_partial_remediated_status`, `doc10_dispute_retained_open`. The shipped report records 390 checks, 0 failures, and the honest `package_status: REVISION_REQUIRED_PENDING_OUTSIDE_REVIEWER_REREVIEW`.

These are well-chosen: each one would fail if the corresponding V3 fix were reverted.

### N-04 Duplicate closure register — **FIXED**

The two `OUTSIDE_REVIEW` registers now hash differently (`5c01ba2c…` vs `a30e8509…`) and carry different columns. `PER_FINDING_CLOSURE_EVIDENCE_REGISTER.csv` now holds what its name promises: `evidence_locator` with 20 distinct values.

### N-05 Unpopulated source crosswalk — **FIXED structurally**

`source_review_ids` now holds 19 distinct values with real identifiers — `CLAUDE-V2-01;CLAUDE-V2-02;PPLX-N-01;PPLX-N-03`. See V3-02 for accuracy concerns.

### N-06 False T1C-004 claim — **FIXED**

T1C-004 was reclassified from `PARTIALLY_REMEDIATED` with the incorrect evidence statement to **`NOT_REMEDIATED_RETAINED_OPEN`**, with the honest note that V3 "does not close the finding by reviewer disagreement." The validator now enforces this with a `doc10_dispute_retained_open` check and a `no_partial_remediated_status` guard.

### P-06 Authority label — **FIXED**

All 170 rows now read `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION`, exactly as recommended.

### FD-001 State-count mismatch — **FIXED**

Both `FOUNDER_DECISION_PACKET.csv` and `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` now read "thirteen-state," and the question text is byte-identical across both for all five decisions. No "eleven-state" wording survives in any operative register.

### Source review authentication — **verified**

`SOURCE_REVIEW_AUTHENTICATION_RECORD.json` records my V2 review at 18,250 bytes, SHA-256 `5375a01523fcd9c1…`. I diffed the included copy against my original: **byte-identical, hash matches exactly**. The Claude review is likewise recorded with a verified hash. This is proper evidence custody.

---

## New findings

### V3-01 — Fixture harness is tautological; it does not exercise the production validator (S2)

The harness contains zero references to `validate_tier1_documents_*`. Each check re-implements the detection predicate inline against the fixture file:

```python
record("non_requirement_as_normative.csv",
       any(r["requirement_type"] == "NORMATIVE_REQUIREMENT" for r in read_csv(...)),
       "unverified normative requirement detected")
```

The fixture was constructed to contain `NORMATIVE_REQUIREMENT`, and the harness checks that it contains `NORMATIVE_REQUIREMENT`. This proves the fixture is well-formed. It does **not** prove the production validator would catch that defect in a real register — which is the entire purpose of a negative fixture.

This is a real improvement over V2 (where fixtures were never touched), but the control does not yet do what T1C-008 claims.

**Standard:** [NIST SP 800-53A Rev.5](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4 — assessment procedures must produce a determination supported by evidence.

**Fix:** have each fixture case copy the fixture over the corresponding register path in a temp package tree, invoke the actual validator, and assert it returns `FAIL` on the expected check name.

Also minor: the `repeated_identical_markdown_sections.md` predicate is `text.count("same") > 1`, a keyword proxy that does not test section-level duplication.

### V3-02 — Several source-review mappings are semantically incorrect (S2)

The crosswalk is now populated, but four mappings attribute a remediation to a finding it does not address. This matters because 11 findings are marked `REMEDIATED_IN_V3_PENDING_REREVIEW` and the crosswalk is the mechanism a re-reviewer uses to verify those claims.

| Row | Cites | Evidence actually describes | Problem |
|---|---|---|---|
| T1C-009 | `PPLX-P-02` | "preserves NO_DISPOSITION_SELECTED" | P-02 is about boilerplate consequence columns, not disposition state |
| T1C-011 | `PPLX-P-05` | "binds thirteen-state terminology" | That is FD-001. P-05 is the five boilerplate lifecycle rule columns |
| T1C-010, T1C-013 | `PPLX-P-09` (both) | production-evidence separation; PR staleness | P-09 is single-platform validation, correctly covered by T1C-020 |
| T1C-012 | `PPLX-N-04` | "orphan duplicate-cluster fixture" | N-04 was the duplicate register file, unrelated to duplicate clusters |

P-02 and P-05 are also correctly listed under T1C-014 as open, so the net disposition is honest — but a reader reconciling T1C-009 or T1C-011 against my findings will not find a match.

**Fix:** correct the four mappings so `REMEDIATED` rows cite only findings they actually resolve.

### V3-03 — The one control that would close this class of defect was not added (S2)

My V2 review recommended a single check: for every register column intended to carry per-row analysis, assert `distinct_values > 1` across the population. I grepped both validators — no such check exists.

The consequence is visible in the RR2 validator's own template check:

```python
fail_if(len(templates) != 19 or len(set(names)) != 19, ...)
```

It validates distinct **names**, not distinct **bodies**. That is precisely why 19 structurally identical templates pass validation while P-04 remains unfixed. A body-hash check on the same line would fail immediately.

**Fix:** add distinct-value assertions for `consequence_if_*` (5 rows), `severity_rationale`/`impact`/`mitigation` (9 rows), the five lifecycle rule columns (169 rows), `required_evidence` after prefix-strip (19 rows), and normalized template bodies (19 files). This converts P-02, P-03, P-05, P-07, and P-04 from prose findings into hard validator failures.

### V3-04 — N-07 only partially addressed (S3)

`DATA_DICTIONARIES/CONTROLLED_VOCABULARY_DEFINITIONS_V3.csv` is new and genuinely good — 6 authored definitions, **0 of 6 trivial**. Six `enum` constraints were added to the T1C register schema.

But the scope is narrow. Across the 23 other dictionaries, **338 of 338 field definitions (100%) remain the field name with underscores replaced by spaces** — `permitted_starting_state` is still defined as "permitted starting state." All 24 schemas still carry `additionalProperties: true`, and the 6 enums cover only the T1C register — not the operative registers (`authority_state`, `permitted`, `requirement_type`, `merge_authority_state`, findings-register `severity`). Coverage is 24 schemas against 48 CSV registers.

---

## Status of all prior findings

| Finding | Status in V3 | Package's own label |
|---|---|---|
| **N-01** manifest regression | **FIXED** — verified, RR2 validator passes | T1C-001 remediated |
| **N-02** inert fixtures | **FIXED** with caveat V3-01 | T1C-008 remediated |
| **N-03** weak validator | **FIXED** | T1C-008 remediated |
| **N-04** duplicate register | **FIXED** — distinct hashes and columns | T1C-007 remediated |
| **N-05** empty crosswalk | **FIXED** structurally; see V3-02 | T1C-007 remediated |
| **N-06** false T1C-004 claim | **FIXED** — reclassified `NOT_REMEDIATED` | T1C-004 |
| **N-07** trivial dictionaries | **Partial** — see V3-04 | T1C-014 open |
| **N-08** partial coverage | Open — 24 schemas / 48 registers | T1C-014 open |
| **P-01** `discovery_method` | **Unchanged** — 96/96 `NOT_PERFORMED`, no rubric | T1C-006 open |
| **P-02** packet consequences | **Unchanged** — 1 distinct × 4 columns × 5 decisions | T1C-014 open |
| **P-03** findings rationale | **Unchanged** — 1 distinct × 3 columns × 9 rows (`root_cause` remains 9 distinct, correct) | T1C-014 open |
| **P-04** templates | **Unchanged** — 19 files, all 43 lines, **1 distinct normalized body** | T1C-004 not remediated |
| **P-05** lifecycle rule columns | **Unchanged** — 5 columns × 1 distinct × 169 rows | T1C-014 open |
| **P-06** authority label | **FIXED** | T1C-005, T1C-018 remediated |
| **P-07** audit matrix | **Unchanged** — 19 raw distinct, **1 after prefix-strip** | T1C-014 open |
| **P-08** thin narratives | Open; partial dictionary credit | T1C-016 open |
| **P-09** single-platform | Open, honestly recorded | T1C-020 nonblocking |
| **FD-001** state count | **FIXED** | T1C-002 remediated |

Eleven of twenty T1C findings are marked remediated. **I independently confirm nine of those eleven.** The two I cannot confirm as described are T1C-009 and T1C-011, whose evidence statements address different concerns than the findings they cite (V3-02) — though both underlying items remain correctly open under T1C-014.

---

## What still needs to be revised

**Should fix before the next cycle:**

1. Make the fixture harness invoke the production validator rather than re-implement predicates (V3-01).
2. Correct the four incorrect source-review mappings in T1C-009, T1C-010, T1C-011, T1C-012, T1C-013 (V3-02).
3. Add distinct-value assertions to the validator; change the template check from distinct names to distinct normalized bodies (V3-03).

**Content authoring — the original Round-2 backlog, all still outstanding:**

4. **P-04** — author purpose-specific required fields for the 19 templates. `SOURCE_MANIFEST` needs source_id / controlling_version / sha256 / byte_length / custody; `SAMPLING_RECORD` needs population_definition / sample_size / sample_method / results / disposition. Largest single item, and the only remaining `BLOCKING` finding marked not remediated.
5. **P-02** — author per-decision consequence text for the five Founder decisions. Bounded language was supplied in Section 5 of my Round-2 review and can be pasted in directly.
6. **P-03** — author per-finding `severity_rationale`, `impact`, `mitigation`.
7. **P-01** — set `discovery_method = KEYWORD_SCAN` and add a rubric.
8. **P-07** — author per-area required evidence, derived from P-04 once those fields exist.
9. **P-05** — collapse the five lifecycle rule columns to a single `rule_reference`, or populate per-transition.
10. **N-07/N-08** — author real definitions for controlled-vocabulary fields in the operative registers; set `additionalProperties: false`; extend coverage past 24 of 48 registers.
11. **P-08** — extend the 03–10 pointer files with purpose, column dictionary, and vocabulary definitions.
12. **P-09** — Linux/CI reproduction run.

**Suggested sequencing:** items 1–3 first (mechanical, and item 3 will convert most of the rest into automated failures rather than prose findings), then 7 and 5 (single-pass register edits), then 6, 8, 9, then 4 and 10–11 (the substantial authoring), then 12.

---

## Note on trajectory

My V2 review flagged a pattern: defects being closed by adding artifacts *shaped like* the fix. V3 breaks that pattern. The manifest was actually regenerated with correct scope, the fixtures actually execute, the duplicate file is actually distinct, the false claim was actually retracted rather than defended, and my own review was carried into the package byte-identical with a verified hash.

The two things V3 did best are not in any register. First, it retracted T1C-004 to `NOT_REMEDIATED_RETAINED_OPEN` rather than softening it — reclassifying a finding *downward* under review pressure is uncommon and is the correct behaviour under [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 10.2. Second, it added validator guards that would fail if its own fixes were reverted, which is what makes a remediation durable rather than cosmetic.

The remaining work is now almost entirely content authoring that no generator can produce from structure alone. Adopting the distinct-value check (V3-03) before that work begins would give it an objective completion test.

---

## Boundary re-statement

Nothing in this review declares adoption, activation, implementation, production authorisation, merge authorisation, certification, or legal compliance. Alignment with a standard is not certification against it. The following remain in force:

**`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`**

---

## Appendix — verification steps performed

1. Extracted V3: 209 files.
2. Ran `validate_tier1_documents_03_10_rr2.py --package-root .` → **`PASS`, 260 checks, 0 failures** (V2 returned `FAIL`, 3 failures).
3. Ran `validate_tier1_documents_03_10_v3.py` → `PASS`, all 13 checks including `negative_fixtures_execute`.
4. Ran `execute_negative_fixtures_v3.py` → `PASS`, 11 fixtures, all `expected_failure_detected: true`.
5. Read all 42 lines of the fixture harness; confirmed predicates are real, and confirmed zero references to any production validator.
6. Compared `MANIFEST_OF_MANIFESTS.csv` (34 rows) against `PACKAGE_MANIFEST.json` (173 entries) — not a duplicate; 34 of 34 rows are manifest/checksum files; self-reference absent.
7. Recomputed SHA-256 for every manifest-of-manifests entry → 0 mismatches, 0 missing.
8. Walked the filesystem against both manifests → 2 files uncovered (root manifest, root checksum), matching the disclosed bootstrap limitation.
9. Hashed both `OUTSIDE_REVIEW` registers → distinct; confirmed distinct column sets.
10. Counted distinct values per column: packet consequences (1 of 5 × 4 columns), findings register (1 of 9 × 3 columns, `root_cause` 9 of 9), lifecycle matrix (1 distinct × 5 columns × 169 rows), source register `authority_state` (6 values), audit matrix (19 raw → 1 prefix-stripped).
11. Normalized all 19 templates (stripped title and `Template name:` lines), hashed → **1 distinct body of 19**; all exactly 43 lines.
12. Grepped the package for "eleven-state" → present only in validator detection strings and archived review copies, absent from all operative registers.
13. Compared packet and register question text for all five decisions → byte-identical, both "thirteen-state."
14. Checked 338 data-dictionary rows for trivial definitions → 338 of 338; checked 24 schemas for enums → 6 total, all in the T1C schema; `additionalProperties: true` throughout.
15. Diffed the bundled `PERPLEXITY_V2_REMEDIATION_REVIEW.md` against my original → identical, SHA-256 `5375a015…` matching the authentication record.
16. Read the full T1C register (20 rows), `V3_REMEDIATION_SUMMARY.md`, `SOURCE_REVIEW_AUTHENTICATION_RECORD.json`, and the V3 validation report.
