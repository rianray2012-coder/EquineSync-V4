# CGP-003 Founder Decision Reconciliation

**Program:** EquineSync Code Implementation Guide Program
**Prompt ID:** `CGP-003`
**Execution ID:** `CGEXEC-20260726-0002`
**Repository:** `rianray2012-coder/EquineSync-V4`
**Decision date:** `2026-07-26`
**Execution baseline:** `905f9503e3d3a2dad7d74599fa53efa3eaee240d`
**Primary source-inventory commit:** `a3481f6566d2e7c1fbc7866f10cc8e6327501722`
**Original metadata finalization commit:** `c3b1447b4e6ded5851bf383a801b7bfc073ec8cc`

## Disposition Summary

Founder disposition accepted the CGP-003 source inventory as a broad discovery and reconciliation index. It is not the final frozen source set for any individual Code Guide. Each guide must later establish its own exact, checksum-controlled source freeze before substantive drafting begins.

## Decision Records

### CGP003-D-0001 Binding External Standards

**Status:** `CLOSED_WITH_DEFERRED_GUIDE_SPECIFIC_ADOPTION`

Existing references to external standards, frameworks, platforms, and providers remain `SUPPORTING` sources unless and until a specific external standard and version are separately adopted through authorized guide-drafting, legal, product, privacy, security, safeguarding, or Founder disposition. A repository reference does not make an external standard binding.

Required later action: guide-specific drafting may propose a standard for adoption, but may not silently elevate that standard into controlling authority.

### CGP003-D-0002 Exact PIA and Source-Package Bytes

**Status:** `CLOSED_WITH_MANDATORY_GUIDE_SPECIFIC_SOURCE_FREEZE`

Every Code Guide must complete an exact-byte source freeze before advancing from `CHARTERED` to `DRAFTING`. The freeze must identify controlling source IDs, repository paths, artifact or package versions, approval or adoption records, checksums, checksum verification results, custody status, unresolved conflicts, retained historical sources, and superseded or non-controlling sources.

Required later action: no Code Guide may rely solely on a directory-level source-family designation where multiple versions, packages, or historical records coexist.

### CGP003-D-0003 Code Behavior Conflicting With Documentary Authority

**Status:** `CLOSED_DOCUMENTARY_AUTHORITY_CONTROLS`

When current code, tests, migrations, CI behavior, or runtime behavior conflicts with adopted documentary authority, adopted documentary authority remains controlling and code is implementation evidence only. Conflicts must be recorded as implementation divergence, defect, stale-document candidate, or decision request.

Required later action: changing documentary authority requires separate governance or Founder disposition; changing code requires separate implementation authority.

### CGP003-D-0004 Authority and Precedence

**Status:** `CLOSED_WITH_INTERIM_PRECEDENCE_RULE`

Interim precedence is approved in this order: latest explicit Founder disposition; adopted global and artifact-specific governance; Founder-approved PIAs; approved architecture and implementation standards; approved implementation atlases; repository code/tests/CI/reports/runtime as implementation evidence only; proposed, candidate, blocked, historical, or superseded material as non-controlling context.

Additional treatment: a specific source controls only within its authorized scope; a specific source may not silently weaken global prohibitions, safety, safeguarding, privacy, financial, or activation boundaries; later supersession must be explicit; an implementation atlas may not override a PIA; application code may not override documentary authority.

Required later action: this interim program rule must later be expressed as stable controls in `ES-CG-01` under authorized guide drafting.

### CGP003-D-0005 Activation of Code Guides as Engineering Gates

**Status:** `CLOSED_SEPARATE_ACTIVATION_DISPOSITION_REQUIRED`

Code Guide adoption alone does not activate a guide as an implementation, pull-request, merge, release, deployment, pilot, or production gate. Activation requires a separate disposition after substantive guide approval, repository accession of exact approved bytes, successful guide validation, required reviews, mappings, operational ownership, enforcement behavior, rollback or disablement treatment, and confirmation that the gate does not create unauthorized authority.

Required later action: until such a disposition exists, every Code Guide remains documentary and advisory for controlled planning and review.

## Source-Freeze Treatment

A guide-specific exact-byte source freeze is mandatory before an affected guide advances from `CHARTERED` to `DRAFTING`. CGP-004 may proceed after CGP-003 repository integration because it is a program-level current-state assessment and not substantive guide drafting.

## Retained Findings

The retained P2 and P3 findings remain open. They do not block CGP-003 repository integration, but they block affected guide adoption or activation where the required later treatment has not been completed.

## Non-Authorization

CGP-004 was not begun. No substantive Code Guide controls, domain policies, implementation profiles, application-code changes, PIA amendments, atlas amendments, production CI changes, deployment actions, pilot actions, or activation authority were created or exercised.
