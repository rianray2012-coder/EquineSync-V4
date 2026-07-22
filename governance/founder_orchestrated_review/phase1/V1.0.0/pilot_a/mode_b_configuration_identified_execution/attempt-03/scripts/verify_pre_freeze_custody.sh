#!/bin/sh
set -eu

repo=/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_execution.nosync/EquineSync-V4
runtime=/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_03_runtime.nosync
attempt01=$repo/governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-01
attempt02=$repo/governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-02
attempt01_rel=governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-01
attempt02_rel=governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-02
expected_commit=dc5dc547df84eca59c265c355f86331f80c2ee59
expected_branch=codex/founder-review-phase1-pilot-a-mode-b-attempt-03-v1

/usr/bin/printf 'TIMESTAMP_UTC|'
/bin/date -u '+%Y-%m-%dT%H:%M:%SZ'
/usr/bin/printf 'REPO|%s\n' "$repo"
/usr/bin/printf 'RUNTIME|%s\n' "$runtime"

actual_commit=$(git -C "$repo" rev-parse HEAD)
actual_branch=$(git -C "$repo" symbolic-ref --short HEAD)
[ "$actual_commit" = "$expected_commit" ]
[ "$actual_branch" = "$expected_branch" ]
/usr/bin/printf 'COMMIT|PASS|%s\n' "$actual_commit"
/usr/bin/printf 'BRANCH|PASS|%s\n' "$actual_branch"

git -C "$repo" status --porcelain=v2
git -C "$repo" diff --cached --exit-code --quiet
git -C "$repo" diff --exit-code --quiet
[ -z "$(git -C "$repo" ls-files --others --exclude-standard)" ]
/usr/bin/printf 'GIT_STATUS|PASS\nSTAGED_INDEX|PASS\nUNSTAGED_WORKTREE|PASS\nUNTRACKED_FILES|PASS\n'

(cd "$attempt01" && /usr/bin/shasum -a 256 -c MODE_B_CHECKSUMS.sha256 >/dev/null)
(cd "$attempt02" && /usr/bin/shasum -a 256 -c MODE_B_CHECKSUMS.sha256 >/dev/null)
git -C "$repo" diff --exit-code --quiet "$expected_commit" -- "$attempt01_rel" "$attempt02_rel"
/usr/bin/printf 'ATTEMPT_01_CHECKSUMS|PASS\nATTEMPT_02_CHECKSUMS|PASS\nHISTORICAL_TREE_COMPARISON|PASS\n'

dataless_count=$(find "$repo" "$runtime" -flags +dataless -print 2>/dev/null | /usr/bin/wc -l | /usr/bin/tr -d ' ')
compressed_count=$(find "$repo" "$runtime" -flags +compressed -print 2>/dev/null | /usr/bin/wc -l | /usr/bin/tr -d ' ')
[ "$dataless_count" = 0 ]
[ "$compressed_count" = 0 ]
/usr/bin/printf 'DATALESS_COUNT|PASS|%s\n' "$dataless_count"
/usr/bin/printf 'COMPRESSED_COUNT|PASS|%s\n' "$compressed_count"

find "$runtime" -type f -exec /bin/cat {} \; >/dev/null
/usr/bin/printf 'ALL_RUNTIME_FILE_READS|PASS\n'
/bin/ls -ldO "$repo" "$repo/.git" "$repo/.git/index" "$runtime" "$runtime/role_inputs" "$runtime/role_outputs" "$runtime/evidence" "$runtime/hidden_oracle"
/usr/bin/stat -f 'GIT_INDEX|path=%N|size=%z|mode=%Sp|flags=%Sf|inode=%i' "$repo/.git/index"
/usr/bin/shasum -a 256 "$repo/.git/index"
/usr/bin/printf 'PREFREEZE_CUSTODY_RESULT|PASS\n'
