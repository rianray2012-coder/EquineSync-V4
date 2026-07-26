# EquineSync Code Implementation Guide Program

**Current foundation prompt:** `CGP-002`
**Execution ID:** `CGEXEC-20260726-0001`
**Next prompt after CGP-002 return:** `CGP-003`

This directory is the canonical documentary and machine-readable home for the EquineSync Code Implementation Guide program.

## Foundation Components

- `schemas/CODE_GUIDE_CONTROLLED_VALUES.json` is the canonical controlled-value source.
- `schemas/` contains versioned JSON schema definitions for guides, controls, invariants, questions, dependencies, traceability, profiles, evidence, exceptions, and findings.
- `templates/` contains reusable generic templates for future guide work.
- `validation/` contains deterministic validators, fixtures, tests, and the portfolio entrypoint.
- `registers/` stores trackers, logs, dependency records, evidence records, findings, decisions, exceptions, supersession records, and session receipts.
- `reviews/`, `receipts/`, and `packages/` preserve validation, custody, and package records.

No official Code Guide program work exists without a prompt ID, execution ID, artifact inventory row, and receipt.

## Boundary

CGP-002 establishes shared machinery only. It does not create substantive Code Guide controls, product policy, implementation authority, deployment authority, pilot authority, production authority, financial authority, messaging/community authority, AI authority, moderation authority, archival migration authority, or enrollment authority.
