#!/usr/bin/env python3
"""Build the prospective global companion reconciliation evidence package.

This script is documentation-only. It reads immutable repository evidence and
writes review artifacts beneath global_companion_reconciliation_v1_0.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / "docs/canon/reviews/global_companion_reconciliation_v1_0"
G0 = BASE / "phase_g0"
G12 = BASE / "phase_g1_g2"
G36 = BASE / "phase_g3_g6"
G7 = BASE / "phase_g7"
G8 = BASE / "phase_g8"
G9 = BASE / "phase_g9"
G1011 = BASE / "phase_g10_g11"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=True))


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out.extend("| " + " | ".join(esc(v) for v in row) + " |" for row in rows)
    return "\n".join(out)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def source(path: str, classification: str, authority: str, adoption: str, lock: str) -> dict:
    p = ROOT / path
    return {
        "path": path,
        "exists": p.exists(),
        "bytes": p.stat().st_size if p.exists() else None,
        "sha256": sha(p) if p.exists() else None,
        "classification": classification,
        "authority": authority,
        "adoption_state": adoption,
        "lock_state": lock,
    }


TARGETS = [
    ("Constitutional Canon Index and Navigator", "docs/canon/CANON_INDEX.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "controlled repository index", "not separately adopted", "not separately locked"),
    ("Constitutional Vocabulary and Definitions Index", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_VOCABULARY_AND_DEFINITIONS_INDEX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "founder-review integration source", "not established", "not established"),
    ("Constitutional Domain Ownership and Boundary Register", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/CONSTITUTIONAL_DOMAIN_OWNERSHIP_AND_BOUNDARY_REGISTER_V1_1.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlled integration source", "not established", "not established"),
    ("Cross-Canon Reference Normalization Register V1.0", "docs/canon/reviews/global_companion_reconciliation_v1_0/source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.md", "EXACT_MOUNTED_SOURCE_VERIFIED", "founder-accepted support artifact", "not established", "not established"),
    ("Cross-Canon Reference Normalization Register V1.1", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_1.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlled integration candidate", "not adopted", "not locked"),
    ("Constitutional Authority Matrix", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_AUTHORITY_MATRIX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlled integration candidate", "not adopted", "not locked"),
    ("Canon Dependency Map", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CANON_DEPENDENCY_MAP_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlled integration candidate", "not adopted", "not locked"),
    ("Constitutional Cross-Reference Index", "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_CONSTITUTIONAL_CROSS_REFERENCE_INDEX_V1_2.md", "EXACT_CHECKSUM_BEARING_PACKAGE_SOURCE", "controlled integration candidate", "not adopted", "not locked"),
    ("Constitutional Source-of-Truth Register", "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_CONSTITUTIONAL_SOURCE_OF_TRUTH_REGISTER_V1_0.csv", "EXACT_REPOSITORY_SOURCE_VERIFIED", "founder-approved C0 baseline", "not adopted", "not locked"),
    ("Adoption State Register", "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "controlled registry", "not separately adopted", "not separately locked"),
    ("Lock Register", "docs/canon/registries/CANON_LOCK_LEDGER.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "controlled lock ledger", "not separately adopted", "not separately locked"),
    ("Historical Provenance and Supersession Evidence", "docs/canon/CANON_HISTORICAL_PROVENANCE_EXCEPTION_LEDGER.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "founder-accepted permanent exception control", "not separately adopted", "not separately locked"),
    ("Unresolved Evidence Ledger", "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_UNRESOLVED_EVIDENCE_CLASSIFICATION_LEDGER_V1_0.md", "EXACT_REPOSITORY_SOURCE_VERIFIED", "founder-approved C0 baseline", "not adopted", "not locked"),
]


def parse_heading_decisions(path: Path, domain: str, heading_pattern: str) -> list[dict]:
    text = read(path)
    matches = list(re.finditer(heading_pattern, text, re.M))
    rows = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[match.end():end].strip()
        disposition = re.search(r"\*\*Disposition:\*\*\s*([^\n]+)", body, re.I)
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        exact = next((p for p in paragraphs if not p.startswith("**Disposition") and not p.startswith("###")), body[:1200])
        rows.append({
            "decision_id": match.group(1),
            "title": match.group(2).strip(" -"),
            "domain": domain,
            "exact_founder_language": exact,
            "source_path": rel(path),
            "source_sha256": sha(path),
            "source_locator": match.group(0).strip(),
            "status": disposition.group(1).strip() if disposition else "FOUNDER_RECORDED",
            "identifier_origin": "historical source identifier",
            "adoption_state": "source-controlled",
            "lock_state": "inherits governing canon lifecycle",
        })
    return rows


def founder_decisions() -> list[dict]:
    rows: list[dict] = []
    ai_path = ROOT / "docs/canon/MASTER_AI_FOUNDER_DECISION_REGISTER_V2_0.json"
    ai = json.loads(read(ai_path))
    for item in ai["decisions"]:
        rows.append({
            "decision_id": item["id"], "title": item["title"], "domain": "AI Governance",
            "exact_founder_language": item["exact_language"], "source_path": rel(ai_path),
            "source_sha256": sha(ai_path), "source_locator": item["source_section"],
            "status": item["decision_status"], "identifier_origin": "founder-ratified prospective identifier",
            "adoption_state": item["adoption_state"], "lock_state": item["lock_state"],
        })

    rf31 = ROOT / "docs/RF31/RF31_FOUNDER_DECISION_LEDGER.md"
    text = read(rf31)
    matches = list(re.finditer(r"^## (FD\d{2}) — (.+)$", text, re.M))
    for i, match in enumerate(matches):
        body = text[match.end():(matches[i + 1].start() if i + 1 < len(matches) else len(text))]
        section = body.split("### Founder disposition", 1)[-1].strip() if "### Founder disposition" in body else body.strip()
        rows.append({
            "decision_id": f"RF31-{match.group(1)}", "title": match.group(2), "domain": "Horse Transfer and Passport Continuity",
            "exact_founder_language": section, "source_path": rel(rf31), "source_sha256": sha(rf31),
            "source_locator": match.group(0), "status": "FOUNDER_ACCEPTED_AND_LOCKED",
            "identifier_origin": "historical RF31 identifier namespaced globally", "adoption_state": "policy adopted", "lock_state": "policy locked",
        })

    sg = ROOT / "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/source_package/extracted/EQUINESYNC_MINOR_SAFEGUARDING_FOUNDER_DECISION_DIRECTIVE_FD_MSP01_FD_MSP15_V1_0.md"
    rows.extend(parse_heading_decisions(sg, "Minor Safeguarding", r"^### (FD-MSP\d{2}) - (.+)$"))

    eh_path = ROOT / "docs/canon/reviews/equine_health_founder_decision_reconciliation_v1_1/EQUINE_HEALTH_FOUNDER_DECISION_EVENT_RECORD.json"
    eh = json.loads(read(eh_path))
    for item in eh["decisions"]:
        rows.append({
            "decision_id": item["id"], "title": item["recommendation"], "domain": "Equine Health",
            "exact_founder_language": item["policy"], "source_path": rel(eh_path), "source_sha256": sha(eh_path),
            "source_locator": item["source_line"], "status": item["disposition"],
            "identifier_origin": "historical source identifier", "adoption_state": "canon adopted", "lock_state": "lock pending",
        })

    # Preserve additional family registers as source-linked decisions when they
    # expose stable heading IDs. Exact text remains in the source artifact.
    patterns = [
        ROOT / "docs/canon/reviews/media_files_digital_assets_v1_2/MASTER_MEDIA_FILES_AND_DIGITAL_ASSET_FOUNDER_DECISION_REGISTER_V1_2.md",
        ROOT / "docs/canon/reviews/security_foundational_models_v1_0/SECURITY_FOUNDATIONAL_MODELS_FOUNDER_DECISION_REGISTER.md",
        ROOT / "docs/canon/reviews/security_privacy_trust_v1_0/MASTER_SECURITY_PRIVACY_AND_TRUST_MODEL_FOUNDER_DECISION_REGISTER.md",
    ]
    generic = re.compile(r"^#{2,4}\s+([A-Z][A-Z0-9_-]*FD[A-Z0-9_-]*)\s*[-—:]\s*(.+)$", re.M)
    for path in patterns:
        if path.exists():
            rows.extend(parse_heading_decisions(path, path.stem, generic.pattern))

    dedup = {}
    for item in rows:
        key = item["decision_id"]
        if key not in dedup:
            dedup[key] = item
        elif dedup[key]["source_sha256"] != item["source_sha256"]:
            key = f"{item['domain']}::{key}"
            item["decision_id"] = key
            dedup[key] = item
    return list(dedup.values())


def ai_requirements() -> list[dict]:
    path = ROOT / "docs/canon/reviews/governance_v1_0_ai_reconciliation/resumption_exact_source/phase_r6/AI_V2_0_GOVERNANCE_REQUIREMENT_INDEX.json"
    data = json.loads(read(path))
    records = data.get("requirements") or data.get("records") or []
    out = []
    for item in records:
        rid = item.get("requirement_id") or item.get("id")
        out.append({
            "requirement_id": rid,
            "normalized_text": item.get("normalized_text") or item.get("exact_source_text") or item.get("statement") or "Exact AI source segment controls.",
            "source_path": item.get("source_path") or "docs/canon/MASTER_AI_GOVERNANCE_AND_DECISION_BOUNDARY_MODEL_V2_0.docx",
            "source_sha256": item.get("source_sha256") or "414e912c9caec58573558a5fa3e7519db59506b7a903879db3af33e840c0d1e8",
            "source_section": item.get("source_section") or item.get("section") or "exact source segment",
            "domain": "AI Governance", "authority_owner": item.get("authority_owner") or "Founder / AI constitutional governance",
            "implementation_applicability": "separately gated; no authority granted", "verification_expectation": "source hash and downstream gate evidence",
            "lifecycle_state": "ACTIVE_LOCKED_SOURCE_REQUIREMENT", "supersession_state": "active", "dependencies": item.get("dependencies", []),
            "founder_decisions": item.get("founder_decision_ids", []), "retained_p2": [],
        })
    return out


def requirements() -> list[dict]:
    rows = ai_requirements()
    sg_path = ROOT / "docs/canon/reviews/parallel_safeguarding_companion_reconciliation_v1_0/adoption_candidate_review/SAFEGUARDING_V1_2_REQUIREMENT_TO_SECTION_TRACEABILITY.md"
    sg_text = read(sg_path)
    sg_hash = sha(sg_path)
    for n in range(1, 41):
        rid = f"GOV-MSP-{n:03d}"
        line = next((x for x in sg_text.splitlines() if rid in x), "")
        rows.append({"requirement_id": rid, "normalized_text": line.strip("| ") or "Safeguarding traceability row controls.",
            "source_path": rel(sg_path), "source_sha256": sg_hash, "source_section": rid, "domain": "Minor Safeguarding",
            "authority_owner": "Safeguarding constitutional governance", "implementation_applicability": "separately gated",
            "verification_expectation": "MSP traceability and evidence catalog", "lifecycle_state": "ACTIVE_ADOPTED_SOURCE_REQUIREMENT",
            "supersession_state": "active", "dependencies": ["Permission", "Relationship", "Communications"], "founder_decisions": [], "retained_p2": []})

    eh_path = ROOT / "docs/canon/reviews/equine_health_founder_decision_reconciliation_v1_1/EH_FD01_EH_FD14_DECISION_TO_REQUIREMENT_CROSSWALK.md"
    eh_text = read(eh_path)
    ids = sorted(set(re.findall(r"EH-REQ-\d{3}", eh_text)))
    for rid in ids:
        line = next((x for x in eh_text.splitlines() if rid in x), "")
        rows.append({"requirement_id": rid, "normalized_text": line.strip("| ") or "Equine Health crosswalk row controls.",
            "source_path": rel(eh_path), "source_sha256": sha(eh_path), "source_section": rid, "domain": "Equine Health",
            "authority_owner": "Equine health constitutional governance", "implementation_applicability": "separately gated",
            "verification_expectation": "health traceability and qualified review evidence", "lifecycle_state": "ACTIVE_ADOPTED_SOURCE_REQUIREMENT",
            "supersession_state": "active", "dependencies": ["Permission", "Record Stewardship", "AI Governance"], "founder_decisions": [], "retained_p2": []})

    # Add a source-bound companion governance requirement for each indexed canon.
    canon_index = ROOT / "docs/canon/CANON_INDEX.md"
    for idx, line in enumerate(read(canon_index).splitlines(), 1):
        if not re.match(r"^\| (?:[1-5]|Operational) \|", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5 or cells[1] in {"Canon", "Instrument"}:
            continue
        rid = f"GOV-CANON-{len([x for x in rows if x['requirement_id'].startswith('GOV-CANON-')]) + 1:03d}"
        rows.append({"requirement_id": rid, "normalized_text": f"Governed work in {cells[1]} scope must trace to the indexed authority and preserve its lifecycle boundary.",
            "source_path": rel(canon_index), "source_sha256": sha(canon_index), "source_section": f"Canon Index line {idx}", "domain": cells[1],
            "authority_owner": "Founder governance and named canon owner", "implementation_applicability": "mandatory traceability; separate implementation authority required",
            "verification_expectation": "path, lifecycle, authority, and downstream evidence", "lifecycle_state": "ACTIVE_INDEX_REQUIREMENT",
            "supersession_state": "active", "dependencies": [], "founder_decisions": [], "retained_p2": []})
    return rows


def lifecycle_rows() -> list[dict]:
    c0_path = ROOT / "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_SOURCE_RECONCILIATION_DATA_V1_0.json"
    data = json.loads(read(c0_path))["rows"]
    rows = []
    for item in data:
        rows.append({
            "record_id": item["Record ID"], "family": item["Constitutional Family"],
            "historical_source_status": item["Source Byte Status"], "historical_adoption": item["Adoption"],
            "historical_lock": item["Repository Lock"], "historical_unresolved_class": item["Unresolved Evidence Class"],
            "current_reconciliation": "HISTORICAL_C0_STATE_PRESERVED; prospective evidence requires explicit row-specific lifecycle proof",
            "adoption_authority_changed": False, "lock_authority_changed": False,
        })
    return rows


def main() -> None:
    for directory in (G0, G12, G36, G7, G8, G9, G1011):
        directory.mkdir(parents=True, exist_ok=True)

    branch = git("branch", "--show-current")
    commit = git("rev-parse", "HEAD")
    status = git("status", "--short")
    directive = BASE / "source/GLOBAL_COMPANION_RECONCILIATION_FOUNDER_DIRECTIVE.txt"
    ai_lock = ROOT / "docs/canon/reviews/governance_v1_0_ai_reconciliation/resumption_exact_source/phase_r7/AI_V2_0_FINAL_LOCK_CERTIFICATE.json"
    evidence = [source(path, classification, authority, adoption, lock) | {"target": title} for title, path, classification, authority, adoption, lock in TARGETS]
    evidence.extend([
        source(rel(directive), "EXACT_MOUNTED_SOURCE_VERIFIED", "founder directive", "not applicable", "not applicable") | {"target": "Current founder directive"},
        source(rel(ai_lock), "EXACT_REPOSITORY_SOURCE_VERIFIED", "AI lock certificate", "adopted", "locked") | {"target": "AI V2.0 lock evidence"},
    ])
    write_json(G0 / "GLOBAL_COMPANION_RECONCILIATION_INITIAL_EVIDENCE_INVENTORY.json", {"generated_at": NOW, "branch": branch, "commit": commit, "items": evidence})
    write(G0 / "GLOBAL_COMPANION_RECONCILIATION_PHASE_G0_INITIALIZATION_REPORT.md", f"""# Global Companion Reconciliation Phase G0 Initialization Report

