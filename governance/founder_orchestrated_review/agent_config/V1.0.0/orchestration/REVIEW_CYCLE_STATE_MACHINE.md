# Review Cycle State Machine

## States

1. `AUTHORIZED`
2. `INTAKE_IN_PROGRESS`
3. `BASELINE_FROZEN`
4. `DRAFTING_IN_PROGRESS`
5. `CANDIDATE_FROZEN`
6. `REVIEW_IN_PROGRESS`
7. `VALIDATION_IN_PROGRESS`
8. `GOLDEN_PATH_SPECIFIED`
9. `EXECUTION_IN_PROGRESS`
10. `REMEDIATION_REQUIRED`
11. `REMEDIATION_IN_PROGRESS`
12. `VERIFICATION_IN_PROGRESS`
13. `COMPLETION_GATE_REVIEW`
14. `READY_FOR_FOUNDER_DISPOSITION`
15. `FOUNDER_DISPOSITIONED`
16. `CLOSED`
17. `BLOCKED`
18. `REOPENED`

## Required transitions

- Authorization creates `AUTHORIZED`.
- Evidence intake moves to `INTAKE_IN_PROGRESS`.
- Unique package identity and freeze move to `BASELINE_FROZEN`.
- Authorized drafting moves to `DRAFTING_IN_PROGRESS`.
- Custodian freeze moves to `CANDIDATE_FROZEN`.
- Review and challenge move to `REVIEW_IN_PROGRESS`.
- Machine work moves to `VALIDATION_IN_PROGRESS`.
- Approved specification moves to `GOLDEN_PATH_SPECIFIED`.
- Authorized execution moves to `EXECUTION_IN_PROGRESS`.
- Blocking findings move to `REMEDIATION_REQUIRED`.
- Authorized repair moves to `REMEDIATION_IN_PROGRESS`.
- Fresh review moves to `VERIFICATION_IN_PROGRESS`.
- All required outputs move to `COMPLETION_GATE_REVIEW`.
- Passing the completion gate moves to `READY_FOR_FOUNDER_DISPOSITION`.
- Express Founder decision moves to `FOUNDER_DISPOSITIONED`.
- Final custody package moves to `CLOSED`.
- Any missing critical prerequisite may move to `BLOCKED`.
- New evidence or invalidation may move a closed or dispositioned cycle to `REOPENED` only through Founder authorization.

No state transition implies adoption, lock, release, or production authority unless the Founder decision expressly states it.
