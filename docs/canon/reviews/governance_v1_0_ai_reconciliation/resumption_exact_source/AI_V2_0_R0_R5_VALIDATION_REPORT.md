# AI V2.0 R0-R5 Validation Report

## Validation result

`PASSED_WITH_NARROW_FOUNDER_RATIFICATION_GATE_OPEN`

## Executed validations

| Validation | Actual result |
| --- | --- |
| Uploaded, preserved, and canonical DOCX SHA-256 comparison | 3 copies passed; all `414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8` |
| DOCX ZIP/OPC integrity | Passed |
| Read-only rendering | 42 pages rendered and visually inspected; passed |
| JSON parsing | All R0-R5 JSON artifacts passed |
| Section 96 extraction | Exact 13 bullets matched the DOCX in order |
| Decision grouping | AI-FD01 through AI-FD12 passed; AI-FD12 preserves two exact bullets |
| R3/R4 artifact hash verification | Passed |
| Finding-ledger gate | P0 0, closed P1 1, open P1 1, R6 unauthorized |
| Secret-pattern scan | Passed |
| Trailing-whitespace scan | Passed |
| `git diff --check` | Passed |

## Source comparison result

The earlier `(1)` candidate and founder-approved candidate differ in lifecycle wording, Document Control, and terminal state. Section 96 and the substantive AI boundaries remain aligned. The later founder-approved file is classified as the selected controlling source candidate; the earlier file remains preserved historical review evidence.

## Stop condition

Founder ratification of the newly assigned IDs and derived matrix remains outstanding. Phase R6 and later phases were not executed. No adoption or lock record was created.
