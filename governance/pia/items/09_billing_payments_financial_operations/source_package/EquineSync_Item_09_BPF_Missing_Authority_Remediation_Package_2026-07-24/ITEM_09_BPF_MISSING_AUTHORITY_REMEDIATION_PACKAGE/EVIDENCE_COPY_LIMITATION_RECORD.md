# Item 09 BPF Evidence Copy Limitation Record

Record ID: ES-PIA-ITEM-09-BPF-EVIDENCE-COPY-LIMITATION-2026-07-24-01

Prepared by: Codex

Prepared on: 2026-07-24

## Limitation

During preparation of this remediation package, direct reads and copy operations against several R15 evidence files stalled in the shell session. Codex stopped those operations and did not use stalled or partially copied bytes as evidence.

## Retained Copied Evidence

The only copied preserved evidence retained in this remediation package is the Founder documentary directive family that copied cleanly:

- `EquineSync_Item_09_BPF_PIA_V0_2_FOUNDER_APPROVED_CODEX_DIRECTIVE.md`
- `EquineSync_Item_09_BPF_PIA_V0_2_FOUNDER_APPROVED_CODEX_DIRECTIVE.md.sha256`
- `INTAKE_AND_AUTHORITY_CLASSIFICATION_NOTE.md`

## Accounted Evidence Not Re-Embedded

The following evidence remains accounted for by previously observed path, sidecar, manifest, and hash verification rather than by re-embedded file copy:

- R15 Item 09 status note.
- Handoff manifest and handoff checksum ledger.
- Outer handoff ZIP bytes.
- Inner V0.2 BPF source package ZIP bytes.
- Extracted V0.2 package manifest, checksum ledger, strengthened Markdown, DOCX, machine-readable JSON, review, and validation artifacts.

## Custody Effect

This limitation does not close the missing-approval blocker. It further supports the fail-closed determination: Item 09 remains blocked unless the exact original standalone Founder approval record is supplied and authenticated or a replacement Founder approval/disposition is executed.
