# EquineSync Tier 1 Docs 03–10 — V4 Bounded Rereview Adjudication

**Reviewer role:** Independent outside adjudication (Cursor)  
**Review date (UTC):** 2026-08-04  
**Package:** `EQUINESYNC_TIER_1_DOCUMENTS_03_10_REVISION_ROUND_2_V5_ADJUDICATION_INCORPORATION_CANDIDATE`  
**User paths (local):** ZIP + detached `.sha256` under `.../fi/outputs/`  
**Authenticated artifact:** Draft PR #90 tip `8b8f7a57551dd80f37f479dd72a129f41db2e14f`

---

## Authentication

| Item | Value |
|---|---|
| ZIP SHA-256 | `7070c863890cd1a6fc3938256588602d9eaf71164a3dd53ef268a931835f482a` |
| ZIP bytes | `2763428` |
| Detached `.sha256` | **MATCH** |
| `unzip -t` | **OK** |
| Predecessor (V3) SHA | `ad8805d5…` / `2711586` (recorded in README) |
| Authenticated V3 reviews | Perplexity `0b5f16db…`; Claude `5e4666b1…`; Cursor V3 report `b4659e4f…` |

Authority boundary preserved:  
`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`.

This adjudication does **not** authorize adoption, activation, implementation, production use, merge, certification, waiver, risk acceptance, or Founder approval.

---

## Verdict

### Packaging posture: **ACCEPTED**

`PACKAGING_READY_FOR_BOUNDED_REREVIEW` is justified.

### Content posture: **CONTENT_REVISION_REQUIRED** (retained)

Open substantive T1C rows remain (Founder residual risk, Doc03 verification, production evidence, depth/staleness items). Package self-status and V4 validator status are truthful.

### Validator posture: **ACCEPTED**

| Check | Result |
|---|---|
| Authoritative `validate_tier1_documents_03_10_v4.py --package-root` | `STRUCTURAL_PASS_SUBSTANTIVE_CLOSURE_BLOCKED` / 0 failures |
| `execute_negative_fixtures_v4.py --package-root` | **PASS** (5 mutated-package fixtures) |
| Legacy v2 / v3 / rr2 | `NON_OPERATIVE_HISTORICAL` |
| Retained report status | Same structural/blocked status |

Handoff claim of single authoritative V4 validator + truthful blocked-closure semantics is **confirmed**.

---

## Doc10 / T1C-004 adjudication (primary ask)

### What changed in V4

- All **19** templates rewritten as `V4_PURPOSE_SPECIFIC_DRAFT`.
- After stripping H1 + `Template name`, bodies are **19 unique** (was **1** in V3).
- **Purpose** unique across 19; **Required Evidence Fields** unique across 19.
- Shared control-floor text remains for Scope Boundary / Collection Method / Required Determinations (1 shared each) — acceptable common floor, not identity collapse.
- Evidence table assigns `V4-PURPOSE-SPECIFIC-NN` clusters; disposition `T1C-004_AUTHORED_IN_V4_PENDING_INDEPENDENT_ADJUDICATION`.
- Doc10 narrative no longer claims “structurally distinct” while evidence said otherwise; it states rewrite + dispute pending adjudication.
- Legacy **F-02** correctly reopened to `REOPENED_V4_TEMPLATE_PURPOSE_SPECIFICITY_PENDING_INDEPENDENT_ADJUDICATION` (not falsely `REMEDIATED`).
- V4 validator gates `distinct_doc10_normalized_template_bodies` and negative fixture `doc10_template_body_collapse`.

### Independent adjudication

| Question | Decision |
|---|---|
| Was the prior identical-body / non-specificity **blocking defect** remediated? | **YES** |
| Are templates purpose-distinguishable enough for documentary use? | **YES** (via unique Purpose + required fields) |
| May T1C-004 substance be **accepted** by outside reviewer? | **YES — ACCEPT remediation** |
| May the package **self-close** T1C-004? | **No** (correctly left open for adjudication) |
| Does acceptance authorize certification / closing audits? | **No** |

**Recommended register update after this adjudication:**  
`T1C-004` → `REMEDIATED_IN_V4_ACCEPTED_BY_OUTSIDE_REVIEWER` with evidence pointers to the 19 templates + purpose-specificity table + this report. Closure still requires package owners to record that acceptance; this review does not mutate PR #90.

**Residual (nonblocking for Doc10 identity):** Doc10 path/filename still contains `BOUNDED_CERTIFICATION_PACKAGE`; body terminology is self-declaration-correct.

---

## Doc03 / T1C-006 adjudication

### What changed

- **51/96** rows retyped `REJECTED_SOURCE_FRAGMENT_NOT_REQUIREMENT` / `REJECTED_NOT_A_REQUIREMENT`.
- Quarantine register `NON_REQUIREMENT_SOURCE_FRAGMENT_QUARANTINE.csv` present (51 rows); rejected IDs retained in main register for custody (correct).
- **45** remain `SOURCE_TEXT_CANDIDATE` / `NOT_ACCEPTED_AS_REQUIREMENT`.
- Readiness string moved off “READY_FOR_FOUNDER…”.

### Independent adjudication

| Question | Decision |
|---|---|
| Is fragment-noise honesty remediation sufficient? | **YES — ACCEPT quarantine remediation** |
| Is Doc03 an independently verified requirement baseline? | **NO** |
| May T1C-006 close? | **NO — retain OPEN** |

**Defect retained (should fix in next content pass):** Doc03 principal narrative still says every row is typed `SOURCE_TEXT_CANDIDATE`, which is now false (51 rejected). Align narrative to the dual typing model.

`T1R2-REQ-0001` (meta coding-prompt instruction) remains a candidate, not quarantined — acceptable judgment call; still not a verified requirement.

---

