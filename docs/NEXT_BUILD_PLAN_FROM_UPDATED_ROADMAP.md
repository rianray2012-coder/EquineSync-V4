# EquineSync Next Build Plan From Updated Roadmap

Status: proposed gated plan after 15R-H lock.

## Purpose

This plan turns the updated build packet and current roadmap into a practical
sequence of gated implementation phases. It is intentionally split into small
reviewable phases so billing, mobile readiness, owner privacy, and launch
foundation work do not blur together.

The source packet lives in `docs/equine_sync_build_packet/`.

## Current Baseline

Locked foundations already in place:

- Admin Portal Admin-1 through Admin-8 plus Admin-4b.
- HorseOps 1A through 1K.
- Phase 15 Stripe Subscription Billing.
- Phase 15R-A through 15R-H.
- Updated build packet added to repo docs.

Hard rules that still apply:

- No Phase 15 hard-blocking unless a separate enforcement phase is approved.
- No Phase 16 legacy cleanup without a dedicated reconciliation and
  hard-delete plan.
- Invited Horse Owner Portal remains free/manual, not a paid Stripe product.
- Web Stripe and future Apple billing are payment providers; backend
  entitlements remain the app source of truth.
- Owner-facing surfaces must stay backend-authoritative and owner-safe.

## Recommended Next Sequence

### Build-Next-1 — Billing Launch Verification and Apple Contract Prep

Status: Codex-approved and locked.

Goal: finish low-rework billing readiness now that the live Stripe catalog is
reconciled.

Scope:

- Verify live Stripe catalog rows through local startup and admin integration
  surfaces.
- Confirm public plan responses stay Stripe-ID-scrubbed.
- Draft Apple product-id mapping placeholders and response-shape contract.
- Add a read-only Apple billing gap report if useful.

Deferred:

- No Apple receipt validation.
- No App Store server notifications.
- No Stripe subscription-item mutations.
- No hard usage blocking.
- No Phase 16 deletion work.

Exit criteria:

- Stripe live catalog is visible only where operationally appropriate.
- Public/app-safe responses omit operational Stripe IDs.
- Apple product-id work has a clear future map without blocking web launch.

Delivered:

- `backend/core/billing_launch_readiness.py`
- `backend/scripts/build_next_1_billing_launch_readiness.py`
- `backend/tests/test_build_next_1_billing_launch_readiness.py`
- `outputs/build_next_1_billing_launch_readiness_report.md`

Constants-only report result: 11 catalog plans, 12 add-ons, 0 blockers,
0 warnings. Apple product-id placeholders are documented for the eight
self-service plans.

Codex review closeout: stale Stripe Product/Price IDs in supplied Mongo-shaped
catalog rows now become blocker-level readiness issues, and the public
`/billing/plans-public` Stripe-ID scrubber is pinned by a Build-Next source
guard. Build-Next-1 is locked with 13/13 focused tests and 96/96 full available
15R + Build-Next tests green.

### Build-Next-2A — Mobile Evidence Inventory And Source Guards

Status: Codex-approved and locked.

Goal: inventory phone-first launch evidence, reuse locked screenshots, and pin
source-level mobile contracts without claiming final live screenshot closure.

Scope:

- Reuse locked HorseOps mobile screenshots for staff daily care, Care Ledger,
  owner request, and admin horse directory.
- Pin source-level mobile contracts for billing subscription, Signup Step 3,
  dashboard, and Mobile Readiness.
- Explicitly define the follow-up Build-Next-2B live screenshot gate for those
  four broader launch routes.

Deferred:

- No native app.
- No offline sync.
- No push notification implementation.
- No workflow-engine rewrite.

Exit criteria for 2A:

- Existing screenshot evidence remains valid.
- Remaining broader launch-route screenshot gaps are explicitly tracked for
  Build-Next-2B.
- Focused source/evidence tests pass.

Delivered:

- `BUILD_NEXT_2_MOBILE_READINESS_README.md`
- `outputs/build_next_2_mobile_readiness_matrix.md`
- `backend/tests/test_build_next_2_mobile_readiness.py`

Result: locked HorseOps-1J evidence already covers the six most sensitive Care
Ledger mobile screens at 390x844. Build-Next-2A pins source-level mobile
contracts for billing subscription, Signup Step 3, Dashboard, and Mobile
Readiness. Those four broader launch paths are not claimed as closed; they are
the explicit scope of Build-Next-2B.

