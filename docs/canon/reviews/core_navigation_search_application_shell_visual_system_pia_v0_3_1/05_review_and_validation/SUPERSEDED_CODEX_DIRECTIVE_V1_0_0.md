# Founder Directive to Codex
## Integrate the Founder-Approved Core Navigation Visual-System PIA Package

**Directive ID:** `ES-CODEX-DIR-NAV-VISUAL-V1.0.0`  
**Date:** July 22, 2026  
**Founder authority:** Rian Ray  
**Execution class:** Controlled documentary repository integration only  
**Implementation authority:** `FALSE`  
**Deployment authority:** `FALSE`  
**Production authority:** `FALSE`  
**Enrollment authority:** `FALSE`

## 1. Objective

Integrate the Founder-approved EquineSync Core Navigation, Search, and Application Shell visual-system PIA package into the official EquineSync repository as a controlled documentary and reference-asset package. Record Founder approval, preserve the complete review chain, verify all bytes and identifiers, and produce an auditable repository receipt.

Do not implement the application shell, fonts, icons, favicons, themes, mascot, search behavior, feature flags, source code, schema, deployment configuration, or production assets.

## 2. Controlling Founder Disposition

`FOUNDER_APPROVED_V0_3_DOCUMENTARY_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`

The approved PIA answers are:

- Engineering buildability: `YES_WITH_EVIDENCE`
- Objective QA verification: `YES_WITH_EVIDENCE`
- Governance and MIAP traceability: `YES_WITH_EVIDENCE`
- Operational safety and recovery: `NO`
- First-user enrollment readiness: `NO`

Do not convert Questions 4 or 5 to a positive answer. Do not describe the capability as operationally ready, production ready, deployment ready, pilot ready, or enrollment ready.

## 3. Repository and Baseline Rules

1. Locate the official repository and verify the remote before writing. The expected official repository is `rianray2012-coder/EquineSync-V4`; do not rely on that expectation without verification.
2. Identify the current canonical documentary integration baseline using repository evidence. Do not assume that an old branch, preserved review branch, local checkout, or package-generation branch is current.
3. Record the starting branch, starting commit, remote URL, default branch, worktree status, and index status.
4. Do not modify an existing preserved branch or historical package.
5. Create a new bounded branch. Preferred name: `codex/core-navigation-visual-system-pia-founder-approved-v1`.
6. If the repository has a mandatory naming convention that conflicts with the preferred name, follow the repository convention and report the exact branch used.
7. Do not merge, create a pull request, retag, or modify protected branches unless the Founder separately authorizes it.

## 4. Package Intake and Integrity

1. Copy the supplied archive to an isolated staging directory outside the repository.
2. Verify the outer archive SHA-256 against the supplied checksum file.
3. Extract once into a new empty directory.
4. Verify every file against `07_integrity/CHECKSUMS.sha256` and `07_integrity/PACKAGE_MANIFEST.csv`.
5. Treat PNG files as immutable binary evidence. Do not recompress, optimize, recolor, resize, strip metadata, or normalize them.
6. Preserve UTF-8 and LF for controlled text files.
7. If any checksum, manifest count, path, or required file fails, stop fail-closed. Do not partially integrate the package.

## 5. Canonical Repository Placement

First inspect existing repository PIA and governance layout. Use the established canonical location and naming pattern if one exists.

If no controlling placement exists, use:

`governance/pia/core_navigation_search_application_shell/visual_system/V0.3.1/`

The integrated package shall include, at minimum:

- Founder-approved V0.3.1 PIA section;
- Founder approval record;
- Founder decision register;
- Founder typography memorandum;
- Codex directive;
- V0.3 review report;
- deterministic validation report;
- V0.1, V0.2, and V0.3 historical documentary evidence;
- all five supplied reference images;
- package README;
- asset and package manifests; and
- checksum ledger.

If an existing repository rule requires historical drafts in a different archive location, follow that rule while preserving exact byte identity and cross-reference them from the approved package README.

## 6. Approved Documentary State to Record

The canonical integrated PIA shall state:

