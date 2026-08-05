# PERPLEXITY_INDEPENDENT_REVIEW_FEATURE_TO_GOVERNANCE_MATRIX

Reviewer: Perplexity Computer, independent (external) reviewer
Package under review: `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0` (zip provided 2026-08-03)
Repository referenced: `rianray2012-coder/EquineSync-V4`, branch `integrate-emergent-final-zip`, baseline commit `1eb384d80daa700ba2e71ee42872cc9bba926332` (verified as a real commit on GitHub, merge of PR #79 dated 2026-08-01)
Authority boundary: This review creates **no** adoption, merge, implementation, deployment, pilot, staging, or production authority. It does not close any finding or approve any artifact. It is a standalone independent report only.

---

## 1. Executive conclusion and status recommendation

The V1.0 package is a large, well-structured, structurally-consistent documentary shell. Byte-length manifests, SHA-256 checksums, controlled vocabularies, dashboard reconciliations, dependency acyclicity, queue derivations, and the 18 declared adversarial scenarios all pass the supplied validator (which I re-ran successfully). Those checks are real and useful.

However, structural pass does not equal substantive correctness. Independent inspection of the authoritative CSVs (matrix, field dictionary, governance inventory, PIA feature coverage summary, dependency register, PIA supplement mapping, and conflict register) reveals that the semantic layer of the matrix is materially deficient in ways the validator was not designed to catch. Specifically:

- Every one of the 314 feature descriptions is a pure syntactic template ("Atomic coverage row for `<name>` within `<domain>`.") of 8-13 words. None state purpose, workflow, actors, data, or business outcome. The matrix is therefore a well-typed row set, not a feature inventory as the required-question section demands.
- Every one of the 11 `FULLY_COVERED` rows is `IMPLEMENTED_UNVERIFIED` with `REPOSITORY_EVIDENCE_REFERENCED_NOT_BEHAVIOR_VERIFIED` and `RUNTIME_VERIFICATION_NOT_PERFORMED`. Seven of the 11 rely on a governing PIA whose primary package the source register itself records as `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER`; the remaining 4 rely on PIAs in `SUCCESSOR_TEXT_PENDING_FRESH_REVIEW` status. The `FULLY_COVERED` classification is therefore internally inconsistent with the package's own PIA source-status register.
- The `FIELD_DICTIONARY.csv` documents 147 of 147 columns but 143 of them share one identical boilerplate description; only 5 distinct descriptions exist. Type, ownership, derivation, null handling, and maintenance metadata are absent for every field. The required-question about the field dictionary is not satisfied.
- Risk scoring produces only six distinct integers (4, 6, 8, 9, 12, 16) across 314 rows, with 141 rows tied at 12 and 130 rows tied at 8. `LIKELY` is applied to 286 of 314 rows (91.1%). Readiness scores collapse to 8 distinct integers. The methodology does not, in practice, differentiate feature-level risk.
- The `DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv` contains only 5 conflicts, four of which enumerate 100+ feature IDs each in a single row. Findings are neither granular nor per-pair actionable.
- The 14 proposed PIA supplements target existing PIAs, but 8 of those existing PIAs (02, 04, 05, 06, 07, 08, 09, 10) have `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` and the other 2 are in successor-pending state — you cannot supplement a document that does not exist. The register acknowledges the source problem in `CONFLICT-002` but still recommends supplement drafting.
- Multiple governance domains the review prompt explicitly required (accessibility/WCAG, AI/model governance beyond one code guide gap, security assurance such as SOC 2 or ISO 27001, regulatory mapping such as GDPR/CCPA/COPPA, records retention as an independent artifact, incident response as a runbook family, and vendor/third-party risk) do not have proposed supplement or new-PIA candidates. The prompt's requirement to identify these is unmet.
- Every one of 313 dependency edges is basis `STRONGLY_INFERRED`; only one edge is `CONFIRMED`. The claimed "313 downstream" blast radius rests on a single high-degree hub (`ES-FEAT-PLATFORM-001`) plus four 292-block ties, all inferred.

**Final status recommendation:** `REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW` (formal disposition in §9). The matrix is not yet ripe for Founder decision on the questions the package itself claims are ready; several of those questions conceal unresolved evidence and methodology defects.

---

## 2. Scope, files reviewed, sampling method, and limitations

### Files reviewed (all files in the `MATRIX_PACKAGE/` directory)

Read in the order prescribed by `README_FIRST.md`, then cross-referenced pairwise:

Markdown / JSON overviews: `README_FIRST.md`, `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.md`, `COVERAGE_ANALYSIS_AND_RECOMMENDATIONS_REPORT.md`, `DASHBOARD_SUMMARY.md`, `DASHBOARD_SUMMARY.json`, `NEW_PIA_CANDIDATE_ANALYSIS.md`, `RISK_PRIORITY_METHODOLOGY.md`, `GOVERNANCE_LAYER_AND_READINESS_METHODOLOGY.md`, `IMPLEMENTATION_VERIFICATION_METHODOLOGY.md`, `VERSION_CHANGE_REPORT.md`, `PACKAGE_MANIFEST.json`, `PACKAGE_METRICS.json`, `DOCUMENTARY_VALIDATION_REPORT.json`.

Authoritative row-level CSVs: `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` (314 rows × 147 columns), `FIELD_DICTIONARY.csv`, `FEATURE_TAXONOMY_AND_ID_REGISTER.csv`, `GOVERNANCE_ARTIFACT_INVENTORY.csv`, `SOURCE_AND_AUTHORITY_REGISTER.csv`, `PIA_SUPPLEMENT_ROW_MAPPING.csv`, `PIA_FEATURE_COVERAGE_SUMMARY.csv`, `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv`, `CODE_GUIDE_GAP_ANALYSIS.csv`, `DEPENDENCY_REGISTER.csv`, `NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv`, `UNGOVERNED_CAPABILITY_REGISTER.csv`, `DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv`, `PRIORITIZED_WORK_QUEUES.csv`, `FOUNDER_DECISION_QUESTION_REGISTER.csv`, `ADVERSARIAL_REVIEW_RESULTS.csv`, `IMPLEMENTATION_TEST_AND_EVIDENCE_STATUS_SUMMARY.csv`.

Executables: `validators/validate_master_product_feature_coverage_matrix.py`, `tests/test_master_product_feature_coverage_matrix.py`. I re-ran the validator; it printed `DOCUMENTARY_VALIDATION_PASS feature_rows=314 source_rows=374`. `sha256sum -c CHECKSUMS.sha256` reported all 32 tracked files OK.

External verification: I confirmed via the GitHub API that `rianray2012-coder/EquineSync-V4` exists, that `integrate-emergent-final-zip` is its default branch, and that commit `1eb384d80daa700ba2e71ee42872cc9bba926332` exists and is dated 2026-08-01 (merge of PR #79). I did not run application code, did not execute the referenced tests, did not perform runtime or behavioral verification.

### Sampling method

- **Structural checks (all rows, 100%):** column-completeness, controlled-vocabulary conformance, uniqueness of Feature IDs, description templating, distinct-value cardinality of risk/likelihood/readiness/persona sets, evidence-path multiplicity, dependency basis distribution, `Governance coverage state × PIA_COVERAGE_STATE` cross-tab, `Governance coverage state × Governing PIA lifecycle` cross-tab.
- **Critical-risk rows (all 15, 100%):** every row with `RISK_SEVERITY=CRITICAL` inspected end-to-end. All 14 are Incidents-domain rows plus `ES-FEAT-HORSE-008 emergency transfer`.
- **`FULLY_COVERED` rows (all 11, 100%):** every FULLY_COVERED row inspected end-to-end and cross-referenced to `GOVERNANCE_ARTIFACT_INVENTORY.csv` and `PIA_FEATURE_COVERAGE_SUMMARY.csv`.
- **New-PIA candidate rows (all 14, 100%):** every `ES-FEAT-MARKETPLACE-###` row inspected against `NEW_PIA_CANDIDATE_ANALYSIS.md` and `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv`.
- **Cross-domain sample (random_state=1, n=8):** `CARE-014 bodywork`, `ADMINOPS-013 release`, `DEVELOPER-010 developer credentials`, `AI-009 human review`, `MEDIA-001 uploads`, `LESSONS-005 horse assignment`, `DEVELOPER-012 deprecation`, `MEDIA-011 attachment lifecycle`.
- **`NOT_FOUND` rows (all 13, 100%):** inspected for the alleged inconsistency of listing repository evidence paths despite `NOT_FOUND` status.
- **Governance inventory (all 54 entries):** examined lifecycle and authority-state distribution for CANONs, PIAs, and Code Guides.
- **PIA supplement register (all 15 rows):** examined reason strings for supplement adequacy.

### Limitations

- I did not open the referenced source-code files inside the repository beyond confirming a small sample of route filenames exist under `backend/routes/`. Behavioral or contract verification of those files is out of scope for this review and, per package methodology, out of scope for the package itself.
- I did not run the pytest-form validator test file; the standalone validator ran cleanly.
- External-authority citations in §6 are for the reader's context on what a mature governance program in this domain would normally include; they are not adoption recommendations.

---

## 3. Strengths supported by evidence

- **Explicit authority disclaimers are pervasive and consistent.** Every artifact carries `DOCUMENTARY_COVERAGE_ANALYSIS_ONLY_NO_ADOPTION_IMPLEMENTATION_DEPLOYMENT_PILOT_OR_PRODUCTION_AUTHORITY` and enumerates 18 specific "NO_X" statements. The `authority_confirmations` block in `DOCUMENTARY_VALIDATION_REPORT.json` records `false` for every activation flag. This is a real, verifiable strength.
- **Structural validator is real, deterministic, and passes.** Re-running `python3 validators/validate_master_product_feature_coverage_matrix.py` produced `DOCUMENTARY_VALIDATION_PASS feature_rows=314 source_rows=374`. `sha256sum -c CHECKSUMS.sha256` confirmed 32 file hashes.
- **Baseline commit exists in the referenced repository.** I confirmed via the GitHub API that `1eb384d80daa700ba2e71ee42872cc9bba926332` is a real commit on `rianray2012-coder/EquineSync-V4`, dated 2026-08-01.
- **Governance state / implementation state / readiness state are properly separated as fields.** Nowhere does the matrix conflate "PIA drafted" with "runtime verified".
- **Evidence lifecycle vocabulary is well-defined.** `IMPLEMENTED_UNVERIFIED`, `REPOSITORY_EVIDENCE_REFERENCED_NOT_BEHAVIOR_VERIFIED`, `RUNTIME_VERIFICATION_NOT_PERFORMED`, and related enums (visible in `FIELD_DICTIONARY.csv` for a handful of fields and in the methodology docs) accurately signal that no behavioral verification has occurred.
- **Dashboard counts reconcile.** I recomputed governance-state, implementation-state, risk-severity, and readiness-band distributions from `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv`; the numbers match `DASHBOARD_SUMMARY.md`, `COVERAGE_ANALYSIS_AND_RECOMMENDATIONS_REPORT.md`, and the main matrix Markdown.
- **PIA source-status honesty at the summary level.** `PIA_FEATURE_COVERAGE_SUMMARY.csv` openly records `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` for PIAs 02, 04, 05, 06, 07, 08, 09, 10 and `SUCCESSOR_TEXT_PENDING_FRESH_REVIEW` for PIAs 01 and 03. The package therefore contains the raw material needed to detect the internal inconsistencies I identify below.

---

## 4. Findings table

Severity legend: `BLOCKER` = must be corrected before Founder review is meaningful; `HIGH` = should be corrected before Founder disposition; `MEDIUM` = should be corrected in next revision; `LOW` = optional improvement.

| Finding ID | Severity | Affected files/fields/feature IDs | Evidence (reproducible) | Consequence | Required correction | Acceptance test |
|---|---|---|---|---|---|---|
| F-01 | BLOCKER | `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv`, column `Feature or workflow description`; all 314 rows | Regex `^Atomic coverage row for .+ within .+\.$` matches 314 / 314 rows. Word count: min 8, median 11, max 13, mean 10.6. | Descriptions do not state purpose, workflow, actors, data, or business outcome. The matrix is not a substantive feature inventory; every downstream semantic classification (personas, data classification, PIA mapping, gap type, risk) rests on the feature *name* alone. Founder decisions FDQ-002, 006, 007, 009, 011, 012 depend on this. | Replace each description with at least 40 words that name purpose, primary user, key data types, and business outcome, and cite the source of the intent (canon, PIA position, source register entry, or Founder directive). | Sampling 30 random rows shows unique, distinguishing descriptions per row; no row description substring is more than 30% shared with any other row's description. |
| F-02 | BLOCKER | Cross-file inconsistency: `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` (11 FULLY_COVERED rows) versus `GOVERNANCE_ARTIFACT_INVENTORY.csv` and `PIA_FEATURE_COVERAGE_SUMMARY.csv` | 7 of 11 FULLY_COVERED rows depend on a governing PIA with lifecycle `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` (PIAs 04, 05, 06, 08, 09, 10). The other 4 (Identity) depend on PIAs 01/03 in `SUCCESSOR_TEXT_PENDING_FRESH_REVIEW`. All 11 are `IMPLEMENTED_UNVERIFIED` with `REPOSITORY_EVIDENCE_REFERENCED_NOT_BEHAVIOR_VERIFIED` and `RUNTIME_VERIFICATION_NOT_PERFORMED`. | The `FULLY_COVERED` label is internally overstated. It contradicts the package's own PIA source-status data. Founder question FDQ-007 ("Should FULLY_COVERED require adopted governance, active governance, or documentary coverage only?") is not ripe because the current classification would fail its own criteria under any interpretation stricter than "documentary reference exists". | Either (a) demote all 11 rows to `COVERED_WITH_RETAINED_GAP` with an explicit `PIA_SOURCE_UNLOCATED` or `PIA_SUCCESSOR_PENDING` retained-gap tag; or (b) redefine `FULLY_COVERED` in `GOVERNANCE_LAYER_AND_READINESS_METHODOLOGY.md` to explicitly permit unlocated-PIA references and update the readiness cap rules to match. | No row is `FULLY_COVERED` while any governing PIA lifecycle contains `NO_PRIMARY_PIA_PACKAGE_LOCATED` or `SUCCESSOR_TEXT_PENDING_FRESH_REVIEW`; the validator enforces this. |
| F-03 | BLOCKER | `FIELD_DICTIONARY.csv` | 147 fields; 143 share the identical description "Matrix field retained or added for Founder-review traceability, planning, governance coverage, implementation evidence, or validation." Only 5 distinct descriptions across the file. 127 of 147 fields share the identical `controlled_values` string `FREE_TEXT_OR_SEMICOLON_LIST_AS_APPLICABLE`. No column in the dictionary contains type, ownership, derivation, null handling, or maintenance metadata. | The prompt's required question about the field dictionary defining "meaning, type, allowed values, source, ownership, derivation, null handling, and maintenance expectations" is not met. Downstream reviewers cannot tell what any given free-text field is supposed to contain, who owns it, how it is derived, or how nulls should be interpreted. | Replace each row's description with a field-specific meaning sentence, add columns `data_type`, `allowed_values`, `owner`, `derivation`, `null_handling`, `maintenance_expectation`, and populate for every field. | A random sample of 20 fields all have distinct descriptions, non-generic `controlled_values` where applicable, and populated new columns. |
| F-04 | HIGH | `RISK_PRIORITY_METHODOLOGY.md`, `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` columns `RISK_SEVERITY`, `RISK_LIKELIHOOD`, `RISK_SCORE` | Only 6 distinct `RISK_SCORE` values across 314 rows (12 = 141 rows, 8 = 130, 9 = 15, 16 = 15, 6 = 9, 4 = 4). No `LOW` severity anywhere. No `RARE` likelihood. `LIKELY` on 286 / 314 rows (91.1%). All 14 Incidents rows and `HORSE-008` are identical (`CRITICAL`/`LIKELY`/16). All 8 `FULLY_COVERED` "governance-ready" rows collapse to score 4 or 6. | Risk scoring does not meaningfully differentiate features. The severity/likelihood axes are declared to consider ~12 factors, but the observed collapsed distribution shows they were applied by broad rule of thumb, not per-feature analysis. The `FOUNDER_DECISION_QUEUE` and `IMPLEMENTATION_VERIFICATION_QUEUE` are both 314 items long — no queue sequencing signal is produced. | Rescore severity and likelihood per feature using the factors declared in the methodology, requiring per-row justification text in a new `RISK_RATIONALE` column. Expand likelihood to actively use `RARE` and `POSSIBLE` where governance gaps are compensated by containment. Expected outcome: a spread of at least 10 distinct scores; no single score value covers more than 25% of rows. | Distinct-`RISK_SCORE` count ≥ 10; no bucket > 25% of rows; every row has non-empty `RISK_RATIONALE` referencing at least two of the declared severity factors. |
| F-05 | HIGH | `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv`, `PIA_SUPPLEMENT_ROW_MAPPING.csv`, `PIA_FEATURE_COVERAGE_SUMMARY.csv` | 14 proposed supplements each target one or more of PIAs 01-10. Governance inventory records the primary PIA package as unlocated for 8 of those 10 PIAs and successor-pending for the remaining 2. Every supplement register row states `reason_supplement_is_insufficient = NOT_APPLICABLE_SUPPLEMENT_RECOMMENDED` and `reason_existing_pia_cannot_adequately_own_it = NOT_APPLICABLE_EXISTING_PIA_OWNER_IDENTIFIED` — yet the "existing PIA owner" is unlocated. Conflict `CONFLICT-002` in the conflict register already notes the source-identity problem. | The proposed 14 supplements cannot be drafted against parent PIAs whose primary text is not located. Founder question FDQ-002 ("Are the proposed fourteen PIA supplements the correct grouping?") conceals a prior blocker: the parents do not currently exist as located artifacts. This is a methodology-order defect, not merely a naming issue. | Insert a mandatory prerequisite step: `PIA source-identity reconciliation` (already named in `CONFLICT-002`) must produce located primary PIA packages for 02, 04, 05, 06, 07, 08, 09, 10 before supplement drafting can be usefully sequenced. Reorder Recommended Sequencing item 2 to depend on item 4. Add a `PARENT_PIA_SOURCE_STATE` column to the supplement register and mark rows blocked. | No supplement carries `SUPPLEMENT_EXISTING_PIA` while its parent PIA lifecycle is `NO_PRIMARY_PIA_PACKAGE_LOCATED`; the validator enforces this. |
| F-06 | HIGH | Absent domains across `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` and `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv` | Full-text scan across all 147 columns × 314 rows: `accessib*` = 0 hits; `WCAG` = 0; `SOC 2` = 0; `ISO 27` = 0; `GDPR` = 0; `CCPA` = 0; `HIPAA` = 0; `COPPA` = 0; `age verification` = 0; `background check` = 0; `third-party` = 0; `model govern*` = 0; `security assurance` = 0. `vendor` appears in 67 rows (inventory rows) but no `vendor risk` or `third-party risk` supplement is proposed. Only one AI-related governance grouping exists (`DOC-CG-AI-ASSISTED-WORKFLOW`, a Code Guide, not a PIA). | The prompt required proposed supplements or new PIAs for: Marketplace, Provider Network, Community, accessibility, safeguarding, vendor/third-party risk, AI/model governance, security assurance, regulatory mapping, records, and incident response. Only Marketplace/Provider Network/Community, care/incident operating standards, and one AI code guide are named. Accessibility, vendor risk, AI model governance, security assurance, and regulatory mapping are simply absent. Safeguarding appears as an inline concern but has no dedicated proposed artifact. Records retention appears as an inline canon reference but has no dedicated supplement. | Add proposed artifact candidates and matrix mapping columns for each of: accessibility (WCAG 2.2 / Section 508 alignment), vendor/third-party risk management, AI/model governance (aligned to NIST AI RMF or an equivalent framework), security assurance (SOC 2 Type I/II or ISO/IEC 27001), regulatory mapping (US federal-and-state privacy + COPPA + OSHA reporting), records retention (independent artifact, not only canon reference), and incident-response runbook family. Each new candidate needs `applicable_layers`, `affected_rows`, `founder_question`, and rank. | The proposed-artifact register contains at minimum: 1 accessibility artifact, 1 vendor-risk artifact, 1 AI governance artifact, 1 security-assurance artifact, 1 regulatory-mapping artifact, 1 records-retention artifact, and 1 incident-response runbook family. |
| F-07 | HIGH | `DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv` | Only 5 rows in the entire register. Rows `OVERLAP-003`, `OVERLAP-004`, `OVERLAP-005` each list 100+ Feature IDs concatenated with semicolons in a single `AFFECTED_FEATURE_IDS` cell. `CONFLICT-001` lists 16+ rows in one cell. Only `OVERLAP-005` mentions provider authority, which is the most actionable per-pair conflict area (Stripe vs. QuickBooks payment authority; Twilio SMS vs. push authority; identity provider IdP vs. account authority). | The prompt required conflict findings that are "granular, actionable, assigned, and supported." Multi-hundred-row semicolon lists cannot be triaged as discrete conflicts; they aggregate away the very pair-level information needed to route each to an owner. | Convert each of the 3 mass-overlap rows into a per-pair sub-register: one row per `(feature_A, feature_B, artifact_A, artifact_B, conflict_type, severity, proposed_resolution, owner, acceptance_test)`. Retain the mass rows as themes if desired, but they cannot be the operational conflict register. | Register has ≥ 50 per-pair conflict rows, each with two named features and a single-owner assignment. |
| F-08 | HIGH | `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` columns `IMPLEMENTATION_EVIDENCE_PATHS`, `IMPLEMENTATION_STATE`; 13 `NOT_FOUND` rows | All 13 `NOT_FOUND` rows still list repository evidence paths — commonly `frontend/src/pages/Integrations.jsx` — because the paths were assigned by keyword search on unrelated dashboards or listing screens. Sample: `ES-FEAT-INTEGRATIONS-002 QuickBooks` (NOT_FOUND) lists `frontend/src/pages/Integrations.jsx;frontend/src/pages/Expen…`. The path list is therefore not a signal of implementation state. Additionally, the 3 sentinel strings `exact collection-level ownership requires follow-up mapping`, `native app directories present`, and `feature-specific native implementation not verified by this matrix` appear as "evidence paths" on all 314 rows. | Repository-path evidence, per the package's own methodology, is meant to support only `IMPLEMENTED_UNVERIFIED`. Populating paths on `NOT_FOUND` rows undermines the methodology and could mislead the Founder into believing partial implementation exists. Sentinel strings in an evidence-path column further blur the signal. | Blank `IMPLEMENTATION_EVIDENCE_PATHS` for all `NOT_FOUND` rows, or move keyword-matched-but-unrelated paths to a new `KEYWORD_MATCH_NOISE_PATHS` diagnostic column. Move the 3 sentinel strings out of the evidence-paths column entirely into a new `EVIDENCE_LIMITATION_NOTES` column. | For every `NOT_FOUND` row, `IMPLEMENTATION_EVIDENCE_PATHS` is empty; no cell in `IMPLEMENTATION_EVIDENCE_PATHS` contains any of the 3 sentinel strings; validator enforces both. |
| F-09 | HIGH | `DEPENDENCY_REGISTER.csv`, `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` columns `DEPENDS_ON_FEATURE_IDS`, `BLOCKS_FEATURE_IDS`, `DEPENDENCY_BASIS`, `DEPENDENCY_CONFIDENCE` | 313 of 314 rows have `DEPENDENCY_BASIS = STRONGLY_INFERRED`; only 1 is `CONFIRMED`. The "313 downstream" blast radius comes from a single feature (`ES-FEAT-PLATFORM-001 application shell`). Four features (`COMMUNICATIONS-001`, `IDENTITY-001`, `RELATIONSHIP-001`, `TASKS-001`) each show identical 292 downstream blocks — an implausibly identical count that suggests templated fan-out rather than analysis. | The claim of "high-degree hubs: 8" and a "row affecting 313 downstream features" is nominally true but methodologically weak: the fan-out is inferred rather than confirmed, and the four 292-block rows appear synthetic. Founder decisions that rely on dependency-informed sequencing (FDQ-006, 011, 012) may be misprioritized. | Downgrade fan-out claims to "inferred blast radius" and add per-edge rationale in `DEPENDENCY_REGISTER.csv`. Convert at least the top 8 hubs into `CONFIRMED` edges via inspection of at least the entry points listed in `SOURCE_AND_AUTHORITY_REGISTER.csv`. | Top-8 hubs each have `DEPENDENCY_CONFIDENCE = CONFIRMED` for their outgoing edges; the four 292-block ties are broken with per-edge rationale distinguishing them. |
| F-10 | HIGH | `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` column `Affected personas`; `DASHBOARD_SUMMARY.md` persona table | Only 21 distinct `Affected personas` semicolon-lists exist across 314 rows despite the dashboard advertising 25 distinct personas. `Barn Manager` appears on 302 / 314 rows (96.2%), `Owner` on 273, `Trainer` on 270, `Guardian` on 242, `Staff` on 211. The lists show heavy repetition, suggesting per-domain persona templates rather than per-feature persona analysis. | Persona relevance is not being determined per feature. The purpose of persona mapping is lost when 96% of rows share a persona. | Add a `PERSONA_ASSIGNMENT_RATIONALE` column and require per-persona `PRIMARY / SECONDARY / OBSERVER` role per feature. Expect coverage to drop substantially and become useful. | No single persona appears on more than 60% of rows in the `PRIMARY` role; every row has `PERSONA_ASSIGNMENT_RATIONALE` populated. |
| F-11 | HIGH | `CODE_GUIDE_GAP_ANALYSIS.csv` | 49 rows, but the `expected_code_guide` value for every sampled row is the placeholder `ES-CG-00`. Notes on the sampled rows are identical templated strings: "Classification is documentary; Code Guide creation or activation requires se…". `existing_code_guide_should_be_amended` is `YES` and `new_code_guide_required` is `NO` on every sampled row — internally contradictory when the "existing" code guide id is a placeholder. | Founder question FDQ-006 ("Which Code Guide gaps should be drafted or amended first?") is not ripe: the register does not distinguish which existing Code Guide (out of the 14 in `GOVERNANCE_ARTIFACT_INVENTORY.csv`) is being amended, nor when a truly new Code Guide is needed. | Replace `ES-CG-00` with the actual expected Code Guide ID from the governance inventory for each row; where none applies, set `new_code_guide_required = YES` with a proposed ID. | For every Code Guide gap row, `expected_code_guide` matches an entry in `GOVERNANCE_ARTIFACT_INVENTORY.csv` (`artifact_class = CODE_GUIDE`) or is a new `DOC-CG-…` candidate with proposed scope. |
| F-12 | MEDIUM | `FOUNDER_DECISION_QUESTION_REGISTER.csv`, `README_FIRST.md`, and revision-status header | The main matrix Markdown declares status `REVISION_COMPLETE_READY_FOR_FOUNDER_REVIEW` and lists 10 Founder Review Questions plus 12 in the FDQ register. Given findings F-01 through F-11, questions FDQ-002 (PIA supplements), FDQ-003 (risk methodology), FDQ-006 (Code Guide sequencing), FDQ-007 (FULLY_COVERED standard), and FDQ-009 (authoritative baseline) are not ripe: they conceal unresolved evidence or methodology defects that must be corrected before a Founder disposition would be meaningful. | Founder decision cycles waste time and can produce dispositions the package cannot honor when the underlying data is corrected. | Mark FDQ-002, 003, 006, 007, 009 as `PREREQUISITE_CORRECTION_REQUIRED` in the FDQ register with pointers to the relevant findings above. Retain FDQ-001, 004, 005, 008, 010, 011, 012 as ripe. | Every FDQ row has a `RIPENESS` column with values `RIPE`, `PREREQUISITE_CORRECTION_REQUIRED`, or `DEFERRED_UNTIL_LATER_PHASE`. |
| F-13 | MEDIUM | `DASHBOARD_SUMMARY.md` "Release-Target Distribution" table | `RELEASE_TARGET` = `UNASSIGNED` on 314 / 314 rows (100.0%). | The declared release-planning fields carry no signal. Founder question FDQ-005 ("May MVP classifications and future release targets be used as planning assumptions?") is moot: there are none. | Either populate `RELEASE_TARGET` (and `MVP_CLASSIFICATION`) using stated criteria and rationale, or remove the fields from the matrix schema and the dashboard until they can carry signal. | Either 0 rows show `UNASSIGNED`, or the field is removed from schema/dashboard. |
| F-14 | MEDIUM | `Feature name` uniqueness across `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv` | 13 feature *names* recur across different domains: `disputes` (3), `financial reporting` (2), `recovery` (2), `correction` (2), `expiration` (2), `owner updates` (2), `service accounts` (2), `transfer` (2), `retention` (2), `escalation` (2), `consent` (2), `assignments` (2), `events` (2). Notable: `owner updates` appears in both `Lessons` and `Communications` and both rows are FULLY_COVERED with PIA supplement/coverage claims. | Ambiguity in the feature inventory. A reader cannot tell from `Feature name` alone which "owner updates" or "transfer" or "consent" they are looking at. | Add a domain-qualified `Feature name` column such as `owner updates (Communications)` versus `owner updates (Lessons)`, or require unique cross-domain `Feature name` values. | No duplicate `Feature name` across domains, or all duplicates are domain-qualified. |
| F-15 | LOW | `NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv` (314 rows, 25 columns) | The register mirrors the matrix row-for-row and produces 314 identically-shaped rows. It duplicates data already in the master matrix and is not, functionally, a compact non-PIA gap register. | Increased review burden; two artifacts to keep in sync; risk of drift. | Compress to only rows where `has_non_pia_governance_gap = YES` and add a top-level `SUMMARY_BY_GAP_TYPE` header. | Register has ≤ number of rows equal to rows with a non-PIA gap; a summary block is present. |
| F-16 | LOW | `ADVERSARIAL_REVIEW_RESULTS.csv` | 18 declared scenarios, all `PASS`. None of the scenarios target semantic issues surfaced by this review: templated descriptions, coarse persona lists, mass-conflict rows, unlocated-parent-PIA supplements, keyword-noise evidence paths. | The adversarial suite gives a false sense of substantive robustness. | Add adversarial scenarios ADV-19..ADV-25 for: templated-only description, ≤ 6 distinct risk scores, > 90% likelihood clustered on one value, `FULLY_COVERED` with unlocated-parent PIA, `NOT_FOUND` row with evidence paths, mass-`AFFECTED_FEATURE_IDS` conflict row (>20 IDs), placeholder Code Guide ID (`ES-CG-00`). | Validator implements and fails on synthetic examples for each new scenario. |

---

## 5. Separate analysis

### 5.1 Feature semantics

The 314-row inventory is well-partitioned across 22 product domains and uses a stable and hierarchical `ES-FEAT-<DOMAIN>-<NNN>` ID scheme (`FEATURE_TAXONOMY_AND_ID_REGISTER.csv` lists 22 `ES-FEAT-<DOMAIN>-000` domain-parent rows plus the 314 leaf rows, for 336 total). ID uniqueness holds (validator confirms). But at the semantic level:

- Descriptions are pure templates (F-01). Because the descriptions carry no content, every mapping — personas, data classification, PIA linkage, gap type — is anchored to the two-to-three-word `Feature name` alone. This is why the matrix produces implausible uniformities (F-04, F-10): the analysis has nothing feature-specific to differentiate on.
- Feature *names* are terse and 13 collide across domains (F-14).
- The description problem propagates into `Open gaps`, `Closure criteria`, and `Recommended owner` fields, which I sampled and found to be similarly templated.

### 5.2 Governance mappings

Governance-layer coverage is properly modeled with a nine-layer vector (PIA, Code Guide, ADR, operating standard, runbook, AI, safeguarding, privacy, reporting) each in a shared vocabulary of nine states. The overall `Governance coverage state` derivation is deterministic and documented. But:

- The `Governing PIA` field is mapped for every row despite the source register recording that 8 of the 10 governing PIAs are `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` (F-02, F-05).
- Applicable Code Guides, ADRs, operating standards, and runbooks are mapped chiefly to placeholder IDs (`ES-CG-00`, F-11).
- No mappings exist for accessibility, WCAG, AI/model governance beyond one code guide gap, security assurance, GDPR/CCPA/COPPA, records retention as independent artifact, incident-response runbook family, or vendor/third-party risk (F-06).

### 5.3 Evidence claims

The methodology's evidence lifecycle is disciplined in vocabulary: `IMPLEMENTED_UNVERIFIED`, `REPOSITORY_EVIDENCE_REFERENCED_NOT_BEHAVIOR_VERIFIED`, `RUNTIME_VERIFICATION_NOT_PERFORMED`, `TESTS_REQUIRED_BUT_ABSENT_OR_NOT_LOCATED_BY_KEYWORD_SEARCH`. Every row's runtime state is `RUNTIME_VERIFICATION_NOT_PERFORMED`, which is correct given the authority boundary.

But the *content* of evidence claims is contaminated:

- 3 sentinel strings are treated as evidence paths across 314 rows (F-08).
- Repository paths were populated by keyword search, so `NOT_FOUND` rows still list paths that keyword-matched but do not implement the feature (F-08).
- 68 tests are cited across two files (`backend/tests/test_operations_routes.py`, `backend/tests/test_operations_scoping.py`) but with `TEST_EXECUTION_STATUS = TESTS_REQUIRED_BUT_ABSENT_OR_NOT_LOCATED_BY_KEYWORD_SEARCH` — i.e. the test files may exist but were not executed to establish evidence.

Documentary, repository-discovered, test-verified, runtime-verified, and Founder-verified evidence are correctly separated as *categories*; the *content* of the repository-discovered category is the weak link.

### 5.4 Risk / readiness methodology

Methodology text is coherent: severity × likelihood, 12 declared factors, layer-weighted readiness with cap. Applied output is uniform (F-04):

- 6 distinct risk scores across 314 rows.
- 8 distinct readiness scores.
- 91% of rows are `LIKELY`.
- All 14 Incidents rows are identical (`CRITICAL / LIKELY / 16 / readiness 64`).
- All 11 governance-ready rows collapse to score 4 or 6.

The methodology does not distinguish features. Founder question FDQ-003 asks whether the weighting is acceptable; the more urgent prior question is whether the *application* of the weighting is per-feature at all. Nothing in the observed distribution supports the claim of per-feature analysis.

### 5.5 Dependencies

`DEPENDS_ON_FEATURE_IDS` and `BLOCKS_FEATURE_IDS` are populated. Distribution:

- 22 rows have 0 outgoing blocks; 292 rows have zero blocks; 8 hubs have between 15 and 313 blocks.
- 313 of 314 dependency inputs are basis `STRONGLY_INFERRED`; only 1 is `CONFIRMED`.
- The 313-block claim is entirely one row (`ES-FEAT-PLATFORM-001 application shell`).
- Four separate rows (`COMMUNICATIONS-001`, `IDENTITY-001`, `RELATIONSHIP-001`, `TASKS-001`) each show identical 292 downstream blocks — the identity of the number is implausibly consistent and suggests programmatic fan-out from a fixed rule (F-09).

Acyclicity holds (validator confirms). Dependency mappings are structurally clean but semantically inferred, and the fan-out claims should be reported as inferred (F-09).

### 5.6 PIA architecture

The 10 named PIAs plus the proposed 11th (Marketplace / Provider Network / Community) form the coverage denominator. But:

- PIA-02, PIA-04, PIA-05, PIA-06, PIA-07, PIA-08, PIA-09, PIA-10 have primary packages recorded as `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER`.
- PIA-01 and PIA-03 are `UNDERLYING_ITEM_01_DESIGN_APPROVED_SUCCESSOR_TEXT_PENDING_FRESH_REVIEW` and `UNDERLYING_COMPONENT_A_DESIGN_APPROVED_SUCCESSOR_TEXT_PENDING_FRESH_REVIEW` respectively.
- Every proposed supplement declares it is supplementing one of the above (F-05).

The proposed new-PIA candidate (Marketplace/Provider Network/Community) is coherent as a single-family grouping and I can see the argument for one new PIA (as the analysis document recommends). But it too rests on the denominator problem: it must not override PIA-03 permission, PIA-09 financial truth, and PIA-10 communications authority, per the register — yet those three cannot themselves be pointed at as authoritative located documents.

Additionally, the review prompt asked for special attention to Marketplace, Provider Network, Community, accessibility, safeguarding, vendor/third-party risk, AI/model governance, security assurance, regulatory mapping, records, and incident response. Only Marketplace/Provider Network/Community, incidents-as-operating-standard, and one AI code guide gap actually appear as proposed artifacts. Accessibility, vendor/third-party risk, AI governance as PIA or ADR, security assurance, regulatory mapping, and independent records retention are absent from the proposed-artifact family (F-06).

### 5.7 Field dictionary

Structurally covers 147 / 147 columns (F-03). Substantively covers ~4. Not fit for the purpose stated in the review prompt.

### 5.8 Conflict register

Only 5 conflicts, three of which enumerate 100+ Feature IDs each in a single cell (F-07). Not granular, not per-pair actionable, not assignable at the observed granularity.

---

## 6. External-source observations

External-authority anchors below are provided to illustrate what a mature governance program in EquineSync's operating context would normally include. They are not adoption recommendations, and they are not required to be adopted by this package. The relevant observation is that the matrix's proposed-artifact family does not currently name equivalents.

- **Privacy impact assessments and DPIAs:** The UK Information Commissioner's Office publishes methodology guidance for Data Protection Impact Assessments including screening criteria, scope, necessity, and consultation steps ([ICO Data Protection Impact Assessments guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/)). EquineSync's numbering scheme (PIA-01..PIA-10) uses "PIA" as a house term for domain-owning authority artifacts; wherever EquineSync collects UK/EU personal data, the DPIA framework would be a natural cross-check for structural completeness. This is relevant to F-03, F-05, and F-06.
- **AI risk management framework:** NIST publishes the AI Risk Management Framework (AI RMF 1.0) and a Generative AI Profile ([NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework); [NIST AI RMF 1.0 PDF](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf); [NIST GenAI Profile AI 600-1 PDF](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)). The matrix names one AI Code Guide gap (`DOC-CG-AI-ASSISTED-WORKFLOW`, 12 rows) and an AI implications sub-field on many rows but does not propose a PIA or ADR for AI/model governance. Relevant to F-06.
- **Children's data:** The FTC's COPPA Rule (16 CFR Part 312) applies to operators of online services directed to children under 13 or with actual knowledge of collecting children's personal information ([FTC COPPA Rule](https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa)). EquineSync's `Minor Rider` and `Guardian` personas are declared in the matrix, and 49 rows mention `minor` in some column, but the term `COPPA` does not appear anywhere. Relevant to F-06.
- **Workplace incident reporting:** OSHA requires notification within 8 hours for fatalities and within 24 hours for hospitalizations, amputations, or eye loss under 29 CFR 1904.39 ([OSHA Report a Fatality or Severe Injury](https://www.osha.gov/report)). All 14 Incidents-domain features are `CRITICAL / LIKELY / risk 16`, including `staff injury`. `ES-FEAT-INCIDENT-014 regulatory reporting` exists but does not name OSHA reporting timelines in the matrix I inspected. Relevant to §5.1 and F-06 (incident-response runbook family).
- **Accessibility:** WCAG 2.2 is the current W3C recommendation ([W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/)). Zero matrix rows or supplements name WCAG. Relevant to F-06.
- **Security assurance:** ISO/IEC 27001:2022 is the ISMS standard ([ISO/IEC 27001:2022](https://www.iso.org/standard/27001)) and SOC 2 Trust Services Criteria are published by the AICPA ([AICPA SOC 2](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2)). Neither term appears in the matrix. Relevant to F-06.

The purpose of these citations is to demonstrate that governance completeness at the level of "documentary coverage" cannot be judged purely by counting internal PIA/Code Guide/ADR/OS/runbook categories that the package itself defines. External frameworks that materially inform whether the coverage plan is *complete* are not represented in the current proposed-artifact family, and the review prompt explicitly asked for this cross-check.

---

## 7. Founder-decision readiness assessment

Ripeness of the 12 questions in `FOUNDER_DECISION_QUESTION_REGISTER.csv`:

| FDQ | Topic | Ripeness | Rationale |
|---|---|---|---|
| FDQ-001 | Marketplace PIA structure | **RIPE** | Clearly presented with 4 alternatives, tradeoffs, and a recommendation; 14 rows explicitly enumerated. Note: the recommendation depends on PIA-03/09/10 as authority owners, which have source-status issues, but the Marketplace decision itself is well-scoped enough to proceed. |
| FDQ-002 | PIA supplement grouping | **PREREQUISITE_CORRECTION_REQUIRED** | See F-05. Supplements name unlocated parent PIAs. |
| FDQ-003 | Risk methodology | **PREREQUISITE_CORRECTION_REQUIRED** | See F-04. Methodology text is acceptable in principle; the applied output is not usefully differentiated. |
| FDQ-004 | Readiness methodology | RIPE (with cautions) | Layer weights are declared; readiness bands are deterministic. The methodology can be approved as-is, provided the Founder understands that in the current package it produces 8 discrete scores across 314 rows. |
| FDQ-005 | Release planning assumptions | Moot as posed | 100% of rows are `UNASSIGNED` for `RELEASE_TARGET` (F-13). There is nothing to approve. |
| FDQ-006 | Code Guide sequencing | **PREREQUISITE_CORRECTION_REQUIRED** | See F-11. Every Code Guide reference is `ES-CG-00`. |
| FDQ-007 | Fully-covered standard | **PREREQUISITE_CORRECTION_REQUIRED** | See F-02. The 11 rows currently classified fail the interpretation the question is asking about. |
| FDQ-008 | Runtime verification later | RIPE | Reasonable to defer to a separate authorized phase. |
| FDQ-009 | Authoritative baseline | **PREREQUISITE_CORRECTION_REQUIRED** | Elevating a baseline that carries F-01, F-02, F-03, F-04, F-06 into an "authoritative baseline for governance-to-code conformity review" would freeze the defects. |
| FDQ-010 | Future planning dimensions | RIPE | Straightforward future-scope question. |
| FDQ-011 | Operating-standard gaps sequencing | RIPE (with cautions) | Incidents-domain enumeration is clear; sequencing can be decided with the risk-clustering caution. |
| FDQ-012 | Runbook gap sequencing | RIPE (with cautions) | Same as FDQ-011. |

Net: 5 of 12 Founder questions are not currently ripe. The package's own `Revision status: REVISION_COMPLETE_READY_FOR_FOUNDER_REVIEW` overstates readiness accordingly.

---

## 8. Required revisions versus optional improvements

### Required before Founder review (BLOCKER + HIGH)

Correct, in the order listed:

1. **F-01** Rewrite all 314 feature descriptions with per-feature semantics (purpose, primary user, key data, business outcome, source anchor). Downstream mappings must then be re-derived, not the other way around.
2. **F-02** Resolve `FULLY_COVERED` semantics: either demote current 11 rows to `COVERED_WITH_RETAINED_GAP` with a `PIA_SOURCE_UNLOCATED` retained-gap tag, or redefine `FULLY_COVERED` and re-apply the readiness cap rules.
3. **F-03** Replace the `FIELD_DICTIONARY.csv` with per-field meaning, type, allowed values, source, ownership, derivation, null handling, and maintenance metadata.
4. **F-05** Add `PIA source-identity reconciliation` as a prerequisite step; block supplement drafting on it. Add `PARENT_PIA_SOURCE_STATE` to the supplement register.
5. **F-06** Add proposed artifacts for accessibility, vendor/third-party risk, AI/model governance, security assurance, regulatory mapping, records retention, and incident-response runbook family. External anchors in §6 are illustrative of what "complete" would look like.
6. **F-04** Rescore severity, likelihood, and risk per feature with per-row `RISK_RATIONALE`.
7. **F-07** Convert mass-`AFFECTED_FEATURE_IDS` conflict rows into per-pair conflict rows.
8. **F-08** Clean `IMPLEMENTATION_EVIDENCE_PATHS`: blank for `NOT_FOUND`, no sentinel strings in that column.
9. **F-09** Confirm the top-8 dependency hubs; downgrade fan-out language.
10. **F-10** Re-derive `Affected personas` per feature with `PRIMARY / SECONDARY / OBSERVER` roles.
11. **F-11** Replace `ES-CG-00` placeholders with actual expected Code Guide IDs.

### Recommended in next revision (MEDIUM)

12. **F-12** Annotate FDQ ripeness in the Founder-decision register.
13. **F-13** Populate or remove `RELEASE_TARGET` and `MVP_CLASSIFICATION`.
14. **F-14** Deduplicate cross-domain `Feature name` collisions.

### Optional improvements (LOW)

15. **F-15** Compress `NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv` to only rows with gaps.
16. **F-16** Add adversarial scenarios ADV-19..ADV-25 to the validator for the semantic defect classes surfaced in this review.

---

## 9. Final disposition

`REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW`

Rationale: three BLOCKER findings (F-01 templated descriptions, F-02 `FULLY_COVERED` overstatement vs. own PIA source-status, F-03 non-substantive field dictionary) and eight HIGH findings materially defeat the substantive-correctness questions the review prompt required me to answer. The package's own `PIA_FEATURE_COVERAGE_SUMMARY.csv` and `DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv` (`CONFLICT-002`) contain the raw admission that 8 of 10 governing PIAs are unlocated, and the rest of the package builds coverage claims and supplement proposals on top of that unlocated denominator. Five of the twelve Founder-decision questions are not ripe (§7). Structural integrity is intact (validator, checksums, dashboard reconciliation), so this is not a `MATERIAL_RECONSTRUCTION_REQUIRED` case — the shell can be preserved and the semantic layer re-populated. But the current text is not ready for Founder review as the package claims.

---

## Appendix A. Reproducibility notes

All numeric claims in this report were computed against the exact bytes shipped in `EquineSync_Feature_to_Governance_Matrix_Perplexity_Cursor_Review_2026-08-03.zip`. Independent reviewers can reproduce every count as follows:

- Extract the zip; enter `MATRIX_PACKAGE/`.
- Run `python3 validators/validate_master_product_feature_coverage_matrix.py` (expects `DOCUMENTARY_VALIDATION_PASS`).
- Run `sha256sum -c CHECKSUMS.sha256` (expects all OK for 32 files).
- To reproduce F-01: `python3 -c "import pandas as pd, re; df=pd.read_csv('EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.csv',dtype=str).fillna(''); p=re.compile(r'^Atomic coverage row for .+ within .+\.$'); print((df['Feature or workflow description'].apply(lambda s: bool(p.match(s.strip())))).sum(), 'of', len(df))"`.
- To reproduce F-02: cross-tab `Governance coverage state == FULLY_COVERED` against `Governing PIA` lookup into `GOVERNANCE_ARTIFACT_INVENTORY.csv.lifecycle_state`.
- To reproduce F-04: `df[['RISK_SEVERITY','RISK_LIKELIHOOD','RISK_SCORE']].value_counts()`.
- To reproduce F-05: read `PIA_FEATURE_COVERAGE_SUMMARY.csv`, filter to `source_status` containing `NO_PRIMARY_PIA_PACKAGE_LOCATED`, list the resulting PIA IDs; then read `PROPOSED_NEW_PIA_AND_SUPPLEMENT_DECISION_REGISTER.csv` and confirm rows target those PIAs.
- To reproduce F-06: for each term in `[accessib, WCAG, SOC 2, ISO 27, GDPR, CCPA, HIPAA, COPPA, model govern, security assurance, third-party]`, count matching rows in the master CSV. All should return 0 or (for `third-party`) 0 explicit matches.
- To reproduce F-08: filter master CSV to `IMPLEMENTATION_STATE == NOT_FOUND` (13 rows) and inspect `IMPLEMENTATION_EVIDENCE_PATHS`; then count occurrences of the sentinel strings across all 314 rows (each appears exactly 314 times).
- External-source citations were fetched via public web search on 2026-08-03. URLs are stable public references.

---
End of report.
