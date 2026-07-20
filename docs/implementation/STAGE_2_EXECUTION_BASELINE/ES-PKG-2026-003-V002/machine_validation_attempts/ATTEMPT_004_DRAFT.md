# Draft Machine Validation Attempt 004

- UTC: `2026-07-20T03:45:00Z`
- Phase: `draft`
- Result: `FAIL`
- Score: `38/40`
- Expected failure 1: the prior 76-file review snapshot correctly detected the two post-review remediations.
- Expected failure 2: initial generic paired-format parity rules were too broad for a detailed JSON / summary Markdown evidence pair.

The failed attempt was preserved. The parity rule was narrowed to require exact identifier parity for true companion pairs and explicit aggregate parity for the detailed source-verification JSON and its controlled Markdown summary.
