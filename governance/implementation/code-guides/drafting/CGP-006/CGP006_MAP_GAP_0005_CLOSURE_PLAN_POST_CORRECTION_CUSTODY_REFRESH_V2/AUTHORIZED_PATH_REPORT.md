# Authorized Path Report

## Authorized Changed Paths

```text
governance/implementation/code-guides/PROGRAM_STATUS.md
governance/implementation/code-guides/receipts/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2_RECEIPT.md
governance/implementation/code-guides/drafting/CGP-006/CGP006_MAP_GAP_0005_CLOSURE_PLAN_POST_CORRECTION_CUSTODY_REFRESH_V2/
```

## Explicitly Excluded Paths And Activities

- Product code: `NO_PRODUCT_CODE_CHANGED`
- Schema and migrations: `NO_SCHEMA_OR_MIGRATION_CHANGED`
- Dependencies and lockfiles: no changes authorized
- Deployment, staging, pilot, production, and public launch: no changes authorized
- Provider-connected Stripe activity: `NO_STRIPE_API_CALL_OCCURRED`
- Stripe sandbox mutation: `NO_STRIPE_SANDBOX_MUTATION_OCCURRED`
- Live Stripe access: `NO_LIVE_STRIPE_ACCESS_OCCURRED`
- Stripe object or secret use: `NO_STRIPE_SECRET_OR_OBJECT_USED`
- PR #69: `PR_69_NOT_MODIFIED_OR_MERGED`
- PR #70: `PR_70_NOT_MODIFIED_OR_MERGED`

The refresh package and validator enforce that changed paths remain limited to the authorized governance refresh paths.
