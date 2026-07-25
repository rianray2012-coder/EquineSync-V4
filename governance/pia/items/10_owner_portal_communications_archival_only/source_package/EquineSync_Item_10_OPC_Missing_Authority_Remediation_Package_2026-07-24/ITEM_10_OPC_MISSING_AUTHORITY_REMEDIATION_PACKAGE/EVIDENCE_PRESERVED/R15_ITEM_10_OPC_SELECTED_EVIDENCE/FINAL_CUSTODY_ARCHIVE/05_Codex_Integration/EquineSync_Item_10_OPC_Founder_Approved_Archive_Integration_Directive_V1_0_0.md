# Codex Directive
## Item 10 Owner Portal and Communications Founder-Approved Archive Intake

## 1. Authority and task boundary

You are authorized to perform documentary-only custody validation, repository reconciliation, additive archive integration, and structured review intake for the supplied EquineSync Item 10 Owner Portal and Communications package.

This directive does **not** authorize application code, schemas, migrations, infrastructure changes, provider activation, external messaging, community activation, deployment, production use, pilot enrollment, first-user enrollment, or modification of locked governance artifacts.

Do not infer design approval or implementation authority from the phrase "Founder-approved archive." The Founder approval applies to archival custody, documentary governance, and structured repository review only.

## 2. Controlled package identity

