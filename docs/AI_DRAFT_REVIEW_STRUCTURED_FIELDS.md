# AI Draft Review Structured Fields

## Scope

This slice strengthens the draft-only AI reviewer by making every supported source type ask for and normalize the same reviewer-facing fields:

- `review_summary`
- `confidence`
- `missing_information`
- `blocked_actions`

The source types remain invoices, service invoices, photo inventory, ride data, lesson schedules, training notes, voice-note transcripts, and health observations.

## Boundary

This work does not add official record saving, autonomous workflow actions, diagnosis, treatment recommendations, payment status changes, participant notifications, access-control changes, or live SMS/email sends. Review actions remain `approved_no_save` or `rejected`.

## Closure

Closure for this source slice requires source tests and a focused PR into `integrate-emergent-final-zip`. Deployment and live proof remain separately gated until Founder approval after the PR is reviewed.
