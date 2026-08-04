# CURSOR_INDEPENDENT_REVIEW_FEATURE_TO_GOVERNANCE_MATRIX

**Artifact reviewed:** EquineSync Master Product Feature-to-Governance Coverage Matrix V1.0  
**Review package:** `EquineSync_Feature_to_Governance_Matrix_Perplexity_Cursor_Review_2026-08-03.zip`  
**Review type:** Independent repository-oriented technical and semantic review  
**Authority of this review:** `INDEPENDENT_DOCUMENTARY_REVIEW_ONLY` — no package modification, adoption, merge, activation, implementation, deployment, pilot, production use, certification, or automatic finding closure.

---

## 1. Executive conclusion and recommended status

The package is a coherent, checksum-sealed **documentary planning control plane** with strong mechanical integrity (CSV/JSON parity, score arithmetic, queue/count reconciliation, manifest/checksum enforcement). It is **not** yet a reliable semantic baseline for governance-to-code conformity review.

Validator and tests pass and catch many structural overclaims. They do **not** catch materially wrong but vocabulary-valid mappings, weak keyword-matched evidence paths, domain-templated risk, hub-templated dependencies, or mega-blob conflict entries. All 11 `FULLY_COVERED` rows remain `IMPLEMENTED_UNVERIFIED` with `RUNTIME_VERIFICATION_NOT_PERFORMED`; several cite weakly related repository paths under CODE_INSPECTED sampling.

**Final disposition:** `REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW`

---

## 2. Environment, commands run, files inspected, and limitations

### 2.1 Environment

| Item | Value |
| --- | --- |
| Review date | 2026-08-04 |
| Host workspace | `/workspace` (EquineSync-V4 checkout) |
| Workspace HEAD / branch | `1eb384d80daa700ba2e71ee42872cc9bba926332` on `integrate-emergent-final-zip` |
| Package baseline commit | `1eb384d80daa700ba2e71ee42872cc9bba926332` (matches workspace) |
| Authenticated review snapshot (package README) | `9ace3eed6b949d7e3ed38fcbfba21bcaec8e3991` |
| Python | 3.12.3 |
| pytest | not installed; tests run via package `__main__` runner |
| Isolated copy | `/tmp/matrix_isolated_repo/governance/portfolio/coverage/drafting/EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0` |

Repository access: **available**. Path checks below are labeled `PATH_CONFIRMED`, `CODE_INSPECTED`, `TEST_EXECUTED`, or `RUNTIME_VERIFIED` and are never collapsed.

### 2.2 Commands run and results

```bash
# Extract review ZIP (store-only archive)
unzip -o EquineSync_Feature_to_Governance_Matrix_Perplexity_Cursor_Review_2026-08-03_985e.zip

# Isolated repo-shaped copy (matches validator PACKAGE.parents[4] depth)
mkdir -p /tmp/matrix_isolated_repo/governance/portfolio/coverage/drafting
cp -a MATRIX_PACKAGE \
  /tmp/matrix_isolated_repo/governance/portfolio/coverage/drafting/EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0

cd /tmp/matrix_isolated_repo
PKG=governance/portfolio/coverage/drafting/EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0

PYTHONDONTWRITEBYTECODE=1 python3 $PKG/validators/validate_master_product_feature_coverage_matrix.py
# RESULT: DOCUMENTARY_VALIDATION_PASS
#         feature_rows=314
#         source_rows=374
#         exit=0

PYTHONDONTWRITEBYTECODE=1 python3 $PKG/tests/test_master_product_feature_coverage_matrix.py
# RESULT: VALIDATOR_TESTS_PASS
#         exit=0

cd $PKG && sha256sum -c CHECKSUMS.sha256
# RESULT: all listed entries OK

cd <review_zip_root> && sha256sum -c REVIEW_PACKAGE_CHECKSUMS.sha256
# RESULT: all listed entries OK
```

Adversarial probes (isolated copy; restored after each):

| Probe | Result |
| --- | --- |
| Append bytes to `README_FIRST.md` | Validator fails: manifest byte/sha + checksum mismatch |
| Delete `VERSION_CHANGE_REPORT.md` | Validator fails: manifest coverage / missing path |
| Change only `DASHBOARD_SUMMARY.json` `top_governance_blockers` to a nonexistent ID | Validator fails on hash/checksum (not on semantic content of blockers list) |
| Set `Governing PIA` to a different valid `PIA-*` on a supplement row | `validate_payload` returns **0** errors |
| Clear `BLOCKED_BY_FEATURE_IDS` while `DEPENDS_ON_FEATURE_IDS` remains set | `validate_payload` returns **0** errors |

