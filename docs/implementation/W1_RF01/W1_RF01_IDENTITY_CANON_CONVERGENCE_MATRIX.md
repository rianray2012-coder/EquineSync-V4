# W1-RF01 Identity Canon Convergence Matrix

| Canon requirement | Repository reality | Gap class | Future action |
| --- | --- | --- | --- |
| Account distinct from person/actor | `users` combines credential, profile, role, barn, billing fields | Data-model | Additive identifiers and projections |
| One durable actor identity | `users.id` is de facto actor; domain records duplicate people | Mapping/data | Preserve ID, link domain persons, quarantine ambiguity |
| Scoped multi-role membership | Single `users.role`; additive memberships exist | Authorization | Membership-aware active context |
| Authority provenance | Role/platform role fields often lack source/revision | Audit/security | Versioned grants and decision evidence |
| Relationship-aware access | Implemented unevenly by domain | Authorization | Shared evaluation plus field projection |
| Historical continuity | Audit/user IDs exist | Partial | Never rewrite attribution; supersede relationships |
| Revocation continuity | Suspension checked each request | Partial | Bind relationship/role revision and session invalidation |
| Guardian/minor continuity | Dedicated records/routes | Partial | Canonical relationship mapping and specialist review |
| Provider least privilege | Explicit grants in newer paths | Partial | Universal grant expiry/revocation contract |
| Platform/barn separation | Distinct `platform_role` and `role` | Aligned | Preserve and add provenance |

No locked-canon conflict requires changing canon. Runtime convergence remains separately gated.

