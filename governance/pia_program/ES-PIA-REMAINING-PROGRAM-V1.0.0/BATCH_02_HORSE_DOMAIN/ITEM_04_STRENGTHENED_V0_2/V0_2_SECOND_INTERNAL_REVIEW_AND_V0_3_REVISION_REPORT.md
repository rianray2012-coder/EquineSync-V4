# EquineSync Item 04 Second Internal Review and V0.3 Revision Report

**PIA:** Horse Identity, Profile, and Lifecycle  
**PIA ID:** `ES-PIA-HORSE-IDENTITY-LIFECYCLE`  
**Reviewed candidate:** `V0.2 STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`  
**Revised successor:** `V0.3 SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`  
**Review type:** `SECOND_INTERNAL_SUBSTANTIVE_DRAFTING_REVIEW_NOT_INDEPENDENT_REVIEW`  
**Review date:** `2026-07-22`  
**Implementation authority:** `FALSE`

## 1. Review conclusion

V0.2 was structurally complete, internally consistent, and suitable for a deeper substantive review. The second review found no defect requiring abandonment of the design. It did identify several material ambiguities that could still force engineering or downstream PIAs to make unauthorized product decisions.

The most important unresolved ambiguity was the scope of the canonical Horse ID across tenant boundaries. V0.2 required one durable identity while also requiring strict tenant isolation, but it did not decide whether the canonical identity was platform-global, tenant-local, or layered. V0.3 exposes that choice as `HOR-FD-016` and recommends a layered model: one non-public platform identity key, tenant-scoped records and projections, blind cross-tenant matching, and no automatic convergence.

V0.3 is recommended for companion-register construction, deterministic package validation, freeze, and compliant fresh independent review.

Exact disposition:

`ITEM_04_V0_3_SECOND_REVIEW_STRENGTHENED_DOCUMENTARY_CANDIDATE_READY_FOR_COMPLIANT_FRESH_REVIEW`

## 2. Material findings and dispositions

| Finding | V0.2 condition | V0.3 disposition |
| --- | --- | --- |
| Cross-tenant identity scope | One durable Horse ID and tenant isolation were both required, but platform-global versus tenant-local scope was unresolved. | Added `HOR-FD-016`, tenant-scoped record definitions, blind matching, mediated handoff, non-enumeration requirements, acceptance criteria, tests, and adversarial cases. |
| Passport and export revocation semantics | V0.2 could be read as though EquineSync could revoke or remove a downloaded external copy. | Revised `HOR-FD-014`; distinguishes platform invalidation and future trusted reliance from remote deletion, which cannot be guaranteed. Added verification-status controls. |
| Transfer effective-time model | V0.2 acknowledged different transfer consequences but still centered a case-level effective state. | Added `HOR-FD-017`, impact-specific effective times, a transfer-impact state axis, continuity-packet limitations, and tests for staggered custody, relationship, access, and financial effects. |
| External identifier collision | Microchips, registry numbers, brands, tattoos, and similar values lacked a full namespace rule. | Added issuer, registry, jurisdiction, type, and effective-period qualification. Replaced, duplicated, mistyped, fraudulent, retracted, and disputed identifiers preserve lineage. |
| Public identifier enumeration | V0.2 prohibited restricted-identifier search but did not explicitly bar canonical Horse IDs from public URLs or shared surfaces. | Added public-safe, non-enumerable references and purpose-scoped share tokens. Canonical internal Horse IDs may not serve as public locators. |
| Derived age | Birth precision was governed, but age could still be implemented as a stale stored fact. | Age is now a derived value based on source-qualified birth evidence and an explicit as-of date. |
| Twins, clones, and genetically identical horses | DNA and pedigree were bounded as evidence, but genetically identical distinct horses were not explicitly protected from convergence. | Added a direct prohibition on DNA-only merge and separate identity requirements and tests for twins and clones. |
| Multiple reproductive outcomes | Expected-foal activation was defined for one outcome but did not expressly support zero, one, or multiple outcomes. | Added reproductive predecessor records and one-to-many linkage to separate live-born Horse IDs. |
| Continuity-packet completeness | The transfer packet was permission-filtered but could still be interpreted as complete. | Packets must disclose omissions, conflicts, stale items, restrictions, and completeness limitations. |
| Human data inside horse history | V0.2 protected privacy broadly but did not fully address lawful minimization or erasure of human data without destroying horse continuity. | Added separate governance for human names, contacts, signatures, addresses, minor data, and professional identifiers, including minimization, restriction, pseudonymization, correction, and lawful erasure. |
| Hidden media and document metadata | Media sensitivity was addressed, but EXIF, device IDs, embedded contact details, and document properties were not explicit. | Added sanitization and redaction requirements with preserved source-to-derivative lineage. |
| Downstream death and missing-state effects | Death, missing, stolen, and recovery states were defined, but the boundary between Item 04 events and other PIAs' mutations needed reinforcement. | Item 04 emits permission-filtered reconciliation obligations. It may not directly delete tasks, cancel care, refund charges, or send notices owned by other PIAs. |
| Unknown or disputed owner | Horse-first onboarding did not expressly state that a horse can exist without a known or uncontested owner. | Added requirement and test prohibiting forced or manufactured owner relationships. |
| Reference durability after convergence | V0.2 required downstream reconciliation but did not expressly require durable redirects or tombstones. | Added permission-checked tombstones and redirects after merge, unmerge, and split correction. |

