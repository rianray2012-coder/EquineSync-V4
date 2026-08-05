# EquineSync Tier 1 Docs 03–10 — V3 Outside Review Report

**Reviewer role:** Independent adversarial documentary/technical review (Cursor)  
**Review date (UTC):** 2026-08-04  
**Package reviewed:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V3_REVIEW_FINDINGS_REMEDIATION_CANDIDATE`  
**User path (not present in cloud uploads):** `/Users/rianray/Documents/Codex/2026-08-01/fi/outputs/EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V3_REVIEW_FINDINGS_REMEDIATION_CANDIDATE.zip`  
**Closest authenticated artifact:** PR #90 head `b6e98e0002451e49edebbf41175322ab3d151398` (`codex/tier-1-docs-03-10-outside-review-remediation-20260804`)

---

## Authentication

| Item | Value |
|---|---|
| ZIP path (repo) | `governance/portfolio/tier-1/drafting/EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V3_REVIEW_FINDINGS_REMEDIATION_CANDIDATE.zip` |
| ZIP SHA-256 | `ad8805d5edb18e90ea6b838c75a77a162376e198e39b5b25ffca7b456d5bf785` |
| ZIP bytes | `2711586` |
| Detached `.sha256` | **MATCH** |
| `unzip -t` | **OK** |
| Handoff report SHA | Same as above |
| Source reviews authenticated | Perplexity `5375a015…` / 18250 B; Claude duplicate inputs byte-identical `f305cc7f…` / 13702 B |

Preserved authority boundary (unchanged; required):  
`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

**No adoption, activation, implementation, production use, merge, certification, risk acceptance, or finding closure is authorized by this review.**

---

## Disposition

### `REVISION_REQUIRED`

The V3 package is a **material honesty and integrity upgrade** over prior RR2 / V2 remediation states, and its **own package status is correctly revision-required pending outside rereview**. Independently, **blocking substance defects remain open**, most importantly Doc10 template body identity (`T1C-004`) and the Doc10 prose contradiction that overclaims those templates. Doc03 remains candidate-only with ~40 non-requirement source fragments still in the register (`T1C-006`). Founder residual-risk disposition is correctly unclosed (`T1C-003`).

This review **agrees** with the package’s `REVISION_REQUIRED_PENDING_*` self-status and **does not** elevate the package to Founder directional “ready.”

---

## Validator results (this environment)

| Check | Result |
|---|---|
| `validate_tier1_documents_03_10_v3.py` | **PASS / 0 failures** |
| `validate_tier1_documents_03_10_rr2.py` (package-only) | **PASS / 0 failures** |
| `execute_negative_fixtures_v3.py "$ROOT"` (positional) | **PASS** (11 fixtures) |
| `execute_negative_fixtures_v3.py --package-root "$ROOT"` | **FAIL** — treats `--package-root` as a path (`FileNotFoundError`) |

Structural PASS is **not** substance clearance. Notably, the duplicate-template negative fixture only compares two strings inside `duplicate_templates.json`; it does **not** hash the 19 live templates under `10_CLOSING_AUDIT_PROTOCOL/templates/`.

Retained validation report `package_root` points at a macOS local path (consistent with open `T1C-020`).

---

## T1C register assessment (package self-disposition)

| Disposition | Count |
|---|---|
| `REMEDIATED_IN_V3_PENDING_REREVIEW` | 11 |
| `VALID_OPEN_RETAINED` | 7 |
| `NOT_REMEDIATED_RETAINED_OPEN` | 1 (`T1C-004`) |
| `RETAINED_NONBLOCKING_OPEN` | 1 (`T1C-020`) |
| `second_reviewer_state` | all `NOT_PERFORMED_NOT_FABRICATED` |

**Independent verdict on remediations claimed pending rereview:**

