# EquineSync Refinement Roadmap

Date: 2026-07-06

Status: RF0, RF1, RF2, RF3, RF4, RF5, RF6, RF7, RF8, RF9, RF10, RF11, RF12, RF13, RF14, RF15, RF16, RF17, and RF18 CODEX-REVIEWED & LOCKED. RF19 is prepared for Codex review.

## Purpose

This roadmap starts the RF refinement track after the locked BN21 web-first first-client pilot go/no-go gate. RF is not a single mega-PR. Each phase must be small, evidence-backed, independently reviewed, and locked before the next phase expands scope.

Current launch posture remains:

- Web-first / PWA-assisted pilot.
- Native App Store / Google Play distribution is source-shell ready through
  RF16, and local Android debug / iOS simulator builds pass. Store submission
  remains out of scope.
- Online-first with limited field recovery, not full offline support.
- No universal cached reads, universal queued writes, service-worker offline
  shell, IndexedDB universal outbox, broad conflict-review UI, provider
  offline support, app-store availability claim, app-store submission claim, or
  native billing compliance claim.
- Feature shells and readiness surfaces must not be treated as complete daily workflows.

## RF Phase List

| Phase | Name | Purpose | Acceptance Criteria |
| --- | --- | --- | --- |
| RF0 | Refinement Intake, Evidence Freeze, and Scope Control | Inventory known findings and freeze scope before fixes. | Every known issue has a classification and RF phase; source evidence is recorded; next phase is recommended; founder/product owner approves ordering. |
| RF1 | P0 Data Fences and Backend Capability Gates | Fix highest-risk tenant isolation, owner-safe data, backend authorization, and export scoping. | Owner cannot receive unrelated horses or invoices; cross-barn billing/export leakage is impossible; sensitive writes have backend gates; direct-route tests prove boundaries. |
| RF2 | Identity-Based Access Migration | Replace highest-risk name-based access matching with stable IDs. | Staff self-service access no longer depends on display names; payroll supports stable staff filtering; document signature identity evidence is recorded; provider, message, and full workforce identity work is explicitly deferred to RF8/RF10/RF13/RF17. |
| RF3 | Onboarding 2.0, Import Concierge, and Setup Integrations | Turn onboarding/import/setup into guided, review-first workflows. | Users can import draft data safely; required/optional setup is clear; integration readiness is truthful; AI suggestions require review. |
| RF4 | Feature Completion Certification and Placeholder Elimination | Classify every visible feature as hidden, scaffold, readiness, pilot beta, live, or deprecated. | No daily user sees a fake-live feature; every nav item maps to a live/pilot or approved readiness surface; no placeholder/dev/test copy in user-facing production UI. |
| RF5 | Admin Portal Intelligence, Customer Success, Web Enrollment, Billing Intervention, and Account Health | Expand platform admin into customer-success, web enrollment/signup entry-point health, billing health, support, account health, and product intelligence. | Platform admins can see user/facility health; support can find stuck users; login/home signup entry points route no-account users to the correct enrollment path; billing actions are audited; sensitive content is scrubbed; barn admins remain separate. |
| RF6 | Canonical Systems Consolidation | Choose one source of truth per domain and retire split systems. | Operational tasks, inventory, owner updates, documents, billing, and integration readiness each have one canonical system or explicit migration/hide decision. |
| RF7 | Owner, Guardian, and Client Portal Hardening | Finish owner/guardian/rider trust surfaces. | Owners, guardians, and riders see only linked records; staff/internal notes remain hidden; payment/document/request state is accurate. |
| RF8 | Staff Workforce Model | Unify staff identity, scheduling, tasks, handoffs, time clock, and payroll export. | Staff schedule, My Work, time clock, handoffs, and payroll use stable user IDs and audited corrections; operational tasks remain Task Engine tasks. |
| RF9 | Trainer Operating Center and Trainer Fluidity | Build real trainer workflows across lessons, horse training, haul-ins, packages, and multi-facility contexts. | Trainers can operate across barns without leakage; lessons and horse training are separate workflows; records link by stable IDs. |
| RF10 | Service Provider / Care Partner Multi-Barn Model | Support vets, farriers, bodyworkers, haulers, and other providers across barns and clients. | Providers have scoped multi-barn/client access, explicit horse grants, revocation, visit notes, documents, and invoices when enabled. |
| RF11 | Property, Location, Map, and Community Help System | Replace text-based location records with canonical property/location models and safe contribution logs. | Horses have canonical home/current locations; moves are audited; owner/rider map/help access is explicit and permissioned. |
| RF12 | Billing, Payments, Exports, and Financial Truth | Separate bookkeeping, owner payments, provider status, app-store billing policy, and export truth. | No cross-barn exports; payment UI does not overstate Stripe; invoices/payments/refunds/voids are scoped and audited; store billing policy is documented. |
| RF13 | Messaging, Notifications, and Delivery Truth | Make communication real, traceable, guardian-safe, and not overpromised. | Sent means delivered or logged; recipients are ID-based; guardian/minor rules are enforced; push readiness does not imply live push. |
| RF14 | Documents, Signatures, and Storage Consolidation | Make document signatures/storage canonical and truthful. | Legal signatures are not confused with local acknowledgements; guardian/minor signer rules are enforced; signed metadata is auditable. |
| RF15 | Offline, Lock-Screen, and Field Reliability Implementation | Build the real weak-signal/offline reliability system if claims require it. | Last-known-good reads, queued field-critical writes, draft recovery, reconnect sync, conflict review, and cache clearing are proven before claims. |
| RF16 | PWA, Native App, App Store, and Google Play Implementation | Move from native-store deferred to actual mobile distribution readiness. | iOS/Android projects run; TestFlight/Play internal tests exist; metadata/privacy/data-safety/review account/screenshots/billing policy are complete. |
| RF17 | Feature-Shell Retirement and UX Truth Pass | Ensure every visible page is real workflow, readiness/admin setup, or hidden. | No "almost feature" appears in daily nav; readiness lives under Admin Setup; empty states are truthful and actionable. |
| RF18 | QA, UAT, Migration, and Public Launch Re-Readiness | Prove all refinements before broader launch. | No P0 data leaks; no split truth; no name-based primary access; trainer/provider/onboarding/admin/offline/native claims match source truth. |
| RF19 | Official Staging UAT Evidence Capture | Execute the RF18 UAT ledger in the approved staging environment and package evidence without mutating production or approving public launch. | Every RF18 UAT row has staging evidence, sanitized artifact references, pass/fail/blocker status, and founder-decision rows remain unaccepted until explicit founder review. |

