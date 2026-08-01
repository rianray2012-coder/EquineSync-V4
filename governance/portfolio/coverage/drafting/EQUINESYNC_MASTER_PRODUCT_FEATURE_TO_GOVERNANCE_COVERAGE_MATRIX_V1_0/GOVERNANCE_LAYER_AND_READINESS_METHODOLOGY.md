# GOVERNANCE_LAYER_AND_READINESS_METHODOLOGY

Authority statement: `DOCUMENTARY_COVERAGE_ANALYSIS_ONLY_NO_ADOPTION_IMPLEMENTATION_DEPLOYMENT_PILOT_OR_PRODUCTION_AUTHORITY`

## Layer Model

Every matrix row carries explicit documentary coverage fields for PIA, Code Guide, ADR, operating standard, runbook, AI governance, safeguarding, privacy, and reporting. The allowed layer vocabulary is `NOT_APPLICABLE`, `NOT_IDENTIFIED`, `GAP`, `CANDIDATE`, `PARTIAL`, `COVERED_WITH_RETAINED_GAP`, `COVERED`, `ADOPTED_NOT_ACTIVE`, and `ACTIVE`. This revision does not use `ACTIVE` because no separate activation evidence was supplied or authorized.

## Overall State Derivation

Overall `Governance coverage state` is derived by priority: new-PIA missing ownership, PIA supplement partial coverage, Code Guide gap, ADR gap, operating-standard gap, runbook gap, fully covered documentary coverage, or retained implementation/evidence gap. The state is a documentary planning classification only.

## Readiness Score

Scores are calculated from weighted layer coverage: PIA 30, Code Guide 15, ADR 10, operating standard 10, runbook 8, AI 7, safeguarding 8, privacy 8, and reporting 4. State factors are: not applicable/covered 100 percent, covered with retained gap 78 percent, partial 55 percent, candidate 35 percent, gap 12 percent, not identified 0 percent. Scores are capped by overall state so a missing mandatory layer cannot appear governance-ready.

## Bands

| score_range | band |
| --- | --- |
| 0-24 | CRITICAL_GOVERNANCE_GAP |
| 25-49 | LOW_READINESS |
| 50-74 | PARTIAL_READINESS |
| 75-89 | HIGH_READINESS_WITH_RETAINED_GAPS |
| 90-100 | GOVERNANCE_READY |

Readiness does not mean implementation completeness, runtime safety, production readiness, adoption, activation, or release approval.
