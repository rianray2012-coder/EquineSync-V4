# PHASED_EXECUTION_PLAN.md
# EquineSync Refactor Execution Plan

> Production priority order (from `FEATURE_ROADMAP.md`): **Security & Stability → Mobile Workflows → Care Operations → Owner Trust → Billing Clarity → Reporting → AI Assistance → Ecosystem Expansion.**

## Phase 1: Documentation & Governance
**Status: ✅ Complete** (this pass)
Goals:
- Complete the `/docs` folder (in-repo source of truth)
- Add engineering rules
- Add architecture docs
- Add product vision
- Add permission matrix
- Add trust framework
- Reconcile stale/conflicting docs (DESIGN_TOKENS → Brand Guide)
- Create a code-grounded `KNOWN_TECH_DEBT.md`
- Save brand/logo assets

## Phase 2: Security Stabilization
**Status: ✅ Complete (2026-05-30)**
- **2A — ✅:** Removed unsafe JWT fallback; centralized config (`backend/config.py`) + fail-fast startup validation; dev-safe ephemeral secret; `tests/test_config.py`.
- **2B — ✅:** Rate limiting on auth endpoints (`backend/rate_limit.py`, `limits`) + CORS tightening (prod rejects `*`); `tests/test_rate_limit.py`.
- **2C — ✅:** Password reset + email verification (hashed single-use expiring tokens, `backend/auth_tokens.py`) + Resend templates; `email_verified` with safe backfill + off-by-default `ENFORCE_EMAIL_VERIFICATION`; `GET /api/health`; `tests/test_auth_tokens.py`, `tests/test_phase2c_auth.py`.
- **2D — ✅:** Account-level brute-force lockout (`backend/login_attempts.py`, 423 on lock, clear on success); branded `/reset-password` + `/verify-email` pages + Login "Forgot password?" flow; `tests/test_login_lockout.py`.

> Full backend suite: 235 passed, 1 skipped.

## Phase 3: Backend Modularization
**Status: In Progress (3A complete)** — see `PHASE3_MODULARIZATION_MAP.md`.
- **3A — ✅ Complete (2026-05-30):** Moved `config.py`, `rate_limit.py`, `auth_tokens.py`, `login_attempts.py` → `backend/core/` (via `git mv`); updated all imports; no behavior change; `/api/health` gained a `version` field.
- **3B — Planned:** Extract system/admin/analytics routes.
- **3C–3F — Planned:** Horse → Care/Task → Owner/Report → Billing route extraction.
- **3G — Planned:** server.py reduced to app assembly; JWT/auth helpers → `core/security.py`.

Goals:
- Break `server.py` into modular route files
- Move business logic into services
- Move schemas into schema files
- Create centralized config and security utilities

## Phase 4: Multi-Tenancy & Permissions
Goals:
- Enforce `barn_id` on all operational entities
- Add tenant isolation tests
- Add centralized permission service
- Align code with `ROLE_PERMISSION_MATRIX.md`

## Phase 5: Audit Logging
Goals:
- Create `AuditLog` model
- Track critical changes
- Add audit log service
- Add tests

## Phase 6: Care Workflow Strengthening
Goals:
- Improve feeding, turnout, medication, rehab, stall rest, grooming, training workflows
- Align with `WORKFLOW_MAPS.md`

## Phase 7: Owner Trust Layer
Goals:
- Improve owner dashboard
- Add weekly recap framework
- Add owner-facing update controls
- Add approval flow for sensitive updates

## Phase 8: Mobile Optimization
Goals:
- Optimize barn workflows for phone use
- Improve task completion UX
- Improve horse profile mobile view
- Improve quick notes and photo upload

## Phase 9: Billing Improvements
Goals:
- Improve invoice structure
- Add line-item clarity
- Support recurring charges
- Improve owner billing visibility

## Phase 10: Production Readiness
Goals:
- Add release checklist enforcement (`RELEASE_CHECKLIST.md`)
- Improve logging
- Add monitoring
- Prepare deployment checklist

---

## Build Packet Baseline (June 2026)