## Phase Ordering

Recommended default order:

```text
RF0 -> RF1 -> RF2 -> RF3 -> RF4 -> RF5 -> RF6 -> RF7 -> RF8 -> RF9 -> RF10 -> RF11 -> RF12 -> RF13 -> RF14 -> RF15 -> RF16 -> RF17 -> RF18 -> RF19
```

Acceleration is allowed only after RF1 and RF2 are safe. Do not build RF9/RF10 trainer/provider expansion on top of unsafe data fences or name-based access.

## Current Recommendation

Current gated phase is RF19 - Official Staging UAT Evidence Capture. RF19 is
prepared for Codex review as an evidence-capture gate. It records locked RF18
input evidence and blocks official UAT closure until the staging URL, safe UAT
account roster, redaction rules, and sanitized artifact index are supplied.

RF1 locked these source-backed blocker fixes:

- QuickBooks invoice export reads invoices by `barn_id`.
- Backlog owner-portal billing/forms/health/training predicates use stable owner/user/horse clauses.
- Sensitive financial/reporting routes retain backend capability gates proven by RF1 source tests.

RF2 locked as a narrow identity-access migration for staff
self-service predicates, payroll export stable filtering, and document
signature identity evidence. It intentionally defers full workforce backfill,
provider grants, message-recipient identity, and feature-shell UI rewrites to
RF8/RF10/RF13/RF17.

