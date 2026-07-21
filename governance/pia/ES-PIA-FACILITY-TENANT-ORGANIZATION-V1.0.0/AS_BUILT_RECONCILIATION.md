# As-Built Reconciliation

## Current evidence

- `backend/core/account_memberships.py` projects current `users.barn_id` and `users.role` into compatibility membership rows. It explicitly says this is not the final multi-role model.
- `backend/routes/barns.py` provisions one barn and first admin together, uses `barn_id`, and documents one-barn/no-switching behavior as deferred.
- `W1_RF01_TENANT_AND_FACILITY_ISOLATION_REPORT.md` records a `primary` fallback, single legacy user barn, limited membership-aware context, missing universal server context binding, and unresolved `barn` versus `barns` references.

## Candidate-to-as-built gaps

The target design requires distinct Tenant, Facility, Organization, Relationship membership, and Permission concepts; explicit active context; multi-facility/multi-organization cardinalities; temporal lifecycle; public projections; legacy quarantine; and fail-closed online/offline/search/job behavior. Those requirements are not represented as implemented.

## Reconciliation rule

As-built behavior is evidence, never higher authority. No existing table, collection, route, UI label, or fallback is reclassified as canonical by this PIA. A later separately authorized plan must inventory all data, define deterministic mappings, quarantine ambiguity, prove access deltas, preserve rollback, and execute no customer or production mutation without explicit authority.

## Activity statement

No code, schema, database, migration, startup, route, UI, worker, provider, or production change occurred in Task B.
