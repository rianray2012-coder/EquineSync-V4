# Foundation Validation Attempt 002 — Failed and Preserved

- Failure stage: `DISPOSABLE_SOURCE_RECOVERY_CLONE`
- Failure class: `LOCAL_HARNESS_RESOURCE_INEFFICIENCY`
- Results accepted: `false`
- Production access: `0`
- Provider attempts: `0`
- Live-data access: `0`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The run reached the disposable source-recovery rehearsal, where a
`--no-hardlinks` local clone began copying loose Git objects into the
cloud-backed runtime directory. The candidate results were discarded. Only
the owned validation group was interrupted; the orchestrator then verified and
stopped the exact owned API PID 10022 and MongoDB PID 10019. Ports 8019 and
27029 closed, PID controls were absent, and the owner-marked runtime directory
was purged.

The remediation changes only the local rehearsal transport: a bounded shared-
object, no-checkout clone is created under the system temporary directory and
removed afterward. A separate post-push fresh-clone control remains responsible
for independent-object repository reproducibility.
