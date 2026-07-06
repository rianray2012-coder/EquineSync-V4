# RF7 Owner, Guardian, and Client Portal Hardening

Date: 2026-07-06

Status: Codex-reviewed and locked.

## Purpose

RF7 hardens the owner, guardian, and client portal trust surface after RF1, RF5,
and RF6. It uses existing owner-safe backend contracts rather than expanding
the product surface.

## Completed Hardening

| Area | RF7 Status | Evidence |
| --- | --- | --- |
| Owner portal horse inventory | ready | Owner and guardian portal horse lists now call `/owner-portal/horses` and normalize the backend `{items}` response. Staff preview users continue to call `/horses`. |
| Owner/guardian service submission | ready | Horse owners and guardian-linked parent users submitting from `OwnerPortal.jsx` now post to `/horse-ledger/{horse_id}/owner-service-requests`, which validates owner/guardian horse linkage, rate limits, and strips staff notes from owner/guardian reads. |
| Owner request display | ready | Owner portal request rows now render either legacy `type/details` rows or owner-care-ledger `request_type/message` rows. |
| Owner-safe backend horse contract | ready | RF1 `/owner/horses` and `/owner-portal/horses` remain present with stable owner, guardian, and rider predicates. |
| Owner care ledger contract | ready | Owner summary and owner service-request endpoints remain on the hardened HorseOps owner ledger contract; guardian-linked parent users may submit/read only their own requests for guardian-linked horses. |
| Backlog owner portal feeds | ready | Media, forms, and health-document feeds continue to use stable owner/user/horse clauses. |

## Deferred or Founder-Decision Items

| Item | Status | Next Action |
| --- | --- | --- |
| Feature-module owner media updates | deferred | `owner_updates` is canonical, but `owner_media_updates` remains a migration/hide candidate for RF17. |
| Limited modified-individual-owner trial access caps | deferred | RF5/RF7 document the posture. Server-side access-cap enforcement must be accepted and tested in RF18 before stronger claims. |
| Leasee invite/grant/revocation model | deferred | Leasee access remains invite-only from horse owner or assigned trainer with owner oversight preserved. RF7 does not implement the grant model. |
| Concierge billing/payment truth | deferred | RF7 preserves staff/admin preview service-request behavior. Payment truth remains RF12. |

## Founder Decision Rows

| Decision | Status | Phase |
| --- | --- | --- |
| Accept that RF7 hardens owner portal reads and owner request submission without implementing leasee grants. | requires founder review | RF7/RF18 |
| Accept limited modified-individual-owner trial posture as documented but not fully enforced in RF7. | requires founder review | RF7/RF18 |
| Accept Owner Updates lifecycle as canonical for owner-trust updates. | requires founder review | RF6/RF7/RF17 |
| Accept the legacy concierge service request workflow for staff/admin preview users while horse owners submit through owner-care-ledger requests. | requires founder review | RF7/RF12 |

## Launch Claim Boundary

Current launch/pilot claims may say owner portal horse inventory and
owner/guardian request submission use owner-safe contracts.

Do not claim:

- full leasee support;
- fully enforced limited-trial access caps;
- feature-module owner media migration completion;
- universal owner portal UAT acceptance;
- payment/concierge billing truth;
- provider or native app readiness from RF7.

## Evidence

Generated report:
`outputs/rf7_owner_client_portal_hardening_report.md`.

Review package:
`outputs/build_next_rf7_owner_client_portal_hardening.zip`.

## RF7 Lock Note

RF7 is Codex-reviewed and locked after re-review found no remaining blocker
findings. The generated report status is `ready` with zero blocked or missing
rows.

Lock verification:

- Focused RF7 tests passed.
- RF7 report generation passed with blocker failure enabled.
- Frontend build passed.
- Zip integrity and expected manifest checks passed.
- `git diff --check` and RF7 secret-shape scan passed.

RF7 does not implement leasee grants, full limited-trial enforcement,
feature-module owner-media retirement, concierge billing truth, provider calls,
native apps, or founder acceptance auto-marking.