## Lock Note

RF0 is Codex-reviewed and locked as an evidence-only refinement intake. It does
not implement RF1-RF18.

## RF1 Lock Note

RF1 is Codex-reviewed and locked as a narrow P0 data-fence and
backend-capability gate. See `docs/RF1_DATA_FENCES_CAPABILITY_GATES.md` and
`outputs/rf1_data_fences_capability_gates_report.md`.

RF4 is Codex-reviewed and locked. RF5 may proceed.

## RF3 Lock Note

RF3 is Codex-reviewed and locked. See
`docs/RF3_ONBOARDING_IMPORT_SETUP.md` and
`outputs/rf3_onboarding_import_setup_report.md`.

RF3 must not be expanded into a full importer rewrite, AI auto-mapping, live
provider setup, service-provider grants, or staff workforce backfill after lock.
Active import scope is horses and owners; riders, staff, service providers, and
feed/medication lists remain explicitly deferred.

## RF2 Lock Note

RF2 is Codex-reviewed and locked. See
`docs/RF2_IDENTITY_BASED_ACCESS_MIGRATION.md` and
`outputs/rf2_identity_access_migration_report.md`.

RF2 must not be expanded into RF8 workforce implementation after lock. Strict
stable-ID staff self-service matching is accepted for RF2, and legacy name-only
staff rows remain RF8 migration/backfill work.

## RF4 Lock Note

RF4 is Codex-reviewed and locked. See
`docs/RF4_FEATURE_COMPLETION_CERTIFICATION.md` and
`outputs/rf4_feature_completion_certification_report.md`.

RF4 locked with report status `ready`, zero blocker rows, and one deferred
scaffold row for Staff Tasks versus Task Engine consolidation. RF4 classifies
all 32 feature-module keys, pins eight direct feature/readiness routes, and
narrows copy for manifest exports, push previews, local form/signature status,
integration readiness, limited field-recovery/mobile readiness, Admin Portal
permissions, and owner role-intake fallback panels.

RF4 does not close RF6/RF8/RF12/RF13/RF14/RF15/RF16/RF17. Founder review still
must decide which readiness/scaffold pages stay visible before RF17 and whether
manifest-only exports and push previews are acceptable until their later
implementation phases.

## RF4 Pre-Lock Enrollment Note

Before RF4 lock, founder requested that EquineSync add a general web-based
enrollment workflow. This is recorded as RF0-F19 in the master fix list and is
mapped into the current RF plan:

- RF5 owns the web enrollment/signup foundation: home-page signup, login-page
  join/signup entry point, account creation credentials, critical signup data,
  and a clear four-path selector for individual horse owner, barn owner/manager,
  service provider, and trainer.
- Rider, guardian, and staff accounts are invite-first; RF5 may record a
  limited seven-day modified individual-owner trial fallback when facility,
  trainer, or provider contact information is supplied, but enforcement remains
  future work.
- Leasee access must be invite-only from the horse owner or assigned trainer,
  while the owner keeps oversight access.
- RF7 owns individual horse/owner enrollment depth, including owners whose barns
  are not on EquineSync, owners keeping horses on their own land, family or
  informal care contexts, limited-trial semantics, and leasee invite/grant
  behavior.
- RF9 owns trainer-specific enrollment depth.
- RF10 owns service-provider enrollment depth.
- RF18 must re-test the enrollment paths before broader launch.

RF4 does not implement enrollment. This note is included so RF5 planning does
not miss the signup entry-point and individual-horse enrollment requirement.

## RF5 Entry Boundary

RF5 may start with the RF0-F19 web enrollment foundation and evidence-backed
customer-success/account-health inventory. RF5 must not implement RF7 owner
portal hardening, RF9 trainer operating-center depth, RF10 service-provider
multi-barn grants, RF12 payment truth, or RF18 UAT closure inside the opening
RF5 pass.

## RF5 Lock Note

