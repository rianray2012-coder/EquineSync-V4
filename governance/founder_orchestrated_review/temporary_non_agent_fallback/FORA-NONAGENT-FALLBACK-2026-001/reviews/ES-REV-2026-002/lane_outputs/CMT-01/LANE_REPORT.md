# CMT-01 Evidence Custody and Input Integrity Report

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## 1. Run identity

- Review cycle: `ES-REV-2026-002`
- Lane: `CMT-01`
- Role: generic controlled Codex thread performing Evidence Custody and Input Integrity
- Agent-run identifier: `CMT-01-ES-REV-2026-002-RUN-01`
- Custom-agent identity: none loaded or claimed
- Review package: `ES-IDENTITY-RELATIONSHIPS-CONTROLLED-MULTI-THREAD-REVIEW-HANDOFF-V1.0.0`
- Directive: `ES-FORA-DIR-CMT-IDENTITY-RELATIONSHIPS-REVIEW-V1.0`
- Authorization: `FORA-NONAGENT-FALLBACK-2026-001`
- Repository base commit: `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`
- Review branch observed: `codex/identity-relationships-controlled-thread-review-v1`
- UTC start: `2026-07-20T19:46:13Z`
- UTC evidence-procedure end: `2026-07-20T20:01:02Z`

## 2. Runtime and thread provenance

- Thread ID: `019f810e-dfc4-7073-8fe0-16d3296c8b12`
- Parent/coordinator thread ID: `019f8104-9235-7f03-8a3e-c68d4b199e09`
- Model provenance exposed to this thread: GPT-5 family; exact model build not exposed
- Codex runtime: `codex-cli 0.144.6`
- Host: `macOS 26.5.2 (25F84)`, `arm64`
- Shell: `/bin/zsh`
- Effective host permission profile supplied to this thread: `danger-full-access`, approval policy `never`
- Path isolation: procedural, not technically enforced by the host sandbox
- Network use: zero
- Connector use: zero
- Application execution: zero
- Git mutation: zero

## 3. Authorization and scope

Authorized scope was limited to frozen-input custody, bytes, SHA-256 values, ZIP integrity, package manifests, expected repository objects, authority records, lifecycle records, source registers, and evidence inventory. The lane did not review ADR substance or make a semantic ratification recommendation.

Authorized reads were the frozen handoff, read-only expanded package files, and repository authority records at the base commit. Authorized writes were limited to the CMT-01 lane-output directory. Implementation, product execution, PR, merge, tag, release, deployment, F-0001 closure, and Founder disposition were not performed.

## 4. Package identity and frozen-input results

The external handoff ZIP SHA-256 is `91cdb1c24f13940814035036c2c76c7cec415945337edbf3778e2a77c4a140f6`, matching the review plan. ZIP compressed-data testing passed.

Deterministic byte results:

- Expanded handoff: `15/15` files byte-equal to the external ZIP; `14/14` checksum entries passed; `13/13` manifest entries matched declared bytes and SHA-256.
- Embedded packages: `5/5` ZIP tests passed.
- Expanded review materials: `140/140` files byte-equal to their embedded ZIP entries; zero missing and zero mismatched files.
- Internal package checksums: `130/130` passed.
- Internal package manifests: `130/130` entries matched; package denominators were `38 + 12 + 24 + 24 + 32`.
- JSON: `16/16` parsed.
- CSV: `48/48` parsed, covering `841` data rows.
- Post-permission-update rehash: zero byte drift across the external ZIP, 15 expanded-handoff files, and 140 expanded-package files.

These results establish observed byte identity at the recorded check times. They do not establish ongoing immutability because the containing directories remained owner-writable.

## 5. Repository authority verification

