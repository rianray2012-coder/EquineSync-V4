# AI V2.0 Exact-Source Chain of Custody

## Source event

- Ingestion timestamp: `2026-07-16T03:42:35Z`
- Source event: Founder-supplied exact-source ingestion directive and DOCX attachment
- Founder classification: `FOUNDER_IDENTIFIED_CORRECT_AI_V2_0_SOURCE_CANDIDATE`
- Repository commit at ingestion: `9f812280542f6e9c43935563badec2de1448947b`
- Branch: `integrate-emergent-final-zip`
- Worktree: pre-existing dirty worktree; no unrelated changes reverted or incorporated

## Custody records

| Role | Path | SHA-256 | Bytes | Treatment |
| --- | --- | --- | ---: | --- |
| Mounted uploaded source | `/Users/rianray/Downloads/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0_FOUNDER_APPROVED.docx` | `414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8` | 140,809 | Read-only source evidence |
| Preserved uploaded copy | `docs/canon/reviews/governance_v1_0_ai_reconciliation/resumption_exact_source/source_uploaded/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0_FOUNDER_APPROVED.docx` | `414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8` | 140,809 | Byte-identical evidence copy |
| Canonical-name repository copy | `docs/canon/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0.docx` | `414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8` | 140,809 | Byte-identical controlling-source candidate copy; not yet adopted or locked |
| Earlier review candidate | `/Users/rianray/Downloads/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0(1).docx` | `9495982c16f73b12a5c254583932578f6037f484285cd0e4c1ebb0a33c5d186b` | 140,749 | Preserved as noncontrolling earlier review candidate |
| Preserved earlier candidate | `docs/canon/reviews/governance_v1_0_ai_reconciliation/resumption_exact_source/source_uploaded/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0(1).docx` | `9495982c16f73b12a5c254583932578f6037f484285cd0e4c1ebb0a33c5d186b` | 140,749 | Byte-identical historical evidence copy |

## Operations performed

1. File listing, file-type detection, and SHA-256 calculation.
2. Read-only ZIP/OPC validation.
3. Read-only OOXML property and text extraction.
4. Read-only rendering to temporary PDF and PNG files for visual inspection.
5. Direct byte-preserving filesystem copies.
6. Byte identity verification by SHA-256 and binary comparison.

No source DOCX was edited or resaved.
