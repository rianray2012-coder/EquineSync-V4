# EquineSync Feature-to-Governance Coverage Matrix V1.0 — Independent Engineering Audit

**Auditor role:** Senior Software Architect / Staff Engineer / Technical Program Manager / Governance Engineer  
**Scope:** Technical usefulness for implementing and maintaining a large SaaS codebase  
**Package audited:** `EQUINESYNC_MASTER_PRODUCT_FEATURE_TO_GOVERNANCE_COVERAGE_MATRIX_V1_0` (Parts 1–2)  
**Baseline commit claimed:** `1eb384d80daa700ba2e71ee42872cc9bba926332` (matches current workspace HEAD)  
**Audit date:** 2026-08-03  
**Method:** Package integrity verification, structural analysis of all 314 matrix rows / companion registers / validator, and cross-check against the live EquineSync repository (`frontend/`, `backend/`, `governance/`)

**Authority note:** This audit evaluates engineering utility only. It does not adopt, reject, or authorize governance artifacts.

---

## Verdict (executive)

The matrix is a **strong documentary inventory and governance-gap planning instrument**, but it is **not yet trustworthy as a canonical implementation-to-governance reference**. Evidence paths are keyword-correlated rather than behavior-verified; dependencies are almost entirely synthetic; implementation-guidance fields are domain-templated boilerplate; and several high-risk rows claim `IMPLEMENTED_UNVERIFIED` for capabilities that do not exist as discrete product behaviors in code.

**Would you adopt this matrix as the canonical implementation-to-governance reference?**  
**No** — not in its current form. Adopt it as a **draft governance coverage backlog and feature taxonomy seed**, after remediating Critical/High issues below.

| Score | Value |
| --- | ---: |
| Overall Engineering Score | **4.5 / 10** |
| Implementation Readiness | **3 / 10** |

---

## Package integrity

| Check | Result |
| --- | --- |
| SHA-256 Part 1 | Match (`0187ce8e…53299`) |
| SHA-256 Part 2 | Match (`c3dfbe70…32b98`) |
| Reassembly | Both ZIPs extract to same root; 34 package files |
| Self-reported validation | Documentary checks PASS; adversarial scenarios are schema/consistency only |
| Standalone validator run | **Fails** when package is not at `governance/portfolio/coverage/drafting/...` (`REPO = PACKAGE.parents[4]` IndexError) |

---

## Evaluation by criterion

### 1. Feature Coverage — Partial / misleading completeness

**What works:** 314 stable `ES-FEAT-*` IDs across 22 domains give a useful product surface map. Domains broadly align with the SaaS (identity, care, billing, documents, mobile, AI, marketplace).

**What fails:**
- Feature descriptions are 100% templated (`Atomic coverage row for <name> within <domain>`). No acceptance criteria, API contracts, UI flows, or data models.
- Taxonomy is flat: parents are synthetic `*-000` domain buckets that are **not** feature rows.
- Recent implemented program work is missing or only loosely covered as atomic features: Today’s Pulse, entitlements/seats, multi-barn active context, role intake/home, DocuSign JWT/webhook flows, capability gates/data fences, lock-screen field reliability.
- Incident domain invents atomic features (`fire`, `quarantine`, `medication error`, `regulatory reporting`, `safeguarding incident`) that the UI does not implement as types, while real UI types (`kick`, `fall`, `trailer`, `fence`, `facility`) are absent.
- Duplicate feature names across domains (`disputes`×3, `owner updates`×2, `escalation`×2, etc.) without disambiguation IDs in human-facing names.

### 2. Governance Mapping — Structurally present, often not technically actionable

**What works:** Explicit layer model (PIA / Code Guide / ADR / OS / runbook / AI / safeguarding / privacy / reporting), readiness scoring formula, PIA supplement candidate grouping, marketplace new-PIA analysis, conflict register for a few real authority overlaps.

