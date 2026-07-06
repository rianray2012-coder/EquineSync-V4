# Build-Next-14A - Roadmap Alignment + Pre-Expansion Hardening

Status: Codex-reviewed and locked.

## Purpose

BN14A is an evidence and planning gate before the newly uploaded phased roadmap
is implemented. It compares the current EquineSync codebase against
`/Users/rianray/Downloads/equinesync_phased_plan_md 2/`, identifies what is
already built, what is a foundation or placeholder, and what must be hardened
before the next product phase begins.

BN14A does not add product behavior.

## Scope

Included:

- Roadmap-to-code alignment across uploaded phases 0 through 14.
- Current backend route, frontend page, Admin Portal, HorseOps, billing, and
  role-home inventory.
- Permission and role-routing status review.
- Placeholder / generic shell audit.
- Pre-expansion hardening findings.
- Recommended next phase sequence.
- Focused verification of current role-home and frontend build health.

Excluded:

- No new product workflows.
- No backend route, schema, auth, permission, billing, Stripe, Apple, DocuSign,
  HorseOps, Admin Portal, landing-page, service-worker, push, native-mobile,
  offline, AI, scheduler, or workflow-engine behavior changes.
- No seed/demo/UAT account mutation.
- No destructive cleanup of existing untracked or modified files.

## Evidence Files

- `outputs/build_next_14a_roadmap_alignment_report.md`
- `outputs/build_next_14a_phase_matrix.md`
- `outputs/build_next_14a_hardening_findings.md`
- `outputs/build_next_14a_recommended_sequence.md`
- `outputs/build_next_14a_roadmap_alignment_hardening.zip`

## Verification Snapshot

- Frontend production build: PASS.
- Focused source tests:
  - `test_build_next_13p_role_home_title_case.py`: PASS.
  - `test_build_next_13o_role_screenshot_pass.py`: PASS.
  - `test_admin_portal_route_lock_guard.py`: FAIL in relocated local checkout
    because the test still hardcodes `/app/...` for import path, package scan
    path, and `portal.py` read path. This is recorded as a BN14A hardening
    finding; product behavior was not changed in this phase.

## High-Level Verdict

EquineSync should not restart at the uploaded Phase 0. The app is well beyond
that baseline: Admin Portal, HorseOps, billing, DocuSign, role homes, UAT
evidence, and account-context work are already materially implemented.

However, EquineSync should also not jump straight into new feature expansion.
Several uploaded roadmap areas currently exist as generic backlog foundations,
setup-intent screens, or placeholder shells rather than fully governed product
workflows.

Recommended next gate: BN14B - Role UX + Hardening Cleanup, then BN15A -
Today's Pulse Data Contract.

## Lock Criteria

BN14A is locked. Codex accepted that:

- the uploaded roadmap has been mapped to current code;
- foundation-only vs built workflows are clearly separated;
- pre-expansion hardening findings are documented;
- next phase sequencing is explicit;
- no product behavior changed.

## Lock Note

Round-1 P2 wording cleanup was applied before lock: the Admin Portal route-lock
hardening note now states that the test hardcodes `/app/...` for import path,
package scan path, and `portal.py` read path.

Next gated phase: BN14B - Role UX + Hardening Cleanup.