RF5 is Codex-reviewed and locked. See
`docs/RF5_WEB_ENROLLMENT_ACCOUNT_HEALTH.md` and
`outputs/rf5_web_enrollment_account_health_report.md`.

RF5 opening-gate status is `ready` with zero blocker rows. It adds a public
`/enroll` path selector, routes home and login Join actions to enrollment before
credential collection, locks signup role/context to the selected enrollment
path, keeps rider/guardian/staff out of the main public path grid, records the
limited-trial and leasee caveats, and inventories Admin Portal
account-health/customer-success surfaces.

RF5 does not lock founder decisions or complete RF7 individual owner depth, RF9
trainer operating-center workflows, RF10 service-provider access grants, RF12
billing intervention/payment truth, or RF18 UAT acceptance.

RF6 may proceed as a canonical systems consolidation gate. RF6 should identify
one source of truth, alias/read-only posture, hide decision, or explicit
migration/defer decision for duplicated operational tasks, inventory, owner
updates, documents/signatures, billing, and integration-readiness surfaces.

## RF6 Lock Note

RF6 is Codex-reviewed and locked. See
`docs/RF6_CANONICAL_SYSTEMS_CONSOLIDATION.md` and
`outputs/rf6_canonical_systems_consolidation_report.md`.

RF6 status is `ready` with zero blocker rows. It records source-of-truth posture
for six duplicated domains:

- Task Engine is canonical for operational tasks; Staff Tasks is a migration,
  hide, or admin-readiness candidate for RF8/RF17.
- Inventory is canonical for stock/supply truth; Supply Inventory should alias,
  migrate, or hide before operators rely on it as a second stock ledger.
- Owner Updates is canonical for owner-trust lifecycle; owner media updates
  should migrate or hide in RF7/RF17.
- Document Signatures is canonical for legal signature workflows; Digital Forms
  remains local acknowledgement/readiness until RF14.
- Account subscription records are canonical billing entitlement truth; legacy
  membership/payment feature records are not subscription truth.
- Integration readiness remains manifest/status evidence only until later
  provider phases.

RF6 does not migrate data, hide routes, redirect URLs, add schemas, change auth,
mutate billing, call providers, or mark founder decisions accepted.

RF7 may proceed as the owner, guardian, and client portal hardening gate. RF7
should build on RF1 stable owner-safe predicates, RF5 enrollment caveats, and
RF6 canonical owner-update decisions without expanding trainer/provider,
billing, document-signature, or feature-shell retirement scope beyond the owner
trust surface.

## RF7 Lock Note

RF7 is Codex-reviewed and locked. See
`docs/RF7_OWNER_GUARDIAN_CLIENT_PORTAL_HARDENING.md` and
`outputs/rf7_owner_client_portal_hardening_report.md`.

RF7 status is `ready` with zero blocked or missing rows. It hardens
`frontend/src/pages/OwnerPortal.jsx` so owner/guardian horse inventory uses
`/owner-portal/horses`, while staff preview users continue to use `/horses`.
Owner/guardian service submissions from the owner portal now use the hardened
owner-care-ledger request contract at
`/horse-ledger/{horse_id}/owner-service-requests`; request display handles both
legacy `type/details` rows and owner-care-ledger `request_type/message` rows.

RF7 does not implement leasee grants/revocation, full limited-trial server
access caps, feature-module owner-media migration/hide, concierge billing truth,
provider calls, native app work, or founder acceptance auto-marking.

RF8 may proceed as the staff work and Task Engine alignment gate.

## RF8 Lock Note

RF8 is Codex-reviewed and locked. See `docs/RF8_STAFF_WORKFORCE_MODEL.md` and
`outputs/rf8_staff_workforce_model_report.md`.

RF8 status is `ready` with zero blocked or missing rows. It adds a safe
same-barn staff directory endpoint, requires stable staff IDs on new covered
staff-module creates, normalizes supplied staff user IDs to trusted display
names server-side, and updates staff scheduling, Staff Tasks, handoff, and
time-clock create flows to require and submit stable staff user IDs.

