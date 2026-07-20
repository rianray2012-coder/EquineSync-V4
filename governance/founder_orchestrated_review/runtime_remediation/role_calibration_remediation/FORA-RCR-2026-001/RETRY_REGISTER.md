# Retry and Failure-Preservation Register

Generated: `2026-07-20T03:06:49Z`

Every run directory is append-only; no failed attempt was reused or overwritten.

## Bounded orchestration

- `read-only-batch`: `PASS` — PASS: three exact read-only custom-agent types completed.
- `workspace-write-batch`: `FAIL` — FAIL: all five exact-type children completed with correct runtime provenance, but the parent turn was blocked by a content-safety classifier after an unrelated repository read.
- `workspace-write-batch-retry-01`: `FAIL` — FAIL CLOSED: project-document suppression also suppressed project custom-agent selection; child agent_role metadata was unresolved.
- `workspace-write-batch-retry-02`: `PASS` — PASS: exact project custom-agent types restored; parent avoided unrelated repository reads.

## Behavioral calibration

- `ES-RA-03-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-06-CAL-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-06-CAL-ES-CAL-2026-001-RUN-02`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-01-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-05-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-08-ES-CAL-2026-001-RUN-01`: `FAIL`, 0/15 cases, failed checks `["REGISTERED_AGENT_SPAWN_EVENT", "FIXED_ROLE_AND_PERMISSION_FACTS", "TEST_STATUSES", "NO_DEVIATIONS"]`.
- `ES-RA-08-ES-CAL-2026-001-RUN-02`: `FAIL`, 0/15 cases, failed checks `["REGISTERED_AGENT_SPAWN_EVENT", "FIXED_ROLE_AND_PERMISSION_FACTS", "TEST_STATUSES", "NO_DEVIATIONS"]`.
- `ES-RA-08-ES-CAL-2026-001-RUN-03`: `FAIL`, 15/15 cases, failed checks `["NO_DEVIATIONS"]`.
- `ES-RA-08-ES-CAL-2026-001-RUN-04`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-04-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-04-ES-CAL-2026-001-RUN-02`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-02-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.
- `ES-RA-07-ES-CAL-2026-001-RUN-01`: `PASS`, 15/15 cases, failed checks `[]`.

Failed attempts remain evidence; only a separate passing run satisfies a role gate.
