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
10. After Founder approval, record the six approved decisions, reconcile bounded metadata, rerun validation, and integrate through protected pull-request workflow.
11. After initiation integration, create a repository-integration receipt using the self-reference-safe pattern.
12. Complete mandatory document sorting and classification before any candidate guide text is drafted.
13. Do not adopt, activate, implement, merge a substantive Wave 1 candidate package, or begin CGP-007 without separate authority.

## Self-Reference-Safe Receipt Plan

Use the CGP-004/CGP-005 pattern:

- primary package PR records candidate bytes and validation evidence;
- repository-integration receipt is added by a follow-up PR;
- metadata reconciliation is added by a final follow-up PR when needed;
- receipt fields that cannot self-reference their own final merge commit remain explicitly pending in-repo and are completed in the final handoff or later metadata PR.

## Remote Advancement Rule

If the remote default branch advances after this branch is created, inspect intervening commits before any rebase or restart. Do not rebase, merge, or restart if the conflict is material without refreshed authority.

The remote default branch advanced from `3eb6825091241709f255b8ccf296987fa9b20724` to `36fa3c81f24d19708b9ee80377cf774b3122f07f` before Founder-disposition reconciliation. The intervening commits were inspected and affect `governance/implementation/technical-audit/` paths only; PR `#24` remains confined to `governance/implementation/code-guides/`.
