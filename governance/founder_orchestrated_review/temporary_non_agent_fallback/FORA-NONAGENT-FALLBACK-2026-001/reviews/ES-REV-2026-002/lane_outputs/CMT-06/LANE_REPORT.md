# CMT-06 Machine Validation Lane Report

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## Disposition

- Lane: `CMT-06`
- Review cycle: `ES-REV-2026-002`
- Directive: `ES-FORA-DIR-CMT-IDENTITY-RELATIONSHIPS-REVIEW-V1.0`
- Lane role: generic controlled Codex thread performing deterministic non-application machine validation
- Lane result: `CMT06_MACHINE_VALIDATION_COMPLETE_WITH_OPEN_P1_AND_P2_OBSERVATIONS`
- Frozen-input integrity: `PASS`
- Input-integrity blocker triggered: `FALSE`
- Machine-validation findings: `P0=0`, `P1=4`, `P2=3`
- Custom agents activated or executed: `0`
- Frozen-input modifications: `0`
- Application code, tests, databases, providers, product workflows, or network used: `0`

This is a completed lane report, not a Founder decision, ratification, implementation authorization, execution authorization, PR, merge, tag, release, deployment, production-readiness statement, enrollment-readiness statement, or F-0001 closure. This lane does not return the directive's final review disposition; synthesis remains segregated to `CMT-08` and the coordinator.

## Runtime and thread provenance

- Current controlled thread ID: `019f810f-9602-7db0-8f92-e7dab25330d0`
- Delegating source thread ID: `019f8104-9235-7f03-8a3e-c68d4b199e09`
- Runtime: Codex desktop generic controlled thread; exact backend model identifier was not exposed through the runtime environment
- Host: `Darwin 25.5.0 arm64`; macOS `26.5.2`
- Python: `3.14.6`
- Info-ZIP: `6.00`
- SHA utility version observed: `6.02`; deterministic validation hashes were computed with Python `hashlib.sha256`
- Formal instrumented validation start UTC: `2026-07-20T19:48:05Z`
- Deterministic validation completion UTC: `2026-07-20T19:53:23Z`
- Artifact self-audit completion UTC: `2026-07-20T19:57:31Z`
- Review-plan start UTC: `2026-07-20T19:42:33Z`
- Review branch recorded by the controlling plan: `codex/identity-relationships-controlled-thread-review-v1`
- Base commit recorded by the controlling plan: `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`
- Git verification limitation: branch and base-commit values were read from the controlling plan; this lane did not mutate Git or use network access.

## Inputs and custody result

Frozen handoff directory:

`/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/frozen_review_object/EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Handoff_V1_0_0`

Read-only expanded materials:

`/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials`

Original frozen handoff ZIP used only for read-only byte comparison:

`/Users/rianray/Downloads/EquineSync_Identity_Relationships_Controlled_Multi_Thread_Review_Handoff_V1_0_0.zip`

- Original handoff ZIP bytes: `301007`
- Original handoff ZIP SHA-256: `91cdb1c24f13940814035036c2c76c7cec415945337edbf3778e2a77c4a140f6`
- Original ZIP entries: `15/15` CRC-valid, safe, unique, unencrypted, and byte-identical to the frozen handoff directory
- Frozen handoff inventory: `15` files, `336992` bytes, deterministic inventory SHA-256 `756f78dc966e42c62be72cd6d06e55a8c73fb88aedb17fd7c28b2a42a85e17ba`
- Expanded-material inventory: `140` files, `811571` bytes, deterministic inventory SHA-256 `e85e037e518aac4f9f8a1fbd416cb7fdc58d983b09c08f50235c8f2a4d371551`
- Writable input files found: `0`
- Root manifest payload entries: `13/13` exact path, byte-count, and SHA-256 matches
- Root checksum entries: `14/14` exact matches, including `PACKAGE_MANIFEST.json`
- Embedded ZIPs: `5/5` CRC-valid; `140/140` entries byte-identical to expanded packages; no duplicate entry, traversal path, symlink, or encrypted entry
- Embedded package manifests: `130/130` payload entries exact
- Embedded package checksum lists: `130/130` payload hashes exact

The inner `SHA256SUMS.txt` files intentionally cover package payload files but not the package manifest or checksum file itself. The frozen handoff compensates for this within the reviewed custody chain by hashing each complete embedded ZIP at the root level. Standalone re-use of an extracted inner package would require retaining the outer ZIP/hash evidence or adding a separately anchored manifest hash.

