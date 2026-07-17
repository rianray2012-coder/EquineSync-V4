# Master EquineSync Wave 2 Risk Register

| ID | Severity | Risk | Control |
| --- | --- | --- | --- |
| W2-P1-01 | P1 | free-form horse mutation can bypass identity/history | governed patch allowlist and revision history |
| W2-P1-02 | P1 | fragmented operational writes lack common idempotency/audit | canonical write service |
| W2-P1-03 | P1 | legacy location/stall sources could become dual-writable | canonical-only writes; read adapter |
| W2-P1-04 | P1 | cross-facility references can leak or corrupt | scoped reference resolution and 404 |
| W2-P2-01 | P2 | infrastructure egress controls remain defense-in-depth | Platform Operations owner |
| W2-P2-02 | P2 | full offline client sync deferred | future mobile/offline RF |
| W2-P2-03 | P2 | RF31 transfer workflow remains unopened | preserve continuity only |

P0: `0`. P1 findings are isolated to the authorized Wave 2 implementation.
