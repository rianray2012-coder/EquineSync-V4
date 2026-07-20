#!/usr/bin/env python3
"""Fail-closed start/status/stop orchestration for the Stage 2A sandbox."""
from __future__ import annotations

import argparse
import ctypes
import datetime as dt
import hashlib
import json
import os
import signal
import shlex
import shutil
import socket
import subprocess
import sys
import time
import struct
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from lib.control import REPO, RUNTIME, ROOT, load_env, validate_env

MONGO_PID = RUNTIME / "mongod.pid"
API_PID = RUNTIME / "api.pid"
API_PROFILE = RUNTIME / "api.profile"
MONGO_PORT = 27029
API_PORT = 8019
CONTROLLED_PORTS = {"mongo": MONGO_PORT, "api": API_PORT}


class ProcessIdentityError(RuntimeError):
    pass


def _identity_timestamp_valid(value: object, now: dt.datetime | None = None) -> bool:
    try:
        parsed = dt.datetime.fromisoformat(str(value))
    except ValueError:
        return False
    current = now or dt.datetime.now(dt.timezone.utc)
    return (
        parsed.tzinfo is not None
        and parsed.utcoffset() == dt.timedelta(0)
        and parsed <= current + dt.timedelta(seconds=5)
    )


def _read_record(pid_file: Path, expected_kind: str | None = None, expected_port: int | None = None) -> dict[str, object] | None:
    if not pid_file.exists():
        return None
    try:
        value = json.loads(pid_file.read_text(encoding="utf-8"))
        if (
            value.get("owner") != "ES-PKG-2026-004-V003"
            or not isinstance(value.get("pid"), int)
            or not isinstance(value.get("process_group_id"), int)
            or not isinstance(value.get("command_line_sha256"), str)
            or not isinstance(value.get("parent_pid"), int)
            or not isinstance(value.get("executable_path"), str)
            or not isinstance(value.get("working_directory"), str)
            or not isinstance(value.get("controlled_port"), int)
            or not isinstance(value.get("observed_command_line"), str)
            or not isinstance(value.get("launch_nonce_sha256"), str)
            or not isinstance(value.get("identity_recorded_utc"), str)
            or value.get("parent_pid_policy") != "CREATION_PARENT_OR_INIT_REPARENT_ONLY"
            or not _identity_timestamp_valid(value.get("identity_recorded_utc"))
            or (expected_kind is not None and value.get("kind") != expected_kind)
            or (expected_port is not None and value.get("controlled_port") != expected_port)
        ):
            raise ProcessIdentityError(f"malformed or conflicting process identity record: {pid_file.name}")
        return value
    except (ValueError, json.JSONDecodeError) as exc:
        raise ProcessIdentityError(f"unparseable process identity record: {pid_file.name}") from exc


