# EquineSync — Tier 1 Documents 03–10, Revision Round 2

## Externally Sourced Standards and Benchmark Review

**Package under review:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V1` (delivered 2026-08-01)
**Prior review of record:** `EXTERNAL_REVIEW/EQUINESYNC_T1_RR2_EXTERNAL_STANDARDS_BENCHMARK_REVIEW.md` (Round-1 external review, disposition `REVISION_REQUIRED`)
**This review, performed:** 2026-08-04 (America/Chicago)
**Package root SHA / integrity:** validator status `PASS`, 212 checks, 0 failures on both `REPOSITORY_MODE` and `STANDALONE_EXTRACTED_PACKAGE` validation reports as shipped, and reproduced by re-run inside this review environment.

---

## Author self-identification and mandatory scope statement

This review is a **documentary review only**, produced by Perplexity Computer acting as a machine-assisted independent reviewer at the founder's request.

- The reviewer is **not** an accredited certification body under ISO/IEC 17021-1:2015 clause 5, is **not** a licensed CPA or auditor firm, is **not** a governmental conformity assessment body, and is **not** a legal advisor.
- Under ISO/IEC 17000:2020 clause 4.4 this activity is best characterised as a **second-party review of documentary evidence**, not a first-party self-declaration and not a third-party certification. It is **not** an audit as defined by ISO 19011:2018 clause 3.1 because it does not include on-the-record interviews, sampling of operational records, or field observation of controls in operation.
- The following authority boundary tokens from the shipped `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md` are preserved and are **not** displaced by this review:
  `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.
- Nothing in this review declares adoption, activation, implementation, production authorisation, merge authorisation, certification, or legal compliance. Alignment with a standard **is not** certification against that standard.

---

## 1. Executive benchmark conclusion

The RR2 package is a **materially improved** documentary artefact relative to the round-1 review. Six of the seven "blocking-minimum" S1 findings from the prior review (F-01, F-03, F-04, F-05, F-06, F-07, F-10, F-11, F-15) have been substantively remediated in the documentary evidence, and the shipped validator has been rewritten to use failure-capable predicates that would actually fail if the invariants they claim to check were violated. The package now correctly labels its own claims: dispositions read `NO_DISPOSITION_SELECTED`, authority reads `NONE_BY_THIS_PACKAGE`, requirement rows read `SOURCE_TEXT_CANDIDATE` rather than "requirement", and dashboard counts (`2884 unique / 68 clusters / 77 redundant / 145 member rows` in `SOURCE_DISPOSITION_DASHBOARD.csv`) reproduce independently from the underlying register.

However, three defects prevent an unqualified `READY` disposition:

1. **F-02 is not substantively remediated.** All 19 self-declaration templates in `10_CLOSING_AUDIT_PROTOCOL/DOCUMENTARY_TEMPLATES_LIBRARY/` remain byte-length 43 lines each and share an identical six-heading structure with generic prompts. They differ only in the `Template name:` line and the title heading. The prior review's substantive requirement — 19 purpose-specific templates each with required fields particular to their subject — is not met. Distinct SHA-256 hashes and cleaned terminology are necessary conditions, but not sufficient.
2. **Consequence and rationale fields remain single-value boilerplate in several core registers.** In `FOUNDER_DECISION_PACKET.csv` all four `consequence_if_*` columns contain exactly one distinct string across all five decisions; in `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv` the `severity_rationale`, `impact`, and `mitigation` fields contain exactly one distinct string across all nine findings; in `10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv` the `required_evidence` differs across the 19 rows only in a template-name prefix; in `04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv` the five rule columns (`reversal_rules`, `suspension_rules`, `supersession_rules`, `reactivation_rules`, `archival_rules`) each contain exactly one distinct string across all 169 rows. This is a documentary-evidence-quality gap: it does not endanger the boundary tokens but it undermines the register's usefulness as decision support.
3. **A minor factual regression in `03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv`.** All 96 rows now read `discovery_method = NOT_PERFORMED`. In fact these rows *were* discovered by keyword scan of source text (that is how they came to be listed in this register at all). The truthful value would be `KEYWORD_SCAN` with a rubric line recorded elsewhere; `NOT_PERFORMED` misrepresents historical fact of how the candidate rows entered the register.

Given the disciplined preservation of authority-boundary tokens, the sound remediation of the six blocking-minimum findings, and the fact that the residual gaps are documentary-quality rather than boundary-safety, the package is **decision-ready for Founder review with tracked non-blocking revisions**. The five Founder decisions are sufficiently bounded to be answerable without extending package authority. Recommended disposition is **`READY_WITH_NONBLOCKING_REVISIONS`** conditioned on the tracked items in Section 3.

---

## 2. Standards crosswalk

The crosswalk below evaluates the package against **primary sources only** (standards bodies, government publications, and equivalent). Where a prior-review crosswalk item was carried forward it is retained; where RR2 changed the evidence, the alignment status is updated based on independently verified content of the shipped registers and validator.

Legend for `Alignment`:
- **A** = Aligned in documentary form (does not equal certification).
- **PA** = Partially aligned; a substantive gap remains but the package does not misrepresent its own claim.
- **NA** = Not aligned; substantive gap and/or the package's own text overstates its posture.
- **N/A** = Standard is informative context, not something the package could align to at documentary stage.