- Global Governance V1.0 commit `acb518ea5a160820e64681ff95a16b010fe1156c`: present.
- Annotated tag `equinesync-governance-v1.0-locked-2026-07-16`: present and peels to the expected baseline commit.
- Aggregate baseline manifest: `2208/2208` entries independently read from Git objects and verified for bytes and SHA-256; total `255522257` bytes; manifest SHA-256 `f5666ebffbfe527f6d01eb7fe7fbe9f21de541b7b3afe5c4a1fe2d1b3379bfe9`.
- Controlled-thread authorization commit `75c56ac67b0de694436c093fc2dc5ff5dffe4ff3`: present and current HEAD.
- Preceding runtime-requalification commit `da84c25eaf7a5973f1b7309b7a99ba8fc0e72b60`: present and parent/ancestor of the authorization commit.
- Four fallback authority records in the working tree matched their committed Git blobs at the base commit; the authorization checksum set passed.
- Stage 2A closure commit `56dc68ce761b84800caa60997af7fb62ab34f82d`: absent from the local, non-shallow repository object database.
- Stage 2A document references `2ffdeeaff402ff6efbfebc192b728148c02fb617`, `3b9669231e01cf23edcfc2251674af15be1786dc`, and `3245ec6f94b4c47653f7737a2083079de736ec6e`: all absent locally.
- Coordinator update: the coordinator reported authenticated GitHub API verification that `56dc68ce761b84800caa60997af7fb62ab34f82d` exists in `rianray2012-coder/EquineSync-V4`, with message `Record Founder closure of Stage 2A Candidate 009 package findings` and timestamp `2026-07-20T14:34:37Z`. CMT-01 did not use network and did not independently reperform that verification. Local absence is `DETERMINISTICALLY_VERIFIED` at `E4`; remote existence is `REPORTED_BUT_NOT_VERIFIED` at `E1` for this lane.

## 6. Authority, lifecycle, and source results

The authority and lifecycle register accounts for 44 records, including 28 package source-reconciliation rows.

- Exact repository path and declared hash matched at the base commit for `6/28` source rows.
- Repository paths existed but the package registers omitted a declared hash for `10/28` rows; CMT-01 computed the base-commit hashes without changing the source registers.
- `12/28` rows used unresolved or non-repository references. Some declared hashes could be located elsewhere in the baseline, but active path and lifecycle were not thereby established; others had no located source bytes or no declared hash.
- Relationships Founder-decision lifecycle records conflict at the status layer: two registers contain `16` `PENDING` rows while the controlled-sequence ingestion contains `16` `FOUNDER_APPROVED_AS_RECOMMENDED` rows.
- Relationships ADR recommendation lifecycle records conflict at the status layer: the recommendation register contains `7` pending rows while the controlled-sequence ingestion contains `7` `FOUNDER_APPROVED_RECOMMENDATION` rows.
- Earlier packages were preserved as predecessor evidence. Their status text was not silently promoted by later packages.

No semantic comparison of the decisions or ADR texts was performed.

## 7. Custody and segregation observations

At first observation, the expanded handoff files were mode `0644` and their directories were writable. Expanded review-material files were mode `0444`, but all six containing directories were owner-writable.

The coordinator then reported that both trees had been set to directories `0555` and files `0444`, with metadata-only change. Two direct CMT-01 rechecks at `2026-07-20T19:53:00Z` and `2026-07-20T19:53:10Z` observed all 155 input files at `0444`, but all 13 input directories at `0700` and owner-writable. Rehashing confirmed zero byte drift. The coordinator report and direct observation are preserved separately; CMT-01 does not treat the directories as technically read-only.

No other lane output was read. No frozen input or Git object was modified.

One contained procedural deviation occurred during output creation: three CMT-01 draft files initially resolved beneath the generated thread directory because the patch tool used that directory as its relative root. The same patch mechanism moved all three files into the authorized CMT-01 lane directory, and the empty accidental directory tree was removed. No frozen input, repository source, or other lane output was touched. This deviation is preserved rather than erased.

## 8. Procedures

1. Read the complete lane prompt, repository `AGENTS.md`, orchestration directive, common operating contract, runtime permission control, fallback authorization, review protocol, review plan, handoff start file, Founder directive, authorization context, and package manifest.
2. Calculated SHA-256 with `shasum -a 256`; validated checksum lists with `shasum -c`.
3. Tested ZIP containers with `unzip -t`; enumerated with `unzip -Z1`; streamed entries with `unzip -p` and compared their SHA-256 values with expanded files.
4. Validated package-manifest path, byte-count, SHA-256, and count fields against the expanded packages.
5. Parsed JSON with `jq` and CSV with Ruby CSV parsing.
6. Inspected repository objects and ancestry using read-only `git cat-file`, `git show`, `git rev-parse`, `git merge-base`, `git ls-tree`, and `git hash-object` operations.
7. Independently streamed all 2,208 baseline-manifest Git blobs through `git cat-file --batch` and recomputed byte counts and SHA-256 values.
8. Checked source-register repository paths and declared hashes at the base commit; searched the baseline manifest by exact source hash where paths were unresolved.
9. Inspected file and directory modes with `stat`, `find`, `ls`, and nonmutating writability checks before and after the coordinator update.
10. Rehashed frozen inputs after permission metadata changed.
11. Wrote only the required final deliverables to the authorized lane-output path after containing the recorded patch-relative draft-path deviation.

