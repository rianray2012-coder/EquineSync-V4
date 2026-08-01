# Human and Machine-Readable Consistency Report

Target head: `95672eac54ae1be715e8c612c712506661e1df03`

## Consistent

- Rule ID set is identical across Markdown catalog, JSON `normative_rule_catalog`, and schema enum: 39 IDs; no orphan rule references; no unused defined IDs.
- Artifact class IDs, authority event IDs, FCR class IDs, prohibited-overclaim IDs, reopening trigger IDs, and readiness/closure state IDs match between JSON and corresponding CSV matrices.
- FCR-01..FCR-10 required columns are populated in the FCR matrix and JSON certification classes.
- Package manifest inventory covers 25 files; checksum ledger verifies all 24 non-self entries.
- Source register repository paths SRC-001..SRC-038 hash/byte values match exact PR-head bytes.
- OQ-001..OQ-010 are closed with disposition text preserved (status not stale-open).

## Inconsistent / defective

1. **Section pointer drift (P1):** JSON `markdown_section` values for 13 rules and 9 adversarial scenarios do not match current Markdown `##` headings. See `CB-001`, `CB-002`.
2. **OQ implementation section cites (P1):** `CONFLICT_AND_OPEN_QUESTION_REGISTER.csv` OQ-002/003/004/009 cite stale section numbers relative to current Markdown. See `CB-003`.
3. **Closure checklist under-specification (P2):** Completion matrix closure rows do not enumerate all `ES-GPS-CLOSE-001` / MD §16 required elements. See `CB-004`.
4. **Template vs schema (P2):** Waiver template omits schema-required `date`, `certifying_founder`, and `authority_effect`. See `CB-005`.
5. **FCR template coverage (P2):** FCR-02 and FCR-09 lack templates. See `CB-006`.
6. **Validator self-satisfaction (P2):** `VAL-016` PASS evidence relies on generator provenance and missed the section mismatches above. See `CB-007`.

## Not treated as defects

- `ADOPTION_LOCK_ACCESSION_CUSTODY_ACTIVATION_MATRIX.csv` has 7 rows while `AUTHORITY_EFFECT_MATRIX.csv` has 12: intentional subset (ALACA scope) plus Founder certification.
- Manifest `sha256: null` for `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256`: documented self-reference policy; ledger verifies the manifest.
