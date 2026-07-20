# Foundation Validation Attempt 003 — Failed and Preserved

- Failure stage: `DISPOSABLE_SOURCE_RECOVERY_CHECKOUT`
- Failure class: `BOUNDED_TIMEOUT_TOO_SHORT`
- Results accepted: `false`
- Production access: `0`
- Provider attempts: `0`
- Live-data access: `0`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The system-temporary shared-object clone succeeded, but a full-worktree checkout
exceeded the bounded 30-second timeout. The candidate results were discarded.
The existing owned PID records were used to stop only API group 11220 and
MongoDB group 11215. Both controlled ports closed and the owner-marked runtime
directory was purged.

The correction uses a sparse checkout containing only the fixture path under
test, retains bounded 120-second checkout and restore timeouts, and adds an
emergency-cleanup guard to the validator so unexpected failures invoke verified
orchestrator shutdown and runtime purge before propagating the error.
