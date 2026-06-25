# Phase HorseOps-1K - Release Readiness & Privacy Hardening

Status: Codex-approved and locked.

## Purpose

HorseOps-1K is a release-readiness closure pass for the locked HorseOps
track. It consolidates evidence from HorseOps-1A through 1J, verifies the
privacy boundaries that matter most before launch hardening, and packages a
small review artifact.

This is not a feature phase.

## Scope

Allowed:

- Documentation and evidence consolidation.
- Focused source-level verification.
- Focused test coverage for release-readiness invariants.
- Package integrity verification.

Not allowed:

- Backend route, schema, auth, permission, owner-projection, billing, Stripe,
  Admin Portal capability, landing-page, service-worker, push-notification,
  native-mobile, offline-sync, AI-reply, scheduler, or workflow-engine changes.
- New HorseOps product behavior.
- Owner-visible expansion of any staff, alert, history, audit, or daily-check
  internals.

## Release-Readiness Matrix

The phase-by-phase matrix is captured in:

```text
outputs/horseops_1k_release_readiness_matrix.md
```

It covers HorseOps-1A through HorseOps-1J and records the launch boundary for
each phase.

## Privacy Boundaries Re-Checked

1K re-checks the following release boundaries:

- Owner-facing surfaces must not expose staff notes, raw daily-check payload
  internals, alert triggers, `source_check_id`, audit diffs, auth tokens,
  passwords, Stripe IDs, or private admin/staff-only fields.
- Platform Admin horse inspection remains summary-only.
- Product Care Ledger routes remain barn-scoped.
- Platform cross-facility inspection remains limited to the Admin Portal
  summary surface.
- Under-qualified staff denials preserve the locked zero-operational-artifact
  behavior.
- Owner service requests keep the locked request type and rate-limit model.
- Barn-wide visibility templates cannot expand owner-safe keys.
- HorseOps-1J mobile screenshot evidence remains present and valid.

## Verification

Focused verification:

```bash
python -m pytest backend/tests/test_horse_ledger_1k.py -q
python -m pytest backend/tests/test_horse_ledger_1h.py backend/tests/test_horse_ledger_1i.py backend/tests/test_horse_ledger_1j.py backend/tests/test_horse_ledger_1k.py -q
```

Local results:

- `backend/tests/test_horse_ledger_1k.py` — 5/5 passed.
- `backend/tests/test_horse_ledger_1h.py backend/tests/test_horse_ledger_1i.py backend/tests/test_horse_ledger_1j.py backend/tests/test_horse_ledger_1k.py` — 19/19 passed.

Broad live HorseOps regression was attempted with local Mongo environment
variables, but this Codex tool sandbox could not open direct Mongo connections
to `127.0.0.1:27017` (`Operation not permitted`). That is an environment
limitation for the live DB-backed tests; the 1K package itself is source,
docs, and evidence only.

The 1K test pins:

- phase matrix completeness for 1A through 1J,
- evidence-only scope language,
- owner/admin privacy boundary language,
- 1J screenshot existence, JPEG signatures, and 390x844 dimensions,
- source-level guards for owner-safe UI and summary-only Admin horse surfaces.

## Live Regression Follow-Up

Founder-run live regression surfaced two test-harness portability issues, both
fixed in this package:

- `backend/tests/test_horse_ledger_1a.py` no longer reads
  `/app/backend/routes/horse_ledger.py`; it resolves `horse_ledger.py` from the
  checked-out repository root.
- `backend/tests/test_horse_ledger_1f.py` now signs up with the public-safe
  `horse_owner` role and then promotes the test user to the intended
  `barn_manager` / `admin` role through test DB setup, matching the pattern used
  by the other HorseOps suites.
- Root `pytest.ini` adds a narrow warning filter for Starlette 0.37.2 importing
  python-multipart through its legacy `multipart` module name. This removes the
  non-actionable `PendingDeprecationWarning` from test output without changing
  runtime dependencies or product behavior.

## Package

Package path:

```text
outputs/phase_horseops_1k_changes.zip
```

Expected files:

- `PHASE_HORSEOPS_1K_README.md`
- `memory/PRD.md`
- `backend/tests/test_horse_ledger_1a.py`
- `backend/tests/test_horse_ledger_1f.py`
- `backend/tests/test_horse_ledger_1k.py`
- `outputs/horseops_1k_release_readiness_matrix.md`
- `pytest.ini`

## Deferred

No Phase 16 work starts in this phase. No mobile-native, push notification,
offline sync, AI reply, inventory purchasing, vendor ordering, breeding, or
new workflow work starts here.

## Lock Notes

HorseOps-1K is Codex-approved and locked. Full founder-run live HorseOps
regression passed after the 1A/1F test-harness fixes and the targeted
Starlette multipart warning filter:

```text
398 passed, 0 warnings
```

Next stage must start with a gated Phase 16 plan.
