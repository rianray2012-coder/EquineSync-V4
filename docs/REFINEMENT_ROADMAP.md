# EquineSync Refinement Roadmap

Date: 2026-07-06

Status: RF0, RF1, RF2, RF3, RF4, RF5, RF6, RF7, RF8, RF9, and RF10 CODEX-REVIEWED & LOCKED. RF11 is ready for planning.

## Purpose

This roadmap starts the RF refinement track after the locked BN21 web-first first-client pilot go/no-go gate. RF is not a single mega-PR. Each phase must be small, evidence-backed, independently reviewed, and locked before the next phase expands scope.

Current launch posture remains:

- Web-first / PWA-assisted pilot.
- Native App Store / Google Play distribution deferred.
- Online-first with limited field recovery, not full offline support.
- No universal cached reads, universal queued writes, service-worker offline shell, IndexedDB universal outbox, broad conflict-review UI, provider offline support, or native app-store readiness claim.
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

## Phase Ordering

Recommended default order:

```text
RF0 -> RF1 -> RF2 -> RF3 -> RF4 -> RF5 -> RF6 -> RF7 -> RF8 -> RF9 -> RF10 -> RF11 -> RF12 -> RF13 -> RF14 -> RF15 -> RF16 -> RF17 -> RF18
```

Acceleration is allowed only after RF1 and RF2 are safe. Do not build RF9/RF10 trainer/provider expansion on top of unsafe data fences or name-based access.

## Current Recommendation

Proceed with RF11 - Property, Location, Map, and Community Help System.

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

RF11 may proceed as the Property, Location, Map, and Community Help System
gate. See `docs/RF11_PROPERTY_LOCATION_MAP_COMMUNITY_HELP_PLAN.md`.