| # | Package element | External benchmark (primary source) | Citation | Alignment | Gap / evidence | Recommended revision |
|---|---|---|---|---|---|---|
| C-01 | 03 Requirement Traceability Register — labels rows `SOURCE_TEXT_CANDIDATE`, sets `verification_method=NOT_PERFORMED`, `confidence=NOT_SCORED` | Requirements shall be *unambiguous*, *verifiable*, *singular*, *complete*, and *traceable* per requirements-engineering characteristics | [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) §5.2.4; [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) Systems and software engineering — Software life cycle processes | A | Rows are correctly non-asserted as requirements; verification is honestly `NOT_PERFORMED`; register does not claim traceability that has not been established. | Retain wording. Optionally add a one-paragraph rubric definition alongside `discovery_method` — see Section 3 finding P-04. |
| C-02 | 03 register `discovery_method=NOT_PERFORMED` for all 96 rows | Records should preserve **evidence of process** by which they came to be created | [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §5.2, §7.1 (records characteristics: authenticity, reliability) | NA | Rows were in fact populated by keyword scan of source text; recording that as `NOT_PERFORMED` is factually incorrect. | Replace `NOT_PERFORMED` with `KEYWORD_SCAN` (or the actual method used) and add a `discovery_method_rubric` cell to `03_IMPLEMENTATION_TRACEABILITY/DEFINITIONS.md`. See Section 3 finding P-01. |
| C-03 | 04 `LIFECYCLE_TRANSITION_MATRIX.csv` — 13 states (`CANDIDATE, DRAFT_UNMERGED, FOUNDER_REVIEW_READY, REMEDIATION_REQUIRED, REJECTED, BLOCKED_EVIDENCE_REQUIRED, ADOPTED, ACTIVE, LOCKED, SUSPENDED, HISTORICAL_RETAINED, SUPERSEDED, ACCESSIONED`), 169 rows, 15 permitted transitions with **distinct** `required_authority` and `required_evidence` per transition | Change control shall require authorised approval, evidence, and prohibition of invalid transitions | [NIST SP 800-53 Rev.5 Release 5.2.0 (Aug 2025)](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) CM-3, CM-4, CM-5, SA-10; [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) A.8.32; [COBIT 2019](https://www.isaca.org/resources/cobit) BAI06 Manage Changes | A | 13 states include the previously-missing `REJECTED`, `REMEDIATION_REQUIRED`, `DRAFT_UNMERGED`, `BLOCKED_EVIDENCE_REQUIRED`. 154 of 169 rows are labelled `permitted=NO` and each carries the transition identifier in `prohibited_transitions`. | Retain. See P-05 for optional per-transition specificity in the five rule columns. |
| C-04 | 04 five rule columns — one distinct string each across all 169 rows | Documented information should be **sufficient to determine** the specific authority, evidence, and reversibility of each transition | [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1 documented information; [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) information items | PA | The columns are populated but with boilerplate that adds no per-transition information beyond what the `permitted`/`required_authority`/`required_evidence` triple already carries. | Either (a) collapse the five rule columns into a single `rule_reference` column pointing at a numbered rule in a rules narrative; or (b) supply per-transition specificity where it varies. See P-05. |
| C-05 | 04 `INVALID_STATE_RULES.csv` — 12 rules, all `ENFORCED_BY_VALIDATOR = YES`, `failure_capable = YES` | Assessment procedures shall produce a determination and evidence of that determination | [NIST SP 800-53A Rev.5 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4; [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 9.2; [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 3.10 audit evidence | A | Validator source (`VALIDATION/validate_tier1_documents_03_10_rr2.py`) implements each of the 12 rules with a concrete predicate wrapped in `fail_if()`; sample rules include duplicate SHA-256 identity, orphan cluster FK, off-enum disposition, blank appointment status, and missing manifest coverage. | Retain. |
| C-06 | 05 `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` — all 5 `selected_disposition = NO_DISPOSITION_SELECTED`, `authority_granted = NONE_BY_THIS_PACKAGE` | Governance shall establish structures, authority, and responsibility explicitly — decisions must not be reported as taken when they are not | [COSO Internal Control – Integrated Framework 2013](https://www.coso.org/guidance-on-ic) Principle 3, Principle 5; [NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) GV.RR-02 | A | Register correctly documents pending state; no self-declared adoption. | Retain. |
| C-07 | 05 `FOUNDER_DECISION_PACKET.csv` question text is byte-identical to register question text; `recommended_option = NO_RECOMMENDATION_SELECTED` | Governance information provided to a decision-maker must be **consistent** and must not pre-empt the decision | [COSO 2013](https://www.coso.org/guidance-on-ic) Principle 3, Principle 14; [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 6.5 decision-making | A | Independent byte comparison confirms match for FD-T1R2-001…005. Packet does not pre-state a founder recommendation. | Retain. |
| C-08 | 05 packet `consequence_if_approved`, `_deferred`, `_rejected`, `_remediation_required` — 1 distinct value across all 5 decisions | Documented information supporting a decision shall be **specific enough** for the decision-maker to distinguish outcomes | [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 5.5 monitoring and review; [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html); [ISO 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5 | PA | Consequences are stated in generic identical strings; the decisions differ substantially and their consequences differ substantially — the packet does not surface that. | Populate the four consequence columns per-decision. See P-02. Recommended bounded language for the five decisions is in Section 5 below. |
| C-09 | 06 `FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv` — 9 findings mapped to prior-review F-01..F-09-ish; `root_cause` populated; no `accepted residual risk` row class | Findings must be **objective evidence of nonconformity** with root cause identified; corrective action ≠ risk acceptance | [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 10.2; [NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) ID.RA; [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 6.5.3 risk treatment; [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) attestation/declaration distinction | A | Register is now truthful about the actual findings raised by the prior review. `record_classification` values are all `finding` (not "risk acceptance"), so no waiver is being misrepresented as a finding. | Retain content of `root_cause`; extend `severity_rationale`, `impact`, `mitigation` to be per-finding. See P-03. |
| C-10 | 06 register — `severity_rationale`, `impact`, `mitigation` each 1 distinct string across 9 rows | Findings shall include specific analysis, not generic language | [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 6.4.8 documenting findings; [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4 evidence | PA | The rationale/impact/mitigation strings are identical across all nine findings; while they are truthful they carry no per-finding information. | Populate per-finding text. See P-03. |
| C-11 | 07 `OWNERSHIP_ACCOUNTABILITY_MATRIX.csv` — 14 role rows, `accountable_function` = `INTERIM_FUNCTION_DEFINED_NOT_PERSON_APPOINTED`; new column `accountability_gap_effect` describes the specific effect of the vacancy per row | Governance requires **named accountable** individuals; where vacant, the fact and its effect on control operation must be disclosed | [COSO 2013](https://www.coso.org/guidance-on-ic) Principle 3, Principle 5; [NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) GV.RR-01, GV.RR-02; [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) A.5.2 | A | Vacancy is disclosed, `accountability_gap_effect` states that closure/approval/waiver/acceptance controls are not operative pending appointment. Founder decision FD-T1R2-002 is the disposition mechanism. | Retain. |
| C-12 | 07 `REVIEW_CALENDAR.csv` — 14 rows, `overdue_state = NOT_OPERATIVE_PENDING_APPOINTMENT` | Recurring management review is required and must not be reported "on schedule" when unstaffed | [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 9.3; [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) cl. 9.3; [ISO 9001:2015 §9.3](https://www.iso.org/standard/62085.html) | A | Overdue state honestly reports non-operative rather than treating unscheduled reviews as compliant. | Retain. |
| C-13 | 08 `SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` (2,961 rows) + `DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv` (145 rows across 68 clusters) — `duplicate_cluster_id` populated on every register row; FK to cluster register with 0 broken references; `SOURCE_DISPOSITION_DASHBOARD.csv` counts `2884 unique / 68 clusters / 77 redundant / 145 member rows` | Records shall have **integrity** (referential completeness) and **usability** (findability by identifier) | [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §5.2.2, §5.2.3; [ISO 14721:2012 OAIS](https://www.iso.org/standard/57284.html) preservation description information; [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | A | Independently re-computed unique / cluster / redundant counts on the shipped register match the dashboard exactly. `superseded_sources` explicitly noted `NOT_CONFLATED_WITH_HISTORICAL_RETAINED`. | Retain. |
| C-14 | 08 register `authority_state` field still contains value `FOUNDER_APPROVAL_EVIDENCE_PRESENT` on 170 rows | Terms that could be read as adoption/authorisation should carry an explicit non-authority disclaimer, per package boundary tokens | [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 4.2 declaration ≠ attestation; [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) certification definition | PA | The paired label `SOURCE_CONTAINS_ADOPTION_OR_LOCK_EVIDENCE_NOT_PACKAGE_ADOPTION` was correctly relabelled — the parallel label was not. A reader could still read `FOUNDER_APPROVAL_EVIDENCE_PRESENT` as this package granting founder approval. | Relabel to `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION`. See P-06. |
| C-15 | 09 `WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv` — 9 open PRs (#29, #67, #68, #69, #70, #77, #80, #81, #82); columns `review_thread_state`, `ci_failure_analysis`, `merge_authority_state`, `founder_decision_required`, `url` all populated | Change management shall record change state, review outcome, testing outcome, and authorisation status per change | [NIST SP 800-53 Rev.5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) CM-3 configuration change control; [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) A.8.32; [SLSA v1.0](https://slsa.dev/spec/v1.0/levels) source integrity; [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final) PS.1, PS.2 | A | All 9 rows populated with GitHub metadata; `MERGE_NOT_AUTHORIZED` at row and package level; `review_thread_state = REVIEW_DECISION_NOT_AVAILABLE` and `ci_failure_analysis = NO_FAILURE_REPORTED_AT_CAPTURE` are honest sentinel values indicating the register captures the observation at capture time. | Retain. `founder_decision_required` correctly ties to FD-T1R2-005. |
| C-16 | 09 register merge-authorisation labelling — package explicitly says merge is not authorised | Merge authorisation is a change-control action requiring documented authority and evidence | [NIST SP 800-53 Rev.5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) CM-5 access restrictions for change; [SLSA v1.0](https://slsa.dev/spec/v1.0/levels) build/source provenance; [CISA Secure Software Development Attestation Form](https://www.cisa.gov/sites/default/files/2024-03/secure-software-development-attestation-form.pdf) | A | Package uniformly preserves `MERGE_NOT_AUTHORIZED`. | Retain. |
| C-17 | 10 `AUDIT_REQUIREMENTS_MATRIX.csv` — 19 rows, one per template, `required_evidence` differs only in the prefix "Evidence specific to <TEMPLATE_NAME>:" | Audit criteria must be **specific to the audit area** to be usable as evaluation basis | [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 5.5.5 audit criteria; [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 4.5 audit definition | PA | Distinct-string count = 19, but the substantive text is identical after the prefix. | Populate per-area required evidence — see P-07. |
| C-18 | 10 templates library — 19 `.md` files, each 43 lines, six identical section headings (Document Control / Purpose / Scope / Authority Boundary / Evidence Population / Determinations / Evidence Table / Exceptions / Prohibited Conclusions / Sign-Off), differ only in template title/name line | Information items should contain **content types appropriate to the purpose** of the item | [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) information item content; [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html); [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1 | NA | Structural framing (headings) is appropriate, but the 19 templates carry no purpose-specific required fields. A "Source Manifest" template and a "Sampling Record" template need different required fields; this package supplies the same skeleton to both. Terminology has been relabelled away from "Certificate"/"Audit Plan"/"Recertification" — that part is remediated. | Author per-template required fields. See P-08 (this is the largest tracked non-blocking item). |
| C-19 | Root `MANIFEST_OF_MANIFESTS.csv` (18 entries) — binds each per-directory `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256`; explicitly excludes root `PACKAGE_MANIFEST.json`, `CHECKSUMS.sha256`, and `MANIFEST_OF_MANIFESTS.csv` itself, with rationale disclosed | Records systems require that files be **bound to identifiers** and **integrity-verifiable** | [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §5.2.2 authenticity, §5.2.4 integrity; [ISO 14721:2012 OAIS](https://www.iso.org/standard/57284.html) fixity information; [NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) PS.3 archive integrity | A (with disclosed limitation) | Two root files and the manifest-of-manifests file itself cannot bind themselves without a circular reference. The exclusion is disclosed in the disposition register and the validator explicitly guards this bootstrap. | Retain. The bootstrap limitation is real; a follow-on delivery could publish a detached signature over the entire package via an external notary — outside the scope of this documentary package. |
| C-20 | Root `PACKAGE_MANIFEST.json` — 141 entries; `VALIDATION_RESULTS/*.json` — `manifest_integrity` count = 141, status `PASS`, failures `0` | Assessment reports must be **current** to the artefact assessed | [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 9.1 monitoring; [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4 assessment currency | A | Fresh re-run of the shipped validator in this review environment yields status `PASS` with 0 failures and 212 checks — matches the shipped `VALIDATION_RESULTS/*.json` reports byte-similarly (same check count and status). | Retain. |
| C-21 | `VALIDATION_RESULTS/*.json` `platform: macOS-26.5.2-arm64`, `python_version: 3.14.6` | Assessment records should indicate the environment in which assessment ran | [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4 evidence collection procedures | PA | Single-host validation. This is disclosed as tracked non-blocking item F-28 in the disposition register. | Retain disclosure. Consider adding a second-host validation run before formal Founder decision, if practicable. |
| C-22 | 04 register uses controlled vocabulary of 13 states with explicit definitions | Requirements engineering needs a **defined vocabulary** for lifecycle states | [ISO/IEC/IEEE 15288:2015](https://www.iso.org/standard/63711.html) systems life cycle; [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html); [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) | A | The 13 states cover initial, drafting, review, remediation, terminal, and archival positions. FD-T1R2-001 correctly puts vocabulary approval to the Founder. | Retain. |
| C-23 | 05 packet & register — `authority_granted = NONE_BY_THIS_PACKAGE` | Delegation of authority must be documented; the absence of delegation must be equally explicit | [COSO 2013](https://www.coso.org/guidance-on-ic) Principle 3; [NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) GV.RR-01 | A | Explicit non-grant is preserved throughout the package. | Retain. |
| C-24 | Package terminology guard — validator forbids `CERTIFICATION`, `CERTIFICATE`, `AUDIT_PLAN`, `RECERTIFICATION` in template file names; existing templates renamed | Terms `certification` and `audit` are specifically defined by conformity-assessment standards and their misuse creates a material misrepresentation risk | [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 5.5 certification; [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 3.1 audit; [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) requirements for certification bodies | A | Templates now named e.g. `SELF_DECLARATION_OF_DOCUMENTARY_CONFORMANCE_TEMPLATE.md`, `PERIODIC_DOCUMENTARY_REFRESH_TEMPLATE.md`, `INTERNAL_DOCUMENTARY_REVIEW_PLAN_TEMPLATE.md`. Validator would fail if any forbidden term reappeared. | Retain. See Section 4 for legal-terminology caution. |
| C-25 | Round-1 review disposition register `EXTERNAL_REVIEW_FINDING_DISPOSITION_REGISTER.csv` — F-01..F-28 each carry a `remediation_status` and a `remediation_evidence` string | Corrective action records must be traceable to the specific finding being corrected | [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 10.2 (b), (c); [ISO 9001:2015](https://www.iso.org/standard/62085.html) cl. 10.2 | A | Each finding is retained with a status and evidence pointer. F-02 is claimed `REMEDIATED` but this review finds it substantively unmet — see F-02 in Section 3. | Update F-02 disposition to `REMEDIATED_PARTIAL_TERMINOLOGY_ONLY` and re-issue as an open item pending template authoring. |
| C-26 | `TIER_1_DOCUMENT_INVENTORY.csv` and `PACKAGE_MANIFEST.json` — 8 principal docs (03..10) each backed by a pointer `.md` (7–19 lines) and a set of CSVs / templates carrying the substance | Documentation of a management system should include the documented information necessary for its effectiveness | [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1; [ISO 9001:2015](https://www.iso.org/standard/62085.html) §7.5.1 | PA | The pointer-.md convention is efficient and machine-readable, but the pointer files carry no narrative that explains to a human reader what the CSVs mean or how they should be used. This is tracked non-blocking F-27. | Extend each pointer `.md` to ~40–80 lines with a purpose statement, register-column meanings, and cross-references. See P-09. |
| C-27 | Prior review's crosswalk to EU AI Act — package makes no operative claim to AI Act compliance, and the terminology guard prevents inadvertent certification-style language | The AI Act's general-application obligations began applying **2 August 2026**; documentation and record-keeping obligations for high-risk AI systems require specific technical documentation content | [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) Articles 11, 12, 17, 18, 113 | N/A for this documentary package | The package does not represent itself as AI Act technical documentation. Whether EquineSync product features fall inside the AI Act's scope is a product-scoping question outside this documentary review. | No package change. Product-scoping determination is a separate work item for the founder. |
| C-28 | Package uses ISO 31000:2018 vocabulary (risk, likelihood, impact) with explicit note that ISO 31000 is not certifiable | ISO 31000 is a **guidance** standard and is not certifiable; ISO Guide 73 was withdrawn and replaced by ISO 31073:2022 | [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 1 scope; [ISO 31073:2022](https://www.iso.org/standard/79637.html) risk management — vocabulary | A | Vocabulary use is correct; non-certifiability is preserved. | Retain. |
| C-29 | Package uses NIST CSF 2.0 vocabulary (GV.RR-02 roles, responsibilities, and authorities) for ownership/appointment framing | NIST CSF 2.0 is an **outcomes** framework, not certifiable; GV.RR-02 addresses roles, responsibilities, and authorities | [NIST CSF 2.0](https://doi.org/10.6028/NIST.CSWP.29) GV.RR-02 | A | Framing is consistent with CSF 2.0. | Retain. |
| C-30 | Package `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md` uses the phrase "second-party documentary review" and identifies the reviewer role | ISO/IEC 17000:2020 defines first, second, and third-party assessment | [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 4.4 first/second/third-party | A | Package is correctly labelled as documentary and second-party. | Retain. |
| C-31 | Package `UNRESOLVED_ISSUE_REGISTER.csv` — 28 rows carry over from prior review with per-row disposition text | Nonconforming items should remain visible until closed with evidence | [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 10.2 (a)–(e); [ISO 9001:2015](https://www.iso.org/standard/62085.html) cl. 10.2 | A | 28 rows preserved with per-row status; disposition strings, though similar, do point back to concrete remediation evidence in the package. | Retain, and add three new rows per this review's P-01, P-02, P-03. |
| C-32 | `NIST SSDF` alignment (source integrity and build reproducibility) is claimed only to the extent supported by evidence — the package does not claim SLSA level attainment | Software attestation requires named authority, method, and evidence per attestation | [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final); [SLSA v1.0](https://slsa.dev/spec/v1.0/levels); [CISA attestation form](https://www.cisa.gov/sites/default/files/2024-03/secure-software-development-attestation-form.pdf) | A | No SSDF/SLSA compliance claim is made in the package; alignment is directional only. | Retain. |

---

## 3. Severity-ranked findings (this review)

Findings are numbered `P-##` to avoid collision with the package's own F-## series and the prior review's F-## series. Severity uses the same S1/S2/S3 taxonomy as the prior review.

### P-01 — Regression: `discovery_method = NOT_PERFORMED` misrepresents historical fact (S2)

- **Location:** `03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv`, all 96 rows, column `discovery_method`.
- **Observation:** All 96 rows carry `NOT_PERFORMED`. In fact the candidate rows were populated by keyword scan of the source text (that is how these particular source phrases came to be flagged in this register in the first place).
- **Standard:** [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) §5.2.2 authenticity — a record must reflect what it purports to reflect.
- **Impact:** Misrepresents the register's own provenance and impairs auditability of the discovery step.
- **Remediation:** Set `discovery_method = KEYWORD_SCAN` (or the actual method) and add a `discovery_method_rubric` row/column defining the rubric. Do **not** upgrade the `confidence`, `requirement_type`, or `verification_method` fields — those correctly remain `NOT_SCORED`, `SOURCE_TEXT_CANDIDATE`, `NOT_PERFORMED`.
- **Non-blocking:** yes, this can be closed with a single register edit.

### P-02 — Founder decision packet consequence columns are one-value boilerplate (S2)

- **Location:** `FOUNDER_DECISION_PACKET.csv`, columns `consequence_if_approved`, `consequence_if_deferred`, `consequence_if_rejected`, `consequence_if_remediation_required`, all 5 decisions.
- **Observation:** Each of the four columns contains exactly one distinct string across all five decisions. A decision-maker reading the packet sees no per-decision variance in stated consequences.
- **Standard:** [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 6.5 decision-making requires that decision-support material be specific to the decision; [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1 (documented information); [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html).
- **Impact:** Documentary quality gap; does not endanger boundary tokens but makes the packet less usable as decision support. This is a **material auditability defect** because the register cannot be relied on to have distinguished the consequences of the five decisions.
- **Remediation:** Populate the four consequence columns per-decision. Bounded language recommendations for the five decisions are in Section 5.
- **Non-blocking for package delivery, blocking for Founder decision-quality if not remediated before signature.**

### P-03 — Findings register `severity_rationale`, `impact`, `mitigation` are one-value boilerplate (S2)

- **Location:** `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv`, columns `severity_rationale`, `impact`, `mitigation`, all 9 findings.
- **Observation:** Each of the three columns contains exactly one distinct string across all nine findings.
- **Standard:** [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 6.4.8 (documenting findings); [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) cl. 10.2 (b)–(c) corrective action; [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4.
- **Impact:** Findings are recorded honestly but the specific reasoning that ties each finding to its severity classification is not surfaced. External reviewers cannot tell whether S1/S2 classifications were considered on the merits.
- **Remediation:** Populate the three columns per-finding.
- **Non-blocking:** yes, but strongly recommended before founder disposition on FD-T1R2-004.

### P-04 — F-02 template substance not remediated (S1 — non-blocking pending founder decision, but material) (Section 3 detail)

- **Location:** `10_CLOSING_AUDIT_PROTOCOL/DOCUMENTARY_TEMPLATES_LIBRARY/*.md` (19 files).
- **Observation:** All 19 templates are identical in structure and content except for the `Template name:` line and the top-of-file title. Each is 43 lines and shares an identical six-heading skeleton (`Document Control`, `Purpose`, `Scope of Documentary Basis`, `Authority Boundary`, `Evidence Population`, `Determinations Recorded (Not Attested)`, `Evidence Table`, `Exceptions and Deviations`, `Prohibited Conclusions Restated`, `Sign-Off Blocks`). The generic prompt content is identical across templates. Distinct SHA-256 identity is achieved only through the title/name line, not through purpose-specific required fields.
- **What was remediated:** Terminology was corrected (removal of `CERTIFICATION`, `CERTIFICATE`, `AUDIT_PLAN`, `RECERTIFICATION` and equivalent replacements). This is a genuine remediation of the terminology-exposure part of F-02.
- **What is not remediated:** The prior review's substantive requirement was that each of 19 templates carry **purpose-specific required fields**. A `Source Manifest` needs (source_id, controlling_version, sha256, byte_length, licence, custody, provenance chain). A `Sampling Record` needs (population_definition, sample_size, sample_method, confidence_target, results, disposition). An `Evidence Index` needs (evidence_id, associated_control, evidence_type, storage_location, retention, integrity_hash). None of these are surfaced.
- **Standard:** [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) information item content; [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html); [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1.
- **Impact:** The templates cannot be used as pre-authored evidence templates. They are structurally correct placeholders, not usable instruments.
- **Remediation:** Author 19 per-template required-fields blocks. This is the largest tracked non-blocking item. Reclassify prior-review F-02 as `REMEDIATED_TERMINOLOGY_ONLY_TEMPLATE_SUBSTANCE_OPEN`.
- **Boundary safety:** The package still uniformly preserves `NOT_ADOPTED`, `NOT_ACTIVE`, `IMPLEMENTATION_NOT_AUTHORIZED`, and the terminology guard, so this defect **does not permit false claims** in the current state. It is a fitness-for-use defect, not a boundary-safety defect.

### P-05 — Lifecycle rule columns are boilerplate across all 169 rows (S3)

- **Location:** `04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv`, columns `reversal_rules`, `suspension_rules`, `supersession_rules`, `reactivation_rules`, `archival_rules`.
- **Observation:** Each column has exactly 1 distinct value across 169 rows.
- **Standard:** [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1; [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html).
- **Remediation:** Either collapse the five columns to a single reference to a numbered rule (e.g., `rule_reference = R-04.reversal-01`) with the rules narrative held in `04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_RULES.md`, or supply per-transition specificity. Either is acceptable; the current form conveys no per-row information.
- **Non-blocking, cosmetic.**

### P-06 — `FOUNDER_APPROVAL_EVIDENCE_PRESENT` authority-state label reads as adoption (S2)

- **Location:** `08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv`, `authority_state` column, 170 rows.
- **Observation:** The paired label `SOURCE_CONTAINS_ADOPTION_OR_LOCK_EVIDENCE_NOT_PACKAGE_ADOPTION` was correctly relabelled to include the boundary disclaimer; the parallel `FOUNDER_APPROVAL_EVIDENCE_PRESENT` label was not.
- **Standard:** [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 4.2 declaration ≠ attestation; boundary token `NOT_ADOPTED`.
- **Impact:** A reader looking only at this column could conclude the package grants founder approval.
- **Remediation:** Relabel to `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION`.

### P-07 — `AUDIT_REQUIREMENTS_MATRIX` distinct-string count is superficial (S3)

- **Location:** `10_CLOSING_AUDIT_PROTOCOL/AUDIT_REQUIREMENTS_MATRIX.csv`, 19 rows.
- **Observation:** The 19 `required_evidence` strings differ only in the "Evidence specific to <TEMPLATE_NAME>:" prefix; the remainder is identical boilerplate ("source rows, evidence rows, sampled records, unresolved findings, exclusions, authority evidence, sign-off evidence").
- **Standard:** [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 5.5.5 audit criteria.
- **Remediation:** Populate per-area required evidence. This is closely related to P-04 (templates); if per-template required fields are authored, the audit requirements matrix should be derived from them.
- **Non-blocking, but paired with P-04.**

### P-08 — Principal document narratives are 7–19 line pointers (S3)

- **Location:** All 8 principal document `.md` files (`03_IMPLEMENTATION_TRACEABILITY.md`, `04_AUTHORITY_LIFECYCLE_REGISTER.md`, …, `10_CLOSING_AUDIT_PROTOCOL.md`).
- **Observation:** Each pointer file is 7–19 lines and contains no narrative that explains the register columns, their controlled vocabularies, or how a reader should interpret them. Tracked non-blocking by prior review F-27.
- **Standard:** [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html); [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) §7.5.1.
- **Remediation:** Extend each pointer file to include (a) purpose, (b) column dictionary for each CSV/JSON referenced, (c) controlled-vocabulary definitions, (d) cross-references to the shared standard.
- **Non-blocking, quality improvement.**

### P-09 — Validation-report platform diversity (S3, previously tracked as F-28)

- **Location:** `VALIDATION_RESULTS/*.json` `platform` field.
- **Observation:** Both reports run on `macOS-26.5.2-arm64`. There is no cross-platform validation record.
- **Standard:** [NIST SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final) §2.4.
- **Remediation:** Add a Linux (or CI) re-run of `validate_tier1_documents_03_10_rr2.py` and check in the resulting JSON as a third validation report.
- **Non-blocking, disclosed.**

**Severity summary:** 0 findings at S1 blocking-severity; 3 findings at S2 documentary-quality; 4 findings at S3 quality-improvement. Prior-review F-02 is reclassified as S1 for the substance and remains open; the boundary-safety part of F-02 (terminology) is remediated.

---

## 4. Legal and compliance terminology — caution

The package correctly avoids the following categories of language. This section restates why the caution matters and where the package must **continue** to avoid these words.

1. **"Certification" / "certificate"** — defined by [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 5.5 as third-party attestation, issued by a body meeting [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) or an equivalent accreditation. This package is not, and cannot be, a certification. The templates library must remain named `SELF_DECLARATION_...` not `CERTIFICATION_...`. The validator's forbidden-list guard is the right mechanism.
2. **"Audit"** — [ISO 19011:2018](https://www.iso.org/standard/70017.html) cl. 3.1 defines an audit as a systematic, independent process for obtaining objective evidence. The package's *closing audit protocol* is documentary; it is not an audit as ISO 19011 uses the term. The pointer file for Doc 10 correctly frames it as `CLOSING_AUDIT_PROTOCOL` in the sense of "closing-review procedure carried by documented evidence," which is a permitted use because the phrase is a documented internal term of art. The templates in that directory must not be called audit plans, audit reports, or audit findings unless the reviewer performing that step is an accredited auditor.
3. **"Compliance"** — a legal/regulatory term. Alignment with an ISO or NIST standard is not compliance with any regulator. The package must not represent GDPR, HIPAA, SOC 2, PCI-DSS, or EU AI Act compliance in any documentary artefact without a separate compliance determination by qualified counsel.
4. **"Attestation"** — [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) cl. 4.2 defines attestation as issuance of a statement based on a decision following review. A self-declaration is a form of first-party attestation *only when performed by the entity itself*; this package produces documentary evidence, not attestations, until the Founder signs.
5. **"Adoption" / "authorisation" / "approval"** — the package correctly preserves `NOT_ADOPTED`, `NONE_BY_THIS_PACKAGE`, `IMPLEMENTATION_NOT_AUTHORIZED`, `MERGE_NOT_AUTHORIZED`, and the source-register terms must be relabelled to include the disclaimer suffix (P-06).
6. **"Residual risk acceptance"** — under [ISO 31000:2018](https://www.iso.org/standard/65694.html) cl. 6.5, risk acceptance requires an accountable decision-maker. Because Founder appointments are pending (FD-T1R2-002), no residual risk can be accepted by this package. The findings register correctly does not contain any `residual_risk_accepted` classification.

The RR2 terminology remediation is real and the validator guard is a good ongoing control.

---

## 5. Recommended bounded language for FD-T1R2-001..005

The five decisions are, as written in `FOUNDER_DECISION_PACKET.csv`, sufficiently bounded to be answerable. The bounded language below is offered as **suggested phrasing to populate the four per-decision `consequence_if_*` columns of the packet**, together with a suggested `decision_scope_boundary` sentence per decision. Preserve the authority boundary tokens exactly. The proposed language does not extend package authority and does not create adoption, activation, or certification.

### FD-T1R2-001 — Adopt the eleven-state lifecycle vocabulary as the documentary lifecycle standard for Tier 1 documents

*(Note: the shipped `LIFECYCLE_TRANSITION_MATRIX.csv` contains 13 states, not 11 — the decision text and the register are one-generation offset. This should be reconciled before the decision is put to the Founder. Assuming the intended vocabulary is the 13-state one in the shipped register.)*

- **Decision scope boundary:** This decision approves the **documentary lifecycle vocabulary and permitted transitions** for Tier 1 documents. It does not adopt, activate, or authorise implementation of any Tier 1 document; it does not authorise merge; it does not create operative control of any system. It defines the words the documents will use to describe their own states.
- **Consequence if approved:** The 13-state vocabulary in `04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv` becomes the documentary standard for state values across all Tier 1 registers. Subsequent revisions of any Tier 1 register must use these state names. No document is thereby adopted or activated.
- **Consequence if deferred:** The package remains in `FOUNDER_REVIEW_READY` state indefinitely; downstream documents continue to reference draft-state vocabulary and are exposed to future terminology divergence.
- **Consequence if rejected:** The 13-state vocabulary is not adopted; the package must be revised to propose an alternative controlled vocabulary before Founder review is re-requested. The remaining four Founder decisions cannot be meaningfully answered because they use this vocabulary.
- **Consequence if remediation required:** The Founder identifies specific states to add, remove, rename, or redefine; the package is returned to `REMEDIATION_REQUIRED` and re-issued for a new review cycle.

### FD-T1R2-002 — Appoint named natural persons to the fourteen accountable functions in `OWNERSHIP_ACCOUNTABILITY_MATRIX.csv`

- **Decision scope boundary:** This decision **appoints** individual natural persons to the fourteen functions defined in `07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv`. Until named appointments are made, `overdue_state = NOT_OPERATIVE_PENDING_APPOINTMENT` remains in effect for review, closure, waiver, and acceptance controls. This decision does not adopt any Tier 1 document and does not authorise operation of a control activity; it only assigns accountability for the future operation.
- **Consequence if approved:** Named individuals are recorded in the register with acceptance evidence; the review calendar becomes operative in principle; approvals, closures, waivers, and acceptances are subsequently available upon documented appointment-effective-date and acceptance-evidence recording.
- **Consequence if deferred:** All 14 functions remain vacant; the review calendar remains not operative; no `closure_evidence`, `waiver_approval`, `residual_risk_acceptance` action can be recorded by any authority downstream. The package remains dependent on the Founder personally for any control operation.
- **Consequence if rejected:** The current 14-function structure is not endorsed; the ownership matrix must be revised (function definitions, count, RACI arrangement) before a new appointment decision is proposed.
- **Consequence if remediation required:** The Founder identifies function-definition changes (rename, merge, split, add, remove) before appointing any person. `OWNERSHIP_ACCOUNTABILITY_MATRIX.csv` is amended and re-issued.

### FD-T1R2-003 — Adopt the source-precedence hierarchy for competing source documents

- **Decision scope boundary:** This decision adopts the **rules of precedence** to apply when two or more source documents assert conflicting information about the same subject. It does not adopt any specific source document; it does not remove any duplicate from `08_SOURCE_RECONCILIATION/DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv`. It defines how future disposition decisions will be reasoned.
- **Consequence if approved:** The precedence rules become the documentary standard for future dispositions. Duplicate clusters and semantic overlaps identified in the source reconciliation register can subsequently be resolved by applying the rules. `founder_disposition_required` counts (currently 578 as reported by the dashboard) can be reduced by applying the rules; each disposition remains a separately recorded action.
- **Consequence if deferred:** The 578 pending source-disposition items remain pending; the source register carries `sources_safe_for_implementation_use = 0` indefinitely.
- **Consequence if rejected:** Alternative precedence rules must be authored and re-submitted; source register remains stalled.
- **Consequence if remediation required:** The Founder specifies particular precedence-rule wording changes; the rules are edited and re-issued for a next-round decision.

### FD-T1R2-004 — For each of the nine findings in `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv`, select one of: acceptance / remediation / defer

- **Decision scope boundary:** This decision **records the intended disposition** of the nine findings raised by the round-1 external review, per-finding. It does not close any finding: closure requires evidence recorded in `closure_evidence` following the disposition. It does not accept any residual risk beyond the specific finding named.
- **Consequence if approved (per-finding):**
  - *If `remediation` is selected for finding F-##:* the finding is recorded as `remediation_selected`; a work item is created; the finding remains `open` until `closure_evidence` is recorded.
  - *If `acceptance` is selected for finding F-##:* the finding is recorded as `residual_risk_accepted_by_authorised_founder`; a `business_justification`, `compensating_controls`, `expiration_date`, and `renewal_evidence` must be recorded (the register already carries these columns). This is the **only** path by which a finding can be closed without corrective action, and it requires a named Founder-authorised signature — not this package.
  - *If `defer` is selected for finding F-##:* the finding is recorded as `deferred_with_date`; a due date is required; the finding remains `open` and re-enters the next review cycle.
- **Consequence if deferred (the whole decision):** All nine findings remain in `open` status; the closing-audit protocol cannot proceed.
- **Consequence if rejected:** The Founder rejects the review classifications; findings must be re-analysed and re-classified before a next-round decision.
- **Consequence if remediation required:** The Founder identifies specific findings whose severity/root-cause classification needs revision before disposition can be selected.

### FD-T1R2-005 — Merge sequencing of the nine open PRs (#29, #67, #68, #69, #70, #77, #80, #81, #82)

- **Decision scope boundary:** This decision **records a sequencing intent** for the nine open PRs listed in `09_WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv`. It **does not authorise merge**. Merge authorisation is a separate change-control action that requires (a) named accountable authority (dependent on FD-T1R2-002), (b) documented CI evidence, (c) documented review-thread evidence, (d) `MERGE_AUTHORIZED` recording per PR at the time of merge. Package-level `MERGE_NOT_AUTHORIZED` is preserved throughout.
- **Consequence if approved:** The register records a proposed merge order and any dependency notes. `founder_decision_required` is set to `NO` for the sequencing question; `merge_authority_state` remains `MERGE_NOT_AUTHORIZED` for each PR pending the separate merge-authorisation action. `review_thread_state` and `ci_failure_analysis` continue to be observations at capture-time and must be reconfirmed at merge time.
- **Consequence if deferred:** All nine PRs remain in draft; no sequencing intent is recorded; the PR set continues to age and `base_drift` risk grows.
- **Consequence if rejected:** The Founder identifies structural objections (e.g., overlap between PRs, redundancy, or scope creep); the workstream register must be revised.
- **Consequence if remediation required:** The Founder identifies specific PRs to split, combine, close, or rebase before sequencing is decided.

**Note on the boundary between FD-T1R2-005 and merge authorisation:** These are deliberately separated. Approving the sequencing does not authorise the merges. This separation is a control feature and should be preserved in any revision to the packet.

---

## 6. Assessment of whether the package prevents unsupported claims

The package **does substantively prevent** unsupported claims of implementation, operation, closure, or certification in its current documentary form, through the following mechanisms whose presence and functioning were independently verified in this review:

1. **Authority boundary tokens** are preserved across every principal document, the shared standard, the founder-decision packet, and the disposition register. The tokens are:
   `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.
2. **Disposition register controlled vocabulary** — `selected_disposition = NO_DISPOSITION_SELECTED` and `authority_granted = NONE_BY_THIS_PACKAGE` on all five founder decisions.
3. **Terminology guard in the validator** — the file `VALIDATION/validate_tier1_documents_03_10_rr2.py` implements a failure-capable check that forbids `CERTIFICATION`, `CERTIFICATE`, `AUDIT_PLAN`, `RECERTIFICATION` in template file names. Any reintroduction of those terms into template names would cause the validator to fail.
4. **Invalid-state rules are failure-capable** — 12 invalid-state rules in `04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv` are implemented as concrete predicates in the validator, each wrapped in `fail_if()`. The validator would refuse to certify PASS if any of the 12 conditions were violated.
5. **Requirement rows are not requirements** — `03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv` correctly labels all 96 rows as `SOURCE_TEXT_CANDIDATE` with `verification_method = NOT_PERFORMED` and `confidence = NOT_SCORED`.
6. **Findings are findings, not "residual risks accepted"** — `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv` correctly classifies all 9 rows as `finding`.
7. **Merge authorisation is not granted** — `09_WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv` sets `merge_authority_state = MERGE_NOT_AUTHORIZED` per-PR and package-wide, with `founder_decision_required = YES` on the nine open PRs.
8. **Source dashboard prevents implicit adoption** — `SOURCE_DISPOSITION_DASHBOARD.csv` explicitly reports `sources_safe_for_implementation_use = 0` and `sources_not_safe_for_implementation_use = 2961`.

The remaining exposures P-06 (`FOUNDER_APPROVAL_EVIDENCE_PRESENT` label without a boundary suffix) and P-04 (template substance) are **fitness-for-use** exposures rather than **claim-preventing** exposures. Neither, in the current state of the package, allows a reader acting in good faith to infer adoption, activation, implementation, production authorisation, merge authorisation, or certification.

---

## 7. Assessment of Founder decision bounding and decision-readiness

The five decisions are **sufficiently bounded** to be answerable without extending package authority beyond documentary-review scope, provided the packet's per-decision `consequence_if_*` fields are populated per P-02 before the Founder is asked to sign. The decisions do not require the Founder to make merge, adoption, or activation determinations except where explicitly named (FD-T1R2-002 for appointments is the one decision that produces immediate downstream operative effect, and even then only after acceptance evidence is recorded).

One recon item: **FD-T1R2-001 refers to an "eleven-state lifecycle vocabulary" but the shipped `LIFECYCLE_TRANSITION_MATRIX.csv` contains 13 states**. This is a package internal-consistency issue. It should be reconciled before Founder review — either the decision text is updated to reference 13 states or the matrix is trimmed to 11.

---

## 8. Final disposition

**`READY_WITH_NONBLOCKING_REVISIONS`**, conditioned on the tracked items in Section 3.

Rationale:
- The seven prior-round S1 blocking-minimum findings are substantively remediated (F-01, F-03, F-04, F-06, F-07, F-10, F-15) and one is remediated with a disclosed structural limitation that is fundamental rather than optional (F-05 root manifest self-reference).
- Prior F-02 is remediated in its terminology-exposure dimension (validator guard, template renaming) but not in its substance dimension (per-template required fields), and this review reclassifies that residual as **P-04 open non-blocking**.
- The residual defects P-01 through P-09 are documentary-quality issues that do not permit any unsupported claim to be made by the package in its current form.
- The five Founder decisions are sufficiently bounded to be answerable and do not extend package authority.

Recommended sequencing before Founder review:

1. Reconcile FD-T1R2-001 "eleven-state" wording to match the 13-state shipped matrix.
2. Correct P-01 (regression, single-file edit).
3. Populate the four `consequence_if_*` columns per decision in the packet (P-02) using the bounded language in Section 5.
4. Populate `severity_rationale`, `impact`, `mitigation` per-finding in the findings register (P-03).
5. Relabel `FOUNDER_APPROVAL_EVIDENCE_PRESENT` to `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION` (P-06).
6. Track P-04 (template substance), P-05, P-07, P-08, P-09 in the unresolved-issue register as open non-blocking items with committed remediation windows.
7. Optional: add a Linux CI re-run of the validator and check in a third `VALIDATION_RESULTS/*.json` (P-09).

Nothing in this review displaces or replaces the following authority boundary tokens, which continue in force:

**`NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.**

---

## Appendix A — Primary sources consulted

- International Organization for Standardization (ISO):
  - [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) — Systems and software engineering — Life cycle processes — Requirements engineering.
  - [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) — Systems and software engineering — Software life cycle processes.
  - [ISO/IEC/IEEE 15288:2015](https://www.iso.org/standard/63711.html) — Systems and software engineering — System life cycle processes.
  - [ISO/IEC/IEEE 15289:2019](https://www.iso.org/standard/74909.html) — Systems and software engineering — Content of life-cycle information items.
  - [ISO 31000:2018](https://www.iso.org/standard/65694.html) — Risk management — Guidelines. **Not certifiable.**
  - [ISO 31073:2022](https://www.iso.org/standard/79637.html) — Risk management — Vocabulary. **Replaces withdrawn ISO Guide 73:2009.**
  - [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) — Information security management systems — Requirements.
  - [ISO/IEC 27002:2022](https://www.iso.org/standard/75652.html) — Information security controls.
  - [ISO/IEC 42001:2023](https://www.iso.org/standard/6afb0f60-3fbc-59cc-ab24-0ef9acba1da5) — AI management systems.
  - [ISO 19011:2018](https://www.iso.org/standard/70017.html) — Guidelines for auditing management systems.
  - [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) — Conformity assessment — Vocabulary and general principles.
  - [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) — Conformity assessment — Requirements for bodies providing audit and certification of management systems.
  - [ISO 15489-1:2016](https://www.iso.org/standard/62542.html) — Information and documentation — Records management.
  - [ISO 14721:2012](https://www.iso.org/standard/57284.html) — Space data and information transfer systems — OAIS reference model.
  - [ISO 9001:2015](https://www.iso.org/standard/62085.html) — Quality management systems — Requirements.
- United States National Institute of Standards and Technology (NIST):
  - [NIST SP 800-53 Rev.5 Release 5.2.0 (August 2025)](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) — Security and Privacy Controls; [NIST SP 800-53A Rev.5 Release 5.2.0](https://csrc.nist.gov/pubs/sp/800/53a/r5/upd1/final).
  - [NIST SP 800-37 Rev.2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) — Risk Management Framework.
  - [NIST Cybersecurity Framework 2.0 (CSWP 29)](https://doi.org/10.6028/NIST.CSWP.29) — including GV.RR-01, GV.RR-02.
  - [NIST AI RMF 1.0 (AI 100-1)](https://doi.org/10.6028/NIST.AI.100-1).
  - [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final).
- Governance frameworks:
  - [COSO Internal Control – Integrated Framework (2013)](https://www.coso.org/guidance-on-ic) — Principles 3, 5, 16, 17.
  - [COBIT 2019 (ISACA)](https://www.isaca.org/resources/cobit) — including BAI06 Manage Changes.
- Records and provenance:
  - [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) — Provenance Data Model.
- Software supply chain:
  - [SLSA v1.0](https://slsa.dev/spec/v1.0/levels).
  - [NTIA SBOM Minimum Elements (2021)](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom).
  - [CISA Secure Software Development Attestation Form (March 2024)](https://www.cisa.gov/sites/default/files/2024-03/secure-software-development-attestation-form.pdf).
- Regulation:
  - [Regulation (EU) 2024/1689 (AI Act)](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — Articles 11, 12, 17, 18, 113. General application from 2 August 2026.

## Appendix B — Independent verification steps performed in this review

1. Extracted and inspected package structure: 8 principal directories (03..10), root files (`PACKAGE_MANIFEST.json`, `CHECKSUMS.sha256`, `MANIFEST_OF_MANIFESTS.csv`, `FOUNDER_DECISION_PACKET.md/.csv`, `UNRESOLVED_ISSUE_REGISTER.csv`, `SHARED_TIER_1_DOCUMENTARY_STANDARD_REVISION_ROUND_2_V1.md`, `REVISION_ROUND_2_DELTA_REPORT.md`, `TIER_1_DOCUMENT_INVENTORY.csv`).
2. Re-ran the shipped validator (`VALIDATION/validate_tier1_documents_03_10_rr2.py --package-root . --mode package-only`) inside this review environment; obtained status `PASS`, 212 checks, 0 failures.
3. Read the validator source in full (167 lines) and confirmed each of the 12 invalid-state rules is implemented with a concrete predicate wrapped in `fail_if()` (i.e., failure-capable rather than always-pass).
4. Independently recomputed unique/cluster/redundant counts on `SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` from the `sha256` column; obtained 2884 unique / 68 clusters / 77 redundant / 145 cluster-member rows, matching `SOURCE_DISPOSITION_DASHBOARD.csv` exactly.
5. Verified FK integrity: 0 broken references between the source register `duplicate_cluster_id` column and the cluster register.
6. Verified 96/96 rows in `REQUIREMENT_TRACEABILITY_REGISTER.csv` carry `requirement_type=SOURCE_TEXT_CANDIDATE`, `verification_method=NOT_PERFORMED`, `confidence=NOT_SCORED`.
7. Verified 5/5 rows in `FOUNDER_DECISION_DISPOSITION_REGISTER.csv` carry `selected_disposition=NO_DISPOSITION_SELECTED`, `authority_granted=NONE_BY_THIS_PACKAGE`; verified byte-identical question text between register and packet.
8. Verified `LIFECYCLE_TRANSITION_MATRIX.csv` contains 13 states, 169 rows, 15 permitted transitions with 13 distinct `required_authority` values and 15 distinct `required_evidence` values.
9. Verified `INVALID_STATE_RULES.csv` contains 12 rules, all `ENFORCED_BY_VALIDATOR=YES`, `failure_capable=YES`.
10. Verified `OWNERSHIP_ACCOUNTABILITY_MATRIX.csv` contains 14 rows, includes new `accountability_gap_effect` column, and correctly disposes ownership pending FD-T1R2-002.
11. Verified `REVIEW_CALENDAR.csv` contains 14 rows all with `overdue_state=NOT_OPERATIVE_PENDING_APPOINTMENT`.
12. Verified `WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv` contains 9 PRs with populated GitHub metadata columns, `merge_authority_state=MERGE_NOT_AUTHORIZED` on all rows.
13. Inspected 19 templates in `DOCUMENTARY_TEMPLATES_LIBRARY/`: confirmed distinct SHA-256 hashes but identical 43-line body structure and identical prompts across templates.
14. Confirmed terminology remediation: no template file name contains `CERTIFICATION`, `CERTIFICATE`, `AUDIT_PLAN`, or `RECERTIFICATION`.
15. Confirmed root manifest coverage of on-disk files: `PACKAGE_MANIFEST.json` entries (141) match on-disk files minus the 20 deliberately excluded manifest/checksum files, which are covered by `MANIFEST_OF_MANIFESTS.csv` (18 of 20) with the remaining 2 (root manifest and root checksum) plus `MANIFEST_OF_MANIFESTS.csv` itself excluded by disclosed bootstrap rationale.
16. Confirmed `SOURCE_DISPOSITION_DASHBOARD.csv` fields `superseded_sources=NOT_CONFLATED_WITH_HISTORICAL_RETAINED`, `sources_safe_for_implementation_use=0`, `sources_not_safe_for_implementation_use=2961`.

## Appendix C — Reviewer identity and boundary re-statement

- **Reviewer:** Perplexity Computer — machine-assisted independent documentary reviewer, acting at the founder's request.
- **Not:** an accredited certification body under ISO/IEC 17021-1:2015; a licensed CPA firm; a licensed law firm; a third-party conformity assessment body; a governmental accrediting authority; a person authorised to declare adoption, activation, implementation, production authorisation, merge authorisation, certification, or legal compliance on behalf of the founder or any related party.
- **Scope:** documentary review only, of the artefacts named in this document, in the state captured on 2026-08-04.
- **Preserved authority boundary tokens:** `NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.
