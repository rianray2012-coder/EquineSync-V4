#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def add(results, name, ok, detail):
    results.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("package_root", nargs="?")
    parser.add_argument("--package-root", dest="package_root_opt")
    parser.add_argument("--json-output")
    args = parser.parse_args()
    package = Path(args.package_root_opt or args.package_root or Path.cwd()).resolve()
    results = []
    failures = 0

    manifest = json.loads((package / "PACKAGE_MANIFEST.json").read_text())
    for item in manifest["files"]:
        path = package / item["path"]
        failures += add(results, f"root_manifest:{item['path']}", path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == item["byte_length"], "root manifest hash and byte-length binding")

    checksum_rows = [line.split(maxsplit=1) for line in (package / "CHECKSUMS.sha256").read_text().splitlines() if line.strip()]
    for digest, rel in checksum_rows:
        rel = rel[2:] if rel.startswith("./") else rel
        path = package / rel
        failures += add(results, f"root_checksum:{rel}", path.is_file() and sha(path) == digest, "root checksum binding")

    mom = rows(package / "MANIFEST_OF_MANIFESTS.csv")
    forbidden = {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256", "MANIFEST_OF_MANIFESTS.csv"}
    failures += add(results, "manifest_of_manifests_no_root_self_reference", not any(r["path"] in forbidden for r in mom), "root/self references excluded")
    failures += add(results, "manifest_of_manifests_only_manifest_checksum_files", all(Path(r["path"]).name in {"PACKAGE_MANIFEST.json", "CHECKSUMS.sha256"} for r in mom), "only per-directory manifest/checksum files")
    for item in mom:
        path = package / item["path"]
        failures += add(results, f"manifest_of_manifests:{item['path']}", path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == int(item["byte_length"]), "per-directory manifest/checksum binding")

    reg = rows(package / "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv")
    closure = package / "OUTSIDE_REVIEW/PER_FINDING_CLOSURE_EVIDENCE_REGISTER.csv"
    failures += add(results, "source_review_ids_populated", all("SOURCE_REVIEW_IDS_POPULATED" not in r["source_review_ids"] and "see consolidated" not in r["source_review_ids"] and r["source_review_ids"] for r in reg), "actual source review identifiers are populated")
    failures += add(results, "no_partial_remediated_status", all(r["current_target_disposition"] != "PARTIALLY_REMEDIATED" for r in reg), "ambiguous PARTIALLY_REMEDIATED status absent")
    failures += add(results, "closure_register_distinct", sha(closure) != sha(package / "OUTSIDE_REVIEW/T1C_CONSOLIDATED_FINDINGS_DISPOSITION_REGISTER.csv"), "closure evidence register is not a byte duplicate")
    failures += add(results, "doc10_dispute_retained_open", any(r["t1c_id"] == "T1C-004" and r["current_target_disposition"] == "NOT_REMEDIATED_RETAINED_OPEN" for r in reg), "Doc 10 dispute conservatively retained open")

    text_files = []
    excluded_scan_parts = {"SOURCE_REVIEWS", "VALIDATION", "VALIDATION_RESULTS"}
    for path in package.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".csv", ".md", ".json", ".txt", ".py"}:
            if any(part in excluded_scan_parts for part in path.relative_to(package).parts):
                continue
            try:
                text_files.append((path, path.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                pass
    failures += add(results, "no_eleven_state_wording", not any("eleven-state" in t or "Eleven-state" in t for _, t in text_files), "eleven-state wording absent")
    failures += add(results, "source_authority_label_scoped", not any("FOUNDER_APPROVAL_EVIDENCE_PRESENT" in t for _, t in text_files), "unsafe source authority label absent")
    failures += add(results, "authority_boundary_present", any("NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED" in t for _, t in text_files), "controlling boundary present")

    harness = package / "VALIDATION/execute_negative_fixtures_v3.py"
    harness_result = subprocess.run([sys.executable, str(harness), str(package)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    failures += add(results, "negative_fixtures_execute", harness_result.returncode == 0, harness_result.stdout if harness_result.returncode == 0 else harness_result.stderr)

    report = {
        "status": "PASS" if failures == 0 else "FAIL",
        "failures": failures,
        "package_root": str(package),
        "package_status": "REVISION_REQUIRED_PENDING_OUTSIDE_REVIEWER_REREVIEW",
        "authority_boundary": "NOT_ADOPTED; NOT_ACTIVE; IMPLEMENTATION_NOT_AUTHORIZED; PRODUCTION_USE_NOT_AUTHORIZED; MERGE_NOT_AUTHORIZED; CERTIFICATION_NOT_COMPLETE; FOUNDER_REVIEW_REQUIRED; UNRESOLVED_ITEMS_REMAIN_OPEN_AS_IDENTIFIED",
        "archive_hash_location": "detached .sha256 and reviewer handoff report generated after archive creation",
        "results": results,
    }
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.json_output:
        output = Path(args.json_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
