#!/usr/bin/env python3
"""Fail-closed start/status/stop orchestration for the Stage 2A sandbox."""
from __future__ import annotations

import argparse
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
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from lib.control import REPO, RUNTIME, ROOT, load_env, validate_env

MONGO_PID = RUNTIME / "mongod.pid"
API_PID = RUNTIME / "api.pid"
API_PROFILE = RUNTIME / "api.profile"
MONGO_PORT = 27029
API_PORT = 8019


def _read_record(pid_file: Path) -> dict[str, object] | None:
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
            or value.get("parent_pid_policy") != "CREATION_PARENT_OR_INIT_REPARENT_ONLY"
        ):
            return None
        return value
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        return None


def _ps_identity(pid: int) -> dict[str, object] | None:
    result = subprocess.run(
        ["ps", "-o", "ppid=,pgid=,command=", "-p", str(pid)],
        text=True,
        capture_output=True,
        check=False,
    )
    fields = result.stdout.strip().split(None, 2)
    if result.returncode != 0 or len(fields) != 3:
        return None
    return {"parent_pid": int(fields[0]), "process_group_id": int(fields[1]), "command_line": fields[2]}


def _executable_path(command: list[str]) -> str:
    candidate = Path(command[0]) if "/" in command[0] else Path(shutil.which(command[0]) or command[0])
    return str(candidate.resolve())


def _write_record(pid_file: Path, pid: int, kind: str, command: list[str], cwd: Path, port: int) -> None:
    process_group_id = os.getpgid(pid)
    if process_group_id != pid:
        raise RuntimeError(f"{kind} did not start as its own process group")
    identity = _ps_identity(pid)
    if not identity or identity["parent_pid"] != os.getpid() or identity["process_group_id"] != process_group_id:
        raise RuntimeError(f"{kind} process identity unavailable or conflicting at creation")
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


def _process_files(pid: int) -> str:
    result = subprocess.run(
        ["lsof", "-a", "-nP", "-p", str(pid), "-d", "txt,cwd"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _expected(record: dict[str, object] | None, kind: str) -> bool:
    if not record or record.get("kind") != kind:
        return False
    pid = int(record["pid"])
    process_group_id = int(record["process_group_id"])
    files = _process_files(pid)
    if not files:
        return False
    identity = _ps_identity(pid)
    if not identity:
        return False
    if (
        process_group_id != pid
        or identity["process_group_id"] != process_group_id
        or identity["parent_pid"] not in {record.get("parent_pid"), 1}
        or hashlib.sha256(str(identity["command_line"]).encode()).hexdigest() != record.get("command_line_sha256")
        or str(record.get("executable_path")) not in files
        or str(record.get("working_directory")) not in files
    ):
        return False
    return True


def _alive(record: dict[str, object] | None, kind: str) -> bool:
    if not _expected(record, kind):
        return False
    pid = int(record["pid"])
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False


def _listener_pid(port: int) -> int | None:
    result = subprocess.run(
        ["lsof", "-nP", "-t", f"-iTCP:{port}", "-sTCP:LISTEN"],
        text=True,
        capture_output=True,
        check=False,
    )
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


def _wait_exit(record: dict[str, object], kind: str, timeout: float) -> bool:
    pid = int(record["pid"])
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        try:
            waited, _ = os.waitpid(pid, os.WNOHANG)
            if waited == pid:
                return True
        except ChildProcessError:
            pass
        if not _alive(record, kind):
            return True
        time.sleep(0.1)
    return not _alive(record, kind)


def _terminate(kind: str, pid_file: Path, port: int) -> dict[str, object]:
    record = _read_record(pid_file)
    saved_pid = int(record["pid"]) if record else None
    listener = _listener_pid(port)
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
    if not _expected(record, kind):
        raise RuntimeError(f"refusing to signal unverified {kind} PID {pid}")
    if listener != pid:
        raise RuntimeError(f"refusing to signal {kind} PID {pid}: controlled port {port} is not attributed to that PID")
    if saved_pgid != pid:
        raise RuntimeError(f"refusing to signal {kind}: PID/PGID identity mismatch")
    os.killpg(saved_pgid, signal.SIGTERM)
    forced = False
    if not _wait_exit(record, kind, 10):
        os.killpg(saved_pgid, signal.SIGKILL)
        forced = True
        if not _wait_exit(record, kind, 5):
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
    if _read_record(MONGO_PID) or _read_record(API_PID) or _listener_pid(MONGO_PORT) or _listener_pid(API_PORT):
        raise RuntimeError("Stage 2A runtime or controlled port is already active")

    mongo_log = (RUNTIME / "logs/mongod.log").open("ab")
    mongo_command = ["mongod", "--dbpath", str(RUNTIME / "mongo"), "--port", str(MONGO_PORT), "--bind_ip", "127.0.0.1", "--nounixsocket", "--quiet"]
    mongo = subprocess.Popen(
        mongo_command,
        stdout=mongo_log,
        stderr=subprocess.STDOUT,
        env=env,
        start_new_session=True,
    )
    try:
        _write_record(MONGO_PID, mongo.pid, "mongo", mongo_command, ROOT, MONGO_PORT)
    except Exception:
        _contain_unrecorded_spawn(mongo, "mongo")
        MONGO_PID.unlink(missing_ok=True)
        raise
    try:
        _wait_port("127.0.0.1", MONGO_PORT, 15)
        if failpoint == "after_datastore_ready":
            raise RuntimeError("intentional Stage 2A interrupted-start failpoint")
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
        api = subprocess.Popen(command, stdout=api_log, stderr=subprocess.STDOUT, env=env, cwd=cwd, start_new_session=True)
        try:
            _write_record(API_PID, api.pid, "api", command, cwd, API_PORT)
        except Exception:
            _contain_unrecorded_spawn(api, "api")
            API_PID.unlink(missing_ok=True)
            raise
        API_PROFILE.write_text(profile, encoding="utf-8")
        _wait_port("127.0.0.1", API_PORT, 120)
        health = _wait_health(ready_url, 60)
        if not _alive(_read_record(MONGO_PID), "mongo") or not _alive(_read_record(API_PID), "api"):
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
    mongo_record = _read_record(MONGO_PID)
    api_record = _read_record(API_PID)
    mongo_listener = _listener_pid(MONGO_PORT)
    api_listener = _listener_pid(API_PORT)
    return {
        "mongo_pid": mongo_record.get("pid") if mongo_record else None,
        "mongo_alive": _alive(mongo_record, "mongo"),
        "mongo_port_open": _port_open("127.0.0.1", MONGO_PORT),
        "mongo_foreign_listener_pid": mongo_listener if mongo_record is None and mongo_listener else None,
        "mongo_identity": mongo_record,
        "api_pid": api_record.get("pid") if api_record else None,
        "api_alive": _alive(api_record, "api"),
        "api_port_open": _port_open("127.0.0.1", API_PORT),
        "api_foreign_listener_pid": api_listener if api_record is None and api_listener else None,
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
