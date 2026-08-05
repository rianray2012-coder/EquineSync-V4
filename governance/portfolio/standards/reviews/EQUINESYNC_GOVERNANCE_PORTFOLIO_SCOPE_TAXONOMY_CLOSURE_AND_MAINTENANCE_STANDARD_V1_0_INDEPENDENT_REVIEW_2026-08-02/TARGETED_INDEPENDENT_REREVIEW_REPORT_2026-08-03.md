# Targeted Independent Re-Review Report

**Subject:** EquineSync Governance Portfolio Scope, Taxonomy, Closure, and Maintenance Standard V1.0 — Revised Candidate (`77d5894`)

**Review type:** Targeted independent re-review (verification of prior Critical/High remediation; regression and new-defect scan)

**Reviewer posture:** Independent documentary assessment only. No approval, adoption, activation, certification, merge, or governance-status authority.

**Review date:** 2026-08-03

**Package self-declared status:** `OUTSIDE_REVIEW_COMPLETE_REVISION_REQUIRED_NOT_READY_FOR_FOUNDER_APPROVAL`

**Package self-declared readiness:** `REVISION_COMPLETE_READY_FOR_TARGETED_OUTSIDE_REREVIEW`

**Independent package checks executed in this review:**
- `sha256sum -c CHECKSUMS.sha256` → all listed files OK
- `python3 tools/validate_governance_portfolio_package.py --package-dir .` → VALIDATION PASSED
- `python3 tools/generate_governance_portfolio_package.py --check` → exit 0 (no generator drift observed)

---

## Executive Summary

The revised package is a **material improvement** over the second draft. It adds truthful validation vocabulary, separates structural from unimplemented categories, introduces a non-waivable core, class-specific FCR schema conditionals, privacy controls, delegation/succession/role matrices, certification status instruments, generator/validator tooling, and correctly marks several repository-context checks as `PENDING`.

It does **not** yet fully resolve the prior Critical lifecycle and production-path defects, and it still overstates some semantic/legal checks as `PASS` despite limitations that require outside or legal confirmation. Founder exception power is better bounded on paper, but dual control remains soft (“where available”), identity binding remains unimplemented, and certification-as-lifecycle-state modeling persists alongside a separate certification-status register—creating duplicated, conflicting models.

**Readiness assessment: NEEDS ADDITIONAL REVISION** before Founder approval review.

**Confidence: High** for package-internal structural/truthfulness verification; residual uncertainty remains for live repository source bytes and branch-protection enforcement, which the package itself marks `NOT_EXECUTED` / `PENDING`.

---

## Previous Findings Verification

Prior Critical/High findings from the 2026-08-02 independent review are verified below against package evidence, not remediation claims.

### C-1 — Founder exception authority can nullify fail-closed substance

**Status: Partially Resolved**

**Evidence of progress:**
- `ES-GPS-CORE-001` and `NON_WAIVABLE_CORE_MATRIX.csv` define a non-waivable core.
- Temporary-only waiver/exception language appears across FCR classes; permanent waivers are prohibited in MD/FCR matrix.
- `EXCEPTION_BUDGET_AND_WAIVER_AGING_RULES.csv` adds aging/escalation.
- FCR-09/FCR-10 require second-review fields and non-waivable-core confirmation.

**Why not fully resolved:**
- The non-waivable core is largely **meta-documentary** (non-falsification, durable records, overclaim prohibition, exact-scope production wording). It does **not** hard-block waiver of substantive control classes such as independent custody verification, material defect disclosure as a non-waivable gate, or security/privacy verification baselines.
- Dual control remains conditional: “second review **where available**”; role matrix defaults Founder into steward roles and records Second Reviewer as “Unavailable unless named.”
- `ES-GPS-FAIL-001` still fails closed only absent Founder certification; Founder may still waive broad internal tests via FCR-03 (now time-bounded, but still single-actor capable when second reviewer is absent and disclosed via FCR-08).

### C-2 — Lifecycle conflates certifications/production with lifecycle states