- Official repository: `rianray2012-coder/EquineSync-V4`
- Portfolio position: Item 10
- PIA family: Owner Portal and Communications
- Current PIA ID: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.2.0`
- Historical predecessor: `ES-PIA-OWNER-PORTAL-COMMUNICATIONS-V0.1.0`
- Founder approval record: `ES-PIA-OPC-FAR-2026-07-23-01`
- Founder disposition: `FOUNDER_APPROVED_FOR_DOCUMENTARY_GOVERNANCE_ARCHIVAL_CUSTODY_AND_STRUCTURED_REPOSITORY_REVIEW_ONLY`
- Current PIA status: `ITEM_10_V0_2_MATERIALLY_STRENGTHENED_DOCUMENTARY_DRAFT_READY_FOR_STRUCTURED_REVIEW`
- Requested repository disposition: `ACCEPT_V0_2_AS_MATERIALLY_STRENGTHENED_DOCUMENTARY_DRAFT_FOR_STRUCTURED_REVIEW_ONLY`
- Authority effect beyond documentary intake: `NONE`

## 3. Mandatory fail-closed intake

Before branch creation, file copying, staging, commit, or push:

1. Verify the outer ZIP SHA-256 against the supplied `.zip.sha256` sidecar.
2. Run `unzip -t` and require success.
3. Extract into a new empty temporary directory outside the repository.
4. From the extracted package root, verify every entry in `06_Controls/PACKAGE_CHECKSUMS.sha256`.
5. Parse `06_Controls/PACKAGE_MANIFEST.json` and require agreement on:
   - Item 10;
   - V0.1 as historical predecessor;
   - V0.2 as current strengthened successor;
   - the Founder approval record ID;
   - documentary-only authority; and
   - every implementation, activation, production, and enrollment flag remaining false.
6. Confirm the four required source files are present and nonempty.
7. Confirm both DOCX files pass ZIP-container integrity checks.
8. Confirm the V0.1 and V0.2 Markdown headers identify the correct PIA IDs and versions.
9. Confirm the Founder approval record does not claim Founder design approval, implementation authority, operational readiness, community activation, or enrollment authority.
10. Confirm the package validation report states `PASS` and no unresolved package-integrity error.
11. Confirm the official remote resolves to `rianray2012-coder/EquineSync-V4`.
12. Confirm no unrelated Git write, active index lock, merge, rebase, cherry-pick, unresolved conflict, or dirty worktree is present.
13. Fetch remote refs without altering the working tree.
14. Determine the current canonical Remaining PIA Program baseline and Item 10 registry location from repository evidence. Do not assume that the default branch or a historical baseline is current.

Stop before mutation if any check fails. Report the exact failure and preserve all supplied evidence. Do not delete locks, terminate processes, reset branches, clean unrelated files, or improvise a reconciliation.

## 4. Source-byte preservation

1. Preserve every supplied source and control file byte-for-byte.
2. Do not resave DOCX files, normalize Markdown, change line endings, run formatters, regenerate documents, or alter metadata.
3. Preserve V0.1 as historical evidence. Do not overwrite, replace, or silently supersede it.
4. Store V0.2 as the current materially strengthened documentary successor, not as an implemented or design-approved baseline.
5. If repository convention requires path-safe copies, retain original filenames and hashes in the manifest and do not alter copied bytes.
6. If any repository hook changes controlled bytes, stop before commit and report.

## 5. Repository baseline and branch

1. Use a fresh clone or a demonstrably clean synchronized checkout.
2. Inspect current repository instructions, program manifests, neighboring PIA integrations, and Item 10 records.
3. Select the repository-evidenced canonical Remaining PIA Program baseline.
4. Record the immutable starting commit.
5. Create a new additive work branch only after all preflight checks pass.

Recommended branch name:

`codex/item-10-opc-founder-approved-archive-intake-v1`

If that branch exists, add a numeric suffix only after confirming the existing branch must be preserved. Never force-reset or reuse an existing branch.

Recommended commit message:

`docs(governance): archive Item 10 owner portal communications PIA lineage`

Do not create a pull request or merge unless separately directed by the Founder.

## 6. Canonical placement

Determine the exact destination from current repository evidence. Use the same item hierarchy and control-file pattern as the most recent accepted PIA archive.

The repository placement must preserve:

- V0.1 DOCX and Markdown as historical predecessor files;
- V0.2 DOCX and Markdown as the current strengthened documentary successor;
- the strengthening review report;
- Founder approval record and certificate;
- both the historical directive, when supplied, and this successor directive;
- the package manifest, checksum ledger, and validation report; and
- a repository integration receipt generated only after actual integration.

Do not invent a new top-level governance taxonomy when a canonical structure exists.

## 7. Structured review intake

After custody validation and placement, perform only the bounded documentary checks needed to confirm repository intake:

1. Item identity and version continuity.
2. Presence and order of the 43 required PIA sections.
3. Preservation of `OPC-FD-001` through `OPC-FD-024`.
4. Five-question vocabulary and answer consistency.
5. V0.1 historical preservation and V0.2 successor treatment.
6. Review-register continuity for `OPC-REV-001` through `OPC-REV-006`.
7. Disclosure of the retained open P1 row-level traceability finding.
8. Consistency of all false authority flags.
9. Checksum and manifest parity after repository copy.

Do not close retained findings without evidence. Do not create architecture, security, privacy, safeguarding, legal, operational, or independent-assurance claims merely from repository intake.

## 8. Commit and remote verification

If all intake and repository checks pass:

1. Stage only the intended additive documentary files.
2. Review the exact staged diff.
3. Recompute and compare controlled-file hashes against the package manifest.
4. Commit with the recommended message or an equally precise documentary message.
5. Push only the new branch.
6. Verify the remote branch resolves to the exact local commit.
7. Confirm the worktree and index are clean.
8. Do not create a tag, release, pull request, or merge unless separately authorized.

## 9. Required repository receipt

After successful push, create a repository receipt that records:

- official remote;
- resolved canonical baseline and starting commit;
- branch name;
- ending commit;
- remote-ref verification;
- exact package ZIP SHA-256;
- internal checksum result;
- manifest identity;
- copied repository paths;
- staged-diff summary;
- controlled-file hash parity;
- clean-worktree result;
- any retained findings; and
- confirmation that no implementation, activation, production, or enrollment authority was created.

If no repository mutation occurs, do not create a success receipt. Preserve the package's pending-receipt notice and provide a fail-closed report.

## 10. Completion disposition

The maximum authorized completion state is:

`ITEM_10_OPC_FOUNDER_APPROVED_ARCHIVE_INTEGRATED_FOR_STRUCTURED_DOCUMENTARY_REVIEW_ONLY`

This state does not approve the V0.2 design, close `OPC-REV-006`, authorize implementation, activate providers or community messaging, establish operational readiness, permit production use, or authorize any user enrollment.
