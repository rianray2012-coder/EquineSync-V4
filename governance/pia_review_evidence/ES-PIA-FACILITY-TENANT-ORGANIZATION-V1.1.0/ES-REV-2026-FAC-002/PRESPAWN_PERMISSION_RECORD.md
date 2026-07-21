# Pre-Spawn Permission Record

- Review cycle: `ES-REV-2026-FAC-002`
- Intended agent run: `ES-RA-02-ES-REV-2026-FAC-002-RUN-01`
- Intended role: registered `ES-RA-02` Segregated Review Agent
- Founder authorization: `VALID_FRESH_SEGREGATED_REVIEW_DIRECTIVE`, SHA-256 `ce9de1ea05619ce3748742d9c0d034ba63555057e48906bf4857cce1f115b9d0`
- Recorded before reviewer creation: `YES`
- Timestamp: `2026-07-21T08:08:40Z`
- Parent surface: Codex desktop task, `/root` primary agent
- Starting repository commit: `de7b0166a440673d023160ed7c3af214d49cd40f`
- Candidate ZIP SHA-256: `9665172277ea50eb7a3f1c6e04ae3540211adcf8b9c471937180b4488931e5eb`
- Result: `FAIL`

## Required versus observed

| Control | Required | Observed before spawn | Result |
| --- | --- | --- | --- |
| Registered reviewer identity | ES-RA-02 loaded and provable | Repository configuration exists; active registered identity cannot be loaded or proven by this runtime | FAIL |
| Sandbox | Read-only | `danger-full-access` / unrestricted filesystem | FAIL |
| Approval mode | `on-request` | `never` | FAIL |
| Unrestricted override | Absent | Present | FAIL |
| Network | Disabled unless expressly allowed | Parent network capability enabled | FAIL |
| Shell/connectors/MCP/plugins | Disabled unless allowed | Tool capabilities remain available at parent; reviewer-scoped disablement cannot be proven | FAIL |
| Frozen candidate mutation | Technically impossible | Procedurally prohibited, but parent filesystem is writable | FAIL |
| Drafting worktree | Not used by reviewer | No reviewer created; intended clean checkout not created | NOT REACHED |
| Clean isolated input | Required | Input packages verified by parent; reviewer environment not created | NOT REACHED |
| Environment sanitization | Proven before process creation | Cannot be established for an uncreated registered reviewer under this runtime | FAIL |

## Stop decision

The effective environment cannot satisfy the mandatory read-only/on-request configuration. No reviewer process, subagent, custom agent, or substitute review session was created. No substantive review began.

`FACILITY_PIA_FRESH_SEGREGATED_REVIEW_BLOCKED_MANDATORY_PERMISSION_CONTROL_NOT_SATISFIED`
