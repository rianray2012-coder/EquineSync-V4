# CMT-08 Segregated Synthesis and Proposed Redlines

`NON_AGENT_CONTROLLED_THREAD_REVIEW`

`NOT_ES_RA_AGENT_EVIDENCE`

## Control and provenance

- Review cycle: `ES-REV-2026-002`
- Directive: `ES-FORA-DIR-CMT-IDENTITY-RELATIONSHIPS-REVIEW-V1.0`
- Lane: `CMT-08`
- Role: generic controlled Codex thread performing segregated documentary synthesis; no `ES-RA-*` identity was claimed, loaded, or executed
- Current thread ID: `019f811f-155f-7eb1-90eb-60b7f9bba4d5`
- Delegating source thread ID: `019f8104-9235-7f03-8a3e-c68d4b199e09`
- Runtime/model provenance visible to this lane: Codex desktop generic controlled thread; GPT-5 family; exact deployed model identifier not exposed
- Codex runtime: `codex-cli 0.144.6`
- Host: Darwin `25.5.0` arm64; macOS `26.5.2`; zsh `5.9`
- Observed thread start UTC derived from the runtime thread identifier: `2026-07-20T20:02:05Z`
- Report generated UTC: `2026-07-20T20:06:25Z`
- Frozen evidence root: `/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/review_materials`
- Preserved lane-output root: `/Users/rianray/Documents/Codex/2026-07-20/open-start-here-md-then-execute/work/EquineSync-V4-controlled-review/governance/founder_orchestrated_review/temporary_non_agent_fallback/FORA-NONAGENT-FALLBACK-2026-001/reviews/ES-REV-2026-002/lane_outputs`
- Authorized write root: the `CMT-08` directory containing this report

This lane used no network, connector, application runtime, database, provider, product workflow, production credential, or Git mutation. It did not modify frozen inputs or any other lane output.

## Proposed final disposition

`IDENTITY_AND_RELATIONSHIPS_REQUIRE_BOUNDED_REMEDIATION`

This is the only directive-listed disposition proposed by CMT-08. It is a synthesis recommendation, not a Founder decision, approval, ratification, adoption, lock, waiver, risk acceptance, implementation authorization, execution authorization, PR, merge, tag, release, deployment, production-readiness statement, enrollment-readiness statement, or `F-0001` closure.

Identity is not ready for exact-text Founder ratification because two open P0 control weakenings and multiple open P1 traceability, authority, contract, and state-model findings remain. Relationships is not ready because open P1 decision-to-ADR, delegation, lifecycle, source, contract, and state-model findings remain. The directive forbids a ratification-ready recommendation while any P0 or P1 is open.

## Severity rollup

The normalized, deduplicated CMT-08 synthesis contains:

| Severity | Open synthesized findings |
|---|---:|
| `P0` | 2 |
| `P1` | 16 |
| `P2` | 7 |

These are synthesized issue groups, not a sum of lane row counts. The preserved lane counts remain attributable: CMT-01 `0/4/1`; CMT-02 `2/15/1`; CMT-03 `0/8/1`; CMT-04 `0/3/1`; CMT-05 `0/5/3`; CMT-06 `0/4/3`; CMT-07 `0/4/2` for `P0/P1/P2`, excluding CMT-05's separately observed out-of-scope implementation concern. Cross-lane duplicates were consolidated without erasing their source IDs.

## Integrity, authority, lifecycle, and segregation

These dimensions are intentionally separate:

