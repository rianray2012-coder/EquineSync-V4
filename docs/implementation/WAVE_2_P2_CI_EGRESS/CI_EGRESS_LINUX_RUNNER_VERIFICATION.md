# CI Egress Linux Runner Verification

**Finding:** `CI-EGRESS-P2-01-LINUX-RUNNER-FIRST-EXECUTION`  
**Disposition:** `CLOSED`  
**Environment:** GitHub-hosted Ubuntu runner  
**Verification branch:** `codex/ci-egress-runner-verification-20260712`  
**Successful commit:** `d93ed30b3650118016ca17fc24754b743ba97dcb`  
**Successful run:** [Provider isolation 29225375131](https://github.com/rianray2012-coder/EquineSync-V4/actions/runs/29225375131)  
**Completed:** 2026-07-13T05:04:29Z

## Successful Verification

The controlled Linux runner completed all required checks:

- CI egress policy validation passed.
- Process-wide no-egress provider-isolation tests passed.
- The isolated Linux network namespace had no default route.
- A direct non-loopback connection was denied.
- Loopback remained available for local test infrastructure.
- Provider-isolation tests passed inside the network namespace.
- The workflow rejected uncontrolled provider-test opt-in.
- Provider variables remained scrubbed and sandbox opt-in remained false.

No production credentials, production endpoint, provider activation, external
mutation, runtime activation, deployment, or public launch was authorized or
used.

## Attempt History

| Run | Commit | Result | Disposition |
| --- | --- | --- | --- |
| `29224438844` | `9da8ad0baeaea733944e34ba7fe5f1da94dc4c4f` | Harness failed because `pytest` was not on the `sudo` secure path; kernel outbound denial and loopback checks passed. | Preserved as non-security harness failure. |
| `29225308588` | `4ecdaa4ae0e9f367a8c88ba501f93f0127fea319` | Harness reached the namespace tests; DNS denial occurred before the unit-test connection guard. | Preserved as non-security deterministic-test correction. |
| `29225375131` | `d93ed30b3650118016ca17fc24754b743ba97dcb` | All workflow steps passed. | Qualifying closure evidence. |

The two failed attempts did not demonstrate an egress bypass. Both preserved
kernel-level outbound denial. The corrections retained the same deny-by-default
boundary: the active Python toolchain path is preserved inside the namespace,
and the unit probe uses the reserved TEST-NET-3 address `203.0.113.10` so it
does not depend on DNS.

## Governance Effect

`CI-EGRESS-P2-01-LINUX-RUNNER-FIRST-EXECUTION` is closed. Wave 0, Wave 1, and
Wave 2 remain locked; Wave 2 was not reopened. Production, public launch,
runtime activation, external-provider activation, and Wave 3 authority remain
false.