Lock note: Build-Next-2A is complete as an inventory/source-guard phase. It
does not close the live screenshot evidence for the four broader launch routes.

### Build-Next-2B — Live Mobile Screenshot Gate

Status: Codex-approved and locked.

Goal: capture and verify the four broader launch-route mobile screenshots that
Build-Next-2A intentionally source-pins but does not close.

Scope:

- `/billing/subscription` with a real or seeded barn-manage account.
- Signup Step 3 with public plans loaded.
- `/dashboard` for a barn-management user.
- `/mobile-readiness` for an integrations/admin user.

Deferred:

- No native app.
- No offline sync.
- No push notification implementation.
- No workflow-engine rewrite.
- No backend route/schema/auth/permission changes.
- No billing behavior changes.
- No Admin Portal capability changes.

Exit criteria:

- Four new 390x844 screenshots exist, have valid image signatures and mobile
  dimensions, and are packaged under `outputs/`.
- Screenshots do not expose staff notes, raw daily-check payload internals,
  alert triggers, audit diffs, auth tokens, passwords, Stripe IDs, or private
  owner/admin-only fields.
- Focused screenshot-integrity tests pass.

Evidence captured: all four required live screenshots exist under
`outputs/build_next_2b_screenshots/`, have PNG signatures, and are exactly
`390x844`. Focused screenshot-integrity tests pass.

Lock note: Build-Next-2B is complete. Round-1 review fixes recaptured the
dashboard with a disposable `Build Next Manager` session and removed the static
Emergent badge from the app shell before all four screenshots were refreshed.

### Build-Next-3 — Multi-Barn / Multi-Role Account Model Gap Report

Status: Codex-approved and locked in
`outputs/build_next_3_multi_barn_multi_role_gap_report.md`.

Goal: reconcile the build packet's multi-barn/multi-role requirement with the
current implementation before expanding invites/transfers.

Scope:

- Read-only code/data audit of current `users`, `barns`, memberships, roles,
  permissions, invites, and ownership fields.
- Identify where one user can safely belong to multiple barns or roles today.
- Produce migration and route-impact plan.
- Add focused source/read-only tests only where they pin current assumptions.
- Package a gap report under `outputs/`.

Deferred:

- No schema migration.
- No account transfer writes.
- No invite behavior changes.
- No permission expansion.
- No billing, Stripe, Apple, HorseOps privacy, Admin Portal capability, landing
  page, native app, offline sync, or Phase 16 changes.

Exit criteria:

- Founder has a concrete gated implementation plan for multi-barn/multi-role
  support.
- The report separates safe-now behavior from future migration work and ends
  with the founder decisions required for implementation.

Founder decisions applied:

- Future membership collection: `account_memberships`.
- Users may hold multiple roles across owner, parent/student, lesson
  participant, trainer, staff, and facility contexts.
- Individual users may be active without an active facility; future onboarding
  should search for a facility and collect barn information as a sales lead when
  no active membership exists.
- Billing entitlements remain account/facility scoped, with the exception of a
  free individual-owner one-horse account.

Founder decisions locked before BN3A:

- Owner access remains horse-specific for launch.
- Preserve `users.barn_id` and `users.role` as compatibility mirrors through
  launch.
- Standalone owner account ids are generated, not raw `user_id`.
- Facility search / lead capture applies to all non-platform onboarding paths
  except invited users; individual owners may continue without an active
  facility.

### Build-Next-3A — Account Membership Schema Foundation

Status: Codex-approved and locked in
`BUILD_NEXT_3A_ACCOUNT_MEMBERSHIPS_README.md`.

Delivered:

- `account_memberships` foundation.
- Named indexes.
- Idempotent startup compatibility backfill from `users.barn_id` / `users.role`.
- Generated standalone owner account ids.

Strictly unchanged: auth, route guards, invites, onboarding, owner projection,
billing, Admin Portal, HorseOps privacy, landing pages, native/offline/push
behavior, and Phase 16.

### Build-Next-3B — Active Context + Facility Search Planning

Status: Codex-approved and locked in
`BUILD_NEXT_3B_ACTIVE_CONTEXT_README.md`.

Delivered:

- `backend/core/account_context.py` read-only active-context helpers.
- `GET /api/account/context` contract under `backend/routes/account_context.py`.
- Compatibility fallback from `users.barn_id` / `users.role` when no
  `account_memberships` rows exist.
