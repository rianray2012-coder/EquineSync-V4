# Build Next RF7 Owner Client Portal Hardening

RF7 packages owner, guardian, and client portal hardening evidence for review.

## Scope

- Use the existing owner-safe horse endpoint for owner/guardian portal horse inventory.
- Route owner and guardian service submissions through the owner-care-ledger request endpoint.
- Preserve staff/admin preview service-request behavior.
- Document deferred leasee, limited-trial, owner-media, and billing truth decisions.
- Generate a reproducible report and review zip.

## Out of Scope

- No provider calls.
- No Stripe, Apple, Google, DocuSign, Resend, MongoDB Atlas, Vercel, or Render mutations.
- No native app implementation.
- No leasee grant/revocation implementation.
- No full limited-trial access-cap enforcement.
- No founder acceptance auto-marking.
- No RF17 feature-shell retirement.

## Files

- `frontend/src/pages/OwnerPortal.jsx`
- `backend/routes/horse_ledger.py`
- `docs/RF7_OWNER_GUARDIAN_CLIENT_PORTAL_HARDENING.md`
- `backend/core/rf7_owner_client_portal_hardening.py`
- `backend/scripts/build_rf7_owner_client_portal_hardening.py`
- `backend/tests/test_rf7_owner_client_portal_hardening.py`
- `outputs/rf7_owner_client_portal_hardening_report.md`
- `outputs/build_next_rf7_owner_client_portal_hardening.zip`

## Verification Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf7_owner_client_portal_hardening.py
.venv/bin/python backend/scripts/build_rf7_owner_client_portal_hardening.py --fail-on-blockers
npm --prefix frontend run build
unzip -t outputs/build_next_rf7_owner_client_portal_hardening.zip
git diff --check
```
