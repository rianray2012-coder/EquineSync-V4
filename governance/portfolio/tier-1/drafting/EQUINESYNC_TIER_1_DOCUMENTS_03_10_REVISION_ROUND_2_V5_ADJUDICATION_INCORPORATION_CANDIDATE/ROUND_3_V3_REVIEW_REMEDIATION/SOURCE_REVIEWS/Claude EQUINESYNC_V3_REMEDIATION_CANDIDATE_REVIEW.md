# Review — V3 Review Findings Remediation Candidate

**Artifact:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V3_REVIEW_FINDINGS_REMEDIATION_CANDIDATE.zip`
**SHA-256:** `ad8805d5edb18e90ea6b838c75a77a162376e198e39b5b25ffca7b456d5bf785` · 2,711,586 bytes · 209 files · 0 macOS metadata
**Predecessor:** `9a79d947…` (V2, 2,688,284 B, 189 files)
**Declared status:** `REVISION_REQUIRED_PENDING_BOUNDED_INDEPENDENT_CLOSURE_REREVIEW`
**Reviewer disposition:** **`REVISION_REQUIRED`** — one blocking defect remains, and it is new. Everything else moved forward.

`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`

---

## Executive assessment

**This is the best build in the series, and it closed almost everything raised against V2.** Integrity verifies cleanly at 173/173. The stale 212-check PASS reports are gone. `source_review_ids` is now populated with real crosswalk IDs — 19 distinct values across 20 rows, `CLAUDE-V2-04;PPLX-FD-001` rather than a prose pointer. The hedging is gone: exactly one row in the consolidated register still contains " may ", and T1C-002 now states the defect as fact. The disposition vocabulary was split exactly as recommended into `REMEDIATED_IN_V3_PENDING_REREVIEW` (11), `VALID_OPEN_RETAINED` (7), `NOT_REMEDIATED_RETAINED_OPEN` (1), and `RETAINED_NONBLOCKING_OPEN` (1), so nobody can read half the register as half-fixed any more. The per-finding evidence register now carries 20 distinct `evidence_locator` values with a uniform, correct `closure_assertion=NOT_CLOSED_BY_THIS_PACKAGE`.

**R2-02 is finally repaired.** `FD-T1R2-001` reads "thirteen-state" in `FOUNDER_DECISION_DISPOSITION_REGISTER.csv:2`, the matching `.json:21`, and `FOUNDER_DECISION_PACKET.csv:2`. The external reviewer's original wording is preserved unaltered in `EXTERNAL_REVIEW/` and the source reviews, which is right.

**The negative fixtures are real.** `execute_negative_fixtures_v3.py` runs 11 fixtures and detects the expected failure in every one, including `decision_text_lifecycle_count_mismatch.json`, `production_claim_without_evidence.csv`, `ci_failure_without_analysis.csv`, and `repeated_identical_markdown_sections.md`. That is the first hard evidence in this series that the controls can actually fail — it converts the invalid-state and terminology rules from assertion into demonstrated capability, which is what R2-07 asked for.

**The named-person problem was resolved the right way.** `FOUNDER_DECISION_PACKET.md:17` now says Patrick K. Spoon Sr. "is treated only as designated in directive context. This package does not assert that a formal appointment…" while Document 07 holds all 14 functions at `appointment_evidence=NOT_RECORDED`. Explicit non-assertion rather than quiet deletion or quiet appointment.

**One blocking defect, and it is new.** The package ships three validators that disagree about this build. `validate_tier1_documents_03_10_v3.py` returns PASS/390. `validate_tier1_documents_03_10_rr2.py` returns PASS/260. `validate_tier1_documents_03_10_v2.py` returns **FAIL, 2 failures** — and the two failing checks are `no_self_closed_findings` and `founder_packet_no_preselected_approval`, the two substantive governance controls. Both are false positives from brittle substring matching against V2-era vocabulary, but a re-reviewer running the shipped V2 validator sees `no_self_closed_findings: FAIL` — the single most alarming signal this package could emit, and a direct contradiction of the property V2 and V3 were built to demonstrate.

---

## Findings

| ID | Severity | Location | Evidence | Impact | Fix |
|---|---|---|---|---|---|
| **V3-01** | BLOCKING | `VALIDATION/validate_tier1_documents_03_10_v2.py:35,38` | `no_self_closed_findings` requires `"OPEN" in closure_state or "RETAINED" in closure_state`. V3's 11 remediated rows read `REMEDIATED_PENDING_OUTSIDE_REVIEWER_REREVIEW` — neither substring. **The rows are not self-closed**: `second_reviewer_state=NOT_PERFORMED_NOT_FABRICATED` on all 20, and that check passes. Separately, `founder_packet_no_preselected_approval` requires `"NO_DISPOSITION_SELECTED" in packet`; the string does not appear in `FOUNDER_DECISION_PACKET.md` at all — the packet uses `NO_RECOMMENDATION_SELECTED` in the CSV. Its second conjunct (`"APPROVED" not in packet`) is also unsound: any packet with a `consequence_if_approved` column matches. | Three validators, three answers, on one build. The stale one emits FAIL on the exact governance property the package exists to evidence. An independent closure re-reviewer following the package's own tooling will open with "findings appear self-closed" and the engagement is spent relitigating a string match. | Either delete `validate_tier1_documents_03_10_v2.py` from the shipped package, or update it to the V3 vocabulary: accept `REMEDIATED_PENDING_OUTSIDE_REVIEWER_REREVIEW` as non-self-closed, key `founder_packet_no_preselected_approval` off the CSV field `recommended_option == "NO_RECOMMENDATION_SELECTED"` rather than markdown substrings, and replace the bare `"APPROVED" not in packet` test with a field-level check. State in `INDEPENDENT_CLOSURE_REREVIEW_PACKAGE_AND_PROMPT.md` which single validator is authoritative and give its exact invocation. |
| **V3-02** | HIGH | `VALIDATION_RESULTS/STANDALONE_EXTRACTED_PACKAGE_VALIDATION_REPORT_V3.json` | Headline `status: PASS`. The honest determination lives in a sibling field, `package_status: REVISION_REQUIRED_PENDING_OUTSIDE_REVIEWER_REREVIEW`. V2's headline was `STRUCTURAL_PASS_SUBSTANTIVE_CONTROL_BLOCKED`, which carried the blockage in the field a reader checks first. | Regression in headline honesty. Any CI gate, dashboard, or reviewer reading `.status` sees PASS on a package that is `REVISION_REQUIRED` and has nine findings open. This is the failure mode the whole `STRUCTURAL_PASS` vs `SUBSTANTIVE_CONTROL_BLOCKED` distinction was invented to prevent. | Restore a compound headline: `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED` whenever any T1C row has `closure_state` other than closed. Keep `package_status` as the second field. Do not let `status: PASS` appear on a build with open blocking findings. |
| **V3-03** | MEDIUM | `README_FIRST.md:1` | Title reads "EquineSync Tier 1 Documents 03-10 **V2** Outside Review Remediation Candidate" in a package whose directory, archive name, validator, and validation report are all V3. | The first line of the entry-point document misidentifies the build. Given that two prior review cycles in this series were consumed by artifact-identity confusion, a mislabeled README is not a cosmetic issue. | Retitle to V3. Add a version block: build version, archive SHA-256, byte length, file count, predecessor digest, and generation timestamp. |
| **V3-04** | MEDIUM | `OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv`, T1C-004 | Restated as "Document 10 template purpose-specificity remains disputed by source reviewers" and correctly dispositioned `NOT_REMEDIATED_RETAINED_OPEN` — but severity is still **BLOCKING**. Independent inspection of all 19 templates found them purpose-specific: distinct Prohibited Conclusions sections, per-template evidence populations, and `bounded_complete_allowed=NO_IF_EXCLUSIONS_OR_OPEN_ITEMS_REMAIN` throughout. | A BLOCKING severity resting on reviewer disagreement rather than an established defect. With six BLOCKING findings in the register, one that cannot be substantiated dilutes the other five. | Downgrade to MEDIUM or OBSERVATION and record it as a disputed finding requiring re-reviewer adjudication, naming the specific template alleged to be generic. If no specific template can be named, close as `NOT_SUSTAINED_ON_CURRENT_TARGET`. |
| **V3-05** | LOW | `MANIFEST_OF_MANIFESTS.csv`; RR2 validator check count | Row count dropped 168 → **34**, and RR2 validator checks dropped 389 → 260. All 34 rows are per-directory `CHECKSUMS.sha256` / `PACKAGE_MANIFEST.json` files. **This is a correct semantic fix** — the file is now a manifest *of manifests* rather than a duplicate of the root manifest — but nothing in the package says so, and a reviewer comparing check counts across builds will read a 129-check drop as a weakened validator. | Legitimate improvement that looks like a regression in the one metric a skeptical reviewer will compare first. | Note the scope change in `REVISION_ROUND_2_TO_V2_DELTA_REPORT.md` and its V3 successor: state that `MANIFEST_OF_MANIFESTS.csv` was rescoped to manifest artifacts only, that per-file binding is fully covered by the 173 `manifest_integrity` checks, and that total coverage increased rather than decreased. |

---

## Carried forward — correctly open

These are unchanged in the operative registers and correctly marked open. No action requested here; recording so the position is unambiguous.

| Prior ID | T1C | State in V3 | Verified |
|---|---|---|---|
| R2-03 | T1C-003 | `VALID_OPEN_RETAINED` | `FD-T1R2-004` question unchanged; Document 06 holds 9 rows, all `record_classification=finding`, zero risk/exception/waiver |
| R2-04 | T1C-007 | open | 19 of 28 external findings still absent from Document 06 |
| R2-05 | T1C-007 | open | Document 06: 1 distinct `closure_evidence` across 9 rows; `second_reviewer_not_assigned=YES` on all 9 |
| R2-06 | T1C-008 | open | Per-document validators remain presence-only |
| R2-08 | T1C-006 | `VALID_OPEN_RETAINED` | Document 03 corpus unchanged |

The V3 package is explicit that it does not close these, and `second_reviewer_state=NOT_PERFORMED_NOT_FABRICATED` holds across all 20 rows. That is the correct posture.

---

## Verification performed

```bash
sha256sum -c CHECKSUMS.sha256                       # 173 OK / 173, 0 FAILED
python3 VALIDATION/validate_tier1_documents_03_10_rr2.py --package-root . \
        --mode package-only                          # PASS, 0 failures, 260 checks
python3 VALIDATION/validate_tier1_documents_03_10_v3.py .   # PASS, 0 failures, 390 checks
python3 VALIDATION/validate_tier1_documents_03_10_v2.py .   # FAIL, 2 failures  ← V3-01
python3 VALIDATION/execute_negative_fixtures_v3.py          # PASS, 11/11 expected failures detected
grep -rn "eleven-state" --include=*.csv --include=*.json .  # 0 in operative files
```

---

## Recommendation

Fix V3-01 and V3-02 — one file each, and neither touches the registers. V3-03 is a one-line retitle. Those three clear the handoff.

**With V3-01 cleared, this package is ready to go to the independent closure re-reviewer.** The integrity holds, the crosswalk is machine-joinable, the dispositions are honestly graded, the negative fixtures prove the controls can fail, and nothing is closed by self-review. The nine open findings are correctly retained as open, and the re-reviewer's scope is legible from the register without reading prose.

Do not ship with three disagreeing validators. Pick one, name it in the re-review prompt, and delete or repair the others.
