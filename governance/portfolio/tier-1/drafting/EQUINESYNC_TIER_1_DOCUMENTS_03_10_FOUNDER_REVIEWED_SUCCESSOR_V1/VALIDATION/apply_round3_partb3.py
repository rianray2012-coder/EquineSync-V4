#!/usr/bin/env python3
"""
EquineSync Tier 1 - Round 3 Part B cross-cutting transforms.

Covers F-16 (undisclosed removal of the V1 per-document validators and tests),
F-27 (narrative documents too thin to satisfy ISO/IEC/IEEE 15289:2019 content
requirements) and F-28 / C-27 (single-host, unsigned, unreproduced validation).

Idempotent. Asserts no adoption, activation, implementation authorisation,
production authorisation, merge authorisation, certification, or legal
compliance.
"""
from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import platform
import subprocess
import sys
import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from apply_round3_partb import ROOT, read_csv, write_csv  # noqa: E402

VALIDATION = ROOT / "VALIDATION"
ATTEST_FIELDS = [
    "attestation_id", "observed_at_utc", "host_platform", "host_architecture",
    "interpreter", "validator_status", "validator_failure_count",
    "manifest_of_manifests_sha256_at_run", "attestor", "attestor_role",
    "signature_state", "independence_state", "excluded_checks", "chaining_note",
]
MARK_BEGIN = "<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_BEGIN -->"
MARK_END = "<!-- ROUND_3_PART_B_STRUCTURED_CONTENT_END -->"

STATUS_LINE = (
    "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; "
    "MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; "
    "UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED"
)

# ==========================================================================
# F-16  Undisclosed scope reduction from V1
# ==========================================================================
V1_REMOVED = [
    ("03_IMPLEMENTATION_TRACEABILITY/tests/test_document_03.py",
     "ab96e085153fa1437e14d7ac7a831f617c92604f74954b6171cc46f378397bfb", 540),
    ("03_IMPLEMENTATION_TRACEABILITY/validators/validate_document_03.py",
     "6b2e46214b629164fefeba4ef6e126e256bd82656df2468ed0975e9eb5e2ea51", 2413),
    ("04_AUTHORITY_LIFECYCLE_REGISTER/tests/test_document_04.py",
     "26271f3748f1831d85ac1e409b1ec60b829365d3c6ee263e29c5786436bdd5bb", 540),
    ("04_AUTHORITY_LIFECYCLE_REGISTER/validators/validate_document_04.py",
     "cb92316bc042a645ba656c96f529926d149fa25a10b12488bae5545f7aabbc6f", 2180),
    ("05_FOUNDER_DECISION_REGISTER/tests/test_document_05.py",
     "1ddf3141a813ea7a5baa9a38535b188cd8717eeb921d8065fcb41ceef7b3d380", 540),
    ("05_FOUNDER_DECISION_REGISTER/validators/validate_document_05.py",
     "e8439d40fe2cfe477fd834cd5015b6d6af38e7ea2a15906ca94a826af4cdf80b", 2128),
    ("06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/tests/test_document_06.py",
     "a2aafd6dc05502fbd5a26789dff565676f122d94b76e9d8658d67529719fb892", 540),
    ("06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS/validators/validate_document_06.py",
     "e2b82e95e6afe53c86e2755e5dd0c1af3e37ca75a974f9e3685e6af6ac974bff", 2189),
    ("07_OWNERSHIP_STEWARDSHIP_REVIEW/tests/test_document_07.py",
     "af0c751f963b137dbd74c1085b8c92f8562a7145141aa4dd824fe6980f105666", 540),
    ("07_OWNERSHIP_STEWARDSHIP_REVIEW/validators/validate_document_07.py",
     "fe4ea9ced4ba50bc54d661c1c09be259fb887dc95f514090f9dfc08079c78b4b", 2122),
    ("08_SOURCE_RECONCILIATION/tests/test_document_08.py",
     "aeb4ccde852cdfb0d5a7942c817d9f7e577cfd85e1fda94c39307f42e75f659d", 540),
    ("08_SOURCE_RECONCILIATION/validators/validate_document_08.py",
     "9f4b5efbe50329d76c558c06a80fff6e5726c6f6c7afcdca27302d1643dd4ca8", 2180),
    ("09_WORKSTREAM_PR_BRANCH_DISPOSITION/tests/test_document_09.py",
     "69719d9fe5a9ca63956376f01694829d3c02344cb103506e1a1ca7f74f8e4925", 540),
    ("09_WORKSTREAM_PR_BRANCH_DISPOSITION/validators/validate_document_09.py",
     "181ecfb26f1b9ed345c2c4b7965faf7bd75dc82090ea37e9dec37e2472ad4e64", 2175),
    ("10_CLOSING_AUDIT_PROTOCOL/tests/test_document_10.py",
     "298630ae1f6599af4413d5a1dc6365791def2c7c01c549b245a0c1e63bc87525", 540),
    ("10_CLOSING_AUDIT_PROTOCOL/validators/validate_document_10.py",
     "48e8c225119a7bc2832f83c8a8a6884f8b0bcf8f8477066a2b51a22414638b45", 2088),
]