## 9. Scope-denominator accounting

All 20 ledger procedures are accounted for in `WORK_COMPLETENESS_LEDGER.csv`. Procedures with unavailable authority objects, unresolved source identity, or permission-control discrepancies are marked `COMPLETED_WITH_LIMITATION`; no assigned item is silently omitted.

## 10. Findings and classifications

| Finding | Severity | Classification | Lifecycle | Result |
|---|---|---|---|---|
| `ES-REV-2026-002-CMT-01-F-0001` | `P1_BLOCKING` | `SOURCE_GAP` | `OPEN` | Expected Stage 2A authority commit and its three documentary chain commits are absent locally. Coordinator-reported remote existence of the expected closure commit is E1 for this lane, not an independent byte-level verification. |
| `ES-REV-2026-002-CMT-01-F-0002` | `P1_BLOCKING` | `CONTROL_WEAKENING` | `OPEN` | All input files are now `0444`, but all 13 containing directories are `0700` and owner-writable, contrary to the reported `0555`; replacement or deletion is not technically prevented. |
| `ES-REV-2026-002-CMT-01-F-0003` | `P1_BLOCKING` | `SOURCE_GAP` | `OPEN` | Only 6 of 28 source-reconciliation rows carry an exact path and matching declared hash at the base commit; 10 omit hashes and 12 remain unresolved or non-repository references. |
| `ES-REV-2026-002-CMT-01-F-0004` | `P1_BLOCKING` | `AMBIGUOUS_REQUIRES_REMEDIATION` | `OPEN` | Relationships decision and ADR recommendation status registers preserve pending states alongside later approval-ingestion states without a single reconciled lifecycle locator. |
| `ES-REV-2026-002-CMT-01-F-0005` | `P2_NONBLOCKING` | `EDITORIAL_ONLY` | `OPEN` | Completion-summary ZIP filenames include `_Package` while the actual frozen archive locators omit it; hashes identify the intended bytes. |
| `ES-REV-2026-002-CMT-01-F-0006` | `OBSERVATION` | `CONTROL_WEAKENING` | `VERIFIED_CLOSED` | Three draft outputs briefly resolved under the generated thread root; they were moved to the authorized path and the empty accidental tree was removed, with no input or cross-lane contact. |

Lane finding counts: `P0 0 / P1 4 / P2 1 / observations 1`.

## 11. Claim-to-evidence links

- External ZIP identity: `E-EXT-001`.
- Expanded handoff: `E-HOF-001` through `E-HOF-015`.
- Expanded package inventory: `E-IDN-*`, `E-RAD-*`, `E-RCS-*`, `E-RPI-*`, and `E-RPR-*`.
- Repository objects and tag: `E-GIT-001` through `E-GIT-008`.
- Coordinator-reported remote commit verification: `E-COORD-001`.
- Base-commit authorization records: `E-AUT-001` through `E-AUT-004`.
- Governance lock records and manifest: `E-GOV-001` through `E-GOV-004`.
- Authority and lifecycle details: `AUTHORITY_AND_LIFECYCLE.csv`.

## 12. Assumptions and contradictions

- The coordinator’s authenticated GitHub API statement is treated as a reported single-source observation because no API response artifact or remote Git object was supplied to this lane.
- The coordinator’s `0555` directory-mode statement conflicts with two direct local observations of `0700`.
- Later approval-ingestion records may intentionally preserve predecessor pending registers, but the supplied lifecycle records do not provide one unambiguous reconciled status locator.
- No reviewed-document instruction was treated as an instruction unless it was part of the controlling authorization, contract, directive, plan, or lane prompt.

## 13. Blocked, unavailable, and untested areas

