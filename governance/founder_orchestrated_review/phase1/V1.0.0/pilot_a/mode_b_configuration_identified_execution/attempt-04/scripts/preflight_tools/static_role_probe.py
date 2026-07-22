#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import time


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def denied_read(path: Path) -> dict[str, object]:
    try:
        path.read_bytes()
    except OSError as exc:
        return {"path": str(path), "denied": True, "errno": exc.errno, "error": type(exc).__name__}
    return {"path": str(path), "denied": False, "errno": 0, "error": "NONE"}


def denied_write(path: Path) -> dict[str, object]:
    try:
        path.write_text("PROHIBITED\n", encoding="utf-8")
    except OSError as exc:
        return {"path": str(path), "denied": True, "errno": exc.errno, "error": type(exc).__name__}
    return {"path": str(path), "denied": False, "errno": 0, "error": "NONE"}


def main() -> None:
    if len(sys.argv) != 10:
        raise SystemExit("usage: static_role_probe.py ROLE INPUT OUTPUT SIBLING_INPUT SIBLING_OUTPUT ORACLE SYNTHETIC_CREDENTIAL ORCHESTRATION UNRELATED")
    role_id = sys.argv[1]
    input_dir = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])
    sibling_input = Path(sys.argv[4])
    sibling_output = Path(sys.argv[5])
    oracle = Path(sys.argv[6])
    synthetic_credential = Path(sys.argv[7])
    orchestration = Path(sys.argv[8])
    unrelated = Path(sys.argv[9])

    own_canary = (input_dir / "ROLE_CANARY.txt").read_text(encoding="utf-8").strip()
    assigned = input_dir / "candidate" / "valid_policy.json"
    output_probe = output_dir / "A04_BOUNDARY_WRITE_PROBE.txt"
    output_probe.write_text(f"{role_id}|ASSIGNED_OUTPUT_ONLY\n", encoding="utf-8")
    result = {
        "schema_version": "1.0.0",
        "probe_id": f"A04-STATIC-ROLE-BOUNDARY-{role_id}",
        "role_id": role_id,
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "argv": sys.argv,
        "working_directory": os.getcwd(),
        "own_packet_read": True,
        "own_canary": own_canary,
        "known_answer_sha256": hashlib.sha256(b"abc").hexdigest(),
        "assigned_file_sha256": sha256(assigned),
        "assigned_output_write": output_probe.is_file(),
        "assigned_output_readback": output_probe.read_text(encoding="utf-8").strip(),
        "denials": {
            "input_write": denied_write(input_dir / "PROHIBITED_INPUT_WRITE.txt"),
            "sibling_input_read": denied_read(sibling_input / "ROLE_CANARY.txt"),
            "sibling_output_read": denied_read(sibling_output / "SIBLING_OUTPUT_CANARY.txt"),
            "hidden_oracle_read": denied_read(oracle),
            "synthetic_credential_read": denied_read(synthetic_credential),
            "orchestration_read": denied_read(orchestration),
            "unrelated_read": denied_read(unrelated),
            "unrelated_write": denied_write(unrelated.parent / "PROHIBITED_UNRELATED_WRITE.txt"),
        },
        "network_probe_performed": False,
        "network_disabled_environment": os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED") == "1",
        "actual_credential_path_referenced": False,
        "provider_or_model_operation_performed": False,
    }
    print(json.dumps(result, sort_keys=True))
    time.sleep(1.0)


if __name__ == "__main__":
    main()
