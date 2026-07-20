# Foundation Validation Attempt 004 — Failed

- Detected: `2026-07-20T07:33:22Z`
- Implementation commit: `7c7581bc4541f365b66fdce841c64af3d27c81aa`
- Result: `FAIL_CLOSED`
- Failed control: `PROCESS_IDENTITY_MEASUREMENT`
- Execution: `EXECUTION_NOT_AUTHORIZED`

The first corrected-candidate lifecycle rerun failed because the controlled macOS sandbox denied the `ps` subprocess used for PID identity measurement. No lifecycle conclusion from the attempt is reusable or promoted.

Emergency cleanup confirmed no recorded process, removed the owner-marked runtime, and left both controlled ports clear. No repository-controlled artifact or frozen failed-candidate byte was changed.

The remediation replaces `ps` with sandbox-permitted `lsof` PPID/PGID measurement and macOS `KERN_PROCARGS2` full argument and executable measurement. The orchestrator continues to fail closed when any identity field is unavailable or conflicting.
