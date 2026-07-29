# ES-CG-01 Quality, Usability, And Accessibility Requirements

| requirement_id | name | requirement | verification_method |
| --- | --- | --- | --- |
| QUAL-01 | Clarity | Each requirement uses direct mandatory language and identifies the authority boundary it depends on. | Document review plus validator-required fields. |
| QUAL-02 | Consistent terminology | Guide terms preserve V1.1 controlled meanings for adoption, accession, activation, implementation, evidence, warning, and gap states. | Controlled-token scan and cross-guide review. |
| QUAL-03 | Discoverability | A reviewer can find source, control, invariant, question, verification, finding, and checklist evidence from the package manifest. | Manifest and reference validation. |
| QUAL-04 | Implementer comprehension | A future implementer can identify applicable controls, prohibited actions, and required evidence without inventing product policy. | Implementer usability review. |
| QUAL-05 | Reviewer comprehension | A reviewer can distinguish documentary evidence from future implementation or runtime evidence. | Peer, assurance, and adversarial review. |
| QUAL-06 | Low-ambiguity control language | Controls avoid undefined discretion and preserve exception treatment. | Control catalog validation. |
| QUAL-07 | Machine readability | CSV and JSON artifacts parse and use stable identifiers. | Package-local validator and tests. |
| QUAL-08 | Error-state usefulness | Validation failures identify missing, malformed, prohibited, or inconsistent inputs. | Negative fixture tests. |
| QUAL-09 | Accessibility | Guide text and tables preserve plain-language labels, stable headings, and non-visual status tokens. | Document review. |
| QUAL-10 | Predictable templates | Required per-guide files use the same names and field structure. | Required-file validation. |
| QUAL-11 | Minimal duplicate entry | Master registers are derived from per-guide registers and preserve identifier equality. | Reference validation. |
| QUAL-12 | Offline documentary usability | A reviewer can inspect the package from repository files without network calls after checkout. | Local validator design. |
| QUAL-13 | Traceability navigation | Source, atlas, repository-responsibility, and verification rows preserve bidirectional identifier references. | Traceability validation. |
| QUAL-14 | Exception usability | Exception eligibility and future authority requirements are visible for each control. | Control and finding review. |
| QUAL-15 | Evidence submission usability | The package identifies which evidence is present now, future implementation evidence, and future runtime evidence. | Assurance review and readiness matrix. |
