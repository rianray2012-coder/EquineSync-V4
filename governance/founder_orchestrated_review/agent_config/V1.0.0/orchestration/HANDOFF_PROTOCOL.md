# Controlled Agent Handoff Protocol

Every handoff is a registered evidence event.

## Required handoff fields

- Handoff ID
- Review-cycle ID
- Sender agent/run
- Recipient agent/role
- Package ID/version/hash
- Files and evidence IDs transferred
- Authorized purpose
- Included and excluded scope
- Questions requiring response
- Expected output files and schemas
- Prohibited actions
- Blind-review flag
- Date and time
- Custodian registration ID

## Rules

- No undocumented side-channel collaboration.
- Questions and answers that affect analysis become evidence.
- Material clarification may require a new package version or review restart.
- The recipient must acknowledge package identity before work.
- The Custodian preserves the handoff and output receipt.