- Multiple-membership selection by requested `account_id`.
- Planning-only facility-search contract that records the founder decision but
  performs no lead-capture writes.
- Conservative rejected/suspended handling: non-selectable memberships remain
  visible in `available_contexts` but are not selected as `active_context`.
- Round-1 P1 fallback fix: no-membership `horse_owner` users with no `barn_id`
  project as read-only `individual_owner` contexts, not the legacy `primary`
  facility.
- Round-2 P1 post-backfill fix: stored BN3A-shaped `source="users_mirror"`
  primary facility rows for no-barn horse owners are normalized at read time
  the same way, without mutating Mongo or changing BN3A backfill behavior.

Strictly unchanged: auth, route guards, invites, onboarding, facility-search UI,
lead-capture writes, owner projection, billing, Stripe, Apple, Admin Portal,
HorseOps privacy, landing pages, native/offline/push behavior, and Phase 16.

### Build-Next-3C — Route Guard Migration Plan

Status: Codex-reviewed and locked in
`BUILD_NEXT_3C_ROUTE_GUARD_MIGRATION_PLAN.md`.

Goal: migrate the first small pilot set of product read route guards from legacy
`users.barn_id` assumptions toward selected `account_memberships` context while
preserving launch-safe compatibility fallback.

Delivered pilot:

- dashboard read endpoints;
- horse roster/detail read endpoints.

Verification: 37/37 focused Build-Next-3 through Build-Next-3C tests passed.
Round-1 patch cleared the disabled legacy `users.barn_id` / selected active
facility edge case and repackaged `backend/server.py` with the review zip.

Strictly deferred: invite acceptance, onboarding/facility-search writes,
account transfer, role-switcher UI, Admin Portal capability changes, HorseOps
privacy changes, billing/Stripe/Apple/Phase 15R behavior, hard enforcement,
landing pages, native/offline/push work, and Phase 16 cleanup.

### Build-Next-3D — Task/Today Read-Scope Migration

Status: Codex-reviewed and locked in
`BUILD_NEXT_3D_TASK_CONTEXT_README.md`.

Goal: extend the BN3C selected-account read pattern to task-engine read routes
without migrating task writes or workflow behavior.

Delivered pilot:

- task template reads;
- task list reads;
- task today reads;
- horse timeline reads;
- staff activity reads;
- task analytics summary reads.

Verification: 43/43 focused Build-Next-3 through Build-Next-3D tests passed.

Strictly deferred: task/template writes, invite acceptance,
onboarding/facility-search writes, account transfer, role-switcher UI, Admin
Portal capability changes, HorseOps privacy changes, billing/Stripe/Apple/Phase
15R behavior, hard enforcement, landing pages, native/offline/push work, and
Phase 16 cleanup.

### Build-Next-4 — Invite, Registration, and Onboarding Polish

Status: Codex-reviewed and locked in
`BUILD_NEXT_4_INVITE_ONBOARDING_README.md`.

Goal: harden the launch-critical invite path now that `account_memberships`
exists.

Delivered:

- Existing-user invite acceptance without duplicate user creation.
- Existing-user invite acceptance requires the existing account password before
  membership/session issuance.
- Accepted invites create/update `account_memberships` rows with
  `source="invite"`.
- Existing users keep their current `users.barn_id` and `users.role` mirrors.
- Public duplicate signup remains blocked.
- Expired/revoked invite behavior.

Verification: 49/49 focused Build-Next-3 through Build-Next-4 tests passed.

Lock note: Codex P0 was closed by requiring existing-user password verification
before invite membership/session issuance.

Strictly deferred:

- No broad messaging rewrite.
- No legal document gates unless Build-Next-6 is approved first.

Exit criteria:

- Barn owner/manager can invite the right user, to the right barn/horse, with
  predictable status and no duplicate account drift.

### Build-Next-5 — Minor / Parent Safeguard Plan

Goal: turn the build packet's minor/student safety requirements into a gated
technical plan before messaging expansion.

Status: BN5-A, BN5-B, BN5-C, and BN5-D are Codex-reviewed and locked.

Scope:

- Parent/guardian profile requirements.
- Under-18 communication rules.
- Under-13 COPPA/legal decision points.
- Server-side enforcement matrix.
- Audit and privacy requirements.

Deferred:

- No messaging implementation until the rule matrix is approved.
- No legal claims beyond product requirements.

Exit criteria:

- Founder-approved rule matrix for parent-included communication and student
  account behavior.

Recommended shape:

- BN5-A: rule matrix and schema prep. Locked.
- BN5-B: guardian / student invite foundation. Locked.
- BN5-C: server-side minor communication guard. Locked.
- BN5-D: QA evidence and launch checklist. Locked.

Detailed gated execution plan, package names, scope ceilings, and acceptance
criteria live in `BUILD_NEXT_5_MINOR_PARENT_SAFEGUARDS_PLAN.md`.

### Build-Next-6 — Document / Signature Decision Gate

Goal: avoid rebuilding legal-document workflows by deciding integration vs
in-house before implementation.

Status: BN6A signature connector prep is Codex-reviewed and locked. BN6B
document workflow provider contract is ready for Codex review in
`BUILD_NEXT_6B_DOCUMENT_WORKFLOW_PROVIDER_README.md`.

Scope:

- Define document types required for launch.
- Use third-party e-signature for legal documents and in-house tracking for
  lower-risk operating acknowledgements.
- Prepare a DocuSign-style provider readiness connector.
- Define retention and countersignature needs.
- Draft data model and QA plan.

Deferred:

- No document signing implementation.
- No DocuSign SDK dependency or provider API call.
- No envelope creation, signing URL generation, provider webhook sync, or
  signed-document retrieval until a later legal/provider workflow phase.
- No required-document participation gate until approved.

Exit criteria:

- Approved document/signature implementation path with legal/accounting review
  notes captured.
- Connector readiness API reports required credential posture without exposing
  credential values.
- BN6B source contract defines the document matrix, signer routing, provider
  lifecycle status mapping, retention/export privacy boundary, and keeps all
  launch effects soft-warning only.

BN6A lock note:

- Read-only DocuSign-style provider readiness endpoint added at
  `/api/document-signatures/providers`.
- Endpoint requires `integration:read`, so owner/parent roles cannot inspect
  provider configuration posture.
- No DocuSign SDK, provider API calls, envelope creation, signing links,
  signed-document storage, or participation gates were added.

BN6B review note:

- Contract-only helper added in `backend/core/document_workflows.py`.
- No live signing workflow, provider webhook route, signing URL, signed-document
  storage, or participation gate was added.

BN6C lock note:

- Local template/request foundation added under `/api/document-signatures/*`.
- Facility `admin` and `barn_manager` users can register local document
  templates and create local document requests for their own barn.
- Local template/request list and detail reads are manager-only in BN6C; owner
  or parent request access remains deferred to the later signing experience.
- Request creation computes signer roles from the BN6B matrix and existing
  minor-status rules.
- Provider template IDs are stored only as local references. No live DocuSign
  envelope, signing URL, provider webhook, signed-document storage, legal text
  storage, or hard participation gate was added.
- Codex review found no remaining BN6C findings after the manager-only
  template/request read boundary was patched and verified.
- Next implementation remains split behind later approval.

Status: BN6D is Codex-reviewed and locked.

BN6D review note:

- Backend-only DocuSign sandbox JWT smoke added.
- `DOCUSIGN_PRIVATE_KEY_PATH` is supported as a safer alternative to inline
  private-key env text.
- The smoke script requests an OAuth access token only and never prints the
  token, JWT assertion, private key, private-key path, account id, user id, or
  provider payload.
- The smoke script also verifies that the configured account id is visible to
  the token through DocuSign `oauth/userinfo`.
- Local verification passed: BN6A-BN6D focused suite. Live DocuSign sandbox JWT
  smoke received an access token, verified the configured API account ID through
  `oauth/userinfo`, and attempted no envelope creation.
- No envelope creation, signing URL, provider webhook, signed-document storage,
  legal text storage, hard participation gate, owner signing UX, billing,
  Stripe, Apple, HorseOps, Admin Portal, landing, native, offline, push, service
  worker, or Phase 16 work was added.

Status: BN6E is Codex-reviewed and locked.

BN6E implementation note:

- Adds manager-only `POST /api/document-signatures/requests/{request_id}/sandbox-envelope`.
- Requires `DOCUSIGN_SANDBOX_ENVELOPES_ENABLED=true`, the DocuSign demo auth
  server, the DocuSign demo REST base URL, BN6D credentials, and a sandbox test
  signer email.
- Creates a DocuSign draft envelope only (`status=created`) from an existing
  BN6C local document request/template.
- Updates local request metadata only; normal projections continue to strip
  `provider_envelope_id`.