RF8 preserves RF2 self-service ID predicates for My Work, staff task status,
time clock, and payroll export. RF8 does not migrate historical name-only rows,
delete Staff Tasks, migrate Staff Tasks into Task Engine, change billing truth,
add provider grants, or mark founder decisions accepted.

RF9 may proceed as the Trainer Operating Center and Trainer Fluidity gate. See
`docs/RF9_TRAINER_OPERATING_CENTER_PLAN.md`.

## RF9 Lock Note

RF9 is Codex-reviewed and locked. See `docs/RF9_TRAINER_OPERATING_CENTER.md` and
`outputs/rf9_trainer_operating_center_report.md`.

RF9 status is `ready` with zero blocked or missing rows. It adds an
ID-scoped trainer operating-center read model, stable trainer-owned lesson and
training log semantics, stable-ID Training Plan creates, and a trainer-specific
dashboard at `/dashboard/trainer`.

RF9 preserves trainer intake as review-gated setup intent. RF9 does not
implement trainer package billing, Stripe changes, haul-in workflows,
school-horse workflows, broad multi-facility trainer grants, service-provider
multi-barn grants, native/offline behavior, or founder acceptance
auto-marking.

RF10 is Codex-reviewed and locked as the Service Provider / Care Partner
Multi-Barn Model gate. See `docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md`.

## RF10 Package Note

RF10 is Codex-reviewed and locked. See
`docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md` and
`outputs/rf10_service_provider_care_partner_report.md`.

RF10 status is `ready` with zero blocked or missing rows. It adds an explicit
provider-grant helper, same-barn stable `provider_user_id` validation for Care
Ledger provider assignments, safe grant projections, a provider-role operating
center at `/service-provider/operating-center`, provider-authored visit notes,
direct provider horse/care read scoping, and a real service-provider dashboard.

RF10 does not implement provider invoices, payouts, Stripe changes, live
provider API calls, messaging delivery truth, legal signature/storage truth,
provider canonical care-write authority, account-level cross-facility provider
identity, native/offline behavior, or founder acceptance auto-marking.

RF11 proceeded as the Property, Location, Map, and Community Help System
gate. See `docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP_PLAN.md`.

## RF11 Lock Note

RF11 is Codex-reviewed and locked. See
`docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP.md` and
`outputs/rf11_property_location_map_community_help_report.md`.

RF11 status is `ready` with zero blocked or missing rows. It hardens existing
barn-location and arena-share endpoints with explicit share-state metadata and
owner/parent-safe projections. Owner/parent barn-location shares require the
stored share setting to be enabled and omit internal stall notes and pasture
weather-rule text. Owner/parent arena shares include only
`shared_with_owners` blocks and omit internal owner-name, notes, and share
metadata fields.

RF11 does not implement canonical property/location IDs, movement audit history,
live maps, geocoding, route navigation, dispatch, public community networking,
native/offline behavior, true QR encoding, QR scanning, provider calls, or
founder acceptance auto-marking.

RF12 proceeded as the Billing, Payments, Exports, and Financial Truth gate.
See `docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH_PLAN.md`.

## RF12 Lock Note

RF12 is Codex-reviewed and locked. See
`docs/RF12_BILLING_PAYMENTS_EXPORTS_FINANCIAL_TRUTH.md` and
`outputs/rf12_billing_payments_exports_financial_truth_report.md`.

RF12 status is `ready` with zero blocked or missing rows. It fixes automation
billing recommendations so overdue invoice counts are scoped to the current
`barn_id`, proves owner payment preparation remains configuration-only, and
keeps QuickBooks/report/payroll exports truthful as scoped manifest/download
readiness.

RF12 does not implement live QuickBooks sync, provider payouts, paid trainer
package billing, native app-store billing, refunds/voids, live payment
collection, provider calls, or founder acceptance auto-marking.

RF13 may proceed as the Messaging, Notifications, and Delivery Truth gate. See
`docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH_PLAN.md`.

