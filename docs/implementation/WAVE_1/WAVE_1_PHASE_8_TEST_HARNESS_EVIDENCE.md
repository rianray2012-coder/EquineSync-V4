# Wave 1 Phase 8 Test Harness Evidence

State: `WAVE_1_PHASE_8_FULL_TEST_HARNESS_COMPLETE`

The isolated harness used MongoDB on `127.0.0.1:27018`, a `wave1_*` database,
the local API on `127.0.0.1:8001`, synthetic demo accounts, a test JWT secret,
empty Stripe configuration, and disabled DocuSign webhooks.

## Results

| Suite | Result |
| --- | --- |
| Previously blocked server suites (`test_phase2c_auth.py`, `test_admin_portal_admin3.py`) | 42 passed |
| Wave 1 hardening/integration/context/convergence | 33 passed |
| Invite public-route regression plus refresh race | 21 passed |
| Frontend role-status permission tests | 3 passed |
| Focused backend compilation | passed |
| Focused ESLint | passed |
| `git diff --check` | passed |

Repairs made while restoring the harness: explicit local demo seeding, public
invite routes use the optional-auth facility gate, fixed routes precede dynamic
invite IDs, and refresh replay preserves one atomic winner while revoking the
entire family. No test was replaced or marked obsolete.