**What fails:**
- Most PIA primary packages are recorded as `NO_PRIMARY_PIA_PACKAGE_LOCATED_IN_REALIGNMENT_REGISTER` while still used as `Governing PIA` on hundreds of rows.
- Code Guide refs are broad semicolon bundles (`ES-CG-00;…;ES-CG-13`) applied en masse; Wave 1 guides are source-frozen but non-substantive; most others are `PLANNED`.
- ADR / operating-standard / runbook columns are single placeholder strings on **all 314 rows**, not concrete artifact IDs.
- Multi-PIA ownership (`PIA-07;PIA-02;PIA-08`) without a designated **primary** owner makes RACI and code-review gates ambiguous.
- `FULLY_COVERED` (11 rows) is documentary-only and coexists with `IMPLEMENTED_UNVERIFIED` — engineers will misread this as “safe to ship.”

### 3. Engineering Utility — Low for day-to-day engineering

Engineers would **not** use the 147-column denormalized CSV as a working reference. Companion registers help governance PMs more than implementers. Missing for engineering use:
- Route/API/endpoint IDs
- Schema / collection / event names
- Permission capability keys
- Test IDs / CI job names
- PR / CODEOWNERS linkage
- Concrete acceptance tests
- Release train / epic mapping (`RELEASE_TARGET` = `UNASSIGNED` for 100%)

### 4–10. Summarized findings

| Area | Finding |
| --- | --- |
| Missing implementation guidance | Failure/recovery/audit/notification/required-impl/required-test/closure fields are identical across all 314 rows |
| Ambiguous governance refs | Placeholder ADR/OS/runbook; multi-PIA lists; Code Guides not activation-ready |
| Potential mapping errors | Keyword path matching; `admin_billing` on 87 non-financial rows; marketplace→`Signup.jsx`; incident subtypes→generic pages; media features→intake routes |
| Duplicate governance | Conflict register only 5 rows; PIA overlaps are widespread but under-enumerated; CONFLICT queue has 116 rows derived broadly |
| Future maintainability | 147 columns + generated mirrors; manual drift risk; field dictionary is boilerplate; no repo-path CI hook in current tree |
| Repository evolution | No machine-readable link from feature ID → routes/components; baseline commit pinned but no automated rebase/diff workflow documented for code drift |
| Versioning strategy | Artifact versioning exists; feature-row version fields present; no semver policy for breaking taxonomy changes, no changelog of semantic mapping quality |

---

## Support for intended engineering workflows

| Workflow | Supported? | Notes |
| --- | --- | --- |
| Code reviews | **Weak** | No enforceable feature↔diff checklist; evidence paths too noisy |
| Implementation planning | **Weak–Medium** | Domain inventory useful; effort mostly `M`/`PRELIMINARY`; no release targets |
| Requirements validation | **Weak** | No requirements text beyond names; origin IDs exist but descriptions are empty templates |
| Audit readiness (governance documentary) | **Medium–Strong** | Checksums, manifests, authority disclaimers, queues, layer model |
| Audit readiness (implementation conformity) | **Weak** | Explicitly no runtime verification; evidence is path presence |
| Regression analysis | **Weak** | No test↔feature binding that CI can execute |
| Change impact analysis | **Weak** | Dependency graph is synthetic hubs (platform blocks 313; messaging/identity/tasks/relationships block 292) |
| Governance evolution | **Medium–Strong** | Supplement/new-PIA candidates and founder questions are useful planning inputs |

---

## Issues (severity / impact / fix / effort)

### ISS-01 — False-positive implementation evidence via keyword path matching
- **Severity:** Critical  
- **Impact:** Features marked `IMPLEMENTED_UNVERIFIED` / `PARTIAL_IMPLEMENTATION` when code only shares tangential files (e.g., `PersonalDashboard.jsx` on 126 rows; `Signup.jsx` on all 14 marketplace rows; intake routes as “media” evidence). Creates false launch confidence and bad verification queues.  
- **Recommended Fix:** Require evidence to include at least one of: owning route handler + primary UI entry + permission key + test that names the feature ID. Demote rows without symbol/behavior proof to `NOT_FOUND` or `DOCUMENTED_ONLY`. Separate `EVIDENCE_NOTES` from `IMPLEMENTATION_EVIDENCE_PATHS`.  
- **Estimated Effort:** L (systematic re-verification pass + validator rules)

