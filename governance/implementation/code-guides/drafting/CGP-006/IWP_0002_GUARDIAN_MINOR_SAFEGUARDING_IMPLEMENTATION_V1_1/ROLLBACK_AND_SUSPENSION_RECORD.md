# Rollback And Suspension Record

Status: `READY_PENDING_PROTECTED_MERGE`

Rollback boundary:
- Revert the implementation PR if protected merge has not occurred.
- If a partial rollback would leave any old route able to bypass the Guardian/Minor guard, suspend the affected workflow route until the central guard and sink wiring are restored.
- Do not downgrade relationship/consent evidence or silently grandfather missing legacy authority.
- Preserve the authenticated source package, directive, manifests, and evidence records as historical custody artifacts.

Suspension candidates if safe rollback is unavailable: lesson/training participation, messaging, waiver/document/media requests, payment/recurring payment actions, event signup, and guardian lifecycle participant mutation.

No deployment rollback was performed because no deployment was authorized or executed.
