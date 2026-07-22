# Mode B Attempt 02 Repository Custody Record

- remote repository: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- remote default branch: `integrate-emergent-final-zip`
- exact starting commit: `624d01af32fa3c04333be7ac2e65222d17d70a44`
- starting tree: `182db74b0aa16957f383ed7da2d1f3641b688db5`
- starting parent: `6565c87f2d2a1499ecd7f6efd83fbbbb67aeb29b`
- Attempt 02 branch: `codex/founder-review-phase1-pilot-a-mode-b-attempt-02-v1`
- source Founder attachment SHA-256: `3c969248a855052d33829cd0f6ceb90737f6d7960475f1d6f467336e35bb88c9`
- packet freeze: `2026-07-22T01:34:05Z`

The fresh clone fetched remote branches and tags, checked out exact commit `624d01af...`, established a clean branch before packet freeze, and created the authorized Attempt 02 branch. The remote branch did not exist before creation.

At formal packet freeze, the Git index had been offloaded by the host filesystem and was marked `hidden,compressed,dataless`. `git status --porcelain=v2` failed with exit 128 twice; `git diff` against the Attempt 01 path also failed because the index could not be mapped. Direct `shasum` of the logical 770,782-byte index yielded the empty-stream digest and `dd` returned `Operation timed out`, proving the bytes were unavailable locally. Attempt 01's committed `MODE_B_CHECKSUMS.sha256` still verified with exit 0.

Two post-failure `brctl download` diagnostics returned exit 0 but did not hydrate `.git/index`. They were not used to requalify the preflight. Any alternate index used solely to create the additive blocked-evidence commit is delivery tooling, not evidence that the original formal index/worktree control passed.

Attempt 01 and all predecessor paths are intended to remain byte-identical. The authorized scope is additive under this `attempt-02/` directory only.
