# Cross-PR Interaction And Sequence Analysis

## File Overlap

- PR #65 and PR #66 overlap: none.
- PR #65 and PR #67 overlap: none.
- PR #66 and PR #67 overlap: `.github/workflows/ci.yml`.

## Interaction Findings

1. PR #64 is documentary only and should remain separate from remediation PRs.
2. PR #65 is documentation/metadata only. It can merge before PR #66 because its `backend/requirements-dev.txt` instruction is explicitly conditional on the file being present.
3. PR #66 changes backend dependency locations and backend CI installs.
4. PR #67 adds backend static tooling reports that currently install `backend/requirements.txt`. After PR #66, those tools are no longer in runtime requirements. This requires a correction or rebase before PR #67 Founder disposition.
5. PR #67 also needs explicit workflow permissions for least-privilege evidence.

## Advisory Sequence

1. PR #64 - documentary package.
2. PR #65 - documentation and metadata.
3. PR #66 - backend runtime/dev dependency split.
4. PR #67 - CI assurance reporting and Dependabot, only after the two enumerated corrections are made and checks rerun.

## Post-Merge Verification Requirements

- After any merge, re-check protected head and changed-file scope.
- After PR #66, verify backend CI installs from `backend/requirements-dev.txt` and runtime install from `backend/requirements.txt` remains coherent.
- Before PR #67 merge consideration, verify the assurance job installs the post-split dev manifest and has explicit least-privilege permissions.
- After PR #67, verify the assurance report remains nonblocking and does not print secret values.
