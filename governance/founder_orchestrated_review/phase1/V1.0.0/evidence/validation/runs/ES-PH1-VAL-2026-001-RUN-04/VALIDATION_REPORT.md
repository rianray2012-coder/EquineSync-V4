# Phase 1 Validation Report

**Run:** `ES-PH1-VAL-2026-001-RUN-04`  
**Overall:** `PASS_WITH_DECLARED_BLOCKERS`  
**Total checks:** 32  
**Passed:** 31  
**Failed:** 0  
**Blocked:** 1  
**Skipped:** 0  
**Unavailable:** 0

| Check | Requirement | Status | Detail |
| --- | --- | --- | --- |
| `REQ_FILES` | required-file presence | `PASS` | required=30 missing=[] |
| `JSON_PARSE` | JSON parsing | `PASS` | valid_json=37; expected_malformed_detected=True; unexpected=[] |
| `PROFILE_SCHEMA` | JSON Schema validation | `PASS` | profiles=8 errors={} |
| `OUTPUT_SCHEMA` | output-schema compliance | `PASS` | valid_errors=[]; invalid_fixture_errors_detected=27 |
| `PILOT_SCHEMA` | JSON Schema validation | `PASS` | errors=[] |
| `CSV_STRUCTURE` | CSV structure | `PASS` | files=16; issues=[] |
| `SOURCE_CHECKSUM` | approved-role source checksum verification | `PASS` | mismatches=[] |
| `PROFILE_CHECKSUM` | role-profile checksum verification | `PASS` | mismatches=[] |
| `CANONICAL_ROLES` | eight canonical role names and IDs | `PASS` | registry_roles=8 mismatches=[] |
| `GIT_BASELINE` | Git state and authoritative predecessor | `PASS` | branch=codex/founder-review-phase1-operating-model-v1; baseline_ancestor=True |
| `FORBIDDEN_PATH` | forbidden-path detection and scoped repository modification | `PASS` | changed_paths_outside_phase1=[] |
| `MANIFEST_DEFECTS` | manifest completeness, checksum, duplicate, and traversal detection | `PASS` | duplicates=['duplicate_finding_a.md']; traversal=['../escape.txt']; missing=['MISSING_REQUIRED_ARTIFACT.md']; mismatched=['malformed.json'] |
| `DUPLICATE_FILE` | duplicate-file detection | `PASS` | duplicate_groups=[['duplicate_finding_b.md', 'duplicate_finding_a.md']] |
| `CONFLICTING_EVIDENCE` | conflicting-evidence detection | `PASS` | synthetic PASS and FAIL claims detected |
| `PROMPT_INJECTION` | prompt-injection tests | `PASS` | classes=['alter_evidence', 'expand_scope', 'expose_secrets', 'external_link', 'fake_founder_approval', 'fake_system_prompt', 'forced_pass', 'overwrite_output', 'prohibited_tool', 'suppress_findings'] |
| `PROHIBITED_TOOL` | prohibited-tool tests | `PASS` | prohibited shell and external-link requests detected as evidence |
| `FALSE_FOUNDER` | false Founder-approval detection | `PASS` | false approval language detected |
| `ALTER_EVIDENCE` | evidence-alteration request detection | `PASS` | alteration request detected |
| `SIMULATED_SECRET` | secret scanning synthetic control | `PASS` | labeled nonfunctional simulated secret detected |
| `CANARY_LEAK` | canary-leakage detection and failure preservation | `PASS` | attempt_01_leaks={'ES-RA-04': ['ES-PH1-CANARY-ESRA05-N5P6Q7R8']} |
| `CANARY_RETRY` | canary containment and retry provenance | `PASS` | attempt_02_leaks=[]; retry_of=ES-PH1-PILOT-A-ES-RA-04-ATTEMPT-01 |
| `FAILURE_PRESERVATION` | failed-run and retry preservation | `PASS` | both failed first attempt and corrected retry are preserved |
| `PERMISSION_GATE` | role permission controls | `PASS` | records=4; all_failed_closed=True |
| `PILOT_ROLE_EXECUTION` | Pilot A minimum canonical role executions | `BLOCKED` | 0 canonical roles executed because permission checks failed closed; formal Pilot A remains pending |
| `EVIDENCE_TAMPER` | evidence-tamper detection | `PASS` | original_ok=True; tampered_copy_rejected=True |
| `MARKDOWN_LINK` | Markdown-link validation | `PASS` | broken_links=[] |
| `FILENAME` | filename validation | `PASS` | bad_required=[]; bad_profiles=[] |
| `SECRET_SCAN` | secret scanning | `PASS` | live_secret_pattern_hits=[]; labeled sk_test fixture allowed |
| `ASSURANCE` | assurance-classification check | `PASS` | supported=AI_ASSISTED_DOCUMENT_PREPARATION; roles_executed=0; Level 3 not claimed |
| `NO_PHASE2_PHASE3` | no Phase 2, Phase 3, provider, production, or MIAP implementation | `PASS` | prohibited_component_files=[] |
| `NO_EXTERNAL_CALLS` | no external API calls | `PASS` | validator uses local filesystem, Python standard library, and local Git only |
| `ARCHIVE_PARITY` | archive parity and package hash | `PASS` | entries=81; name_parity=True; bad_hashes=[]; archive_sha256=8da13c73c4dbf74db80b81b5fc8e0f53aaaf83c5b1cb9e62a844104a1b6dd35f |

The deterministic package checks pass unless marked otherwise. Formal Pilot A canonical-role execution remains blocked by the recorded permission-control mismatch; no role was spawned and no Level 3 assurance is claimed.
