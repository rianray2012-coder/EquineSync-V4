# Event Transition Revalidation Evidence

Status: `CORRECTED`

Event signup and community-program signup service requests are guarded at creation and again before approval. The approval transition reloads the current horse/student subject, reloads current Guardian-link and workflow-consent authority rows, and passes the stored `guardian_guard_state_token` into the central guard before the status is changed to `approved`.

If Guardian authority or consent was revoked, expired, suspended, disputed, transferred, made stale, or the participant state changed after creation, approval is blocked with the disclosure-safe Guardian/Minor response.

Evidence:

- `GMS-T-032`: event signup without event consent denies.
- `GMS-T-034`: stale state after Guardian revocation is rejected.
- `GMS-T-048`: stale state after consent withdrawal is rejected.
- `GMS-T-051`: approval revalidation occurs before the status update and uses the stored token.
