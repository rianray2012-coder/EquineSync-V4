# PIA Five-Question Framework Identification

**Record ID:** `ES-PIA-REMAINING-FIVE-Q-ID-V1.0.0`  
**Status:** `CANONICAL_FIVE_QUESTION_FRAMEWORK_ESTABLISHED_WITH_RECORDED_TERMINOLOGY_OVERRIDE`  
**Implementation authority:** `FALSE`

## Canonical location

The exact five mandatory readiness questions appear in `ES-PIA-MASTER-STANDARD-V1.1` at section 44, PDF page 38. The controlled template implements the same framework at section 41, PDF page 60. The governing source-ingestion commit is `3b17840aae3b0693e006e9378606c1ca1c11286a`; the canonical PDF SHA-256 is `c751a73331d89eb4dd5d5ff3b059c81bb1d99284102c6f39a008aeb84620bbbc`.

## Exact-source wording

The following block preserves the exact wording from the adopted PDF. The source uses the legacy acronym `MAIP`; it is quoted only to authenticate the source and is not the active program term.

> 1. Can engineering build the capability without making unauthorized product decisions?
>
> 2. Can quality assurance determine objectively whether the capability works?
>
> 3. Can a reviewer trace the capability to EquineSync's controlling governance and the MAIP?
>
> 4. Can EquineSync safely operate, support, monitor, recover, and maintain the capability?
>
> 5. Can the Founder determine whether the capability is ready for first-user enrollment?

## Active controlled wording

The current Founder directive expressly establishes `MIAP` as **Master Implementation Atlas Program** and prohibits active renaming to `MAIP`. Therefore active PIA artifacts must reproduce Questions 1, 2, 4, and 5 exactly and reproduce Question 3 with the single hierarchy-authorized terminology correction:

> Can a reviewer trace the capability to EquineSync's controlling governance and the MIAP?

This is a disclosed Founder-directed terminology correction, not a silent edit to the locked PDF.

## Permitted answers

The adopted V1.1 answer vocabulary controls:

- `YES_WITH_EVIDENCE`
- `NO`
- `PARTIALLY_SATISFIED`
- `NOT_APPLICABLE_WITH_JUSTIFICATION`

Questions 1 through 3 must be `YES_WITH_EVIDENCE` before implementation authorization. All five must be `YES_WITH_EVIDENCE` before first-user enrollment. This program grants neither authority.

## Derivative framework disposition

The creation-kit file `00_CONTROL/FIVE_MANDATORY_READINESS_QUESTIONS.md` is complete as a working explanation but paraphrases all five questions and changes answer labels to `YES` and `NOT_APPLICABLE_WITH_APPROVED_RATIONALE`. Those variants are non-canonical summaries. They may supply explanatory fields, but they may not replace the exact active wording or V1.1 answer values.

Every response must state its answer, rationale, supporting source and requirement IDs, assumptions, unresolved blockers, required Founder decisions, and downstream gate effect.

`FIVE_QUESTION_GATE_PASS`
