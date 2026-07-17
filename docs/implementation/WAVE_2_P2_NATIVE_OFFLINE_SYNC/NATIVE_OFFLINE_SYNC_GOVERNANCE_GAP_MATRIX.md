# Native Offline Sync Governance Gap Matrix

| ID | Gap/decision | Severity | Blocking now | Owner/future gate | Required disposition |
| --- | --- | --- | --- | --- | --- |
| NOS-P2-01 | Select and approve native encrypted database and browser adapter after a vendor-neutral spike | P2 | No | Future offline implementation RF / Engineering + Security | Evidence-backed selection; no provider authority implied |
| NOS-P2-02 | Approve offline permission-lease durations by capability and data class | P2 | No | Identity/Permission governance + Founder | Explicit durations and revocation policy before runtime |
| NOS-P2-03 | Approve local retention and purge periods; legal-hold/privacy interaction | P2 | No | Record Stewardship/Privacy + Founder | Retention schedule before storage implementation |
| NOS-P2-04 | Approve safety-critical domain policy for medication, feed, turnout, location, and incidents | P2 | No | Domain safety review + Founder | Qualified roles, staleness, escalation, conflict thresholds |
| NOS-P2-05 | Define supported browser/OS/device matrix and capability degradation | P2 | No | Product/Engineering future gate | Published compatibility contract before pilot |
| NOS-P2-06 | Define synchronization SLOs, queue/storage limits, battery/data budgets | P2 | No | Platform Operations future gate | Measured thresholds and alerts before production |
| NOS-P2-07 | Approve support diagnostics and queue-repair authority model | P2 | No | Support/Security/Audit future gate | Least-privilege tools and audit contract |
| NOS-P2-08 | Assign implementation RF sequence without opening Wave 3 implicitly | P2 | No | Implementation Atlas + Founder | Separate kickoff and runtime authority |

## Closed Findings

| ID | State | Closure evidence |
| --- | --- | --- |
| NOS-P1-01 | Closed | Founder-accepted bounded corrective archive |
| NOS-P1-02 | Closed | Founder-accepted bounded corrective archive |
| NOS-P1-03 | Closed | Founder-accepted bounded corrective archive |

The eight P2 items are planning decisions. They do not describe active defects in locked Wave 2, do not reopen it, and are nonblocking for readiness-package completion. Each becomes blocking before its named implementation or production gate.