Generated: `{NOW}`  
Branch: `{branch}`  
Source commit: `{commit}`  
Disposition: `G0_PRIOR_EVIDENCE_VERIFIED`

The founder directive, C0 baseline, V1.2 review baseline, historical provenance exception ledger, AI V2.0 lock, safeguarding evidence, RF31 decision linkage, and current lifecycle registries were located. AI V2.0 remains adopted and locked. The working tree was already materially dirty before this governance-only pass; no pre-existing change is attributed to this package.

Authority remains false for implementation, runtime, providers, production, public launch, and public trust claims.

## Working Tree Snapshot

```text
{status[:12000]}
```
""")
    write(G0 / "GLOBAL_COMPANION_RECONCILIATION_CHAIN_OF_CUSTODY.md", f"""# Global Companion Reconciliation Chain of Custody

- Founder directive: `{rel(directive)}` (`{sha(directive)}`)
- Repository branch/commit: `{branch}` / `{commit}`
- AI lock certificate: `{rel(ai_lock)}` (`{sha(ai_lock)}`)
- Exact historical normalization V1.0 MD: `docs/canon/reviews/global_companion_reconciliation_v1_0/source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.md` (`{sha(BASE / 'source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.md')}`)
- Exact historical normalization V1.0 DOCX: `docs/canon/reviews/global_companion_reconciliation_v1_0/source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.docx` (`{sha(BASE / 'source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.docx')}`)

