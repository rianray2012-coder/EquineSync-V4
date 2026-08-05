# EquineSync Tier 1 Documents 03–10 — Revision Round 2
## Independent Externally Sourced Standards and Benchmark Review

| Field | Value |
|---|---|
| Review type | Documentary standards-benchmark review against external primary sources |
| Reviewer | Perplexity Computer — machine-assisted independent documentary review. **Not** an accredited certification body, **not** a licensed CPA firm, **not** a third-party conformity assessment body under ISO/IEC 17021-1 |
| Review date | 2026-08-01 (America/Chicago) |
| Package reviewed | `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V1.zip` |
| Package SHA-256 | `aa61978cf952a6b93abcb20c009ce28d862734258e7aae7a4a2b12788563545f` — **VERIFIED, matches declared value** |
| Package size | 2,545,176 bytes — matches declared value |
| Retrieved from | `rianray2012-coder/EquineSync-V4`, PR [#83](https://github.com/rianray2012-coder/EquineSync-V4/pull/83) (draft, unmerged), path `governance/portfolio/tier-1/drafting/` |
| Review head | `a1a1ff5cf056e7e78c99c4038fb8afcb95aebab7` |
| Base branch / base SHA | `integrate-emergent-final-zip` / `1eb384d80daa700ba2e71ee42872cc9bba926332` |
| Internal checksum verification | 132 of 132 `CHECKSUMS.sha256` entries verified OK by independent re-run |
| V1 source provenance | User-supplied `..._V1.zip` SHA-256 `d3cd02bb…541db` == embedded `SOURCE_PACKAGE/..._V1_SOURCE.zip` == declared value — **three-way match VERIFIED** |
| Files on disk | 152 (132 covered by manifest/checksums; 20 uncovered — see F-05) |

**Authority boundary of this review.** This is a documentary review only. Nothing in this document declares or implies adoption, activation, implementation, production authorization, merge authorization, certification, or legal compliance. Alignment with an external standard is **not** conformity, and conformity is **not** certification.

---

## 1. Executive Benchmark Conclusion

The Round 2 package is a **structurally sophisticated, evidentially thin** governance artifact. Measured against current primary standards, it performs well on two dimensions and materially under-performs on four.

**Where it meets or exceeds prevailing practice.** The package's most distinctive strength is its *negative authority discipline*: it states with unusual precision what it does **not** authorize. Eight status tokens (`NOT_ADOPTED`, `NOT_ACTIVE`, `IMPLEMENTATION_NOT_AUTHORIZED`, `PRODUCTION_USE_NOT_AUTHORIZED`, `MERGE_NOT_AUTHORIZED`, `CERTIFICATION_NOT_COMPLETE`, `FOUNDER_REVIEW_REQUIRED`, `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`) are propagated consistently across registers. This is a genuinely stronger separation of *documentary candidate* from *authorized control* than most early-stage governance programs achieve, and it directly satisfies the intent of the ISO/IEC 17000:2020 distinction between attestation, declaration, and certification ([ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html)). Cryptographic fixity discipline is also above-median: content hashing, byte counts, an embedded verifiable source-package copy, and a three-way provenance chain that this review independently reproduced. That is consistent with OAIS fixity and Preservation Description Information concepts in [ISO 14721:2025](https://www.iso.org/standard/87471.html) and with the record qualities of authenticity, reliability, integrity, and usability in [ISO 15489-1:2016](https://www.iso.org/standard/62542.html).

**Where it materially under-performs.** Four problems are structural rather than cosmetic.

*First, the traceability register does not contain requirements.* `T1R2-REQ-0001` is an AI coding instruction ("Implement the smallest viable fix. Avoid architectural changes unless required.") and `T1R2-REQ-0002` is a JSON error-message literal (`"message": "User lacks required permissions."`). Both are typed `NORMATIVE_REQUIREMENT`. Against the nine individual requirement characteristics in ISO/IEC/IEEE 29148:2018 Clause 5 — necessary, appropriate, unambiguous, complete, singular, feasible, **verifiable**, correct, conforming ([ISO](https://www.iso.org/standard/72089.html)) — these entries are not requirements at all. They are keyword-scan artifacts. Every downstream coverage metric inherits this defect.

*Second, several documented controls are not implemented, and the package asserts that they are.* `INVALID_STATE_RULES.csv` defines twelve `BLOCKING_FAILURE` rules; the shipped validator implements approximately three. Rule 12 — the rule preventing candidate evidence from being represented as adopted authority — is unimplemented, yet Document 04's prose states "The validator fails candidate packages that represent candidate evidence as adopted authority." Two validator checks (`source_disposition_rules`, `workstream_completeness`) never increment the failure counter and therefore cannot fail a build under any input. A control that is documented, asserted as operating, and not operating is the specific condition ISO/IEC 27001:2022 Clause 9.2 internal audit exists to detect ([ISO](https://www.iso.org/standard/27001)), and is a deficiency requiring communication under COSO Internal Control Principle 17 ([COSO](https://www.coso.org/guidance-on-ic)).

*Third, the evidence-integrity controls do not authenticate themselves, and the recorded validation evidence does not correspond to the shipped bytes.* Of 152 files, the 20 not covered by any manifest or checksum are precisely the `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256` files. Both `VALIDATION_RESULTS/*.json` record `manifest_accuracy … files=130` while the shipped manifest contains 132 entries, and `REPOSITORY_MODE_VALIDATION_REPORT.json` records `git_metadata` as the base SHA `1eb384d8…`, not the review head `a1a1ff5c…`. The substance survives — this review re-ran the manifest check against the shipped package and found zero integrity failures — but the *attestation of record* is stale and was produced at a different repository state. Under [NIST SP 800-53 Rev. 5](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) CA-2, an assessment report must reflect the assessed object; under SA-10 the developer must "document and manage the integrity of the baseline configuration." Neither holds here.

*Fourth, the Founder decision instruments are internally contradictory and not decision-ready.* All five rows record `exact_decision_text = NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE` and `authority_granted = NONE_BY_THIS_PACKAGE`, yet `selected_disposition` is populated with three different values, none drawn from the declared enum, including `documentary approval only` for FD-T1R2-003 — a phrase that asserts an approval that the same row says was never recorded.

**Terminology exposure is the single highest-risk area for unintended representation.** The package uses "certification," "bounded certification," "Final Closing Certificate," "audit," "closing audit protocol," "ratification," "accession," and "independent validator." Under [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) clause 7.6, *certification* is reserved for third-party attestation; under [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) only an accredited body may issue a management-system certificate. Under [ISO 19011:2018](https://www.iso.org/standard/70017.html) clause 3.1, an *audit* is a "systematic, independent and documented process for obtaining objective evidence." A self-generated, self-validated package that issues its own "Closing Certificate" through a template it also authored does not satisfy either definition. The package's own disclaimers mitigate but do not cure this, because the disclaimers sit in prose while the certificate-issuing instruments sit in templates a future reader may execute in isolation.

**Net position.** The governance *architecture* is defensible and, in its authority-boundary discipline, better than prevailing early-stage practice. The governance *content* is not yet evidence. The package is best characterised as a well-designed empty frame: the schemas are largely right, the population of those schemas is demonstration data, and several of the automated controls that are supposed to prevent exactly this condition do not execute. It is not ready to be relied upon as an assurance record, and the five Founder decisions cannot be safely taken in their current form. It is, however, a credible foundation that requires bounded remediation rather than redesign.

**Final disposition: `REVISION_REQUIRED`.** Rationale is given in Section 7.

---

## 2. Standards Crosswalk

Alignment key: **A** = aligned; **P** = partially aligned; **G** = gap; **X** = conflicts with the benchmark.
Obligation key: **M** = mandatory ("shall") where conformity is claimed; **R** = recommended good practice; **V** = voluntary framework; **I** = inference by this reviewer, not a standard requirement.

| # | Package element | External benchmark | Citation | Oblig. | Align | Gap identified | Recommended revision |
|---|---|---|---|---|---|---|---|
| C-01 | `03_.../REQUIREMENT_TRACEABILITY_REGISTER.csv` — 96 rows typed `NORMATIVE_REQUIREMENT` | ISO/IEC/IEEE 29148:2018 Cl. 5 — nine characteristics of individual requirements (necessary, unambiguous, singular, **verifiable**…) | [ISO 29148](https://www.iso.org/standard/72089.html) | M | **X** | Rows are keyword-scan hits, not requirements. REQ-0001 is a coding prompt; REQ-0002 a JSON literal | Retype all 96 rows as `SOURCE_TEXT_CANDIDATE`; do not use `NORMATIVE_REQUIREMENT` until each row passes an explicit 29148 Cl. 5 characteristic check recorded per row |
| C-02 | Same register — `verification_method` = "static repository path and keyword scan" for 96/96 | ISO/IEC/IEEE 29148:2018 Cl. 5 verifiability; ISO 19011:2018 cl. 3.8 objective evidence | [ISO 29148](https://www.iso.org/standard/72089.html); [ISO 19011](https://www.iso.org/standard/70017.html) | M / R | **G** | Keyword scanning is a discovery method, not a verification method | Rename the column `discovery_method`; add a separate `verification_method` field left as `NOT_PERFORMED` |
| C-03 | Same register — 70 rows populate `test_id` while `exact_test_or_assertion_locator` = `FILE_LEVEL_CANDIDATE_ONLY` | ISO/IEC/IEEE 29148:2018 Cl. 6 traceability outcomes; NIST SP 800-53A Rev. 5 assessment methods (examine/interview/test) | [ISO 29148](https://www.iso.org/standard/72089.html); [SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final) | M / M | **X** | Populated `test_id` implies a verified link that the locator column simultaneously denies | Null the `test_id` for all rows whose locator is not assertion-level; retain the candidate file path only |
| C-04 | Same register — no design/architecture layer, no parent/child links, forward-only | ISO/IEC/IEEE 29148:2018 Cl. 6; ISO/IEC/IEEE 15288:2023 Configuration Management | [ISO 29148](https://www.iso.org/standard/72089.html); [ISO 15288:2023](https://www.iso.org/standard/81702.html) | M | **G** | No bidirectional traceability and no intermediate design tier | Add `parent_requirement_id`, `derived_from`, and a design-artifact tier; state explicitly that bidirectional trace is `NOT_ESTABLISHED` |
| C-05 | `03_.../COVERAGE_METRICS_BY_DOMAIN.csv` — "coverage 31.2%" | ISO/IEC/IEEE 15289:2019 information-item content (identification, status, basis) | [ISO/IEC/IEEE 15289:2019](https://standards.ieee.org/standard/15289-2019.html) | M | **X** | "Coverage" counts keyword matches with zero verifications executed; `requirements_with_open_gaps`=96 contradicts the register's 76/20 split; `tests_specified` always equals `tests_located` (circular); General Governance shows 53 tests against 13 requirements | Rename to `candidate_match_rate`; add a computed reconciliation check; publish `verified_coverage = 0%` as a distinct, prominent metric |
| C-06 | `04_.../INVALID_STATE_RULES.csv` — 12 `BLOCKING_FAILURE` rules | ISO/IEC 27001:2022 Cl. 9.2 internal audit; COSO ICIF 2013 Principle 17 (evaluate and communicate deficiencies); NIST SP 800-53 CA-2 | [ISO 27001](https://www.iso.org/standard/27001); [COSO](https://www.coso.org/guidance-on-ic); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) | M / R / M | **X** | Rules 03–07, 10, 11, 12 are unimplemented; Document 04 prose asserts rule 12 is enforced | Add an `implementation_status` column per rule; correct the Document 04 sentence; either implement or downgrade the rules to `DOCUMENTED_NOT_ENFORCED` |
| C-07 | `04_.../LIFECYCLE_TRANSITION_MATRIX.csv` — 81 rows (9×9) | ISO/IEC/IEEE 15288:2023 / 12207:2026 Configuration Management (baseline, change control, status accounting) | [ISO 15288:2023](https://www.iso.org/standard/81702.html); [ISO/IEC/IEEE 12207:2026](https://www.iso.org/standard/90219.html) | M | **P** | Matrix covers 9 of the 11 declared states — `DRAFT_UNMERGED` and `BLOCKED_EVIDENCE_REQUIRED` are absent; all permitted rows share one generic authority and one generic evidence string | Extend to 11×11; make `required_evidence` transition-specific rather than a single boilerplate sentence |
| C-08 | Same matrix — permitted transitions form a near-linear chain with no rejection path | ISO/IEC/IEEE 12207:2026 Decision Management process; ISO 31000:2018 Cl. 6.5 risk treatment | [ISO 12207:2026](https://www.iso.org/standard/90219.html); [ISO 31000](https://www.iso.org/standard/65694.html) | M / R | **X** | No `REJECTED`, `WITHDRAWN`, or `REMEDIATION_REQUIRED` state exists, yet the Founder decision options include "reject" and "require remediation" — two of five offered options have no representable outcome | Add `REJECTED` and `REMEDIATION_REQUIRED` states with transitions from `FOUNDER_REVIEW_READY` |
| C-09 | `05_.../FOUNDER_DECISION_DISPOSITION_REGISTER.csv` — `selected_disposition` populated | ISO/IEC/IEEE 12207:2026 Decision Management; NIST SP 800-53 CA-6 (Authorization); NIST SP 800-37 Rev. 2 Authorize step | [ISO 12207:2026](https://www.iso.org/standard/90219.html); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [SP 800-37r2](https://csrc.nist.gov/pubs/sp/800/37/r2/final) | M / M / M | **X** | Values are off-enum ("deferred", "no decision recorded", "documentary approval only") and contradict `exact_decision_text = NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE`. "Documentary approval only" asserts an approval | Set all five to the literal `NO_DISPOSITION_SELECTED`; enforce the enum in the validator |
| C-10 | `FOUNDER_DECISION_PACKET.csv` — `consequences_of_each_option` and `relevant_evidence` identical across all 5 decisions | ISO/IEC/IEEE 12207:2026 Decision Management (alternatives, criteria, consequences per alternative, rationale) | [ISO 12207:2026](https://www.iso.org/standard/90219.html) | M | **G** | One boilerplate consequence string serves five materially different decisions; `relevant_evidence` is the generic phrase "Round 2 package registers and validation reports" with no locator | Write per-decision consequences for each of the five options; replace `relevant_evidence` with exact file paths, row IDs, and SHA-256 values |
| C-11 | Packet vs. register decision framing | ISO/IEC/IEEE 15289:2019 information-item identification and consistency | [ISO/IEC/IEEE 15289:2019](https://standards.ieee.org/standard/15289-2019.html) | M | **X** | Scope drift between the two instruments: FD-001 is "lifecycle authority **vocabulary**" in the register but "lifecycle authority **rules**" in the packet; FD-003 gains the word "final"; FD-005 gains "adoption" | Make `question_presented` byte-identical across register, packet CSV, and packet MD |
| C-12 | `06_.../FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv` — 8 rows | ISO 31000:2018 Cl. 6 risk process; ISO 31073:2022 (risk owner, residual risk, risk acceptance, risk treatment); ISO/IEC 27001:2022 Cl. 10.2 nonconformity and corrective action | [ISO 31000](https://www.iso.org/standard/65694.html); [ISO 31073:2022](https://www.iso.org/standard/79637.html); [ISO 27001](https://www.iso.org/standard/27001) | R / R / M | **X** | One row per taxonomy class with identical `severity_rationale`, `impact`, `mitigation`, dates, and owner. These are schema demonstrations, not findings. No root-cause field. `T1R2-FRWE-006` is classed "accepted residual risk" while `accepted_risks` = `NONE_ACCEPTED_BY_THIS_PACKAGE` | Relabel the file `..._SCHEMA_EXEMPLAR.csv` and add an empty production register; add `root_cause` per ISO 27001 Cl. 10.2; resolve the FRWE-006 contradiction |
| C-13 | Same register vs. `DUPLICATE_AND_STALENESS_ANALYSIS.csv` vs. `CROSS_DOCUMENT_RECONCILIATION_REPORT.md` | NIST SP 800-53 CA-5 (POA&M updated from assessment findings); COSO ICIF Principle 17 | [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [COSO](https://www.coso.org/guidance-on-ic) | M / R | **X** | Self-reported `findings_lacking_evidence: 8` and `semantic_overlaps: 2` coexist with a reconciliation report claiming 0 duplicates | Reconcile the three artifacts; add an automated cross-register arithmetic check |
| C-14 | `07_.../OWNERSHIP_ACCOUNTABILITY_MATRIX.csv` — 14 roles, all `INTERIM_FUNCTION_DEFINED_NOT_PERSON_APPOINTED` | NIST CSF 2.0 **GV.RR-02** ("roles, responsibilities, and authorities … established, communicated, understood, and enforced"); COBIT 2019 RACI per objective; COSO ICIF Principles 3 and 5; NIST AI RMF GOVERN 2.1 | [NIST CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final); [ISACA COBIT](https://www.isaca.org/resources/cobit); [COSO](https://www.coso.org/guidance-on-ic); [NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) | V / V / R / V | **P** | Functions are defined but no person is accountable anywhere in the package; `appointment_evidence` and `acceptance_evidence` are `NOT_RECORDED` for all 14. Honest, but the capability is absent | Correctly scoped as FD-T1R2-002. Add an `accountability_gap_effect` column stating which controls are inoperative while the role is vacant |
| C-15 | `07_.../REVIEW_CALENDAR.csv` — 14 reviews assigned to vacant roles | ISO/IEC 27001:2022 Cl. 9.3 management review; NIST CSF 2.0 GV.OV-01/-03 | [ISO 27001](https://www.iso.org/standard/27001); [NIST CSF 2.0](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final) | M / V | **G** | A review schedule with no accountable reviewer is not an operative control | Mark every calendar row `NOT_OPERATIVE_PENDING_APPOINTMENT` and make the dates conditional on the FD-002 appointment date |
| C-16 | `08_.../SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` — 2,961 rows, `duplicate_cluster_id` empty in **all** rows | W3C PROV-DM (entities, derivations, agents); ISO 14721:2025 OAIS Preservation Description Information; ISO 15489-1:2016 integrity | [W3C PROV-DM](https://www.w3.org/TR/prov-dm/); [ISO 14721:2025](https://www.iso.org/standard/87471.html); [ISO 15489-1](https://www.iso.org/standard/62542.html) | V / R / R | **X** | The foreign key to `DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv` (145 member rows) is unpopulated, so the two registers cannot be joined — while the cross-document report claims "0 broken cross-references" | Populate `duplicate_cluster_id`; add a referential-integrity check to the validator; correct the "0 broken cross-references" claim |
| C-17 | Same register — `canonical_representation` equals the row's own path in all 2,961 rows | W3C PROV-DM derivation/revision; ISO 15489-1:2016 records controls through time | [W3C PROV-DM](https://www.w3.org/TR/prov-dm/); [ISO 15489-1](https://www.iso.org/standard/62542.html) | V / R | **G** | Self-referential canonicalisation performs no supersession resolution; `content_differs_from_canonical` is `NOT_APPLICABLE` for every row | Resolve each cluster to a single canonical member; leave unresolved clusters explicitly `CANONICAL_NOT_DETERMINED` |
| C-18 | `08_...` dashboard counts | ISO 15489-1:2016 authenticity/reliability/integrity; NIST SP 800-53 CA-2(c) assessment report accuracy | [ISO 15489-1](https://www.iso.org/standard/62542.html); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) | R / M | **X** | `exact_duplicates: 145` is the cluster-register row count, not a duplicate count. Independent recomputation: 2,884 unique SHA-256 values, **68 clusters, 77 redundant copies**. `superseded_sources: 51` equals `historical_sources: 51`, conflating two states the shared standard defines separately | Republish corrected counts; separate `SUPERSEDED` from `HISTORICAL_RETAINED` in the dashboard |
| C-19 | `08_...` cluster `T1R2-SRC-CLUSTER-001` | ISO 15489-1:2016 integrity; W3C PROV-DM | [ISO 15489-1](https://www.iso.org/standard/62542.html); [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | R / V | **X** | Two byte-identical files (`exact_byte_identity` YES, `content_differs` NO) carry different `controlling_version` values (`VERSION_NOT_DECLARED` vs `V1.0`) — a logical impossibility | Force version equality where byte identity holds, or record the divergence as an explicit finding |
| C-20 | `08_...` `authority_state` — 598 `ADOPTION_OR_LOCK_EVIDENCE_PRESENT`, 170 `FOUNDER_APPROVAL_EVIDENCE_PRESENT` | ISO/IEC 17000:2020 cl. 7.3 attestation; package's own `NOT_ADOPTED` token | [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) | R | **P** | These labels assert adoption and approval evidence inside a package that declares `NOT_ADOPTED` package-wide. Defensible if read as *historical* evidence about *other* artifacts, but the labels do not say so | Rename to `HISTORICAL_ADOPTION_EVIDENCE_OBSERVED` and `HISTORICAL_FOUNDER_APPROVAL_EVIDENCE_OBSERVED` |
| C-21 | `09_.../WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv` — 9 PRs | NIST SP 800-53 **CM-3** (configuration change control: document decisions, retain records, CCB oversight), CM-4, SA-10; ISO/IEC 27002:2022 8.32 change management; COBIT 2019 BAI domain | [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [ISO 27002](https://www.iso.org/standard/75652.html); [ISACA COBIT](https://www.isaca.org/resources/cobit) | M / R / V | **P** | Strong on change-authority separation (all `MERGE_NOT_AUTHORIZED`). Weak on record completeness: `review_thread_state` is blank for all 9 despite being retrievable from GitHub; one PR shows a CI `FAILURE` with no analysis field; `base_drift` is YES for all 9 while `merge_state` is CLEAN for 3 | Populate `review_thread_state`; add `ci_failure_analysis`; reconcile `base_drift` against `merge_state` |
| C-22 | `10_.../templates/` — 19 templates | ISO 19011:2018 cl. 3.1, 3.7–3.11 (audit, criteria, evidence, findings, conclusion); ISO/IEC/IEEE 15289:2019 generic document types | [ISO 19011](https://www.iso.org/standard/70017.html); [ISO/IEC/IEEE 15289:2019](https://standards.ieee.org/standard/15289-2019.html) | R / M | **X** | **All 19 templates are byte-identical except the H1 title and the `Template ID:` line** (verified by normalised hashing — 19/19 collapse to one hash). A Reopening Notice, a Conflict Disclosure, a Recertification Record, and an Audit Plan share identical section structure. Document 10 prose claims template 17 "requires the reviewer to state what was reviewed, what was not reviewed…"; the file contains no such distinct fields | Author 19 genuinely distinct templates with purpose-specific required fields, or reduce the set to the number of genuinely distinct instruments and renumber |
| C-23 | `10_.../AUDIT_REQUIREMENTS_MATRIX.csv` — 19 rows | ISO 19011:2018 cl. 3.7 audit criteria; NIST SP 800-53A Rev. 5 assessment procedures | [ISO 19011](https://www.iso.org/standard/70017.html); [SP 800-53A](https://csrc.nist.gov/pubs/sp/800/53/a/r5/final) | R / M | **X** | All 19 rows carry an identical `required_evidence` string — no criterion is specific to its audit area | Write area-specific evidence requirements per row |
| C-24 | `VALIDATION/validate_tier1_documents_03_10_rr2.py` | NIST SP 800-53 CA-2, CA-7; ISO/IEC 27001:2022 Cl. 9.2; COSO ICIF Principle 16 | [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [ISO 27001](https://www.iso.org/standard/27001); [COSO](https://www.coso.org/guidance-on-ic) | M / M / R | **X** | `source_disposition_rules` and `workstream_completeness` never increment `failures` and cannot fail. `evidence_state_separation` inspects only the `result` column, ignoring `runtime_evidence` and `execution_*`. `ownership_vacancy_handling` does not prevent invented appointments. No referential-integrity, enum, or dashboard-arithmetic checks | Make every declared check failure-capable; add referential-integrity, enum, and cross-register arithmetic checks; add a self-test proving each check can fail |
| C-25 | Manifest/checksum coverage — 20 of 152 files uncovered | ISO 14721:2025 OAIS fixity; NIST SP 800-53 SA-10(d); NTIA SBOM minimum elements (author, timestamp, unique identifier) | [ISO 14721:2025](https://www.iso.org/standard/87471.html); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [NTIA](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom) | R / M / R | **G** | The uncovered 20 are exactly the manifests and checksum files — the integrity controls do not authenticate themselves | Add a root `MANIFEST_OF_MANIFESTS.sha256` covering all manifest and checksum files, and record its hash in the package record |
| C-26 | `VALIDATION_RESULTS/*.json`, `REPOSITORY_MODE_VALIDATION_REPORT.json` | NIST SP 800-53 CA-2(c) (assessment report reflects the assessed object); SLSA build provenance (industry consensus, not a mandate) | [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf); [SLSA v1.1](https://slsa.dev/spec/v1.1/) | M / V | **X** | Reports record `files=130` against a 132-entry shipped manifest, and `git_metadata` = base SHA `1eb384d8…` not review head `a1a1ff5c…`. Validation was not run at the reviewed state | Re-run validation at `a1a1ff5c…` against the shipped bytes and replace the recorded results |
| C-27 | Validation environment — single host, `macOS-26.5.2-arm64`, Python 3.14.6, `/tmp/tier1_rr2_standalone.04VWbt` | ISO 19011:2018 independence principle; ISO/IEC 17000:2020 cl. 4.3 first-party activity; SLSA provenance | [ISO 19011](https://www.iso.org/standard/70017.html); [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html); [SLSA v1.1](https://slsa.dev/spec/v1.1/) | R / R / V | **P** | Single-host, unsigned, unreproduced. Correctly self-labelled first-party, but no independent re-run or signature | Add a signed, containerised, reproducible validation run; record the container digest |
| C-28 | `UNRESOLVED_ISSUE_REGISTER.csv` — 4 issues | ISO/IEC 27001:2022 Cl. 10.2; NIST SP 800-53 CA-5 POA&M | [ISO 27001](https://www.iso.org/standard/27001); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) | M / M | **G** | Four entries materially understate the open population (this review alone identifies 28 findings; the package's own registers report 578 `founder_decisions_required` in Document 08) | Expand to a full POA&M with owner, due date, and closure criteria per item |
| C-29 | Regression from V1 → RR2 | ISO/IEC/IEEE 15288:2023 / 12207:2026 Configuration Management status accounting; NIST SP 800-53 CM-3(c) (document change decisions) | [ISO 15288:2023](https://www.iso.org/standard/81702.html); [SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) | M | **X** | V1 shipped 8 per-document validators and 8 per-document test files (16 artifacts). RR2 ships one package-level validator and **no tests at all**. The delta documentation does not disclose this removal | Disclose the removal explicitly in the delta record with rationale, or restore per-document tests |
| C-30 | Documents 03–10 principal `.md` files — 15–30 lines each; shared standard 37 lines | ISO/IEC/IEEE 15289:2019 required information-item content (identification, purpose, scope, references, structure, status, authority) | [ISO/IEC/IEEE 15289:2019](https://standards.ieee.org/standard/15289-2019.html) | M | **P** | De-duplicating boilerplate into a shared standard was correct, but the per-document narrative fell from ~103 lines (V1) to 15–30 with no document-specific method, scope-limitation, or interpretation guidance added | Add per-document scope, method, limitations, and register-reading guidance |
| C-31 | Certification and audit vocabulary throughout Documents 05, 10 and templates | ISO/IEC 17000:2020 cl. 7.3/7.5/7.6/7.7; ISO/IEC 17021-1:2015; ISO 19011:2018 cl. 3.1; AICPA AT-C 105/205 | [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html); [ISO/IEC 17021-1](https://www.iso.org/standard/61651.html); [ISO 19011](https://www.iso.org/standard/70017.html); [AICPA](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2) | R / M / R / M | **X** | "Certification", "bounded certification", "Final Closing Certificate", "audit", "ratification", "attestation", "independent validator" are used for first-party self-assessment activity | See Section 5 for the full term-by-term substitution table |
| C-32 | AI-assisted authorship ("Codex machine-assisted documentary review") | NIST AI RMF 1.0 GOVERN 1.1, 2.1, 4.2 (document roles, risks, and impacts); ISO/IEC 42001:2023 documented information | [NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf); [ISO/IEC 42001](https://www.iso.org/standard/81230.html) | V / M | **P** | Authorship is honestly disclosed — better than most practice — but there is no record of AI model, version, prompt provenance, human-review scope, or the limitations of machine-generated governance content | Add an AI-authorship provenance record: tool, version, date, human reviewer, review depth, and known limitations. Do **not** claim ISO/IEC 42001 conformity |

---

## 3. Severity-Ranked Findings

Severity: **S1** material — undermines the package's own assurance claims; **S2** significant — creates contradiction or unsupported inference; **S3** moderate — weakens defensibility; **S4** minor — clarity and completeness.

### S1 — Material

**F-01 · Traceability register does not contain requirements.**
`03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv`, rows `T1R2-REQ-0001`–`T1R2-REQ-0096`, column `requirement_type`.
All 96 rows are typed `NORMATIVE_REQUIREMENT`. `T1R2-REQ-0001` is "Implement the smallest viable fix. Avoid architectural changes unless required." — an AI coding instruction sourced from `docs/AI_CODING_PROMPTS.md` line 48. `T1R2-REQ-0002` is `"message": "User lacks required permissions."` — a JSON string literal. Neither is necessary, singular, or verifiable in the sense of [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) Clause 5. Every coverage figure in the package is computed over this population.
*Effect:* the central evidentiary claim of Document 03 is not supportable as stated.

**F-02 · All 19 closing-audit templates are the same file.**
`10_CLOSING_AUDIT_PROTOCOL/templates/01_AUDIT_PLAN.md` through `19_RECERTIFICATION_RECORD.md`.
Normalised hashing (excluding the H1 title line and the `Template ID:` line) collapses all 19 files to a single hash. Each is 59 lines. The Reopening Notice, Conflict Disclosure Statement, Founder Ratification Instrument, and Bounded Scope Closing Certificate are structurally indistinguishable from the Audit Plan, and each carries the same example evidence row (`SRC-RR2-00001` / `T1R2-REQ-0001`). Document 10's prose asserts template 17 "requires the reviewer to state what was reviewed, what was not reviewed, unresolved ownership, unresolved implementation evidence, unresolved activation authority, and reliance limitations" — the file contains no such distinct required fields.
*Effect:* Document 10 does not deliver the audit instrument set it describes, and the described control does not exist.

**F-03 · Two validator checks are structurally incapable of failing.**
`VALIDATION/validate_tier1_documents_03_10_rr2.py`, checks `source_disposition_rules` and `workstream_completeness`.
Neither code path increments the `failures` counter under any input. Both nonetheless report as executed checks in `VALIDATION_RESULTS/`.
*Effect:* two controls reported as passing have never been capable of not passing — the reported PASS conveys no information.

**F-04 · Nine of twelve blocking invalid-state rules are unimplemented, and the package asserts one of them is enforced.**
`04_AUTHORITY_LIFECYCLE_REGISTER/INVALID_STATE_RULES.csv` (rules 03–07, 10, 11, 12) against `VALIDATION/validate_tier1_documents_03_10_rr2.py`.
Document 04's principal `.md` states: "The validator fails candidate packages that represent candidate evidence as adopted authority." That is rule 12, which is not implemented.
*Effect:* an affirmative statement that a control operates, where it does not. This is the highest-exposure statement in the package.

**F-05 · The integrity controls do not authenticate themselves.**
Root and per-directory `PACKAGE_MANIFEST.json` and `CHECKSUMS.sha256`.
152 files are present on disk; 132 are covered by manifest and checksums. The 20 uncovered files are exactly the manifest and checksum files. Nothing in the package binds them.
*Effect:* an actor who could modify package content could modify the manifests with no detectable inconsistency inside the package boundary. `00_PROGRAM_CONTROL/ROUND_2_PACKAGE_ZIP_RECORD.json` candidly concedes the related point — "this internal package record does not self-authenticate the archive that contains it" — which is commendable, but the same limitation applies one level down and is not disclosed there.

**F-06 · Recorded validation evidence is stale and was produced at the wrong repository state.**
`VALIDATION_RESULTS/*.json` (`manifest_accuracy … files=130`) against the shipped root `PACKAGE_MANIFEST.json` (132 entries); `REPOSITORY_MODE_VALIDATION_REPORT.json` `git_metadata` = `1eb384d80daa700ba2e71ee42872cc9bba926332`.
The recorded git state is the protected base head, not the review head `a1a1ff5cf056e7e78c99c4038fb8afcb95aebab7`. This reviewer independently re-ran the manifest verification against the shipped package and found **zero integrity failures** — the substance is sound. The *attestation of record* is not.
*Effect:* the assessment report does not reflect the assessed object, contrary to [NIST SP 800-53 Rev. 5](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) CA-2(c).

### S2 — Significant

**F-07 · Founder decision dispositions are off-enum and self-contradictory.**
`05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv`, column `selected_disposition`, rows FD-T1R2-001…005.
Declared enum (`options_considered`): approve; approve with modification; defer; reject; require remediation. Actual values: `deferred`, `no decision recorded`, `documentary approval only`, `deferred`, `no decision recorded`. None is a member of the enum. `documentary approval only` (FD-T1R2-003) asserts an approval in a row whose `exact_decision_text` reads `NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE` and whose `authority_granted` reads `NONE_BY_THIS_PACKAGE`.
*Effect:* the highest-risk single string in the package for creating an unintended representation of Founder approval.

**F-08 · The decision packet pre-states recommended outcomes that conflict with the no-decision register state.**
`FOUNDER_DECISION_PACKET.md` and `FOUNDER_DECISION_PACKET.csv`, `recommended_option`.
Five recommendations are pre-stated ("approve with retained conditions", "appoint named accountable functions or delegate appointment authority", "approve hierarchy after source review", "remediate before acceptance where feasible", "defer until review complete"). Three of the five recommended options are themselves off-enum.
*Effect:* a reader may mistake the machine-generated recommendation for the Founder's position.

**F-09 · Scope drift between the decision register and the decision packet.**
FD-T1R2-001 is "Approve lifecycle authority **vocabulary** for future use" in the register and "Approve lifecycle authority **rules**" in the packet. FD-T1R2-003 gains the word "final". FD-T1R2-005 is "Authorize future merge sequencing" in the register and "Approve future **adoption** or merge sequencing" in the packet.
*Effect:* the two instruments present materially different questions. Vocabulary is not rules; merge sequencing is not adoption.

**F-10 · The `duplicate_cluster_id` foreign key is empty in all 2,961 rows.**
`08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv` against `DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv` (145 member rows).
The two registers cannot be joined. `CROSS_DOCUMENT_RECONCILIATION_REPORT.md` simultaneously claims "0 broken cross-references."
*Effect:* a broken referential link, plus an affirmative claim that no such link is broken.

**F-11 · Source-reconciliation dashboard counts are wrong.**
`08_SOURCE_RECONCILIATION/` dashboard. Reported `exact_duplicates: 145` is the cluster-register row count, not a duplicate count. Independent recomputation over the 2,961 recorded SHA-256 values yields **2,884 unique hashes, 68 clusters, 77 redundant copies**. Separately, `superseded_sources: 51` equals `historical_sources: 51`, conflating `SUPERSEDED` and `HISTORICAL_RETAINED` — states the shared standard defines distinctly.

**F-12 · The findings register contains no findings.**
`06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv`, rows `T1R2-FRWE-001`…`008`.
One row per taxonomy class, sharing identical `severity_rationale`, `impact`, `mitigation`, `affected_requirement_or_control`, `affected_actors`, created date (2026-08-02), and due date (2026-09-01). `owner` = `FOUNDER_APPOINTMENT_REQUIRED`, `closure_evidence` = `NONE_RECORDED`, `independent_validator` = `NOT_ASSIGNED` throughout. There is no root-cause field, contrary to [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) Clause 10.2. `T1R2-FRWE-006` is classed "accepted residual risk" while `accepted_risks` reads `NONE_ACCEPTED_BY_THIS_PACKAGE`; `T1R2-FRWE-008` is classed "permanent policy decision" inside a package declared `NOT_ADOPTED`.

**F-13 · Coverage metrics do not reconcile with the register they summarise.**
`03_IMPLEMENTATION_TRACEABILITY/COVERAGE_METRICS_BY_DOMAIN.csv`.
`requirements_with_open_gaps` = 96 overall; the register's `gap_state` splits 76 `OPEN_EVIDENCE_GAP` + 20 `IMPLEMENTATION_AND_TEST_CANDIDATES_IDENTIFIED_NOT_EXECUTED`. `tests_specified` always equals `tests_located` (circular). The General Governance domain reports 53 `tests_specified` against 13 `mapped_requirements`. The OVERALL row reports 96 requirements, 30 mapped, **0 verified, 0 executed**, "coverage 31.2%".

**F-14 · Populated `test_id` values imply verification that the adjacent locator denies.**
Same register: 70 rows carry a `test_id` while `exact_test_or_assertion_locator` reads `FILE_LEVEL_CANDIDATE_ONLY`; 30 rows report `IMPLEMENTATION_CANDIDATE_LOCATED` while the symbol identifier reads `PATH_LEVEL_CANDIDATE_ONLY`; 66 rows have no candidate at all.

**F-15 · The lifecycle has no rejection or remediation state, though two of the five offered decision options require one.**
`04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv` (81 rows, 9 permitted transitions: CANDIDATE → FOUNDER_REVIEW_READY → ADOPTED → LOCKED → ACCESSIONED → ACTIVE → {SUSPENDED ⇄ ACTIVE, SUPERSEDED → HISTORICAL_RETAINED}).
There is no `REJECTED`, `WITHDRAWN`, or `REMEDIATION_REQUIRED` state. A document at `FOUNDER_REVIEW_READY` has exactly one permitted exit — forward to `ADOPTED`. Yet `options_considered` in Document 05 offers "reject" and "require remediation".
The matrix also omits 2 of the 11 states declared in the shared standard: `DRAFT_UNMERGED` and `BLOCKED_EVIDENCE_REQUIRED` — the two that best describe the package's own present condition.

**F-16 · Round 2 silently removed all per-document validators and tests.**
V1 shipped `validators/validate_document_0N.py` and `tests/test_document_0N.py` for N = 03…10 (16 files). RR2 ships one package-level validator and **no test files**. The delta documentation does not disclose the removal.
*Effect:* a reduction in verification capability presented as a Round 2 improvement.

### S3 — Moderate

**F-17 · Confidence scores have no defined scale.** `03_.../REQUIREMENT_TRACEABILITY_REGISTER.csv`, `confidence`: MEDIUM (80 rows) / LOW (16 rows), with no rubric and zero verification performed. A confidence value derived from no verification is not a measure.

**F-18 · Version identity is largely undeclared.** `source_version` = `VERSION_NOT_DECLARED` in 96/96 rows of Document 03; `controlling_version` = `VERSION_NOT_DECLARED` in 1,046 of 2,961 rows in Document 08. Against [NTIA SBOM minimum elements](https://www.ntia.gov/report/2021/minimum-elements-software-bill-materials-sbom), version is a baseline data field.

**F-19 · Byte-identical files carry divergent version metadata.** `08_.../DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv`, cluster `T1R2-SRC-CLUSTER-001`: `exact_byte_identity` = YES and `content_differs` = NO, yet `controlling_version` differs (`VERSION_NOT_DECLARED` vs `V1.0`).

**F-20 · Adoption-evidence labels conflict with the package-wide `NOT_ADOPTED` state.** `08_.../SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv`, `authority_state`: 598 rows `ADOPTION_OR_LOCK_EVIDENCE_PRESENT`, 170 rows `FOUNDER_APPROVAL_EVIDENCE_PRESENT`.

**F-21 · The review calendar schedules reviews for roles that do not exist.** `07_.../REVIEW_CALENDAR.csv`: 14 reviews, next review 2026-10-31, escalation 2026-11-14, all `NOT_COMPLETED`, every reviewer drawn from `VACANCY_AND_SUCCESSION_REGISTER.csv` where all 14 rows read `VACANT_PENDING_FOUNDER_APPOINTMENT`.

**F-22 · The unresolved-issue register understates the open population.** `UNRESOLVED_ISSUE_REGISTER.csv` records 4 issues (owner appointments; runtime/production not observed; merge authority absent; independent certification absent). Document 08 alone reports `founder_decisions_required: 578`.

**F-23 · Audit criteria are not area-specific.** `10_.../AUDIT_REQUIREMENTS_MATRIX.csv`: all 19 rows share an identical `required_evidence` string. `TEMPLATE_INDEX.csv`: 19 rows differing only in name and path.

**F-24 · Decision consequences are boilerplate.** `FOUNDER_DECISION_PACKET.csv`: `consequences_of_each_option` and `relevant_evidence` are identical strings across all five decisions; `relevant_evidence` reads "Round 2 package registers and validation reports" with no file, row, or hash locator.

**F-25 · Change records omit available GitHub data.** `09_.../WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv`: `review_thread_state` is blank for all 9 PRs; one PR carries `{"FAILURE": 1, "SUCCESS": 3, "UNKNOWN": 1}` with no analysis field; `base_drift` = YES for all 9 while `merge_state` = CLEAN for 3.

**F-26 · No bidirectional traceability and no design tier.** Document 03 provides a forward-only source→candidate mapping with no parent/child requirement links and no design or architecture layer.

### S4 — Minor

**F-27 · Per-document narrative is now too thin to guide a reader.** Documents 03–10 principal `.md` files are 15–30 lines; the shared standard is 37 lines; `FOUNDER_DECISION_PACKET.md` is 7 lines. De-duplication was correct; the resulting documents no longer carry document-specific method, scope limitation, or register-reading guidance expected of an information item under [ISO/IEC/IEEE 15289:2019](https://standards.ieee.org/standard/15289-2019.html).

**F-28 · Validation is single-host, unsigned, and unreproduced.** Recorded environment `macOS-26.5.2-arm64`, Python 3.14.6, working directory `/tmp/tier1_rr2_standalone.04VWbt`. No container digest, no signature, no second-party re-run.

---

## 4. What the Package Does Well

Recorded so the remediation does not discard working controls.

- **Authority-boundary discipline.** The eight-token status vocabulary is applied consistently across every register and is materially stronger than typical early-stage practice.
- **Verified provenance chain.** The V1 source archive hash matches the embedded copy and the declared value on a three-way independent check.
- **Honest self-limitation.** `ROUND_2_PACKAGE_ZIP_RECORD.json` states plainly that the record "does not self-authenticate the archive that contains it." Reviewer attribution is disclosed as "Codex machine-assisted documentary review; not independent certification." Candour of this kind is uncommon and should be preserved verbatim through remediation.
- **Change-authority separation.** All nine open PRs carry `MERGE_NOT_AUTHORIZED` with an identified Founder decision requirement — consistent with the intent of [NIST SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) CM-3 and CM-5.
- **Machine-readable throughout.** CSV/JSON registers with accompanying schemas and data dictionaries make every finding above independently reproducible — which is itself the strongest available evidence of auditability.

---

## 5. Legal and Compliance Caution

This section identifies terminology that could create unintended representations. It is a documentary observation, not legal advice, and no legal-compliance determination is made or implied.

### 5.1 The controlling distinction

[ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) fixes the vocabulary:

| Concept | Clause | Definition | Who performs it |
|---|---|---|---|
| Attestation | 7.3 | "issue of a statement, based on a decision, that fulfilment of specified requirements has been demonstrated" — and it "does not, of itself, provide contractual or other legal guarantees" | any party |
| Declaration | 7.5 | **first-party** attestation | the organisation itself |
| Certification | 7.6 | **third-party** attestation | an independent accredited body |
| Accreditation | 7.7 | third-party attestation as to a conformity assessment body's competence | an accreditation body |

Only a body operating under [ISO/IEC 17021-1:2015](https://www.iso.org/standard/61651.html) may issue a management-system certificate; that standard states that "certification of management systems is a third-party conformity assessment activity." Separately, [ISO 19011:2018](https://www.iso.org/standard/70017.html) clause 3.1 defines an audit as a "systematic, **independent** and documented process for obtaining objective evidence."

Everything in this package is **first-party**. Nothing in it is certification, and nothing in it is an audit in the ISO 19011 sense.

### 5.2 Terms creating exposure, with recommended substitutions

| Term as used | Where | Why it creates exposure | Recommended substitution |
|---|---|---|---|
| "certification", "bounded certification" | Doc 10 title and prose; templates 10, 17, 19 | Reserved by ISO/IEC 17000 cl. 7.6 for third-party attestation | `FIRST_PARTY_SELF_DECLARATION` |
| "Final Closing Certificate" / "Bounded Scope Closing Certificate" | `templates/17_BOUNDED_SCOPE_CLOSING_CERTIFICATE.md` | A document titled "Certificate", executable by its author, reads as a certification instrument regardless of surrounding disclaimers | `BOUNDED_SCOPE_SELF_DECLARATION_RECORD` |
| "audit", "closing audit protocol" | Doc 10 throughout | ISO 19011 cl. 3.1 requires independence, which is absent | `INTERNAL_DOCUMENTARY_REVIEW_PROTOCOL` |
| "Recertification Record" | `templates/19_RECERTIFICATION_RECORD.md` | Presupposes a prior certification that does not exist | `PERIODIC_SELF_DECLARATION_REFRESH_RECORD` |
| "Founder Certification Schedule" | `templates/10_FOUNDER_CERTIFICATION_SCHEDULE.md` | "Certification" by an internal principal is a declaration, not a certification | `FOUNDER_ATTESTATION_SCHEDULE` |
| "attestation" (unqualified) | Doc 10, templates | Correct under ISO/IEC 17000 cl. 7.3, but colloquially read as third-party; in the U.S. software context it also evokes the mandatory [CISA Secure Software Development Attestation Form](https://www.cisa.gov/resources-tools/resources/secure-software-development-attestation-form) | Always qualify: `FIRST_PARTY_ATTESTATION` |
| "independent validator" | Doc 06 register, column `independent_validator` | No independent party exists; the validator is authored and run by the same party | `SECOND_REVIEWER_NOT_ASSIGNED` |
| "PASS" determinations | `VALIDATION_RESULTS/*.json` | Two of the checks cannot fail (F-03), so "PASS" overstates | `CHECK_EXECUTED_NO_FAILURE_DETECTED`, with a per-check `failure_capable: true/false` flag |
| "ratification" | Doc 05; `templates/12_FOUNDER_RATIFICATION_INSTRUMENT.md` | Connotes binding corporate action | `FOUNDER_DOCUMENTARY_ACKNOWLEDGEMENT` unless a binding corporate act is genuinely intended |
| "accession" | Doc 04 lifecycle | Archival term of art from OAIS/records practice ([ISO 14721:2025](https://www.iso.org/standard/87471.html)) used here for a control state; not wrong, but ordering `LOCKED → ACCESSIONED → ACTIVE` inverts normal archival sequence | Define the term explicitly in the shared standard with a note that it departs from OAIS usage |
| "documentary approval only" | Doc 05, `selected_disposition` for FD-T1R2-003 | Asserts an approval in a row that also states no decision was recorded (F-07) | `NO_DISPOSITION_SELECTED` |
| "0 broken cross-references" | `CROSS_DOCUMENT_RECONCILIATION_REPORT.md` | Contradicted by F-10 | Correct the claim |

### 5.3 Framework-specific cautions

- **ISO 31000, COSO, and COBIT are not certifiable.** ISO's own catalogue states ISO 31000 "cannot be used for certification purposes" ([ISO](https://www.iso.org/standard/65694.html)). [COSO](https://www.coso.org/guidance-on-ic) and [COBIT 2019](https://www.isaca.org/resources/cobit) have no organisational certification scheme. Use "informed by" or "aligned with", never "compliant with" or "certified to".
- **NIST CSF 2.0 and the NIST AI RMF are voluntary.** Neither creates a compliance obligation ([NIST CSWP 29](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final); [NIST AI 100-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)).
- **Do not imply EU AI Act status.** [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) Articles 11, 12, 17 and 18 impose technical-documentation, logging, quality-management and 10-year retention duties on providers of **high-risk** AI systems, with the general application date of 2 August 2026 under Article 113. Whether EquineSync falls in scope is a classification question this review does not decide. The package should state `AI_ACT_CLASSIFICATION_NOT_DETERMINED` rather than remain silent.
- **SLSA and in-toto are industry consensus, not government or ISO standards** ([slsa.dev](https://slsa.dev/spec/v1.1/)). Cite them as informative only.
- **Currency corrections for any future citation.** ISO Guide 73:2009 is **withdrawn**, replaced by [ISO 31073:2022](https://www.iso.org/standard/79637.html). ISO 14721 and ISO 16363 are now **2025** editions, superseding the 2012 versions. ISO/IEC/IEEE 12207 is now the **2026** 2nd edition ([ISO](https://www.iso.org/standard/90219.html)) and 15288 the **2023** 2nd edition ([ISO](https://www.iso.org/standard/81702.html)). NIST SP 800-53 Rev. 5 is at **Release 5.2.0** (August 2025).

---

## 6. Recommended Bounded Language for FD-T1R2-001 – FD-T1R2-005

The five decisions are **not currently decision-ready**. Common defects: `selected_disposition` values that are off-enum and contradict `exact_decision_text` (F-07); pre-stated recommendations that conflict with the no-decision state (F-08); question text that differs between the register and the packet (F-09); and consequence and evidence fields that are identical boilerplate across all five (F-24).

Below is bounded, decision-ready replacement language. Adopting this text records a decision **frame**; it does not record a decision, and it grants no authority.

**Mandatory preamble for each decision record:**

> This decision is documentary. It grants no authority beyond the authority expressly named in the `authority_granted` field of this row. It does not effect adoption, activation, implementation, merge, production use, or certification. Status remains: `NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

---

### FD-T1R2-001 — Lifecycle authority vocabulary

**Question presented (use identically in register, packet CSV, and packet MD):**
> Do you approve the eleven-state lifecycle vocabulary and the state-transition rules defined in `04_AUTHORITY_LIFECYCLE_REGISTER/` as the **documentary vocabulary** to be used in future EquineSync Tier 1 governance drafting?

**Scope:** vocabulary and transition rules only, as recorded in `AUTHORITY_LIFECYCLE_STATE_REGISTER.csv`, `LIFECYCLE_TRANSITION_MATRIX.csv`, and `INVALID_STATE_RULES.csv`.
**Expressly out of scope:** any transition of any actual artifact into any state; any adoption, lock, accession, or activation.

**Conditions precedent (all must be satisfied before this decision may be taken):**
1. `LIFECYCLE_TRANSITION_MATRIX.csv` extended from 9×9 to cover all 11 declared states, adding `DRAFT_UNMERGED` and `BLOCKED_EVIDENCE_REQUIRED` (F-15).
2. `REJECTED` and `REMEDIATION_REQUIRED` states added, with transitions from `FOUNDER_REVIEW_READY`, so that the "reject" and "require remediation" options offered in this very register have a representable outcome (F-15).
3. `INVALID_STATE_RULES.csv` given an `implementation_status` column, with rules 03–07, 10, 11, 12 marked `DOCUMENTED_NOT_ENFORCED`, and the Document 04 sentence asserting enforcement of rule 12 corrected (F-04).

**Options:** `APPROVE_VOCABULARY_AS_DOCUMENTARY_STANDARD` · `APPROVE_WITH_MODIFICATION` · `DEFER` · `REJECT` · `REQUIRE_REMEDIATION_BEFORE_RECONSIDERATION`

**Authority granted if approved:** permission to use this vocabulary in future Tier 1 governance drafting. Nothing further.
**Authority expressly not granted:** no artifact enters any state; no adoption; no lock; no accession; no activation.
**Consequence if not decided:** future drafting continues without a settled vocabulary, and inconsistent state language will accumulate across documents.

---

### FD-T1R2-002 — Appointment of accountable roles

**Question presented:**
> Do you appoint named natural persons to the fourteen accountable functions in `07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv`, or delegate that appointment authority to a named person?

**Scope:** the 14 functions, all currently `INTERIM_FUNCTION_DEFINED_NOT_PERSON_APPOINTED` with `appointment_evidence` and `acceptance_evidence` = `NOT_RECORDED`.
**Expressly out of scope:** compensation, employment status, and any authority beyond the governance function described in the matrix row.

**Conditions precedent:**
1. The matrix gains an `accountability_gap_effect` column stating, per row, which controls are inoperative while that role is vacant (C-14).
2. `REVIEW_CALENDAR.csv` rows marked `NOT_OPERATIVE_PENDING_APPOINTMENT`, with dates made relative to the appointment date rather than fixed at 2026-10-31 (F-21).

**Options:** `APPOINT_NAMED_PERSONS` (attach per-role name, date, and written acceptance) · `DELEGATE_APPOINTMENT_AUTHORITY_TO_NAMED_PERSON` · `APPOINT_SUBSET_AND_DEFER_REMAINDER` · `DEFER_ALL`

**Authority granted if approved:** the appointed person holds only the governance accountability described in that matrix row.
**Authority expressly not granted:** no appointee gains merge, adoption, activation, production, or spending authority.
**Consequence if not decided:** this is the load-bearing gap. Fourteen functions remain unowned; the review calendar cannot operate; no finding in Document 06 can be closed, because closure requires an accountable owner. Every other decision here is weakened by it. This addresses [NIST CSF 2.0 GV.RR-02](https://csrc.nist.gov/pubs/cswp/29/the-nist-cybersecurity-framework-csf-20/final) and COSO ICIF Principles 3 and 5.

---

### FD-T1R2-003 — Source-control hierarchy

**Question presented:**
> Do you approve the precedence hierarchy by which one of several competing source documents is treated as controlling, as recorded in `08_SOURCE_RECONCILIATION/`?

**Scope:** the precedence **rule**, applied across 2,961 recorded sources.
**Expressly out of scope:** approval of the content of any individual source; any adoption of any source.

**Conditions precedent — this decision cannot responsibly be taken until all four are met:**
1. `duplicate_cluster_id` populated in the 2,961-row register so it can be joined to the 145-row cluster register (F-10).
2. Dashboard counts corrected: true figures are 2,884 unique hashes, 68 clusters, 77 redundant copies — not `exact_duplicates: 145` (F-11).
3. `SUPERSEDED` separated from `HISTORICAL_RETAINED` in the dashboard, where both currently read 51 (F-11).
4. `canonical_representation` resolved to an actual canonical member per cluster rather than each row pointing at itself; unresolvable clusters marked `CANONICAL_NOT_DETERMINED` (C-17). Note that 1,046 rows still carry `controlling_version = VERSION_NOT_DECLARED` (F-18), and cluster `T1R2-SRC-CLUSTER-001` contains byte-identical files with divergent versions (F-19).

**Options:** `APPROVE_HIERARCHY_RULE` · `APPROVE_WITH_MODIFICATION` · `DEFER_PENDING_DATA_CORRECTION` · `REJECT`
**Recommended framing:** the current `selected_disposition` value `documentary approval only` must be removed and replaced with `NO_DISPOSITION_SELECTED` before this decision is presented (F-07).

**Authority granted if approved:** a documentary precedence rule for future reconciliation work.
**Authority expressly not granted:** no source becomes adopted, controlling, or active.
**Consequence if not decided:** 578 recorded `founder_decisions_required` items in Document 08 remain unresolvable, and supersession relationships stay undetermined.

---

### FD-T1R2-004 — Residual risk acceptance or remediation

**Question presented:**
> For each open item in `06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/`, do you accept the residual risk, require remediation, or defer?

**Scope:** open findings, risks, exceptions, waivers, and residual risks.
**Expressly out of scope:** risks not recorded in the register, including any risk arising in operation, since no runtime evidence exists.

**Conditions precedent — this decision is not currently answerable:**
1. The eight existing rows are schema demonstrations, not findings: identical `severity_rationale`, `impact`, `mitigation`, and dates across all eight (F-12). The file should be renamed `..._SCHEMA_EXEMPLAR.csv` and a genuine register populated.
2. A `root_cause` field added per [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) Clause 10.2.
3. The contradiction resolved whereby `T1R2-FRWE-006` is classed "accepted residual risk" while `accepted_risks` reads `NONE_ACCEPTED_BY_THIS_PACKAGE` (F-12).
4. The self-reported `findings_lacking_evidence: 8` reconciled against the reconciliation report's claim of 0 duplicates (F-13).
5. `UNRESOLVED_ISSUE_REGISTER.csv` expanded from 4 entries to a full plan of action and milestones with owner, due date, and closure criteria per item, per [NIST SP 800-53](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-53r5.pdf) CA-5 (F-22).

**Options (to be exercised per finding, not in bulk):** `ACCEPT_RESIDUAL_RISK` (requires named accepting person, date, expiry, and stated basis) · `REQUIRE_REMEDIATION` (requires owner and due date) · `GRANT_TIME_BOUND_WAIVER` (requires expiry ≤ 90 days) · `DEFER`

**Authority granted if approved:** risk acceptance is recorded for the named item only, for the named period only.
**Authority expressly not granted:** acceptance of a documentary risk is not acceptance of an operational risk; no runtime, pilot, or production risk has been observed or assessed.
**Consequence if not decided:** findings remain open with no owner and no closure evidence, and the register cannot demonstrate the corrective-action cycle ISO/IEC 27001 Clause 10.2 describes.
**Note:** bulk acceptance should be avoided. Per-item acceptance with a named accepting person is the defensible form under [ISO 31073:2022](https://www.iso.org/standard/79637.html) risk-acceptance concepts.

---

### FD-T1R2-005 — Future merge sequencing

**Question presented (register and packet must match; the packet's additional word "adoption" must be removed — F-09):**
> Do you approve a **sequence** in which the nine open pull requests in `09_WORKSTREAM_PR_BRANCH_DISPOSITION/` would be considered for merge, if and when merge is separately authorized?

**Scope:** ordering only, for PRs #29, #67, #68, #69, #70, #77, #80, #81, #82.
**Expressly out of scope:** merge authorization itself; adoption; activation. Approving a sequence is not approving a merge.

**Conditions precedent:**
1. `review_thread_state` populated for all nine rows — the data is available from GitHub and is currently blank (F-25).
2. A `ci_failure_analysis` field added for the PR recording `{"FAILURE": 1, …}` (F-25).
3. `base_drift` reconciled against `merge_state`, which currently reads YES for all nine while three are CLEAN (F-25).

**Options:** `APPROVE_SEQUENCE` · `APPROVE_SEQUENCE_WITH_MODIFICATION` · `DEFER_UNTIL_FD-T1R2-002_AND_FD-T1R2-003_RESOLVED` · `REJECT_SEQUENCE`

**Authority granted if approved:** an ordering preference only.
**Authority expressly not granted:** `MERGE_NOT_AUTHORIZED` remains in force for all nine PRs. No PR may be merged on the basis of this decision.
**Consequence if not decided:** all nine PRs remain in `BLOCKED_PENDING_FOUNDER_DIRECTION` or `BLOCKED_PENDING_EVIDENCE_OR_REBASE`, with base drift accumulating against `1eb384d8…` and rising supersession risk (5 of 9 already HIGH).
**Dependency note:** this decision should be sequenced **after** FD-T1R2-002, since merge sequencing without an accountable owner cannot be executed by anyone.

---

## 7. Final Disposition

# `REVISION_REQUIRED`

**Basis.** The disposition is not `MATERIAL_REWORK_REQUIRED` because the architecture is sound, the schemas are largely correct, the authority-boundary discipline is genuinely strong, and the provenance chain verifies. Nothing needs to be redesigned.

It is not `READY` or `READY_WITH_NONBLOCKING_REVISIONS` because six S1 findings are blocking, and three of them are affirmative statements that a control operates where it does not:

1. **F-04** — Document 04 states the validator enforces a rule that is not implemented.
2. **F-03** — Two validator checks report PASS and cannot fail.
3. **F-02** — Document 10 describes an audit template set that does not exist; all 19 templates are one file.
4. **F-01** — The traceability register's contents are not requirements.
5. **F-05** — The integrity controls do not authenticate themselves.
6. **F-06** — The recorded validation evidence is stale and was produced at the wrong repository state.

An assurance package whose own controls overstate their operation cannot be relied upon as assurance, however carefully its authority boundaries are drawn. The remediation is bounded and mechanical: correct three prose assertions, make the validator checks failure-capable, retype 96 register rows, author genuinely distinct templates, add a manifest-of-manifests, and re-run validation at the review head.

**Minimum set to reach `READY_WITH_NONBLOCKING_REVISIONS`:** close F-01 through F-07, F-10, and F-15. The remaining findings can be dispositioned as tracked non-blocking revisions.

**Recommended sequence:** FD-T1R2-002 first — the ownership appointments unblock closure authority for everything else — then F-01 through F-06 remediation, then FD-T1R2-001, then FD-T1R2-003, then FD-T1R2-004, then FD-T1R2-005.

---

## 8. Reviewer Limitations

- Documentary review only. No code was executed beyond re-running the package's own manifest and checksum verification. No runtime, staging, pilot, or production behaviour was observed.
- The reviewer is **not** an accredited certification body, **not** a licensed CPA firm, and **not** a third-party conformity assessment body under [ISO/IEC 17021-1](https://www.iso.org/standard/61651.html). This is a second-party documentary review in the sense of [ISO/IEC 17000:2020](https://www.iso.org/standard/73029.html) clause 4.4, not an audit under [ISO 19011:2018](https://www.iso.org/standard/70017.html) clause 3.1.
- Standards content behind ISO and COSO paywalls was cited from official catalogue records, official scope and abstract text, and official joint communiqués. Where verbatim clause text was not publicly retrievable — notably the COSO 17-principle and 20-principle enumerations and ISO 31073:2022 term definitions — the citation identifies the framework and structure rather than quoting protected text. Those specific enumerations should be confirmed against the purchased publications before external use.
- Independently recomputed figures in this review (2,884 unique hashes; 68 clusters; 77 redundant copies; 19/19 identical templates; 132 manifest entries; 152 files on disk) were derived from the shipped package bytes and are reproducible from the verified archive.
- Findings are stated against the package as it exists at SHA-256 `aa61978cf952a6b93abcb20c009ce28d862734258e7aae7a4a2b12788563545f`. Any change to the package invalidates the file and row references above.

---

`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
