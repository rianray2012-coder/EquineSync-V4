# PR #3 CI Test Inventory

Generated during PR #3 CI methodology hardening.

## Collection

| Metric | Count |
| --- | ---: |
| Before hardening | 2269 |
| After hardening | 2286 |
| New hardening tests | 17 |

## Live Selection

| Metric | Count |
| --- | ---: |
| Explicit live tests | 1206 |
| CI-runnable not-live tests | 1080 |
| Live-only modules | 43 |
| Mixed modules | 28 |
| Allowlist selectors | 768 |

## Auxiliary Inventory

| Marker | Count | Limitation |
| --- | ---: | --- |
| behavioral | 3 | Preliminary TestClient/client-fixture proxy only. |
| artifact | 19 | Preliminary `outputs/` source signal only. |
| sourcegrep | 98 | Preliminary `read_text()` source signal only. |

## Local CI-Runnable Result

This table records the local clean-clone measurement run after the branch was
synchronized with the current base. GitHub Actions run counts are recorded in
the PR body and in the uploaded Actions artifacts.

| Result | Count |
| --- | ---: |
| Passed | 920 |
| Failed | 157 |
| Errored | 3 |
| Skipped | 0 |
| Selected | 1080 |
| Deselected live | 1206 |

Artifact-related tests were inventoried, not remediated. No failing tests were
deleted, weakened, blanket-skipped, or blanket-`xfail`ed.