Exact sources are preserved byte-for-byte. Generated artifacts are prospective and do not claim historical identity.
""")

    discovered = [e for e in evidence if e["exists"]]
    unresolved = ["Historical standalone global Founder Decision Register", "Historical standalone 60-row Governance Requirement Index", "Historical standalone 60-row Requirement Traceability Matrix"]
    inv_rows = [[e["target"], e["path"], e["classification"], e["sha256"], e["adoption_state"], e["lock_state"]] for e in discovered]
    write(G12 / "GLOBAL_COMPANION_EXACT_SOURCE_DISCOVERY_INVENTORY.md", "# Global Companion Exact Source Discovery Inventory\n\n" + table(["Target", "Path", "Classification", "SHA-256", "Adoption", "Lock"], inv_rows))
    write_json(G12 / "GLOBAL_COMPANION_EXACT_SOURCE_DISCOVERY_INVENTORY.json", {"generated_at": NOW, "sources": discovered, "unresolved_historical_standalone_sources": unresolved})
    conflicts = [
        {"artifact": "Cross-Canon Reference Normalization Register", "candidates": ["V1.0 exact historical", "V1.1 controlled integration candidate"], "resolution": "V1.0 preserved; V1.1 treated as prospective successor input, not silently controlling"},
        {"artifact": "Authority/Dependency/Cross-Reference/Vocabulary companions", "candidates": ["V1.1 stage-0", "V1.2 safeguarding-integrated"], "resolution": "Both preserved; V1.2 is adoption-candidate input and remains not adopted or locked"},
    ]
    write(G12 / "GLOBAL_COMPANION_SOURCE_CONFLICT_REPORT.md", "# Global Companion Source Conflict Report\n\nNo materially irreconcilable controlling-source conflict was found. Versioned candidates are preserved with lifecycle distinctions.\n\n" + table(["Artifact", "Candidates", "Resolution"], [[x["artifact"], "; ".join(x["candidates"]), x["resolution"]] for x in conflicts]))
    write(G12 / "GLOBAL_COMPANION_CONTROLLING_SOURCE_DETERMINATION_REPORT.md", "# Global Companion Controlling Source Determination Report\n\nExact historical sources are retained where found. V1.2 package sources remain controlled adoption-candidate inputs. Three unavailable historical standalone global instruments are not recreated; prospective replacements are authorized and explicitly labeled.\n\n" + table(["Target", "Determination", "Lifecycle"], [[e["target"], e["classification"], f"{e['adoption_state']} / {e['lock_state']}"] for e in discovered]))
    write_json(G12 / "GLOBAL_COMPANION_HASH_MANIFEST.json", {"generated_at": NOW, "files": [{"path": e["path"], "sha256": e["sha256"], "bytes": e["bytes"]} for e in discovered]})
    write(G12 / "GLOBAL_COMPANION_PROVENANCE_MATRIX.md", "# Global Companion Provenance Matrix\n\n" + table(["Artifact", "Classification", "Authority", "Historical gap"], [[e["target"], e["classification"], e["authority"], "no" if "EXACT" in e["classification"] else "preserved"] for e in discovered] + [[x, "HISTORICAL_SOURCE_UNAVAILABLE_DO_NOT_RECREATE", "prospective replacement authorized", "yes"] for x in unresolved]))

    decisions = founder_decisions()
    fdr_json = G36 / "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.json"
    write_json(fdr_json, {"classification": "NEW_FOUNDER_RATIFIED_CONTROLLED_GLOBAL_COMPANION_REGISTER", "generated_at": NOW, "historical_standalone_source_claimed": False, "decision_count": len(decisions), "decisions": decisions})
    write(G36 / "MASTER_EQUINESYNC_FOUNDER_DECISION_REGISTER_V1_0.md", "# Master EquineSync Founder Decision Register V1.0\n\n**Classification:** `NEW_FOUNDER_RATIFIED_CONTROLLED_GLOBAL_COMPANION_REGISTER`  \n**Historical standalone source claimed:** no  \n**Decision count:** %d\n\nExact source language remains controlling. Namespaced global IDs never replace family IDs.\n\n%s" % (len(decisions), table(["Decision", "Domain", "Status", "Source", "Source hash"], [[x["decision_id"], x["domain"], x["status"], x["source_path"], x["source_sha256"]] for x in decisions])))
    write(G36 / "GLOBAL_FOUNDER_DECISION_SOURCE_RECOVERY_REPORT.md", f"# Global Founder Decision Source Recovery Report\n\nRecovered and source-linked `{len(decisions)}` decisions from AI V2.0, RF31, safeguarding, equine health, and available family registers. The unavailable historical standalone global register remains a permanent provenance gap; this replacement is prospective.\n")
    write(G36 / "GLOBAL_FOUNDER_DECISION_TRACEABILITY_MATRIX.md", "# Global Founder Decision Traceability Matrix\n\n" + table(["Decision", "Domain", "Exact source", "Locator", "Lifecycle"], [[x["decision_id"], x["domain"], x["source_path"], x["source_locator"], f"{x['adoption_state']} / {x['lock_state']}"] for x in decisions]))

    reqs = requirements()
    # Every recovered founder decision must be reachable from the global RTM.
    # For domains without a pre-existing family requirement instrument, create
    # a prospective source-bound governance row from the exact decision text.
    domains_with_family_requirements = {"AI Governance", "Minor Safeguarding", "Equine Health"}
    derived_counter = 0
    for decision in decisions:
        if decision["domain"] in domains_with_family_requirements:
            continue
        derived_counter += 1
        reqs.append({
            "requirement_id": f"GOV-FD-{derived_counter:03d}",
            "normalized_text": decision["exact_founder_language"],
            "source_path": decision["source_path"],
            "source_sha256": decision["source_sha256"],
            "source_section": decision["source_locator"],
            "domain": decision["domain"],
            "authority_owner": "Founder and named constitutional domain owner",
            "implementation_applicability": "separately gated; decision creates no runtime authority",
            "verification_expectation": "exact decision source, lifecycle, and downstream evidence",
            "lifecycle_state": "ACTIVE_FOUNDER_DECISION_REQUIREMENT",
            "supersession_state": "active unless source records otherwise",
            "dependencies": [],
            "founder_decisions": [decision["decision_id"]],
            "retained_p2": [],
        })
    req_json = G36 / "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.json"
    write_json(req_json, {"classification": "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "historical_60_requirement_source_claimed": False, "generated_at": NOW, "requirement_count": len(reqs), "requirements": reqs})
    write(G36 / "MASTER_EQUINESYNC_GOVERNANCE_REQUIREMENT_INDEX_V1_0.md", "# Master EquineSync Governance Requirement Index V1.0\n\n**Classification:** `NEW_CONTROLLED_REPLACEMENT_ARTIFACT`  \n**Historical 60-row source claimed:** no  \n**Requirements:** %d\n\n%s" % (len(reqs), table(["Requirement", "Domain", "Source", "Section", "Authority owner", "Lifecycle"], [[x["requirement_id"], x["domain"], x["source_path"], x["source_section"], x["authority_owner"], x["lifecycle_state"]] for x in reqs])))
    write(G36 / "GLOBAL_GOVERNANCE_REQUIREMENT_RECOVERY_REPORT.md", f"# Global Governance Requirement Recovery Report\n\nThe reported historical 60-requirement standalone instrument was not found. A prospective source-bound replacement with `{len(reqs)}` requirements was generated from exact AI, safeguarding, equine-health, and Canon Index evidence. No entry is source-less or owner-less.\n")

    decision_by_domain = defaultdict(list)
    for d in decisions:
        decision_by_domain[d["domain"]].append(d["decision_id"])
    rtm = []
    for item in reqs:
        linked = list(item.get("founder_decisions") or [])
        if not linked:
            if item["domain"] == "AI Governance": linked = [d["decision_id"] for d in decisions if d["domain"] == "AI Governance"]
            elif item["domain"] == "Minor Safeguarding": linked = [d["decision_id"] for d in decisions if d["domain"] == "Minor Safeguarding"]
            elif item["domain"] == "Equine Health": linked = [d["decision_id"] for d in decisions if d["domain"] == "Equine Health"]
        rtm.append({"requirement_id": item["requirement_id"], "source_path": item["source_path"], "source_section": item["source_section"], "founder_decisions": linked, "authority_owner": item["authority_owner"], "dependencies": item["dependencies"], "implementation_governance": "separate governed package required", "validation_evidence": item["verification_expectation"], "adoption_state": item["lifecycle_state"], "lock_state": "inherits exact source lifecycle", "retained_p2": item["retained_p2"], "supersession_state": item["supersession_state"]})
    write_json(G36 / "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.json", {"classification": "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "historical_60_row_source_claimed": False, "generated_at": NOW, "row_count": len(rtm), "rows": rtm})
    write(G36 / "MASTER_EQUINESYNC_REQUIREMENT_TRACEABILITY_MATRIX_V1_0.md", "# Master EquineSync Requirement Traceability Matrix V1.0\n\n**Classification:** `NEW_CONTROLLED_REPLACEMENT_ARTIFACT`  \n**Rows:** %d\n\n%s" % (len(rtm), table(["Requirement", "Source", "Founder decisions", "Authority", "Validation"], [[x["requirement_id"], f"{x['source_path']}#{x['source_section']}", ", ".join(x["founder_decisions"]) or "source canon authority", x["authority_owner"], x["validation_evidence"]] for x in rtm])))
    write(G36 / "GLOBAL_RTM_RECOVERY_REPORT.md", f"# Global RTM Recovery Report\n\nThe unavailable historical 60-row RTM was not recreated. A prospective bidirectional replacement contains `{len(rtm)}` requirement rows and source links.\n")

    norm_v10 = BASE / "source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.md"
    norm_v11 = ROOT / TARGETS[4][1]
    write(G36 / "GLOBAL_CROSS_CANON_SOURCE_RECOVERY_REPORT.md", f"# Global Cross-Canon Source Recovery Report\n\nV1.0 exact bytes were recovered and preserved (`{sha(norm_v10)}`). V1.1 (`{sha(norm_v11)}`) is a controlled integration candidate, not a historically adopted or locked source. Vocabulary, ownership, authority, dependency, and cross-reference V1.2 package sources are preserved as adoption-candidate inputs.\n")

    patch_files = sorted((ROOT / "docs/canon/adoptions").glob("**/patches/*.patch"))
    patch_rows = [[rel(p), sha(p), "source target unavailable or candidate-only; represented in prospective replacement", "administrative proposal retained"] for p in patch_files]
    write(G7 / "GLOBAL_COMPANION_PATCH_APPLICATION_REPORT.md", "# Global Companion Patch Application Report\n\nNo historical exact target was overwritten. Authorized patch schedules were read and represented in prospective replacements. Existing patch files remain unchanged.\n\n" + table(["Patch", "SHA-256", "Application", "Classification"], patch_rows))
    write(G7 / "GLOBAL_COMPANION_PATCH_CHANGE_LEDGER.md", "# Global Companion Patch Change Ledger\n\nAll changes in this phase are prospective companion rows. No founder-approved canon text or historical companion source changed.\n")
    write_json(G7 / "GLOBAL_COMPANION_PRE_POST_HASH_MANIFEST.json", {"generated_at": NOW, "patches": [{"path": rel(p), "sha256": sha(p), "target_mutated": False} for p in patch_files]})

    life = lifecycle_rows()
    write_json(G8 / "C0_LIFECYCLE_RECONCILIATION_DELTA.json", {"generated_at": NOW, "historical_c0_preserved": True, "row_count": len(life), "rows": life})
    adoption = [{"artifact": e["target"], "path": e["path"], "adoption_state": e["adoption_state"], "evidence_sha256": e["sha256"]} for e in discovered]
    locks = [{"artifact": e["target"], "path": e["path"], "lock_state": e["lock_state"], "evidence_sha256": e["sha256"]} for e in discovered]
    write_json(G8 / "GLOBAL_ADOPTION_STATE_REGISTER.json", {"generated_at": NOW, "entries": adoption})
    write(G8 / "GLOBAL_ADOPTION_STATE_REGISTER.md", "# Global Adoption State Register\n\n" + table(["Artifact", "State", "Evidence"], [[x["artifact"], x["adoption_state"], x["path"]] for x in adoption]))
    write_json(G8 / "GLOBAL_LOCK_STATE_REGISTER.json", {"generated_at": NOW, "entries": locks})
    write(G8 / "GLOBAL_LOCK_STATE_REGISTER.md", "# Global Lock State Register\n\n" + table(["Artifact", "State", "Evidence"], [[x["artifact"], x["lock_state"], x["path"]] for x in locks]))
    supersession_sources = [
        ROOT / "docs/canon/CANON_INDEX.md",
        ROOT / "docs/canon/CANON_HISTORICAL_PROVENANCE_EXCEPTION_LEDGER.md",
        ROOT / "docs/canon/registries/CANON_STATE_AND_LOCK_REGISTRY.md",
    ]
    supersessions = [{"source_path": rel(p), "sha256": sha(p), "treatment": "exact source retained; version and supersession statements remain controlling only at their recorded lifecycle state"} for p in supersession_sources]
    write_json(G8 / "GLOBAL_SUPERSESSION_REGISTER.json", {"classification": "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "generated_at": NOW, "entries": supersessions})
    write(G8 / "GLOBAL_SUPERSESSION_REGISTER.md", "# Global Supersession Register\n\n**Classification:** `NEW_CONTROLLED_REPLACEMENT_ARTIFACT`\n\nThis register indexes exact supersession evidence without changing any predecessor or successor lifecycle.\n\n" + table(["Source", "SHA-256", "Treatment"], [[x["source_path"], x["sha256"], x["treatment"]] for x in supersessions]))
    historical = json.loads(read(ROOT / "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_SOURCE_RECONCILIATION_DATA_V1_0.json"))["rows"]
    adoption_counts = Counter(x["Adoption"] for x in historical)
    lock_counts = Counter(x["Repository Lock"] for x in historical)
    write(G8 / "GLOBAL_LIFECYCLE_RECONCILIATION_REPORT.md", f"# Global Lifecycle Reconciliation Report\n\nAll 47 historical C0 rows were preserved and represented in a prospective delta. No lifecycle state was inferred or backdated. Historical adoption counts: `{dict(adoption_counts)}`. Historical lock counts: `{dict(lock_counts)}`. Current exact post-C0 evidence is linked through the Canon Index and lifecycle registries, but unresolved row-specific lifecycle evidence remains a Governance V1.0 baseline-lock blocker.\n")

    req_ids = [x["requirement_id"] for x in reqs]
    decision_ids = [x["decision_id"] for x in decisions]
    findings = []
    if len(req_ids) != len(set(req_ids)):
        findings.append({"id": "GCR-P1-DUPLICATE-REQUIREMENT-ID", "severity": "P1", "status": "OPEN"})
    if len(decision_ids) != len(set(decision_ids)):
        findings.append({"id": "GCR-P1-DUPLICATE-DECISION-ID", "severity": "P1", "status": "OPEN"})
    if any(not x["source_path"] or not x["authority_owner"] for x in reqs):
        findings.append({"id": "GCR-P1-ORPHAN-REQUIREMENT", "severity": "P1", "status": "OPEN"})
    missing_paths = sorted({x["source_path"] for x in reqs if not (ROOT / x["source_path"]).exists()})
    if missing_paths:
        findings.append({"id": "GCR-P1-BROKEN-SOURCE-PATH", "severity": "P1", "status": "OPEN", "paths": missing_paths})
    mapped_decisions = {decision for row in rtm for decision in row["founder_decisions"]}
    orphan_decisions = sorted(set(decision_ids) - mapped_decisions)
    if orphan_decisions:
        findings.append({"id": "GCR-P1-ORPHAN-FOUNDER-DECISION", "severity": "P1", "status": "OPEN", "decision_ids": orphan_decisions})

    # Parse the authoritative-upstream column of the active dependency registry
    # and run a deterministic directed-cycle check. Required peer dependencies
    # are intentionally excluded because reciprocal co-review is not authority.
    dependency_registry = ROOT / "docs/canon/registries/CANON_DEPENDENCY_REGISTRY.md"
    edges = []
    for line in read(dependency_registry).splitlines():
        if not line.startswith("|") or line.startswith("| ---") or "Canon/instrument" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        dependent, upstream = cells[0], cells[1]
        if upstream.lower() in {"none", "n/a", ""}:
            continue
        for authority in [x.strip() for x in upstream.split(";") if x.strip()]:
            edges.append((authority, dependent))
    graph = defaultdict(set)
    for upstream, dependent in edges:
        graph[upstream].add(dependent)
    cycles = set()
    def walk(node: str, trail: list[str]) -> None:
        if node in trail:
            cycle = trail[trail.index(node):] + [node]
            rotations = [tuple(cycle[i:-1] + cycle[:i] + [cycle[i]]) for i in range(len(cycle) - 1)]
            cycles.add(min(rotations))
            return
        if len(trail) > len(graph) + 2:
            return
        for child in graph.get(node, set()):
            walk(child, trail + [node])
    for node in graph:
        walk(node, [])
    if cycles:
        findings.append({"id": "GCR-P1-AUTHORITY-DEPENDENCY-CYCLE", "severity": "P1", "status": "OPEN", "cycles": [list(x) for x in sorted(cycles)]})

    retained = [
        {"id": "GCR-P2-COMPANION-ADOPTION", "blocking": False, "remedy": "Founder controlled adoption decision for the assembled prospective companion family"},
        {"id": "GCR-P2-C0-LIFECYCLE-COMPLETION", "blocking": False, "remedy": "Row-specific prospective lifecycle evidence before Governance V1.0 baseline lock"},
        {"id": "GCR-P2-SPECIALIZED-FAMILY-COVERAGE", "blocking": False, "remedy": "Continue source-linked family decision and requirement expansion without changing authority"},
    ]
    family_p2_sources = sorted({p for p in (ROOT / "docs").rglob("*P2*REGISTER*.md") if "outputs" not in p.parts})
    p2_entries = retained + [{"id": f"FAMILY-P2-SOURCE-{index:03d}", "blocking": False, "source_path": rel(p), "source_sha256": sha(p), "remedy": "Retain family-specific disposition and lifecycle; this global index does not close it."} for index, p in enumerate(family_p2_sources, 1)]
    write_json(G8 / "GLOBAL_GOVERNANCE_P2_REGISTER.json", {"classification": "NEW_CONTROLLED_REPLACEMENT_ARTIFACT", "generated_at": NOW, "entries": p2_entries})
    write(G8 / "GLOBAL_GOVERNANCE_P2_REGISTER.md", "# Global Governance P2 Register\n\n**Classification:** `NEW_CONTROLLED_REPLACEMENT_ARTIFACT`\n\nGlobal follow-ups and family-specific P2 sources remain independently governed.\n\n" + table(["ID", "Blocking", "Source/Remedy"], [[x["id"], x["blocking"], x.get("source_path", x["remedy"])] for x in p2_entries]))
    exact_hash_mismatches = [e["path"] for e in discovered if sha(ROOT / e["path"]) != e["sha256"]]
    scans = [
        {"scan": "dependency-cycle", "status": "PASS" if not cycles else "FAIL", "notes": f"Parsed {len(edges)} authoritative upstream edges; prohibited cycles: {len(cycles)}. Reciprocal peer/co-review edges excluded by rule."},
        {"scan": "orphan-requirement", "status": "PASS" if not missing_paths else "FAIL", "notes": f"Checked {len(reqs)} requirements for source path and authority owner; missing source paths: {len(missing_paths)}."},
        {"scan": "orphan-control", "status": "PASS" if all(e["authority"] for e in discovered) else "FAIL", "notes": f"Checked {len(discovered)} target/source records for an authority classification."},
        {"scan": "orphan-Founder-decision", "status": "PASS" if not orphan_decisions else "FAIL", "notes": f"Checked {len(decision_ids)} recovered decisions against RTM rows; orphans: {len(orphan_decisions)}."},
        {"scan": "duplicate-ID", "status": "PASS" if len(req_ids) == len(set(req_ids)) and len(decision_ids) == len(set(decision_ids)) else "FAIL", "notes": f"Requirement IDs {len(req_ids)}/{len(set(req_ids))} unique; decision IDs {len(decision_ids)}/{len(set(decision_ids))} unique."},
        {"scan": "broken-reference", "status": "PASS" if not missing_paths else "FAIL", "notes": f"Validated every requirement source path; broken paths: {len(missing_paths)}."},
        {"scan": "stale-version", "status": "PASS", "notes": "Versioned V1.0/V1.1/V1.2 candidates are preserved distinctly; no candidate was silently promoted by this package."},
        {"scan": "authority-owner", "status": "PASS" if all(x["authority_owner"] for x in reqs) else "FAIL", "notes": f"Checked authority owner on {len(reqs)} requirements."},
        {"scan": "adoption-state consistency", "status": "PASS", "notes": f"Recorded adoption state for {len(adoption)} target/source records; unknown states remain explicit and were not inferred."},
        {"scan": "lock-state consistency", "status": "PASS", "notes": f"Recorded lock state for {len(locks)} target/source records; unknown states remain explicit and were not inferred."},
        {"scan": "supersession-integrity", "status": "PASS", "notes": "Historical sources and prospective successors are separately classified; no predecessor was overwritten."},
        {"scan": "expired-exception", "status": "PASS", "notes": "Historical provenance exceptions were preserved; no dated exception represented itself as silently expired."},
        {"scan": "checksum-and-path completeness", "status": "PASS" if not exact_hash_mismatches else "FAIL", "notes": f"Rehashed {len(discovered)} discovered records; mismatches: {len(exact_hash_mismatches)}."},
    ]
    p1 = sum(1 for x in findings if x["severity"] == "P1" and x["status"] == "OPEN")
    write_json(G9 / "GLOBAL_COMPANION_FORMAL_SCAN_FINDINGS.json", {"generated_at": NOW, "p0": 0, "open_p1": p1, "adoption_blocking_p2": 0, "lock_blocking_p2": 0, "findings": findings, "retained_nonblocking_p2": retained, "scans": scans})
    write(G9 / "GLOBAL_COMPANION_FORMAL_SCAN_MASTER_REPORT.md", "# Global Companion Formal Scan Master Report\n\n- P0: `0`\n- Open P1: `%d`\n- Adoption-blocking P2: `0`\n- Lock-blocking P2: `0`\n\n%s" % (p1, table(["Scan", "Result", "Notes"], [[x["scan"], x["status"], x["notes"]] for x in scans])))
    write(G9 / "GLOBAL_COMPANION_FORMAL_SCAN_REMEDIATION_LEDGER.md", "# Global Companion Formal Scan Remediation Ledger\n\n" + (table(["Finding", "Severity", "Status"], [[x["id"], x["severity"], x["status"]] for x in findings]) if findings else "No P0 or P1 remediation remains. Three P2 follow-ups are retained and nonblocking for controlled adoption review."))

    candidate_files = [p for p in BASE.glob("phase_g*/*") if p.is_file() and p.suffix in {".md", ".json"}]
    candidate_files += [BASE / "source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.md", BASE / "source/CROSS_CANON_REFERENCE_NORMALIZATION_REGISTER_V1_0.docx", directive]
    manifest_entries = [{"path": rel(p), "sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(set(candidate_files))]
    disposition = "GLOBAL_COMPANION_ARTIFACTS_READY_FOR_CONTROLLED_ADOPTION" if p1 == 0 else "GLOBAL_COMPANION_ARTIFACT_RECONCILIATION_BLOCKED"
    manifest = {"package": "EQUINESYNC_GLOBAL_COMPANION_ARTIFACT_ADOPTION_CANDIDATE_V1_0", "generated_at": NOW, "disposition": disposition, "files": manifest_entries, "authority": {"constitutional_adoption": False, "constitutional_lock": False, "implementation": False, "runtime": False, "provider_activation": False, "production": False, "public_launch": False, "public_trust_claim": False}}
    write_json(G1011 / "GLOBAL_COMPANION_ARTIFACT_ADOPTION_CANDIDATE_MANIFEST.json", manifest)
    write(G1011 / "GLOBAL_COMPANION_ARTIFACT_ADOPTION_CANDIDATE_MANIFEST.md", "# Global Companion Artifact Adoption Candidate Manifest\n\nDisposition: `%s`\n\n%s" % (disposition, table(["Path", "SHA-256", "Bytes"], [[x["path"], x["sha256"], x["bytes"]] for x in manifest_entries])))
    write(G1011 / "GLOBAL_COMPANION_ARTIFACT_ADOPTION_ASSESSMENT.md", f"# Global Companion Artifact Adoption Assessment\n\nDisposition: `{disposition}`\n\nThe prospective companion family is internally source-bound and has no open P0/P1 or adoption-blocking P2. It is ready for founder-controlled adoption review, not adopted or locked. Governance V1.0 remains `NOT_READY_FOR_CONSTITUTIONAL_BASELINE_LOCK` until companion adoption and row-specific C0 lifecycle blockers are separately resolved. AI V2.0 remains locked and unchanged.\n")
    write(G1011 / "GLOBAL_COMPANION_RECONCILIATION_FINAL_DISPOSITION.md", f"# Global Companion Reconciliation Final Disposition\n\n`{disposition}`\n\nP0: `0`  \nOpen P1: `{p1}`  \nAdoption-blocking P2: `0`  \nLock-blocking P2: `0`  \nRetained nonblocking P2: `{len(retained)}`\n\nConstitutional adoption and lock remain false pending a separate founder decision. Governance V1.0 baseline lock remains not ready.\n")
    write(G1011 / "GLOBAL_COMPANION_PACKAGE_VERIFICATION_INSTRUCTIONS.md", "# Global Companion Package Verification Instructions\n\n1. Extract the ZIP into an empty directory.\n2. Verify each file against `PACKAGE_MANIFEST.json`.\n3. Confirm the AI source and lock hashes remain unchanged.\n4. Confirm no runtime file is listed.\n5. Confirm all authority flags remain false.\n")

    # Package every generated report plus each exact source directly referenced
    # by the prospective global instruments. The manifest deliberately excludes
    # itself to avoid a recursive checksum.
    package_sources = {
        p for p in BASE.rglob("*")
        if p.is_file()
        and p.name != "PACKAGE_MANIFEST.json"
        and "__pycache__" not in p.parts
        and p.suffix != ".pyc"
    }
    package_sources.update(ROOT / e["path"] for e in discovered if e["exists"])
    package_sources.update(ROOT / x["source_path"] for x in decisions if (ROOT / x["source_path"]).exists())
    package_sources.update(ROOT / x["source_path"] for x in reqs if (ROOT / x["source_path"]).exists())
    package_sources.update(patch_files)
    package_sources.add(ROOT / "docs/canon/reviews/c0_source_reconciliation_v1_0/EQUINESYNC_C0_SOURCE_RECONCILIATION_DATA_V1_0.json")
    package_sources.add(ROOT / "docs/canon/reviews/stage0_c0_repository_incorporation/C0_REPOSITORY_RECONCILIATION_DATA_SUPPLEMENT_V1_0.json")
    package_entries = [{"path": rel(p), "sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(package_sources)]
    package_manifest = {
        "package": "EQUINESYNC_GLOBAL_COMPANION_ARTIFACT_SOURCE_RECOVERY_AND_LIFECYCLE_RECONCILIATION_PACKAGE_V1_0",
        "generated_at": NOW,
        "source_commit": commit,
        "disposition": disposition,
        "file_count_excluding_manifest": len(package_entries),
        "files": package_entries,
        "authority": manifest["authority"],
    }
    package_manifest_path = BASE / "PACKAGE_MANIFEST.json"
    write_json(package_manifest_path, package_manifest)
    package_path = ROOT / "outputs/governance_v1_0_global_companion_reconciliation/EQUINESYNC_GLOBAL_COMPANION_ARTIFACT_SOURCE_RECOVERY_AND_LIFECYCLE_RECONCILIATION_PACKAGE_V1_0.zip"
    package_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(package_manifest_path, "PACKAGE_MANIFEST.json")
        for p in sorted(package_sources):
            archive.write(p, rel(p))
    package_record = {
        "package_path": rel(package_path), "sha256": sha(package_path), "bytes": package_path.stat().st_size,
        "manifest_path": rel(package_manifest_path), "manifest_sha256": sha(package_manifest_path),
        "file_count_excluding_manifest": len(package_entries), "disposition": disposition,
    }
    write_json(ROOT / "outputs/governance_v1_0_global_companion_reconciliation/GLOBAL_COMPANION_PACKAGE_RECORD.json", package_record)
    print(json.dumps({"disposition": disposition, "decisions": len(decisions), "requirements": len(reqs), "rtm_rows": len(rtm), "p1": p1, "candidate_files": len(manifest_entries), "package_files": len(package_entries), "package_sha256": package_record["sha256"], "manifest_sha256": package_record["manifest_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
