# EquineSync Tier 1 — Founder Review Brief

**Prepared for:** Founder review of the Tier 1 Documents 03–10 package, Round 3 Part B candidate
**Covers:** the 6 unresolved issues in `UNRESOLVED_ISSUE_REGISTER.csv` and the 5 undecided
decisions in `05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv`
**Package integrity root:** `a995b2dc85165ef10d9208897ec9099941729c3c9dbb8c241ce89bcdfd58a9f5`
**Validator:** PASS, 0 failures, 47 failure-capable checks, 51 self-test cases

This brief presents questions. It does not answer them, does not recommend a disposition, and does
not carry authority to do either. Where a decision cannot be answered as drafted, that is stated
plainly rather than worked around.

---

## The Short Version

Five decisions are open. **Two of them cannot be answered in their current form**, and one of the
three that can is blocked behind a missing rule. Only one is cleanly answerable today.

| Decision | Question | Answerable now? |
|---|---|---|
| FD-T1R2-002 | Appoint accountable governance roles | **Yes** |
| FD-T1R2-001 | Approve lifecycle authority vocabulary | Yes, but has no unresolved issue behind it |
| FD-T1R2-003 | Approve source-control hierarchy | **Blocked** — no canonicality rule exists to approve |
| FD-T1R2-004 | Accept or remediate residual risks | **Not answerable** — zero observed findings to accept |
| FD-T1R2-005 | Authorize future merge sequencing | **Not answerable as drafted** — merge authority is outside this package's scope |

Separately, **two of the six unresolved issues have no decision presented against them at all**:
runtime evidence (UNRES-002) and independent certification (UNRES-004). Neither is something you can
dispose of by choosing an option; both need work commissioned under separate authority.

If you do one thing: **FD-T1R2-002**. Fourteen vacant roles are the upstream cause of most of what
follows.

---

## The Six Unresolved Issues

| ID | Issue | Scale | Blocking | Decision attached |
|---|---|---|---|---|
| UNRES-001 | Named owner appointments absent | 14 roles | Adoption | FD-T1R2-002 |
| UNRES-002 | Runtime and production behaviour not observed | 96 requirements | Certification | **none** |
| UNRES-003 | Merge authority absent | 9 pull requests | Merge | FD-T1R2-005 |
| UNRES-004 | Independent certification absent | 1 package scope | Certification | **none** |
| UNRES-005 | Source dispositions outstanding at row level | 578 source rows | Adoption | FD-T1R2-003 |
| UNRES-006 | No canonicality rule for duplicate clusters | 68 clusters | Adoption | blocks FD-T1R2-003 |

None of the six blocks the documentary review itself. Four block adoption or certification; one
blocks merge.

### UNRES-001 — 14 vacant roles (the upstream one)

All fourteen roles in the accountability matrix read `VACANT_PENDING_FOUNDER_APPOINTMENT`. Part B
added a per-role statement of what that vacancy actually costs, and reading them together is the
clearest argument for acting on FD-T1R2-002:

- **product domain ownership** — no function is answerable for the 96 requirement rows;
  `requirements_with_no_owner` is 96 of 96.
- **technical implementation** — 66 of 96 requirements have no implementation candidate and no one
  is answerable for locating them.
- **records and evidence custody** — the `LOCKED` and `ACCESSIONED` lifecycle states are unreachable.
- **release authority** — the `ACCESSIONED → ACTIVE` transition is unreachable.
- **review administration** — 14 review dates and 14 escalation deadlines are unmonitored.
- **source reconciliation** — no function is answerable for the 2,961 source rows or the 578
  requiring your disposition.
- **findings management** — an empty findings register cannot be distinguished from an unexamined
  one, because no one is required to open, age, or close anything.
- **equine health and welfare** — the single welfare-relevant requirement has no implementation
  candidate and no owner.
- **privacy / safeguarding / financial controls** — 5, 1, and 2 relevant requirements respectively,
  all unowned.

The review calendar is labelled `NOT_OPERATIVE_PENDING_FOUNDER_APPOINTMENT` on every row for this
reason. Dates exist; nobody holds them.