- No sent envelopes, signing URLs, provider webhook receiver, signed-document
  storage, signer UX, hard participation gate, billing, Stripe, HorseOps,
  Admin Portal, landing, native/offline/push, service worker, or Phase 16 work
  was added.
- Round-1 fixes: exact parsed demo REST base URL validation closes lookalike
  prefix hosts, and top-level sandbox readiness now mirrors full readiness.

Status: BN6F is Codex-reviewed and locked.

BN6F implementation note:

- Adds a live-capable, disabled-by-default DocuSign Connect webhook receiver at
  `/api/document-signatures/docusign/webhook`.
- Processing requires `DOCUSIGN_WEBHOOKS_ENABLED=true`, a configured
  `DOCUSIGN_WEBHOOK_SECRET`, valid `X-DocuSign-Signature-1` HMAC, matching
  `DOCUSIGN_ACCOUNT_ID`, and optional
  `DOCUSIGN_CONNECT_CONFIGURATION_ID=22209160`.
- The webhook updates only existing local document requests by
  `provider_envelope_id`; unknown envelopes return accepted/no-op.
- Stores status-only provider metadata and emits the existing safe audit
  projection.
- No raw provider payload, signer identity, envelope document, PDF bytes,
  signing URL, signed document, legal text, notification delivery, hard
  participation gate, billing, Stripe, Apple, HorseOps, Admin Portal, landing,
  native/offline/push, service worker, or Phase 16 work was added.
- Round-1 review finding closed: webhook matching is scoped to DocuSign
  provider-signature rows only, with a route-level fake-DB regression proving
  in-house/non-DocuSign rows sharing an envelope id are ignored.

### Build-Next-7 — Launch QA / UAT Gate

Status: Codex-reviewed and locked.

Goal: convert the build packet QA plan into an executable launch gate.

Scope:

- Role-based test matrix.
- Mobile evidence matrix.
- Billing provider safety matrix.
- Owner privacy matrix.
- Admin support matrix.
- Known-deferred-items list.

Deferred:

- No product feature work unless a blocker is found and separately scoped.

Exit criteria:

- Founder has a launch-readiness checklist tied to tests/evidence rather than
  loose confidence.

Delivered:

- `BUILD_NEXT_7_LAUNCH_QA_UAT_GATE_README.md`
- `outputs/build_next_7_launch_readiness_report.md`
- `outputs/build_next_7_evidence/manifest.md`
- `backend/tests/test_build_next_7_launch_gate.py`

Gate result:

- Controlled founder/staging UAT is conditionally ready.
- First-client pilot remains blocked pending human UAT, live payment lifecycle
  verification, DocuSign webhook deployment/verification, and production ops
  sign-off.
- Broad public launch remains no-go until the pilot blockers and go-live
  runbook are closed.

### Phase 16 — Legacy Billing Reconciliation and Cleanup

Phase 16 remains deferred until separately approved.

Minimum plan requirements:

- Reconcile in-flight legacy `payment_transactions`.
- Define deprecation window for old `/api/membership/*` stubs.
- Define hard-delete sequence and rollback plan.
- Confirm observability and support messaging.
- Confirm production Stripe price/config rollout status.

## Recommended Immediate Next Phase

After BN8 lock, close the remaining launch evidence gap:

- **Build-Next-9** — staging UAT execution evidence fill, using the locked BN7A
  checklist and BN8 runbook.

Phase 16 remains deferred until a separate legacy billing reconciliation and
hard-delete plan is approved.

### Build-Next-7A — Staging UAT Evidence Capture

Status: Codex-reviewed and locked.

Goal: turn BN7's launch-gate residual note into an executable staging UAT
evidence packet.

Delivered:

- `BUILD_NEXT_7A_STAGING_UAT_EVIDENCE_README.md`
- `outputs/build_next_7a_staging_uat_evidence_report.md`
- `outputs/build_next_7a_evidence/staging_uat_checklist.md`
- `outputs/build_next_7a_evidence/sanitized_evidence_log.md`
- `backend/tests/test_build_next_7a_staging_uat_evidence.py`

Gate result:

- The evidence packet is Codex-reviewed and locked.
- Human/staging UAT execution remains pending.
- First-client pilot remains blocked until BN7A required rows are passed or
  explicitly founder-accepted.
- Broad public launch remains no-go.

Next likely gate after BN7A review: execute the staging UAT checklist and then
prepare Build-Next-8 production go-live runbook.

### Build-Next-8 — Production Go-Live Runbook