## 3. Expansion summary

V0.3 contains:

- 43 canonical sections in exact order;
- 120 unique normative requirements;
- 50 objective acceptance criteria;
- 60 mapped design tests;
- 10 golden paths;
- 40 adversarial, negative, and abuse scenarios;
- 17 proposed Founder decisions with recommended answers and gate effects;
- exact wording for all five mandatory readiness questions; and
- the documentary authority prohibition notice.

Net additions over V0.2:

- 20 requirements;
- 10 acceptance criteria;
- 15 tests;
- 2 golden paths;
- 8 adversarial scenarios; and
- 2 Founder decisions.

## 4. New Founder decisions

### `HOR-FD-016`: Canonical identity scope across tenants

**Decision:** Is the canonical Horse ID platform-global, tenant-local, or layered?

**Recommended answer:** Adopt a layered model: one non-public platform identity key for the real-world horse, tenant-scoped Horse Records and projections, blind cross-tenant matching, no cross-tenant enumeration, and no automatic convergence. The implementation form remains separately gated.

**Gate effect:** Required before schema, cross-tenant transfer, and duplicate-convergence authorization.

### `HOR-FD-017`: Impact-specific transfer effective times

**Decision:** May transfer consequences become effective at different times?

**Recommended answer:** Yes. Relationship, custody, possession, access, care responsibility, facility assignment, financial context, and case completion must retain separate effective times and reconciliation states.

**Gate effect:** Required before transfer implementation.

`HOR-FD-014` was also materially revised to clarify that EquineSync may invalidate a Passport or export for future trusted reliance but may not claim that a downloaded external copy has been remotely deleted.

## 5. Five-question disposition

| Question | V0.3 answer |
| --- | --- |
| Can engineering build without unauthorized product decisions? | `NO` |
| Can QA determine objectively whether the capability works? | `PARTIALLY_SATISFIED` |
| Can a reviewer trace the capability to governance and MIAP? | `PARTIALLY_SATISFIED` |
| Can EquineSync safely operate, support, monitor, recover, and maintain it? | `NO` |
| Can the Founder determine first-user enrollment readiness? | `NO` |

The answers remain appropriately conservative. V0.3 increases design clarity but does not create implementation, operational, or enrollment evidence.

## 6. Deterministic documentary validation

| Check | Result |
| --- | --- |
| Sections 1 through 43 present in canonical order | `PASS` |
| Exact five readiness questions present once each | `PASS` |
| Permitted answer vocabulary | `PASS` |
| Requirements 001 through 120 unique and contiguous | `PASS` |
| Acceptance criteria 001 through 050 unique and contiguous | `PASS` |
| Tests 001 through 060 unique and contiguous | `PASS` |
| Golden paths 001 through 010 unique and contiguous | `PASS` |
| Adversarial scenarios 001 through 040 unique and contiguous | `PASS` |
| Founder decisions 001 through 017 unique and contiguous | `PASS` |
| Unknown out-of-range requirement, acceptance, test, path, scenario, or decision references | `0` |
| Table rows with malformed closing delimiters | `0` |
| LF line endings | `PASS` |
| Tabs | `0` |
| Trailing whitespace | `0` |
| Implementation and enrollment prohibition notice | `PASS` |

## 7. File identity

| File | Lines | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| V0.2 reviewed candidate | 1,965 | 120,310 | `16345629e88801ebb12d582b91fb87dc2d6637d16ac37a69a16eb834403c4fae` |
| V0.3 revised successor | 2,238 | 151,975 | `daae9b0ebe1551217a96c0cb640939752807d12c1e2241f0a936bb9ce14a21e5` |

## 8. Remaining work before compliant fresh review

1. Create the machine-readable source, source-conflict, requirement, entity, state, permission, workflow, evidence, acceptance, test, Founder-decision, unresolved-item, cross-PIA, and traceability registers.
2. Create a validation report, artifact manifest, and checksum ledger.
3. Resolve or explicitly carry `HOR-FD-001` through `HOR-FD-017` into the frozen review package.
4. Freeze V0.3 and its companion artifacts as the exact review input.
5. Provision a GFD-007-compliant isolated review environment under separate Founder authority.
6. Conduct compliant fresh independent review.
7. Create a new successor for any post-freeze correction.

## 9. Authority boundary

This second internal review and V0.3 revision do not constitute independent review, Founder approval, adoption, ratification, lock, implementation authorization, schema authorization, migration authorization, deployment authorization, production authorization, or enrollment authorization.

`NO_IMPLEMENTATION_NO_SCHEMA_NO_MIGRATION_NO_DEPLOYMENT_NO_PRODUCTION_NO_ENROLLMENT`