### UNRES-002 — no runtime evidence (96 requirements)

Every one of the 96 requirement rows has `tests_executed = 0` and `runtime_evidence_present = 0`.
Part B recomputed the coverage table honestly as a result: `verified_coverage_percentage` reads
**0.0** for every domain and overall, and `test_cases_specified` reads **0**. Seventy candidate test
files were identified by path; none was opened, and identifying a file is not identifying a test.

**No decision is presented for this.** It is not a question you can answer — it is work that has to
be commissioned. The register's stated next action is to execute a runtime evidence plan under
separate authority.

### UNRES-003 — merge authority absent (9 pull requests)

Nine draft pull requests are open against `integrate-emergent-final-zip`. All nine have zero reviews,
zero review threads, and no review decision. Live observation of the repository shows:

| PR | Behind base | Ahead | Drift |
|---|---|---|---|
| 82 | 0 | 18 | no |
| 81 | 0 | 1 | no |
| 80 | 0 | 2 | no |
| 77 | 6 | 2 | yes |
| 70 | 20 | 1 | yes — **`Backend known-failure non-regression gate` = FAILURE** |
| 68 | 20 | 4 | yes |
| 67 | 20 | 4 | yes |
| 69 | 29 | 5 | yes |
| 29 | **113** | 1 | yes |

PR 29 is 113 commits behind. That is the one worth a decision on its own terms — at that distance,
rebasing and re-reviewing may cost more than re-deriving the change.

### UNRES-004 — independent certification absent

No independent reviewer is assigned in any register. Both reproducibility attestations in the package
were run by the preparer, on two different hosts, and both say so:
`NOT_INDEPENDENT_RUN_BY_THE_PREPARER`. A second machine is not independence.

**No decision is presented for this either.** Assigning a reviewer is an appointment, not a
disposition.

### UNRES-005 — 578 source rows awaiting disposition

578 of the 2,961 source rows carry `founder_disposition_required = YES`. These should not be
dispositioned one at a time. The register's stated next action is that you approve a source-control
hierarchy under FD-T1R2-003, so the 578 can be resolved **by rule** rather than individually.

Two further figures from the same register bear on that rule: **1,032 rows have no version string at
all** in the source, and **69 rows carry conflicting version declarations**.

### UNRES-006 — no canonicality rule (68 clusters, and this is the blocker)

There are 68 duplicate clusters covering 145 rows and 77 redundant copies. Each cluster records a
`preferred_canonical_representation`, but every one is flagged
`NO_CANONICALITY_RULE_DECLARED_THIS_IS_A_CLAIM_NOT_A_DETERMINATION`. The preference was expressed;
the rule that would justify it was never written.

Cluster `T1R2-SRC-CLUSTER-001` shows why this matters. Two files are **byte-identical**
(`exact_byte_identity = YES`, `content_differs = NO`) — `docs/canon/MASTER_BARN_LIFECYCLE.md` and a
copy under `docs/canon/reviews/…/current_repository_source/`. One declares no controlling version;
the other declares `V1.0`. Identical bytes, contradictory version claims. No rule in the package
decides which governs.

**UNRES-006 must be closed before FD-T1R2-003 can honestly be answered.** Approving a hierarchy while
no canonicality rule exists would approve a set of preferences, not a hierarchy.

---

## The Five Decisions

Each is presented with its options and the actual consequence of each option, drawn from the decision
packet. No option is recommended.

### FD-T1R2-001 — Approve lifecycle authority vocabulary for future use

*Why you: only Founder or delegated governance authority can adopt lifecycle rules.*
*Evidence: `LIFECYCLE_TRANSITION_MATRIX.csv` — 196 rows, 14 states, 26 permitted transitions.*

- **Approve** — the vocabulary becomes what future packages must use. It moves no artifact into any
  state.