Successful validator/test execution is **not** semantic approval.

### 2.3 Files inspected

All review-package files were opened or programmatically parsed, including:

- Outer: `REVIEW_PACKAGE_README.md`, both review prompts, `REVIEW_PACKAGE_CHECKSUMS.sha256`
- `MATRIX_PACKAGE/README_FIRST.md` and the full read-order set
- Authoritative `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0.{csv,json,md}`
- `FIELD_DICTIONARY.csv`, methodologies, `DOCUMENTARY_VALIDATION_REPORT.json`, `PACKAGE_MANIFEST.json`, `PACKAGE_METRICS.json`, `DASHBOARD_SUMMARY.{md,json}`
- Registers: sources, dependencies, queues, conflicts, PIA mapping, decisions, gaps, ungoverned, Code Guide gaps, adversarial results, taxonomy, founder questions, implementation summary
- `validators/validate_master_product_feature_coverage_matrix.py`, `tests/test_master_product_feature_coverage_matrix.py`

### 2.4 Limitations

- No product-feature tests were executed against the application (`TEST_EXECUTED` applies only to the matrix validator suite).
- No runtime / UAT / provider / staging verification (`RUNTIME_VERIFIED`: none).
- Source URIs `external-codex-attachment://…`, `FOUNDER_SUPPLIED_ATTACHMENT:…`, and `repository-search://…` (4 sources) are not filesystem-resolvable here.
- Bounded path sampling (97 feature rows), not exhaustive inspection of all 4,764 path-token citations.
- Package was not modified; probes used a disposable isolated copy.

---

## 3. Automated analysis results (reproducible counts)

### 3.1 Inventory and parity

| Metric | Count |
| --- | ---: |
| CSV feature rows | 314 |
| JSON `features` | 314 |
| Unique Feature IDs | 314 |
| CSV/JSON exact list equality | True |
| Columns (CSV = JSON `feature_columns` = field dictionary) | 147 |
| Product domains | 22 |
| Distinct personas (semicolon-split) | 25 |
| Source register rows | 374 |
| Queue rows | 1340 |
| Dependency register rows | 314 |
| Conflict register rows | 5 |
| Decision register rows | 15 (1 new-PIA + 14 supplements) |
| PIA supplement mapping rows | 179 |
| Ungoverned register rows | 26 |
| Code Guide gap rows | 49 |

### 3.2 Governance / implementation / risk / readiness

| Dimension | Distribution |
| --- | --- |
| Governance coverage state | PIA_SUPPLEMENT_CANDIDATE 179; CODE_GUIDE_GAP 49; OPERATING_STANDARD_GAP 25; ADR_GAP 16; RUNBOOK_GAP 16; NEW_PIA_CANDIDATE 14; FULLY_COVERED 11; COVERED_WITH_RETAINED_GAP 4 |
| Gap classification (parallel taxonomy) | Same as above except FULLY_COVERED→EVIDENCE_ONLY_GAP (11), COVERED_WITH_RETAINED_GAP→IMPLEMENTATION_ONLY_GAP (4) |
| Implementation state | IMPLEMENTED_UNVERIFIED 232; PARTIAL_IMPLEMENTATION 65; NOT_FOUND 13; DOCUMENTED_ONLY 4 |
| Risk severity | HIGH 163; MEDIUM 136; CRITICAL 15; **LOW 0** |
| Risk likelihood | LIKELY 286; POSSIBLE 17; UNLIKELY 11; **RARE 0** |
| Risk score | 12→141; 8→130; 16→15; 9→15; 6→9; 4→4 |
| Readiness band | PARTIAL_READINESS 285; LOW_READINESS 14; GOVERNANCE_READY 11; HIGH_READINESS_WITH_RETAINED_GAPS 4 |
| Founder decision state | PENDING **314** |
| Runtime verification | RUNTIME_VERIFICATION_NOT_PERFORMED **314** |
| Repo verification | REPOSITORY_EVIDENCE_REFERENCED_NOT_BEHAVIOR_VERIFIED **314** |
| Release target | UNASSIGNED **314** |
| Dependency confidence | STRONGLY_INFERRED 313; CONFIRMED 1 |

