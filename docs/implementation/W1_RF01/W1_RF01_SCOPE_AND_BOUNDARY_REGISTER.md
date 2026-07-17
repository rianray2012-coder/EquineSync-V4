# W1-RF01 Scope and Boundary Register

## In Scope

- `backend/routes/auth.py`, `backend/core/auth.py`, `backend/auth_security.py`
- auth tokens, login attempts, configuration, middleware, audit, tenancy, account context, memberships, invites, admin-user controls, seeds, and tests
- frontend auth context, API token handling, role/permission mirrors, enrollment and invite surfaces
- locked Identity, Relationship, Permission, Audit, Stewardship, External Architecture, and Platform Operations canon

## Read-Only Runtime Boundary

Runtime, schema, migration, deployment, environment, provider, credential, customer-data, and production artifacts may be inspected but not modified.

## Exclusions

No containment, refactor, provider research requiring vendor contact, data correction, account action, environment action, or release action is included.