- **Approve with modification** — usable only as amended; the matrix must be rebuilt before reuse.
- **Defer** — nothing is settled and every future package restates its own state definitions.
- **Reject** — the matrix is withdrawn; Document 04 is redrafted from the state list upward.
- **Require remediation** — named defects closed and the matrix re-validated before re-presentation.

*Note: this is the only one of the five with no unresolved issue behind it. Round 2 recorded a
drafting note of "approve with retained conditions", which was retained in the packet but is
explicitly not a recommendation.*

### FD-T1R2-002 — Appoint accountable governance roles

*Why you: the package cannot appoint owners.*
*Evidence: 14 roles, 14 vacancies, 14 non-operative reviews.*

- **Approve** — named functions become accountable for all 14 roles and the 14 reviews stop being
  non-operative.
- **Approve with modification** — only the roles you name become accountable; the rest stay vacant
  and their reviews stay non-operative.
- **Defer** — all 14 stay vacant, no review date binds anyone, every escalation deadline is
  unenforceable.
- **Reject** — the role model is withdrawn and Document 07 is redrafted.
- **Require remediation** — appointment and acceptance evidence fields populated before
  re-presentation.

**This is the decision with the widest downstream effect.** Appointment is also partly delegable: you
can name an appointment authority rather than 14 individuals.

### FD-T1R2-003 — Approve source-control hierarchy

*Why you: it controls which sources are authoritative.*
*Evidence: 2,961 rows / 2,884 unique hashes; 68 clusters / 145 members / 77 redundant copies.*

- **Approve** — the preferred representation for each of the 68 clusters becomes controlling, and the
  145 rows currently `CANONICAL_NOT_DETERMINED` can be resolved.
- **Approve with modification** — only the clusters you name are resolved.
- **Defer** — all 145 rows stay undetermined and the version conflict in cluster 001 stays open.
- **Reject** — no hierarchy exists; every duplicate is treated as an independent source.
- **Require remediation** — a written canonicality rule is drafted and applied before
  re-presentation.

**Blocked by UNRES-006.** On the present evidence, "require remediation" and "approve" are not
symmetric choices: approving would ratify 68 preferences that no rule supports.

### FD-T1R2-004 — Accept or remediate unresolved residual risks

*Why you: risk acceptance requires authority.*
*Evidence: findings register — **0 observed rows**; schema exemplar — 8 rows that are explicitly not
findings; unresolved issue register — 6 issues.*

- **Approve** — **not available as drafted.** There is no observed finding to accept.
- **Approve with modification** — you would have to name the specific risk being accepted, since none
  is recorded.
- **Defer** — `accepted_risks` stays `NONE_ACCEPTED_BY_THIS_PACKAGE`; no residual risk position
  exists.
- **Reject** — the question is withdrawn as unanswerable on the present evidence.
- **Require remediation** — a real findings population must be produced before any acceptance
  question can be presented.

Part B is the reason this reads as it does. Round 2's findings register held eight illustrative rows
that looked like real findings; they were moved to a clearly-labelled exemplar file and the live
register was rewritten with zero rows. The question was answerable before only because it was being
asked against illustrations.

### FD-T1R2-005 — Authorize future merge sequencing

*Why you: merge and adoption are outside this package.*
*Evidence: 9 pull requests; 6 behind base; 1 failing check on PR 70.*

- **Approve** — **not available as drafted.** Merge authority is outside the scope of a documentary
  package; `MERGE_NOT_AUTHORIZED` is a boundary of this review, not a gap in it.
- **Approve with modification** — you may issue a **separate merge directive naming exact pull
  requests and exact head SHAs**. This is the only route that works.
- **Defer** — all nine stay unmerged and six keep drifting further behind.
- **Reject** — the pull requests are retained as historical candidates only.
- **Require remediation** — the six behind base are rebased and PR 70's failing check is resolved
  before re-presentation.

---

## Suggested Sequence

This is a dependency ordering, not a recommendation on any disposition.

1. **FD-T1R2-002 (appointments)** — unblocks the review calendar, gives every other issue an
   addressee, and is the only decision whose "approve" path has no precondition.
