# Authorized Pre-Freeze Diagnostic Probe

This was the one configuration probe authorized before packet freeze. It is diagnostic evidence only and is not a passing Attempt 02 preflight control.

| Probe | Result |
| --- | --- |
| known-answer checksum for exact `abc\n` bytes | PASS; `edeaaff3f1774ad2888673770c6d64097e391bc362d7d6fb34982ddf0efd18cb`; exit 0 |
| assigned-output write | PASS; exit 0 |
| assigned-input write | DENIED; exit 1 |
| sibling read | DENIED; exit 1 |
| hidden-oracle read | DENIED; exit 1 |
| unrelated read | DENIED; exit 1 |
| `/Users/rianray/.codex/auth.json` read | DENIED; exit 1 |
| direct network via `curl` | DENIED; exit 6 |

The probe used the non-`/tmp` layout and the exact least-privilege `shasum` dependency paths listed in the execution-environment specification.
