# Register Data Dictionary

**Prompt ID:** `CGP-001`

The register headers below preserve the required CGP-001 column contracts. The program tracker adds `work_status` to record the directive-required `NOT_STARTED` work package state without overloading guide maturity or prompt status.

## CODE_GUIDE_PROGRAM_TRACKER.csv

| Column | Definition |
|---|---|
| `record_id` | Stable row identifier. |
| `record_type` | Program, guide, work package, or other row type. |
| `guide_id` | Canonical guide identifier when applicable. |
| `work_item` | Short documentary name for the tracked item. |
| `wave` | Dependency wave or program wave marker. |
| `primary_dependency` | High-level upstream dependency recorded without control-level detail. |
| `maturity_state` | Guide or program maturity value from CONTROLLED_VALUES.md. |
| `current_prompt` | Prompt currently governing the row. |
| `prompt_status` | Prompt status value from CONTROLLED_VALUES.md. |
| `adoption_state` | Adoption state value from CONTROLLED_VALUES.md. |
| `accession_state` | Accession state value from CONTROLLED_VALUES.md. |
| `owner` | Responsible person or role, if assigned. |
| `next_action` | Next documentary action. |
| `next_prompt` | Next prompt or drafting prompt expected for the row. |
| `blocked_by` | Known blocker, if any. |
| `last_updated` | Date the row was last updated. |
| `receipt_path` | Repository path to the controlling receipt. |
| `notes` | Non-substantive notes. |
| `work_status` | Work package state; added in CGP-001 to represent NOT_STARTED explicitly. |

## CODE_GUIDE_PROMPT_EXECUTION_LOG.csv

| Column | Definition |
|---|---|
| `execution_id` | CGP-001 register field reserved for later authorized detail. |
| `prompt_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `work_package` | CGP-001 register field reserved for later authorized detail. |
| `platform` | CGP-001 register field reserved for later authorized detail. |
| `issued_date` | CGP-001 register field reserved for later authorized detail. |
| `issued_by` | CGP-001 register field reserved for later authorized detail. |
| `baseline_commit` | CGP-001 register field reserved for later authorized detail. |
| `source_freeze_id` | CGP-001 register field reserved for later authorized detail. |
| `input_package_id` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `returned_date` | CGP-001 register field reserved for later authorized detail. |
| `output_package_id` | CGP-001 register field reserved for later authorized detail. |
| `output_paths` | CGP-001 register field reserved for later authorized detail. |
| `findings_p0` | CGP-001 register field reserved for later authorized detail. |
| `findings_p1` | CGP-001 register field reserved for later authorized detail. |
| `findings_p2` | CGP-001 register field reserved for later authorized detail. |
| `findings_p3` | CGP-001 register field reserved for later authorized detail. |
| `open_decisions` | CGP-001 register field reserved for later authorized detail. |
| `retained_gaps` | CGP-001 register field reserved for later authorized detail. |
| `commit_sha` | Result commit recorded after commit when available. |
| `remote_verified` | Remote branch verification state. |
| `next_prompt` | Next prompt or drafting prompt expected for the row. |
| `receipt_path` | Repository path to the controlling receipt. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_ARTIFACT_INVENTORY.csv

| Column | Definition |
|---|---|
| `artifact_id` | CGP-001 register field reserved for later authorized detail. |
| `program_or_guide_id` | CGP-001 register field reserved for later authorized detail. |
| `artifact_type` | CGP-001 register field reserved for later authorized detail. |
| `title` | CGP-001 register field reserved for later authorized detail. |
| `expected_path` | CGP-001 register field reserved for later authorized detail. |
| `required_stage` | CGP-001 register field reserved for later authorized detail. |
| `required` | CGP-001 register field reserved for later authorized detail. |
| `version` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `source_prompt` | CGP-001 register field reserved for later authorized detail. |
| `checksum` | SHA-256 checksum or documented self-reference marker. |
| `commit_sha` | Result commit recorded after commit when available. |
| `remote_verified` | Remote branch verification state. |
| `supersedes` | CGP-001 register field reserved for later authorized detail. |
| `superseded_by` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_CONTROL_REGISTER.csv

| Column | Definition |
|---|---|
| `control_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `title` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `assurance_class` | CGP-001 register field reserved for later authorized detail. |
| `risk_domains` | CGP-001 register field reserved for later authorized detail. |
| `governing_sources` | CGP-001 register field reserved for later authorized detail. |
| `requirement` | CGP-001 register field reserved for later authorized detail. |
| `applicability` | CGP-001 register field reserved for later authorized detail. |
| `required_positive_tests` | CGP-001 register field reserved for later authorized detail. |
| `required_negative_tests` | CGP-001 register field reserved for later authorized detail. |
| `required_evidence_grade` | CGP-001 register field reserved for later authorized detail. |
| `independent_review_required` | CGP-001 register field reserved for later authorized detail. |
| `exception_allowed` | CGP-001 register field reserved for later authorized detail. |
| `activation_gate` | CGP-001 register field reserved for later authorized detail. |
| `version` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_INVARIANT_REGISTER.csv

