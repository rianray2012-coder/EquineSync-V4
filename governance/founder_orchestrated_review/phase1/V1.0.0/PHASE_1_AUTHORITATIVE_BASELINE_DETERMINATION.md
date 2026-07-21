# Phase 1 Authoritative Baseline Determination

**Determination date:** 2026-07-21  
**Remote repository:** `https://github.com/rianray2012-coder/EquineSync-V4.git`  
**Remote default branch:** `integrate-emergent-final-zip` at `acb518ea5a160820e64681ff95a16b010fe1156c`  
**Selected predecessor:** `codex/founder-review-agent-runtime-requalification-v1` at `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`  
**Phase 1 starting commit:** `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`  
**Unresolved ambiguity:** None.

## Method

All remote branches and tags were fetched before branch creation. Candidate tips were compared by tree contents, exact required artifact paths, historical-evidence counts, ancestry, and changed-path scope. Commit date alone was not used. No branch was combined, cherry-picked, or synthesized.

Commit `57210494c1e82e60efd4c329ebf34fda236972d8` is the tip of `origin/agent/install-founder-review-agents-v1.0.0` and an ancestor of the nine `origin/codex/*` branches listed below. It is not the complete latest predecessor because it lacks the later 97-file runtime-requalification family and the four-file controlled non-agent fallback authorization.

## Candidate comparison

| Remote branch | Tip commit | Framework and 8 roles | Calibration / installation | Runtime remediation, failed canary, generic fallback | Latest runtime-limitation disposition | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `origin/integrate-emergent-final-zip` | `acb518ea5a160820e64681ff95a16b010fe1156c` | Missing | Missing | Missing | Missing | Not a candidate |
| `origin/agent/add-founder-review-agent-package-v1.0.0` | `0350730469a9960632270a480347f46c9a86ef56` | Archive and sidecar only; expanded role sources missing | Missing | Missing | Missing | Incomplete |
| `origin/agent/install-founder-review-agents-v1.0.0` | `57210494c1e82e60efd4c329ebf34fda236972d8` | Present: 69 configuration files and 8 role prompts | Present: 106 calibration files and 5 installation reports | Present: 620 runtime-remediation files; failed canary and generic fallback preserved | Earlier `REMEDIATION_REQUALIFICATION_FAILED_FIRST_CANARY`; later requalification family missing | Complete historical base but not latest authoritative predecessor |
| `origin/codex/founder-review-agent-runtime-requalification-v1` | `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3` | Present and byte-unchanged from `5721049` | Present and byte-unchanged | Present and byte-unchanged; adds 97 runtime-requalification files | Present: `FOUNDER_REVIEW_AGENTS_BLOCKED_BY_CONFIRMED_RUNTIME_PRODUCT_LIMITATION`; adds 4-file Founder-authorized temporary non-agent fallback | **Selected** |
| `origin/codex/identity-relationships-controlled-thread-review-v1` | `b8b46d80bebefca1ef42a10419479dd080126122` | Present | Present | Present | Present | Excluded: adds Identity and Relationships review work |
| `origin/codex/identity-relationships-bounded-remediation-v1` | `3b17840aae3b0693e006e9378606c1ca1c11286a` | Present | Present | Present | Present | Excluded: adds review and remediation work |
| `origin/codex/pia-portfolio-realignment-v1` | `b8f34aef390c5fec6f942a6253edf6acc9488c44` | Present | Present | Present | Present | Excluded: adds PIA portfolio work |
| `origin/codex/facility-tenant-organizational-structure-pia-v1` | `a5cf78295ad43cde7f73e383b3d5e98a11000382` | Present | Present | Present | Present | Excluded: adds Facility PIA work |
| `origin/codex/facility-pia-founder-decisions-v1` | `de7b0166a440673d023160ed7c3af214d49cd40f` | Present | Present | Present | Present | Excluded: adds Facility PIA and Founder-decision work |
| `origin/codex/facility-pia-founder-decisions-and-structured-review-v1` | `56b0a88722d983e05baec0d3b1ea5b7b88c24001` | Present | Present | Present | Present | Excluded: adds Facility PIA structured-review work |
| `origin/codex/facility-pia-valid-fresh-segregated-review-v1` | `1741ab394e4b23c5ec85a71483d90ea1d95b6863` | Present | Present | Present | Present | Excluded: adds Facility PIA fresh-review work |
| `origin/codex/facility-pia-r2-compliant-structured-review-v1` | `5e549056ee25fd1992846bbd6fedaba4329ab668` | Present | Present | Present | Present | Excluded: adds Facility PIA R2 review-cycle work |

The remaining remote branches (`codex/ci-egress-runner-verification-20260712`, `codex/stage2-f0001-execution-baseline`, and `codex/stage2a-execution-foundation-remediation`) do not contain the Founder-Orchestrated Review framework and are not candidates.

## Selection rationale

`75c56ac67b0de694436c093fc2dc5ff5dffe4ff3` is the latest commit whose changes remain exclusively within the Founder-Orchestrated Review evidence and authorization scope. Relative to `5721049`, it adds only:

- the complete runtime-requalification evidence family, including the confirmed selector limitation, failed attempts and retries, fresh-clone proof, and machine-readable final disposition; and
- the Founder authorization for a temporary, explicitly non-agent, procedurally segregated review fallback.

The sealed configuration, eight canonical prompts, calibration evidence, installation evidence, activation evidence, and prior runtime-remediation evidence are byte-unchanged between `5721049` and `75c56ac`. Every descendant branch adds a product-domain review, remediation, PIA, or portfolio workstream that is unrelated to establishing the general Phase 1 operating model.

The fresh clone was checked out at `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`; tracked files, index, and untracked-file checks were clean before creating `codex/founder-review-phase1-operating-model-v1` from that exact commit.
