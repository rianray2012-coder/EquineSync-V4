# Directive Authority Record

## Authenticated Sources

Current refresh directive source: `/Users/rianray/.codex/attachments/f03767a3-4f43-4840-b072-74a29d2f1f59/pasted-text.txt`

- SHA-256: `1039daa658e68e026d8adbece43ee7be20874a5f012ba9acba9b1a7cbc705442`
- Byte length: `18229`

Prior merge directive source: `/Users/rianray/.codex/attachments/29edbb36-ce9c-4d31-8665-27e8869ba196/pasted-text.txt`

- SHA-256: `37ecbb31e15b7be7be6da3a0669ee614c3ffd53038416045f69e6736aea01799`
- Byte length: `17393`
- Source type: standalone pasted text
- ZIP package: not applicable for this authenticated prior source

## Authority Determination

`PR_64_66_MERGES_AND_PR_67_CORRECTION_AUTHENTICATED_AS_DIRECTIVE_AUTHORIZED`

## Located Authority Clauses

- Merge authority: prior directive lines 35-43 expressly authorized merging PR #64, PR #65, and PR #66, updating PR #67, implementing the two PR #67 corrections, rerunning validation, and returning PR #67 for Founder disposition.
- Ready-for-review transitions and protected-branch process: prior directive lines 130-139 authorized marking PR #64 ready if draft status prevented merge and merging through the protected pull-request process; lines 177-185 did the same for PR #65; lines 214-222 did the same for PR #66.
- Permitted branch updates: prior directive lines 161-169 authorized a non-substantive PR #65 base update; lines 208-220 applied the same restriction to PR #66; lines 307-321 authorized updating PR #67 onto the resulting protected branch state.
- PR #67 correction authority: prior directive lines 243-252 authorized modifying PR #67 only to incorporate the resulting protected branch state, install `backend/requirements-dev.txt`, add least-privilege permissions, resolve mechanical conflicts, rerun checks, and return the pull request for Founder disposition.
- PR #67 metadata/body authority: prior directive lines 313-321 required recording old and new PR #67 heads and rerunning checks; lines 369-377 allowed directly required evidence or metadata updates within the authorized PR #67 scope. The PR #67 body update was classified as a non-code metadata update recording corrected custody and validation evidence for Founder disposition.
- Post-merge custody/reporting requirements: prior directive lines 409-487 required reporting directive authentication, PR #64-#66 execution, PR #67 remediation, validation, and final repository state.
- Continuing non-authorizations: prior directive lines 379-391 prohibited unrelated refactoring, dependency changes, source cleanup, finding closure, activation records, IWP activation, deployment changes, unrelated workflow modernization, and modification of PR #64-#66 content after merge; lines 395-405 preserved PR #68 as documentary and unmerged; lines 542-552 retained no-merge, no-activation, no-implementation, and no-finding-closure boundaries; lines 563-569 prohibited direct protected-branch mutation and merging PR #67 or PR #68.

## Action Comparison

| Action | Authority result |
| --- | --- |
| Mark PR #64 ready and merge | AUTHORIZED |
| Mark PR #65 ready, base-update, and merge | AUTHORIZED |
| Mark PR #66 ready, base-update, and merge | AUTHORIZED |
| Update PR #67 onto protected head `9996e948ede39a968b8facd8afe15c2b1a345204` | AUTHORIZED |
| Correct PR #67 workflow install path and permissions | AUTHORIZED |
| Update PR #67 body with custody/validation metadata | AUTHORIZED_METADATA_UPDATE |
| Merge PR #67 | NOT_AUTHORIZED_AND_NOT_PERFORMED |
| Merge PR #68 | NOT_AUTHORIZED_AND_NOT_PERFORMED |

No authority mismatch was identified.
