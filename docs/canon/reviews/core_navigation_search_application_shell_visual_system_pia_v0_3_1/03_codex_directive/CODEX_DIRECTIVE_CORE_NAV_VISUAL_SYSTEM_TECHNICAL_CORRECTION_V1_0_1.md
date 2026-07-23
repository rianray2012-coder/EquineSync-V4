# Founder Technical-Correction Directive to Codex
## Integrate the Founder-Approved Core Navigation Visual-System PIA Package

**Directive ID:** `ES-CODEX-DIR-NAV-VISUAL-V1.0.1`  
**Supersedes:** `ES-CODEX-DIR-NAV-VISUAL-V1.0.0`  
**Date:** July 22, 2026  
**Founder authority:** Rian Ray  
**Execution class:** Controlled documentary repository integration only  
**Correction class:** Non-substantive package-integrity correction  
**Implementation authority:** `FALSE`  
**Deployment authority:** `FALSE`  
**Production authority:** `FALSE`  
**Enrollment authority:** `FALSE`

## 1. Objective

Integrate the Founder-approved EquineSync Core Navigation, Search, and Application Shell visual-system PIA V0.3.1 using the technically corrected V0.3.2 package wrapper. Record Founder approval, preserve the complete review and fail-closed evidence chain, verify all bytes and identifiers under the non-circular integrity model, and produce an auditable repository receipt.

Do not implement the application shell, fonts, icons, favicons, themes, mascot, search behavior, feature flags, source code, schema, deployment configuration, production assets, or enrollment.

## 2. Controlling Founder Disposition

`FOUNDER_APPROVED_V0_3_DOCUMENTARY_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`

The approved PIA answers remain:

- Engineering buildability: `YES_WITH_EVIDENCE`
- Objective QA verification: `YES_WITH_EVIDENCE`
- Governance and MIAP traceability: `YES_WITH_EVIDENCE`
- Operational safety and recovery: `NO`
- First-user enrollment readiness: `NO`

Do not convert Questions 4 or 5 to a positive answer. Do not describe the capability as operationally ready, production ready, deployment ready, pilot ready, or enrollment ready.

## 3. Technical-Correction Authority

The V0.3.2 wrapper corrects only the prior package's integrity-control structure. It does not change the approved PIA V0.3.1 or its Founder disposition.

The prior fail-closed stop was correct. Preserve its receipt. Do not treat the prior stop as a defect in Codex execution.

## 4. Repository and Baseline Rules

1. Locate the official repository and verify the remote before writing. The expected official repository is `rianray2012-coder/EquineSync-V4`; verify rather than assume.
2. Identify the current canonical documentary integration baseline using repository evidence.
3. Record the starting branch, starting commit, remote URL, default branch, worktree status, and index status.
4. Do not modify an existing preserved branch or historical package.
5. Create a new bounded branch. Preferred name: `codex/core-navigation-visual-system-pia-founder-approved-v1`.
6. Follow a controlling repository naming convention if one exists and report the exact branch used.
7. Do not merge, create a pull request, retag, or modify protected branches without separate Founder authorization.

## 5. Package Intake and Non-Circular Integrity Verification

1. Copy the supplied V0.3.2 archive to an isolated staging directory outside the repository.
2. Verify the outer archive SHA-256 against the supplied sidecar checksum file.
3. Extract once into a new empty directory.
4. Read `07_integrity/INTEGRITY_MODEL.md` before running internal validation.
5. Count all extracted regular files.
6. Verify that `07_integrity/PACKAGE_MANIFEST.csv` has exactly one data row for every extracted regular file, including itself and `07_integrity/CHECKSUMS.sha256`.
7. Verify that the path set in the manifest exactly equals the extracted regular-file path set.
8. Verify that `07_integrity/CHECKSUMS.sha256` contains exactly `actual file count - 2` entries.
9. Verify that the only files excluded from the checksum ledger are:
   - `07_integrity/CHECKSUMS.sha256`
   - `07_integrity/PACKAGE_MANIFEST.csv`
10. Run SHA-256 verification for every ledger-listed file.
11. Compute the actual SHA-256 of `07_integrity/CHECKSUMS.sha256` and verify that it matches the manifest row for that file.
12. Verify that the manifest row for `07_integrity/PACKAGE_MANIFEST.csv` uses `SELF_REFERENCE_EXCLUDED` and `OUTER_ARCHIVE_SHA256` as its verification authority.
13. Verify all manifest byte counts for files with numeric byte values.
14. Treat PNG files as immutable binary evidence. Do not recompress, optimize, recolor, resize, strip metadata, or normalize them.
15. Preserve UTF-8 and LF for controlled text files.
16. If any outer hash, internal hash, count, path, size, required-file, or integrity-treatment check fails, stop fail-closed before repository mutation.

This V1.0.1 integrity rule intentionally replaces the impossible V1.0.0 requirement that both integrity-control files hash each other and themselves.

## 6. Canonical Repository Placement

First inspect the existing repository PIA and governance layout. Use the established canonical location and naming pattern if one exists.

If no controlling placement exists, use:

`governance/pia/core_navigation_search_application_shell/visual_system/V0.3.1/`

The integrated package shall include, at minimum:

