# F-0002 Evidence Register

- Package: `ES-PKG-2026-003-V002`
- Finding: `ES-REV-2026-001-F-0002`
- Sealed predecessor: `ES-PKG-2026-002-V001` / `268fdd714264c5c0ae8f599a312c90e37ec44b908b438a1384c88f897bf03b9f`
- Repository baseline: `acb518ea5a160820e64681ff95a16b010fe1156c` / tree `a85a59e414016c7b0beb91f16ead1fb187c868d0`
- Controlled branch: `codex/stage2-f0001-execution-baseline`
- Execution: `EXECUTION_NOT_AUTHORIZED`
- Assurance: `NOT_EXTERNALLY_ASSURED`


| ID | Command/evidence | Result | Status |
|---|---|---|---|
| F2-E-001 | git remote get-url origin | https://github.com/rianray2012-coder/EquineSync-V4.git | PASS |
| F2-E-002 | git rev-parse HEAD; git rev-parse 'HEAD^{tree}' | acb518ea5a160820e64681ff95a16b010fe1156c; a85a59e414016c7b0beb91f16ead1fb187c868d0 | PASS |
| F2-E-003 | git symbolic-ref -q --short HEAD | codex/stage2-f0001-execution-baseline | PASS_ATTACHED_LOCAL_BRANCH |
| F2-E-004 | git fsck --full --strict --no-reflogs | exit 0; no output | PASS |
| F2-E-005 | git rev-list --objects acb518ea5a160820e64681ff95a16b010fe1156c \| git cat-file --batch-check | 5228 checked; 156 commits; 1287 trees; 3785 blobs; 0 missing | PASS |
| F2-E-006 | git ls-files -s; diff-files; diff-index --cached | 3340 stage0; 0 higher stage; exact clean before work | PASS |
| F2-E-007 | partial/sparse/promisor/alternates configuration audit | all absent | PASS |
| F2-E-008 | submodule/LFS pointer audit | none detected; git-lfs tool absent but not required | PASS_WITH_SCOPE_NOTE |
| F2-E-009 | git ls-remote --heads origin codex/es-ip-v1.1.0-remediation | 0 lines | PASS_BRANCH_ABSENT |
| F2-E-010 | git ls-remote --symref origin HEAD | integrate-emergent-final-zip -> acb518ea5a160820e64681ff95a16b010fe1156c at verification time | PASS_OBSERVATION_ONLY |
| F2-E-011 | git verify-tag equinesync-governance-v1.0-locked-2026-07-16 | exit 1: error: no signature found | PASS_ACCURATE_UNSIGNED_ANNOTATED_TAG_RECORD |
| F2-E-012 | sealed predecessor branch-not-found log | sha256 ff055c54c35be8e81d8c70a856f9fa1ff277dce4f92aae21392b120b7ee92f39 | PASS_IMMUTABLE_HISTORICAL_EVIDENCE |

All commands were read-only evidence checks. The source path shown by `--show-toplevel` is intentionally omitted from package content because local absolute paths are prohibited.
