#!/usr/bin/env python3
import csv
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REQUIRED = ['EQUINESYNC_CURRENT_GOVERNANCE_AUTHORITY_LIFECYCLE_LOCK_ACCESSION_CUSTODY_AND_SUPERSESSION_REGISTER_V2_0.md', 'AUTHORITY_LIFECYCLE_REGISTER_GUIDE.md', 'AUTHORITY_LIFECYCLE_REGISTER.csv', 'AUTHORITY_LIFECYCLE_REGISTER.json', 'LIFECYCLE_CONFLICT_REGISTER.csv', 'SUPERSESSION_GRAPH.json', 'STALE_RECORD_REPORT.md', 'SOURCE_REGISTER.csv', 'PACKAGE_MANIFEST.json', 'CHECKSUMS.sha256']
FORBIDDEN = ("TO" + "DO", "T" + "BD")

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    errors = []
    for rel in REQUIRED:
        if not (BASE / rel).exists():
            errors.append(f"missing required file: {rel}")
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix == ".csv":
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        if path.suffix in {".md", ".csv", ".json", ".py"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            for marker in FORBIDDEN:
                if marker in text:
                    errors.append(f"forbidden marker {marker} in {path.relative_to(BASE)}")
    checksum_path = BASE / "CHECKSUMS.sha256"
    if checksum_path.exists():
        for line in checksum_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, rel_path = line.split(None, 1)
            rel_path = rel_path.strip()
            target = BASE / rel_path
            if not target.exists():
                errors.append(f"checksum target missing: {rel_path}")
            elif sha256(target) != digest:
                errors.append(f"checksum mismatch: {rel_path}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("DOCUMENT_04_VALIDATION_PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
