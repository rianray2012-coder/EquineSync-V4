# Validation Report

Validation was run after the corrective commit placed the exact approved ZIP in `HEAD`, because the hardened validators intentionally prove custody from `HEAD:<approved-zip-path>`.

## Results

| Gate | Result |
| --- | --- |
| Approved ZIP tracked by Git | `PASS` |
| `git cat-file -e HEAD:<approved-zip-path>` | `PASS` |
| ZIP Git-object SHA-256 | `56cec940bef67ca1a6932428398fdde7b3f7e78a9aee9f2b2f8e84b47ea49b95` `PASS` |
| ZIP Git-object byte length | `117450` `PASS` |
| Corrected accession validator | `PASS` |
| Corrected custody validator with accession dependency | `PASS` |
| Correction package validator | `PASS` |
| Focused positive and negative tests | `20 passed` |
| `py_compile` | `PASS` |
| `pyflakes` | `PASS` |
| `git diff --check` and cached diff check | `PASS` |
| Manifest and checksum consistency | `PASS` |
| Secret-like scan | `PASS`; only validator regex definitions matched the search pattern |
| Product-code/schema/dependency path review | `PASS`; no product, schema, migration, dependency, deployment, PR #69, or PR #70 path changed |

## Boundary Confirmation

```text
NO_STRIPE_API_CALL_OCCURRED
NO_STRIPE_SANDBOX_MUTATION_OCCURRED
NO_LIVE_STRIPE_ACCESS_OCCURRED
NO_STRIPE_SECRET_OR_OBJECT_USED
NO_PRODUCT_CODE_CHANGED
NO_SCHEMA_OR_MIGRATION_CHANGED
NO_DEPLOYMENT_AUTHORIZED
NO_STAGING_AUTHORIZED
NO_PILOT_AUTHORIZED
NO_PRODUCTION_USE_AUTHORIZED
NO_PUBLIC_LAUNCH_AUTHORIZED
PR_69_NOT_MODIFIED_OR_MERGED
PR_70_NOT_MODIFIED_OR_MERGED
CGP006_MAP_GAP_0005_REMAINS_OPEN
PROVIDER_ASSURANCE_MAY_RESUME_ONLY_FROM_PHASE_0_AFTER_REFRESHED_CUSTODY
```

Post-merge custody refresh remains required before the provider-assurance directive may resume from Phase 0.
