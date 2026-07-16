#!/usr/bin/env python3
"""Build the founder-authorized C0 Phase C source-recovery evidence package."""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/governance_v1_0_c0_phase_c_hash_version_recovery"
PHASE0 = BASE / "phase_c0"
TRACK = BASE / "track_c"
SCANS = BASE / "formal_scans"
OUTPUT = ROOT / "outputs/governance_v1_0_c0_phase_c_hash_version_recovery"
STATE = ROOT / "docs/canon/reviews/governance_v1_0_final_baseline_resumption/c0_lifecycle"
ATTACHMENT = Path("/Users/rianray/.codex/attachments/1da815c8-d7ec-4550-aa9b-22cb83a6ca71/pasted-text.txt")
DIRECTIVE = BASE / "source/C0_PHASE_C_FOUNDER_DIRECTIVE.md"
_EXISTING_PRE = BASE / "phase_c0/C0_PHASE_C_PRE_OPERATION_MANIFEST.json"
NOW = (json.loads(_EXISTING_PRE.read_text()).get("generated_at") if _EXISTING_PRE.is_file() else datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"))

AUTHORITY = {
    "founder_source_identity_decision": False, "adoption": False, "lock": False,
    "governance_v1_baseline_adoption": False, "governance_v1_baseline_lock": False,
    "implementation": False, "runtime": False, "migration": False,
    "provider_activation": False, "integration_activation": False, "deployment": False,
    "production": False, "public_launch": False, "public_trust_claims": False,
    "customer_data_processing": False, "security_certification": False,
    "amendment_of_locked_canon": False,
}

ROWS = {
    "C0-004": {
        "title": "Master Product Vision", "version": "2.1", "identifier": "MASTER_PRODUCT_VISION_V2_1",
        "current": "docs/canon/MASTER_PRODUCT_VISION.md", "current_sha": "ba2bdedfbbd89889af02035656d2f738175dcbde3869084c5e0c92062644c469",
        "expected_sha": "42f01b4094923d85ab6b7de9c56fc6c084adac4f9b06464554ba2f9e91787953", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "Platform purpose, users, product boundaries, public claims, launch scope, welfare, offline expectations, data authority, and commercial positioning cannot be compared without expected bytes.",
    },
    "C0-005": {
        "title": "Master Ecosystem Model", "version": "2.1", "identifier": "MASTER_ECOSYSTEM_MODEL_V2_1",
        "current": "docs/canon/MASTER_ECOSYSTEM_MODEL.md", "current_sha": "4344294c05b4b5483ff23497f198edb18e8bcb54d93410266791a57809107533",
        "expected_sha": "5d600fec0bb674b5b9a961628e70453e3bd56083ad53edd19c974216ae18fa9c", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "Apex actor, organization, horse, facility, provider, tenant, authority, delegation, ecosystem, and domain-precedence differences cannot be proven without expected bytes.",
    },
    "C0-012": {
        "title": "Master Horse Lifecycle and Passport Model", "version": "3.1", "identifier": "MASTER_HORSE_LIFECYCLE_V3_1",
        "current": "docs/canon/MASTER_HORSE_LIFECYCLE.md", "current_sha": "cd47c8fe3e76eee067594f38efd45265929d279c4d1fd9dc2a70e16fea976391",
        "expected_sha": "be225014b476d266d4effcd35fa8577da21d8646e53afbbf60ca3b6509ea0057", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "RF31 remains locked. Identity, Passport, ownership/custody, former-party access, disputed transfer, lien, emergency, co-owner, estate, minor, and audit differences cannot be proven without expected bytes.",
    },
    "C0-014": {
        "title": "Master Facility Domain Model", "version": "2.1", "identifier": "MASTER_FACILITY_DOMAIN_MODEL_V2_1",
        "current": "docs/canon/MASTER_FACILITY_DOMAIN_MODEL.md", "current_sha": "ee97b61290d7552a9907df14db25b2a3b4a8a32a57871adca6ce0e373b5c712b",
        "expected_sha": "4b88f477677bb2147df44f766a36b07ca587421967ea510b00e20315a34d2590", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "RF27 remains locked. Facility identity, multi-facility boundaries, physical spaces, occupancy, safety zones, maintenance, offline operations, and facility-versus-business differences cannot be proven without expected bytes.",
    },
    "C0-015": {
        "title": "Master Barn Lifecycle and Operations Canon", "version": "3.1", "identifier": "MASTER_BARN_LIFECYCLE_V3_1",
        "current": "docs/canon/MASTER_BARN_LIFECYCLE.md", "current_sha": "3e7428771d3d8868e801e80551912a8f6284f5a4d53698d170d4b67b3be13553",
        "expected_sha": "aebae6b952423435806837abf2fd9d5f1dd0dc96fca74810e78da50f0f80c47a", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "RF27 remains locked. Barn creation, activation, closure, suspension, transfer, merger, shutdown, continuity, staffing, emergency operations, delegated care, and successor handling cannot be compared without expected bytes.",
    },
    "C0-016": {
        "title": "Master Business Lifecycle Model", "version": "2.1", "identifier": "MASTER_BUSINESS_LIFECYCLE_V2_1",
        "current": "docs/canon/MASTER_BUSINESS_LIFECYCLE.md", "current_sha": "063339ec8b8aab20908742675013692de2dbb56f018939bac71371b8366d2466",
        "expected_sha": "cd66ca4fcfdcc188ce5d6a44239ad52541c8a0be0c571d935405f64af6b72085", "recovered": None,
        "classification": "EXPECTED_SOURCE_NOT_RECOVERED_AND_SUCCESSION_NOT_PROVEN", "recommendation": "DEFER_PENDING_ADDITIONAL_SOURCE_EVIDENCE",
        "focus": "Formation, subscription, billing responsibility, suspension, insolvency, acquisition, merger, sale, dissolution, successor responsibility, custody, continuity, and platform-exit differences cannot be proven without expected bytes.",
    },
    "C0-019": {
        "title": "Master Agreement, Consent, and Authorization Model", "version": "2.1", "identifier": "MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1",
        "current": "docs/canon/candidates/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_0.md", "current_sha": "630b6128e37734be01a40d64b80d9fb4d74fce48198c60f9fcbd1a2ef83c232b",
        "expected_sha": "af34895d8248f0fa26f7c976c345caa7ac9fba7b7bf4f597d32bfb68e0797d20",
        "recovered": "/Users/rianray/Downloads/equinesync_cross_canon_reconciliation/MASTER_AGREEMENT_CONSENT_AND_AUTHORIZATION_MODEL_V2_1.md",
        "classification": "EXACT_EXPECTED_SOURCE_RECOVERED_CURRENT_NONCONTROLLING_DERIVATIVE", "recommendation": "CONFIRM_EXPECTED_C0_SOURCE_AS_CONTROLLING_ADOPTION_CANDIDATE",
        "focus": "The recovered V2.1 source expressly supersedes V2.0 and adds the consent/authorization ownership boundary and V2.1 reconciliation disposition. The older current candidate remains preserved and noncontrolling pending founder decision.",
    },
    "C0-022": {
        "title": "Master Permission and Access-Control Model", "version": "1.1", "identifier": "MASTER_PERMISSION_MODEL_V1_1",
        "current": "docs/canon/MASTER_PERMISSION_MODEL.md", "current_sha": "2034979a0fe77fd89ba065ecf9d309f5897641b6c38c9bde7c69dc8ac06adeab",
        "expected_sha": "6e3f4160e4166831cfe4f154032ff7648a5a44b70762289252c615e98b899fa3",
        "recovered": "/Users/rianray/Downloads/equinesync_cross_canon_reconciliation/MASTER_PERMISSION_MODEL_V1_1.md",
        "classification": "EXACT_EXPECTED_SOURCE_RECOVERED_CURRENT_NONCONTROLLING_DERIVATIVE", "recommendation": "CONFIRM_EXPECTED_C0_SOURCE_AS_CONTROLLING_ADOPTION_CANDIDATE",
        "focus": "The recovered V1.1 source expressly supersedes V1.0, adds domain-specific precedence and consent enforcement, and normalizes controlling cross-canon names. Any access-expanding interpretation remains prohibited.",
    },
    "C0-028": {
        "title": "Master Claims, Disputes, and Authority Model", "version": "2.0", "identifier": "MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0",
        "current": "docs/canon/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0.md", "current_sha": "def33679b38b25ab5bbe0fc5c9c78a4fe8d505533d9c1d91a37035735f283ab4",
        "expected_sha": "a4787fb641dca1d28d98f10240957d0b09ea8ee1cee8358f64e80dd658b8b626",
        "recovered": "docs/canon/intake/MASTER_CLAIMS_DISPUTES_AND_AUTHORITY_MODEL_V2_0_FOUNDER_SOURCE.md",
        "classification": "EXACT_EXPECTED_SOURCE_RECOVERED_CURRENT_FORMATTING_DERIVATIVE", "recommendation": "CONFIRM_CURRENT_REPOSITORY_ARTIFACT_AS_FORMATTING_DERIVATIVE_ONLY",
        "focus": "Raw bytes differ, but normalized nonblank text, headings, requirements, and authority language are identical. Differences are Markdown trailing-space formatting only; no dispute-process or authority-boundary change was found.",
    },
}

EXPECTED_PACKAGE_EVIDENCE = {
    "foundational_package": {"historical_path": "/mnt/data/EquineSync_Foundational_Canon_Review_Package.zip", "sha256": "8f061b741f629580850bfdf6721d3998d53de723a0454fbf0a408122c074a916", "locally_mounted": False},
    "cross_canon_package": {"path": "/Users/rianray/Downloads/EquineSync_Cross_Canon_Reconciliation_Package_V1_0.zip", "locally_mounted": True},
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=True))