## Pending-remediated T1C findings — accept / withhold

Outside-reviewer acceptance means: evidence is sufficient to treat the defect as remediated for rereview purposes. It does **not** mean Founder adoption or merge authority.

| ID | Sev | Package state | Adjudication |
|---|---|---|---|
| **T1C-001** | BLOCKING | Remediated pending rereview | **ACCEPT** — integrity chain / manifests / ZIP SHA bind |
| **T1C-002** | BLOCKING | Remediated pending rereview | **ACCEPT** — 13-state wording; FD posture clean |
| **T1C-003** | BLOCKING | Valid open retained | **KEEP OPEN** — no Founder residual-risk disposition |
| **T1C-004** | BLOCKING | Open pending Doc10 adjudication | **ACCEPT remediation** (see above); update register |
| **T1C-005** | BLOCKING | Remediated pending rereview | **ACCEPT** — candidate-tree rows no longer `authoritative current source` |
| **T1C-006** | BLOCKING | Valid open retained | **KEEP OPEN** — candidates/quarantine ≠ verified requirements |
| **T1C-007** | HIGH | Remediated pending rereview | **ACCEPT** — source-review IDs + distinct closure register |
| **T1C-008** | HIGH | Remediated pending rereview | **ACCEPT** — V4 authoritative; fixtures mutate package; status not bare PASS |
| **T1C-009** | HIGH | Remediated pending rereview | **ACCEPT** — all FD `NO_DISPOSITION_SELECTED` / `NO_RECOMMENDATION_SELECTED` |
| **T1C-010** | HIGH | Valid open retained | **KEEP OPEN** — no production/deployment evidence columns/claims closed |
| **T1C-011** | MEDIUM | Remediated pending rereview | **ACCEPT** |
| **T1C-012** | MEDIUM | Remediated pending rereview | **ACCEPT** |
| **T1C-013** | MEDIUM | Valid open retained | **KEEP OPEN** — PRs 83/84/90 present as time-bound captures, not live-verified |
| **T1C-014** | MEDIUM | Valid open retained | **KEEP OPEN** — Doc06 improved (8/9 distinct rationales) but depth concerns remain |
| **T1C-015** | MEDIUM | Remediated pending rereview | **ACCEPT with residual** — terminology fixed; filename path debt remains |
| **T1C-016** | MEDIUM | Valid open retained | **KEEP OPEN** — principals thicker than V3 but still thin control surfaces |
| **T1C-017** | LOW | Remediated pending rereview | **ACCEPT** |
| **T1C-018** | LOW | Remediated pending rereview | **ACCEPT** (with T1C-005) |
| **T1C-019** | LOW | Valid open retained | **KEEP OPEN** — boundary preserved; appointment/performance not evidenced |
| **T1C-020** | LOW | Retained nonblocking open | **KEEP OPEN (nonblocking)** — local validation; Linux/CI reproduction not shown |

**Scoreboard:** 12 accepted remediations (incl. T1C-004 substance); 8 retained open (incl. 3 blocking: 003, 006, 010).

---

## V4 remediation of prior Cursor VR3 findings

| Prior finding | V4 treatment | Adjudication |
|---|---|---|
| VR3-001 Doc10 identity + overclaim | Templates rewritten; dispute retained for adjudication | **ACCEPT authoring**; **ACCEPT** purpose-specificity on review |
| VR3-002 status/readiness drift | Inventory/README/Doc readiness → content-revision-required | **ACCEPT** |
| VR3-003 shared-standard tokens / triplicate | All 8 tokens in Authority Boundaries; single External Standards note | **ACCEPT** |
| VR3-004 candidates authoritative | Relabeled `candidate source requiring authority confirmation` | **ACCEPT** |
| VR3-005 validator blind spots | Live normalized-body gate + mutated-package fixtures; `--package-root` works | **ACCEPT** |
| VR3-006 Doc03 fragments | Quarantine + reject typing | **ACCEPT honesty fix**; T1C-006 stays open |
| VR3-007 stubs/thinness/Doc09 | Partial (Doc09 PRs added; depth still open) | **PARTIAL — as packaged** |

---

## Remaining nonblocking package hygiene

1. **T1C MD ↔ CSV drift:** MD still shows T1C-004 as `NOT_REMEDIATED_RETAINED_OPEN`; CSV shows `VALID_OPEN_RETAINED_PENDING_INDEPENDENT_DOC10_ADJUDICATION`. MD date still `19:05:58` (V3-era). Synchronize after recording this adjudication.  
2. **Closure evidence register** for T1C-004 still cites V3 “conservative evidence table” language — update to V4 authored templates.  
3. **Doc03 narrative** typing claim outdated.  
4. **Doc10 filename** still contains `CERTIFICATION`.  
5. Cross-recon table still lists “Blocking minimum remediated F-01…F-02…” while F-02 was reopened for adjudication — reconcile after register update.

None of these reopen the packaging-ready determination if corrected in a bounded follow-up; they should not be ignored before any Founder directional “ready” claim.

---

## Bottom line

V4 **is sufficient** for the bounded packaging/rereview handoff the authors claimed:

- Doc10 identical-body defect: **remediated and accepted here**.  
- Doc03 fragment quarantine: **accepted as honesty remediation**; verification baseline **still open**.  
- Most V3 `REMEDIATED_*_PENDING_REREVIEW` mechanical findings: **accepted**.  
- Blocking opens that correctly remain: **T1C-003, T1C-006, T1C-010** (plus medium/low retained opens).

**Overall outside-review disposition:**  
`PACKAGING_READY_FOR_BOUNDED_REREVIEW` **accepted**;  
`CONTENT_REVISION_REQUIRED` **retained**;  
`MERGE_NOT_AUTHORIZED` / full authority boundary **unchanged**.
