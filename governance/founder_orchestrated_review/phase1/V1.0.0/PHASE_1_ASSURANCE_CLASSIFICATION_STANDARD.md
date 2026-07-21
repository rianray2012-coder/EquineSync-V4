# Phase 1 Assurance Classification Standard

| Level | Classification | Minimum evidence |
| ---: | --- | --- |
| 1 | `AI_ASSISTED_DOCUMENT_PREPARATION` | AI-created material with disclosed scope and limitations; no qualifying review claim |
| 2 | `SINGLE_EXECUTION_AI_REVIEW` | One identified, bounded execution with controlled input/output and preserved evidence |
| 3 | `PROCEDURALLY_SEGREGATED_INTERNAL_AI_REVIEW` | Valid profiles; isolated and blind executions; no canary leakage; frozen candidate; output schemas; deterministic validation; custody; reconciliation; Founder control |
| 4 | `MULTI_PROVIDER_CORROBORATED_INTERNAL_AI_REVIEW` | Level 3 plus genuinely separate providers and corroboration requirements |
| 5 | `INDEPENDENT_HUMAN_INTERNAL_REVIEW` | A separately identifiable qualified internal human reviewer with documented independence |
| 6 | `INDEPENDENT_EXTERNAL_ASSURANCE` | Qualified external assurance under an applicable professional engagement |

Classification is evidence-derived and machine-checkable where practical. Phase 1 can reach at most Level 3. Any failed segregation, unresolved identity or permission control, missing output, unsealed blind result, candidate drift, or incomplete custody lowers the supported level. A partial Pilot A or documentary package alone remains Level 1.

Never describe Level 3 as independent human review, organizational independence, audit, certification, attestation, regulatory review, or external assurance.
