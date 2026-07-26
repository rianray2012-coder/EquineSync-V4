# CGP-006 Repository Lifecycle Plan

**Prompt ID:** `CGP-006`
**Execution ID:** `CGEXEC-20260726-0005`
**Branch:** `codex/code-guide-controlled-initiation-cgp-006-v1`
**Starting commit:** `3eb6825091241709f255b8ccf296987fa9b20724`

## Lifecycle Treatment

1. Start from refreshed remote default head `3eb6825091241709f255b8ccf296987fa9b20724`.
2. Create dedicated branch `codex/code-guide-controlled-initiation-cgp-006-v1`.
3. Prepare documentary initiation package only.
4. Run CGP-002 through CGP-005 validators and ledgers.
5. Run CGP-006 initiation validator.
6. Generate `CGP_006_PACKAGE_MANIFEST.json` and `CGP_006_CHECKSUMS.sha256`.
7. Produce bounded diff under `governance/implementation/code-guides/`.
8. Commit and push the candidate package if validation passes.
9. Open a pull request for Founder review if repository workflow allows.
10. Do not merge, adopt, activate, or begin CGP-007 without separate authority.

## Self-Reference-Safe Receipt Plan

If Founder later approves repository integration, use the CGP-004/CGP-005 pattern:

- primary package PR records candidate bytes and validation evidence;
- repository-integration receipt is added by a follow-up PR;
- metadata reconciliation is added by a final follow-up PR when needed;
- receipt fields that cannot self-reference their own final merge commit remain explicitly pending in-repo and are completed in the final handoff or later metadata PR.

## Remote Advancement Rule

If the remote default branch advances after this branch is created, inspect intervening commits before any rebase or restart. Do not rebase, merge, or restart if the conflict is material without refreshed authority.
