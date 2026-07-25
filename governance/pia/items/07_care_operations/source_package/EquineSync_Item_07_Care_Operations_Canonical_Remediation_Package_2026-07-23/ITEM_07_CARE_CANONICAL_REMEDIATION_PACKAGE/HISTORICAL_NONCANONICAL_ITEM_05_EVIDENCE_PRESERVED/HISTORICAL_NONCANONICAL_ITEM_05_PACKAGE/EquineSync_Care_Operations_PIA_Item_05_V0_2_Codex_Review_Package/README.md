# EquineSync Care Operations PIA Item 05 V0.2 Codex Review Package

## Package purpose

This package supplies the preserved Care Operations PIA V0.2 strengthened documentary candidate, its V0.1 predecessor evidence, the internal V0.1-to-V0.2 review record, deterministic validation evidence, and the governing Codex directive for repository intake and a compliant fresh structured review.

## Controlled identity

- Portfolio position: `Item 05`
- PIA ID: `ES-PIA-CARE-OPERATIONS-V0.2.0`
- Master template: `ES-PIA-MASTER-STANDARD-V1.1`
- Candidate status: `ITEM_05_V0_2_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`
- Founder decisions: `CARE-FD-001` through `CARE-FD-020`, approved for documentary drafting
- Authority effect: documentary only
- Implementation, schema, migration, deployment, production, pilot, and enrollment authority: `FALSE`

## Directory map

- `CURRENT_CANDIDATE/` contains the V0.2 DOCX, controlled Markdown, and machine-readable JSON.
- `PREDECESSOR_EVIDENCE/` contains the preserved V0.1 documentary set and the internal review/revision report.
- `VALIDATION/` contains the deterministic V0.2 documentary validation report.
- `CODEX_DIRECTIVE.md` contains the execution directive.
- `PACKAGE_MANIFEST.json` records package identity and payload metadata.
- `CHECKSUMS.sha256` covers every package file except itself.

## Integrity model

1. Verify the outer ZIP checksum supplied beside the archive.
2. Run `unzip -t` against the archive.
3. From the extracted package root, run `sha256sum -c CHECKSUMS.sha256`.
4. Confirm the controlled identity above before any repository mutation.

Any checksum, identity, item-number, authority, or repository-program mismatch is a fail-closed stop condition.