**Status: Not Resolved** (register addition is insufficient)

**Evidence of incomplete remediation:**
- `FOUNDER_CERTIFIED_EXCEPTION` remains a lifecycle state (`LIFECYCLE_STATE_DEFINITION_MATRIX.csv`).
- Transitions still move artifacts into that state (`TR-017`, `TR-020`).
- `PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS` remains a lifecycle state.
- No “overlay” / concurrent-dimension model is stated in the MD lifecycle section.
- A parallel certification-status model now exists (`CERTIFICATION_REGISTER.csv`, FCR status set `ACTIVE/EXPIRED/REVOKED/...`), which **duplicates** lifecycle states `EXPIRED`, `REVOKED`, `NARROWED`, `SATISFIED_BY_EVIDENCE` rather than replacing the exclusive-state design.

This remains a functional modeling defect against `ES-GPS-CLASS-001`.

### C-3 — Production path is exception-centric; clean production underspecified

**Status: Not Resolved**

**Evidence:**
- Lifecycle production transitions remain only:
  - `TR-018 OPERATIONALLY_READY → PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS`
  - `TR-019 PILOT_AUTHORIZED → PRODUCTION_AUTHORIZED_WITH_EXPRESS_EXCEPTIONS`
- No transition or state for production authorization with empty/none exception inventory.
- Package search found no operative “without express exceptions” / empty-exception attestation path.
- `ES-GPS-CERT-PROD-001` still frames production through identified exceptions.

### H-1 — No segregation of duties, succession, or Founder-incapacity controls

**Status: Partially Resolved**

**Evidence of progress:** `ROLE_DEFINITION_AND_ASSIGNMENT_MATRIX.csv`, `DELEGATION_AND_SUCCESSION_CONTROL_MATRIX.csv`, `DELEGATION_REGISTER.csv`, `ES-GPS-DELEG-001`, challenge procedure.

**Residual:** Founder currently fills multiple roles; succession alternate is “None unless delegated”; SoD limitation is disclosed in `KNOWN_LIMITATIONS.md` rather than operationally closed. Adequate for documentary maturity disclosure; not adequate as implemented independence.

### H-2 — Schema lacks class-specific mandatory field enforcement

**Status: Partially Resolved**

**Evidence of progress:** JSON Schema `allOf`/`if`/`then` conditionals exist for FCR-01..FCR-10; class templates exist; validator confirms conditional presence and template field names.

**Residual defect:** class payload property types are unions including `null`. A record can include all required keys with `null` values and still be schema-structurally acceptable. Package validator does not reject null/empty payload values. `additionalProperties: true` remains on class payloads.

### H-3 — Founder identity binding weak

**Status: Partially Resolved (documentary) / Not Resolved (operational binding)**

**Evidence of progress:** Tamper-evidence matrix and approval fields expanded; limitations disclosed.

**Residual:** `TAMPER_EVIDENCE_CONTROL_MATRIX.csv` records signed commits / signed tags / independent package-hash anchoring as `FALSE` / not implemented. No mandatory cryptographic or IdP-bound Founder attestation is enforced by schema or validator.

### H-4 — Self-validation report creates false assurance

**Status: Partially Resolved**

**Evidence of strong correction:**
- Validation vocabulary includes PASS/FAIL/PENDING/NOT_EXECUTED/BLOCKED/NOT_APPLICABLE.
- Prior unexecuted git/path checks are now `PENDING` (`VAL-018`, `VAL-019`, `VAL-020`) with null execution metadata.
- Overall result is `PENDING_FINAL_REPOSITORY_CONTEXT`, not unqualified PASS.
- Category matrix marks repository/implementation/production verification `NOT_EXECUTED`.
- Prior-report supersession acknowledgement is explicit.