- Direct local verification of commit `56dc68c` and the three Stage 2A chain commits was unavailable.
- CMT-01 did not access GitHub or refresh refs because network use was prohibited.
- Source lifecycle was not independently established for rows lacking exact active paths, hashes, or terminal lifecycle records.
- The application, database, schemas, migrations, provider workflows, GP-05, and production were not run or tested.
- Semantic ADR conformance, ratification readiness, adversarial review, machine-validation breadth, and documentary golden paths belong to other lanes and were not assessed.

## 14. Required next actions

1. Preserve the coordinator’s authenticated GitHub API response as a registered evidence artifact, or make commit `56dc68c` and its relevant source tree available to an isolated read-only verifier for direct byte-level confirmation.
2. Apply and verify non-writable directory modes or a host-enforced immutable/read-only mount for both frozen input trees; repeat mode and hash checks afterward.
3. Reconcile all 28 source-register rows to exact active paths, hashes, and lifecycle records without rewriting predecessor evidence.
4. Add one explicit lifecycle reconciliation that distinguishes predecessor pending registers from later approved ingestion for 16 decisions and seven ADR recommendations.
5. Do not represent input integrity as cleared until the open P1 custody findings are reconciled by the coordinator and preserved in the review evidence package.

## 15. Completeness and reliability

- Completeness: `C4_COMPLETE_FOR_RECORDED_SCOPE`
- Reliability: `R2_INTERNALLY_CHECKED`
- Lane result: `CMT01_PROCEDURES_COMPLETE_INPUT_INTEGRITY_NOT_CLEARED`
- Confidence: `HIGH` for observed bytes, hashes, local Git objects, parser results, and modes; `LOW` for coordinator-reported remote commit existence until its evidence artifact is preserved; `UNRESOLVED` for incomplete source lifecycle.

This is a custody result only and not a semantic ratification recommendation or Founder disposition.

## 16. Self-audit

1. Remained within role: yes; no semantic recommendation made.
2. Reviewed the correct package: yes; external hash and expanded-byte equality verified.
3. Accounted for every assigned item: yes; see the ledger.
4. Distinguished claims from evidence: yes; remote verification is labeled reported.
5. Avoided overstating verification: yes; local and remote commit evidence are separate.
6. Disclosed assumptions and conflicts: yes.
7. Disclosed exclusions, unavailable areas, and untested areas: yes.
8. Used objective closure criteria: yes; exact hashes, paths, modes, counts, and Git-object presence.
9. Did not approve, waive, accept risk, or exercise Founder authority: yes.
10. Made the method reproducible: yes; procedures and denominators are recorded.
11. Verified evidence and output references: yes, subject to the output manifest’s self-hash exclusion.
12. Invalidation conditions: any byte change, replaced directory entry, different Git object set, unreconciled remote evidence, source-lifecycle change, or post-freeze package modification requires revalidation.

## 17. Completion Attestation

> I completed the procedures identified in the Work Completeness Ledger for the recorded scope. This attestation does not constitute Founder approval, external assurance, legal certification, or proof that undiscovered defects do not exist.

## 18. What This Work Did Not Establish

This work did not establish that Identity or Relationships ADRs are semantically aligned, ratification-ready, implementation-authorized, execution-ready, production-ready, externally assured, or approved by the Founder. It did not close F-0001, resolve the runtime selector limitation, activate any ES-RA custom agent, authorize Stage 2, or validate application behavior. No-issue results apply only to the exact recorded sources, procedures, and limitations.

## 19. Output hashes

- `EVIDENCE_INVENTORY.csv`: `0708dd9a185f9d93bee41f5d2880112a4afab2b812598ec59985a6901cfcb1bf`
- `AUTHORITY_AND_LIFECYCLE.csv`: `b4e3176bdf7754bdb8ac6ba03760df452f7c4759377ea5a6154c8b1f1051f6e9`
- `WORK_COMPLETENESS_LEDGER.csv`: `6c42788c0e2ae9a1edbe81481c67429c4ff37d96e202fa8beeefa00c55d1daef`
- Final `LANE_REPORT.md` and the non-self output-manifest entries are recorded in `OUTPUT_MANIFEST.json`.

`OUTPUT_MANIFEST.json` excludes its own final-byte SHA-256 because embedding that value would be self-referential. Its final external SHA-256 is calculated during lane handoff validation.
