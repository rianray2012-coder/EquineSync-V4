# Build Next RF10 Service Provider / Care Partner

RF10 is Codex-reviewed and locked as the service-provider and care-partner grant hardening gate.

## Scope

- Add explicit provider grant helpers backed by active `horse_provider_assignments`.
- Link service-provider catalog/assignment rows to stable `provider_user_id`.
- Add a grant-scoped service-provider operating-center API.
- Add provider-authored visit notes for granted horses.
- Scope direct provider horse/care reads to explicit grants.
- Scope provider medication-log reads by granted medication and barn.
- Keep canonical care writes facility-owned; provider-authored RF10 entries use visit notes only.
- Return safe grant projections instead of raw assignment rows.
- Replace the service-provider dashboard shell with a grant-scoped workspace.
- Preserve provider enrollment, billing, messaging, document, native, and offline deferrals.

## Out of Scope

- No Stripe, provider invoice, payout, refund, or payment mutations.
- No live provider API calls.
- No DocuSign, Resend, Apple, Google, Vercel, Render, Atlas, or UAT account mutation.
- No messaging delivery truth.
- No legal document/signature/storage truth.
- No broad barn-wide provider grants.
- No account-level cross-facility provider identity claim.
- No provider canonical care-write authority beyond provider visit notes.
- No founder acceptance auto-marking.

## Files

- `backend/core/provider_access.py`
- `backend/routes/service_provider_center.py`
- `backend/routes/horses.py`
- `backend/routes/care.py`
- `backend/routes/horse_ledger.py`
- `backend/server.py`
- `frontend/src/features/dashboards/ServiceProviderDashboard.jsx`
- `backend/core/rf10_service_provider_care_partner.py`
- `backend/scripts/build_rf10_service_provider_care_partner.py`
- `backend/tests/test_rf10_service_provider_care_partner.py`
- `docs/RF10_SERVICE_PROVIDER_CARE_PARTNER.md`
- `docs/RF10_SERVICE_PROVIDER_CARE_PARTNER_PLAN.md`
- `outputs/rf10_service_provider_care_partner_report.md`
- `outputs/build_next_rf10_service_provider_care_partner.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf10_service_provider_care_partner.py
.venv/bin/python backend/scripts/build_rf10_service_provider_care_partner.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf10_service_provider_care_partner.zip
git diff --check
```