## RF13 Lock Note

RF13 is Codex-reviewed and locked. See
`docs/RF13_MESSAGING_NOTIFICATIONS_DELIVERY_TRUTH.md` and
`outputs/rf13_messaging_notifications_delivery_truth_report.md`.

RF13 status is `ready` with zero blocked or missing rows. It scopes Task Engine
notification candidates to the event barn/tenant, normalizes Group Messaging
custom recipients into stable `recipient_user_ids`, hardens owner/guardian
announcement projections, and keeps push manifests and Group Messaging UI
truthful as preview-only/local-log readiness.

RF13 does not implement live APNs/FCM push delivery, SMS, broad email
messaging, provider/trainer direct messaging, public community messaging,
device-token collection, provider receipts, provider calls, or founder
acceptance auto-marking.

## RF14 Lock Note

RF14 is Codex-reviewed and locked. See
`docs/RF14_DOCUMENTS_SIGNATURES_STORAGE_CONSOLIDATION.md` and
`outputs/rf14_documents_signatures_storage_consolidation_report.md`.

RF14 report status is `ready` with zero blocked or missing rows. It enforces
guardian IDs for guardian-required document requests, keeps signer/provider
references out of default document projections, labels Digital Forms as local
acknowledgement or provider-readiness records, and records document scan
storage as upload-intent-only evidence.

RF14 does not implement live DocuSign envelope sending, signing URLs,
production signed-document storage, storage retention/deletion workflows,
provider/trainer document access, provider calls, or founder acceptance
auto-marking.

RF15 has completed and locked as the Offline, Lock-Screen, and Field
Reliability Implementation gate.

## RF15 Lock Note

RF15 is Codex-reviewed and locked. See
`docs/RF15_OFFLINE_LOCK_SCREEN_FIELD_RELIABILITY.md` and
`outputs/rf15_offline_lock_screen_field_reliability_report.md`.

RF15 report status is `ready` with zero blocker rows. It creates an explicit
workflow capability registry, preserves narrow queued-write claims for task
complete, task skip/refuse, and bulk task complete, preserves draft-only claims
for QuickAdd and HorseOps forms, and keeps sensitive/provider/admin/billing/
legal/medical/incident/owner-request/provider-visit workflows online-only or
provider-online.

RF15 does not implement full offline app support, service-worker/PWA offline
app shell, native app behavior, IndexedDB universal outbox, universal cached
reads, universal queued writes, broad conflict-review UI, provider offline
support, UAT mutation, provider calls, or founder acceptance auto-marking.

RF16 has completed and locked as the PWA, Native App, App Store, and Google
Play Readiness gate.

## RF16 Lock Note

RF16 is Codex-reviewed and locked. See
`docs/RF16_PWA_NATIVE_APP_STORE_READINESS.md` and
`outputs/rf16_pwa_native_app_store_readiness_report.md`.

RF16 report status is `ready` with zero source or local build blocker rows. It
adds Capacitor dependencies/config, generates iOS and Android project shells,
proves web build output exists, records app identity defaults as `EquineSync`
/ `com.equinesync.app`, verifies Android debug and iOS simulator build
outputs, and keeps store-submission, native billing, and broad native/offline
overclaim guards clean.

RF16 does not submit to App Store Connect or Google Play Console, create store
listings or review accounts, implement native billing, complete privacy labels
or Google Data safety answers, call providers, mutate UAT accounts, broaden
RF15 offline claims, or auto-mark founder acceptance.

RF17 has completed and locked as the Feature-Shell Retirement and UX Truth Pass.

## RF17 Lock Note

RF17 is Codex-reviewed and locked. See
`docs/RF17_FEATURE_SHELL_UX_TRUTH.md` and
`outputs/rf17_feature_shell_ux_truth_report.md`.

