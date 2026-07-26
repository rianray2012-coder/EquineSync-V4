# Master Code Guide Source Reconciliation Report

**Prompt ID:** `CGP-003`
**Execution ID:** `CGEXEC-20260726-0002`
**Baseline:** `905f9503e3d3a2dad7d74599fa53efa3eaee240d`
**Branch:** `codex/code-guide-master-source-inventory-cgp-003-v1`
**Status:** `RETURNED_FOR_FOUNDER_REVIEW_WITH_RETAINED_FINDINGS`

## Scope

CGP-003 created a repository-native master inventory of sources that may govern, constrain, inform, or provide evidence for future Code Guide drafting. The inventory is documentary and evidentiary only. It does not draft Code Guide controls, answer policy questions, adopt external standards, or activate guides.

## Source Counts

- Total inventoried source records: `2620`
- Source-to-guide mappings: `14176`
- Controlling records: `403`
- Retained gaps: `7`
- Source conflicts: `4`
- Supersession rows: `4`
- Findings: `5`
- Decision records: `5`
- Open decisions after Founder disposition: `0`

## Classes

- `ADOPTED_GOVERNANCE`: `826`
- `APPROVED_ARCHITECTURE`: `108`
- `APPROVED_PIA`: `10`
- `BLOCKED_OR_CONDITIONAL`: `4`
- `EXTERNAL_STANDARD`: `9`
- `FOUNDER_AUTHORITY`: `43`
- `HISTORICAL_PREDECESSOR`: `38`
- `IMPLEMENTATION_ATLAS`: `603`
- `IMPLEMENTATION_STANDARD`: `247`
- `PROPOSED_NOT_ADOPTED`: `70`
- `REPOSITORY_EVIDENCE`: `629`
- `REVIEW_EVIDENCE`: `29`
- `TEST_EVIDENCE`: `4`

## Authority Status

- `BLOCKED`: `4`
- `CONTROLLING`: `403`
- `HISTORICAL`: `38`
- `PROPOSED`: `70`
- `SUPPORTING`: `2105`

## Guide Coverage

- `ES-CG-00`: `2214` mappings
- `ES-CG-01`: `2214` mappings
- `ES-CG-02`: `655` mappings
- `ES-CG-03`: `392` mappings
- `ES-CG-04`: `694` mappings
- `ES-CG-05`: `478` mappings
- `ES-CG-06`: `218` mappings
- `ES-CG-07`: `735` mappings
- `ES-CG-08`: `557` mappings
- `ES-CG-09`: `554` mappings
- `ES-CG-10`: `2103` mappings
- `ES-CG-11`: `78` mappings
- `ES-CG-12`: `1019` mappings
- `ES-CG-13`: `2265` mappings

## Reconciliation Treatment

- Adopted and locked canon sources are recorded as controlling only when supported by adoption, lock, or registry evidence.
- Candidate, historical, review, and blocked materials remain preserved without being promoted.
- PIA directories are recorded as approved PIA source families, but exact nested package parity remains a retained source-freeze requirement.
- Implementation code, tests, CI, and reports are recorded as repository or test evidence, not governing authority.
- External standards and provider references are inventoried only where already present in repository sources; CGP-003 adopts no new external standard.

## Retained Findings

Findings are registered in `registers/CODE_GUIDE_FINDING_REGISTER.csv` and mirrored to `registers/GUIDE_REVIEW_FINDING_REGISTER.csv` for CGP-002-era review tooling.

## Non-Authorization

CGP-004 was not begun. No substantive Code Guide controls, domain policies, implementation profiles, application-code changes, PIA amendments, atlas amendments, production CI changes, deployment actions, pilot actions, or activation authority were created or exercised.


## Founder Decision Disposition

Founder disposition dated `2026-07-26` accepted the CGP-003 source inventory as a broad discovery and reconciliation index and closed the five CGP-003 decision records. The closed decision records remain preserved in the decision registers and are documented in `governance/implementation/code-guides/receipts/CGP_003_FOUNDER_DECISION_RECONCILIATION.md`.

CGP-003 does not create a final frozen source set for any individual guide. Guide-specific source freezes remain required before an affected guide enters `DRAFTING`.
