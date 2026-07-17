# W1-RF01 Authorization Test Matrix

Every protected resource needs permitted, unrelated, cross-barn, wrong-facility, pending-review, suspended, revoked-relationship, stale-context, guardian, minor, provider, barn-role, and platform-role cases.

Required invariants:

- frontend hiding never substitutes for backend denial;
- unknown capabilities deny;
- platform role does not derive from barn role;
- requested enrollment role does not equal granted authority;
- selected context must be an active authorized membership;
- membership existence alone does not grant sensitive fields;
- provider access requires explicit current grant;
- guardian access requires verified relationship and scope;
- cross-barn objects return generic non-existence where appropriate;
- permission and field projection use current policy/relationship revisions;
- every material denial and privileged action has audit correlation.

