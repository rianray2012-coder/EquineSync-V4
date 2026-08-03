# EquineSync — Product, UX & Governance Review

**Date:** 2026-08-03
**Scope:** Full repository — frontend, backend, admin portal, brand system, governance corpus.
**Method:** Direct code inspection (routes, models, components) cross-checked against rendered product screenshots (`p_onboarding.jpg`, `p_billing.jpg`, `c_onboarding.jpg`, `c_reports.jpg`).

An interactive version of this report (with a navigable feature matrix) is available as a Claude Artifact; this file is the durable, repo-committed record.

## Executive summary

- The core operating loop — barn setup, care tasks, trainer/staff/service-provider dashboards, Stripe billing, e-signatures — is real and functioning, not scaffolding.
- The three consumer-facing roles the brand is built around (Horse Owner, Rider, Guardian) land on a static placeholder dashboard with zero API calls.
- The shipped app uses a light lavender theme; every design document in the repo (`design_guidelines.json`, `docs/DESIGN_TOKENS.md`, `docs/BRAND_AND_LOGO_GUIDE.md`) specifies a dark "Luxury" theme. The two have diverged silently.
- A **"Made with Emergent" watermark renders in the live product UI**, visible in onboarding, admin reports, and billing screenshots. This is the single highest-priority fix.
- `barn_id` multi-tenant isolation is enforced in roughly one of eight backend route modules — a structural gap for a product whose pitch is multi-barn coordination.
- The governance/doc corpus (~1,900 markdown files, 790 in `docs/canon/` alone) is disproportionate to the actual codebase (582 files, ~129k lines), two internal tech-debt registers disagree with each other, and some docs are stale in both directions.
- The admin portal has strong observability (KPIs, audit log, support tickets, role-gated access) but is read-only on billing, has no impersonation, and no in-app role/permission management.

## Function & UX by role

| Role | Dashboard status | Notes |
|---|---|---|
| Barn / Facility Owner | Exists | Real API-backed dashboard; most complete journey, including the 9-step onboarding wizard. |
| Trainer | Exists | Dedicated dashboard, own operating-center endpoint, proper loading/error states. |
| Service Provider | Exists | Real data, clear empty state. |
| Barn Staff | Exists | Uses shared "Today" task view. |
| Barn Manager | Needs work | No manager-specific view; silently reuses the Owner (business/financial) dashboard. |
| Horse Owner | Missing/broken | Static shell, no API calls, hardcoded "will appear here" copy. |
| Rider | Missing/broken | Same static shell as Owner. |
| Guardian / Parent | Missing/broken | Same shell; no minor-safety UI surfaced despite that being an actively governed workstream. |

**Strong:** onboarding wizard (autosave, readiness gate), documents/e-signatures, reports/analytics.
**Needs work:** Messaging (55-line form + flat list, no threads/attachments); Billing (no loading/error state, can flash "No invoices yet"); a literal "I" glyph bug in two Admin Reports stat tiles; empty invoice descriptions render as a bare "."; `RoleIntake.jsx` is 2,393 lines in one file.
**Missing:** no service worker anywhere in the frontend despite offline work being described as "locked"; no help center or provider/community marketplace page exists in the app.

## Feature build-out matrix

| Feature area | Status | Evidence |
|---|---|---|
| **Core operations** | | |
| Barn onboarding & setup | Exists | `pages/Onboarding.jsx`, `routes/onboarding.py` |
| Care / task workflows | Exists | `routes/horse_ledger.py` (2,350 lines), `routes/care.py` |
| Horse & profile records | Exists | `routes/horses.py`, `rider_profile.py` |
| ~30 feature-backlog CRUD modules | Needs work | `routes/backlog.py` — generic wrapper schema, weak typing |
| **Money & documents** | | |
| Stripe billing & subscriptions | Exists | `core/billing_provisioning.py`, live webhook handling |
| Owner billing UI | Needs work | `pages/Billing.jsx` — no loading/error state |
| E-signatures (DocuSign) | Needs work | `core/document_signing.py` — sandbox-gated, not confirmed live |
| QuickBooks / Calendar / wearables / doc-scan / QR | Doesn't exist | `backlog.py` — explicit "credentials_required" stubs |
| **Communication** | | |
| Transactional & lifecycle email | Exists | `mailer.py` (Resend), 8 templates |
| Owner daily digest / weekly recap | Exists | `routes/digests.py`, `owner_digest.py` — built, under-promoted |
| In-app messaging | Needs work | `pages/Messaging.jsx` — no threads |
| Push notifications | Doesn't exist | placeholder only |
| **Consumer experience** | | |
| Owner / Rider / Guardian dashboard | Doesn't exist | `PersonalDashboard.jsx` — static, zero API calls |
| Community / help center / marketplace | Doesn't exist | RF11 — plan doc only |
| Horse transfer / passport continuity | Doesn't exist | Deferred to "Wave 3" |
| **Platform & trust** | | |
| Multi-tenant (barn) isolation | Doesn't work | `barn_id` enforced in ~1 of 8 route modules; absent from User model |
| Centralized role permissions | Doesn't work | `ROLE_PERMISSION_MATRIX.md` unenforced beyond one ad hoc check |
| Audit logging | Exists | `core/audit.py`, `routes/audit.py` — works, though `DATA_MODEL.md` still calls it unimplemented |
| Soft delete / retention | Doesn't work | Locations, inventory, staff invites use hard deletes |
| Offline / PWA reliability | Doesn't exist | No service worker found |
| Native app shell (iOS/Android) | Needs work | Capacitor builds locally; store submission, native icons not done |
| **Admin & operations** | | |
| Admin observability (KPIs, audit, tickets) | Exists | `routes/admin_portal/` — 3,945 lines, 14 modules |
| Admin billing actions (refund/override) | Doesn't exist | read-only, no write routes |
| User impersonation for support | Doesn't exist | no route or UI found |
| Role/permission management UI | Doesn't exist | frontend "Permissions" page is a placeholder |

