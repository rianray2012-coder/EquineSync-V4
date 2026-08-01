# Implementation Change Record

Status: `IMPLEMENTED`

Changed implementation surfaces:
- `backend/core/minor_safety.py`: V1.1 Guardian/Minor authority, consent, lifecycle, public-error, audit, state-token, and index helpers.
- `backend/core/minor_communication.py`: DB-backed message participant/minor resolver and per-minor guardian coverage gate.
- `backend/core/lifespan.py`: additive authority/consent index creation.
- `backend/routes/student_guardians.py`: authority-scoped guardian links, workflow consents, revocation, consent cascade, and guarded lesson-ready transition.
- `backend/routes/operations.py`: guarded lessons, training sessions, messages, and event/community-program service requests.
- `backend/routes/document_signatures.py`: guarded waiver/document/media requests and sandbox-envelope transition.
- `backend/routes/billing.py`: guarded invoice create and local paid-status transition.
- `backend/routes/recurring_charges.py`: guarded recurring template create/update and materialized invoice writes.
- `backend/routes/care.py`: rider subject fields for authoritative student/minor resolution.
- `backend/tests/test_cgp006_iwp0002_guardian_minor_safeguarding.py`: 43 focused regression and abuse tests.

No deployment, provider integration, staging, production, GAP_0004, Wave 2, or CGP-007 changes were made.
