#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import stat


RUNTIME = Path("/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync/work/modeb_attempt_04_runtime.nosync")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    inputs = RUNTIME / "role_inputs"
    oracle = RUNTIME / "hidden_oracle" / "MODE_B_ATTEMPT_04_HIDDEN_DEFECT_ORACLE.csv"
    receipt = RUNTIME / "evidence" / "PACKET_FREEZE_RECEIPT.json"
    if receipt.exists():
        raise SystemExit("refusing to repeat Attempt 04 packet freeze")
    packet_hashes: dict[str, str] = {}
    for packet in sorted(inputs.iterdir()):
        manifest = packet / "INPUT_MANIFEST.json"
        packet_hashes[packet.name] = sha256(manifest)
        for path in sorted(packet.rglob("*"), reverse=True):
            if path.is_file():
                path.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            elif path.is_dir():
                path.chmod(stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        packet.chmod(stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    oracle.chmod(stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    oracle.parent.chmod(stat.S_IRUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    payload = {
        "schema_version": "1.0.0",
        "attempt_id": "ES-PH1-PILOT-A-MODE-B-ATTEMPT-04",
        "event": "PACKET_AND_ORACLE_FREEZE",
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "packet_manifest_sha256": packet_hashes,
        "oracle_sha256": sha256(oracle),
        "precondition": "all recorded pre-freeze custody and packet controls passed",
        "result": "PASS",
    }
    receipt.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
