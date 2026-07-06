# EquineSync Refinement Roadmap

Date: 2026-07-06

Status: RF0 and RF1 CODEX-REVIEWED & LOCKED. RF2 is next.

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
| RF2 | Identity-Based Access Migration | Replace name-based matching with stable IDs. | Owner, staff, document, provider, billing, and message access no longer depends on display names; temporary fallbacks are documented and marked for removal. |
| RF3 | Onboarding 2.0, Import Concierge, and Setup Integrations | Turn onboarding/import/setup into guided, review-first workflows. | Users can import draft data safely; required/optional setup is clear; integration readiness is truthful; AI suggestions require review. |
| RF4 | Feature Completion Certification and Placeholder Elimination | Classify every visible feature as hidden, scaffold, readiness, pilot beta, live, or deprecated. | No daily user sees a fake-live feature; every nav item maps to a live/pilot or approved readiness surface; no placeholder/dev/test copy in user-facing production UI. |
| RF5 | Admin Portal Intelligence, Customer Success, Billing Intervention, and Account Health | Expand platform admin into customer-success, billing health, support, account health, and product intelligence. | Platform admins can see user/facility health; support can find stuck users; billing actions are audited; sensitive content is scrubbed; barn admins remain separate. |
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

Proceed to RF2 - Identity-Based Access Migration.

RF1 locked these source-backed blockers:

- QuickBooks invoice export currently reads all invoices in `backend/routes/backlog.py`.
- Backlog owner-portal billing/forms/health/training surfaces still use `full_name`, `owner_name`, `recipient_name`, or free-text sharing fields.
- Some sensitive routes have frontend gates and broad capability groups, but RF1 must prove backend authority for each direct route.

RF2 should follow immediately because several remaining risks are caused by
broader name-based access.

## Lock Note

RF0 is Codex-reviewed and locked as an evidence-only refinement intake. It does
not implement RF1-RF18.

## RF1 Lock Note

RF1 is Codex-reviewed and locked as a narrow P0 data-fence and
backend-capability gate. See `docs/RF1_DATA_FENCES_CAPABILITY_GATES.md` and
`outputs/rf1_data_fences_capability_gates_report.md`.

RF2 may proceed as the next dedicated phase.