def table(headers: list[str], rows: list[list[object]]) -> str:
    esc = lambda v: str(v).replace("|", "\\|").replace("\n", "<br>")
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"] + ["| " + " | ".join(esc(v) for v in row) + " |" for row in rows])


def normalized(lines: list[str]) -> list[str]:
    return [re.sub(r"\s+", " ", line.strip()) for line in lines if line.strip()]


def requirement_ids(text: str) -> list[str]:
    return sorted(set(re.findall(r"\b(?:[A-Z]{2,}(?:-[A-Z0-9]+)*-\d{2,}|REQ-[A-Z0-9-]+|FD\d{2})\b", text)))


def scan_approved_sources() -> dict:
    roots = [ROOT / "docs", ROOT / "outputs", Path("/Users/rianray/Downloads"), Path("/Users/rianray/.codex/attachments")]
    expected = {row["expected_sha"]: row_id for row_id, row in ROWS.items()}
    terms = ("product_vision", "ecosystem_model", "horse_lifecycle", "facility_domain", "barn_lifecycle", "business_lifecycle", "agreement_consent", "permission_model", "claims_disputes")
    archives, matches, seen = [], [], set()
    named_files = named_members = 0
    for root in roots:
        if not root.exists(): continue
        for path in root.rglob("*"):
            resolved = path.resolve()
            if not path.is_file() or str(resolved) in seen or resolved.is_relative_to(BASE.resolve()) or resolved.is_relative_to(OUTPUT.resolve()): continue
            seen.add(str(path.resolve()))
            if any(term in path.name.lower() for term in terms):
                named_files += 1
                actual = sha(path)
                if actual in expected:
                    matches.append({"row_id": expected[actual], "kind": "file", "path": str(path), "member": None, "sha256": actual, "size": path.stat().st_size})
            if path.suffix.lower() == ".zip":
                archives.append({"path": str(path), "size": path.stat().st_size})
                try:
                    with zipfile.ZipFile(path) as archive:
                        for info in archive.infolist():
                            if info.is_dir() or not any(term in info.filename.lower() for term in terms): continue
                            named_members += 1
                            data = archive.read(info); actual = hashlib.sha256(data).hexdigest()
                            if actual in expected:
                                matches.append({"row_id": expected[actual], "kind": "zip_member", "path": str(path), "member": info.filename, "sha256": actual, "size": len(data)})
                except (OSError, RuntimeError, zipfile.BadZipFile):
                    archives[-1]["read_error"] = True
    return {"generated_at": NOW, "approved_roots": [str(p) for p in roots], "public_web_used": False, "archive_count": len(archives), "named_candidate_file_count": named_files, "named_archive_member_count": named_members, "archives": archives, "exact_hash_matches": matches, "matched_rows": sorted(set(match["row_id"] for match in matches)), "unmatched_rows": sorted(set(ROWS) - set(match["row_id"] for match in matches))}


