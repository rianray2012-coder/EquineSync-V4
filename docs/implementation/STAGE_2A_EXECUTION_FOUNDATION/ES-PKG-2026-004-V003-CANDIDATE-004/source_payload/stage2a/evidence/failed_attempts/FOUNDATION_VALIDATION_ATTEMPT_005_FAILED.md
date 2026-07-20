# Foundation Validation Attempt 005 — Failed

- Detected: `2026-07-20T08:12:27Z`
- Implementation commit: `d182ce0854d45a8e691b75915c7c9e2670f93654`
- Result: `FAIL_CLOSED`
- Failed control: `DISPOSABLE_SOURCE_RECOVERY_CHECKOUT_TIMEOUT`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The first Candidate-004 lifecycle run exceeded the 120-second bound while checking out the implementation commit in a disposable shared clone. No lifecycle conclusion from this attempt is reusable or promoted.

Before the unrelated Git timeout, both controlled services were successfully bound to measured launch nonces, PID/PGID identity, parent PID, full command, executable, working path, and their exact controlled listeners. Emergency cleanup verified both process groups stopped, both ports cleared, and the owner-marked runtime was removed.

The recovery rehearsal is narrowed to direct immutable-object materialization and restoration of the single authorized fixture. It no longer checks out unrelated or cloud-backed repository paths.
