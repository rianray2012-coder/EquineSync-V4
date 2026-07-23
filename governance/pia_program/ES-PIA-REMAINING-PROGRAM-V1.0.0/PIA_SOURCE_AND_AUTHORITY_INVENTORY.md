# PIA Source and Authority Inventory

**Record ID:** `ES-PIA-REMAINING-SOURCE-INVENTORY-V1.0.0`
**Inventory baseline:** `5e549056ee25fd1992846bbd6fedaba4329ab668`
**Repository:** `rianray2012-coder/EquineSync-V4`
**Status:** `SOURCE_DISCOVERY_COMPLETE_FOR_PROGRAM_INVENTORY`
**Implementation authority:** `FALSE`

## Applied hierarchy

1. locked constitutional governance;
2. Founder-approved decisions and current Founder directives;
3. constitutional companions and authoritative registers;
4. adopted PIA Master Standard V1.1;
5. adopted MIAP planning and orchestration authorities;
6. approved or current state-qualified PIAs;
7. engineering work packages;
8. code, configuration, migrations, tests, and operational material; and
9. non-authoritative reference material.

Lower levels do not silently override higher levels. Current code is evidence of as-built state, not product authority.

## Program control and custody sources

| Source ID | Authority/status | Exact locator | SHA-256 or Git identity | Use |
| --- | --- | --- | --- | --- |
| `SRC-DIR-001` | Current Founder drafting directive | External supplied text: `/Users/rianray/.codex/attachments/e5d473fc-c150-429d-94b0-598cd256d504/pasted-text.txt` | `f19568fa7ecf6527306808afd5116f6df4a65ab91a7886e2e451a2b87d350d68` | Controls this program's documentary scope, MIAP terminology, lifecycle, deliverables, and prohibitions. |
| `SRC-KIT-001` | `CONTROLLED_WORKING_DERIVATIVE` | External supplied `EquineSync_Remaining_PIA_Creation_Kit_V1_0_0.zip` | `123d29bf5f776ebe100f121b2a759f3ea42363e6559540d6d4f7806f944a6b76` | Authenticated drafting aids, registers, review checklists, schema, and validator. All 31 embedded checks passed. |
| `SRC-GOV-001` | Locked constitutional baseline | `docs/governance_v1_0/GLOBAL_GOVERNANCE_V1_0_LOCK_RECORD.md` | `16c9b4c4f16f078c036c0768da38ae0d70cc643b10f9b5d76a50205a426ba551` | Establishes immutable Global Governance V1.0 and preserves each artifact's own state. |
| `SRC-GOV-002` | Aggregate locked manifest | `docs/governance_v1_0/GLOBAL_GOVERNANCE_V1_0_BASELINE_MANIFEST.json` | `f5666ebffbfe527f6d01eb7fe7fbe9f21de541b7b3afe5c4a1fe2d1b3379bfe9` | Exact locked baseline inventory. |
| `SRC-PIA-STD-001` | Founder-approved, adopted, effective | Canonical V1.1 PDF identified in `PIA_MASTER_TEMPLATE_IDENTIFICATION.md` | `c751a73331d89eb4dd5d5ff3b059c81bb1d99284102c6f39a008aeb84620bbbc` | Controls PIA content, lifecycle, gates, and template. |
| `SRC-PIA-STD-002` | Founder adoption/effectiveness record | `.../source_evidence/adoption/Founder_Adoption_and_Approval_Record_ES_PIA_Master_Standard_V1_1.pdf` | `bd5d466494bf24d5ec6942b8f8c7b9248881d4d731a5861b020cef8a7d6ffcd8` | Establishes V1.1 lifecycle despite the source PDF's preserved pre-adoption header. |
| `SRC-MIAP-001` | `ADOPTED_PLANNING_ATLAS_NOT_LOCKED` | `docs/implementation/MASTER_EQUINESYNC_IMPLEMENTATION_ATLAS_V1_0.md` | `bfa77b5e03fd9a75c8865b723794ee2da687754f030e72022f1476b9af6021d8` | Planning and orchestration authority only. No runtime, schema, migration, production, or enrollment authority. |
| `SRC-MIAP-002` | Founder adoption decision | `docs/implementation/MASTER_EQUINESYNC_IMPLEMENTATION_ATLAS_V1_0_ADOPTION_DECISION.md` | `3ea200c52d2149c2b0eead26ffd88785b2b86947fd7483ea6bbe139f05a665ce` | Confirms planning-only status. |
| `SRC-PORT-001` | Founder-directed controlling portfolio | `governance/pia_portfolio/ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0/sources/LOCKED_TEN_ITEM_PIA_PORTFOLIO.md` | `d487df6cd36b8b4c62c4df59ea6f278a1358c3dee824bda17d74c94732b27dd2` | Caps the portfolio at ten PIAs; a split, merger, addition, or rename requires Founder decision. |
| `SRC-PORT-002` | Realignment/drift control record | `governance/pia_portfolio/ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0/FOUNDER_DIRECTED_PORTFOLIO_LOCK_RECORD.md` | `417002ce200865f93ef677c1854b179ac96bb16d83082b842178dec6e1c75c40` | Establishes current ten-item position and preserves successor-status limits. |
| `SRC-PORT-003` | Detailed discovered inventory | `governance/pia_portfolio/ES-PIA-PORTFOLIO-REALIGNMENT-V1.0.0/PIA_PACKAGE_INVENTORY.csv` | Package-controlled file | Provides package, canon, review, and historical classifications. |