The updated build packet is now stored under
[`docs/equine_sync_build_packet/`](./equine_sync_build_packet/). These markdown
files are the diffable build source for remaining product, UX, engineering,
QA, compliance, payment, and launch planning work:

- `01_Product_Requirements_Document.md`
- `02_Roles_and_Permissions_Matrix.md`
- `03_User_Flows_and_Acceptance_Criteria.md`
- `04_Data_Model_and_Technical_Guide.md`
- `05_Roadmap_and_Feature_Backlog.md`
- `06_QA_and_UAT_Test_Plan.md`
- `07_Compliance_Payments_and_Legal_Docs_Notes.md`
- `08_Launch_Checklist.md`
- `09_Decision_Log_and_Open_Questions.md`

Execution rule: when a new build phase overlaps the build packet, first
translate the packet item into a gated phase prompt with scope, guardrails,
tests, and deferrals. Do not treat the packet as blanket approval to expand
feature surface area inside an unrelated phase.

Current practical sequence after Admin Portal, HorseOps 1A-1J, and 15R prep:

1. Finish 15R catalog/payment-provider prep through the approved Stripe-live
   reconciliation path.
2. Complete mobile readiness and evidence closure for core barn workflows.
3. Use the build packet to gate remaining launch-critical foundations:
   multi-barn/multi-role account model, invite/onboarding polish, minor/student
   communication safeguards, document/signature decision, and launch QA.
4. Return to Phase 16 only after the payment/legacy reconciliation plan is
   approved.

The current proposed next-phase sequence is tracked in
[`NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md`](./NEXT_BUILD_PLAN_FROM_UPDATED_ROADMAP.md).

Build-Next-1 status: Codex-approved and locked. It adds a read-only live Stripe
catalog readiness report plus future Apple product-id placeholders, with no
checkout, webhook, Apple receipt, subscription-item, hard enforcement, Phase 9,
Admin Portal, landing-page, or Phase 16 behavior changes.

Build-Next-2A status: Codex-approved and locked. It adds a mobile evidence
inventory matrix and focused source/evidence tests. It reuses locked HorseOps
390x844 mobile screenshots and marks billing, signup, dashboard, and Mobile
Readiness as source-pinned paths that require the follow-up Build-Next-2B live
390x844 screenshot gate before launch sign-off.

Build-Next-2B status: Codex-approved and locked. It closes the live screenshot
gate for `/billing/subscription`, Signup Step 3, `/dashboard`, and
`/mobile-readiness` with four PNG screenshots at `390x844`.

Build-Next-3 status: Codex-approved and locked. It is a read-only
Multi-Barn / Multi-Role Account Model Gap Report with no schema, invite,
transfer, permission, billing, HorseOps privacy, Admin Portal, landing-page,
native, offline, push, or Phase 16 behavior changes.

Founder decisions applied: future collection name `account_memberships`; users
may hold multiple roles; individual users may be active without an active
facility; billing entitlements remain account/facility scoped except the free
individual-owner one-horse account.

Founder decisions subsequently locked for Build-Next-3A: owner access remains
horse-specific for launch; preserve `users.barn_id` / `users.role` as
compatibility mirrors; use generated standalone owner account ids; apply
facility search / lead capture to all non-platform onboarding paths except
invited users.

Build-Next-3A status: Codex-approved and locked. It adds the
`account_memberships` foundation, named indexes, and an idempotent
compatibility mirror backfill from `users.barn_id` / `users.role`. It does not
change auth, route guards, invites, onboarding, owner projection, billing,
Admin Portal capabilities, HorseOps privacy, landing pages, native/offline/push
behavior, or Phase 16 cleanup.

BN3A founder decisions applied: owner access stays horse-specific for launch;
`users.barn_id` and `users.role` are preserved as compatibility mirrors;
standalone owner account ids are generated rather than raw `user_id`; facility
search / lead capture applies to all non-platform onboarding paths except
invited users, while individual owners may continue without an active facility.

