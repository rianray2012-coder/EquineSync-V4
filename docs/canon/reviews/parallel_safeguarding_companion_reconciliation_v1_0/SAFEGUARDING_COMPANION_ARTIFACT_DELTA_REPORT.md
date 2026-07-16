# Safeguarding Companion Artifact Delta Report

## Available Exact Predecessors

Four Markdown V1.1 predecessors were compared to the package's V1.2 candidates. Machine-readable patches are preserved under `diffs/`.

| Artifact | Predecessor SHA-256 | Candidate SHA-256 | Change size |
| --- | --- | --- | ---: |
| Canon Dependency Map | `516856c982af8d882ec6f94933b5a01ea6558ca63d47c9a6237ee76fe0f12a44` | `7262277efc185c78b911d85fb6d3b8c2556ebe6f5b3b8b5a97b85a34517fa24c` | +19 / -13 |
| Authority Matrix | `1b614fafa17f5841363646e72191883db2bc2b8c5a54a959a6a0bf0f77c018fa` | `31102a8f399d51449807f6bb65c9775e931b5796d2602b029e4a0afb634ade7f` | +44 / -20 |
| Cross Reference Index | `94badc3b6eeae1dd1d96d8c577a187bbdfe696df4db35e573629581a7856904e` | `6e810af409884936ad25f709d0f482f859765a84a5437625e635b1fcdcc239cb` | +53 / -29 |
| Vocabulary and Definitions Index | `ee88f5e8ba3602ffecd3f15f5acc2d8881e58809645dac6d7038c3b1a4d0d0d0` | `aa8888de9f0e60a5c30dffc5f86838129e44f24c2bc65d98ec940056251155fe` | +240 / -3 |

The first three also have distinct predecessor and successor DOCX hashes. The Vocabulary predecessor has no matching mounted DOCX, so Markdown is the semantic comparison source.

## Missing Exact Predecessors

No exact predecessor bytes were found for the Domain Ownership Register or Cross-Canon Reference Normalization Register. Their package artifacts are delta candidates, not exact-source successors.

## Patch Schedules

The package's Canon Index row, 15 FD-MSP rows, 40 GOV-MSP rows, and 40 RTM rows were inspected in Markdown, JSON, and XLSX. They remain unapplied because the four exact target instruments are unavailable and all identifiers remain provisional.

## Delta Risks

- The V1.2 candidates mix valid safeguarding additions with premature active-status language.
- The Vocabulary candidate makes the largest change and needs focused semantic review before any successor decision.
- Package self-validation confirms row counts and duplicates inside the package only; it cannot detect collisions against unmounted exact instruments.

Detailed hash pairs, patch paths, and lifecycle classifications are in `SAFEGUARDING_COMPANION_ARTIFACT_DELTA.csv`.
