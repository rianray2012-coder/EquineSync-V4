# Code Guide Schemas

CGP-002 strengthens the schema skeletons to version `0.2.0`. Schemas define identifiers, status fields, evidence metadata, authority references, retained gaps, supersession, and activation-boundary metadata without creating product policy.

## Controlled Values

`CODE_GUIDE_CONTROLLED_VALUES.json` is the canonical machine-readable source. Validators load that JSON file rather than maintaining independent enum copies.

## Versioning

Schema revisions use semantic version strings and the `schema_revision_status` field. Later schema changes must preserve historical records or document supersession.

## Limits

These schemas validate structure and governance metadata. They do not claim guide completeness, product correctness, implementation readiness, or activation authority.

## CGP-003 Source Accession Schemas

CGP-003 adds source accession schemas for source records, source gaps, source conflicts, source supersession, and source-to-guide mappings. These schemas classify source custody and authority metadata only. They do not adopt new external standards, answer Founder-level decisions, or create substantive guide controls.