| Column | Definition |
|---|---|
| `invariant_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `title` | CGP-001 register field reserved for later authorized detail. |
| `statement` | CGP-001 register field reserved for later authorized detail. |
| `protected_outcome` | CGP-001 register field reserved for later authorized detail. |
| `risk_addressed` | CGP-001 register field reserved for later authorized detail. |
| `verification_methods` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `version` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_QUESTION_REGISTER.csv

| Column | Definition |
|---|---|
| `question_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `question_category` | CGP-001 register field reserved for later authorized detail. |
| `question` | CGP-001 register field reserved for later authorized detail. |
| `required` | CGP-001 register field reserved for later authorized detail. |
| `answer_status` | CGP-001 register field reserved for later authorized detail. |
| `answer_location` | CGP-001 register field reserved for later authorized detail. |
| `source_support` | CGP-001 register field reserved for later authorized detail. |
| `evidence_reference` | CGP-001 register field reserved for later authorized detail. |
| `reviewer_disposition` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_DEPENDENCY_REGISTER.csv

| Column | Definition |
|---|---|
| `dependency_id` | CGP-001 register field reserved for later authorized detail. |
| `downstream_guide` | CGP-001 register field reserved for later authorized detail. |
| `upstream_guide` | CGP-001 register field reserved for later authorized detail. |
| `upstream_control` | CGP-001 register field reserved for later authorized detail. |
| `minimum_version` | CGP-001 register field reserved for later authorized detail. |
| `maximum_version` | CGP-001 register field reserved for later authorized detail. |
| `dependency_type` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `impact_if_unavailable` | CGP-001 register field reserved for later authorized detail. |
| `last_verified` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_VERSION_REGISTER.csv

| Column | Definition |
|---|---|
| `guide_id` | Canonical guide identifier when applicable. |
| `version` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `effective_date` | CGP-001 register field reserved for later authorized detail. |
| `repository_path` | CGP-001 register field reserved for later authorized detail. |
| `package_id` | CGP-001 register field reserved for later authorized detail. |
| `checksum` | SHA-256 checksum or documented self-reference marker. |
| `approval_record` | CGP-001 register field reserved for later authorized detail. |
| `supersedes` | CGP-001 register field reserved for later authorized detail. |
| `superseded_by` | CGP-001 register field reserved for later authorized detail. |
| `compatibility_notes` | CGP-001 register field reserved for later authorized detail. |

## ATLAS_TO_CODE_TRACEABILITY_REGISTER.csv