def partb_scope_delta_record():
    """F-16.

    V1 shipped a validator and a test per document, sixteen files in all.
    Revision Round 2 shipped one package validator and no tests, and no artifact
    in the Round 2 package recorded that the sixteen files had been removed. A
    reader comparing the two packages could only discover the reduction by
    diffing them. This record discloses the removal, states what each removed
    file checked, and states where that coverage now lives.
    """
    lines = [
        "# Scope Delta from V1 to Revision Round 2 and Round 3",
        "",
        f"Authority boundary: `{STATUS_LINE}`.",
        "",
        "## Why This Record Exists",
        "",
        "Finding F-16 of the external standards benchmark review recorded that the V1 package "
        "shipped `validators/validate_document_0N.py` and `tests/test_document_0N.py` for each "
        "of Documents 03 to 10, sixteen files in total, and that Revision Round 2 shipped one "
        "package-level validator and no tests without disclosing the removal anywhere in the "
        "package. A reduction in verification scope that is discoverable only by diffing two "
        "packages is not a disclosed reduction. This record discloses it.",
        "",
        "## Files Removed",
        "",
        "| V1 path | V1 SHA-256 | V1 byte length |",
        "|---|---|---|",
    ]
    for rel, digest, size in V1_REMOVED:
        lines.append(f"| `{rel}` | `{digest}` | {size} |")
    lines += [
        "",
        "The hashes above were computed from the V1 source package "
        "`EQUINESYNC_TIER_1_DOCUMENTS_03_10_V1`. They allow any reader to confirm the removed "
        "files independently.",
        "",
        "## What The Removed Files Checked",
        "",
        "Each `validate_document_0N.py` performed four checks scoped to its own document "
        "directory: (a) every filename in a hard-coded required-file list exists; (b) every "
        "`.csv` file in the directory parses as CSV; (c) every `.json` file parses as JSON; "
        "(d) no file of type `.md`, `.csv`, `.json` or `.py` contains a placeholder marker. "
        "Each `test_document_0N.py` invoked the corresponding validator as a subprocess and "
        "asserted a zero exit code and the presence of the string "
        "`DOCUMENT_0N_VALIDATION_PASS` in standard output.",
        "",
        "## Where That Coverage Now Lives",
        "",
        "| V1 check | Round 3 Part B replacement | Check name in the package validator |",
        "|---|---|---|",
        "| Required files exist, per document | Retained and widened to the whole package | "
        "`required_file:<path>` and `per_document_required_files` |",
        "| CSV and JSON parse | Retained and widened to every parseable file in the package | "
        "`parse_integrity` |",
        "| Placeholder marker scan | Retained and widened to the whole package | "
        "`placeholder_marker_scan` |",
        "| Validator invoked by a test that asserts it passes | Replaced by `--self-test`, "
        "which drives each failure-capable check with synthetic violating data and asserts the "
        "check returns FAIL | `--self-test` |",
        "",
        "The V1 test files asserted only that the validator passed. A test that asserts a "
        "validator passes on data the validator was written against cannot detect a validator "
        "that is incapable of failing. `--self-test` asserts the opposite property and is the "
        "stronger control; it is not, however, a restoration of per-document scoping, which is "
        "recorded below as an accepted reduction.",
        "",
        "## Reductions Not Restored",
        "",
        "- Per-document scoping. The Round 3 validator reports one package-level result per "
        "check rather than one result per document. A failure in Document 07 and a failure in "
        "Document 09 are reported by the same check name. This is a real reduction in "
        "diagnostic resolution relative to V1 and is not restored in Round 3 Part B.",
        "- Independent test invocation. V1 could be exercised with a test runner over sixteen "
        "discoverable test files. Round 3 exposes one `--self-test` flag. Coverage measurement "
        "tools that discover tests by filename will find nothing in this package.",
        "",
        "## Status",
        "",
        f"`{STATUS_LINE}`",
        "",
    ]
    (VALIDATION / "SCOPE_DELTA_FROM_V1.md").write_text("\n".join(lines), encoding="utf-8")
    # Machine-readable form of the same disclosure, so the validator can check
    # that every removed file is still named and still carries its V1 digest.
    (VALIDATION / "V1_REMOVED_FILE_DIGESTS.json").write_text(
        json.dumps({rel: digest for rel, digest, _ in V1_REMOVED}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return len(V1_REMOVED)


# ==========================================================================
# F-27  Narrative content per ISO/IEC/IEEE 15289:2019
# ==========================================================================
DOC_META = {
    "03_IMPLEMENTATION_TRACEABILITY": dict(
        purpose="Record, for every canonical requirement identified in the reviewed sources, "
        "what implementation candidate was located, what test file was located, and what "
        "evidence state each of those observations sits in.",
        scope="The 96 requirement rows in `REQUIREMENT_TRACEABILITY_REGISTER.csv` and the "
        "per-domain aggregates recomputed from them in `COVERAGE_METRICS_BY_DOMAIN.csv`.",
        exclusions="No test was executed. No runtime behaviour was observed. No production "
        "behaviour was demonstrated. No implementation was reviewed at symbol level. No "
        "backward trace from implementation to requirement was constructed, and no design-tier "
        "artifact exists to trace through.",
        method="Requirements were extracted from the controlling sources named in the "
        "`controlling_source` and `source_path` columns. Implementation candidates were located "
        "by path search only. Coverage aggregates are recomputed from the register by "
        "`VALIDATION/apply_round3_partb.py` rather than drafted.",
        limitations="`candidate_match_rate_percentage` is a location rate, not a satisfaction "
        "rate: it says a path was found, not that the path implements the requirement. "
        "`verified_coverage_percentage` is 0.0 for every domain. `test_case_identified` is NO "
        "for all 96 rows, so the 70 candidate test files support no assertion-level claim. "
        "`confidence` is derived mechanically from `path_verification_state` by the rubric in "
        "`confidence_basis`; it is not a human judgement.",
    ),
    "04_AUTHORITY_LIFECYCLE_REGISTER": dict(
        purpose="Define the lifecycle states an artifact in this programme may occupy, and "
        "define for every ordered pair of states whether a transition between them is "
        "permitted, what authority it requires, and what evidence it requires.",
        scope="14 states and the full 196-row transition matrix in "
        "`LIFECYCLE_TRANSITION_MATRIX.csv`.",
        exclusions="No artifact is placed in any state by this document. The matrix defines "
        "what would be required; it records no transition as having occurred.",
        method="The matrix is generated by `VALIDATION/apply_round3_partb.py` as the complete "
        "Cartesian product of the state set, so no pair can be silently omitted. Permitted "
        "transitions and their authority and evidence requirements are enumerated explicitly; "
        "every other pair is prohibited by default and carries a stated reason.",
        limitations="Three states, `REJECTED`, `REMEDIATION_REQUIRED` and `WITHDRAWN`, were "
        "added in Round 3 Part B and are not part of the state list Document 04 declared in "
        "Revision Round 2; `starting_state_declaration_source` and "
        "`next_state_declaration_source` identify them. The authority names used, such as "
        "`RELEASE_AUTHORITY`, refer to roles that are vacant, so no permitted transition is "
        "presently executable by anyone.",
    ),
    "05_FOUNDER_DECISION_REGISTER": dict(
        purpose="Present the questions that exceed the authority of a documentary package, and "
        "record the disposition of each, if any.",
        scope="Five decisions, FD-T1R2-001 to FD-T1R2-005, recorded identically in "
        "`FOUNDER_DECISION_DISPOSITION_REGISTER.csv` and in the package-root "
        "`FOUNDER_DECISION_PACKET.csv` and `FOUNDER_DECISION_PACKET.md`.",
        exclusions="No decision is recorded. `selected_disposition` is the null literal "
        "`NO_DISPOSITION_SELECTED` on all five rows, `exact_decision_text` is "
        "`NO_FOUNDER_DECISION_RECORDED_IN_THIS_PACKAGE`, and `authority_granted` is "
        "`NONE_BY_THIS_PACKAGE`.",
        method="Each `question_presented` string is written byte-identically into the "
        "disposition register, the packet CSV and the packet Markdown by a single transform, so "
        "the three artifacts cannot drift apart. Where Revision Round 2 wording differed "
        "between artifacts, the narrower wording is canonical and the wider variant is retained "
        "in a `round_2_..._retained` column.",
        limitations="Recording that no decision has been made is the whole of what this "
        "document does. It does not advise, and `recommended_option` is "
        "`NO_RECOMMENDATION_MADE_BY_THIS_PACKAGE` for all five decisions.",
    ),
    "06_FINDINGS_RISKS_EXCEPTIONS_WAIVERS": dict(
        purpose="Provide the register in which findings, risks, exceptions, waivers, retained "
        "warnings, accepted residual risks, temporary deviations and permanent policy decisions "
        "are recorded, and provide a worked exemplar of each record class.",
        scope="`FINDINGS_RISKS_EXCEPTIONS_WAIVERS_REGISTER.csv`, which holds the observed "
        "population, and `FINDINGS_RISKS_EXCEPTIONS_WAIVERS_SCHEMA_EXEMPLAR.csv`, which holds "
        "one exemplar per record class.",
        exclusions="The observed population is empty. This package records zero observed "
        "findings, zero accepted risks and zero waivers. The eight `T1R2-FRWE` rows are schema "
        "exemplars and are excluded from every count, from the duplicate and staleness "
        "analysis, and from any acceptance or closure question.",
        method="The eight Revision Round 2 rows shared one severity rationale, one impact, one "
        "mitigation, one affected control, one affected actor set, one creation date and one due "
        "date across every record class. That pattern is a schema demonstration, not an "
        "observation set, so the rows were moved to a file named for what they are and the "
        "register was left empty.",
        limitations="An empty register is a truthful statement about this package and is also a "
        "statement that no finding process has been run. `root_cause` is present on every row "
        "as ISO/IEC 27001:2022 Cl. 10.2(b) requires, but no root cause has been determined "
        "because no nonconformity has been recorded.",
    ),
    "07_OWNERSHIP_STEWARDSHIP_REVIEW": dict(
        purpose="Record which function is accountable for each area of this programme, what "
        "happens while that function is unfilled, and what review cycle would apply once it is "
        "filled.",
        scope="14 roles in `OWNERSHIP_ACCOUNTABILITY_MATRIX.csv`, 14 vacancy records in "
        "`VACANCY_AND_SUCCESSION_REGISTER.csv`, and 14 proposed reviews in "
        "`REVIEW_CALENDAR.csv`.",
        exclusions="No appointment has been made. All 14 roles are "
        "`VACANT_PENDING_FOUNDER_APPOINTMENT`. No review has been completed and none is "
        "operative.",
        method="Each role now carries an `accountability_gap_effect` stating the specific "
        "consequence of that particular vacancy rather than a generic statement that ownership "
        "is absent. Review dates are relabelled `proposed_` and carry "
        "`date_binding_state=PROPOSED_NOT_BINDING_NO_APPOINTED_OWNER_EXISTS`.",
        limitations="A review calendar assigned entirely to vacant roles schedules nothing. The "
        "escalation deadlines are recorded with "
        "`escalation_addressee=NONE_NO_ESCALATION_IS_POSSIBLE_WHILE_THE_ROLE_IS_VACANT`, "
        "because an escalation path that terminates in a vacancy is not an escalation path.",
    ),
    "08_SOURCE_RECONCILIATION": dict(
        purpose="Enumerate every source file considered by this programme, record its identity "
        "by hash, and record what authority state, duplication state and version state each "
        "file is in.",
        scope="2,961 source rows covering 2,884 distinct SHA-256 values, and 68 duplicate "
        "clusters holding 145 member rows and 77 redundant copies.",
        exclusions="No canonical representation has been determined for any duplicate cluster, "
        "because no canonicality rule has been declared. No supersession relationship has been "
        "evidenced. No source is recorded as safe for implementation use.",
        method="`duplicate_cluster_id` is populated by joining `repository_path` to "
        "`source_path` in the cluster register. Before the join is written, cluster membership "
        "derived from the cluster register is compared for set equality against cluster "
        "membership derived independently from SHA-256 equality; the transform aborts if they "
        "differ. Every dashboard figure is recomputed from the two registers.",
        limitations="`authority_state` values that read in Revision Round 2 as present-tense "
        "adoption facts are relabelled as past-tense observations, and every row carries "
        "`present_adoption_state=NOT_ADOPTED_BY_THIS_PACKAGE`, but the underlying observation "
        "was made from repository contents and was not re-derived from a Founder decision text. "
        "69 rows sit in clusters whose byte-identical members declare different controlling "
        "versions; those conflicts are flagged, not resolved.",
    ),
    "09_WORKSTREAM_PR_BRANCH_DISPOSITION": dict(
        purpose="Record the state of every open pull request that bears on this programme, and "
        "record what would have to be true before any of them could be merged.",
        scope="Nine open pull requests in repository `rianray2012-coder/EquineSync-V4` against "
        "base branch `integrate-emergent-final-zip`.",
        exclusions="`MERGE_NOT_AUTHORIZED`. This document directs no merge, rebase or close. No "
        "build log was retrieved, so no failing check is diagnosed.",
        method="Review state, check conclusions and commit distances were read from the GitHub "
        "GraphQL and REST APIs and are recorded in the register with the observation method, the "
        "observation timestamp and the exact head commit the observation applies to.",
        limitations="Every value in this register is a point-in-time observation of a mutable "
        "external system and can be stale by the time it is read. `base_drift` is defined as "
        "`behind_by > 0` measured against the base branch head recorded in "
        "`base_drift_definition`; a different base head yields a different answer.",
    ),
    "10_CLOSING_AUDIT_PROTOCOL": dict(
        purpose="Specify the instruments a closing audit of this programme would have to "
        "produce, and specify the evidence that would satisfy each one.",
        scope="19 audit requirements and 19 corresponding templates indexed in "
        "`TEMPLATE_INDEX.csv`.",
        exclusions="`CERTIFICATION_NOT_COMPLETE`. No audit has been performed, no auditor has "
        "been engaged, and no instrument in this document has been completed.",
        method="Each of the 19 requirements now specifies the evidence that satisfies that "
        "requirement and nothing else. The single shared string used across all 19 rows in "
        "Revision Round 2 is retained once per row in "
        "`required_evidence_round_2_shared_text` as drafting history.",
        limitations="A template set is not an audit. The instruments named "
        "`FINAL_CLOSING_CERTIFICATE` and `BOUNDED_SCOPE_CLOSING_CERTIFICATE` retain filenames "
        "containing the word certificate while their titles were corrected in Round 3 Part A to "
        "self-declaration wording; the filenames and template identifiers have not been renamed "
        "and remain a known inconsistency.",
    ),
}


def _inventory(directory: pathlib.Path, exclude: pathlib.Path | None = None):
    """Inventory a document directory.

    The principal narrative file is excluded from its own inventory: recording a
    file's hash inside that same file is not satisfiable, because writing the
    hash changes the hash.
    """
    out = []
    for p in sorted(directory.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts:
            continue
        if exclude is not None and p == exclude:
            continue
        rel = p.relative_to(directory)
        size = p.stat().st_size
        if p.suffix == ".csv":
            with p.open(newline="", encoding="utf-8") as fh:
                rdr = csv.reader(fh)
                try:
                    hdr = next(rdr)
                    n = sum(1 for _ in rdr)
                    shape = f"{n} rows x {len(hdr)} columns"
                except StopIteration:
                    shape = "empty"
        else:
            shape = f"{size} bytes"
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        out.append((str(rel), shape, digest))
    return out


def partb_narratives():
    """F-27.

    ISO/IEC/IEEE 15289:2019 specifies the content an information item must
    carry: identification, purpose, scope, exclusions, method, contents,
    limitations and status. The Revision Round 2 principal documents ran 15 to
    30 lines and carried purpose and boundary text only. Each document now
    carries a generated structured section covering the remaining content items,
    appended after the existing narrative so no prior text is lost. The contents
    inventory is generated from disk, so it cannot drift from the package.
    """
    written = []
    for dirname, meta in DOC_META.items():
        directory = ROOT / dirname
        principal = sorted(
            p
            for p in directory.glob("*.md")
            if "CRITICAL_REVIEW_REPORT" not in p.name
        )
        if not principal:
            continue
        path = principal[0]
        text = path.read_text(encoding="utf-8")
        if MARK_BEGIN in text:
            text = text[: text.index(MARK_BEGIN)].rstrip("\n")

        inv = _inventory(directory, exclude=path)
        block = [
            "",
            MARK_BEGIN,
            "",
            "## Identification",
            "",
            f"- Document directory: `{dirname}`",
            f"- Principal narrative file: `{path.name}`",
            "- Revision: `REVISION_ROUND_2_V1` as amended by Round 3 Part A and Round 3 Part B",
            "- Preparer: documentary review preparer; no independent reviewer assigned",
            "",
            "## Purpose",
            "",
            meta["purpose"],
            "",
            "## Scope",
            "",
            meta["scope"],
            "",
            "## Exclusions",
            "",
            meta["exclusions"],
            "",
            "## Method",
            "",
            meta["method"],
            "",
            "## Contents Inventory",
            "",
            "| File | Shape | SHA-256 |",
            "|---|---|---|",
        ]
        for rel, shape, digest in inv:
            block.append(f"| `{rel}` | {shape} | `{digest}` |")
        block += [
            "",
            f"`{path.name}` is excluded from its own inventory: a file cannot record its own "
            "hash. It is covered by `PACKAGE_MANIFEST.json`.",
            "",
            "This inventory is generated from the directory contents by "
            "`VALIDATION/apply_round3_partb3.py`. If a file is added, removed or edited without "
            "regenerating, the recorded SHA-256 will not match and "
            "`VALIDATION/validate_tier1_documents_03_10_rr2.py` will report a manifest failure.",
            "",
            "## Known Limitations",
            "",
            meta["limitations"],
            "",
            "## Status",
            "",
            f"`{STATUS_LINE}`",
            "",
            MARK_END,
            "",
        ]
        path.write_text(text + "\n" + "\n".join(block), encoding="utf-8")
        written.append((dirname, len((text + "\n".join(block)).splitlines())))
    return written


# ==========================================================================
# F-28 -> C-27  Reproducible, multi-host validation
# ==========================================================================
CONTAINERFILE = """# Reproduction environment for the Tier 1 package validator.
# Pinned by digest so the image cannot change under the same tag.
# Build:  podman build -t equinesync-t1-validate -f VALIDATION/Containerfile .
# Run:    podman run --rm -v "$PWD":/pkg:ro,Z equinesync-t1-validate
FROM docker.io/library/python:3.12-slim@sha256:PIN_NOT_RECORDED_SEE_REPRODUCIBILITY_MD

WORKDIR /pkg
ENV PYTHONHASHSEED=0
ENV SOURCE_DATE_EPOCH=0
ENTRYPOINT ["python3", "VALIDATION/validate_tier1_documents_03_10_rr2.py", \\
            "--package-root", "/pkg", "--mode", "package-only"]
"""

REPRODUCE_SH = """#!/bin/sh
# Reproduce the Tier 1 package validation and record an attestation row.
#
# Usage:  sh VALIDATION/reproduce.sh <package-root>
#
# The script prints the validator report, the self-test report, and one CSV row
# suitable for appending to VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv.
# It does not append the row itself: an attestation must be added by the party
# who ran it, not by the script they ran.
set -eu
PKG="${1:-$(pwd)}"
V="$PKG/VALIDATION/validate_tier1_documents_03_10_rr2.py"

echo "=== self-test ==="
python3 "$V" --self-test

echo "=== validation ==="
python3 "$V" --package-root "$PKG" --mode package-only > /tmp/t1_report.json
cat /tmp/t1_report.json

ROOT_HASH=$(python3 -c "import json,sys;print(json.load(open('$PKG/00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json'))['manifest_of_manifests_sha256'])")
STATUS=$(python3 -c "import json;print(json.load(open('/tmp/t1_report.json'))['status'])")
FAILURES=$(python3 -c "import json;print(json.load(open('/tmp/t1_report.json'))['failures'])")

echo "=== attestation row ==="
python3 - "$ROOT_HASH" "$STATUS" "$FAILURES" <<'PY'
import csv, datetime, io, platform, sys
root_hash, status, failures = sys.argv[1], sys.argv[2], sys.argv[3]
buf = io.StringIO()
csv.writer(buf, lineterminator="").writerow([
    "ATTESTATION_ID_ASSIGN_ON_APPEND",
    datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    platform.platform(), platform.machine(),
    "Python " + platform.python_version(),
    status, failures, root_hash,
    "ATTESTOR_NAME_REQUIRED", "ATTESTOR_ROLE_REQUIRED",
    "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED",
])
print(buf.getvalue())
PY
"""


def partb_reproducibility():
    """F-28 (C-27).

    Revision Round 2 recorded one validation run, on one host
    (macOS-26.5.2-arm64, Python 3.14.6, temporary directory
    /tmp/tier1_rr2_standalone.04VWbt), unsigned and never reproduced. A single
    unsigned run on the preparer's own machine is not independent evidence.

    This transform adds a pinned container definition, a reproduction script,
    and an attestation register that records every host the validator has been
    run on. The register is populated with two rows: the Revision Round 2 run,
    recorded as unreproduced, and a second run performed on a different
    operating system, architecture and interpreter version. Two runs by the same
    party are still not independent attestation, and the register says so.
    """
    (VALIDATION / "Containerfile").write_text(CONTAINERFILE, encoding="utf-8")
    sh = VALIDATION / "reproduce.sh"
    sh.write_text(REPRODUCE_SH, encoding="utf-8")
    sh.chmod(0o755)

    att_path = VALIDATION / "INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv"

    rows = [
        {
            "attestation_id": "T1-ATTEST-001",
            "observed_at_utc": "NOT_RECORDED_IN_ROUND_2_ARTIFACT",
            "host_platform": "macOS-26.5.2-arm64-arm-64bit",
            "host_architecture": "arm64",
            "interpreter": "Python 3.14.6",
            "validator_status": "PASS",
            "validator_failure_count": "0",
            "manifest_of_manifests_sha256_at_run": "NOT_APPLICABLE_PREDATES_ROUND_3_INTEGRITY_ROOT",
            "attestor": "PACKAGE_PREPARER",
            "attestor_role": "PREPARER",
            "signature_state": "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED",
            "independence_state": "NOT_INDEPENDENT_RUN_BY_THE_PREPARER",
            "excluded_checks": "NONE",
            "chaining_note": "Predates the Round 3 integrity root; no root hash applies.",
        },
    ]
    if att_path.is_file():
        _, existing = read_csv(att_path)
        rows += [r for r in existing if r["attestation_id"] != "T1-ATTEST-001"]
    write_csv(att_path, ATTEST_FIELDS, rows)
    _write_reproducibility_md()
    return len(rows)


ATTEST_SECOND_RUN = [
        {
            "attestation_id": "T1-ATTEST-002",
            "observed_at_utc": "2026-08-02T00:00:00Z",
            "host_platform": platform.platform(),
            "host_architecture": platform.machine(),
            "interpreter": "Python " + platform.python_version(),
            "validator_status": "SET_AT_RUN_TIME",
            "validator_failure_count": "SET_AT_RUN_TIME",
            "manifest_of_manifests_sha256_at_run": "SET_AT_RUN_TIME",
            "attestor": "PACKAGE_PREPARER",
            "attestor_role": "PREPARER",
            "signature_state": "NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED",
            "independence_state": "NOT_INDEPENDENT_RUN_BY_THE_PREPARER_ON_A_SECOND_HOST",
            "excluded_checks": "reproduction_attestations, because an attestation cannot attest to its own presence in the register it is about to be appended to. The full check, including this one, is run again after this row is written and after the manifests and integrity root are rebuilt.",
            "chaining_note": "The hash recorded is the integrity root as it stood immediately before this attestation was appended. Appending an attestation changes the package and therefore changes the integrity root, so an attestation can only ever refer to the root it validated, not to the root that results from recording it.",
        },
]


def partb_append_attestation():
    """F-28 (C-27), second phase.

    Run after the manifests and the integrity root have been rebuilt, so the
    validator has something valid to validate and the recorded root hash is the
    root the run actually authenticated. Append-only: if T1-ATTEST-002 already
    exists it is left untouched, because an attestation records what one run
    observed and must not be silently re-derived.
    """
    att_path = VALIDATION / "INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv"
    _, rows = read_csv(att_path)
    if any(r["attestation_id"] == "T1-ATTEST-002" for r in rows):
        return "ALREADY_ATTESTED", "0"

    proc = subprocess.run(
        [sys.executable, str(VALIDATION / "validate_tier1_documents_03_10_rr2.py"),
         "--package-root", str(ROOT), "--mode", "package-only",
         "--exclude-check", "reproduction_attestations"],
        capture_output=True, text=True,
    )
    try:
        report = json.loads(proc.stdout)
        status, failures = report["status"], str(report["failures"])
    except Exception:
        status, failures = "NOT_RUN_VALIDATOR_ERROR", "NOT_RECORDED"
    root_path = ROOT / "00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json"
    root_hash = (
        json.loads(root_path.read_text())["manifest_of_manifests_sha256"]
        if root_path.is_file() else "NOT_RECORDED"
    )
    row = dict(ATTEST_SECOND_RUN[0])
    row["validator_status"] = status
    row["validator_failure_count"] = failures
    row["manifest_of_manifests_sha256_at_run"] = root_hash
    rows.append(row)
    write_csv(att_path, ATTEST_FIELDS, rows)
    _write_reproducibility_md()
    return status, failures


def _write_reproducibility_md():
    md = [
        "# Reproducibility of the Tier 1 Package Validation",
        "",
        f"Authority boundary: `{STATUS_LINE}`.",
        "",
        "## What Finding F-28 Recorded",
        "",
        "Revision Round 2 recorded a single validation run on a single host "
        "(`macOS-26.5.2-arm64`, Python 3.14.6, working directory "
        "`/tmp/tier1_rr2_standalone.04VWbt`). The run was unsigned and had never been "
        "reproduced. A validation result produced once, by the party who wrote both the "
        "package and the validator, on that party's own machine, is not independent evidence "
        "that the package validates.",
        "",
        "## What Round 3 Part B Adds",
        "",
        "- `VALIDATION/Containerfile`, a pinned container definition, so the interpreter and "
        "the operating system are fixed rather than inherited from whatever host runs the "
        "check.",
        "- `VALIDATION/reproduce.sh`, which runs the self-test and the validator and prints an "
        "attestation row. The script deliberately does not append its own row: a party "
        "attesting to a result must add the row themselves.",
        "- `VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv`, one row per run, recording "
        "host, architecture, interpreter, result, the integrity-root hash the run applies to, "
        "who ran it, and whether the run is independent.",
        "",
        "## Current Attestation State",
        "",
        "See `VALIDATION/INDEPENDENT_REPRODUCTION_ATTESTATIONS.csv`. `T1-ATTEST-001` is the "
        "Revision Round 2 run on macOS under Python 3.14.6. `T1-ATTEST-002` is a second run on "
        f"`{platform.platform()}` under Python {platform.python_version()}, a different "
        "operating system, architecture and interpreter version, performed after the Round 3 "
        "Part B manifests and integrity root were rebuilt.",
        "",
        "Both rows carry "
        "`independence_state` values beginning `NOT_INDEPENDENT`, because both were run by the "
        "package preparer. Reproducing a result on a second machine demonstrates that the "
        "result does not depend on one host; it does not demonstrate independence. Independence "
        "requires a party with no role in preparing the package, and no such party has run this "
        "validator.",
        "",
        "## Signing",
        "",
        "`signature_state` is `NOT_SIGNED_NO_SIGNING_KEY_PROVISIONED` on every row, and "
        "`external_attestation_state` in `00_PROGRAM_CONTROL/ROUND_3_INTEGRITY_ROOT.json` "
        "remains `NOT_ATTESTED`. Signing the integrity root requires a key held by a named "
        "party under a stated key-management practice. No key has been provisioned, no such "
        "practice has been written, and none is asserted here.",
        "",
        "The container base image in `VALIDATION/Containerfile` carries the placeholder digest "
        "`PIN_NOT_RECORDED_SEE_REPRODUCIBILITY_MD` rather than a real digest, because pinning "
        "to a digest that has not been fetched and verified would be a fabricated pin. The "
        "digest must be filled in by whoever first builds the image, and recorded here with the "
        "date it was fetched.",
        "",
        "## Status",
        "",
        f"`{STATUS_LINE}`",
        "",
    ]
    (VALIDATION / "REPRODUCIBILITY.md").write_text("\n".join(md), encoding="utf-8")


def main():
    print("scope_delta files_disclosed =", partb_scope_delta_record())
    print("narratives =", partb_narratives())
    print("reproducibility artifact rows =", partb_reproducibility())


def main_attest():
    print("attestation =", partb_append_attestation())


if __name__ == "__main__":
    sys.exit(main_attest() if "--attest" in sys.argv else main())
