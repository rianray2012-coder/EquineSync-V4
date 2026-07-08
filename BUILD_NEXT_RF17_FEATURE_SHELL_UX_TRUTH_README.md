# RF17 Feature-Shell Retirement and UX Truth Package

Date: 2026-07-07

Status: Codex-reviewed and locked.

## Scope

RF17 retires production-like feature shells from daily user experience where a
canonical workflow already exists. It uses the founder-approved truth-first
posture from July 7, 2026:

- daily role navigation should show only real supported workflows;
- readiness, setup, scaffold, placeholder, or proof surfaces may be moved,
  hidden, redirected, or truth-labeled;
- Inventory is canonical over Supply Inventory;
- Task Engine is canonical over Staff Tasks;
- canonical Owner Updates / Review Queue are canonical over feature-module
  owner media updates;
- Group Messaging remains local-log/readiness only until true delivery exists;
- Advanced Reports remains manifest/readiness until real Excel/PDF export
  exists.

## Included

- direct-route redirects from duplicate feature shells to canonical workflows;
- daily navigation cleanup for Owner Requests and Reports;
- proof code, report script, focused tests, generated report, and review
  package;
- truth-label checks for Group Messaging, Advanced Reports, Mobile Readiness,
  Integrations, and Forms & Signatures;
- founder-decision rows showing which RF17 decisions were explicitly accepted
  and which large external/migration items remain deferred.

## Not Included

- data deletion or destructive migration;
- provider calls or provider mutations;
- App Store or Google Play submission;
- native billing or Apple/Google in-app purchase compliance;
- true provider delivery/sync implementation;
- full offline/native background support;
- UAT account mutation;
- founder acceptance auto-marking outside the explicit RF17 posture accepted in
  this conversation.

## Evidence

- Proof core:
  `backend/core/rf17_feature_shell_ux_truth.py`
- Report script:
  `backend/scripts/build_rf17_feature_shell_ux_truth.py`
- Focused tests:
  `backend/tests/test_rf17_feature_shell_ux_truth.py`
- Review doc:
  `docs/RF17_FEATURE_SHELL_UX_TRUTH.md`
- Plan doc:
  `docs/RF17_FEATURE_SHELL_UX_TRUTH_PLAN.md`
- Generated report:
  `outputs/rf17_feature_shell_ux_truth_report.md`
- Review package:
  `outputs/build_next_rf17_feature_shell_ux_truth.zip`

## Review Commands

```bash
.venv/bin/python -m pytest backend/tests/test_rf17_feature_shell_ux_truth.py
npm --prefix frontend run build
.venv/bin/python backend/scripts/build_rf17_feature_shell_ux_truth.py --fail-on-blockers --zip-output outputs/build_next_rf17_feature_shell_ux_truth.zip
unzip -t outputs/build_next_rf17_feature_shell_ux_truth.zip
```

## Launch Claim Boundary

Current claims may say RF17 retired duplicate daily navigation and direct-route
feature shells where canonical workflows already exist.

Current claims must not say RF17 implemented provider delivery, native billing,
store submission, true Excel/PDF exports, destructive data migration, or full
offline/native support.