### ISS-02 — Incident subtype rows overclaim implementation
- **Severity:** Critical  
- **Impact:** `fire`, `quarantine`, `medication error`, `regulatory reporting`, etc. marked implemented/unverified at risk 16, while `Incidents.jsx` only supports `injury|loose_horse|kick|fall|trailer|fence|facility|other`. Distorts top blockers and safety prioritization.  
- **Recommended Fix:** Collapse to actual incident/emergency product capabilities; map UI enum values 1:1; mark aspirational subtypes `NOT_FOUND` / `POST_MVP`.  
- **Estimated Effort:** M

### ISS-03 — Dependency graph is synthetic and non-actionable
- **Severity:** Critical  
- **Impact:** 313/314 dependencies `STRONGLY_INFERRED`; only 1 `CONFIRMED`. Platform/messaging/identity hubs dominate impact analysis. Cannot drive sequencing or blast-radius reviews.  
- **Recommended Fix:** Model only hard edges (authz, data ownership, provider, shared schema). Cap fan-out; introduce dependency types (`RUNTIME`, `DATA`, `GOVERNANCE`, `UX`). Require human confirmation for hubs.  
- **Estimated Effort:** L

### ISS-04 — Evidence path field polluted with prose on every row
- **Severity:** High  
- **Impact:** All 314 rows include non-path strings (`exact collection-level ownership…`, `native app directories present`, …). Breaks tooling that treats the field as paths; validator does not reject this.  
- **Recommended Fix:** Split path list vs notes; validate path tokens exist in repo at baseline commit.  
- **Estimated Effort:** S

### ISS-05 — Implementation guidance fields are domain-templated boilerplate
- **Severity:** High  
- **Impact:** Failure/recovery/audit/notification/required work/closure identical for all rows → useless for implementation planning and code review.  
- **Recommended Fix:** Per-feature or per-capability-family contracts; allow `NOT_SPECIFIED` rather than fake uniformity.  
- **Estimated Effort:** XL (content), S (schema allowance)

### ISS-06 — Ambiguous / placeholder governance artifact references
- **Severity:** High  
- **Impact:** ADR/OS/runbook placeholders on 314 rows; multi-PIA lists without primary; Code Guides mostly non-active. Engineers cannot resolve “what document governs this change?”  
- **Recommended Fix:** Require resolvable artifact IDs or explicit `GAP`/`NONE`; add `PRIMARY_PIA`; link to repository paths that exist.  
- **Estimated Effort:** M

### ISS-07 — `FULLY_COVERED` / `GOVERNANCE_READY` conflated with product readiness
- **Severity:** High  
- **Impact:** 11 rows score governance-ready while remaining `IMPLEMENTED_UNVERIFIED` and runtime-unverified. Misleads PM/eng gate decisions.  
- **Recommended Fix:** Rename bands (`DOCUMENTARY_GOVERNANCE_COMPLETE`); add separate `SHIP_READINESS` that requires test+runtime evidence.  
- **Estimated Effort:** S

### ISS-08 — Priority inflation destroys sequencing signal
- **Severity:** High  
- **Impact:** Delivery priority P0=156, P1=145; founder decision YES on 299/314; founder decision queue = all rows; risk scores cluster at 8 and 12. Everything is urgent → nothing is.  
- **Recommended Fix:** Hard cap P0 (e.g., ≤15%); founder queue only for true decision families; recalibrate likelihood away from default `LIKELY`.  
- **Estimated Effort:** M

### ISS-09 — Missing mapping to current repository capabilities / BUILD_NEXT surface
- **Severity:** High  
- **Impact:** Entitlements, Today’s Pulse, role intake/home, active context, DocuSign provider path, data fences, etc. absent as first-class features despite substantial code/docs. Matrix drifts from the real product.  
- **Recommended Fix:** Reconcile against route inventory, page inventory, and BUILD_NEXT/RF proof modules; add missing rows or explicit out-of-scope.  
- **Estimated Effort:** L

