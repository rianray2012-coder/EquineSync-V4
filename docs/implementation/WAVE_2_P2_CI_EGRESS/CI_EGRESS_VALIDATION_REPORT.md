# CI Egress Validation Report

## Passed evidence

| Validation | Result |
| --- | --- |
| Workflow policy validator | pass; 1 workflow |
| No-egress/provider/Wave focused tests | 26 passed |
| Initial provider/no-egress tests | 11 passed |
| Wave 2/provider baseline subset | 21 passed |
| RF27/RF28/Passport unaffected subset | 52 passed; two historical RF28 readiness checks intentionally report descendant drift |
| Frontend permission/component tests | 4 suites, 16 tests passed |
| Workflow YAML parse | passed |
| Python compilation | passed |
| `git diff --check` | passed |
| TCP, DNS, UDP, subprocess blocking | passed |
| Loopback preservation | passed |
| Provider credential inheritance denial | passed |
| Deliberate workflow corruption | five cases failed closed |

The two RF28 readiness checks are immutable historical-package checks and correctly detect the later Wave 2 reviewed overlay. They are not product failures and do not affect this package.

## Environment boundary

The Linux `unshare --net` step was not executed locally because this host is macOS and has no Linux container runtime. It is included as a required GitHub Actions step. No provider credential, production endpoint, provider API, deployment, migration, or customer data was used.