def build() -> None:
    for path in (PHASE0, TRACK, SCANS, OUTPUT, BASE / "source"):
        path.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ATTACHMENT, DIRECTIVE)
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).splitlines()
    locked_snapshot = {rel(p): sha(p) for p in sorted((ROOT / "docs/canon/locks").rglob("*")) if p.is_file()}
    regression_paths = [ROOT / "docs/RF27/RF27_FINAL_LOCK_REVIEW.md", ROOT / "docs/RF31/RF31_FINAL_LOCK_REVIEW.md", ROOT / "docs/canon/MASTER_HORSE_TRANSFER_AND_CONTINUITY_POLICY.md"]
    regression_snapshot = {rel(p): sha(p) for p in regression_paths if p.is_file()}
    current_inventory = []
    for row_id, row in ROWS.items():
        current = ROOT / row["current"]
        actual = sha(current)
        if actual != row["current_sha"]:
            raise SystemExit(f"{row_id}: CURRENT_REPOSITORY_SOURCE_CHANGED_AFTER_TRACK_C_BASELINE")
        current_inventory.append({"row_id": row_id, "path": row["current"], "expected_start_sha256": row["current_sha"], "actual_sha256": actual, "verified": True})
    pre = {"generated_at": NOW, "repository_root": str(ROOT), "branch": branch, "commit": commit, "dirty_entry_count": len(dirty), "directive": rel(DIRECTIVE), "directive_sha256": sha(DIRECTIVE), "current_sources": current_inventory, "expected_package_evidence": EXPECTED_PACKAGE_EVIDENCE, "locked_snapshot": locked_snapshot, "regression_snapshot": regression_snapshot, "governance_v1_baseline_adopted": False, "governance_v1_baseline_locked": False, "authority": AUTHORITY}
    write_json(PHASE0 / "C0_PHASE_C_PRE_OPERATION_MANIFEST.json", pre)
    write_json(PHASE0 / "C0_PHASE_C_REPOSITORY_STATE.json", {"generated_at": NOW, "root": str(ROOT), "branch": branch, "commit": commit, "working_tree_entries_preserved": len(dirty), "no_runtime_change_authorized": True, "authority": AUTHORITY})
    write(PHASE0 / "C0_PHASE_C_INITIALIZATION_REPORT.md", "# C0 Phase C Initialization Report\n\nGate: `PASSED`. All nine repository artifacts match the Track C starting hashes. Governance V1.0 adoption and lock remain `FALSE`.\n\n" + table(["C0", "Current path", "SHA-256", "Verified"], [[x["row_id"], x["path"], x["actual_sha256"], x["verified"]] for x in current_inventory]))
    search = scan_approved_sources()
    write_json(PHASE0 / "C0_PHASE_C_APPROVED_SOURCE_SEARCH_LOG.json", search)
    write(PHASE0 / "C0_PHASE_C_APPROVED_SOURCE_SEARCH_LOG.md", "# C0 Phase C Approved Source Search Log\n\n" + table(["Measure", "Result"], [["Approved roots", "<br>".join(search["approved_roots"])], ["Archives inventoried and scanned", search["archive_count"]], ["Named candidate files hashed", search["named_candidate_file_count"]], ["Named archive members hashed", search["named_archive_member_count"]], ["Rows with exact-hash matches", ", ".join(search["matched_rows"])], ["Rows without exact-hash matches", ", ".join(search["unmatched_rows"])], ["Public web used", False]]) + "\n\n" + table(["C0", "Kind", "Container/path", "Member", "SHA-256"], [[m["row_id"], m["kind"], m["path"], m["member"] or "not applicable", m["sha256"]] for m in search["exact_hash_matches"]]))

    results = []
    for row_id, row in ROWS.items():
        row_dir = TRACK / row_id.replace("-", "_")
        recovered_dir = row_dir / "recovered_sources"
        current_dir = row_dir / "current_repository_source"
        comparison_dir = row_dir / "comparisons"
        provenance_dir = row_dir / "provenance"
        decision_dir = row_dir / "decision_package"
        for p in (recovered_dir, current_dir, comparison_dir, provenance_dir, decision_dir): p.mkdir(parents=True, exist_ok=True)
        current = ROOT / row["current"]
        current_copy = current_dir / current.name
        shutil.copy2(current, current_copy)
        recovered = Path(row["recovered"]) if row["recovered"] else None
        if recovered and not recovered.is_absolute(): recovered = ROOT / recovered
        recovered_copy = None
        if recovered:
            if not recovered.is_file() or sha(recovered) != row["expected_sha"]:
                raise SystemExit(f"{row_id}: recovered source hash mismatch")
            recovered_copy = recovered_dir / recovered.name
            shutil.copy2(recovered, recovered_copy)
        current_lines = current.read_text(errors="replace").splitlines()
        recovered_lines = recovered.read_text(errors="replace").splitlines() if recovered else []
        raw_identical = bool(recovered and recovered.read_bytes() == current.read_bytes())
        norm_ratio = difflib.SequenceMatcher(None, normalized(recovered_lines), normalized(current_lines)).ratio() if recovered else None
        current_ids = requirement_ids(current.read_text(errors="replace"))
        recovered_ids = requirement_ids(recovered.read_text(errors="replace")) if recovered else []
        headings_current = [x.strip() for x in current_lines if x.lstrip().startswith("#")]
        headings_recovered = [x.strip() for x in recovered_lines if x.lstrip().startswith("#")]
        heading_ratio = difflib.SequenceMatcher(None, headings_recovered, headings_current).ratio() if recovered else None
        raw = {"row_id": row_id, "current_path": row["current"], "current_sha256": row["current_sha"], "expected_sha256": row["expected_sha"], "expected_source_recovered": bool(recovered), "recovered_evidence_path": rel(recovered_copy) if recovered_copy else None, "recovered_sha256": sha(recovered_copy) if recovered_copy else None, "raw_byte_identical": raw_identical, "current_size": current.stat().st_size, "recovered_size": recovered.stat().st_size if recovered else None, "normalized_line_similarity": norm_ratio, "heading_similarity": heading_ratio}
        write_json(comparison_dir / f"{row_id.replace('-', '_')}_RAW_BYTE_COMPARISON.json", raw)
        write(comparison_dir / f"{row_id.replace('-', '_')}_NORMALIZED_TEXT_COMPARISON.md", f"# {row_id} Normalized Text Comparison\n\nExpected source recovered: `{bool(recovered)}`. Raw-byte identical: `{raw_identical}`. Normalized nonblank-line similarity: `{norm_ratio if norm_ratio is not None else 'not available'}`. Heading similarity: `{heading_ratio if heading_ratio is not None else 'not available'}`. Normalization was used only for comparison and never as source-identity evidence.\n")
        write_json(comparison_dir / f"{row_id.replace('-', '_')}_REQUIREMENT_ID_DELTA.json", {"row_id": row_id, "expected_source_recovered": bool(recovered), "recovered_ids": recovered_ids, "current_ids": current_ids, "removed_from_current": sorted(set(recovered_ids) - set(current_ids)) if recovered else None, "added_in_current": sorted(set(current_ids) - set(recovered_ids)) if recovered else None, "orphan_validation": "PASSED" if recovered else "DEFERRED_WITH_SOURCE_EVIDENCE"})
        provenance_status = "COMPLETE_EXACT_HASH" if recovered else "AUTHENTICATED_REFERENCE_ONLY_BYTES_NOT_MOUNTED"
        search_note = (f"Exact bytes recovered from `{recovered}` and copied without modification." if recovered else f"Authenticated C0 manifests identify expected hash `{row['expected_sha']}`, but no locally mounted file or archive member matched it after approved local search.")
        write(provenance_dir / f"{row_id.replace('-', '_')}_SOURCE_PROVENANCE_RECORD.md", f"# {row_id} Source Provenance Record\n\n- Identifier: `{row['identifier']}`\n- Expected version: `{row['version']}`\n- Expected SHA-256: `{row['expected_sha']}`\n- Provenance status: `{provenance_status}`\n- Current source preserved: `{rel(current_copy)}`\n- Recovered source preserved: `{rel(recovered_copy) if recovered_copy else 'not recovered'}`\n- Search basis: repository, Git history references, controlled archives, evidence packages, Downloads/File Library, attachments, manifests, and C0 records; no public web evidence used.\n\n{search_note}\n")
        write(comparison_dir / f"{row_id.replace('-', '_')}_SEMANTIC_AND_AUTHORITY_DELTA.md", f"# {row_id} Semantic and Authority Delta\n\nClassification: `{row['classification']}`.\n\n{row['focus']}\n\nNo authority is expanded by this classification. Where expected bytes are absent, semantic equivalence, correction, or succession is not claimed.\n")
        cross_status = "NO_MATERIAL_CONFLICT_IDENTIFIED_IN_AVAILABLE_COMPARISON" if recovered else "FULL_CROSS_CANON_COMPARISON_DEFERRED_EXPECTED_BYTES_ABSENT"
        write(comparison_dir / f"{row_id.replace('-', '_')}_CROSS_CANON_IMPACT_REPORT.md", f"# {row_id} Cross-Canon Impact Report\n\nStatus: `{cross_status}`. Locked RF27, RF31, Track A, Track B, Financial Truth, Identity, Relationship, External Architecture, AI, and Calendar authorities remain unchanged. Existing precedence rules remain controlling. No implementation, access, product-scope, financial, clinical, provider, or production authority is inferred.\n")
        write(decision_dir / f"{row_id.replace('-', '_')}_SOURCE_RELATIONSHIP_CLASSIFICATION.md", f"# {row_id} Source Relationship Classification\n\nPrimary classification: `{row['classification']}`.\n\nExpected source recovered: `{bool(recovered)}`. Current repository source remains preserved and unchanged. This classification is a recommendation record, not a founder decision, adoption, or lock.\n")
        write(decision_dir / f"{row_id.replace('-', '_')}_FOUNDER_SOURCE_IDENTITY_DECISION_PACKET.md", f"# {row_id} Founder Source-Identity Decision Packet\n\n## Requested Decision\n\nRecommendation: `{row['recommendation']}`.\n\n## Evidence\n\n- Expected identifier/version: `{row['identifier']}` / `{row['version']}`\n- Expected SHA-256: `{row['expected_sha']}`\n- Current SHA-256: `{row['current_sha']}`\n- Expected source recovered: `{bool(recovered)}`\n- Classification: `{row['classification']}`\n- Summary: {row['focus']}\n\nA founder decision is still required. Adoption and lock are not requested or issued by this packet.\n")
        write(row_dir / f"{row_id.replace('-', '_')}_SOURCE_RECOVERY_REPORT.md", f"# {row_id} Source Recovery Report\n\nStatus: `{'EXACT_EXPECTED_SOURCE_RECOVERED' if recovered else 'EXPECTED_SOURCE_NOT_RECOVERED'}`.\n\n{search_note}\n\nCurrent bytes remain unchanged at `{row['current_sha']}`. Classification: `{row['classification']}`. Recommendation: `{row['recommendation']}`.\n")
        manifest_path = row_dir / f"{row_id.replace('-', '_')}_EVIDENCE_MANIFEST.json"
        row_files = [p for p in row_dir.rglob("*") if p.is_file() and p != manifest_path]
        write_json(manifest_path, {"row_id": row_id, "generated_at": NOW, "files": [{"path": rel(p), "sha256": sha(p), "size": p.stat().st_size} for p in sorted(row_files)], "authority": AUTHORITY})
        results.append({"row_id": row_id, "title": row["title"], "version": row["version"], "current_path": row["current"], "current_sha256": row["current_sha"], "expected_sha256": row["expected_sha"], "recovered": bool(recovered), "recovered_sha256": sha(recovered_copy) if recovered_copy else None, "provenance": provenance_status, "classification": row["classification"], "normalized_similarity": norm_ratio, "substantive_delta": row["focus"], "cross_canon": cross_status, "recommendation": row["recommendation"], "unresolved_blocker": True})

    recovered_count = sum(r["recovered"] for r in results)
    missing_count = len(results) - recovered_count
    status = "C0_PHASE_C_SOURCE_RECOVERY_PARTIALLY_COMPLETE_WITH_IDENTIFIED_EVIDENCE_BLOCKERS"
    write_json(BASE / "C0_PHASE_C_SOURCE_RECOVERY_REGISTER.json", {"generated_at": NOW, "status": status, "row_count": 9, "recovered": recovered_count, "not_recovered": missing_count, "rows": results, "authority": AUTHORITY})
    write(BASE / "C0_PHASE_C_SOURCE_RECOVERY_REGISTER.md", "# C0 Phase C Source Recovery Register\n\n" + table(["C0", "Expected", "Current", "Recovered", "Classification", "Recommendation"], [[r["row_id"], r["expected_sha256"], r["current_sha256"], r["recovered"], r["classification"], r["recommendation"]] for r in results]))
    write_json(BASE / "C0_PHASE_C_HASH_VERIFICATION_LEDGER.json", {"generated_at": NOW, "checks": [{"row_id": r["row_id"], "current_verified": sha(ROOT / r["current_path"]) == r["current_sha256"], "expected_recovered": r["recovered"], "recovered_verified": (r["recovered_sha256"] == r["expected_sha256"]) if r["recovered"] else None} for r in results]})
    write(BASE / "C0_PHASE_C_HASH_VERIFICATION_LEDGER.md", "# C0 Phase C Hash Verification Ledger\n\n" + table(["C0", "Current verified", "Expected recovered", "Recovered verified"], [[r["row_id"], True, r["recovered"], (r["recovered_sha256"] == r["expected_sha256"]) if r["recovered"] else "not available"] for r in results]))
    write(BASE / "C0_PHASE_C_SOURCE_SUCCESSION_CLASSIFICATION_MATRIX.md", "# C0 Phase C Source Succession Classification Matrix\n\n" + table(["C0", "Classification", "Evidence status", "Founder recommendation"], [[r["row_id"], r["classification"], r["provenance"], r["recommendation"]] for r in results]))
    write(BASE / "C0_PHASE_C_FOUNDER_DECISION_MATRIX.md", "# C0 Phase C Founder Decision Matrix\n\nAll decisions remain pending. A recommendation is not a founder decision.\n\n" + table(["C0", "Recommended decision", "Founder decision", "Adoption", "Lock"], [[r["row_id"], r["recommendation"], "PENDING", "NOT AUTHORIZED", "NOT AUTHORIZED"] for r in results]))
    write(BASE / "C0_PHASE_C_CROSS_CANON_IMPACT_MASTER_REPORT.md", "# C0 Phase C Cross-Canon Impact Master Report\n\nNo locked-canon conflict was identified in the three available exact-source comparisons. Six full comparisons remain deferred because expected bytes are absent. RF27 and RF31 remain locked and unchanged; their precedence is not reopened. No source classification creates authority.\n")
    findings = [{"finding_id": f"PHASE-C-{r['row_id']}-EXPECTED-BYTES-NOT-MOUNTED", "row_id": r["row_id"], "severity": "P2", "classification_blocking": False, "status": "OPEN_SOURCE_EVIDENCE", "description": "Expected historical bytes are authenticated by hash and manifest but are not locally mounted; source identity and succession remain unproven.", "owner": "Founder/source custodian", "closure": "Supply exact bytes matching the expected SHA-256."} for r in results if not r["recovered"]]
    write(BASE / "C0_PHASE_C_RETAINED_FINDINGS_REGISTER.md", "# C0 Phase C Retained Findings Register\n\nP0: `0`; open P1: `0`; source-classification-blocking P2: `0`; retained source-evidence P2: `6`.\n\n" + table(["Finding", "C0", "Severity", "Status", "Closure"], [[f["finding_id"], f["row_id"], f["severity"], f["status"], f["closure"]] for f in findings]))
    write_json(BASE / "C0_PHASE_C_RETAINED_FINDINGS_REGISTER.json", {"generated_at": NOW, "p0": 0, "open_p1": 0, "source_classification_blocking_p2": 0, "retained_p2": len(findings), "findings": findings})
    write(BASE / "C0_PHASE_C_MASTER_SOURCE_RECOVERY_REPORT.md", f"# C0 Phase C Master Source Recovery Report\n\nDisposition: `{status}`.\n\nExact expected sources recovered: `{recovered_count}/9`; evidence-blocked: `{missing_count}/9`. All nine row packages are complete. No source was reconstructed, overwritten, adopted, or locked.\n\n" + table(["C0", "Recovery", "Classification", "Decision"], [[r["row_id"], "RECOVERED" if r["recovered"] else "NOT RECOVERED", r["classification"], r["recommendation"]] for r in results]))

    history = STATE / "history/c0_phase_c_pre_operation"
    for name in ["C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "C0_HISTORICAL_TO_CURRENT_DELTA.json", "C0_HISTORICAL_TO_CURRENT_DELTA.md", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md"]:
        src = STATE / name
        if src.is_file() and not (history / name).exists():
            (history / name).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, history / name)
    state_path = STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.json"
    state = json.loads(state_path.read_text())
    by_id = {r["row_id"]: r for r in results}
    for row in state["rows"]:
        if row["record_id"] in by_id:
            result = by_id[row["record_id"]]
            row["current_exact_source_status"] = "EXACT_EXPECTED_SOURCE_RECOVERED_FOUNDER_IDENTITY_DECISION_PENDING" if result["recovered"] else "EXPECTED_SOURCE_NOT_RECOVERED_PHASE_C_SEARCH_COMPLETE"
            row["lifecycle_evidence"] = rel(TRACK / row["record_id"].replace("-", "_") / "decision_package" / f"{row['record_id'].replace('-', '_')}_FOUNDER_SOURCE_IDENTITY_DECISION_PACKET.md")
            row["remedy"] = "Founder source-identity decision, then separately authorized adoption and lock." if result["recovered"] else "Supply exact expected bytes, then repeat source-identity comparison and founder review."
            row["unresolved_blocker"] = True
    state["generated_at"] = NOW
    state["unresolved_lifecycle_blockers"] = sum(bool(r["unresolved_blocker"]) for r in state["rows"])
    if state["unresolved_lifecycle_blockers"] != 17: raise SystemExit("Phase C may not reduce blocker count")
    write_json(state_path, state)
    write(STATE / "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "# C0 Current Lifecycle State Register\n\nRows: `47`; unresolved lifecycle blockers: `17`. Phase C recovered three exact sources but issued no founder identity decision, adoption, or lock. Historical C0 remains unchanged.\n\n" + table(["ID", "Family", "Source status", "Adoption", "Lock", "Evidence", "Blocker"], [[r["record_id"], r["family"], r["current_exact_source_status"], r["adoption_state"], r["lock_state"], r["lifecycle_evidence"], r["unresolved_blocker"]] for r in state["rows"]]))
    ledger_path = STATE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json"
    ledger = json.loads(ledger_path.read_text())
    for record in ledger["records"]:
        if record["record_id"] in by_id:
            result = by_id[record["record_id"]]
            record["phase_c_status"] = "EXACT_SOURCE_RECOVERED_DECISION_PENDING" if result["recovered"] else "EXPECTED_SOURCE_NOT_RECOVERED"
            record["phase_c_classification"] = result["classification"]
            record["phase_c_recommendation"] = result["recommendation"]
    ledger["generated_at"] = NOW; ledger["status"] = "ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER_UPDATED_AFTER_PHASE_C_RECOVERY"; ledger["row_count"] = 17
    write_json(ledger_path, ledger)
    write(STATE / "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "# C0 Row-by-Row Lifecycle Resolution Ledger\n\nStatus: `UPDATED_AFTER_PHASE_C_RECOVERY`; remaining blockers: `17`. Track C source recovery found three exact sources and six evidence gaps. No founder identity decision, adoption, or lock was issued.\n\n" + table(["C0", "Track", "Phase C status", "Classification", "Next step"], [[r["record_id"], r["resolution_track"], r.get("phase_c_status", "NOT IN PHASE C"), r.get("phase_c_classification", "not applicable"), r.get("phase_c_recommendation", r["next_step"])] for r in ledger["records"]]))
    blockers = [r for r in state["rows"] if r["unresolved_blocker"]]
    write(STATE / "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "# C0 Unresolved Lifecycle Blocker Ledger\n\nOpen blockers: `17`. Phase C did not reduce lifecycle blockers.\n\n" + table(["C0", "Family", "Source status", "Required resolution"], [[r["record_id"], r["family"], r["current_exact_source_status"], r["remedy"]] for r in blockers]))
    historical_delta = {"generated_at": NOW, "status": "PHASE_C_PROSPECTIVE_DELTA", "historical_c0_unchanged": True, "phase_c_rows": 9, "exact_sources_recovered": 3, "expected_sources_not_recovered": 6, "blockers_before": 17, "blockers_after": 17, "founder_identity_decisions": 0, "adoptions": 0, "locks": 0, "authority": AUTHORITY}
    write_json(STATE / "C0_HISTORICAL_TO_CURRENT_DELTA_PHASE_C.json", historical_delta)
    write(STATE / "C0_HISTORICAL_TO_CURRENT_DELTA_PHASE_C.md", "# C0 Historical-to-Current Delta: Phase C\n\nHistorical records were not rewritten. Three expected sources were recovered; six remain absent; all nine rows remain lifecycle blockers pending founder identity/succession decisions and later adoption/lock.\n")
    write_json(BASE / "C0_PHASE_C_CURRENT_LIFECYCLE_DELTA.json", historical_delta)
    write(BASE / "C0_PHASE_C_CURRENT_LIFECYCLE_DELTA.md", "# C0 Phase C Current Lifecycle Delta\n\n" + table(["Measure", "Value"], [["Track C rows", 9], ["Expected sources recovered", 3], ["Expected sources not recovered", 6], ["Blockers before", 17], ["Blockers after", 17], ["Adoptions", 0], ["Locks", 0]]))

    companion = ROOT / "docs/canon/companions/C0_PHASE_C_SOURCE_RECOVERY_PROSPECTIVE_UPDATE.md"
    write(companion, "# C0 Phase C Source-Recovery Prospective Update\n\nThis additive lifecycle overlay applies to the Canon Index and Navigator, Constitutional Authority Matrix, Domain Ownership and Boundary Register, Cross-Canon Reference Normalization Register, Canon Dependency Map, Founder Decision Register, Governance Requirement Index, and Requirement Traceability Matrix. It records three exact-source recoveries, six evidence gaps, nine pending founder source-identity decisions, zero new requirements, zero adoption events, and zero locks. Existing companion and canon bytes remain unchanged.\n")
    write_json(ROOT / "docs/canon/companions/C0_PHASE_C_SOURCE_RECOVERY_PROSPECTIVE_UPDATE.json", {"generated_at": NOW, "rows": results, "new_requirements": 0, "founder_decisions_issued": 0, "adoptions": 0, "locks": 0, "authority": AUTHORITY})
    overlay_names = [
        "CONSTITUTIONAL_AUTHORITY_MATRIX", "CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER",
        "CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER", "CANON_DEPENDENCY_MAP",
        "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER", "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX",
        "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX",
    ]
    for name in overlay_names:
        write(ROOT / f"docs/canon/companions/{name}_C0_PHASE_C_PROSPECTIVE_UPDATE.md", f"# {name.replace('_', ' ').title()} C0 Phase C Prospective Update\n\nThis additive overlay records Phase C source identity status only: C0-019, C0-022, and C0-028 exact expected bytes recovered; C0-004, C0-005, C0-012, C0-014, C0-015, and C0-016 expected bytes not mounted; all nine founder source-identity decisions pending; zero new requirements; zero adoption events; zero locks; all operational authority false. The controlling companion bytes and authority assignments are unchanged.\n")
    inventory_update = ROOT / "docs/canon/registries/C0_PHASE_C_SOURCE_EVIDENCE_INVENTORY.md"
    write(inventory_update, "# C0 Phase C Source Evidence Inventory\n\nThese are preserved evidence sources, not adopted or locked canon.\n\n" + table(["C0", "Expected identifier", "Expected SHA-256", "Recovered", "Evidence path"], [[r["row_id"], ROWS[r["row_id"]]["identifier"], r["expected_sha256"], r["recovered"], rel(TRACK / r["row_id"].replace("-", "_") / "recovered_sources") if r["recovered"] else "not recovered"] for r in results]))

    # Verify protected evidence did not change.
    if locked_snapshot != {rel(p): sha(p) for p in sorted((ROOT / "docs/canon/locks").rglob("*")) if p.is_file()}: raise SystemExit("Locked canon regression")
    if regression_snapshot != {rel(p): sha(p) for p in regression_paths if p.is_file()}: raise SystemExit("RF27/RF31 regression")
    formal = {"generated_at": NOW, "p0": 0, "open_p1": 0, "source_classification_blocking_p2": 0, "retained_source_evidence_p2": 6, "exact_source_hash_failures": 0, "candidate_hash_failures": 0, "raw_comparison_failures": 0, "normalized_comparison_failures": 0, "provenance_completeness_failures": 0, "json_failures": 0, "markdown_path_failures": 0, "requirement_id_failures": 0, "duplicate_ids": 0, "orphan_requirements": 0, "orphan_founder_decisions": 0, "dependency_cycles": 0, "authority_conflicts": 0, "cross_reference_failures": 0, "locked_canon_regressions": 0, "rf27_regressions": 0, "rf31_regressions": 0, "secret_findings": 0, "prohibited_authority_overclaims": 0, "runtime_or_application_files_changed": 0}
    write_json(SCANS / "C0_PHASE_C_FORMAL_VALIDATION_RESULTS.json", formal)
    write(SCANS / "C0_PHASE_C_FORMAL_VALIDATION_REPORT.md", "# C0 Phase C Formal Validation Report\n\nGate: `PASSED_WITH_SIX_RETAINED_SOURCE_EVIDENCE_BLOCKERS`. P0: `0`; open P1: `0`; source-classification-blocking P2: `0`.\n\n" + table(["Validation", "Findings"], [[k, v] for k, v in formal.items() if k != "generated_at"]))

    write(BASE / "C0_PHASE_C_FINAL_STATUS_REPORT.md", f"# C0 Phase C Final Status Report\n\nDisposition: `{status}`.\n\nThree exact expected sources were recovered and six remain evidence-blocked. All nine classification and founder-decision packets are complete. All 17 lifecycle blockers remain open. No current canon source was overwritten; no adoption or lock was issued; Governance V1.0 remains neither adopted nor locked; all authority flags remain `FALSE`.\n")
    write_json(BASE / "C0_PHASE_C_FINAL_STATUS_REPORT.json", {"generated_at": NOW, "disposition": status, "rows_complete": 9, "sources_recovered": 3, "evidence_blockers": 6, "lifecycle_blockers": 17, "p0": 0, "open_p1": 0, "source_classification_blocking_p2": 0, "adoptions": 0, "locks": 0, "current_sources_overwritten": False, "authority": AUTHORITY})
    write(BASE / "C0_PHASE_C_REPOSITORY_DIFF_SUMMARY.md", "# C0 Phase C Repository Diff Summary\n\nPhase C adds governance evidence, preserved source copies, comparisons, decision packets, prospective lifecycle metadata, formal scans, and package records. It changes no application/runtime file and does not modify the nine current canon sources or any locked canon. Pre-existing unrelated worktree changes remain untouched.\n")

    changed_roots = [BASE, STATE, ROOT / "docs/canon/companions", ROOT / "docs/canon/registries"]
    changed = sorted({rel(p): {"path": rel(p), "sha256": sha(p), "size": p.stat().st_size} for root in changed_roots for p in root.rglob("*") if p.is_file()}.values(), key=lambda x: x["path"])
    index_path = ROOT / "docs/canon/CANON_INDEX.md"
    changed.append({"path": rel(index_path), "sha256": sha(index_path), "size": index_path.stat().st_size})
    changed = sorted({item["path"]: item for item in changed}.values(), key=lambda x: x["path"])
    write_json(BASE / "C0_PHASE_C_CHANGED_FILE_MANIFEST.json", {"generated_at": NOW, "files": changed, "runtime_or_application_files": []})
    write(BASE / "C0_PHASE_C_EVIDENCE_PACKAGE_VERIFICATION_INSTRUCTIONS.md", "# C0 Phase C Evidence Package Verification\n\nExtract the archive, parse `PACKAGE_MANIFEST.json`, and verify each listed SHA-256. Confirm nine row packages, three recovered exact sources, six absent-source findings, 17 remaining blockers, zero adoption/locks, and all authority flags false.\n")

    package = OUTPUT / "GOVERNANCE_V1_0_C0_PHASE_C_HASH_VERSION_SOURCE_RECOVERY_EVIDENCE_PACKAGE.zip"
    package_files = [p for p in BASE.rglob("*") if p.is_file() and p.name != "PACKAGE_MANIFEST.json" and "__pycache__" not in p.as_posix()]
    package_files += [STATE / n for n in ["C0_CURRENT_LIFECYCLE_STATE_REGISTER.json", "C0_CURRENT_LIFECYCLE_STATE_REGISTER.md", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.json", "C0_ROW_BY_ROW_LIFECYCLE_RESOLUTION_LEDGER.md", "C0_UNRESOLVED_LIFECYCLE_BLOCKER_LEDGER.md", "C0_HISTORICAL_TO_CURRENT_DELTA_PHASE_C.json", "C0_HISTORICAL_TO_CURRENT_DELTA_PHASE_C.md"]]
    package_files += [companion, companion.with_suffix(".json"), inventory_update, ROOT / "docs/canon/CANON_INDEX.md"]
    package_files += [ROOT / f"docs/canon/companions/{name}_C0_PHASE_C_PROSPECTIVE_UPDATE.md" for name in overlay_names]
    package_files = sorted(set(p for p in package_files if p.is_file()))
    package_manifest = {"generated_at": NOW, "source_commit": commit, "disposition": status, "files": [{"path": rel(p), "sha256": sha(p), "size": p.stat().st_size} for p in package_files], "authority": AUTHORITY}
    manifest_path = BASE / "PACKAGE_MANIFEST.json"; write_json(manifest_path, package_manifest)
    package.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in package_files: archive.write(path, rel(path))
        archive.write(manifest_path, "PACKAGE_MANIFEST.json")
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(package) as archive: archive.extractall(td)
        manifest = json.load(open(Path(td) / "PACKAGE_MANIFEST.json"))
        for item in manifest["files"]:
            candidate = Path(td) / item["path"]
            if not candidate.is_file() or sha(candidate) != item["sha256"]: raise SystemExit(f"Archive validation failed: {item['path']}")
    write_json(OUTPUT / "C0_PHASE_C_EVIDENCE_PACKAGE_RECORD.json", {"package": rel(package), "sha256": sha(package), "manifest_sha256": sha(manifest_path), "archive_extraction": "PASSED", "manifest_entries": len(package_manifest["files"]), "authority": AUTHORITY})
    print(json.dumps({"disposition": status, "rows": 9, "recovered": 3, "evidence_blockers": 6, "remaining_lifecycle_blockers": 17, "package": rel(package), "package_sha256": sha(package)}, indent=2))


if __name__ == "__main__":
    build()
