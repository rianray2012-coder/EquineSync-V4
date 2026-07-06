# RF1 Data Fences And Capability Gates Report

Phase: `RF1`

Overall status: `ready`

## Readiness Rows

| Key | Status | Evidence | Next Action |
| --- | --- | --- | --- |
| `owner_safe_horse_endpoint` | `ready` | `backend/routes/horse_ledger.py` exposes owner-safe horse lists using stable owner/guardian/rider IDs. | RF7 can deepen portal UX and response contracts after RF1 is reviewed. |
| `quickbooks_invoice_export_scope` | `ready` | QuickBooks invoice export now reads invoices with `barn_id` scope. | RF12 should handle deeper accounting/export truth and provider/payment variants. |
| `owner_portal_identity_scope` | `ready` | Owner portal media/forms/health/emergency/training reads use stable owner/user/horse predicates. | RF2 should migrate remaining non-RF1 name-based staff/provider/document surfaces. |
| `owner_billing_payment_scope` | `ready` | Owner billing and payment prep are barn-scoped and account-identity-scoped, without horse-only authorization. | RF12 should finish payment truth, refunds, voids, and collection-state accuracy. |
| `owner_updates_relationship_scope` | `ready` | Published owner updates now resolve owned horses through primary/secondary owner ID fields. | RF6/RF7 should consolidate owner updates versus media-update backlog surfaces. |
| `sensitive_route_capability_gates` | `ready` | Financial and reporting routes retain backend capability gates backed by fail-closed permission helpers. | RF2/RF4 should continue route-by-route matrices as feature surfaces are hidden or certified. |
| `reporting_dashboard_revenue_scope` | `ready` | Backlog dashboard revenue totals no longer read all invoices globally. | RF12 should finish export/report format truth. |

## Founder Decision Rows

| Decision | Status | RF Phase | Notes |
| --- | --- | --- | --- |
| Accept stricter owner portal matching for legacy name-only records. | requires founder review | RF1, RF2 | RF1 intentionally does not expose records that only match by display/free-text name; RF2 should migrate legacy data to stable IDs. |
| Decide whether RF1 should be re-run against seeded cross-barn integration fixtures before lock. | optional founder review | RF1 | Source tests prove the fence shape; live-seeded integration tests can be added if desired before lock. |

## Acceptance Boundary

- RF1 closes the P0 source-level tenant/export/owner-portal data fence findings identified in RF0.
- RF1 does not complete RF2 identity migration, RF7 portal UX hardening, RF12 billing/payment truth, or RF17 feature-shell retirement.
- RF1 does not mutate provider services, Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, Render, or UAT accounts.
