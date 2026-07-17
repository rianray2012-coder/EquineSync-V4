# W1-RF01 Recommended Next RF Charter

## W1-RF02 Identity Security Containment and Authority Hardening

### Proposed Scope

- separate enrollment-requested role from granted operational authority;
- centrally deny pending/rejected role status from privileged capability paths;
- consolidate current-user/JWT/password primitives behind one canonical implementation;
- make refresh-token rotation atomic with reuse detection;
- define access-token behavior after password, role, relationship, and suspension changes;
- add focused negative, concurrency, audit, and parity tests.

### Exclusions

No identity-provider selection, OAuth, MFA activation, broad account/actor schema, data migration, production data, deployment, or launch.

### Entry Gate

Founder approval of exact findings and file scope, test plan, rollback, authority matrix, and no-schema/no-migration boundary.

### Exit Evidence

No public role elevation; one auth authority; exactly-one refresh rotation; suspension/revocation continuity; no cross-tenant regression; complete audit correlation; package integrity.