Dashboard JSON counts and `PACKAGE_METRICS.json` percentages independently recomputed from CSV rows: **match**.

### 3.3 Templating / repetition signals

| Field | Unique values / 314 | Observation |
| --- | ---: | --- |
| `ORIGIN_DOCUMENT` | 1 | All rows: `Backend Permission Capability Map` |
| `Required capability or authority basis` | 1 | Identical boilerplate on every row |
| `VERIFICATION_NOTES` | 1 | Identical disclaimer |
| `AUTHORITY_NOTES` | 1 | Identical planning disclaimer |
| `CHANGE_NOTES` | 1 | Identical revision note |
| `RELEASE_PLANNING_BASIS` | 1 | Identical unassigned disclaimer |
| `DEPENDENCY_BASIS` | 2 | Equals `DEPENDENCY_CONFIDENCE` on **314/314** rows (pure restatement) |
| `GAP_OWNER_EXPLANATION` | 4 | One template per owner enum |
| `BUSINESS_VALUE_RATIONALE` | 38 | Domain/risk template strings |
| Stock prose inside `IMPLEMENTATION_EVIDENCE_PATHS` | 314 rows | All three notes present on every row |
| Evidence path tokens | 3726 path-like / 1038 prose | Prose notes stored in a path field |
| Universal source IDs on all 314 rows | 12 | Including permission map, vision, PIAs, founder directives |
| Duplicate `Feature name` values | 13 names | e.g. `disputes`×3, `owner updates`×2, `financial reporting`×2 |
| Parent feature IDs | 22 synthetic `*-000` | **None** exist as matrix Feature IDs |

### 3.4 Dependency graph

| Claim / measurement | Result |
| --- | --- |
| Rows with ≥1 upstream dependency | **313** (matches package §10 wording; not “313 upstream edges on one row”) |
| Max upstream degree | **9** |
| Max downstream `BLOCKS_FEATURE_IDS` | **313** (`ES-FEAT-PLATFORM-001`) |
| Depend on `ES-FEAT-PLATFORM-001` | **313/313** non-roots |
| Depend on `ES-FEAT-IDENTITY-001` | 292 |
| Cycle detected (Kahn topo) | **No** (`314/314` ordered) |
| `DEPENDS_ON` ↔ `BLOCKS` inverse consistency | 0 errors |
| `DEPENDS_ON` ↔ `BLOCKED_BY` set mismatch | **10** rows (all current `FULLY_COVERED`) — `BLOCKED_BY` blank while depends populated |
| Unique `DEPENDS_ON` strings | 59 |
| Rows where `#deps == #distinct dep domains` | 116 (n=8), 89 (n=6), 64 (n=7) | Strong cross-domain-root templating |

### 3.5 Queues

Independently re-derived from matrix rules in the validator for all queues **except** `CONFLICT_RESOLUTION_QUEUE` (explicitly exempted). Counts match `DASHBOARD_SUMMARY.json`.

`CONFLICT_RESOLUTION_QUEUE` (116) equals `NON_PIA_DOCUMENT_AND_CONTROL_GAP_REGISTER.csv` where `conflict_gap=YES`, **not** a deterministic function of the five conflict entries’ affected-ID lists (those lists are 111 / 272 / 150 / 314 / 314).

### 3.6 Source path / hash check vs workspace

| Class | Count |
| --- | ---: |
| Filesystem sources with matching sha256 + byte_length | 370 |
| Hash mismatch | 0 |
| Path missing | 0 |
| Non-filesystem / attachment / search URIs skipped | 4 |

---

## 4. Manual semantic-review sample and results

### 4.1 All CRITICAL-risk rows (15/15)

All are `RISK_SEVERITY=CRITICAL`, `RISK_LIKELIHOOD=LIKELY`, `RISK_SCORE=16`, `IMPLEMENTED_UNVERIFIED`, domain-clustered:

| Feature ID | Name | Governance state |
| --- | --- | --- |
| ES-FEAT-HORSE-008 | emergency transfer | PIA_SUPPLEMENT_CANDIDATE |
| ES-FEAT-INCIDENT-001 … 014 | rider/staff/horse injury, medication error, loose horse, fire, weather, disease, quarantine, safeguarding, contacts, escalation, evidence, regulatory reporting | OPERATING_STANDARD_GAP |

