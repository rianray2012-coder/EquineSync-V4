# RF7 Owner, Guardian, and Client Portal Hardening Report

Phase: `RF7`
Overall status: `ready`

## Status Rows

| Key | Area | Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| owner_portal_uses_owner_safe_horse_inventory | Owner portal horse inventory | ready | Owner and guardian portal horse lists now use `/owner-portal/horses` and normalize the `{items}` response. Staff preview users stay on the barn horse list. | RF18 should browser-smoke the owner, guardian, and staff-preview portal paths with seeded accounts. |
| owner_guardian_requests_use_owner_care_ledger_contract | Owner and guardian service requests | ready | Horse-owner and guardian submissions now go through the owner-care-ledger request route, which validates owner/guardian horse linkage, rate limits, and strips staff notes on owner/guardian reads. | Keep the legacy `/service-requests` approval workflow for staff/admin preview users until RF12 decides concierge billing/payment truth. |
| backend_owner_safe_horse_endpoint_exists | Backend owner-safe horse contract | ready | RF1 owner-safe horse endpoints remain present and are based on stable owner, guardian, and rider identity fields. | Do not reintroduce `/horses` as the default owner portal inventory endpoint. |
| backend_owner_summary_and_request_contract_remains_safe | Owner care ledger contract | ready | Owner summaries and owner-care requests remain on the hardened HorseOps owner ledger contract rather than raw barn operational records. | RF18 should verify no owner surface renders raw alert internals, staff notes, audit rows, or hidden handling fields. |
| owner_portal_backlog_feeds_use_stable_clauses | Backlog owner portal feeds | ready | Owner portal media/forms/health-document feeds continue to rely on stable owner/user/horse clauses rather than display-name matching. | RF17 should migrate or hide feature-module owner media feeds after founder accepts Owner Updates as canonical. |
| owner_updates_canonical_but_media_duplicate_deferred | Owner updates canonical surface | deferred | Owner Updates remains canonical, but feature-module `owner_media_updates` still exists as a migration/hide candidate. | RF17 should hide, redirect, or migrate owner media updates; RF7 does not remove feature-module data. |
| limited_trial_and_leasee_depth_remain_explicit | Enrollment caveats | deferred | RF5/RF7 documents preserve the limited-trial and leasee requirements without claiming the deeper grant, revocation, and access-cap implementation is complete. | Implement leasee grants/revocation and limited-trial server caps only when founder accepts that policy and RF18 UAT scope is ready. |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Accept that RF7 hardens owner portal reads and owner request submission without implementing a leasee grant model. | requires founder review | RF7, RF18 | Leasee invites remain invite-only from the horse owner or assigned trainer, with owner oversight preserved, but grant/revocation data model work is deferred. |
| Accept limited modified-individual-owner trial posture as documented but not fully enforced in RF7. | requires founder review | RF7, RF18 | Rider, guardian, and staff public self-signup must stay invite-first except the limited fallback path; server-side access caps remain RF18/UAT work. |
| Accept Owner Updates lifecycle as canonical for owner-trust updates. | requires founder review | RF6, RF7, RF17 | Feature-module owner media updates remain migration/hide candidates and must not be presented as the canonical owner-update workflow. |
| Accept the legacy concierge service request workflow for staff/admin preview users while horse owners submit through owner-care-ledger requests. | requires founder review | RF7, RF12 | RF7 keeps staff approval/decline behavior intact; later payment/concierge billing truth stays RF12. |

## RF7 Boundary

- RF7 hardens owner/guardian/client portal reads and owner request submission against existing owner-safe backend contracts.
- RF7 does not implement native apps, provider calls, billing mutations, Stripe changes, account deletion flows, broad feature-shell retirement, or founder acceptance auto-marking.
- RF7 does not implement the full leasee grant/revocation model or fully enforce limited-trial access caps; those remain explicit founder/UAT decisions.
- Current launch claims may say owner portal horse inventory and owner/guardian request submission now use owner-safe contracts. They must not claim full leasee support or fully enforced limited-trial access caps.