| ID | Sev | Package claim | Independent view |
|---|---|---|---|
| T1C-001 | BLOCKING | Remediated pending rereview | **Accept pending** — integrity chain/manifests/checksums rebuilt; ZIP SHA authenticates |
| T1C-002 | BLOCKING | Remediated pending rereview | **Accept pending** — 13-state wording present; FD posture preserved |
| T1C-003 | BLOCKING | Valid open retained | **Agree open** — no Founder residual-risk disposition |
| T1C-004 | BLOCKING | **Not remediated** retained open | **Agree open / still blocking** — see VR3-001 |
| T1C-005 | BLOCKING | Remediated pending rereview | **Accept pending with residual** — labels scoped; path/disposition conflict remains (VR3-004) |
| T1C-006 | BLOCKING | Valid open retained | **Agree open** — candidates only; ~40 non-req texts remain |
| T1C-007 | HIGH | Remediated pending rereview | **Accept pending** — source-review IDs populated; closure register distinct |
| T1C-008 | HIGH | Remediated pending rereview | **Accept pending with caveat** — fixtures execute when CLI used correctly; live template identity not gated |
| T1C-009 | HIGH | Remediated pending rereview | **Accept pending** — all FD `NO_DISPOSITION_SELECTED` / `NONE_BY_THIS_PACKAGE` |
| T1C-010 | HIGH | Valid open retained | **Agree open** |
| T1C-011–012,015,017–018 | MED/LOW | Remediated pending rereview | **Accept pending** (mechanical) |
| T1C-013–014,016,019–020 | MED/LOW | Open retained | **Agree open** |

---

## New / confirmed review findings (VR3)

### VR3-001 — BLOCKING — Doc10 templates still one generic body; narrative overclaims

**Evidence**

- All 19 files under `10_CLOSING_AUDIT_PROTOCOL/templates/` share **one identical body** after stripping H1 + `Template name` (normalized body hash count = **1**).
- Shared outline: Document Control, Purpose, Scope, Authority, Evidence Population, Determinations, Mandatory Evidence Table (EXAMPLE only), Exceptions, Prohibited Conclusions, Sign-Off.
- `TEMPLATE_PURPOSE_SPECIFICITY_EVIDENCE_TABLE.csv`: all 19 → `CLUSTER-GENERIC-001`, `INSUFFICIENT_CURRENT_EVIDENCE_TO_CLOSE`, `T1C-004_NOT_REMEDIATED_RETAINED_OPEN`.
- Doc10 principal narrative still states: **“The 19 templates are structurally distinct and area-specific.”**

**Conflict**

- T1C register + evidence table correctly refuse closure.
- Principal Doc10 prose and legacy `EXTERNAL_REVIEW` row **F-02 = `REMEDIATED`** overclaim relative to that evidence.

**Required before any “ready” claim**

1. Rewrite each template with purpose-specific mandatory fields/evidence columns/determinations (not title-only uniqueness).  
2. Align Doc10 narrative and F-02 disposition with `T1C-004` / evidence table.  
3. Gate validators on **normalized body uniqueness / similarity**, not fixture JSON self-equality or name uniqueness alone.

---

### VR3-002 — HIGH — Package status / readiness string drift

| Surface | Status string |
|---|---|
| `README_FIRST.md` title | Still **“V2 Outside Review Remediation Candidate”** (folder/ZIP are V3) |
| `README_FIRST.md` / T1C / V3 summary | `REVISION_REQUIRED_PENDING_*` (**correct**) |
| `TIER_1_DOCUMENT_INVENTORY.csv` (all 8 docs) | `REVISION_ROUND_2_COMPLETE_READY_FOR_FOUNDER_DIRECTIONAL_AND_FINAL_DOCUMENTARY_REVIEW` (**stale / too strong**) |
| Doc03–10 principal readiness lines | `...EXTERNAL_REVIEW_REMEDIATED_READY_FOR_FOUNDER...` (**too strong** vs open blockers) |
| `CROSS_DOCUMENT_RECONCILIATION_REPORT.md` | Same “REMEDIATED_READY…” status |

Inventory/cross-recon “COMPLETE/READY” contradicts open BLOCKING T1C rows and the package’s own revision-required banner.

---

### VR3-003 — MEDIUM — Shared standard Authority Boundaries incomplete + duplicated section

- Authority Boundaries lists **6 of 8** preserved tokens; missing `FOUNDER_REVIEW_REQUIRED` and `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED` (present on README/boundary banners elsewhere).
- “External Standards Terminology Note” section is **triplicated** verbatim at end of shared standard.

---

### VR3-004 — MEDIUM — `docs/canon/candidates/*` still `authoritative current source`

Exactly **4** residual rows (prior OR-008 / remediation feedback):

| source_id | path class | source_disposition | authority_state |
|---|---|---|---|
| SRC-RR2-00265 | `docs/canon/candidates/...` | authoritative current source | `SOURCE_CONTAINS_FOUNDER_APPROVAL_EVIDENCE_NOT_PACKAGE_ADOPTION` |
| SRC-RR2-00266 | same | authoritative current source | same |
| SRC-RR2-00268 | same | authoritative current source | `SOURCE_CONTAINS_ADOPTION_OR_LOCK_EVIDENCE_NOT_PACKAGE_ADOPTION` |
| SRC-RR2-00275 | same | authoritative current source | same |