**Semantic notes:** Likelihood `LIKELY` is applied uniformly to the entire incident domain gap set; severity is domain-templated (entire Incidents domain = CRITICAL). Path sample: every incident row cites `PersonalDashboard.jsx` (14/14) plus shared emergency pages — weak differentiation between “fire”, “quarantine”, and “disease exposure”.

`CODE_INSPECTED` (`EmergencyWorkflows.jsx`): emergency type options include `weather` / `injury` / etc.; no distinct fire, quarantine, or disease-exposure workflows found in that file’s type vocabulary. Label: **CODE_INSPECTED** (not behavior-verified).

### 4.2 All FULLY_COVERED rows (11/11)

| Feature ID | Name | Readiness | Impl state | Safeguarding layer |
| --- | --- | --- | --- | --- |
| ES-FEAT-PLATFORM-001 | application shell | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-PLATFORM-002 | role-aware navigation | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-PLATFORM-004 | search | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-IDENTITY-001 | person identity | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-IDENTITY-002 | accounts | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-IDENTITY-003 | authentication | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-IDENTITY-011 | roles and capabilities | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-HORSE-001 | horse profile | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-LESSONS-014 | owner updates | 94 | IMPLEMENTED_UNVERIFIED | COVERED |
| ES-FEAT-COMMUNICATIONS-004 | owner updates | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |
| ES-FEAT-FINANCIAL-017 | financial reporting | 94 | IMPLEMENTED_UNVERIFIED | NOT_APPLICABLE |

All share near-identical layer vectors (`PIA/Code Guide/Privacy/Reporting=COVERED`; ADR/OS/Runbook/AI usually `NOT_APPLICABLE`). Validator “FULLY_COVERED” checks are structural (score≥90, no GAP layer, no P0/P1 gap severity). They do **not** require behavior evidence, adopted governance, or non-keyword path relevance.

**CODE_INSPECTED examples:**

- `ES-FEAT-PLATFORM-004` cites `AdminBillingDashboard.jsx`: file has owner-email/barn-id **billing** search UI only — not a platform global-search capability. **PATH_CONFIRMED** + **CODE_INSPECTED**; semantic fit weak.
- `ES-FEAT-IDENTITY-003` cites `CareLedgerTab.jsx` / `AdminBillingDashboard.jsx`: auth context imports exist in CareLedgerTab; pages are not authentication implementations. **PATH_CONFIRMED** + **CODE_INSPECTED**; semantic fit weak.
- Duplicate name `owner updates` on LESSONS-014 and COMMUNICATIONS-004 both `FULLY_COVERED` — overlapping product identity without conflict decomposition.

Six `FULLY_COVERED` IDs also appear on `CONFLICT_RESOLUTION_QUEUE`, contradicting an intuitive reading of “fully covered.”

### 4.3 All new-PIA candidates (14/14)

Entire Marketplace domain; identical HIGH/12 / P0 / persona set / `PARTIAL_IMPLEMENTATION` / LOW evidence confidence. Decision analysis recommending one eleventh PIA is directionally plausible.

**Path semantics fail:** all 14 cite `frontend/src/pages/Signup.jsx`. No `Marketplace*` page exists. `Signup.jsx` contains onboarding commentary about a marketplace role pick — not provider listings, rankings, moderation, or disputes. **PATH_CONFIRMED** + **CODE_INSPECTED**; evidence does not support the attributed marketplace capabilities. `ES-FEAT-MARKETPLACE-006` (search ranking) also cites `Expenses.jsx`.

### 4.4 Stratified sample across all 22 domains

Sample of 97 features (all CRITICAL + FULLY_COVERED + NEW_PIA + first/middle/last per domain). Path-token status:

| Status | Features |
| --- | ---: |
| PARTIAL_PATH (some real paths + prose/notes) | 94 |
| PATH_MISSING / NOT_FOUND_BY_KEYWORD_SEARCH dominant | 3 (AI cluster) |