def _ps_identity(pid: int) -> dict[str, object] | None:
    """Measure PPID/PGID with lsof and full argv with macOS KERN_PROCARGS2.

    The controlled sandbox does not permit ``ps`` process inspection. Both
    interfaces used here are available inside the same sandbox profile and
    fail closed when either half of the identity cannot be measured.
    """
    try:
        result = subprocess.run(
            ["lsof", "-a", "-p", str(pid), "-FpgR"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return None
    fields = {line[0]: line[1:] for line in result.stdout.splitlines() if line and line[0] in {"p", "g", "R"}}
    if result.returncode != 0 or fields.get("p") != str(pid) or not fields.get("g") or not fields.get("R"):
        return None
    libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib", use_errno=True)
    mib = (ctypes.c_int * 3)(1, 49, pid)  # CTL_KERN, KERN_PROCARGS2, pid
    size = ctypes.c_size_t()
    if libc.sysctl(mib, 3, None, ctypes.byref(size), None, 0) != 0 or size.value < 8:
        return None
    buffer = ctypes.create_string_buffer(size.value)
    if libc.sysctl(mib, 3, buffer, ctypes.byref(size), None, 0) != 0:
        return None
    raw = buffer.raw[:size.value]
    argc = struct.unpack_from("i", raw)[0]
    if argc < 1:
        return None
    cursor = 4
    executable_end = raw.find(b"\0", cursor)
    if executable_end < 0:
        return None
    observed_executable = raw[cursor:executable_end].decode(errors="surrogateescape")
    cursor = executable_end
    while cursor < len(raw) and raw[cursor] == 0:
        cursor += 1
    argv: list[str] = []
    for _ in range(argc):
        end = raw.find(b"\0", cursor)
        if end < 0:
            return None
        argv.append(raw[cursor:end].decode(errors="surrogateescape"))
        cursor = end + 1
    launch_nonce = None
    while cursor < len(raw):
        end = raw.find(b"\0", cursor)
        if end < 0:
            break
        item = raw[cursor:end].decode(errors="surrogateescape")
        if item.startswith("STAGE2A_LAUNCH_NONCE="):
            launch_nonce = item.split("=", 1)[1]
            break
        cursor = end + 1
    if not launch_nonce:
        return None
    return {
        "parent_pid": int(fields["R"]), "process_group_id": int(fields["g"]),
        "command_line": shlex.join(argv), "observed_executable": str(Path(observed_executable).resolve()),
        "launch_nonce_sha256": hashlib.sha256(launch_nonce.encode()).hexdigest(),
    }


def _executable_path(command: list[str]) -> str:
    candidate = Path(command[0]) if "/" in command[0] else Path(shutil.which(command[0]) or command[0])
    return str(candidate.resolve())


def _write_record(pid_file: Path, pid: int, kind: str, command: list[str], cwd: Path, port: int, launch_nonce: str) -> None:
    if CONTROLLED_PORTS.get(kind) != port:
        raise ProcessIdentityError(f"{kind} controlled-port identity mismatch at creation")
    process_group_id = os.getpgid(pid)
    if process_group_id != pid:
        raise RuntimeError(f"{kind} did not start as its own process group")
    identity = _ps_identity(pid)
    if not identity or identity["parent_pid"] != os.getpid() or identity["process_group_id"] != process_group_id:
        raise RuntimeError(f"{kind} process identity unavailable or conflicting at creation")
    if identity["observed_executable"] != _executable_path(command):
        raise RuntimeError(f"{kind} executable identity unavailable or conflicting at creation")
    files = _process_files(pid)
    if (
        not files
        or files.get("cwd") != str(cwd.resolve())
        or identity["observed_executable"] not in files.get("txt_paths", set())
    ):
        raise RuntimeError(f"{kind} exact executable or working-directory identity unavailable at creation")
    launch_nonce_sha256 = hashlib.sha256(launch_nonce.encode()).hexdigest()
    if identity["launch_nonce_sha256"] != launch_nonce_sha256:
        raise RuntimeError(f"{kind} launch-nonce identity unavailable or conflicting at creation")
    command_line_sha256 = hashlib.sha256(str(identity["command_line"]).encode()).hexdigest()
    pid_file.write_text(json.dumps({
        "owner": "ES-PKG-2026-004-V003",
        "pid": pid,
        "kind": kind,
        "process_group_id": process_group_id,
        "parent_pid": identity["parent_pid"],
        "parent_pid_policy": "CREATION_PARENT_OR_INIT_REPARENT_ONLY",
        "executable_path": _executable_path(command),
        "working_directory": str(cwd.resolve()),
        "controlled_port": port,
        "launch_nonce_sha256": launch_nonce_sha256,
        "identity_recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "command_line_sha256": command_line_sha256,
        "observed_command_line": identity["command_line"],
        "command_display": shlex.join(command),
        "runtime": str(RUNTIME),
    }, sort_keys=True) + "\n", encoding="utf-8")


def _contain_unrecorded_spawn(process: subprocess.Popen[bytes], kind: str) -> dict[str, object]:
    """Contain only the exact child just spawned by this orchestrator.

    This path is used solely when identity capture fails before a PID record can
    be committed. It never adopts a listener or signals a PID discovered by
    scanning the host.
    """
    pid = process.pid
    identity = _ps_identity(pid)
    if (
        process.poll() is None
        and identity
        and identity["parent_pid"] == os.getpid()
        and identity["process_group_id"] == pid
    ):
        os.killpg(pid, signal.SIGTERM)
        try:
            process.wait(timeout=10)
            forced = False
        except subprocess.TimeoutExpired:
            os.killpg(pid, signal.SIGKILL)
            process.wait(timeout=5)
            forced = True
        return {
            "kind": kind,
            "pid": pid,
            "process_group_id": pid,
            "status": "CONTAINED_AFTER_IDENTITY_CAPTURE_FAILURE",
            "forced": forced,
            "scope": "EXACT_NEWLY_SPAWNED_CHILD_PROCESS_GROUP_ONLY",
        }
    if process.poll() is not None:
        return {
            "kind": kind,
            "pid": pid,
            "status": "ALREADY_EXITED_DURING_IDENTITY_CAPTURE",
            "scope": "NO_SIGNAL_SENT",
        }
    raise RuntimeError(
        f"{kind} identity capture failed and exact child identity is conflicting; "
        "refusing to signal an unverified process"
    )


def _process_files(pid: int) -> dict[str, object] | None:
    try:
        result = subprocess.run(
            ["lsof", "-a", "-nP", "-p", str(pid), "-d", "txt,cwd", "-Fftn"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return None
    if result.returncode != 0:
        return None
    descriptor: str | None = None
    cwd_values: set[str] = set()
    txt_paths: set[str] = set()
    for line in result.stdout.splitlines():
        if line.startswith("f"):
            descriptor = line[1:]
        elif line.startswith("n") and descriptor in {"cwd", "txt"}:
            resolved = str(Path(line[1:]).resolve())
            if descriptor == "cwd":
                cwd_values.add(resolved)
            else:
                txt_paths.add(resolved)
    if len(cwd_values) != 1 or not txt_paths:
        return None
    return {"cwd": next(iter(cwd_values)), "txt_paths": txt_paths}


def _expected(record: dict[str, object] | None, kind: str, expected_port: int | None = None) -> bool:
    controlled_port = CONTROLLED_PORTS.get(kind) if expected_port is None else expected_port
    if not record or record.get("kind") != kind or controlled_port != CONTROLLED_PORTS.get(kind):
        return False
    if record.get("controlled_port") != controlled_port or not _identity_timestamp_valid(record.get("identity_recorded_utc")):
        return False
    pid = int(record["pid"])
    process_group_id = int(record["process_group_id"])
    files = _process_files(pid)
    if not files:
        return False
    identity = _ps_identity(pid)
    if not identity:
        return False
    recorded_parent = int(record["parent_pid"])
    observed_parent = int(identity["parent_pid"])
    parent_valid = observed_parent == recorded_parent or (
        observed_parent == 1 and recorded_parent > 1 and not _process_exists(recorded_parent)
    )
    if (
        process_group_id != pid
        or identity["process_group_id"] != process_group_id
        or not parent_valid
        or hashlib.sha256(str(identity["command_line"]).encode()).hexdigest() != record.get("command_line_sha256")
        or identity["observed_executable"] != record.get("executable_path")
        or identity["launch_nonce_sha256"] != record.get("launch_nonce_sha256")
        or str(record.get("executable_path")) not in files.get("txt_paths", set())
        or str(record.get("working_directory")) != files.get("cwd")
    ):
        return False
    return True


def _alive(record: dict[str, object] | None, kind: str, expected_port: int | None = None) -> bool:
    if not _expected(record, kind, expected_port):
        return False
    pid = int(record["pid"])
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def _listener_pid(port: int, expected_pid: int | None = None) -> int | None:
    if not _port_open("127.0.0.1", port):
        return None
    command = ["lsof", "-nP", "-t"]
    if expected_pid is not None:
        command.extend(["-a", "-p", str(expected_pid)])
    command.extend([f"-iTCP:{port}", "-sTCP:LISTEN"])
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"listener identity probe timed out for controlled port {port}") from exc
    pids = sorted({int(x) for x in result.stdout.split() if x.isdigit()})
    if len(pids) > 1:
        raise RuntimeError(f"multiple listeners on controlled port {port}: {pids}")
    return pids[0] if pids else None


def _port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.2):
            return True
    except OSError:
        return False


def _process_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def _wait_port(host: str, port: int, timeout: float) -> None:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if _port_open(host, port):
            return
        time.sleep(0.1)
    raise TimeoutError(f"port {host}:{port} not ready within {timeout}s")


def _wait_health(url: str, timeout: float) -> dict[str, object]:
    end = time.monotonic() + timeout
    last = "not attempted"
    while time.monotonic() < end:
        try:
            with urlopen(url, timeout=2) as response:
                value = json.loads(response.read())
                if response.status == 200:
                    return value
        except (OSError, HTTPError, URLError, json.JSONDecodeError) as exc:
            last = type(exc).__name__
        time.sleep(0.2)
    raise TimeoutError(f"health endpoint not ready within {timeout}s: {last}")


def _wait_exit(record: dict[str, object], kind: str, timeout: float, expected_port: int | None = None) -> bool:
    pid = int(record["pid"])
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            waited, _ = os.waitpid(pid, os.WNOHANG)
            if waited == pid:
                return True
        except ChildProcessError:
            pass
        if not _alive(record, kind, expected_port):
            return True
        time.sleep(0.1)
    return not _alive(record, kind, expected_port)


def _terminate(kind: str, pid_file: Path, port: int) -> dict[str, object]:
    record = _read_record(pid_file, kind, port)
    saved_pid = int(record["pid"]) if record else None
    listener = _listener_pid(port, saved_pid)
    if saved_pid is None and listener is not None:
        raise RuntimeError(f"refusing to adopt unverified foreign-path listener PID {listener} on controlled port {port}")
    pid = saved_pid
    saved_pgid = int(record["process_group_id"]) if record else None
    if record and record.get("controlled_port") != port:
        raise RuntimeError(f"{kind} controlled-port identity mismatch")
    if saved_pid and listener and saved_pid != listener:
        raise RuntimeError(f"{kind} PID/listener mismatch: pid_file={saved_pid} listener={listener}")
    if pid is None:
        pid_file.unlink(missing_ok=True)
        return {"kind": kind, "pid": None, "status": "ALREADY_STOPPED", "port_closed": not _port_open("127.0.0.1", port)}
    if listener is None and not _process_exists(pid):
        pid_file.unlink(missing_ok=True)
        return {
            "kind": kind, "pid": pid, "process_group_id": saved_pgid,
            "status": "ALREADY_EXITED_NO_SIGNAL_SENT", "port_closed": True,
            "command_identity_verified": False,
        }
    if not _expected(record, kind, port):
        raise RuntimeError(f"refusing to signal unverified {kind} PID {pid}")
    if listener != pid:
        raise RuntimeError(f"refusing to signal {kind} PID {pid}: controlled port {port} is not attributed to that PID")
    if saved_pgid != pid:
        raise RuntimeError(f"refusing to signal {kind}: PID/PGID identity mismatch")
    os.killpg(saved_pgid, signal.SIGTERM)
    forced = False
    if not _wait_exit(record, kind, 10, port):
        os.killpg(saved_pgid, signal.SIGKILL)
        forced = True
        if not _wait_exit(record, kind, 5, port):
            raise RuntimeError(f"{kind} PID {pid} survived SIGTERM and SIGKILL")
    if _port_open("127.0.0.1", port) or _listener_pid(port) is not None:
        raise RuntimeError(f"{kind} port {port} remains open after process exit")
    pid_file.unlink(missing_ok=True)
    return {
        "kind": kind, "pid": pid, "process_group_id": saved_pgid,
        "command_identity_verified": True, "status": "STOPPED",
        "forced": forced, "port_closed": True,
    }


def start(profile: str = "full", failpoint: str | None = None) -> dict[str, object]:
    if profile not in {"full", "foundation"}:
        raise ValueError("profile must be full or foundation")
    env = load_env()
    validate_env(env)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    (RUNTIME / ".owner.json").write_text(
        json.dumps({"owner": "ES-PKG-2026-004-V003", "disposable": True}, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (RUNTIME / "mongo").mkdir(parents=True, exist_ok=True)
    (RUNTIME / "logs").mkdir(parents=True, exist_ok=True)
    if _read_record(MONGO_PID, "mongo", MONGO_PORT) or _read_record(API_PID, "api", API_PORT) or _listener_pid(MONGO_PORT) or _listener_pid(API_PORT):
        raise RuntimeError("Stage 2A runtime or controlled port is already active")

    mongo_log = (RUNTIME / "logs/mongod.log").open("ab")
    mongo_command = ["mongod", "--dbpath", str(RUNTIME / "mongo"), "--port", str(MONGO_PORT), "--bind_ip", "127.0.0.1", "--nounixsocket", "--quiet"]
    mongo_nonce = uuid.uuid4().hex
    mongo_env = env | {"STAGE2A_LAUNCH_NONCE": mongo_nonce}
    mongo = subprocess.Popen(
        mongo_command,
        stdout=mongo_log,
        stderr=subprocess.STDOUT,
        env=mongo_env,
        start_new_session=True,
    )
    try:
        _write_record(MONGO_PID, mongo.pid, "mongo", mongo_command, ROOT, MONGO_PORT, mongo_nonce)
    except Exception:
        _contain_unrecorded_spawn(mongo, "mongo")
        MONGO_PID.unlink(missing_ok=True)
        raise
    try:
        _wait_port("127.0.0.1", MONGO_PORT, 15)
        if failpoint == "after_datastore_ready":
            raise RuntimeError("intentional Stage 2A interrupted-start failpoint")
        # No API process exists at this point. Remove only the completed prior
        # guard-session file so the next API can create a new session with
        # exclusive-create semantics; the guard itself never overwrites one.
        (RUNTIME / "network-guard.json").unlink(missing_ok=True)
        api_log = (RUNTIME / "logs/api.log").open("ab")
        if profile == "full":
            command = [
                sys.executable, "-m", "uvicorn", "full_application_profile:app", "--app-dir", str(ROOT),
                "--host", "127.0.0.1", "--port", str(API_PORT), "--log-level", "warning", "--no-access-log",
            ]
            cwd = ROOT
            ready_url = "http://127.0.0.1:8019/api/health/ready"
        else:
            command = [sys.executable, str(ROOT / "foundation_api.py")]
            cwd = ROOT
            ready_url = "http://127.0.0.1:8019/health/ready"
        api_nonce = uuid.uuid4().hex
        api_env = env | {"STAGE2A_LAUNCH_NONCE": api_nonce}
        api = subprocess.Popen(command, stdout=api_log, stderr=subprocess.STDOUT, env=api_env, cwd=cwd, start_new_session=True)
        try:
            _write_record(API_PID, api.pid, "api", command, cwd, API_PORT, api_nonce)
        except Exception:
            _contain_unrecorded_spawn(api, "api")
            API_PID.unlink(missing_ok=True)
            raise
        API_PROFILE.write_text(profile, encoding="utf-8")
        _wait_port("127.0.0.1", API_PORT, 120)
        health = _wait_health(ready_url, 60)
        if not _alive(_read_record(MONGO_PID, "mongo", MONGO_PORT), "mongo", MONGO_PORT) or not _alive(_read_record(API_PID, "api", API_PORT), "api", API_PORT):
            raise RuntimeError("process identity lost after readiness")
        return {
            "status": "STARTED",
            "profile": profile,
            "mongo_pid": mongo.pid,
            "api_pid": api.pid,
            "health": health,
            "health_url": ready_url.replace("http://127.0.0.1:8019", "LOOPBACK_API"),
            "logs": [".runtime/logs/mongod.log", ".runtime/logs/api.log"],
        }
    except Exception:
        stop()
        raise


def stop() -> dict[str, object]:
    api = _terminate("api", API_PID, API_PORT)
    mongo = _terminate("mongo", MONGO_PID, MONGO_PORT)
    API_PROFILE.unlink(missing_ok=True)
    result = {
        "status": "STOPPED",
        "processes": [api, mongo],
        "api_alive": _listener_pid(API_PORT) is not None,
        "mongo_alive": _listener_pid(MONGO_PORT) is not None,
        "ports_closed": not _port_open("127.0.0.1", API_PORT) and not _port_open("127.0.0.1", MONGO_PORT),
        "pid_files_absent": not API_PID.exists() and not MONGO_PID.exists(),
    }
    if result["api_alive"] or result["mongo_alive"] or not result["ports_closed"] or not result["pid_files_absent"]:
        raise RuntimeError(f"controlled shutdown invariant failed: {result}")
    return result


def status() -> dict[str, object]:
    mongo_record = _read_record(MONGO_PID, "mongo", MONGO_PORT)
    api_record = _read_record(API_PID, "api", API_PORT)
    mongo_port_open = _port_open("127.0.0.1", MONGO_PORT)
    api_port_open = _port_open("127.0.0.1", API_PORT)
    mongo_listener = _listener_pid(MONGO_PORT, int(mongo_record["pid"])) if mongo_record else _listener_pid(MONGO_PORT)
    api_listener = _listener_pid(API_PORT, int(api_record["pid"])) if api_record else _listener_pid(API_PORT)
    mongo_expected = _alive(mongo_record, "mongo", MONGO_PORT)
    api_expected = _alive(api_record, "api", API_PORT)
    mongo_listener_bound = bool(mongo_record and mongo_listener == mongo_record.get("pid") and mongo_expected)
    api_listener_bound = bool(api_record and api_listener == api_record.get("pid") and api_expected)
    return {
        "mongo_pid": mongo_record.get("pid") if mongo_record else None,
        "mongo_alive": mongo_listener_bound,
        "mongo_port_open": mongo_port_open,
        "mongo_listener_identity_verified": mongo_listener_bound,
        "mongo_foreign_listener_pid": mongo_listener if mongo_listener and not mongo_listener_bound else None,
        "mongo_listener_attribution_conflict": mongo_port_open and not mongo_listener_bound,
        "mongo_identity": mongo_record,
        "api_pid": api_record.get("pid") if api_record else None,
        "api_alive": api_listener_bound,
        "api_port_open": api_port_open,
        "api_listener_identity_verified": api_listener_bound,
        "api_foreign_listener_pid": api_listener if api_listener and not api_listener_bound else None,
        "api_listener_attribution_conflict": api_port_open and not api_listener_bound,
        "api_identity": api_record,
        "profile": API_PROFILE.read_text(encoding="utf-8").strip() if API_PROFILE.exists() else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop", "status"])
    parser.add_argument("--profile", choices=["full", "foundation"], default="full")
    parser.add_argument("--failpoint", choices=["after_datastore_ready"])
    args = parser.parse_args()
    operation = start(args.profile, args.failpoint) if args.action == "start" else stop() if args.action == "stop" else status()
    print(json.dumps(operation, indent=2, sort_keys=True))