| Column | Definition |
|---|---|
| `trace_id` | CGP-001 register field reserved for later authorized detail. |
| `atlas_id` | CGP-001 register field reserved for later authorized detail. |
| `atlas_version` | CGP-001 register field reserved for later authorized detail. |
| `atlas_task_id` | CGP-001 register field reserved for later authorized detail. |
| `governing_authority` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `control_ids` | CGP-001 register field reserved for later authorized detail. |
| `implementation_profile` | CGP-001 register field reserved for later authorized detail. |
| `expected_components` | CGP-001 register field reserved for later authorized detail. |
| `required_tests` | CGP-001 register field reserved for later authorized detail. |
| `required_evidence` | CGP-001 register field reserved for later authorized detail. |
| `retained_gates` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CONTROL_TO_VERIFICATION_REGISTER.csv

| Column | Definition |
|---|---|
| `verification_id` | CGP-001 register field reserved for later authorized detail. |
| `control_id` | CGP-001 register field reserved for later authorized detail. |
| `invariant_id` | CGP-001 register field reserved for later authorized detail. |
| `verification_type` | CGP-001 register field reserved for later authorized detail. |
| `test_or_inspection_id` | CGP-001 register field reserved for later authorized detail. |
| `environment` | CGP-001 register field reserved for later authorized detail. |
| `positive_or_negative` | CGP-001 register field reserved for later authorized detail. |
| `evidence_grade` | CGP-001 register field reserved for later authorized detail. |
| `independent_execution_required` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `evidence_path` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CONTROL_TO_REPOSITORY_REGISTER.csv

| Column | Definition |
|---|---|
| `mapping_id` | CGP-001 register field reserved for later authorized detail. |
| `control_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `repository_component_type` | CGP-001 register field reserved for later authorized detail. |
| `repository_path_or_planned_component` | CGP-001 register field reserved for later authorized detail. |
| `mapping_status` | CGP-001 register field reserved for later authorized detail. |
| `implementation_commit` | CGP-001 register field reserved for later authorized detail. |
| `test_path` | CGP-001 register field reserved for later authorized detail. |
| `owner` | Responsible person or role, if assigned. |
| `last_verified` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## GUIDE_REVIEW_FINDING_REGISTER.csv

| Column | Definition |
|---|---|
| `finding_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `review_type` | CGP-001 register field reserved for later authorized detail. |
| `severity` | CGP-001 register field reserved for later authorized detail. |
| `title` | CGP-001 register field reserved for later authorized detail. |
| `description` | CGP-001 register field reserved for later authorized detail. |
| `evidence` | CGP-001 register field reserved for later authorized detail. |
| `affected_controls` | CGP-001 register field reserved for later authorized detail. |
| `affected_atlas_tasks` | CGP-001 register field reserved for later authorized detail. |
| `owner` | Responsible person or role, if assigned. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `required_action` | CGP-001 register field reserved for later authorized detail. |
| `disposition_authority` | CGP-001 register field reserved for later authorized detail. |
| `closure_evidence` | CGP-001 register field reserved for later authorized detail. |
| `closed_date` | CGP-001 register field reserved for later authorized detail. |
| `retained_reason` | CGP-001 register field reserved for later authorized detail. |

## OPEN_DECISION_REGISTER.csv

| Column | Definition |
|---|---|
| `decision_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `question` | CGP-001 register field reserved for later authorized detail. |
| `why_existing_authority_is_insufficient` | CGP-001 register field reserved for later authorized detail. |
| `affected_controls` | CGP-001 register field reserved for later authorized detail. |
| `affected_atlas_tasks` | CGP-001 register field reserved for later authorized detail. |
| `options` | CGP-001 register field reserved for later authorized detail. |
| `recommendation` | CGP-001 register field reserved for later authorized detail. |
| `required_authority` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `decision` | CGP-001 register field reserved for later authorized detail. |
| `decision_date` | CGP-001 register field reserved for later authorized detail. |
| `decision_record_path` | CGP-001 register field reserved for later authorized detail. |
| `founder_disposition` | Founder disposition status applied to the decision record. |
| `affected_guides` | Guide IDs affected by the decision disposition. |
| `required_later_action` | Later drafting, implementation, activation, or review action required after disposition. |
| `disposition_notes` | Notes preserving history and explaining the disposition treatment. |

## IMPLEMENTATION_EXCEPTION_REGISTER.csv

| Column | Definition |
|---|---|
| `exception_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `affected_controls` | CGP-001 register field reserved for later authorized detail. |
| `reason` | CGP-001 register field reserved for later authorized detail. |
| `risk` | CGP-001 register field reserved for later authorized detail. |
| `alternative` | CGP-001 register field reserved for later authorized detail. |
| `compensating_controls` | CGP-001 register field reserved for later authorized detail. |
| `owner` | Responsible person or role, if assigned. |
| `approval_authority` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `approved_date` | CGP-001 register field reserved for later authorized detail. |
| `expiration_date` | CGP-001 register field reserved for later authorized detail. |
| `remediation` | CGP-001 register field reserved for later authorized detail. |
| `evidence_path` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## IMPLEMENTATION_EVIDENCE_REGISTER.csv