## Machine-validation summary

| Area | Result | Evidence |
|---|---|---|
| CSV parsing and required columns | PASS | `48/48` CSVs parsed strictly; `841/841` data rows had correct width; no blank or duplicate header; expected header sets present |
| JSON parsing | PASS | `15/15` JSON files parsed; no duplicate object keys |
| Core identifier sequences | PASS | Identity `12` decisions and `7` ADRs; Relationships `16` decisions and `7` ADRs; all expected sequences complete |
| Duplicate identifiers | PASS_WITH_OBSERVATION | `768` identifiers across `44` ID-bearing CSVs had no blank or within-file duplicate; repeated cross-package IDs were expected lineage reuse; three repeated ADR IDs had title drift |
| Human-machine row parity | PASS | Identity `238/238` mapped rows exact; Relationships `360/360` rows exact |
| Validation-report parity | PASS | Human and JSON validation reports matched exactly for `8/8`, `28/28`, and `12/12` checks (`48/48` total) |
| Reference validity | PASS | All extracted requirement, acceptance, source, decision, ADR, traceability, golden-path, adversarial, and source-reconciliation ID references resolved to their target registries |
| Formal ADR files | PASS | Identity `7/7`; Relationships controlled sequence `7/7`; pre-ratification copy `7/7`; filename/header/register ID-title parity exact within each stage |
| Expected decision/ADR counts | PASS | `28` unique Founder decision IDs and `14` unique formal ADR IDs across the two domains |
| MIAP terminology token check | PASS | `58` `MIAP` occurrences; `0` `MAIP` occurrences |
| Source reconciliation | OPEN_P1 | Identity SHA coverage `4/12`; Relationships SHA coverage `8/16`; gaps are explicitly registered upstream |
| Cross-domain contracts | OPEN_P1 | `0/12` rows are final/aligned; all `12/12` carry a blocking dependency and are proposed, partial, or blocked |
| Pre-ratification current-status machine parity | OPEN_P1 | Current-status artifacts state approval while preserved historical machine/register artifacts retain pending statuses without an explicit machine-readable precedence map |

## Findings

### `CMT06-P1-001` — Pre-ratification lifecycle status is not single-valued for machine consumers

- Classification: `AMBIGUOUS_REQUIRES_REMEDIATION`
- Severity: `P1`
- Evidence:
  - `PRE_RATIFICATION_STATUS.json` states `pia_status = FOUNDER_APPROVED_DESIGN_NOT_IMPLEMENTATION_AUTHORIZED`.
  - `FOUNDER_DECISION_TO_FORMAL_ADR_TRACEABILITY.csv` states `FOUNDER_APPROVED_AS_RECOMMENDED` for `16/16` decisions.
  - The bundled `PIA_RELATIONSHIPS_DELEGATED_AUTHORITY_V1_1_0.md` still states `REVISED_CANDIDATE_PENDING_FOUNDER_DECISIONS_AND_STRUCTURED_REVIEW`.
  - The bundled `FOUNDER_DECISION_REGISTER.csv` still marks `16/16` decisions `PENDING`.
  - The bundled `ADR_RECOMMENDATIONS_MACHINE_READABLE.json` retains package and per-ADR `PENDING_FOUNDER_APPROVAL` statuses for `7/7` recommendations.
- Interpretation boundary: the stale-status files are byte-identical preserved artifacts from earlier packages, so this is not corruption. The pre-ratification package lacks a single machine-readable precedence/provenance map that tells a consumer which status fields are historical and which are current.
- Bounded remediation recommendation: in a successor package, add an explicit machine-readable lifecycle/preference map or a current-state status overlay while retaining immutable source hashes. This lane did not edit the frozen package.

### `CMT06-P1-002` — Identity source reconciliation remains incomplete

- Classification: `SOURCE_GAP`
- Severity: `P1`
- Evidence: `4/12` reconciliation rows contain valid SHA-256; `8/12` are blank; `10/12` statuses are pending, partial, or unresolved; `5/12` paths are unresolved or local/controlled placeholders.
- Upstream alignment: confirms the package's existing `IDENTITY-P1-004`; it is not a newly created implementation finding.

### `CMT06-P1-003` — Relationships source reconciliation remains incomplete

