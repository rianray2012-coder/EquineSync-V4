# Founder Decision Package Source Register

Verification timestamp: `2026-07-26T19:24:59Z`

Source directory:

`/Users/rianray/Documents/Codex/2026-07-23/n/outputs/Technical_Audit_Founder_Decision_Packet_2026-07-26/`

## Source Artifacts

| File | Size Bytes | SHA-256 | Verification |
| --- | ---: | --- | --- |
| `TECHNICAL_AUDIT_FOUNDER_DECISION_PACKET.md` | 38909 | `4d97ca4a5f0fc426770f53010d433ae26ecee4a6f609ec1e72a51ceb2f9cfd44` | OK |
| `TECHNICAL_AUDIT_FOUNDER_DECISION_REGISTER.csv` | 3609 | `603e9a9985091a0d6cb619c63f96ab823932bca02604877a56b58df04fec49f9` | OK |
| `DECISION_TO_FINDING_CROSSWALK.csv` | 6565 | `ffdd6df7d0f21983fb2f7e1eaae677b427ebd8e1a07655b3411ced18cdd0636c` | OK |
| `PROPOSED_REMEDIATION_SEQUENCE.md` | 12587 | `130749b29988c4def1a69232688dc1fc673bed76ff27320761b4a3d4a83107c7` | OK |
| `PRODUCT_DECISION_PACKET_SOURCE_REGISTER.md` | 2394 | `146e7c1159939658f03b79db24262ec8cdeb56054e96fb24f7545a3e5bf4648b` | OK |
| `PRODUCT_DECISION_PACKET_VALIDATION_REPORT.md` | 4163 | `5b2020ecb7e7851b1fc975f181b46a021ceafd2d1b2d326ee0b63a989d816f86` | OK |
| `PRODUCT_DECISION_PACKET_SHA256SUMS.txt` | 640 | `7a6ba5f47b8ceac3cb1c10578fc924df2527e00fa30864f73557cf07c5d2724a` | OK |

## Repository Drift Context

Current remote integration head at package preparation:

`636b104a8766f08eb1e4b57d1bc840ef217187e9`

Protected production branch head:

`92e9ccae8695aa523181b4cfe60e554e6c5245bd`

Source packet recorded integration context:

`991d9ea816e5f1309431e7bb66640a3aa8805445`

Observed drift from `991d9ea816e5f1309431e7bb66640a3aa8805445` to `636b104a8766f08eb1e4b57d1bc840ef217187e9` was confined to `governance/implementation/code-guides/` documentary/code-guide files.

Observed drift from the original audit base `ff2748796bf858f49a3f85bad0578850e1deb846` to current integration also includes the six-file deployment-control documentary closure under `governance/implementation/deployment-control/2026-07-26-release-branch-separation/`.

These documentary governance and Code Guide changes were recorded as non-invalidating for the technical findings. No backend, frontend, CI, provider configuration, deployment configuration, environment, schema, migration, Stripe, payment, or test-baseline runtime drift was observed in this drift check.

## Source Limitations And Inferences

- The package records final Founder dispositions but does not classify all 161 retained test nodes; that is delegated to `ES-TA-PRF-008`.
- The non-invalidating drift determination is based on file-path scope inspection, not a fresh full technical audit.
- No fresh provider-setting drift audit was performed; this package did not invoke provider write actions.