| Column | Definition |
|---|---|
| `evidence_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `atlas_task_id` | CGP-001 register field reserved for later authorized detail. |
| `control_ids` | CGP-001 register field reserved for later authorized detail. |
| `evidence_type` | CGP-001 register field reserved for later authorized detail. |
| `evidence_grade` | CGP-001 register field reserved for later authorized detail. |
| `environment` | CGP-001 register field reserved for later authorized detail. |
| `artifact_path` | CGP-001 register field reserved for later authorized detail. |
| `commit_sha` | Result commit recorded after commit when available. |
| `ci_run` | CGP-001 register field reserved for later authorized detail. |
| `reviewer` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `created_date` | CGP-001 register field reserved for later authorized detail. |
| `last_reproduced` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## GUIDE_SUPERSESSION_REGISTER.csv

| Column | Definition |
|---|---|
| `supersession_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `old_version` | CGP-001 register field reserved for later authorized detail. |
| `new_version` | CGP-001 register field reserved for later authorized detail. |
| `effective_date` | CGP-001 register field reserved for later authorized detail. |
| `reason` | CGP-001 register field reserved for later authorized detail. |
| `affected_controls` | CGP-001 register field reserved for later authorized detail. |
| `affected_atlas_tasks` | CGP-001 register field reserved for later authorized detail. |
| `compatibility_required` | CGP-001 register field reserved for later authorized detail. |
| `approval_record` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `notes` | Non-substantive notes. |

## CODE_GUIDE_SESSION_RECEIPT_REGISTER.csv

| Column | Definition |
|---|---|
| `session_id` | CGP-001 register field reserved for later authorized detail. |
| `prompt_id` | CGP-001 register field reserved for later authorized detail. |
| `execution_id` | CGP-001 register field reserved for later authorized detail. |
| `guide_id` | Canonical guide identifier when applicable. |
| `work_package` | CGP-001 register field reserved for later authorized detail. |
| `start_date` | CGP-001 register field reserved for later authorized detail. |
| `end_date` | CGP-001 register field reserved for later authorized detail. |
| `baseline_commit` | CGP-001 register field reserved for later authorized detail. |
| `result_commit` | CGP-001 register field reserved for later authorized detail. |
| `branch` | CGP-001 register field reserved for later authorized detail. |
| `status` | CGP-001 register field reserved for later authorized detail. |
| `receipt_path` | Repository path to the controlling receipt. |
| `artifacts_registered` | CGP-001 register field reserved for later authorized detail. |
| `findings_registered` | CGP-001 register field reserved for later authorized detail. |
| `decisions_registered` | CGP-001 register field reserved for later authorized detail. |
| `next_prompt` | Next prompt or drafting prompt expected for the row. |
| `remote_verified` | Remote branch verification state. |
| `notes` | Non-substantive notes. |

Additional columns are not authorized unless added here with an explicit definition and controlled value reference.
## CGP-002 Additional Register Columns

CGP-002 adds the following columns while preserving all CGP-001 minimum column contracts.