| Domain | Sample IDs | Path label | Notes |
| --- | --- | --- | --- |
| Platform and shell | PLATFORM-001/002/004 | PATH_CONFIRMED (partial) | Shell/nav paths real; search evidence weak |
| Identity and access | IDENTITY-001/002/003 | PATH_CONFIRMED (partial) | Auth/accounts path relevance weak |
| Relationships and guardianship | RELATIONSHIP-001/006/011 | PATH_CONFIRMED (partial) | PARTIAL_IMPLEMENTATION |
| Facility… | FACILITY-001/009/017 | PATH_CONFIRMED (partial) | |
| Horse identity… | HORSE-001/007/008 | PATH_CONFIRMED (partial) | HORSE-008 CRITICAL |
| Care operations | CARE-001/010/018 | PATH_CONFIRMED (partial) | |
| Lessons… | LESSONS-001/008/014 | PATH_CONFIRMED (partial) | LESSONS-014 FULLY_COVERED |
| Tasks… | TASKS-001/008/015 | PATH_CONFIRMED (partial) | TASKS-015 ADR_GAP |
| Communications… | COMMUNICATIONS-001/004/008 | PATH_CONFIRMED (partial) | |
| Documents… | DOCUMENTS-001/008/015 | PATH_CONFIRMED (partial) | |
| Financial… | FINANCIAL-001/010/017 | PATH_CONFIRMED (partial) | |
| Inventory… | INVENTORY-001/007/013 | PATH_CONFIRMED (partial) | |
| Incidents… | INCIDENT-001.. | PATH_CONFIRMED (partial) | Shared path cluster |
| Shows/events… | EVENTS-001/008/014 | PATH_CONFIRMED (partial) | |
| Marketplace… | MARKETPLACE-001..014 | PATH_CONFIRMED (partial) | Semantically weak citations |
| Media… | MEDIA-001/009/016 | PATH_CONFIRMED (partial) | |
| Reporting… | REPORTING-001/006/011 | PATH_CONFIRMED (partial) | OPERATING_STANDARD_GAP |
| Artificial intelligence | AI-001/007/012 | PATH_MISSING / DOCUMENTED_ONLY | Keyword search miss |
| Integrations… | INTEGRATIONS-001/009/016 | PATH_CONFIRMED (partial) | PARTIAL_IMPLEMENTATION |
| Mobile… | MOBILE-001/007/013 | PATH_CONFIRMED (partial) | MOBILE-001 NOT_FOUND |
| Admin/support… | ADMINOPS-001/009/016 | PATH_CONFIRMED (partial) | RUNBOOK_GAP |
| Developer platform… | DEVELOPER-001/007/012 | PATH_CONFIRMED (partial) | CODE_GUIDE_GAP |

**TEST_EXECUTED:** matrix validator suite only. **RUNTIME_VERIFIED:** none.

---

## 5. Findings table