**Residual material issue:**
- `VAL-022` (human semantic review), `VAL-023` (privacy review), `VAL-024` (exception-authority review), and `VAL-025` (external-law review) are marked **PASS** while executed by “Codex package validator,” with limitations stating they are not independent outside validation / make no legal compliance conclusion / require targeted outside or legal confirmation.
- `VCAT-006` semantic human review is also PASS under the same limitation.
- Under `ES-GPS-VALID-001`, reporting an unsupported/incomplete independent review as PASS remains a truthfulness defect, even with limitation text.

### H-5 — Incomplete lifecycle transition graph

**Status: Fully Resolved** (graph completeness) with residual modeling debt from C-2

**Evidence:** Added `LOCKED→ACCESSION_PENDING` (`TR-025`), reopen/suspend/retire/reject/review-pending paths, and no orphan from/to states in independent graph analysis. Inbound/outbound coverage for defined states is complete.

### H-6 — External-obligation control declarative only

**Status: Partially Resolved**

**Evidence of progress:** `REGULATORY_AND_EXTERNAL_OBLIGATION_APPLICABILITY_REGISTER.csv` with `REQUIRES_LEGAL_CONFIRMATION`; FCR-09 requires `external_obligation_check`; known limitations refuse legal compliance conclusions.

**Residual:** `VAL-025` still PASS despite “No legal compliance conclusion made.” Operational legal attestation workflow remains documentary only.

### H-7 — Pilot privacy/safeguarding incomplete

**Status: Fully Resolved** at documentary-control level

**Evidence:** `ES-GPS-PRIV-001`, `PILOT_PRIVACY_AND_EVIDENCE_CONTROL_MATRIX.csv` (lawful basis/consent, notice, minimization, retention, DPIA, minors, incident suspension, etc.), and FCR-06 required payload fields + template. Package correctly does not claim pilot authorization or production privacy verification.

---

## Newly Identified Findings

### High

**N-H1. Semantic/legal validation checks are still marked PASS despite non-independence and incomplete legal confirmation.**
- Affected: `VAL-022`–`VAL-025`, `VCAT-006`.
- Required correction: mark as `PENDING` or `NOT_EXECUTED` until independent outside/legal confirmation exists; keep structural machine checks as PASS only where independently re-executable.

**N-H2. Dual lifecycle/certification-status modeling creates contradictory concurrent truths.**
- Certifications have register statuses (`ACTIVE/EXPIRED/...`) while lifecycle also contains `FOUNDER_CERTIFIED_EXCEPTION`, `EXPIRED`, `REVOKED`, `NARROWED`, `SATISFIED_BY_EVIDENCE`.
- Implementers cannot deterministically know which dimension controls claim validity.
- Required correction: remove certification outcomes from artifact lifecycle; keep them as overlays on `CERTIFICATION_REGISTER`.

### Medium

**N-M1. Schema required fields are null-satisfiable.**
- Class payload required keys accept `null`.
- Validator does not enforce non-null/non-empty payload values.

**N-M2. Non-waivable core omits substantive assurance baselines.**
- Custody independence, material-defect disclosure, and security/privacy verification minima remain waivable/substitutable through FCR paths (subject to temporary limits).

**N-M3. Governance complexity vs current staffing.**
- ~60+ package files, many registers, dual models, and Founder multi-role concentration (disclosed) create maintainability risk even with generator/validator support.

**N-M4. Second-review safeguard is soft-gated.**
- “Where available” plus FCR-08 disclosure path can become the standing operating mode rather than an exception.

**N-M5. Challenge procedure lacks disposition SLA / escalation clock.**
- Credible reports reopen claims, but no mandatory timebound investigation/disposition requirement is defined.

### Low

**N-L1. Lifecycle `terminal` flags are uniformly false**, including `REJECTED`/`RETIRED`/`REVOKED`, reducing machine usefulness.

**N-L2. ORF disposition matrix uses generic boilerplate remediation text** (“Implemented or tracked in changed artifacts”) rather than finding-specific evidence pointers in every row (some evidence fields exist, but remediation narrative is thin).

### Editorial

**N-E1.** MD lifecycle section is thin relative to the matrix complexity; readers must jump to CSV for operative rules.

