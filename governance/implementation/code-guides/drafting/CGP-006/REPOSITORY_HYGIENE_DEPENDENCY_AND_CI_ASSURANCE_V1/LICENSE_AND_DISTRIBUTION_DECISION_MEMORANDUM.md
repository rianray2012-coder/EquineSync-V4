# License And Distribution Decision Memorandum

## Current State

No repository-root `LICENSE`, `LICENSE.*`, `COPYING`, or `COPYING.*` file exists at reviewed commit `396f82c8a7600cae363142175d1d1448e9d2ece2`.

## Decision Space

- Private/no-license posture: preserves default copyright and avoids granting reuse rights, but should be documented so contributors and reviewers do not infer open-source permission.
- Express proprietary notice: can clarify no external reuse without granting an open-source license.
- MIT: permissive grant with warranty disclaimer; requires Founder/legal approval.
- Apache-2.0: permissive grant with patent terms; requires Founder/legal approval.
- GPL-family: copyleft obligations may be incompatible with intended commercial/private distribution; requires Founder/legal approval.
- Contributor treatment: any external contribution model needs explicit terms before accepting third-party code.
- Third-party dependencies: dependency licenses should be reviewed separately before any public distribution claim.
- Public/private/future-distribution scenarios: repository visibility and product commercialization goals should drive the policy.

## Boundary

```text
LICENSE_SELECTION_AND_OPEN_SOURCE_GRANT_NOT_AUTHORIZED
NO_OPEN_SOURCE_LICENSE_GRANT_AUTHORIZED
NO_LICENSE_FILE_ADDED
```