| ID | Severity | Affected | Evidence | Consequence | Required correction | Verification test |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | BLOCKER | All 11 `FULLY_COVERED` rows; `Gap classification=EVIDENCE_ONLY_GAP`; methodologies | Rows labeled FULLY_COVERED / GOVERNANCE_READY while `IMPLEMENTATION_STATE=IMPLEMENTED_UNVERIFIED`, `RUNTIME_VERIFICATION_NOT_PERFORMED`, and several CODE_INSPECTED paths are only keyword-adjacent (PLATFORM-004, IDENTITY-003). Validator only checks score/layers/gap severity. | Founder may treat documentary FULLY_COVERED as conformity-ready coverage. | Rename or qualify state (e.g. `DOCUMENTARY_LAYERS_COMPLETE_UNVERIFIED`); require path-relevance attestation; exclude from GOVERNANCE_READY until evidence tier matches claim language—or change band vocabulary. | Assert FULLY_COVERED ⇒ evidence tier ∈ {REPOSITORY_VERIFIED,…} **or** assert label excludes “covered” without `DOCUMENTARY_` prefix; negative test with weak path + FULLY_COVERED. |
| F-02 | BLOCKER | Validator `validate_payload`; Governing PIA / Code Guide / persona / evidence-path fields | Changing `Governing PIA` to another valid `PIA-*` yields 0 errors. No semantic relevance check for evidence paths or personas. | Structurally valid, materially wrong mappings ship as PASS. | Add bounded semantic checks: PIA∈declared domain owners; evidence paths must be path-shaped; reject prose in path field; optional keyword/domain allowlists with explicit `KEYWORD_MATCH_ONLY` tier. | Unit test: wrong-but-valid PIA on CARE row → fail; prose token in `IMPLEMENTATION_EVIDENCE_PATHS` → fail. |
| F-03 | BLOCKER | `DUPLICATE_OVERLAP_AND_AUTHORITY_CONFLICT_REGISTER.csv` (5 rows); `CONFLICT_RESOLUTION_QUEUE` (116); OVERLAP-004/005 affect **314** features | Conflict entries are portfolio essays, not row-level findings. Queue membership exempted from matrix derivation (`!= CONFLICT_RESOLUTION_QUEUE`) and driven by opaque `conflict_gap=YES`. | Conflict work is not actionable per feature; dashboard understates/overstates simultaneously. | Decompose each conflict into row-level findings with exact proposition, artifacts, and disposition; derive queue strictly from those findings; remove validator exemption. | Test: conflict queue row must cite `conflict_id`+proposition; mega-list (>N features) without per-row clauses → fail. |
| F-04 | HIGH | Risk fields on all 314 rows; `RISK_PRIORITY_METHODOLOGY.md` | Severity almost entirely domain-constant (e.g. all Care=HIGH, all Incidents=CRITICAL, all Platform=MEDIUM). Likelihood = LIKELY for 286 rows and for **every** non-FULLY_COVERED gap state except four COVERED_WITH_RETAINED_GAP. Score is reproducible arithmetic on non-calibrated inputs. | Risk queues are not substantively meaningful for sequencing. | Recalibrate per-row severity/likelihood with written factors; forbid identical likelihood for entire governance-state classes unless justified; include LOW/RARE where warranted. | Test distribution entropy / max domain purity; fail if any domain is 100% one severity without override notes. |
| F-05 | HIGH | Dependency fields; `DEPENDENCY_REGISTER.csv`; PLATFORM-001 blocks 313 | Hub template: 313 depend on PLATFORM-001; many rows have `#deps=#dep-domains`; `DEPENDENCY_BASIS` restates confidence on 314/314. Useful as coarse planning sketch, not architecture. | Planning graph overstates coupling; max block count 313 is a root-label artifact. | Replace domain-root fan-out with explicit dependency types (hard/soft/data/authz); require prose basis ≠ confidence enum; document that PLATFORM-001 block count is “all non-roots.” | Test: `DEPENDENCY_BASIS == DEPENDENCY_CONFIDENCE` → fail; optional max soft-deps warning. |
| F-06 | HIGH | `IMPLEMENTATION_EVIDENCE_PATHS` all rows; Marketplace 001–014; Incidents | 1038 prose tokens stored as paths; 3 stock notes on 314/314 rows. Marketplace→Signup.jsx (14/14). Incidents→PersonalDashboard.jsx (14/14). | Implementation evidence tier overstates repository support. | Split notes into `EVIDENCE_LIMITATIONS`; require real paths only in path field; re-map marketplace/incident evidence or mark `NOT_FOUND` / `KEYWORD_MATCH_ONLY`. | Test: path field tokens must match `^[\w./-]+$` or equivalent; marketplace row citing only Signup.jsx → fail or force LOW+KEYWORD tier. |
| F-07 | HIGH | `ORIGIN_DOCUMENT`; Source IDs; authority propositions | All 314 rows claim origin `Backend Permission Capability Map` while also listing 12 universal sources. Source files hash-match workspace, but do not substantiate per-row propositions (permission map ≠ marketplace disputes, etc.). | Traceability is package-global, not row-propositional. | Require row-specific primary origin; limit universal sources to a separate `PACKAGE_CONTEXT_SOURCES` field. | Test: unique `ORIGIN_DOCUMENT` count ≪ domains → fail; or require `ORIGIN_SECTION` diversity. |
| F-08 | MEDIUM | `BLOCKED_BY_FEATURE_IDS` vs `DEPENDS_ON_FEATURE_IDS` on 10 FULLY_COVERED rows | Depends populated; blocked_by empty; validator ignores. | Dependency semantics inconsistent inside authoritative CSV. | Enforce set equality (or define and validate asymmetric meaning). | Unit test on PLATFORM-002 pattern → fail until fixed. |
| F-09 | MEDIUM | `FIELD_DICTIONARY.csv` | 127/147 fields `FREE_TEXT_OR_SEMICOLON_LIST…`; only 5 unique descriptions (mostly one generic sentence). Controlled vocabularies live in validator constants, not the dictionary. | Schema documentation does not agree in substance with validator enums. | Populate dictionary controlled values from validator allowlists; per-field descriptions. | Test: every validator allowlist field’s dictionary entry lists the same set. |
| F-10 | MEDIUM | Parent feature IDs `ES-FEAT-*-000` (22) | Referenced by all children; no such Feature IDs in matrix; validator does not resolve parents. | Taxonomy parents are unresolved identifiers. | Add parent rows, or mark parents as `TAXONOMY_ONLY` and exclude from feature-ID referential checks explicitly. | Test parent IDs resolve or carry taxonomy-only flag. |
| F-11 | MEDIUM | Duplicate feature names (13 collisions) | e.g. `disputes`×3 across relationship/financial/marketplace; dual `owner updates` both FULLY_COVERED. | Human review and queue readability errors. | Disambiguate names with domain qualifiers. | Test unique `(domain, name)` or globally unique names. |
| F-12 | MEDIUM | Tests vs ADV-16/ADV-18; `validate_authorized_paths` | Unit tests omit checksum/manifest, missing-file, fully-covered-overstatement, and stale non-count dashboard fields. `validate_authorized_paths` fails open (`except: changed=[]`). ADV CSV claims PASS for checksum tamper without a unit test. | Failure-behavior coverage is incomplete relative to adversarial register claims. | Add tests for manifest/checksum/missing file/FULLY_COVERED gap; make path-boundary check fail closed when baseline ref missing in CI. | New unit tests; CI without `origin/integrate-emergent-final-zip` must not silent-pass boundary check. |
| F-13 | MEDIUM | PIA supplement decision register (14 entries) | Near-identical boilerplate for risks/questions/lifecycle; all mapped rows readiness_score exactly **74** (STATE_CAP). | Supplement proposals are domain buckets, not capability-specific control needs. | Specialize per-supplement acceptance criteria and evidence requirements. | Spot-check: no two supplements share identical risk/lifecycle prose. |
| F-14 | LOW | Persona mappings | Barn Manager on 302/314; large repeated 7-persona templates. | Persona impact metrics are inflated/noisy. | Require primary persona + optional secondary; justify broad sets. | Test max personas/row or require `PERSONA_BASIS`. |
| F-15 | LOW | Effort estimate | 261/314 = `M`; entire domains uniform (Marketplace all L, Mobile all L, Adminops all M). | Effort not decision-grade. | Mark UNKNOWN unless estimated; or provide basis. | Optional. |
| F-16 | LOW | `DOCUMENTARY_VALIDATION_REPORT.json` / `DASHBOARD_SUMMARY.md` | Report not input to `validate_payload`; MD narrative not count-checked (JSON is). | Stale narrative possible if hashes regenerated together. | Include report expected check statuses; parse key MD tables or generate MD from JSON only. | Edit MD counts without JSON → fail, or drop MD as authoritative. |