**N-E2.** Dual status labels (`NOT_READY_FOR_FOUNDER_APPROVAL` vs `READY_FOR_TARGETED_OUTSIDE_REREVIEW`) are honest but easy to misquote; retain both and prohibit collapsing them in communications.

---

## Regression Findings

1. **Model duplication regression:** Adding certification status instruments without removing certification/production-as-lifecycle-states increased complexity and reintroduced dimension collision risk (related to unresolved C-2).
2. **Validation-label regression risk:** Replacing prior false PASS with new PASS-on-manual-Codex-review for VAL-022–025 improves disclosure but preserves the same class of overclaim under a different description.
3. **No evidence that remediation weakened non-falsification core text**; that principle remains intact.
4. **Generator/validator addition is net positive** and did not, in independent execution, invent unqualified Founder-approval readiness.

---

## Remaining Risks

| Risk domain | Residual risk |
|---|---|
| Governance authority | Single-actor waiver/override still operable when second reviewer absent |
| Lifecycle implementability | Exclusive-state certification/production modeling will break concurrent truth recording |
| Validation truthfulness | Semantic/legal PASS labels may be cited out of context despite limitations |
| Legal/regulatory | Applicability register exists; no confirmed legal determination |
| Privacy | Documentary controls strong; no operational privacy verification executed |
| Identity/integrity | Unsigned commits/tags; hash manifest only |
| Maintainability | High artifact count vs Founder-concentrated staffing |
| Production assurance | Exception-normalized production path remains the only modeled lifecycle route |

---

## Internal Consistency Assessment

| Area | Assessment |
|---|---|
| Checksums / manifest / generator drift | Consistent (independently verified) |
| Rule catalog presence for required new rules | Consistent (`VALID/CORE/DELEG/CHAL/PRIV/AIAUTH/PROP`) |
| FCR templates vs class required fields | Consistent at field-name level |
| Authority non-implication language | Generally consistent |
| Validation category separation (structural vs implementation/production) | Improved and largely consistent |
| Lifecycle graph completeness | Structurally complete |
| Lifecycle vs CLASS-001 dimension separation | **Inconsistent** (unresolved C-2; worsened by dual status models) |
| Production authority event vs lifecycle transitions | **Incomplete / biased to exceptions** (unresolved C-3) |
| VAL-022–025 PASS vs VALID-001 / limitations | **Tension / residual overclaim** |
| Package readiness claims vs overall validation result | Consistent: not Founder-approval-ready; pending repository context |

---

## Readiness Assessment

### **NEEDS ADDITIONAL REVISION**

**Basis:**
1. Prior Critical findings **C-2** and **C-3** are **Not Resolved**.
2. Prior Critical **C-1** and High **H-2/H-3/H-4/H-6** remain only **Partially Resolved**, with at least one new High truthfulness defect (`VAL-022`–`VAL-025` PASS).
3. Package itself correctly refuses Founder-approval readiness; this re-review agrees that Founder approval review should not begin until the unresolved Critical modeling and validation-truth issues are corrected.

Not rated `NOT READY` because remediation quality is real, tooling works, and several High privacy/transition/validation-integrity defects were substantially improved.

Not rated `READY WITH MINOR CHANGES` because remaining defects are structural (lifecycle dimension model; production path; validation PASS misuse), not editorial.

---

## Confidence Assessment

### **High**

Confidence is high that:
- package integrity checks pass;
- prior C-2/C-3 remain unresolved on package evidence;
- validation PENDING corrections for git/path checks are genuine;
- VAL-022–025 PASS labels are not independently supported as outside/legal confirmation.

Confidence is bounded by package-declared limits: repository evidence review, implementation verification, production verification, signed identity controls, and legal confirmation were not executed and are not assumed.

---

## Authority Statement

This re-review is independent documentary assessment only. It does not approve the standard; authorize adoption, implementation, activation, pilot, or production; authorize certification issuance; authorize repository merge; or alter governance authority.