- Classification: `SOURCE_GAP`
- Severity: `P1`
- Evidence: `8/16` rows contain valid SHA-256; `8/16` are blank; `12/16` statuses are pending, partial, or unresolved; `6/16` paths are unresolved or Founder-provided/unreconciled placeholders. Controlled-sequence and pre-ratification registers are byte-identical.
- Upstream alignment: confirms the existing `REL-CS-P1-001`, `003` through `007` source findings.

### `CMT06-P1-004` — Cross-domain contract completion denominator remains open

- Classification: `AMBIGUOUS_REQUIRES_REMEDIATION`
- Severity: `P1`
- Evidence: `12/12` contract rows have blocking dependencies; status distribution is `PROPOSED=2`, `PARTIALLY_ALIGNED=1`, `BLOCKED_BY_AUTHORIZATION_PIA=2`, `BLOCKED_BY_SOURCE=5`, `BLOCKED_BY_SOURCE_RECONCILIATION=1`, `BLOCKED_BY_MIAP_STAGE_3=1`; finalized/aligned rows are `0/12`.
- Upstream alignment: this confirms supplied dependency/source blockers and does not authorize out-of-scope PIA drafting.

### `CMT06-P2-001` through `CMT06-P2-003` — Cross-stage Relationships ADR title drift

- Classification: `TERMINOLOGY_DRIFT`
- Severity: `P2` each
- `ADR-REL-003`: candidate PIA register uses “Delegation Grant…”; recommendation/formal stages use “Delegation Grants…”.
- `ADR-REL-004`: candidate PIA register uses “Evidence, Verification, Dispute, Restriction…”; recommendation/formal stages use “Evidence, Claim-Specific Verification, Disputes, Restrictions…”.
- `ADR-REL-006`: candidate PIA register uses “Offline Relationship Proposals…Conflict Resolution…”; recommendation/formal stages use “Offline Proposals…Conflict Detection…”.
- All stage-local markdown/register comparisons pass and all decision mappings resolve. The observation is limited to cross-stage canonical-title normalization; no semantic conclusion was made by this machine lane.

## Reference and coverage highlights

- Identity acceptance criteria directly reference `30/48` requirements; every acceptance reference is valid. This is a direct-reference denominator, not proof that the remaining requirements require distinct acceptance rows.
- Identity tests cover `30/30` acceptance criteria.
- Relationships acceptance criteria directly reference `40/68` requirements; every acceptance reference is valid.
- Relationships tests cover `40/40` acceptance criteria.
- Identity requirement-to-source references: `96/96` occurrences valid, covering `16/17` registered source IDs.
- Relationships requirement-to-source references: `124/124` occurrences valid, covering `13/16` registered source IDs.
- Identity formal ADR mappings: `21/21` decision-reference occurrences valid, covering `11/12` Founder decisions.
- Relationships recommendation, controlled-formal, and pre-ratification conformance mappings: `35/35` reference occurrences valid and all `16/16` Founder decisions covered.
- Pre-ratification Founder-decision traceability covers `16/16` decisions and all `7/7` formal ADRs.
- Golden-path ADR coverage and adversarial controlling-ADR references both resolve to all `7/7` Relationships ADRs.

Coverage ratios derived from prose range selectors in engineering work-package registers are not treated as exact denominators. The lane validated every explicit identifier and range endpoint, but entries such as `All first-user enrollment requirements` require a controlled semantic definition before a machine can expand them without assumption.

## Exact commands and procedures

All reads were non-mutating. Output creation used `apply_patch` only.

