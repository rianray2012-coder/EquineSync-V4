# W1-RF02 Acceptance Criteria

- Pending/rejected applicants have no operational authority.
- Approval explicitly promotes requested role and is audited.
- All auth routes and product routes use one canonical password/JWT/current-user implementation.
- Exactly one concurrent refresh succeeds; reuse revokes the family and emits audit evidence.
- Selected membership context belongs to the account, is active, and never silently broadens access.
- Legacy history and identifiers remain intact.
- Full local integration harness and focused frontend/backend tests pass.
- Rollback, secret scan, diff hygiene, manifests, and archives pass.
- Production and public-launch authority remain false.

