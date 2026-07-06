# Build-Next-13P Role Home Title Case Polish Report

Status: CODEX-REVIEWED AND LOCKED

Generated: 2026-07-01

## Scope

BN13P applies the founder copy convention from the BN13O screenshot review:
role/profile landing page titles and major headings should use consistent Title
Case across role-home surfaces.

This report covers source-level proof only. No screenshots were required for
this pass.

## Summary

| Area | Result |
| --- | --- |
| Role-home H1 titles | PASS |
| Main intake panel headings | PASS |
| Conservative empty-state copy | PASS |
| Role routes and data-test IDs preserved | PASS |
| Backend behavior unchanged | PASS |
| BN13O lock preserved | PASS |

## Title Case Updates

| Surface | Before | After |
| --- | --- | --- |
| Staff | `Staff setup intent` | `Staff Setup Intent` |
| Staff intake panel | `Staff intake` | `Staff Intake` |
| Manager | `Manager setup intent` | `Manager Setup Intent` |
| Manager intake panel | `Manager intake` | `Manager Intake` |
| Trainer | `Trainer setup intent` | `Trainer Setup Intent` |
| Trainer intake panel | `Trainer intake` | `Trainer Intake` |
| Facility founder | `Facility setup intent` | `Facility Setup Intent` |
| Founder intake panel | `Founder intake` | `Founder Intake` |
| Owner | `Horse owner setup` | `Horse Owner Setup` |
| Owner intake panel | `Owner intake` | `Owner Intake` |
| Rider intake panel | `Rider intake` | `Rider Intake` |
| Guardian | `Minor rider intake` | `Minor Rider Intake` |
| Guardian intake panel | `Guardian intake` | `Guardian Intake` |

## Empty-State Copy Updates

The previous `Coming soon:` scaffold wording was replaced with conservative
copy that does not imply new workflows are active.

Examples:

- Owner Daily Care now says approved owner-visible care status will appear
  after the barn connects care visibility.
- Owner Requests stays tied to the existing approved workflow.
- Owner/Rider/Guardian document copy stays tied to approved document workflows.
- Rider and Guardian schedule copy waits for barn/program connection.
- Guardian requests explicitly remain separate from staff-only workflows.

## Preserved Contracts

The following source contracts remain unchanged:

- Role-home routes.
- API paths.
- Role switch branches.
- Data-test IDs.
- BN13O missing-intake fallback.
- BN13O locked screenshot evidence.

## Strictly Unchanged

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

## Required Verification

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

## Lock Status

BN13P is Codex-reviewed and locked.
