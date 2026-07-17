# Master EquineSync Wave 2 Final Findings Register

State: `WAVE_2_PHASE_12_FINDINGS_ADJUDICATED`

| ID | Severity | State | Owner / trigger | Lock effect |
| --- | --- | --- | --- | --- |
| `W2-P2-01-CI-EGRESS-DEFENSE-IN-DEPTH` | P2 | retained nonblocking | Platform Operations; before shared CI/provider testing | none |
| `W2-P2-02-FULL-NATIVE-OFFLINE` | P2 | retained nonblocking | Future mobile/offline RF; before offline launch claims | none |
| `W2-P2-03-HORSE-TRANSFER-WORKFLOW` | P2 | retained nonblocking | RF31; before transfer workflow activation | none |

P0: `0`. Open P1: `0`. Wave-2-blocking P1: `0`. Retained P2: `3`.

During verification, a nullable compound-index defect was fixed with partial string-only unique indexes. Two stale tests were aligned with current safety behavior: no automatic routine seeding and rejection of dangling lesson participants. Neither remains open.

`W2-P1-PRODUCTION-DEFAULT-OFF` was discovered during final review and closed before lock. Wave 2 router registration and index setup now share a production-hard-disabled gate, including when an enable-looking variable is present.
