# Mode B Attempt 03 Repository Custody Record

## Repository identity

- Remote: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- Remote default branch: `integrate-emergent-final-zip`
- Accepted predecessor branch: `codex/founder-review-phase1-pilot-a-mode-b-attempt-02-v1`
- Starting commit: `dc5dc547df84eca59c265c355f86331f80c2ee59`
- Attempt 03 branch: `codex/founder-review-phase1-pilot-a-mode-b-attempt-03-v1`
- Fresh checkout: `/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_execution.nosync/EquineSync-V4`

## Initial checkout custody

At `2026-07-22T02:09:45Z`, the detached exact predecessor and later the bounded branch had:

- 4,489 readable worktree files;
- zero compressed or dataless files;
- successful `git fsck`;
- empty staged, unstaged, and untracked sets;
- `.git/index` size 777,859 bytes, mode `-rw-r--r--`, flags `-`, inode 93971970;
- initial index SHA-256 `4295bcc8499d4760db0e24df8b0576425f0fd96bf4d3c8ec6ee790d91cc13707`.

## Pre-freeze custody rerun

At `2026-07-22T02:19:12Z`:

- `git status --porcelain=v2`: exit 0, empty;
- staged-index comparison: exit 0;
- unstaged-worktree comparison: exit 0;
- untracked-file inspection: zero paths;
- Attempt 01 checksum verification: exit 0;
- Attempt 02 checksum verification: exit 0;
- historical-tree comparison: exit 0;
- repository plus runtime dataless count: 0;
- repository plus runtime compressed count: 0;
- all runtime file reads: exit 0;
- `.git/index` size 777,859 bytes, mode `-rw-r--r--`, flags `-`, inode 93977202;
- pre-freeze index SHA-256 `b5573b70febddd7b054ff65ab01134cbe1d8d3077c6cf3f6921a75dd2f05425e`.

The differing raw index hashes reflect Git index rewrites during branch establishment; both measurements were readable and all staged/worktree/tree comparisons were clean and interpretable.

## Historical preservation

Attempt 01 and Attempt 02 were not modified. Their committed checksum-register file SHA-256 values were respectively `fca26e2439ab07758f78ca5115b21ff8f39d92983a4a217f840a0e7c73ee1786` and `8a7d170c96bc3db312ea129422df6f7ac775163949e871047b5e263d9ed86b14`.

Only the new `attempt-03/` evidence family is added by this branch.