RF17 report status is `ready` with zero blocker rows. It redirects duplicate
direct routes from Supply Inventory to Inventory, Staff Tasks to Today, owner
media updates to Review Queue, Group Messaging to Messaging, and Advanced
Reports to Reports. Daily Manager/Trainer navigation now points Owner Requests
at Review Queue, and Trainer Reports at Reports.

RF17 keeps Group Messaging, Advanced Reports, Mobile Readiness, Integrations,
and Forms & Signatures truth-labeled. It does not delete data, perform data
migrations, call providers, submit to stores, implement native billing,
implement true provider sync/delivery, broaden offline/native claims, mutate
UAT accounts, or auto-mark founder acceptance.

RF18 is the next gated phase, but it is not started by RF17 lock.

## RF18 Locked Status

RF18 is Codex-reviewed and locked. See
`docs/RF18_QA_UAT_PUBLIC_LAUNCH_READINESS.md` and
`outputs/rf18_qa_uat_public_launch_readiness_report.md`.

RF18 report status is `ready_for_founder_uat_review` with zero source blocker
rows. It records the locked RF1-RF17 evidence matrix, launch-critical source
evidence, overclaim guards, seven staging-UAT rows, migration/backfill
classification rows, and founder decision rows.

RF18 public launch status is `no_go_until_uat_acceptance`. RF18 does not mutate
production, staging, seeded-demo, or UAT accounts; does not call providers;
does not submit to stores; does not collect live payments; does not run
destructive migrations; and does not approve public launch or auto-mark founder
acceptance.

RF18 package:
`outputs/build_next_rf18_qa_uat_public_launch_readiness.zip`.

Next gated phase: RF19 Official Staging UAT Evidence Capture. RF19 must not
mark founder acceptance, approve public launch, mutate production data, call
external providers, collect live payments, submit app stores, or run
destructive migrations.

## RF19 Plan

RF19 should convert the seven RF18 UAT rows into an official staging evidence
packet.

Recommended RF19 scope:

- Confirm the official staging URL, test accounts, account roles, and evidence
  redaction rules before capture.
- Execute UAT rows for enrollment/signup, owner/guardian/rider visibility,
  staff/trainer workflows, service-provider grants, billing/payment/export
  truth, documents/signatures/messaging, and field reliability/native shell.
- Capture sanitized evidence references only: route, role, expected result,
  observed result, artifact path or screenshot reference, timestamp, and
  pass/fail/blocker status.
- Keep live provider delivery, live legal signatures, live Stripe money
  movement, App Store / Google Play submission, native billing, full offline
  support, destructive migrations, and production mutations out of scope.
- Produce founder-decision rows for blocked, failed, deferred, or launch-risk
  items without auto-accepting them.

Suggested RF19 artifacts:

- `BUILD_NEXT_RF19_STAGING_UAT_EVIDENCE_CAPTURE_README.md`
- `docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE.md`
- `docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE_PLAN.md`
- `backend/core/rf19_staging_uat_evidence_capture.py`
- `backend/scripts/build_rf19_staging_uat_evidence_capture.py`
- `backend/tests/test_rf19_staging_uat_evidence_capture.py`
- `outputs/rf19_staging_uat_evidence_capture_report.md`
- `outputs/build_next_rf19_staging_uat_evidence_capture.zip`

## RF19 Prepared For Review

RF19 is prepared for Codex review. See
`docs/RF19_STAGING_UAT_EVIDENCE_CAPTURE.md` and
`outputs/rf19_staging_uat_evidence_capture_report.md`.

RF19 report status is `blocked_pending_official_staging_evidence`. This is an
intentional gate status because no official staging URL/account roster,
redaction rules, or sanitized evidence artifact index is present in the repo.

RF19 public launch status is `no_go_until_founder_acceptance`. RF19 does not
mutate production, staging, seeded-demo, or UAT accounts by itself; does not
call providers; does not submit to stores; does not collect live payments; does
not run destructive migrations; and does not approve public launch or
auto-mark founder acceptance.

Next action: review RF19, then provide or approve the official staging context
and evidence artifacts before any row can be marked passed.
