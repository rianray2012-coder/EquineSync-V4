# RF10 Service Provider / Care Partner Multi-Barn Model

Date: 2026-07-06

Status: CODEX-REVIEWED & LOCKED.

## Purpose

RF10 creates a backend-authoritative service-provider access foundation without
claiming broad barn-wide provider access, payment truth, messaging delivery, or
legal document workflows.

## Completed Hardening

| Area | RF10 Status | Evidence |
| --- | --- | --- |
| Explicit provider grants | ready | Provider visibility is driven by active `horse_provider_assignments` linked by stable `provider_user_id` or a stable provider catalog row linked to the user. |
| Provider operating center | ready | Adds `/service-provider/operating-center`, provider-role scoped, facility gated, and grant scoped for horses, vet records, farrier records, and visit notes. |
| Provider visit notes | ready | Adds `/service-provider/visit-notes`; provider notes require a granted horse and stamp `provider_user_id`, `horse_name`, and the granted horse barn. |
| Direct horse/care route scoping | ready | Provider roles no longer inherit broad direct horse/care reads; `/horses`, `/vet-records`, `/farrier-history`, `/injuries`, `/wellness`, medication routes, owners, and riders are provider-safe. Medication-log reads are scoped by granted medication and barn. |
| Canonical care write boundary | ready | Provider-authored RF10 care entries are limited to `/service-provider/visit-notes`; canonical care creates and medication/feed completions remain facility-owned. |
| Care Ledger assignment identity | ready | Care Ledger service-provider catalog and assignment rows can carry validated stable `provider_user_id`. |
| Operating-center grant projection | ready | The provider operating-center returns a safe grant projection instead of raw assignment rows or internal assignment notes. |
| Service-provider dashboard | ready | `/dashboard/service-provider` now renders grant-scoped provider work from the new operating-center API. |

## Deferred or Founder-Decision Items

| Item | Status | Next Action |
| --- | --- | --- |
| Provider invoices, payments, payouts, refunds | deferred | RF12 owns billing/payment/provider invoice truth. |
| Provider documents and legal signatures | deferred | RF14 owns legal document/signature/storage truth. |
| Provider messaging delivery | deferred | RF13 owns recipient and delivery truth. |
| External provider integrations | deferred | RF6 integration-readiness boundary remains manifest/status only until provider-specific proof exists. |
| Account-level cross-facility provider identity | deferred | RF10 proves same-barn stable `provider_user_id` assignment validation and explicit grant scoping; broader stable provider identity across unrelated barns needs future account-membership policy and RF18 UAT. |
| First provider type for UAT | requires founder review | Choose farrier, veterinarian, or another service-provider type for seeded RF18 UAT. |

## Founder Decision Rows

| Decision | Status | Phase |
| --- | --- | --- |
| Choose first RF10 provider type for UAT. | requires founder review | RF10 |
| Decide service-provider signup review posture. | requires founder review | RF5/RF10 |
| Decide provider grant authority. | requires founder review | RF10/RF18 |
| Decide provider invoice/payment timing. | requires founder review | RF10/RF12 |

## Launch Claim Boundary

Current launch/pilot claims may say service providers have grant-scoped horse
and care context with provider-authored visit notes.

Do not claim:

- broad barn-wide provider access is complete;
- account-level cross-facility provider identity is complete;
- providers can write canonical care records outside provider visit notes;
- provider invoices, payments, payouts, refunds, or Stripe truth are complete;
- provider messaging delivery is complete;
- provider legal documents/signatures/storage are complete;
- external provider integrations are live;
- native/offline provider behavior is complete.

## Evidence

Generated report:
`outputs/rf10_service_provider_care_partner_report.md`.

Review package:
`outputs/build_next_rf10_service_provider_care_partner.zip`.