- version `0.3.1`;
- status `FOUNDER_APPROVED_DOCUMENTARY_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`;
- Founder documentary design approval `TRUE`;
- implementation, schema, migration, deployment, production, Stead activation, and enrollment authority `FALSE`;
- independent review and external assurance remain `FALSE` / `NOT_EXTERNALLY_ASSURED`;
- V0.1, V0.2, and V0.3 remain preserved historical evidence;
- the former V0.3 design resolutions are ratified as `NAV-FD-005` through `NAV-FD-008`; and
- the next gate is baseline freeze, source/font/asset registration, controlled work-package preparation, and a separate Founder implementation decision.

Do not claim constitutional lock, adoption, external assurance, independent review, implementation completion, verification completion, operational readiness, or enrollment readiness.

## 7. Strict Scope Boundary

Permitted changes:

- add the approved documentary package;
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
- CI/CD behavior except documentary validation already required by repository rules;
- feature flags;
- production configuration;
- app-store metadata;
- deployment or hosting;
- user enrollment;
- unrelated governance or PIA content; and
- substantive rewriting of the approved PIA.

If repository rules require a substantive change to the approved text, stop and present the conflict to the Founder instead of silently revising the document.

## 8. Required Validation

Run bounded validation against only the integrated package and any required index file.

Minimum gates:

1. exact package file count and path inventory;
2. SHA-256 verification for every packaged file;
3. PNG byte identity verification;
4. 43 mandatory PIA sections present in exact order;
5. each of the five mandatory questions present exactly once;
6. question answers are exactly three `YES_WITH_EVIDENCE` and two `NO` values as approved;
7. each answer includes `SATISFIED` completeness and closure/gate effects;
8. no `TODO`, `TBD`, placeholder, or unresolved former `NAV-DR-*` identifier;
9. no implementation, deployment, production, or enrollment authority changed to true;
10. all `NAV-FD-*`, `NAV-REQ-*`, `NAV-AC-*`, `NAV-TEST-*`, `NAV-EVID-*`, and section references resolve without duplicate active identifiers;
11. text files use UTF-8 and LF;
12. `git diff --cached --check` passes, with any intentional Markdown hard breaks explicitly classified if repository rules require them;
13. no staged or unstaged changes outside the bounded documentary package and required index path;
14. repository tests or validators required for documentation-only changes pass; and
15. worktree and index are clean after commit.

Do not run provider-bound model tests, production integrations, app builds, schema operations, deployment commands, or broad destructive cleanup.

## 9. Commit and Push Rules

1. Stage only the bounded approved package and any strictly required documentary index update.
2. Show the exact staged file list and staged diff summary before commit.
3. Commit only after every gate passes.
4. Preferred commit message: `docs(pia): record founder-approved navigation visual system`.
5. Push only the new branch to the verified official remote.
6. Do not create a PR or merge.
7. Do not delete prior branches, drafts, assets, or local evidence.

## 10. Required Completion Receipt

Return a structured receipt containing:

- verified repository and remote;
- default branch;
- new branch;
- starting commit;
- ending commit;
- commit message;
- remote branch verification;
- exact canonical package path;
- total files added and any index files modified;
- package manifest count;
- checksum verification result;
- PNG byte-identity result;
- 43-section validation result;
- five-question validation result;
- identifier and placeholder validation result;
- scoped diff and `git diff --check` result;
- repository-required validator results;
- worktree and index status;
- confirmation that no code, schema, deployment, production, app-store, Stead activation, or enrollment action occurred;
- confirmation that no PR or merge was created; and
- any retained nonblocking limitations.

## 11. Stop Conditions

Stop without commit or push if:

- the official repository or baseline cannot be verified;
- package checksums fail;
- the canonical placement conflicts with a controlling repository rule;
- any required file is absent;
- a substantive edit to approved text appears necessary;
- a change outside the permitted scope is required;
- the five answers or authority flags drift;
- staged files escape the bounded path;
- a mandatory validator fails; or
- an active Git write or lock is not demonstrably owned by this process.

Preserve evidence of the stop condition and report it accurately. Do not improvise around a failed gate.