- Founder-approved V0.3.1 PIA section;
- Founder approval record;
- Founder decision register;
- Founder typography memorandum;
- technical correction record;
- active V1.0.1 Codex directive;
- superseded V1.0.0 directive as historical evidence;
- fail-closed stop receipt;
- V0.3 review and deterministic-validation evidence;
- V0.1, V0.2, and V0.3 historical documentary evidence;
- all five supplied reference images;
- package README;
- integrity model;
- asset and package manifests; and
- checksum ledger.

If an existing repository rule requires historical drafts in a different archive location, follow that rule while preserving exact byte identity and cross-reference them from the approved package README.

## 7. Approved Documentary State to Record

The canonical integrated PIA shall state:

- approved PIA version `0.3.1`;
- package wrapper version `0.3.2` as a non-substantive integrity correction;
- status `FOUNDER_APPROVED_DOCUMENTARY_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`;
- Founder documentary design approval `TRUE`;
- implementation, schema, migration, deployment, production, Stead activation, and enrollment authority `FALSE`;
- independent review and external assurance remain `FALSE` / `NOT_EXTERNALLY_ASSURED`;
- V0.1, V0.2, and V0.3 remain preserved historical evidence; and
- the next gate is baseline freeze, source/font/asset registration, controlled work-package preparation, and a separate Founder implementation decision.

Do not claim constitutional lock, external assurance, independent review, implementation completion, verification completion, operational readiness, or enrollment readiness.

## 8. Strict Scope Boundary

Permitted changes:

- add the corrected documentary package;
- place reference assets in the controlled archive location;
- add repository-local manifests, checksums, indexes, and cross-references required by existing governance conventions;
- update an existing PIA index or documentary registry only where necessary to identify this approved package and its non-implementation status; and
- correct purely mechanical internal links or filenames required by the chosen canonical repository path.

Prohibited changes:

- application or backend source code;
- UI components;
- CSS, design tokens, theme files, icon exports, favicons, app bundles, or font files;
- package dependencies;
- database schema or migrations;
- feature flags;
- production configuration;
- app-store metadata;
- deployment or hosting;
- user enrollment;
- unrelated governance or PIA content; and
- substantive rewriting of the approved PIA.

If repository rules require a substantive change to the approved text, stop and present the conflict to the Founder.

## 9. Required Validation

Run bounded validation against only the integrated package and any required index file.

Minimum gates:

1. non-circular package-integrity checks in Section 5 pass;
2. PNG byte identity passes;
3. 43 mandatory PIA sections are present in exact order;
4. each of the five mandatory questions is present exactly once;
5. question answers are exactly three `YES_WITH_EVIDENCE` and two `NO` values;
6. each answer includes `SATISFIED` completeness and closure or gate effects;
7. no `TODO`, `TBD`, placeholder, or unresolved former `NAV-DR-*` identifier exists;
8. no implementation, deployment, production, or enrollment authority changes to true;
9. all active `NAV-FD-*`, `NAV-REQ-*`, `NAV-AC-*`, `NAV-TEST-*`, `NAV-EVID-*`, and section references resolve without duplicate active identifiers;
10. text files use UTF-8 and LF;
11. `git diff --cached --check` passes, with intentional Markdown hard breaks classified if required;
12. no staged or unstaged changes exist outside the bounded documentary package and required index path;
13. repository validators required for documentation-only changes pass; and
14. worktree and index are clean after commit.

Do not run provider-bound model tests, production integrations, app builds, schema operations, deployment commands, or destructive cleanup.

## 10. Commit and Push Rules

1. Stage only the bounded corrected package and any strictly required documentary index update.
2. Show the exact staged file list and staged diff summary before commit.
3. Commit only after every gate passes.
4. Preferred commit message: `docs(pia): record founder-approved navigation visual system`.
5. Push only the new branch to the verified official remote.
6. Do not create a PR or merge.
7. Do not delete prior branches, drafts, assets, stop evidence, or local evidence.

## 11. Required Completion Receipt

Return a structured receipt containing:

- verified repository and remote;
- default branch;
- new branch;
- starting and ending commits;
- commit message and remote branch verification;
- exact canonical package path;
- total files added and any index files modified;
- actual extracted file count;
- package-manifest row count;
- checksum-ledger line count;
- manifest path-set equality result;
- ledger verification result;
- checksum-ledger hash verification result;
- package-manifest self-reference treatment result;
- PNG byte-identity result;
- 43-section and five-question validation results;
- identifier, placeholder, scoped diff, and `git diff --check` results;
- repository-required validator results;
- worktree and index status;
- confirmation that no code, schema, deployment, production, app-store, Stead activation, or enrollment action occurred;
- confirmation that no PR or merge was created; and
- retained nonblocking limitations.

## 12. Stop Conditions

Stop without commit or push if:

- the official repository or baseline cannot be verified;
- any V0.3.2 integrity check fails;
- the canonical placement conflicts with a controlling repository rule;
- any required file is absent;
- a substantive edit to approved text appears necessary;
- a change outside the permitted scope is required;
- the five answers or authority flags drift;
- staged files escape the bounded path;
- a mandatory validator fails; or
- an active Git write or lock is not demonstrably owned by this process.

Preserve evidence of the stop condition and report it accurately. Do not improvise around a failed gate.
