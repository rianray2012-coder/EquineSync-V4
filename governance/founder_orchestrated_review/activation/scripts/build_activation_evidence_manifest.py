#!/usr/bin/env python3
"""Build or verify the additive manifest for one activation evidence run."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[4]
ACTIVATION_DIR = SCRIPT_PATH.parent.parent
MANIFEST_NAME = "ACTIVATION_EVIDENCE_MANIFEST.json"
CHECKSUM_NAME = "ACTIVATION_EVIDENCE_CHECKSUMS.sha256"
CONTROLLED_ACTIVATION_FILES = [
    ACTIVATION_DIR / "CONTROLLED_ACTIVATION_PROCEDURE.md",
    ACTIVATION_DIR / "FOUNDER_ACTIVATION_DECISION.json",
    ACTIVATION_DIR / "FOUNDER_ACTIVATION_DECISION.schema.json",
    ACTIVATION_DIR / "FOUNDER_ACTIVATION_REVIEW_PACKAGE_STATUS.json",
    ACTIVATION_DIR / "scripts" / "run_post_activation_canaries.py",
    SCRIPT_PATH,
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def evidence_files(run_root: Path, excluded: set[str]) -> list[Path]:
    return [
        path
        for path in sorted(run_root.rglob("*"))
        if path.is_file() and path.name not in excluded
    ]


def manifest_targets(run_root: Path, excluded: set[str]) -> list[Path]:
    targets = [*CONTROLLED_ACTIVATION_FILES, *evidence_files(run_root, excluded)]
    return sorted({path.resolve() for path in targets if path.is_file()})


def build(run_root: Path) -> int:
    manifest_path = run_root / MANIFEST_NAME
    checksum_path = run_root / CHECKSUM_NAME
    entries = [
        {
            "path": path.relative_to(REPO_ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in manifest_targets(run_root, {MANIFEST_NAME, CHECKSUM_NAME})
    ]
    manifest = {
        "schema_version": "1.0.0",
        "activation_run_id": run_root.name,
        "generated_at": utc_now(),
        "manifest_self_included": False,
        "checksum_manifest_included": False,
        "scope": "All controlled activation status, decision, procedure, harness, report, raw-output, provenance, reconciliation, rollback, and run-evidence files changed or created by this activation attempt.",
        "entry_count": len(entries),
        "entries": entries,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    checksum_targets = manifest_targets(run_root, {CHECKSUM_NAME})
    checksum_path.write_text(
        "".join(
            f"{sha256(path)}  {path.relative_to(REPO_ROOT).as_posix()}\n"
            for path in checksum_targets
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "activation_run_id": run_root.name,
                "manifest_entries": len(entries),
                "checksum_entries": len(checksum_targets),
                "status": "BUILT",
            },
            sort_keys=True,
        )
    )
    return 0


def verify(run_root: Path) -> int:
    manifest_path = run_root / MANIFEST_NAME
    checksum_path = run_root / CHECKSUM_NAME
    errors = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"manifest read failed: {error}", file=sys.stderr)
        return 1
    for entry in manifest.get("entries", []):
        path = REPO_ROOT / entry.get("path", "")
        if not path.is_file():
            errors.append(f"missing manifest path: {entry.get('path')}")
            continue
        if path.stat().st_size != entry.get("bytes"):
            errors.append(f"size mismatch: {entry.get('path')}")
        if sha256(path) != entry.get("sha256"):
            errors.append(f"hash mismatch: {entry.get('path')}")
    checksum_lines = checksum_path.read_text(encoding="utf-8").splitlines()
    for line in checksum_lines:
        expected, separator, relative = line.partition("  ")
        if not separator:
            errors.append(f"invalid checksum line: {line}")
            continue
        path = REPO_ROOT / relative
        if not path.is_file():
            errors.append(f"missing checksum path: {relative}")
        elif sha256(path) != expected:
            errors.append(f"checksum mismatch: {relative}")
    expected_manifest_paths = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in manifest_targets(run_root, {MANIFEST_NAME, CHECKSUM_NAME})
    }
    actual_manifest_paths = {entry.get("path") for entry in manifest.get("entries", [])}
    if expected_manifest_paths != actual_manifest_paths:
        errors.append("manifest path set mismatch")
    expected_checksum_paths = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in manifest_targets(run_root, {CHECKSUM_NAME})
    }
    actual_checksum_paths = {
        line.partition("  ")[2] for line in checksum_lines if "  " in line
    }
    if expected_checksum_paths != actual_checksum_paths:
        errors.append("checksum path set mismatch")
    result = {
        "activation_run_id": run_root.name,
        "manifest_entries_verified": len(actual_manifest_paths),
        "checksum_entries_verified": len(actual_checksum_paths),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    run_root = args.run_root.resolve()
    if not run_root.is_dir():
        raise SystemExit(f"run root is not a directory: {run_root}")
    return verify(run_root) if args.verify else build(run_root)


if __name__ == "__main__":
    raise SystemExit(main())