---

## 6. Validator and test-suite assessment

### 6.1 What the validator detects well

- Required columns / non-blank (with dependency-field exceptions)
- Controlled vocabularies for core enums
- Duplicate Feature IDs
- Dependency ID resolution + cycle check
- Risk score = severity×likelihood weights
- Readiness score/band arithmetic (given STATE_CAP)
- Queue derivation (except conflict queue)
- Dashboard/metrics count reconciliation
- Unsupported Founder approval / verification / ACTIVE / runtime claims (structural)
- Manifest file set, byte lengths, sha256; checksum ledger
- Authority disclaimer string presence in selected files

### 6.2 Blind spots / circularity / weak vocabularies

- **Materially wrong valid mappings** (F-02).
- **FULLY_COVERED** is documentary-layer completeness, not semantic coverage (F-01).
- **`expected_governance_state`** is largely an encoding of `ACTION_ARTIFACT_TYPE` + layer GAP flags already on the row — confirms self-consistency, not independent truth.
- **STATE_CAP** binds 245/314 scores; readiness is capped by the same state it helps justify (mitigated because uncapped ≥90 also equals 11, but still state-tied).
- **Conflict queue exemption** (F-03).
- **`DEPENDENCY_BASIS`**, personas, origins, evidence path relevance unchecked.
- **`validate_authorized_paths`** fails open without git baseline ref.
- **Generated outputs:** hash detects byte drift; does not detect semantically stale blocker lists if ledger regenerated; does not parse `DOCUMENTARY_VALIDATION_REPORT.json` freshness against current validator results.

### 6.3 Tests

16 unit tests exercise many failure paths (good). Gaps vs ADV register:

| ADV claim | Unit test? |
| --- | --- |
| ADV-01..15 (most) | Yes (payload mutation tests) |
| ADV-16 fully covered overstatement | **No** dedicated test |
| ADV-17 unresolved gap | Covered by missing-owner test |
| ADV-18 checksum tamper | **No** unit test (only live `main()` path) |

Tests confirm current payload validity **and** several failure behaviors, but not the full adversarial surface advertised.

