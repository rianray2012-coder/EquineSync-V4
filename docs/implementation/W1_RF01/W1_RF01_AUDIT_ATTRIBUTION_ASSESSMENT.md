# W1-RF01 Audit Attribution Assessment

The audit model records user ID, email, role, barn, request IP/user-agent, resource, outcome, status, action, and redacted metadata. Authentication success/failure, reset, verification, refresh, logout, invites, permission denials, and admin mutations have meaningful coverage.

Gaps:

- audit is fail-open and can be lost without blocking sensitive mutations;
- actor and account are conflated through `users.id`;
- membership, relationship, delegation, platform-authority source, and authority revision are not consistently recorded;
- not every direct role or object denial emits evidence;
- background/service actor identity is not universally standardized;
- event delivery health, sequence, retention, and reconciliation need operational evidence.

Target events must include account ID, actor ID, active context, membership/relationship IDs and revisions, authorization decision, request/correlation/causation IDs, before/after state, and policy version while minimizing sensitive data.

