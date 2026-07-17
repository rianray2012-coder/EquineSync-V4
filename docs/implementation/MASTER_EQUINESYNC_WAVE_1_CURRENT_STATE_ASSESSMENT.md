# Master EquineSync Wave 1 Current-State Assessment

## Observed foundations

| Area | Repository evidence | Readiness implication |
| --- | --- | --- |
| Authentication routes | `backend/routes/auth.py` register/signup/login/refresh/logout/reset/verify flows | Existing runtime must be converged, not replaced casually |
| Passwords/tokens | bcrypt, JWT, refresh rotation/revocation, token-purpose helpers | Security review and invariant mapping required |
| Abuse controls | rate limiting and login-attempt lockout | Preserve and test before change |
| Tenant context | authoritative user lookup, `resolve_barn_id`, account context/memberships | Single-role/barn and membership coexistence need mapping |
| Roles/permissions | backend capability logic plus frontend mirrors/navigation maps | Drift and frontend-only assumptions require comparison tests |
| Platform admin | separate `platform_role` and section capabilities | Preserve separation from barn-scoped roles |
| Audit | auth/audit helpers and audit routes/services | Actor attribution contract must be verified end to end |
| Data/indexes | Mongo collections and startup index creation in lifespan | No schema/index change until explicit authorization |
| Seeds/scripts | multiple admin, demo, UAT and role-smoke seed scripts | Must remain non-production and excluded from migration truth |
| Environments | config and deployment references exist | Secret ownership, environment parity and observability remain incomplete |

## Key convergence questions

- Which user/account/actor identifier is canonical across all collections?
- How do `role`, `platform_role`, `role_status`, memberships, barn/facility context, and relationship grants interact?
- Which permission decisions are backend-enforced versus frontend presentation only?
- How are refresh sessions, logout-all, suspension, verification, and recovery invalidated and audited?
- Which startup indexes and seed paths represent production expectations versus local/test support?
- What historical account, actor, barn, and attribution data must survive any later convergence?

## Current conclusion

The repository is ready for a bounded readiness/hardening assessment, not runtime convergence or provider transition. No provider, schema, migration, authentication, permission, or production change is authorized.