Build-Next-3B status: Codex-approved and locked. It adds a read-only
`GET /api/account/context` contract and helper layer over `account_memberships`
so future phases can plan active-context selection without changing current
auth, route guards, invites, onboarding, owner projection, billing, Admin
Portal capabilities, HorseOps privacy, landing pages, native/offline/push
behavior, or Phase 16 cleanup.

BN3B selection behavior: active and pending-review memberships are selectable;
requested account ids select matching memberships; rejected/suspended-only
memberships remain visible in `available_contexts` but are not selected as
`active_context`; current `users.barn_id` / `users.role` mirrors remain the
fallback when membership rows do not exist.

Build-Next-3C status: Codex-reviewed and locked. It migrates only the
approved pilot product read routes (`/dashboard/summary`, `/dashboard/barn-board`,
`/horses`, `/horses/{horse_id}`) toward membership-aware active context,
preserves `users.barn_id` compatibility fallback through launch, clears the
disabled legacy barn / selected active facility edge case, and keeps
invite, onboarding, role-switcher, billing, HorseOps privacy, Admin Portal,
landing, native/offline/push, and Phase 16 work out of scope.

Build-Next-3D status: Codex-reviewed and locked. It extends the same
membership-aware read pattern to task-engine reads (`/task-templates`, `/tasks`,
`/tasks/today`, `/horses/{horse_id}/timeline`, `/staff/{user_id}/activity`,
`/tasks/analytics/summary`) while keeping task writes legacy-scoped and
active-facility gated.

Build-Next-4 status: Codex-reviewed and locked. It allows valid magic
invites to attach existing users to a facility through `account_memberships`
without creating duplicate users or overwriting current `users.barn_id` /
`users.role` mirrors. Public duplicate signup remains blocked. Existing-user
acceptance now verifies the submitted password before membership/session
issuance.

Build-Next-5 status: BN5-A rule matrix/schema prep, BN5-B guardian/student
invite foundation, and BN5-C server-side minor communication guard are
Codex-reviewed and locked. BN5-D QA evidence and launch checklist is also
Codex-reviewed and locked.

Build-Next-6 status: BN6A is Codex-reviewed and locked. It prepares a read-only
DocuSign-style connector readiness contract in
`BUILD_NEXT_6A_SIGNATURE_CONNECTOR_PREP_README.md`, gated by `integration:read`.
BN6B document workflow provider contract is locked in
`BUILD_NEXT_6B_DOCUMENT_WORKFLOW_PROVIDER_README.md`. BN6C local
template/request foundation is Codex-reviewed and locked in
`BUILD_NEXT_6C_DOCUMENT_REQUEST_FOUNDATION_README.md`. Live document signing,
provider API calls, envelope creation, provider webhooks, signed-document
retrieval, and participation gates remain deferred to a later founder/legal
approved implementation phase.

Build-Next-6D status: Codex-reviewed and locked. It adds a backend-only DocuSign
sandbox JWT token smoke script and private-key-path readiness support. It does
not create envelopes, signing URLs, provider webhooks, signed-document storage,
legal text storage, or participation gates.

Build-Next-6E status: Codex-reviewed and locked. It adds sandbox-only DocuSign
draft envelope creation behind `DOCUSIGN_SANDBOX_ENVELOPES_ENABLED=true`.
It is manager-only, demo-auth-server-only, demo-base-url-only, and stores only
safe local request metadata. It does not send envelopes, create signing URLs,
register provider webhooks, retrieve/store signed documents, add signer UX, or
create participation gates.

Round-1 fixes: demo REST base URL validation is now exact/parsed instead of
prefix-based, and the top-level sandbox readiness flag now reflects the full
sandbox readiness result rather than only the env flag.

---

## Phase 15: Subscription Billing v2 (True Stripe Subscriptions)

**Pricing addendum**: Future billing, admin portal, HorseOps usage counters,
owner portal access, and mobile limit messaging must follow
`docs/PRICING_PLAN_ADDENDUM.md`.

