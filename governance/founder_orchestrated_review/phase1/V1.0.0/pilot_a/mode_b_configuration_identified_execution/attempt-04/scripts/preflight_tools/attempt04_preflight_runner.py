#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone


BASE = Path("/Users/rianray/Documents/Codex/2026-07-21/files-mentioned-by-the-user-equinesync")
REPO = BASE / "work/modeb_attempt_04_execution.nosync/EquineSync-V4"
RUNTIME = BASE / "work/modeb_attempt_04_runtime.nosync"
TOOLING = BASE / "work/modeb_attempt_04_preflight.nosync"
ISOLATED_HOME = BASE / "work/modeb_attempt_04_isolated_codex_home.nosync"
ATTEMPT_ROOT = REPO / "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-04"
ATTEMPT03 = REPO / "governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-03"
PYTHON = Path("/Library/Frameworks/Python.framework/Versions/3.14/bin/python3")
PYTHON_ROOT = PYTHON.parents[1]
CODEX = Path("/Users/rianray/.npm-global/bin/codex")
PROBE = TOOLING / "static_role_probe.py"
START = "34c427c0196d3f8273ac3ea88ad05a2bbe5a2c29"
BRANCH = "codex/founder-review-phase1-pilot-a-mode-b-attempt-04-v1"
REMOTE = "https://github.com/EquineSync/EquineSync-V4.git"
ROLES = ("ES-RA-02", "ES-RA-03", "ES-RA-04", "ES-RA-05")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def process_snapshot(root_pid: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    argv = ["/bin/ps", "-axo", "pid=,ppid=,comm=,args="]
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = proc.communicate(timeout=10)
    rows: list[dict[str, object]] = []
    for raw in stdout.splitlines():
        parts = raw.strip().split(None, 3)
        if len(parts) != 4:
            continue
        try:
            pid, ppid = int(parts[0]), int(parts[1])
        except ValueError:
            continue
        rows.append({"pid": pid, "ppid": ppid, "comm": parts[2], "args": parts[3]})
    descendants = {root_pid}
    changed = True
    while changed:
        changed = False
        for row in rows:
            if row["ppid"] in descendants and row["pid"] not in descendants:
                descendants.add(int(row["pid"]))
                changed = True
    selected = [row for row in rows if row["pid"] in descendants]
    ps_record = {
        "argv": argv,
        "pid": proc.pid,
        "ppid": os.getpid(),
        "exit": proc.returncode,
        "stderr": stderr,
    }
    return selected, ps_record


def run_command(command_id: str, argv: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None, sample: bool = False) -> dict[str, object]:
    started = utc_now()
    proc = subprocess.Popen(
        argv,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    snapshots: list[list[dict[str, object]]] = []
    ps_commands: list[dict[str, object]] = []
    if sample:
        time.sleep(0.2)
        snap, ps_record = process_snapshot(proc.pid)
        snapshots.append(snap)
        ps_commands.append(ps_record)
        time.sleep(0.55)
        snap, ps_record = process_snapshot(proc.pid)
        snapshots.append(snap)
        ps_commands.append(ps_record)
    output, _ = proc.communicate(timeout=120)
    return {
        "command_id": command_id,
        "argv": argv,
        "cwd": str(cwd) if cwd else os.getcwd(),
        "pid": proc.pid,
        "ppid": os.getpid(),
        "started_at": started,
        "completed_at": utc_now(),
        "exit": proc.returncode,
        "output": output,
        "descendant_process_snapshots": snapshots,
        "process_snapshot_commands": ps_commands,
    }


def role_probe_argv(role: str) -> list[str]:
    index = ROLES.index(role)
    sibling = ROLES[(index + 1) % len(ROLES)]
    input_dir = RUNTIME / "role_inputs" / role
    output_dir = RUNTIME / "role_outputs" / role
    sibling_input = RUNTIME / "role_inputs" / sibling
    sibling_output = RUNTIME / "role_outputs" / sibling
    oracle = RUNTIME / "hidden_oracle/MODE_B_ATTEMPT_04_HIDDEN_DEFECT_ORACLE.csv"
    synthetic = RUNTIME / "synthetic_credential_canary/SYNTHETIC_CREDENTIAL_CANARY.txt"
    orchestration = RUNTIME / "orchestration_control/ORCHESTRATION_CANARY.txt"
    unrelated = RUNTIME / "unrelated_canary/UNRELATED_CANARY.txt"
    filesystem = (
        'permissions.attempt04_probe={filesystem={'
        f'":minimal"="read","{input_dir}"="read","{output_dir}"="write",'
        f'"{TOOLING}"="read","{PYTHON_ROOT}"="read"'
        '},network={enabled=false}}'
    )
    return [
        str(CODEX), "sandbox", "-P", "attempt04_probe", "-C", str(input_dir),
        "-c", filesystem,
        "-c", 'shell_environment_policy.inherit="none"',
        "--log-denials",
        str(PYTHON), str(PROBE), role, str(input_dir), str(output_dir),
        str(sibling_input), str(sibling_output), str(oracle), str(synthetic),
        str(orchestration), str(unrelated),
    ]


def validate_probe(record: dict[str, object], role: str) -> dict[str, object]:
    require(record["exit"] == 0, f"{role} sandbox process exit {record['exit']}")
    output = str(record["output"])
    payload_line = next((line for line in output.splitlines() if line.startswith("{")), None)
    require(payload_line is not None, f"{role} probe JSON absent")
    payload = json.loads(payload_line)
    require(payload["role_id"] == role, f"{role} identity mismatch")
    require(payload["own_packet_read"] is True, f"{role} own input failed")
    require(payload["assigned_output_write"] is True, f"{role} output write failed")
    require(payload["known_answer_sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad", f"{role} hash known-answer failed")
    require(all(item["denied"] is True for item in payload["denials"].values()), f"{role} prohibited boundary not denied")
    require(payload["network_probe_performed"] is False, f"{role} network probe unexpectedly performed")
    require(payload["network_disabled_environment"] is True, f"{role} network-disabled state absent")
    require(payload["actual_credential_path_referenced"] is False, f"{role} actual credential reference occurred")
    require(payload["provider_or_model_operation_performed"] is False, f"{role} provider/model operation occurred")
    denial_text = output.split("=== Sandbox denials ===", 1)[-1] if "=== Sandbox denials ===" in output else ""
    forbidden_network_markers = ("network-outbound", "network-inbound", "network-bind", "network-connect")
    require(not any(marker in denial_text.lower() for marker in forbidden_network_markers), f"{role} network denial proves an attempted network operation")
    return payload


def prepare_probe_canaries() -> None:
    for role in ROLES:
        path = RUNTIME / "role_outputs" / role / "SIBLING_OUTPUT_CANARY.txt"
        path.write_text(f"A04-SIBLING-OUTPUT-CANARY-{role}\n", encoding="utf-8")


def cleanup_probe_outputs() -> None:
    for role in ROLES:
        for name in ("SIBLING_OUTPUT_CANARY.txt", "A04_BOUNDARY_WRITE_PROBE.txt"):
            path = RUNTIME / "role_outputs" / role / name
            if path.exists():
                path.unlink()


def run_role_probes(mode: str, register: list[dict[str, object]]) -> list[dict[str, object]]:
    prepare_probe_canaries()
    payloads: list[dict[str, object]] = []
    env = {
        "CODEX_HOME": str(ISOLATED_HOME),
        "PATH": "/Users/rianray/.npm-global/bin:/usr/local/bin:/usr/bin:/bin",
        "TMPDIR": str(TOOLING / "tmp"),
    }
    (TOOLING / "tmp").mkdir(exist_ok=True)
    try:
        for role in ROLES:
            record = run_command(f"A04-{mode.upper()}-{role}", role_probe_argv(role), env=env, cwd=RUNTIME / "role_inputs" / role, sample=True)
            register.append(record)
            payloads.append(validate_probe(record, role))
    finally:
        cleanup_probe_outputs()
    return payloads


def verify_checksum_ledger(root: Path, ledger: Path) -> int:
    count = 0
    for raw in ledger.read_text(encoding="utf-8").splitlines():
        if not raw:
            continue
        expected, rel = raw.split("  ", 1)
        path = root / rel
        require(path.is_file(), f"missing checksum path: {path}")
        require(sha256(path) == expected, f"checksum mismatch: {path}")
        count += 1
    return count


def git_command(command_id: str, args: list[str], register: list[dict[str, object]]) -> str:
    argv = ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", "-c", "credential.helper=", "-c", "protocol.allow=never", "-C", str(REPO), *args]
    env = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"}
    record = run_command(command_id, argv, env=env, cwd=REPO, sample=True)
    register.append(record)
    require(record["exit"] == 0, f"Git command failed: {command_id}")
    return str(record["output"]).strip()


def local_formal_checks(register: list[dict[str, object]]) -> dict[str, object]:
    require((RUNTIME / "evidence/PACKET_FREEZE_RECEIPT.json").is_file(), "packet freeze receipt missing")
    require(git_command("A04-FORMAL-GIT-HEAD", ["rev-parse", "HEAD"], register) == START, "starting commit drift")
    require(git_command("A04-FORMAL-GIT-BRANCH", ["branch", "--show-current"], register) == BRANCH, "branch drift")
    require(git_command("A04-FORMAL-GIT-REMOTE", ["remote", "get-url", "origin"], register) == REMOTE, "remote drift")
    require(git_command("A04-FORMAL-ATTEMPT03-DIFF", ["diff", "--exit-code", START, "--", str(ATTEMPT03.relative_to(REPO))], register) == "", "Attempt 03 changed")
    status = git_command("A04-FORMAL-GIT-STATUS", ["status", "--porcelain=v1", "--untracked-files=all"], register)
    status_lines = [line for line in status.splitlines() if line]
    allowed_prefix = "?? governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-04/"
    require(status_lines and all(line.startswith(allowed_prefix) for line in status_lines), "working tree contains change outside additive Attempt 04 scope")
    checksum_entries = verify_checksum_ledger(ATTEMPT03, ATTEMPT03 / "MODE_B_CHECKSUMS.sha256")
    require(checksum_entries == 40, "Attempt 03 checksum denominator changed")

    verifier = ATTEMPT_ROOT / "scripts/verify_attempt04_packets.py"
    env = {"PATH": "/usr/bin:/bin", "A04_PACKET_STATE": "FROZEN", "PYTHONPYCACHEPREFIX": str(TOOLING / "pycache_formal")}
    record = run_command("A04-FORMAL-PACKET-VERIFY", [str(PYTHON), str(verifier)], env=env, cwd=REPO, sample=True)
    register.append(record)
    require(record["exit"] == 0 and '"result": "PASS"' in str(record["output"]), "frozen packet verification failed")

    proof = (TOOLING / "OFFLINE_DIAGNOSTIC_PROOF_04.log").read_text(encoding="utf-8")
    require("PROBE_ID|A04-OFFLINE-DIAGNOSTIC-PROOF-04" in proof, "offline proof identity missing")
    require("NETWORK_POLICY|DENY_ALL" in proof and "codex-cli 0.144.6" in proof, "offline diagnostic proof incomplete")
    require("codex doctor" not in proof.lower(), "prohibited doctor command found in offline diagnostic proof")

    isolated_files = [path.relative_to(ISOLATED_HOME).as_posix() for path in ISOLATED_HOME.rglob("*") if path.is_file()]
    require(not any(path.endswith("auth.json") for path in isolated_files), "credential file present in isolated home")
    require(not any("plugin" in path.lower() or "mcp" in path.lower() or "connector" in path.lower() for path in isolated_files), "plugin/MCP/connector file present in isolated home")

    executable_sources = [PROBE, Path(__file__), ATTEMPT_ROOT / "scripts/prepare_attempt04_packets.py", verifier, ATTEMPT_ROOT / "scripts/freeze_attempt04_packets.py"]
    prohibited_tokens = ("curl ", "wget ", "socket.", "urllib.", "requests.", "codex doctor", "gh ", "git fetch", "git pull", "git push")
    source_hits: list[str] = []
    for path in executable_sources:
        text = path.read_text(encoding="utf-8").lower()
        for token in prohibited_tokens:
            if token in text and path != Path(__file__):
                source_hits.append(f"{path.name}:{token}")
    require(source_hits == [], f"network/provider-capable token in preflight executable: {source_hits}")

    return {
        "starting_commit": START,
        "branch": BRANCH,
        "remote": REMOTE,
        "attempt03_checksum_entries_verified": checksum_entries,
        "additive_attempt04_status_lines": len(status_lines),
        "isolated_home_files": isolated_files,
        "installed_plugins": 0,
        "configured_mcp_servers": 0,
        "configured_connectors": 0,
        "offline_diagnostic_proof": "A04-OFFLINE-DIAGNOSTIC-PROOF-04",
        "codex_doctor_invocations": 0,
    }


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"smoke", "formal"}:
        raise SystemExit("usage: attempt04_preflight_runner.py smoke|formal")
    mode = sys.argv[1]
    register: list[dict[str, object]] = []
    root_record = {
        "mode": mode,
        "runner_argv": sys.argv,
        "runner_pid": os.getpid(),
        "runner_ppid": os.getppid(),
        "runner_executable": sys.executable,
        "started_at": utc_now(),
        "network_library_imports": [],
        "provider_operations_defined": [],
        "actual_credential_paths_defined": [],
    }
    output_root = TOOLING if mode == "smoke" else RUNTIME / "evidence"
    output_root.mkdir(parents=True, exist_ok=True)
    try:
        local = {} if mode == "smoke" else local_formal_checks(register)
        payloads = run_role_probes(mode, register)
        result = {
            "schema_version": "1.0.0",
            "attempt_id": "ES-PH1-PILOT-A-MODE-B-ATTEMPT-04",
            "mode": mode,
            "runner": root_record,
            "local_checks": local,
            "role_boundary_probes": payloads,
            "commands_and_processes": register,
            "pre_execution_counts": {
                "provider_requests": 0,
                "network_connections": 0,
                "successful_network_resolutions": 0,
                "actual_credential_accesses": 0,
                "model_requests": 0,
                "model_responses": 0,
                "canonical_role_invocations": 0,
            },
            "network_evidence_basis": "All executed diagnostic payloads were static/local; each role probe used network.enabled=false; no network operation was requested; no network denial marker was present.",
            "actual_credential_evidence_basis": "No actual credential path was named or accessed; only a harmless synthetic non-secret credential canary was used for boundary testing.",
            "result": "PASS",
            "completed_at": utc_now(),
        }
        name = "PREFREEZE_HARNESS_SMOKE.json" if mode == "smoke" else "FORMAL_NO_PROVIDER_PREFLIGHT.json"
        target = output_root / name
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        if mode == "formal":
            boundary = {
                "schema_version": "1.0.0",
                "attempt_id": "ES-PH1-PILOT-A-MODE-B-ATTEMPT-04",
                "event": "AUTHORIZED_EXECUTION_BOUNDARY_OPENED",
                "timestamp_utc": utc_now(),
                "preflight_sha256": sha256(target),
                "provider_requests_before_boundary": 0,
                "network_connections_before_boundary": 0,
                "successful_network_resolutions_before_boundary": 0,
                "actual_credential_accesses_before_boundary": 0,
                "model_responses_before_boundary": 0,
                "canonical_role_invocations_before_boundary": 0,
                "codex_doctor_invocations": 0,
                "phase_2": "NOT_AUTHORIZED",
                "result": "PASS",
            }
            (output_root / "AUTHORIZED_EXECUTION_BOUNDARY_RECEIPT.json").write_text(json.dumps(boundary, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"result": "PASS", "mode": mode, "evidence": str(target), "commands": len(register), "roles": len(payloads)}, indent=2))
    except Exception as exc:
        failure = {
            "schema_version": "1.0.0",
            "attempt_id": "ES-PH1-PILOT-A-MODE-B-ATTEMPT-04",
            "mode": mode,
            "runner": root_record,
            "commands_and_processes": register,
            "result": "FAIL_CLOSED",
            "error": f"{type(exc).__name__}: {exc}",
            "completed_at": utc_now(),
        }
        (output_root / f"{mode.upper()}_FAILURE.json").write_text(json.dumps(failure, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(failure, indent=2), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
