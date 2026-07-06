# RF10 Service Provider / Care Partner Report

Phase: `RF10`
Overall status: `ready`

## Status Rows

| Key | Area | Status | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| provider_grant_helper | Explicit provider grant helper | ready | RF10 adds a shared provider-access helper driven by active explicit horse-provider assignments, same-barn stable provider user IDs, and explicit provider catalog links. | RF18 should seed revoked/cross-barn/provider-type UAT cases. |
| provider_operating_center | Service-provider operating center API | ready | RF10 adds a provider-role operating center for grant-scoped horses, vet records, farrier records, and provider-authored visit notes. | RF18 should browser-smoke seeded provider accounts. |
| direct_horse_and_care_scoping | Direct route provider scoping | ready | Provider roles no longer inherit broad direct horse/care reads; legacy horse and care routes use explicit provider grants, including medication-log filtering by granted medication and barn. | RF18 should add full browser UAT against direct-route attempts. |
| provider_canonical_care_writes_restricted | Canonical care write boundary | ready | RF10 limits provider-authored care entries to provider visit notes; canonical care creates remain facility-owned until a later policy phase. | Founder should decide which provider types may write canonical care records before that scope is enabled. |
| provider_assignment_stable_user_ids | Provider assignment stable IDs | ready | Care Ledger service-provider and assignment rows can now link to stable provider user IDs with same-barn validation. | Founder should decide grant authority and provider approval posture before broader claims. |
| account_level_provider_identity | Cross-facility provider identity | deferred | RF10 proves explicit grant scoping and same-barn stable provider_user_id assignment validation; account-level provider identity across unrelated barns remains deferred. | RF18 or a future account-membership policy phase should prove stable cross-facility provider identity before stronger multi-barn claims. |
| provider_dashboard_not_shell | Service-provider dashboard | ready | Service-provider dashboard now renders grant-scoped provider work instead of static shell cards. | RF18 should capture provider screenshots with seeded grants. |
| provider_billing_deferred | Provider billing and payouts | deferred | RF10 does not implement provider invoices, payouts, refunds, Stripe, or payment truth. | RF12 owns billing/payment/provider invoice truth. |
| provider_documents_messaging_deferred | Provider documents and messaging | deferred | RF10 does not implement messaging delivery truth, legal signatures, or provider document storage truth. | RF13 owns delivery truth; RF14 owns legal document/signature/storage truth. |

## Founder Decision Rows

| Decision | Status | Phase | Notes |
| --- | --- | --- | --- |
| Choose first RF10 provider type for UAT. | requires founder review | RF10 | Recommended first choice remains farrier or veterinarian because both require explicit horse grants and visit-note context. |
| Decide service-provider signup review posture. | requires founder review | RF5, RF10 | RF5 separates service-provider enrollment; RF10 keeps approval posture as founder-review work. |
| Decide provider grant authority. | requires founder review | RF10, RF18 | Current RF10 mutation path is barn admin / manager through Care Ledger provider assignment rows. |
| Decide provider invoice/payment timing. | requires founder review | RF10, RF12 | RF10 does not implement provider invoice/payment/payout truth. |

## RF10 Boundary

- RF10 hardens service-provider access through explicit active horse grants, same-barn stable provider user IDs, and explicit provider catalog links.
- RF10 provider-authored writes are limited to `/service-provider/visit-notes`; canonical care writes remain facility-owned until a later policy phase.
- RF10 does not implement provider invoices, payouts, Stripe, live provider API calls, messaging delivery truth, legal signatures/storage truth, native/offline behavior, or founder acceptance auto-marking.
- Current launch claims may say providers have grant-scoped horse/care context and provider-authored visit notes. They must not claim broad barn-wide provider access, account-level cross-facility provider identity, canonical care-write authority, payment truth, messaging delivery, or legal document workflows are complete.