## Design & brand

The shipped theme (soft lavender-ivory surfaces, near-black ink text — `frontend/tailwind.config.js`) contradicts every governing design document (Midnight Graphite / Slate Navy / Frost White / Smoky Lilac "Luxury Dark" — `design_guidelines.json`, `docs/DESIGN_TOKENS.md`, `docs/BRAND_AND_LOGO_GUIDE.md`). Only the admin portal kept the original dark palette. This needs a decision (which theme is canonical) followed by doc reconciliation.

**Urgent:** a "Made with Emergent" badge is rendered in the live product UI on every screenshot reviewed — remove before any customer-facing use.

The horse-icon mark is distinctive and well drawn, but its "circuit board" motif reads more fintech/AI-startup than quiet equestrian luxury — a tension worth resolving deliberately rather than leaving implicit. Branding gaps: mobile app icons are still the generic default Capacitor icon (zero brand presence on the home screen); the favicon (a plain "ES" text monogram) doesn't match the horse icon used elsewhere; email templates carry a text-only wordmark on a palette that predates the current brand system; only 4 of 8 catalogued brand-asset variants are actually wired into the app.

## Admin portal

Works well: KPI dashboard, user approve/suspend/reactivate (suspend genuinely revokes tokens), facility disable/re-enable, support ticketing, searchable audit log, usage reports with CSV export, four role-gated admin tiers.

Gaps: billing/subscriptions are entirely read-only (no refund, credit, or plan override — a real fix requires leaving the app for Stripe or the database); no user impersonation for support debugging; no admin MFA despite suspend/disable powers; no feature-flag toggle UI; no GDPR-style export/delete tooling; the founder admin roster is hardcoded via a CLI seed script and the in-app "Permissions" page is a placeholder.

**Verdict:** a real, disciplined observability and light-user-lifecycle tool, not yet sufficient to run day-to-day support and billing operations without dropping into raw infrastructure.

## Governance

The governance system (a ~30-document canon of locked domain models, a program board tracking build "waves," and a 10-item Privacy Impact Assessment portfolio) is coherent in intent but disproportionate in scale: `docs/canon/` alone holds 790 markdown files, and root-level `BUILD_NEXT_*`/`PHASE_*` files number 129, against a codebase of 582 files (~129k lines) that is still a fairly ordinary pre-MVP app (no enforced tenant isolation, no centralized permission service).

Two internal tech-debt registers disagree: the "official" governance register lists ~1 open item; the code-grounded `KNOWN_TECH_DEBT.md` lists 15, each with file/line citations. Documentation is stale in both directions (audit logging marked "not yet implemented" though it works in code; offline reliability described as "locked" though no service worker exists). The PIA work is substantive (including real minor-safeguarding and consent analysis) but paper-stage — not founder-approved for implementation, and the controls it assumes (soft delete, audit trail, tenant isolation) are only partially real.

Every locked canon document explicitly grants zero implementation authority, meaning significant documentation effort is producing artifacts that don't unlock any capability to build — worth a direct conversation about pacing governance work against the concrete, code-grounded gaps above.

**Repo hygiene:** two empty files sit at the repo root with sentence-fragment names — leftover artifacts from a broken prior automated run. Harmless but should be deleted.

## Growth opportunities

- **Surface the digest, don't just build it** — the owner daily digest/weekly recap (`owner_digest.py`) is fully built but under-promoted; anchor the Owner dashboard around it once that page is wired to real data.
- **Horse passport & continuity** — currently deferred to "Wave 3"; a horse's care/vet/ownership history following it across a sale or barn change is a real differentiator, not just a feature.
- **Provider marketplace** — RF11 exists only as a plan; connecting vets/farriers/trainers to barns closes a workflow gap and creates a network effect.
- **Branded owner portal per barn** — a natural premium-tier upsell reusing the existing brand-token system.
- **Trust badges for verified providers** — makes the existing "Owner Trust Framework" doc tangible to users.
- **Push reminders once notifications ship** — vaccination/farrier/vet due-dates pushed to an owner's phone, using the already-scaffolded push stub.

## Priority punch list

1. Remove the "Made with Emergent" watermark from the live product UI. *(Brand — urgent)*
2. Wire the Owner / Rider / Guardian dashboard to real data. *(UX — high)*
3. Decide light vs. dark as the one true theme and reconcile the design docs. *(Design — high)*
4. Enforce `barn_id` tenant isolation across all route modules. *(Platform — high)*
5. Add loading/error states to Billing and Messaging. *(UX — medium)*
6. Generate branded native app icons for Android/iOS. *(Brand — medium, low effort)*
7. Give admin billing at least one write action (refund or credit). *(Admin — medium)*
8. Build a real permission-management UI in the admin portal. *(Admin — medium)*
9. Reconcile the two conflicting tech-debt registers into one source of truth. *(Governance — medium)*
10. Delete the two stray empty junk files at the repo root. *(Hygiene — low)*
