# Build-Next-13P - Role Home Title Case Polish Plan

Status: GATED PLAN - AWAITING APPROVAL

BN13P follows locked BN13O. The screenshot evidence proved all role-home shells
load, and it surfaced one founder copy convention: role/profile landing page
titles and headings should use consistent Title Case across roles.

## Purpose

Make role-home surfaces feel intentionally finished by normalizing visible
titles/headings to Title Case and lightly tightening empty-state copy where the
current wording reads like implementation scaffolding.

This is a polish phase, not a workflow-expansion phase.

## Proposed Scope

### 1. Role Home Title Case

Normalize visible role-home page titles and major section headings in
`frontend/src/pages/RoleHome.jsx`.

Target examples:

- `Manager setup intent` -> `Manager Setup Intent`
- `Staff setup intent` -> `Staff Setup Intent`
- `Horse owner setup` -> `Horse Owner Setup`
- `Minor rider intake` -> `Minor Rider Intake`
- `Founder intake` -> `Founder Intake`
- `Trainer intake` -> `Trainer Intake`
- `Rider intake` -> `Rider Intake`

Title Case applies to:

- H1 page titles.
- Main intake panel headings.
- Major card headings.
- Sidebar/profile role display headings only where they are intended as titles.

Title Case does not apply to:

- Placeholder text inside form fields.
- Body copy paragraphs.
- Legal/privacy language.
- Route names, role codes, API names, data-test IDs, or enum values.

### 2. Empty-State Copy Tightening

Review empty-state helper text on role-home cards for founder-facing clarity.

Allowed edits:

- Replace "Coming soon" wording where it implies a shipped workflow exists.
- Keep language conservative: setup context only, no implied task creation,
  billing changes, care-record changes, membership changes, or document signing.
- Keep owner-facing privacy boundaries explicit.

Out of scope:

- New cards.
- New CTAs.
- New routes.
- New workflow promises.
- New data collection fields.

### 3. Evidence Refresh

Capture a small source/evidence packet that proves the copy convention is now
locked.

Required artifacts:

- `BUILD_NEXT_13P_ROLE_HOME_TITLE_CASE_POLISH_README.md`
- `outputs/build_next_13p_role_home_title_case_report.md`
- `backend/tests/test_build_next_13p_role_home_title_case.py`
- `outputs/build_next_13p_role_home_title_case_polish.zip`

Optional artifacts:

- Updated screenshots only if the user wants a visual proof pass. Source-level
  proof is enough for the first BN13P review unless founder asks for screenshots.

## Strict Guardrails

- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, UAT-account, Stripe, Apple, or DocuSign changes.
- No route changes.
- No role-routing changes.
- No seeded-demo or UAT-account mutation.
- No new workflows.
- No new owner-visible private data.
- No staff notes, raw alert payloads, audit diffs, Stripe IDs, DocuSign IDs,
  passwords, tokens, or secrets in artifacts.

## Proposed Tests

Add focused source-level tests that assert:

- RoleHome H1 strings use Title Case for all role surfaces.
- Main intake panel headings use Title Case.
- Role codes, API paths, and data-test IDs remain unchanged.
- Forbidden launch/workflow expansion strings are not introduced.
- BN13O evidence remains locked and untouched except for PRD carry-forward
  references if needed.

Recommended verification:

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_13p_role_home_title_case.py -q
GENERATE_SOURCEMAP=false npm run build
```

Optional regression:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13o_role_screenshot_pass.py \
  backend/tests/test_build_next_13p_role_home_title_case.py -q
```

## Acceptance Criteria

- All role-home page titles and major headings use consistent Title Case.
- No role-routing, auth, permission, backend, or workflow behavior changes.
- Frontend build compiles.
- Focused BN13P tests pass.
- Package integrity passes.
- BN13P remains explicitly separate from broad public launch approval.

## Founder Decisions To Confirm Before Implementation

1. Should BN13P include screenshots, or source-level proof only?
   Recommendation: source-level proof only unless visual sign-off is desired.

2. Should "Setup Intent" remain the phrase for unfinished role-home setup pages,
   or should it become "Setup" for simpler user-facing language?
   Recommendation: keep "Setup Intent" for now because it clearly avoids
   implying that operational workflows have launched.

3. Should BN13P include minor wording cleanup for "Coming soon" card copy?
   Recommendation: yes, but only where the replacement is more conservative.

4. Should role subtitles be Title Case too?
   Recommendation: no. Keep subtitles as sentence case for readability.