Status: Codex-reviewed and locked.

Goal: create the final production go-live runbook and founder sign-off package.
This phase does not launch, deploy, call providers, mutate data, or approve
public launch.

Delivered:

- `BUILD_NEXT_8_PRODUCTION_GO_LIVE_RUNBOOK_README.md`
- `outputs/build_next_8_go_live_runbook.md`
- `outputs/build_next_8_env_boolean_checklist.md`
- `backend/tests/test_build_next_8_go_live_runbook.py`

Gate result:

- Runbook package is Codex-reviewed and locked.
- Production launch is not approved by this phase.
- First-client pilot still requires BN7A UAT evidence closure and founder
  sign-off.
- Broad public launch remains no-go.

Next likely gate after BN8 lock: run the BN7A staging checklist and fill the
BN8 production runbook with real, sanitized evidence.

### Build-Next-9 — Staging UAT Execution Evidence

Status: Codex-approved and locked.

Goal: convert the locked BN7A staging checklist into explicit evidence rows and
record the current UAT execution state without overclaiming launch readiness.

Delivered:

- `BUILD_NEXT_9_STAGING_UAT_EXECUTION_README.md`
- `outputs/build_next_9_staging_uat_execution_report.md`
- `outputs/build_next_7a_evidence/staging_uat_checklist.md`
- `outputs/build_next_7a_evidence/sanitized_evidence_log.md`
- `backend/tests/test_build_next_9_staging_uat_execution.py`

Gate result:

- All required UAT rows now have stable BN9 evidence references.
- Local dry-run screenshots were captured with disposable BN9 accounts.
- Human/staging walkthroughs remain pending until founder/operator execution.
- Live provider lifecycle evidence remains pending.
- Production operations sign-off remains pending.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

### Build-Next-10 — Official Staging UAT Closure Plan

Status: Codex-approved and locked.

Goal: lock the official evidence rules that turn BN7A/BN9 pending UAT rows into
real `pass`, `founder-accepted`, `fail`, or `deferred` outcomes without using
local dry-run evidence as launch-clearing proof.

Delivered:

- `BUILD_NEXT_10_STAGING_UAT_CLOSURE_README.md`
- `outputs/build_next_10_staging_uat_closure_report.md`
- `outputs/build_next_10_founder_decision_matrix.md`
- `backend/tests/test_build_next_10_staging_uat_closure.py`

Gate result:

- Official UAT environment is production-like staging.
- BN9 local screenshots are reference-only and cannot close UAT rows.
- Rian is the only actor who can mark a row `founder-accepted`.
- Stripe and DocuSign checks are allowed only as controlled live-safe checks.
- Apple remains deferred until the Apple billing phase is approved.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

### Build-Next-11 — Production-Like Staging Environment Proof

Status: Codex-approved and locked.

Goal: create the official staging-environment proof packet required by BN10
before any UAT row can move from `pending` to `pass` or `founder-accepted`.

Delivered:

- `BUILD_NEXT_11_STAGING_ENV_PROOF_README.md`
- `outputs/build_next_11_staging_environment_report.md`
- `outputs/build_next_11_staging_environment_checklist.md`
- `backend/tests/test_build_next_11_staging_environment_proof.py`

Gate result:

- Official staging identity remains blocked until frontend URL/domain, API base
  URL, build/version, environment label, database label, deploy marker, and
  feature-flag summary are supplied.
- Local app health is recorded as reference-only.
- Official role-account readiness remains pending.
- Stripe and DocuSign readiness remain pending.
- Apple remains deferred.
- First-client pilot remains blocked.
- Broad public launch remains no-go.

### Build-Next-12 Prep — Staging Inputs Collection

Status: ready for Codex review.

Goal: defer BN12 execution and create a founder walkthrough for gathering the
official staging identity inputs BN12 will need later.

Delivered:

- `BUILD_NEXT_12_PREP_STAGING_INPUTS_README.md`
- `outputs/build_next_12_prep_staging_inputs_checklist.md`
- `outputs/build_next_12_prep_staging_inputs_walkthrough.md`
- `backend/tests/test_build_next_12_prep_staging_inputs.py`

Gate result:

- BN12 remains deferred.
- Required staging inputs are listed in a safe collection checklist.
- Localhost is explicitly forbidden as official UAT evidence.
- No provider lifecycle actions are executed.
- First-client pilot remains blocked.
- Broad public launch remains no-go.
