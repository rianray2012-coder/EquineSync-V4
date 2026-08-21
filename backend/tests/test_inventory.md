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
| Explicit live tests | 1207 |
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
| Deselected live | 1207 |

Artifact-related tests were inventoried, not remediated. No failing tests were
deleted, weakened, blanket-skipped, or blanket-`xfail`ed.

## Reviewed Known-Failure Baseline

`ci_known_failure_baseline.json` records the reviewed GitHub Actions baseline
from commit `614768d0afe01591c4f044fe6840e5317e6cda56`.

| Result | Count |
| --- | ---: |
| Passed | 919 |
| Failed | 158 |
| Errored | 3 |
| Skipped | 0 |
| Selected | 1080 |
| Deselected live | 1207 |

The backend CI job is now a known-failure non-regression gate. It may pass with
the reviewed failures still present, but it fails on any new failing/erroring
node ID, collection decrease, non-live inventory decrease, live inventory
expansion without review, JUnit parsing failure, or malformed baseline.