| Register | Column | Definition |
|---|---|---|
| `CODE_GUIDE_CONTROL_REGISTER.csv` | `failure_effect` | Non-policy description of validation failure effect for a future control. |
| `CODE_GUIDE_CONTROL_REGISTER.csv` | `supersedes` | Prior control ID if this future control supersedes one. |
| `CODE_GUIDE_CONTROL_REGISTER.csv` | `superseded_by` | Successor control ID if this future control is superseded. |
| `CODE_GUIDE_CONTROL_REGISTER.csv` | `supersession_compatibility` | Compatibility treatment required when a superseded control remains referenced. |
| `CODE_GUIDE_INVARIANT_REGISTER.csv` | `governing_sources` | Source or authority references for an invariant. |
| `CODE_GUIDE_INVARIANT_REGISTER.csv` | `affected_resources_or_actors` | Resource or actor categories affected by an invariant, without creating product policy. |
| `CODE_GUIDE_INVARIANT_REGISTER.csv` | `required_evidence` | Controlled evidence grade required for future validation. |
| `CODE_GUIDE_INVARIANT_REGISTER.csv` | `assurance_class` | Controlled assurance class. |
| `CODE_GUIDE_INVARIANT_REGISTER.csv` | `failure_severity` | Controlled finding severity for invariant failure. |
| `CODE_GUIDE_QUESTION_REGISTER.csv` | `rationale` | Rationale required for not-applicable or deferred question responses. |
| `CODE_GUIDE_QUESTION_REGISTER.csv` | `decision_reference` | Decision reference required for blocked questions. |
| `CODE_GUIDE_DEPENDENCY_REGISTER.csv` | `compatibility_treatment` | Required treatment when a dependency references superseded material. |
| `CONTROL_TO_VERIFICATION_REGISTER.csv` | `retained_gates` | Gates retained after validation. |
| `CONTROL_TO_REPOSITORY_REGISTER.csv` | `activation_boundary` | Boundary preventing repository mapping from implying activation. |
| `IMPLEMENTATION_EVIDENCE_REGISTER.csv` | `result` | Evidence result or outcome. |
| `IMPLEMENTATION_EVIDENCE_REGISTER.csv` | `retained_gates` | Gates retained by an evidence record. |

## CGP-003 Source Accession Registers

CGP-003 adds the following source-accession registers without creating substantive guide controls.

| Register | Purpose |
|---|---|
| `source-accession/MASTER_CODE_GUIDE_SOURCE_REGISTER.csv` | Master inventory of repository sources that may govern, constrain, inform, or evidence future Code Guides. |
| `source-accession/MASTER_CODE_GUIDE_SOURCE_TO_GUIDE_MAP.csv` | Initial source-to-guide coverage map using `MANDATORY`, `SUPPORTING`, `HISTORICAL`, `POTENTIALLY_CONFLICTING`, or `PENDING_REVIEW`. |
| `source-accession/MASTER_CODE_GUIDE_SOURCE_GAP_REGISTER.csv` | Retained source gaps, risk, next action, responsible authority, drafting treatment, and adoption/activation effect. |
| `source-accession/MASTER_CODE_GUIDE_SOURCE_CONFLICT_REGISTER.csv` | Source conflicts that must remain visible until later authority resolves them. |
| `source-accession/MASTER_CODE_GUIDE_SOURCE_SUPERSESSION_REGISTER.csv` | Source predecessor/successor treatment for candidate, adoption, lock, historical, and program-sequence source families. |
| `registers/CODE_GUIDE_FINDING_REGISTER.csv` | CGP-level source assurance findings by severity. |
| `registers/CODE_GUIDE_OPEN_DECISION_REGISTER.csv` | CGP-level decision requests created because existing authority is insufficient. |

The corresponding schemas are `SOURCE_RECORD_SCHEMA.json`, `SOURCE_TO_GUIDE_MAP_SCHEMA.json`, `SOURCE_GAP_SCHEMA.json`, `SOURCE_CONFLICT_SCHEMA.json`, and `SOURCE_SUPERSESSION_SCHEMA.json`.
