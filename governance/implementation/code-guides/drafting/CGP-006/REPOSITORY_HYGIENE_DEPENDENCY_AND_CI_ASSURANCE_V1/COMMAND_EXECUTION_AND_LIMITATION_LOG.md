# Command Execution And Limitation Log

| Command | Result | Evidence Class | Limitation |
|---|---|---|---|
| `shasum -a 256 <directive.md> <directive.zip>` | PASS; Markdown SHA `4959e039...`, ZIP SHA `9446f0a0...` | COMMAND_EXECUTION_EVIDENCE | Local attachment custody only. |
| `unzip -t <directive.zip>` | PASS | COMMAND_EXECUTION_EVIDENCE | No mutation. |
| `shasum -a 256 -c CHECKSUM_MANIFEST.sha256` inside directive package | PASS | COMMAND_EXECUTION_EVIDENCE | Package-local manifest only. |
| `git ls-remote ... integrate-emergent-final-zip` | PASS at `396f82c8a7600cae363142175d1d1448e9d2ece2` | COMMAND_EXECUTION_EVIDENCE | Live GitHub fact at review time. |
| `gh pr view 62` | PASS; merged at `185d37987c11eccabba4436619bdf11e91494711` | COMMAND_EXECUTION_EVIDENCE | PR body/check state read-only. |
| `gh pr view 63` | PASS; merged at `396f82c8a7600cae363142175d1d1448e9d2ece2` | COMMAND_EXECUTION_EVIDENCE | PR body/check state read-only. |
| PR #62 package validator at merge commit | PASS; 32 mandatory artifacts, 18 gaps, 16 findings, 10 Copilot rows | COMMAND_EXECUTION_EVIDENCE | Must run at PR #62 merge commit because later PR #63 custody files are intentionally outside that package path. |
| PR #63 custody validator at protected head | PASS; 18 gaps, 16 findings, 15 candidate IWPs, 0 authorized IWPs | COMMAND_EXECUTION_EVIDENCE | Current custody package only. |
| `npm ls ... --package-lock-only --json` | FAIL as evidence with `ELSPROBLEMS` for React 19 versus `react-day-picker` React 16/17/18 peer range | COMMAND_EXECUTION_EVIDENCE | Expected diagnostic failure; no install or lockfile mutation authorized. |
| `npm audit --package-lock-only --audit-level=moderate --json` | FAIL as evidence; metadata reports 42 advisories, 0 critical, 21 high, 9 moderate, 12 low | COMMAND_EXECUTION_EVIDENCE | Read-only npm registry audit; no fix performed. |
| `.github` inventory | PASS; `CODEOWNERS` and `workflows/ci.yml` only; Dependabot missing | STATIC_REPOSITORY_EVIDENCE | Repository settings were not modified. |
| tracked env-like file path check | PASS; no tracked `.env`, `.env.*`, `.env.example`, credential JSON, token JSON, or PEM paths found | STATIC_REPOSITORY_EVIDENCE | Does not prove historical absence of secrets. |
| broad source/config secret-pattern scans | STOPPED/BOUNDED | BLOCKED_BY_MISSING_TOOL_OR_ENVIRONMENT | Avoided noisy or slow scans and did not print secret candidates. No scanner was configured. |
| full local backend pytest | BLOCKED_MISSING_TOOL | BLOCKED_BY_MISSING_TOOL_OR_ENVIRONMENT | `pytest` not globally installed and package installation was not performed for this review. |

No real credentials, provider data, staging, production, external scanner service, repository app, deployment target, or secret value was used.
