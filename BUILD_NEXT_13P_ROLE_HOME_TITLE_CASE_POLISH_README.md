# Build-Next-13P - Role Home Title Case Polish

Status: CODEX-REVIEWED AND LOCKED

BN13P follows locked BN13O and applies the founder copy convention that
role/profile landing page titles and headings should use consistent Title Case.

This is a narrow frontend copy-polish phase with source-level proof only.

## What Changed

- Normalized major role-home titles and intake panel headings in
  `frontend/src/pages/RoleHome.jsx`.
- Kept "Setup Intent" as the label for unfinished setup-intent surfaces.
- Kept subtitles and body copy in sentence case for readability.
- Replaced "Coming soon:" scaffold wording with conservative, workflow-safe
  empty-state copy.
- Preserved the BN13O missing-intake fallback.

Examples:

- `Staff setup intent` -> `Staff Setup Intent`
- `Manager setup intent` -> `Manager Setup Intent`
- `Trainer setup intent` -> `Trainer Setup Intent`
- `Facility setup intent` -> `Facility Setup Intent`
- `Horse owner setup` -> `Horse Owner Setup`
- `Minor rider intake` -> `Minor Rider Intake`
- `Founder intake` -> `Founder Intake`
- `Rider intake` -> `Rider Intake`

## What Did Not Change

- No backend route, schema, auth, permission, privacy, billing, provider,
  HorseOps, Admin Portal, task, facility setup, email, notification, landing
  page, UAT-account, Stripe, Apple, or DocuSign changes.
- No role-routing changes.
- No route changes.
- No seeded-demo or UAT-account mutation.
- No new workflows.
- No new CTAs.
- No new fields.
- No owner-visible private data changes.
- No screenshots were required for this pass; source-level proof only.
- Broad public launch is not approved by BN13P.

## Artifacts

- `BUILD_NEXT_13P_ROLE_HOME_TITLE_CASE_POLISH_README.md`
- `BUILD_NEXT_13P_ROLE_HOME_TITLE_CASE_POLISH_PLAN.md`
- `outputs/build_next_13p_role_home_title_case_report.md`
- `backend/tests/test_build_next_13p_role_home_title_case.py`
- `outputs/build_next_13p_role_home_title_case_polish.zip`

## Verification

Focused:

```bash
./.venv/bin/python -m pytest backend/tests/test_build_next_13p_role_home_title_case.py -q
```

Regression with locked BN13O:

```bash
./.venv/bin/python -m pytest \
  backend/tests/test_build_next_13o_role_screenshot_pass.py \
  backend/tests/test_build_next_13p_role_home_title_case.py -q
```

Frontend:

```bash
GENERATE_SOURCEMAP=false npm run build
```

Package:

```bash
python - <<'PY'
from pathlib import Path
from zipfile import ZipFile
p = Path("outputs/build_next_13p_role_home_title_case_polish.zip")
with ZipFile(p) as z:
    assert z.testzip() is None
PY
```

## Lock Notes

BN13P is Codex-reviewed and locked. It remains a frontend copy and
source-proof package, not a launch approval or workflow expansion.