**Pre-launch foundation**: Before launch hardening, implement
`docs/PRE_LAUNCH_PRICING_FOUNDATION.md` / `PHASE_HORSEOPS_1J_README.md` so
active/inactive horses, usage counters, free invited owner portal access, and
role-based seat tracking are canonical before enforcement or overage work.

**Locks**: 1c · 2a · 3a · 4a · 5c · 6b (consumer-marketplace MERGE; `facility_id = barn_id`; one user → one facility → one subscription; Enterprise = Contact Sales; soft-warn only; 14-day trial).

### Hard rule — NO hard-blocking anywhere in Phase 15
Throughout Phase 15.A → 15.G, feature enforcement is **soft-warn only**.
No 402 responses. No create-flow blocking on horse/user/storage counts.
Usage endpoints surface counts and entitlements; UI surfaces banners and
upgrade prompts. **Hard enforcement is its own separately approved phase.**

### Sub-phase sequence (locked)
- **15.A** — Subscription foundation, backend-only. ✅ Shipped. Awaiting Codex review.
- **15.B** — Full webhook lifecycle: idempotency table, `subscription_invoices`,
  `payments`, lifecycle sync.
- **15.C** — Facility Owner Billing Portal + pricing-band swap + wizard Step 3 +
  monthly/annual toggle + resume flow + usage/limits display in billing UI.
- **15.D** — Trial email scheduler (env-gated, idempotent, fail-open).
- **15.E** — Platform-admin capability proposal + Admin Billing Dashboard
  (`barn:manage` alone is NOT enough for cross-facility platform billing
  visibility — a separate capability must be proposed and approved first).
- **15.F** — Soft-warn usage indicators in create flows and other operational
  UI surfaces. Still NO hard-blocking.
- **15.G** — Migration cleanup after one quiet release cycle. **Do not** remove
  `/membership/checkout` until telemetry/tests prove no usage.

### Protected during Phase 15
- Phase 9 `invoices` collection and recurring-charges flows are untouched.
  Stripe subscription invoices land in a NEW collection (`subscription_invoices`)
  in 15.B.
- `/api/membership/checkout` (one-time Checkout) stays operational with a
  deprecation comment until 15.G removes it.

### Deferred refactor — Phase 15R Billing Entitlements Refactor
Phase 15R is recorded in
[`PHASE_15R_BILLING_ENTITLEMENTS_REFACTOR.md`](./PHASE_15R_BILLING_ENTITLEMENTS_REFACTOR.md)
and is now proceeding as gated prep/refactor phases while Stripe and Apple
provider work are completed.

The intent is to make Equine Sync's backend entitlements the source of truth
for plan limits while Stripe and Apple are payment providers:
- Stripe is for web-based subscription purchases.
- Apple App Store billing is for iOS-originated purchases.
- Web purchasers still receive app access.
- Apple purchasers receive the same backend entitlements without Stripe IDs.
- Invited Horse Owner Portal access stays free and permission-based under a
  subscribed barn/trainer/facility; do **not** create a paid Stripe Product for
  this access path.

Do not alter checkout/webhook behavior, Apple billing behavior, hard
enforcement, or live pricing displays in 15R without a separately approved
gated plan.

## Build-Next-6F: DocuSign Connect Webhook Status Sync

Status: Codex-reviewed and locked.

BN6F adds a live-capable, disabled-by-default DocuSign Connect webhook receiver
for status-only local document request synchronization.

Strict boundaries:
- Requires `DOCUSIGN_WEBHOOKS_ENABLED=true` and `DOCUSIGN_WEBHOOK_SECRET`.
- Verifies DocuSign Connect HMAC on the raw body.
- Allows optional configuration-id pinning with
  `DOCUSIGN_CONNECT_CONFIGURATION_ID=22209160`.
- Requires payload account id to match `DOCUSIGN_ACCOUNT_ID`.
- Updates only local request status fields for an existing
  DocuSign provider-signature request with an existing `provider_envelope_id`.
- Stores no raw provider payloads, signer identities, envelope documents,
  PDF bytes, signing URLs, signed documents, legal text, or full audit diffs.