1. **Observed byte integrity: PASS.** CMT-01 verified the external handoff ZIP SHA-256 `91cdb1c24f13940814035036c2c76c7cec415945337edbf3778e2a77c4a140f6`, `15/15` expanded-handoff byte equality, `140/140` embedded-package byte equality, `130/130` internal checksum entries, and zero post-permission byte drift. CMT-04, CMT-05, and CMT-06 independently confirmed the package checksum sets; CMT-06 returned frozen-input integrity `PASS`.
2. **Authority and lifecycle: OPEN.** CMT-01 could not locally verify the Stage 2A closure commit or its three cited chain commits; the expected closure commit's remote existence was coordinator-reported but not independently re-performed by CMT-01. Exact active path/hash/lifecycle coverage remains incomplete, and predecessor `PENDING` records coexist with later approval-ingestion records without one unambiguous current-state overlay.
3. **Technical segregation/immutability: OPEN LIMITATION.** CMT-01 twice observed all 13 containing input directories as owner-writable `0700`, despite a coordinator report of `0555`. CMT-06 checked that input files had no write bits, but did not establish non-writable containing directories. No frozen byte drift or cross-lane input modification was observed. The CMT-01 dissent therefore remains open and is not converted into an observed byte-corruption claim.
4. **Procedural lane segregation: COMPLETE WITH DISCLOSED LIMITATIONS.** All seven source lanes reported no other-lane reads where prohibited, no frozen-input modifications, and no prohibited execution. CMT-01 disclosed a contained draft-output path deviation that was corrected and verified closed. Host-level path isolation was procedural rather than sandbox-enforced.

Because the frozen package bytes are present and exact, CMT-08 does not select the directive's input-integrity-failure disposition. Because no cross-lane contamination or input mutation was established, it does not select the directive's segregation-failure disposition. This does not clear or waive the open CMT-01 authority and technical-segregation findings; they remain explicit prerequisites for the coordinator's final package handling.

## Cross-lane synthesis

### Agreements

- The exact frozen bytes are internally coherent and parseable; no byte corruption, missing package file, malformed JSON/CSV, duplicate controlled identifier, or `MAIP` token drift was found.
- All fourteen formal ADRs remain proposed exact text pending ratification and expressly do not authorize implementation.
- Relationships recommendation-to-formal core sections are exact for all seven ADRs. Exact copying does not by itself establish coverage of every higher-authority Founder decision.
- Identity and Relationships maintain the central documentary boundary that authentication is not authorization, a relationship is not permission, provisional claims are not authority, and offline proposals are not authoritative.
- CMT-07 reproduced `13/13` documentary paths, while retaining P1 blockers and explicitly denying any implementation or readiness inference.
- Source reconciliation and cross-domain contract closure remain open in both domains.

### Identity result

The two P0 findings are independently supported by the frozen text and multiple lanes:

- Minor-account separation is mandatory in `IDENTITY-FD-004`, but the workflow makes the minor account optional and the proposed Protected Participant contract says it is only ordinarily separate.
- `IDENTITY-FD-006` keeps high-risk actions restricted until step-up, risk checks, or manual review completes, while the proposed Identity-to-Authorization invariant allows policy acceptance of resulting recovery assurance without preserving that required additional condition.

P1 Identity findings include unmapped or incomplete Founder-decision semantics, unsupported material technical choices in draft ADR text, the Identity-owned multi-location tenancy default, protected-transition timing ambiguity, incomplete state/event and audit matrices, stale-fact and actor-chain contract weaknesses, incomplete Protected Participant boundaries, and unresolved sources/contracts.

### Relationships result

All seven formal ADRs reproduce their approved recommendation core sections exactly. CMT-03 treats that as strong positive conformance and identifies two decision-level ADR-REL-003 defects. CMT-04 independently compares the formal set to the higher-authority Founder directions and identifies broader omissions. Direct CMT-08 checks confirm that several ADR metadata mappings name Founder decisions whose operative rules are absent or only validation-level in the mapped ADR text; this broader traceability dissent remains open rather than being silently resolved against either lane.

The most clearly converged Relationships redlines are:

- make every disputed/inactive required source zero-authority for dependent grants unless a separately approved independent source is revalidated;
- restore automatic expiry by default and current-authority revalidation for every renewal;
- remove the unqualified canonical `VERIFIED` lifecycle state or define it only as a purpose/time/evidence-scoped projection consistent with ADR-REL-004;
- add or accurately remap the missing Founder-decision semantics in the formal ADR set;
- complete typed party and representation-basis contract fields and obtain the missing Authorization counterparty review.

## Dissent preserved

`DISSENT_REGISTER.csv` preserves eight material reconciliations without erasing the lane positions:

- CMT-01 input-integrity-not-cleared versus CMT-06 byte-integrity `PASS`;
- CMT-01 direct `0700` directory observations versus coordinator-reported `0555`;
- local absence versus coordinator-reported remote existence of the Stage 2A closure commit;
- CMT-03's recommendation-core method versus CMT-04's higher-authority decision-semantic method;
- CMT-05 and CMT-06's different acceptance-coverage denominators and inference boundaries;
- CMT-04's P2 status-drift severity versus CMT-03/CMT-06's P1 machine/current-lifecycle ambiguity;
- CMT-07 `PASS_DOCUMENTARY` versus the retained P0/P1 ratification blockers, reconciled as different pass criteria;
- lane-specific severity suffixes such as `P1_BLOCKING` normalized to directive severity `P1` only in CMT-08, without rewriting source evidence.

## Proposed redlines

`PROPOSED_REDLINE_REGISTER.csv` contains only proposals supported by preserved lane evidence plus direct frozen-text confirmation. No frozen ADR or contract was changed. Each proposal remains `PROPOSED_NOT_APPROVED`; material additions require Founder decision, and cross-domain contract changes require owning-domain concurrence and fresh independent review.

The proposed register contains 19 bounded actions covering the two P0 corrections, Identity decision mapping and source/contract/state repairs, Relationships delegation and decision-semantic repairs, current-lifecycle precedence, direct acceptance-traceability closure, and nonblocking terminology clarifications.

## Required Founder action

The exact recommended Founder action is:

> Do not ratify the current Identity or Relationships formal ADR text. Authorize a bounded successor documentary-remediation package that preserves the frozen predecessor, resolves every P0 and P1 synthesized finding, separately resolves or formally dispositions the CMT-01 authority/lifecycle and directory-immutability dissent, carries exact source and approval provenance, applies only independently reviewed proposed redlines, regenerates manifests and checksums, and undergoes a fresh segregated review before any ratification request. Do not authorize implementation, execution, PR, merge, tag, release, deployment, enrollment, production use, or `F-0001` closure through this action.

The coordinator and Founder retain final packaging and decision authority.

## Limitations

- This is a bounded documentary synthesis of preserved CMT-01 through CMT-07 outputs and the frozen review materials only.
- No network, remote repository refresh, external assurance, application, database, provider, schema, migration, workflow, executable test, production environment, or legal determination was used.
- CMT-08 did not independently reproduce every lane procedure; it verified the controlling directive, lane outputs, and the frozen clauses needed for synthesized findings and redline support.
- A proposed redline is not approved text. A lane agreement is not implementation evidence. A documentary pass is not runtime proof.
- Authority/lifecycle gaps, unratified exact wording, implementation absence, and technical segregation limitations remain separate; none is silently promoted to closure.

## Self-audit

1. Both required labels are present in every CMT-08 output: validated through the final manifest procedure.
2. Only directive classifications are used in the synthesized finding and redline classification fields.
3. Nonempty severities use only `P0`, `P1`, or `P2`.
4. Exactly one directive-listed final disposition is proposed.
5. CMT-01 byte findings, authority/lifecycle findings, and segregation findings are separated and its dissent is preserved.
6. Lane attribution and source finding IDs are retained.
7. Proposed redlines are not self-approved and no frozen ADR was changed.
8. Frozen-input modifications: `0`.
9. Other-lane-output modifications: `0`.
10. Network calls: `0`; application/product executions: `0`; Git mutations: `0`.
11. Custom agents claimed, loaded, activated, or executed: `0`.
12. No Founder-reserved action or `F-0001` closure is claimed.
13. CSV and JSON syntax, counts, cross-references, labels, hashes, and manifest self-hash are recorded in `OUTPUT_MANIFEST.json`.

## Completion attestation

`CMT_08_SEGREGATED_SYNTHESIS_COMPLETE_WITH_OPEN_P0_P1_REMEDIATION_REQUIRED`

This attests only that the assigned CMT-08 documentary synthesis and seven-output set are complete for the recorded scope. It does not attest ratification readiness, implementation readiness, execution readiness, operational safety, production readiness, enrollment readiness, external assurance, Founder approval, or `F-0001` closure.

## Output hashes

Final byte sizes and SHA-256 values for all non-manifest CMT-08 outputs are recorded in `OUTPUT_MANIFEST.json`. The manifest records a normalized self-hash computed with its `manifest_self_hash` value replaced by 64 zero characters to avoid recursion.
