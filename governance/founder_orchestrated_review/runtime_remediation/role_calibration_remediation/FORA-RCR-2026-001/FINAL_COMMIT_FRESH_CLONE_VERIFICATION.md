# Final-Commit Fresh-Clone Verification

**Verification ID:** `FORA-FAR-2026-001-FINAL-CLONE-01`

**Verified at:** `2026-07-20T02:51:40Z`

**Result:** `PASS`

## Evidence chain

- Starting evidence baseline: `35119dbfb873e0fd19fef2a1e574d2f8100286f3`
- Remediation commit: `2d2efa9cc9aaaf14723283d94b716b5681c70df4`
- Earlier fresh-clone verification covered: `2d2efa9cc9aaaf14723283d94b716b5681c70df4`
- Final evidence commit: `860da19970604197117b94a2ef7f23dba2dca694`
- Final commit verified by this record: `860da19970604197117b94a2ef7f23dba2dca694`
- Remote branch tip at verification: `860da19970604197117b94a2ef7f23dba2dca694`

The earlier [fresh-clone verification](FRESH_CLONE_VERIFICATION.md) remains historically accurate. It verified the remediation commit before the two fresh-clone evidence files were added. This superseding record verifies the later evidence commit and does not rewrite the earlier result.

## Checksum-count reconciliation

| Commit | Manifest paths | Checksum entries | Failures | Scope |
|---|---:|---:|---:|---|
| `2d2efa9…` | 142 | 141 | 0 | Remediation, runs, reports, and tooling |
| `860da19…` | 144 | 143 | 0 | Same scope plus two fresh-clone evidence files |

The exact files responsible for the increase are:

- `FRESH_CLONE_VERIFICATION.json`
- `FRESH_CLONE_VERIFICATION.md`

No manifest path was removed. At both commits the checksum manifest intentionally omitted only itself, avoiding a self-referential checksum. Therefore, both `141/141` and `143/143` were correct for their respective commits.

## Final evidence verification

- Repository identity: `rianray2012-coder/EquineSync-V4` (`PASS`)
- Branch: `agent/install-founder-review-agents-v1.0.0` (`PASS`)
- Exact final commit: `860da19970604197117b94a2ef7f23dba2dca694` (`PASS`)
- Clean isolated clone: `PASS`
- Final checksum manifest: `143/143 PASS`
- ZIP SHA-256: `604d2c8eb0861120a16efe5f8d042a2bf8fe61c833822334ffb2ece5ef6695b3` (`PASS`)
- Role registration and custom instruction loading: `8/8 PASS`
- ES-RA-04 individual calibration: `15/15 PASS`; harness `10/10 PASS`
- ES-RA-06 individual calibration: `15/15 PASS`; harness `10/10 PASS`
- Bounded orchestration: `8/8 PASS`
- Behavioral aggregate: `120/120 PASS`; `8/8` roles
- Sandbox and denied/restricted network provenance: `8/8 PASS`
- Noninteractive approval evidence: parent and child `never`; no approval-requiring action attempted
- Preserved failed attempts: three behavioral and two bounded-orchestration attempts remain present
- Unauthorized child-created files: none
- Substantive review, production activity, and operational activation: none
- Founder activation approval: `false`
- Default branch: `integrate-emergent-final-zip`
- Final commit contained in default branch: `false`
- Pull requests for the branch: `0`
- Merge status: not merged

The explicit default-branch refspec was fetched before the ancestry check because the verification clone was single-branch.

## Protected-history result

No sealed configuration-package or calibration-suite path changed between the starting baseline and the final evidence commit. No prior runtime-remediation evidence outside the additive role-calibration subtree changed. No role file changed after the remediation commit, including ES-RA-08.

## Boundary

This verification establishes technical evidence integrity for the recorded installation scope. It is not Founder activation approval, external assurance, governance adoption, product readiness, production readiness, or authorization to commence substantive review work.