### ISS-10 — Source register marks nearly all sources `CONTROLLING`
- **Severity:** High  
- **Impact:** 372/374 sources `CONTROLLING`, including 186 as-built tests marked “not executed.” Contaminates authority model used by audits.  
- **Recommended Fix:** Separate `EVIDENCE` vs `CONTROLLING_AUTHORITY`; only constitutional/PIA/founder artifacts can be controlling.  
- **Estimated Effort:** M

### ISS-11 — Validator checks consistency, not correctness
- **Severity:** High  
- **Impact:** Adversarial suite PASSes schema/math/disclaimer checks; does not detect false evidence, missing paths-as-notes, or semantic overclaim. Gives false assurance.  
- **Recommended Fix:** Add path existence, prose-in-path rejection, max evidence fan-out, primary-PIA required, feature-ID references in tests optional gate.  
- **Estimated Effort:** M

### ISS-12 — Validator path coupling / package not in-repo at expected location
- **Severity:** Medium  
- **Impact:** `PACKAGE.parents[4]` assumes fixed depth; extracted package cannot validate; package path advertised in README is not present on current branch. Maintainability and CI integration blocked.  
- **Recommended Fix:** Resolve repo root via git; vendor package under `governance/portfolio/coverage/`; add CI job.  
- **Estimated Effort:** S

### ISS-13 — 147-column denormalized matrix is unusable for engineers
- **Severity:** Medium  
- **Impact:** Cognitive load; Excel fragility; review avoidance. Normalized registers help but authoritative CSV remains the working set.  
- **Recommended Fix:** Publish eng-facing views: `feature_id, name, domain, primary_pia, routes[], permissions[], tests[], ship_state, gaps[]`. Keep wide matrix as archival.  
- **Estimated Effort:** M

### ISS-14 — Field dictionary is non-informative boilerplate
- **Severity:** Medium  
- **Impact:** Every field description repeats the same sentence; controlled values often `FREE_TEXT…` even for enums. Onboarding/maintenance cost rises.  
- **Recommended Fix:** Real definitions, types, cardinality, derivation rules, allowed empties.  
- **Estimated Effort:** M

### ISS-15 — Parent IDs are non-addressable domain buckets
- **Severity:** Medium  
- **Impact:** Breaks hierarchical planning, rollups, and dependency inheritance.  
- **Recommended Fix:** Either materialize parent rows or replace with `domain_id` foreign key.  
- **Estimated Effort:** S

### ISS-16 — Duplicate feature names without UX disambiguation
- **Severity:** Medium  
- **Impact:** Human error in reviews/queues (`disputes`, `owner updates`, `recovery`, …).  
- **Recommended Fix:** Unique display names including domain qualifier; keep IDs stable.  
- **Estimated Effort:** S

### ISS-17 — Persona tagging over-broad
- **Severity:** Medium  
- **Impact:** Barn Manager on 96% of rows; average ~7 personas/feature. Permission and UX impact analysis becomes noise.  
- **Recommended Fix:** Distinguish `primary_actor` vs `indirectly_affected`.  
- **Estimated Effort:** M

### ISS-18 — Conflict/duplicate register understates governance duplication
- **Severity:** Medium  
- **Impact:** Only 5 conflict rows while multi-PIA co-ownership is common; CONFLICT queue has 116 rows with unclear derivation fidelity.  
- **Recommended Fix:** Auto-emit conflict candidates whenever >1 PIA listed without primary + differing truth owners.  
- **Estimated Effort:** M

### ISS-19 — Release / MVP / effort fields not decision-grade
- **Severity:** Medium  
- **Impact:** All release targets `UNASSIGNED`; effort mostly `M` + `PRELIMINARY`; cannot drive roadmap.  
- **Recommended Fix:** Populate only after founder release-planning authorization; until then omit from eng dashboards.  
- **Estimated Effort:** M (process) / S (hide fields)

### ISS-20 — No machine-readable repository evolution / drift workflow
- **Severity:** Medium  
- **Impact:** As code changes, matrix silently decays; version report only tracks matrix self-fields, not code drift.  
- **Recommended Fix:** Feature-ID annotations in code or CODEOWNERS-like map; CI diff of routes/pages vs matrix evidence; changelog policy for taxonomy breaks.  
- **Estimated Effort:** L