1. Prompt completeness: `wc -l <CMT-06_PROMPT.md>` followed by `sed -n '1,260p' <CMT-06_PROMPT.md>`; observed `13` lines and read all lines.
2. Controlled context: `sed -n` reads of `START_HERE.md`, `PACKAGE_MANIFEST.json`, `SHA256SUMS.txt`, both context files, the directive, and the controlled review plan.
3. Inventory: `find <frozen-root> -type f -print | sort` and `find <review-materials> -type f -print | sort`.
4. Runtime capture: `date -u +%Y-%m-%dT%H:%M:%SZ`; selected `printenv` keys; `uname -mrs`; `sw_vers -productVersion`; `python3 --version`; `shasum --version`; `unzip -v`.
5. Hash algorithm: for each file, `hashlib.sha256(path.read_bytes()).hexdigest()`; deterministic inventory hash is SHA-256 over sorted lines formatted `<file-sha256><two spaces><POSIX-relative-path><LF>`.
6. ZIP procedure: Python `zipfile.ZipFile`; run `testzip()`; reject duplicate names, absolute paths, `..` components, symlinks, encrypted entries, missing paths, extra paths, and byte differences; compare each entry's bytes with its expanded counterpart.
7. Manifest procedure: parse JSON; require each declared path, byte count, and SHA-256 to match the filesystem; compare declared path set with actual payload set.
8. Checksum procedure: split every nonblank checksum line on two spaces; require lowercase 64-hex SHA-256 and exact match; compare checksum path set with its declared scope.
9. JSON procedure: `json.loads(..., object_pairs_hook=duplicate_key_detector)` using UTF-8 with optional BOM; check required top-level fields used by companion human/register parity tests.
10. CSV procedure: `csv.reader(..., strict=True)` and `csv.DictReader`; require expected header list, no blank/duplicate header, constant row width, no blank data row, and valid required identifier cells.
11. ID/reference procedure: compare core registries with explicitly generated sequential sets; extract controlled IDs with anchored regular expressions; verify every extracted target exists; compare required set denominators; detect within-file duplicates with `collections.Counter`.
12. Human-machine parity: use explicit field-name maps for `12` Identity JSON arrays and exact dictionary equality for `14` Relationships JSON arrays; compare ADR ID/title/status/mapping fields and human/JSON validation-report check lists.
13. Frozen-permission check: `find <input-root> -type f -perm +0222 -print | wc -l`; observed zero writable files in both roots.
14. Terminology check: case-bounded scan for `MIAP` and `MAIP`; observed `MIAP=58`, `MAIP=0`.

The complete row-level results and denominator evidence are in `MACHINE_VALIDATION_RESULTS.csv` and `REFERENCE_AND_COVERAGE_RESULTS.csv`; execution accountability is in `WORK_COMPLETENESS_LEDGER.csv`.

## Limitations

- No published JSON Schema or CSV schema files were supplied. Validation therefore covers syntax, explicit required headers/keys, companion-artifact parity, reference integrity, and controlled denominators; it does not claim external schema certification.
- No network, repository-source re-fetch, provider, database, application runtime, test suite, or product workflow was permitted or used.
- Source hashes absent from supplied reconciliation registers were not invented or filled from out-of-scope repository paths.
- Human prose semantics, legal sufficiency, and ADR ratification merit are outside this machine lane.
- Git branch/base values are plan provenance, not a Git authority determination by this lane.
- The exact backend model identifier was not runtime-visible; this limitation is explicit rather than inferred.

## Self-audit

- Both required labels appear in every output file: `PASS`.
- Current thread and delegation provenance recorded: `PASS`.
- All five required filenames created in the assigned lane only: `PASS`.
- CSV outputs strict-parse after creation: `PASS`.
- JSON manifest strict-parses after creation: `PASS`.
- Frozen handoff and expanded-material inventory hashes unchanged after output creation: `PASS`.
- Files written outside the assigned CMT-06 lane: `0`.
- Network calls: `0`.
- Application/product execution: `0`.
- Git mutations: `0`.

## Completion attestation

The bounded CMT-06 machine-validation work is complete to the extent permitted by the supplied frozen inputs and lane restrictions. Completion of this lane does not close its reported P1/P2 observations and does not make the reviewed ADRs ready for ratification. No Founder action, ratification, implementation, execution, PR, merge, tag, release, deployment, production action, enrollment action, or F-0001 closure was performed or authorized.

## Output hashes

Final SHA-256 and byte counts for the three CSV outputs are recorded here after finalization; the final `LANE_REPORT.md` hash and all four non-manifest output hashes are recorded in `OUTPUT_MANIFEST.json`. A manifest cannot embed its own final hash without recursion; its SHA-256 is computed and reported externally after the final self-audit.

- `MACHINE_VALIDATION_RESULTS.csv`: `11130` bytes; SHA-256 `31e10a098059551acab5bcacdc4bc3517d1c140afe7eec500ee1f10118665f84`
- `REFERENCE_AND_COVERAGE_RESULTS.csv`: `8529` bytes; SHA-256 `0fb4f6459239aa98f7fbc08d754334794db96ea5efe4f519b9608ec2af3d3717`
- `WORK_COMPLETENESS_LEDGER.csv`: `8043` bytes; SHA-256 `ee4798ed7e2ad1560043726849e44b6677493d8f0fcb4915fb48b466de852edd`
