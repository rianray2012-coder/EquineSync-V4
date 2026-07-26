
# EquineSync Code Implementation Guide Program

**Program status:** CGP-001 scaffold returned for Founder review
**Prompt ID:** `CGP-001`
**Execution ID:** `CGEXEC-20260725-0001`
**Directive ID:** `ES-DIR-CGP-001-CODE-GUIDE-PROGRAM-INITIALIZATION-2026-07-25`
**Next authorized program prompt:** `CGP-002`

This directory is the canonical documentary home for the EquineSync Code Implementation Guide program. It establishes stable paths, identifiers, registers, placeholders, schemas, validator entrypoints, receipts, and package custody records before any substantive Code Guide drafting begins.

## Canonical Guide List

| Guide ID | Canonical title | Wave | Expected drafting prompt |
|---|---|---:|---|
| `ES-CG-00` | Code Guide Charter | 1 | `CG-00-DRAFT` |
| `ES-CG-01` | Engineering Authority and Precedence | 1 | `CG-01-DRAFT` |
| `ES-CG-13` | Completion, Evidence, and Traceability | 1 | `CG-13-DRAFT` |
| `ES-CG-10` | Testing, Verification, and Assurance | 1 | `CG-10-DRAFT` |
| `ES-CG-02` | Architecture and Module Boundaries | 2 | `CG-02-DRAFT` |
| `ES-CG-03` | Identity, Tenancy, and Authorization | 2 | `CG-03-DRAFT` |
| `ES-CG-04` | Data, State, and Migrations | 2 | `CG-04-DRAFT` |
| `ES-CG-05` | Offline, Synchronization, and Conflicts | 3 | `CG-05-DRAFT` |
| `ES-CG-06` | APIs, Events, and External Adapters | 3 | `CG-06-DRAFT` |
| `ES-CG-07` | Web, Mobile, Accessibility, and Human Factors | 3 | `CG-07-DRAFT` |
| `ES-CG-08` | Domain Engineering Standards | 4 | `CG-08-DRAFT` |
| `ES-CG-09` | Safeguarding, Privacy, Security, and AI | 4 | `CG-09-DRAFT` |
| `ES-CG-11` | Observability, Reliability, Support, and Operations | 5 | `CG-11-DRAFT` |
| `ES-CG-12` | Delivery, Release, Deployment, and Activation | 5 | `CG-12-DRAFT` |

The numerical guide IDs remain canonical even though execution is dependency-based.

## Dependency-Wave Approach

Wave 1 establishes charter, authority, evidence, and assurance foundations. Wave 2 depends on that foundation reaching at least `SCENARIO_VALIDATED` unless separately authorized. Wave 3 depends on relevant Wave 2 guides. Wave 4 depends on relevant Waves 1 through 3. Wave 5 depends on relevant Waves 1 through 4.

## Distinct Authorities

Guide adoption means Founder-authorized acceptance of a guide. Implementation means repository or product work performed under separately granted authority. Merge means branch integration. Deployment means release to an environment. Activation means operational use. CGP-001 authorizes none of those outcomes.

## Directory Map

- `registers/` stores trackers, logs, dependency records, evidence records, findings, decisions, exceptions, supersession records, and session receipts.
- `guides/` stores non-substantive guide placeholders.
- `schemas/` stores CGP-001 JSON Schema skeletons reserved for CGP-002 strengthening.
- `profiles/` is reserved for implementation profiles.
- `templates/` stores structural drafting and review templates.
- `validation/` stores validator entrypoint placeholders and tests proving they do not falsely pass.
- `reviews/`, `receipts/`, `packages/`, and `source-accession/` preserve later review, custody, package, and source records.

No official Code Guide program work exists without a prompt ID, execution ID, artifact inventory row, and receipt.

## Non-Authorization Boundary

No substantive Code Guide controls were created by CGP-001. No guide is adopted, accessioned, active, implemented, merged, deployed, piloted, activated, or approved for production use by this scaffold.