Authority **labels** improved (non-adoption scoping). Path-class vs `authoritative current source` disposition remains contradictory for candidate-tree paths.

---

### VR3-005 — MEDIUM — Validator / negative-fixture blind spots

1. Live templates with identical normalized bodies still **PASS** RR2/V3 validators (name count only).  
2. `duplicate_templates.json` fixture does not inspect package templates.  
3. `execute_negative_fixtures_v3.py` does not accept `--package-root` (brittle CLI).  
4. Structural PASS must not be read as closure of T1C-004 / Doc03 substance / production evidence.

---

### VR3-006 — MEDIUM — Doc03 non-requirement source texts unchanged (honesty-only)

- All 96 rows correctly `SOURCE_TEXT_CANDIDATE` / `NOT_ACCEPTED_AS_REQUIREMENT` (keep).  
- ~**40/96** texts remain JSON fragments, table cells/headers, comments, or meta-instructions (e.g. `T1R2-REQ-0002`, `0003–0012`, `0047–0072`, `0075–0076`).  
- Aligns with open **T1C-006**; do not treat Doc03 as a usable normative inventory.

---

### VR3-007 — LOW/MEDIUM — Residual thinness / stubs / naming debt

- Principal Doc 03–10 markdown bodies remain ~0.7–1.4 KB (supports open **T1C-016**).  
- Doc06: 9 findings; **one shared** `severity_rationale` for all rows (**T1C-014**).  
- `UNRESOLVED_ISSUE_REGISTER.csv`: 28 stub `T1R2-EXT-F-*` rows with near-identical descriptions pointing at external register.  
- Doc10 path/filename still contains `BOUNDED_CERTIFICATION_PACKAGE` while body uses self-declaration terminology (**T1C-015** partial).  
- Doc09 lists PRs `{29,67–70,77,80–82}` only — omits remediation PRs **#83 / #84 / #90** (**T1C-013**). Spot-check: PR #82 `head_sha` still matches live `7748c477…`.

---

## What V3 did well (keep)

1. Honest package status: `REVISION_REQUIRED_PENDING_*`; does not self-close high-consequence findings.  
2. Explicit `T1C-004 = NOT_REMEDIATED_RETAINED_OPEN` + purpose-specificity evidence table admitting `CLUSTER-GENERIC-001`.  
3. Integrity rebuild: manifests, `MANIFEST_OF_MANIFESTS.csv`, root checksums, detached ZIP SHA.  
4. Source-review authentication record with real hashes/IDs; distinct closure-evidence register.  
5. FD posture preserved (`NO_DISPOSITION_SELECTED`, `NONE_BY_THIS_PACKAGE`, no recommended option selected).  
6. Lifecycle 13-state wording; calendar `NOT_OPERATIVE_PENDING_APPOINTMENT`.  
7. Negative fixtures present and executable (positional package root).  
8. Second-reviewer boundary not fabricated (`NOT_PERFORMED_NOT_FABRICATED`).  
9. Doc03 narrative correctly refuses “accepted requirements” claim.

---

## Recommended next remediation (bounded)

**Must fix for any post-rereview “ready” consideration**

1. **T1C-004 / VR3-001:** purpose-specific template bodies + remove Doc10 “structurally distinct” claim + correct F-02 if still `REMEDIATED`.  
2. **VR3-002:** align README title (V3), inventory readiness, principal Doc readiness, and cross-recon status with `REVISION_REQUIRED_*` while blockers remain.  
3. Keep **T1C-003 / T1C-006 / T1C-010** open until Founder/substance work actually closes them — do not self-close.

**Should fix**

4. Shared standard: all 8 tokens in Authority Boundaries; dedupe triplicated note.  
5. Relabel four `candidates/` authoritative rows or move out of candidate tree with evidence.  
6. Validator: fail on normalized template-body identity; fix negative-fixture CLI.  
7. Quarantine obvious Doc03 non-requirements into a reject/noise register.  
8. Refresh Doc09 to include current remediation PRs or mark capture as incomplete/time-bound.

---

## Bottom line

V3 is the strongest **process-honest** remediation package in this series: it admits what it did not fix, authenticates source reviews, and rebuilds integrity artifacts. It is **not** substantively ready for Founder directional clearance while Doc10 templates remain a single generic shell under an overclaiming narrative, Doc03 remains an unfiltered candidate scrape, and residual-risk Founder disposition is unclosed.

**Outside-review disposition: `REVISION_REQUIRED`.**

Authority boundary preserved exactly as required.