2. **UNRES-006 (write a canonicality rule)** — must precede FD-T1R2-003. It is drafting work, not a
   decision.
3. **FD-T1R2-003 (source hierarchy)** — once a rule exists, this resolves 145 undetermined rows and
   gives the 578 outstanding dispositions a rule to be settled by.
4. **FD-T1R2-001 (lifecycle vocabulary)** — independent of the others; can be taken at any point.
5. **UNRES-002 (runtime evidence) and UNRES-004 (independent reviewer)** — commission as work under
   separate authority. Neither is a decision.
6. **FD-T1R2-005 (merge)** — via a separate directive naming exact PRs and head SHAs, after the
   rebases and PR 70's failing gate.
7. **FD-T1R2-004 (risk acceptance)** — re-present only after a real findings population exists.

---

## Two Things You Should Know About This Brief

**A defect was found and fixed while preparing it.** The decision packet for FD-T1R2-004 cited
"UNRESOLVED_ISSUE_REGISTER.csv (5 issues)" against a register that holds six. The count had been
typed by hand at a point in the Part B run before the register finished growing. It is now derived
from the register at write time, and a new failure-capable check, `packet_citation_counts`, was added
so a stale cross-reference of this kind fails the validator rather than reaching you. Failure-capable
checks went 46 → 47; self-test cases 49 → 51. The package integrity root changed to
`a995b2dc85165ef10d9208897ec9099941729c3c9dbb8c241ce89bcdfd58a9f5` and both reproducibility
attestations were re-run against the corrected content.

**Nothing in this brief has been decided, and nothing recommends a decision.** Every packet row
carries `recommended_option = NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE` and
`recommendation_authority_state = THIS_PACKAGE_HOLDS_NO_AUTHORITY_TO_RECOMMEND_A_DISPOSITION`. Round
2 drafting notes that read as recommendations were retained in a separately-named column so you can
see they were written, without them reaching you as advice.

---

## Source Registers

All figures above were read from the Round 3 Part B package, not restated from prior summaries:

- `UNRESOLVED_ISSUE_REGISTER.csv` — 6 issues
- `05_FOUNDER_DECISION_REGISTER/FOUNDER_DECISION_DISPOSITION_REGISTER.csv` — 5 decisions
- `FOUNDER_DECISION_PACKET.csv` — options, consequences, evidence locators
- `03_IMPLEMENTATION_TRACEABILITY/REQUIREMENT_TRACEABILITY_REGISTER.csv` and
  `COVERAGE_METRICS_BY_DOMAIN.csv` — 96 requirements, 0 verified coverage
- `07_OWNERSHIP_STEWARDSHIP_REVIEW/OWNERSHIP_ACCOUNTABILITY_MATRIX.csv`,
  `VACANCY_AND_SUCCESSION_REGISTER.csv`, `REVIEW_CALENDAR.csv` — 14 roles
- `08_SOURCE_RECONCILIATION/SOURCE_AUTHORITY_DISPOSITION_REGISTER.csv`,
  `DUPLICATE_COUNTERPART_CLUSTER_REGISTER.csv`, `SOURCE_DISPOSITION_DASHBOARD.csv` — 2,961 rows,
  68 clusters, 578 dispositions
- `09_WORKSTREAM_PR_BRANCH_DISPOSITION/WORKSTREAM_PR_BRANCH_DISPOSITION_REGISTER.csv` — 9 pull
  requests, observed live against
  [rianray2012-coder/EquineSync-V4](https://github.com/rianray2012-coder/EquineSync-V4)
- `04_AUTHORITY_LIFECYCLE_REGISTER/LIFECYCLE_TRANSITION_MATRIX.csv` — 196 rows, 14 states

---

`NOT_ADOPTED`; `NOT_ACTIVE`; `IMPLEMENTATION_NOT_AUTHORIZED`; `PRODUCTION_USE_NOT_AUTHORIZED`; `MERGE_NOT_AUTHORIZED`; `CERTIFICATION_NOT_COMPLETE`; `FOUNDER_REVIEW_REQUIRED`; `UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED`
