
# Data Flow And Trust Boundary Map

## Primary Flows

1. Public and authenticated browser traffic enters the React application, then calls backend `/api` routes.
2. Backend auth routes create and refresh JWT/session tokens and read/write users, refresh tokens, auth tokens, and login-attempt state.
3. Product routes read/write barn-scoped Mongo documents through explicit `barn_filter`, route dependencies, or route-local filters where present.
4. Platform-admin routes use `platform_role` checks and admin reference scrubbing rather than ordinary barn-role trust.
5. Billing routes and webhooks use Stripe SDK references and local Mongo status/idempotency records, but provider behavior is not verified by this audit.
6. Storage routes/helpers prepare local stub or S3/R2-compatible upload intents; provider configuration is not verified by this audit.
7. Minor-safeguarding helpers classify age, guardian requirements, and communication inclusion; complete workflow enforcement remains a gap.
8. Background lifecycle startup creates indexes, optional local seed behavior, task materialization, notification loops, digest loops, and provider catalog provisioning where environment allows.

## Trust Boundaries

| Boundary | Repository Evidence | Current-State Treatment |
| --- | --- | --- |
| Browser to API | `frontend/src/lib/api.js`; `backend/server.py` | Direct code evidence; route-level authorization still needs endpoint matrix. |
| JWT to user document | `backend/core/auth.py` | Authoritative user document is loaded; JWT barn claim is not authority. |
| User to barn/facility | `backend/core/tenancy.py`; `backend/server.py` | Application-level barn and active-facility controls exist; complete route proof incomplete. |
| Barn role to platform role | `backend/core/permissions.py` | Platform role is separate from barn role. |
| Provider callbacks to local state | `backend/routes/subscriptions.py`; `backend/routes/document_signatures.py` | Signature/HMAC checks are coded; provider runtime evidence absent. |
| Audit event writer to audit log | `backend/core/audit.py` | Redaction and write helpers exist; fail-open and retention/recovery require later evidence. |
| Governance documents to implementation | `governance/implementation/code-guides/PROGRAM_STATUS.md` | Documentary authority only; implementation remains unauthorized. |

## Inference Label

Every inference in this file is labeled `INFERENCE_REQUIRES_CONFIRMATION`. Repository evidence is not runtime, staging, pilot, production, or independent security certification evidence.