### ISS-21 — Marketplace `PARTIAL_IMPLEMENTATION` overstates product reality
- **Severity:** Medium  
- **Impact:** Rankings/reviews/referrals/bookings cited via signup/admin/intake paths. Risks premature marketplace PIA/ops investment based on phantom surface.  
- **Recommended Fix:** Reclassify most marketplace rows `NOT_FOUND` or `DOCUMENTED_ONLY` until dedicated modules exist.  
- **Estimated Effort:** S

### ISS-22 — Queue volume (1340) exceeds human throughput
- **Severity:** Low–Medium  
- **Impact:** TPM cannot operate 314-row founder + verification queues meaningfully.  
- **Recommended Fix:** Queue by decision family / epic, not every atomic row.  
- **Estimated Effort:** S

### ISS-23 — Risk methodology lacks discrimination for safety vs finance vs shell
- **Severity:** Low–Medium  
- **Impact:** Domain-uniform scores (all financial ≈12, all incidents ≈16) hide within-domain priority.  
- **Recommended Fix:** Feature-specific likelihood based on exposure, data class, and residual control strength.  
- **Estimated Effort:** M

### ISS-24 — Package split + size of denormalized JSON (~4.5MB) hinder review
- **Severity:** Low  
- **Impact:** Process friction only; content issue is secondary.  
- **Recommended Fix:** Keep CSV authoritative; generate slim JSON views; document reassembly in CI.  
- **Estimated Effort:** S

---

## Top 20 improvements (ordered by value)

1. **Rebuild implementation evidence** with behavior/symbol proof; demote keyword hits.  
2. **Reconcile incident/emergency taxonomy** to actual UI/API enums.  
3. **Replace synthetic dependency graph** with typed, confirmed edges.  
4. **Split evidence paths from notes**; validate path existence at baseline.  
5. **Add eng-facing slim projection** (routes, permissions, tests, ship state).  
6. **Require primary PIA + resolvable artifact IDs** (or explicit GAP).  
7. **Rename documentary “fully covered”** vs ship readiness.  
8. **Deflate P0 / founder / risk defaults** to restore prioritization.  
9. **Inventory-reconcile against current code** (Pulse, entitlements, role intake, DocuSign, fences).  
10. **Fix source authority model** (`CONTROLLING` vs evidence).  
11. **Upgrade validator** to catch semantic overclaim, not just schema math.  
12. **Vendor package into repo + CI** with portable root resolution.  
13. **Write real per-feature acceptance / failure / permission contracts** for P0 safety/finance/identity.  
14. **Materialize or remove parent `*-000` IDs.**  
15. **Disambiguate duplicate feature names.**  
16. **Introduce primary vs secondary personas.**  
17. **Auto-generate conflict candidates** from multi-owner rows.  
18. **Hide unassigned release/effort from eng dashboards** until authorized.  
19. **Add feature-ID ↔ code drift detection.**  
20. **Collapse marketplace overclaims** to honest `NOT_FOUND`/`DOCUMENTED_ONLY`.

---

## Strengths

- Stable feature ID namespace and domain coverage breadth.  
- Clear non-adoption / documentary authority boundaries (reduces accidental “approved” claims).  
- Layered governance model with deterministic readiness math.  
- Useful companion registers (queues, PIA supplement mapping, ungoverned capabilities, marketplace alternatives).  
- Integrity machinery: manifests, checksums, percentage reconciliation, adversarial schema tests.  
- Honest about runtime verification not performed (when read carefully).  
- Conflict themes (financial truth vs relationship authority; projection vs truth; provider activation) are the right architectural concerns.

---

## Weaknesses

- Evidence quality insufficient for implementation truth.  
- Guidance fields are copy-paste governance liturgy, not engineering contracts.  
- Dependency and priority systems amplify noise.  
- Drift from the live codebase’s recent capabilities.  
- Too wide for engineers; too soft for auditors asserting conformity.  
- Placeholder governance references undermine the “mapping” claim.  
- Validator confidence theater relative to semantic correctness.

