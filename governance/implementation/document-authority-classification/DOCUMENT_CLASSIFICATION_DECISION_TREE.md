# Document Classification Decision Tree

Package ID: `ES-DOC-AUTH-CLASSIFICATION-V1.0.0`
Version: `1.0.0`

Use this decision tree for each artifact, not merely for a directory, package, ZIP, or PR.

## Decision Order

1. Does the artifact directly define mandatory system or product behavior?
   - Yes: classify as `NORMATIVE_AUTHORITY`.
   - No: continue.

2. Does it define a binding architecture, interface, schema, workflow, authorization rule, acceptance criterion, or implementation constraint?
   - Yes: classify as `NORMATIVE_AUTHORITY` unless the operative text is a governance decision, in which case classify as `GOVERNANCE_WITH_NORMATIVE_EFFECT`.
   - No: continue.

3. Does it change approval, adoption, supersession, or controlling status?
   - Yes: classify as `GOVERNANCE_WITH_NORMATIVE_EFFECT` if any Code Guide, implementation, pilot, release, or source-freeze interpretation changes; otherwise classify as `GOVERNANCE_ONLY`.
   - No: continue.

4. Does it impose or prohibit implementation behavior?
   - Yes: classify as `GOVERNANCE_WITH_NORMATIVE_EFFECT` if it is a decision, disposition, gate, or policy record; classify as `NORMATIVE_AUTHORITY` if it is the underlying behavior specification.
   - No: continue.

5. Does it control scope, sequencing, risk treatment, pilot posture, release posture, or implementation authorization?
   - Yes: classify as `GOVERNANCE_WITH_NORMATIVE_EFFECT` when design, code, provider behavior, release workflow, pilot eligibility, or acceptance criteria would change; otherwise classify as `GOVERNANCE_ONLY`.
   - No: continue.

6. Does it only prove integrity, provenance, package composition, or repository custody?
   - Yes: classify as `CUSTODY_EVIDENCE`.
   - No: continue.

7. Is it historical or superseded?
   - Yes: classify as `HISTORICAL_REFERENCE` unless it makes a current controlling claim.
   - No: continue.

8. Is it selected by CGP-005?
   - Yes, as `NORMATIVE_SELECTED_SOURCE`: classify according to the artifact's operative content and set source-freeze membership to `NORMATIVE_SELECTED_SOURCE`.
   - Yes, as `GOVERNING_CONSTRAINT`: classify as `GOVERNANCE_AUTHORITY` with `GOVERNANCE_WITH_NORMATIVE_EFFECT`.
   - Yes, as `SUPPORTING_EVIDENCE`: classify as `CUSTODY_EVIDENCE` or the artifact's higher authority class if its operative content requires it.
   - No: continue.

9. Is it referenced by CGP-006?
   - Yes: use the referenced treatment. Context-only reference does not make the artifact normative. A governing-context reference can require CGP-006 input refresh.
   - No: continue.

10. Would a change alter an instruction in an affected Code Guide?
    - Yes: classify as `NORMATIVE_AUTHORITY` or `GOVERNANCE_WITH_NORMATIVE_EFFECT` and apply the impact matrix.
    - No: continue.

11. Is exact-byte identity preserved?
    - Yes: classify relocation or accession as custody refresh unless controlling path or source-freeze membership changes.
    - No or unknown: classify as `UNCLASSIFIED_HIGH_IMPACT` until hash evidence resolves the claim.

12. Is classification ambiguous or disputed?
    - Yes: classify as `UNCLASSIFIED_HIGH_IMPACT` and stop affected drafting or implementation.
    - No: assign the least restrictive remaining supported class.

## Possible Outputs

| Output | Meaning |
| --- | --- |
| `NORMATIVE_AUTHORITY` | Direct product, system, acceptance, architecture, interface, schema, workflow, authorization, privacy, security, safeguarding, or implementation authority. |
| `GOVERNANCE_WITH_NORMATIVE_EFFECT` | Governance artifact that imposes or changes binding implementation, pilot, release, acceptance, source-freeze, or interpretation constraints. |
| `GOVERNANCE_ONLY` | Governance artifact that controls process, sequencing, approval, or review posture without creating implementation requirements. |
| `CUSTODY_EVIDENCE` | Exact-byte, provenance, repository, manifest, receipt, checksum, validation, branch, PR, or package evidence only. |
| `HISTORICAL_REFERENCE` | Superseded, predecessor, archived, or lineage artifact with no current controlling effect. |
| `UNCLASSIFIED_HIGH_IMPACT` | Authority effect unresolved; treat as stop-control until reviewed. |

## Current Workstream Output Summary

| Workstream | Output |
| --- | --- |
| Item 05 | `CUSTODY_EVIDENCE` for repository integration receipts and hashes; underlying approved PIA source remains `NORMATIVE_AUTHORITY`; current workstream result is `ITEM_05_NORMATIVE_RELOCATION_WITH_IDENTICAL_BYTES`. |
| PR #23 | Mixed package; decision packet, approval record, register, crosswalk, and remediation sequence are `GOVERNANCE_WITH_NORMATIVE_EFFECT`; source register, validation report, manifest, checksum ledger, and change log are custody or governance-supporting records. |
| CGP-005 | Existing curated selected-source freeze remains intact; later PR #23 constraints require appendix treatment, not silent source promotion. |
| CGP-006 | May proceed only after classification validation and required appendix/input-refresh treatment for affected guide drafting. |