## PIA and review-state sources

| Source ID | Position | Current evidence | Status/use boundary |
| --- | ---: | --- | --- |
| `SRC-PIA-01` | 01 | Frozen Identity PIA V1.1.0 inside `ES-REM-2026-001/frozen_predecessor/...zip` | Underlying design was Founder approved; current successor text remains pending fresh review and is not ratified. |
| `SRC-PIA-03A` | 03A | Frozen Relationships PIA V1.1.0 revised candidate plus current remediation package | Underlying design was Founder approved; current successor text and 14 ADRs are not Founder approved. |
| `SRC-PIA-02-V100` | 02 | `governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.0` | Preserved initial candidate/review evidence; not approved. |
| `SRC-PIA-02-R3` | 02 | `governance/pia/ES-PIA-FACILITY-TENANT-ORGANIZATION-V1.0.1-FOUNDER-DECISION-INCORPORATED-REVIEW-CANDIDATE` | Founder decisions incorporated; formal fresh review blocked by runtime permission failure; adopted `false`. |
| `SRC-REV-022` | 02 | `governance/founder_orchestrated_review/review_cycles/ES-REV-2026-022` | Six permission records failed before spawn; zero formal review roles started. Mechanical validation is not independent review. |
| `SRC-FALLBACK-001` | All | `governance/founder_orchestrated_review/temporary_non_agent_fallback/FORA-NONAGENT-FALLBACK-2026-001` | Temporary procedural fallback evidence only; use remains subject to its authorization, frozen-input, and lane controls. |
| `SRC-ITEM04-PKG-001` | 04 | Verified external Item 04 Founder-approved V0.3 package integrated under this branch | V0.3 approved documentary design baseline; HOR-FD-001 through HOR-FD-017 approved documentary-only; formal review and implementation remain pending. |

## Canonical source families

The detailed package inventory supplies exact versions, hashes, paths, positions, and dependent positions. The following are the controlling families for remaining-PIA planning:

| Source family | Primary portfolio ownership | Key repository source |
| --- | --- | --- |
| Identity, Account, Actor | 01 | `docs/canon/MASTER_IDENTITY_ACCOUNT_AND_ACTOR_MODEL_V2_0.md` |
| Relationship | 03A | `docs/canon/MASTER_RELATIONSHIP_MODEL.md` |
| Permission and Access Control | 03C | `docs/canon/adopted_sources/MASTER_PERMISSION_AND_ACCESS_CONTROL_MODEL_V1_1_ADOPTED_SOURCE.md` |
| Agreement, Consent, Authorization | 03B, cross-PIA | `docs/canon/adoptions/c0_019_agreement_consent_authorization_v2_1/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1_ADOPTED_PRE_LOCK.md` |
| Facility, Barn, Business, Ecosystem | 02 | adopted sources under `docs/canon/adopted_sources/` |
| Horse Lifecycle and Transfer | 04 | Horse Lifecycle V3.0 broad architecture; locked Transfer and Continuity V2.0; V3.1 state-qualified successor input |
| Equine Health and Barn Operations | 07 | `MASTER_EQUINE_HEALTH_WELFARE_MEDICAL_RECORD_AND_CLINICAL_SUPPORT_MODEL_V1_1_ADOPTED_SOURCE.md`; Barn V3.1 |
| Safeguarding and protected participants | 08 | `MASTER_MINOR_GUARDIANSHIP_SAFEGUARDING_AND_PROTECTED_PARTICIPANT_MODEL_V1_2_ADOPTED_SOURCE.md` |
| Search and Product Vision | 05 | Search V2.0 adopted source; `docs/canon/MASTER_PRODUCT_VISION.md` |
| Communication and Media | 10, with 06 delivery dependencies | Communication V2.0 and Media V2.1 adopted sources |
| Financial Truth | 09 | `docs/canon/MASTER_FINANCIAL_TRUTH_AND_RESPONSIBILITY_MODEL_V2_1.md` plus adoption/lock evidence |
| Claims, disputes, records, audit, privacy | Cross-PIA | adopted sources and lock records identified in `PIA_PACKAGE_INVENTORY.csv` |
| Platform operations, resilience, configuration, integration, vendor security | Cross-PIA | adopted sources under `docs/canon/adopted_sources/` |
| Reporting and analytics | Cross-PIA, surfaced principally through 05 and domain views | `MASTER_REPORTING_ANALYTICS_AND_BUSINESS_INTELLIGENCE_MODEL_V2_0_FOUNDER_APPROVED.md` and constitutional lock record |

## Protected and immutable boundaries

This program will not modify:

- `docs/governance_v1_0/` locked baseline artifacts;
- `docs/canon/locks/` or adopted/founder-approved source bytes;
- any frozen predecessor ZIP, checksum, failed review, or prior draft;
- existing Facility V1.0.0 or V1.0.1-R3 package evidence;
- default/protected branches, tags, release records, application code, schemas, migrations, or infrastructure.

New work is confined to `governance/pia_program/ES-PIA-REMAINING-PROGRAM-V1.0.0/` until a separately controlled PIA workspace is authorized for a selected batch.