`TEST_EXECUTED` (validator suite): **PASS**.

---

## 7. Data-model, evidence-lifecycle, risk/readiness, dependency-graph, and governance-architecture assessments

### 7.1 Data model / schema agreement

CSV schema, JSON features, and field-dictionary **names** agree (147). Derivation rules in methodologies approximately match validator constants. Controlled vocabularies **do not** substantively appear in the field dictionary (F-09). Parallel taxonomies (`Governance coverage state` vs `Gap classification`) are easy to misread (FULLY_COVERED vs EVIDENCE_ONLY_GAP).

### 7.2 Evidence lifecycle

Methodology correctly separates path reference from behavior verification; all rows retain unverified runtime state. In practice, evidence paths conflate real files, `NOT_FOUND_BY_KEYWORD_SEARCH`, and limitation prose (F-06). Implementation states are therefore only as strong as keyword retrieval — **not** supported as behavior evidence. Source register hashes match this workspace baseline (good documentary seal); proposition support per row is weak (F-07).

### 7.3 Risk / readiness

Arithmetic is reproducible. Calibration is not (F-04). Readiness collapses ~91% of rows into PARTIAL_READINESS via caps — limited discrimination for planning.

### 7.4 Dependency graph

Acyclic and internally inverse-consistent for DEPENDS/BLOCKS. Credibility for planning is limited by universal PLATFORM hub and domain-root templates (F-05). The package’s “313 upstream dependency count” means rows-with-upstream=313; max downstream block=313 is real for PLATFORM-001.

### 7.5 Governance architecture proposals

- **New PIA (marketplace):** ownership rationale is sound; evidence underpinning the 14 rows is not (F-06).
- **14 PIA supplements:** sensible domain buckets; templated decision text and uniform score 74 reduce control specificity (F-13).
- **Code Guide / ADR / OS / runbook gaps:** counts are consistent with layer GAP flags; suitability depends on Founder accepting domain-level gap typing.
- **Conflicts:** must be decomposed before architecture use (F-03).

### 7.6 Suitability as future governance-to-code conformity baseline

**Not suitable yet.** Conformity baselines need proposition-level evidence, non-keyword path attestation, calibrated risk, decomposable conflicts, and labels that cannot be read as “covered” without verification. This package is a strong **draft inventory + gap accounting system** pending revision.

---

## 8. Founder-decision readiness assessment

The package already lists the right Founder questions (marketplace PIA structure, supplement groupings, scoring acceptance, FULLY_COVERED meaning, runtime phase, baseline adoption). However, **presenting it for Founder disposition now would ask the Founder to decide on labels and queues that overstate semantic certainty**.

Blocking issues before Founder review:

1. Re-label or requalify `FULLY_COVERED` / `GOVERNANCE_READY` (F-01).
2. Decompose conflicts / fix conflict queue derivation (F-03).
3. Clean evidence-path field and rematerialize marketplace/incident/search/auth evidence tiers (F-06, parts of F-01).
4. Document risk as uncalibrated **or** recalibrate (F-04) before asking Founder to “accept methodology.”

Non-blocking but should ship with any Founder packet: F-08, F-09, F-10, F-11, F-12, F-14–F-16.

---

## 9. Required revisions versus optional improvements

### Required before Founder review

1. Fix F-01 label semantics for FULLY_COVERED / GOVERNANCE_READY.
2. Fix F-02 validator blind spot for wrong-but-valid mappings + path-field hygiene.
3. Fix F-03 conflict decomposition and queue derivation.
4. Fix F-06 evidence path contamination and marketplace/critical weak citations.
5. Either recalibrate F-04 risk or explicitly mark scores `UNCALIBRATED_PLANNING_ONLY` in every row and strip risk-ordered “top blockers” framing from Founder summary.
6. Align ADV register with actual unit tests (F-12) for checksum and FULLY_COVERED overstatement.

### Optional improvements

- Disambiguate duplicate names (F-11); resolve parent IDs (F-10); enrich field dictionary (F-09); tighten personas/effort (F-14/F-15); generate MD dashboards solely from JSON (F-16); enrich dependency basis prose (F-05).

---

## 10. Final disposition

**REVISION_REQUIRED_BEFORE_FOUNDER_REVIEW**

---

*End of independent review. Matrix package bytes were not modified. This report confers no adoption, merge, activation, implementation, deployment, pilot, production, or certification authority.*