- Adds no billing, Stripe, Apple, HorseOps, Admin Portal, landing, native,
  offline, push, service-worker, or Phase 16 behavior.

## Build-Next-7: Launch QA / UAT Gate

Status: Codex-reviewed and locked.

BN7 is an evidence-only launch gate. It maps the build-packet QA and launch
checklist to the current locked product state, reuses existing screenshot/report
evidence, and classifies remaining work as blocker, warning, or deferred.

Gate result:
- Controlled founder/staging UAT is conditionally ready.
- First-client pilot is not yet ready until human UAT, live payment lifecycle
  verification, DocuSign webhook deployment/verification, and production ops
  sign-off are complete.
- Broad public launch remains no-go until pilot blockers and the final go-live
  runbook close.

Package:
- `outputs/build_next_7_launch_qa_uat_gate.zip`

## Build-Next-7A: Staging UAT Evidence Capture

Status: Codex-reviewed and locked.

BN7A creates the staging UAT evidence packet needed to clear BN7's residual
launch note. It includes a role/provider/ops checklist and sanitized evidence
log template, but does not claim human UAT is complete.

Gate result:
- Evidence packet is Codex-reviewed and locked.
- Staging UAT execution remains pending.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_7a_staging_uat_evidence.zip`

## Build-Next-8: Production Go-Live Runbook

Status: Codex-reviewed and locked.

BN8 creates the production launch runbook, boolean-only environment checklist,
provider verification checklist, rollback plan, support/monitoring ownership,
and founder decision sheet.

Gate result:
- Runbook package is Codex-reviewed and locked.
- Production launch is not approved by this phase.
- First-client pilot still requires BN7A UAT evidence closure and founder
  sign-off.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_8_production_go_live_runbook.zip`

## Build-Next-9: Staging UAT Execution Evidence

Status: Codex-approved and locked.

BN9 converts the locked BN7A checklist into an explicit evidence packet with
one stable evidence reference per required UAT row. It records that human role
walkthroughs, live provider lifecycle checks, and production operations sign-off
remain pending until founder/operator execution.

Gate result:
- Staging UAT evidence packet is Codex-approved and locked.
- Local dry-run screenshots were captured with disposable BN9 accounts.
- Human/staging UAT execution remains pending.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_9_staging_uat_execution.zip`

## Build-Next-10: Official Staging UAT Closure Plan

Status: Codex-approved and locked.

BN10 locks the official evidence rules for closing the BN7A/BN9 UAT rows. It
requires production-like staging for launch-clearing evidence, keeps BN9 local
screenshots reference-only, reserves `founder-accepted` for Rian, and allows
only controlled live-safe Stripe and DocuSign checks. Apple remains deferred.

Gate result:
- Official UAT closure rules are encoded as testable artifacts.
- No UAT row is marked `pass` or `founder-accepted` by this phase.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_10_staging_uat_closure.zip`

## Build-Next-11: Production-Like Staging Environment Proof

Status: Codex-approved and locked.

BN11 creates the official staging-environment proof packet required by BN10.
It records local health only as reference evidence and keeps official UAT
blocked until the production-like staging frontend URL/domain, API base URL,
build/version, environment label, database label, deploy marker, feature-flag
summary, role-account readiness, and provider readiness are supplied.

Gate result:
- Official staging identity remains blocked.
- Local health is reference-only and cannot close UAT rows.
- Role-account readiness remains pending.
- Provider readiness remains pending.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_11_staging_environment_proof.zip`

## Build-Next-12 Prep: Staging Inputs Collection

Status: ready for Codex review.

BN12 execution is deferred. BN12-Prep gives the founder a safe walkthrough for
collecting the official staging frontend URL/domain, API base URL, build
identifier, environment label, database label, deploy marker, feature flags,
role-account readiness, and provider readiness without recording secrets.

Gate result:
- BN12 remains deferred.
- Localhost is not accepted as official UAT evidence.
- No UAT row status changes occur.
- No provider lifecycle actions occur.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

Package:
- `outputs/build_next_12_prep_staging_inputs.zip`