---

## Technical debt introduced

- A 314×147 denormalized artifact that will rot without automation.  
- False `IMPLEMENTED_*` labels that future teams may trust.  
- Synthetic dependencies that may be cargo-culted into architecture docs.  
- 1340-row queues that create process thrash and Founder bottleneck theater.  
- Dual sources of truth risk if matrix is treated as equal to PIAs/Code Guides/code.

---

## Technical debt prevented (if used correctly as documentary backlog only)

- Undocumented marketplace governance hole (called out as new PIA candidate).  
- Untracked PIA supplement sprawl (179 candidates grouped).  
- Silent “path exists ⇒ verified” claims are at least labeled unverified.  
- Some cross-domain authority collisions are named instead of rediscovered ad hoc.  
- Checklist of domains where operating standards / runbooks / ADRs are missing.

---

## Scores

### Overall Engineering Score: **4.5 / 10**
Strong as a governed inventory skeleton; weak as an implementation control plane due to evidence false positives, synthetic dependencies, and missing eng contracts.

### Implementation Readiness: **3 / 10**
Cannot safely drive implementation planning, code review gates, regression mapping, or change-impact analysis without a remediation pass. Suitable today as input to governance sequencing decisions only.

---

## Adoption decision

### **No** — do not adopt as the canonical implementation-to-governance reference yet.

**Justification:**
1. Canonical references must have trustworthy feature↔code bindings; current bindings are keyword heuristics with proven false positives (incidents, marketplace, billing-path bleed).  
2. Canonical references must answer “what do I implement/test for feature X?”; required work/testing/failure fields are identical boilerplate.  
3. Canonical impact analysis requires real dependencies; 313 inferred universal hubs do not.  
4. Canonical audit use for implementation conformity requires executable evidence; the package correctly disclaims runtime verification but still emits high-confidence-looking `IMPLEMENTED_UNVERIFIED` at CRITICAL risk, which will be misconsumed.  
5. The package **is** valuable as a **draft taxonomy + governance gap backlog** under its own documentary authority banner — retain that role after fixing Critical/High issues, then reconsider canonical adoption.

**Conditional path to Yes:** Complete ISS-01, ISS-02, ISS-03, ISS-04, ISS-06, ISS-07, ISS-09, ISS-11, and ship an eng-facing slim view + CI drift checks. Re-audit; expect scores in the 7–8 range if evidence quality holds.

---

## Appendix A — Quantitative signals used

| Signal | Value |
| --- | --- |
| Feature rows | 314 |
| Columns | 147 |
| `IMPLEMENTED_UNVERIFIED` | 232 (73.9%) |
| Runtime verified | 0 |
| Release target UNASSIGNED | 314 (100%) |
| Dependency confidence STRONGLY_INFERRED | 313/314 |
| Templated descriptions | 314/314 |
| Evidence fields containing prose notes | 314/314 |
| Unique evidence path sets | 221 (100 features share sets of size ≥3) |
| `admin_billing` cited outside Financial | 87 rows |
| Marketplace rows citing `Signup.jsx` | 14/14 |
| Founder decision required YES | 299 |
| Delivery P0 | 156 |
| PIA primary package “not located” | 8/10 PIAs in summary |
| Conflict register rows | 5 |
| Queue rows | 1340 |

## Appendix B — Representative mapping defects

| Feature | Claim | Repo reality |
| --- | --- | --- |
| `ES-FEAT-INCIDENT-006` fire | Implemented unverified via Incidents/Emergency pages | No `fire` type in Incidents or EmergencyWorkflows enums |
| `ES-FEAT-INCIDENT-009` quarantine | Implemented unverified | No quarantine capability located |
| `ES-FEAT-MARKETPLACE-006` search ranking | Partial via Signup/Enrollment/Expenses | No ranking module evidenced |
| `ES-FEAT-INCIDENT-001` rider injury | Backend includes `admin_billing.py` | Billing route is not injury workflow evidence |
| Media cluster (8 features) | Shared evidence = intake routes | Intake ≠ media asset pipeline |

---

*End of audit.*
