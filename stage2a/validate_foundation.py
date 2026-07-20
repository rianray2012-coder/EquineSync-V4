#!/usr/bin/env python3
"""Validate Stage 2A gaps 003-009 without executing a business workflow."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

import cleanup as cleanup_cli
import orchestrate
from evidence_capture import capture
from lib.control import (
    COLLECTION,
    ENV_FILE,
    EVIDENCE,
    PROVIDER_NAMES,
    REPO,
    ROOT,
    RUNTIME,
    ambient_name_attestation,
    cleanup as row_cleanup,
    database_inventory,
    digest,
    drop_disposable_database,
    file_sha,
    fixture_data,
    load_env,
    load_fixture,
    mongo_client,
    provider_register,
    state_digest,
    validate_env,
)
from rollback_recovery import restore_snapshot, write_snapshot

START = "0be6172a28b75238c5facabf91d43ed09aaf0d54"
EMPTY_STATE_DIGEST = digest([])


def git(*args: str, cwd: Path = REPO) -> str:
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=True).stdout.strip()


def wait_for(path: Path, timeout: float) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if path.exists():
            return True
        time.sleep(0.1)
    return path.exists()


def source_recovery_rehearsal(implementation_commit: str) -> dict[str, object]:
    temp_root = Path(tempfile.mkdtemp(prefix="equinesync-stage2a-source-recovery-", dir="/private/tmp"))
    clone = temp_root / "repo"
    subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout", str(REPO), str(clone)], check=True, timeout=120)
    try:
        subprocess.run(["git", "sparse-checkout", "init", "--no-cone"], cwd=clone, check=True, timeout=30)
        subprocess.run(["git", "sparse-checkout", "set", "stage2a/fixtures/foundation-v1.json"], cwd=clone, check=True, timeout=30)
        subprocess.run(["git", "checkout", "--quiet", "--detach", implementation_commit], cwd=clone, check=True, timeout=120)
        fixture = clone / "stage2a/fixtures/foundation-v1.json"
        expected = file_sha(fixture)
        fixture.write_text("intentional Stage 2A source recovery mutation\n", encoding="utf-8")
        mutated = file_sha(fixture)
        subprocess.run(["git", "restore", f"--source={implementation_commit}", "--", "stage2a/fixtures/foundation-v1.json"], cwd=clone, check=True, timeout=120)
        restored = file_sha(fixture)
        subprocess.run(["git", "checkout", "--quiet", "--detach", START], cwd=clone, check=True, timeout=120)
        prechange_absent = not (clone / "stage2a").exists()
        return {
            "implementation_restore_command": "git restore --source=IMPLEMENTATION_COMMIT -- stage2a/fixtures/foundation-v1.json",
            "prechange_restore_command": "git checkout --detach STARTING_COMMIT",
            "expected_sha256": expected,
            "mutated_sha256": mutated,
            "restored_sha256": restored,
            "restored_matches": expected == restored and expected != mutated,
            "stage2a_absent_at_prechange_anchor": prechange_absent,
            "clone_mode": "DISPOSABLE_SHARED_OBJECTS_SPARSE_SINGLE_FILE",
            "fresh_clone_proof_role": "NOT_APPLICABLE_SEPARATE_POST_PUSH_CONTROL",
            "disposable_clone_removed": True,
        }
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for name in ("FOUNDATION_VALIDATION.json", "foundation-example-pass.json", "foundation-example-intentional-fail.json"):
        (EVIDENCE / name).unlink(missing_ok=True)
    started = dt.datetime.now(dt.timezone.utc)
    checks: list[dict[str, object]] = []
    artifacts: dict[str, object] = {}

    def ck(name: str, ok: bool, detail: object) -> None:
        checks.append({"check": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    env = load_env()
    posture = validate_env(env)
    attestation = ambient_name_attestation()
    implementation_commit = git("rev-parse", "HEAD")
    implementation_tree = git("rev-parse", "HEAD^{tree}")
    tracked_stage2a = git("ls-tree", "-r", "--name-only", implementation_commit, "--", "stage2a").splitlines()
    ck("implementation_commit_anchor", bool(tracked_stage2a) and implementation_commit != START, {
        "commit": implementation_commit,
        "tree": implementation_tree,
        "tracked_stage2a_paths": len(tracked_stage2a),
        "starting_commit": START,
    })
    ck("environment_contract", attestation["prohibited_name_count"] == 0, posture | {"ambient_attestation": attestation, "backend_dotenv_absent": not (REPO / "backend/.env").exists()})

    negative_results = []
    mutations = [
        {"MONGO_URL": "mongodb+srv://production.invalid/db"},
        {"DB_NAME": "equinesync_prod"},
        {"STAGE2A_DISPOSABLE": "0"},
        {"DISABLE_NOTIFICATIONS": "false"},
        *[{name: "REDACTED_PRESENT"} for name in sorted(PROVIDER_NAMES)],
    ]
    for mutation in mutations:
        bad = deepcopy(env)
        bad.update(mutation)
        try:
            validate_env(bad)
            denied = False
        except Exception:
            denied = True
        negative_results.append({"names": sorted(mutation), "denied": denied, "values_recorded": False})
    inherited = env | {"STRIPE_API_KEY": "REDACTED_PRESENT"}
    inherited_check = subprocess.run(
        [sys.executable, str(ROOT / "isolation_check.py")],
        cwd=ROOT,
        env=inherited,
        text=True,
        capture_output=True,
        timeout=10,
    )
    ck("isolation_negative_tests", all(x["denied"] for x in negative_results) and inherited_check.returncode != 0, {
        "configuration_denials": len(negative_results),
        "provider_names_tested": len(PROVIDER_NAMES),
        "inherited_provider_name_exit": inherited_check.returncode,
        "values_recorded": False,
    })

    denied_network = []
    for endpoint in [("127.0.0.1", 9), ("192.0.2.1", 443)]:
        try:
            with socket.create_connection(endpoint, timeout=1):
                denied = False
                error = "connection unexpectedly permitted"
        except OSError as exc:
            denied = isinstance(exc, PermissionError)
            error = f"{type(exc).__name__}:errno={getattr(exc, 'errno', None)}"
        denied_network.append({"endpoint_class": "UNAPPROVED_LOOPBACK" if endpoint[0].startswith("127.") else "DOCUMENTATION_EXTERNAL", "denied_by_sandbox": denied, "error": error})
    ck("exact_port_egress_denial", all(x["denied_by_sandbox"] for x in denied_network), denied_network)

    pre_stop = orchestrate.stop()
    try:
        orchestrate.start("full", "after_datastore_ready")
        interrupted_denied = False
        interrupted_error = "failpoint did not fire"
    except RuntimeError as exc:
        interrupted_denied = "intentional Stage 2A interrupted-start failpoint" in str(exc)
        interrupted_error = str(exc)
    interrupted_status = orchestrate.status()
    ck("interrupted_start_cleanup", interrupted_denied and not any(interrupted_status[k] for k in ("mongo_alive", "mongo_port_open", "api_alive", "api_port_open")), {
        "error": interrupted_error,
        "post_failure_status": interrupted_status,
        "precondition_stop": pre_stop,
    })

    start = orchestrate.start("full")
    ck("cold_start_full_application", start["profile"] == "full" and start["health"].get("status") == "ok", start)
    status = orchestrate.status()
    ck("process_identity", status["mongo_alive"] and status["api_alive"] and status["mongo_port_open"] and status["api_port_open"], status)

    client = mongo_client(env)
    db = client[env["DB_NAME"]]
    startup_inventory = database_inventory(db)
    startup_documents = sum(int(x["document_count"]) for x in startup_inventory["collections"])
    ck("startup_side_effect_inventory", startup_documents == 0 and len(startup_inventory["collections"]) > 0, {
        "profile": "full EquineSync application",
        "profile_control": env["STAGE2A_STARTUP_PROFILE"],
        "catalog_materialization": "DISABLED_BY_STAGE2A_WRAPPER",
        "collections_with_index_metadata": len(startup_inventory["collections"]),
        "startup_document_writes": startup_documents,
        "inventory_digest": startup_inventory["digest"],
        "background_flags": {name: env[name] for name in sorted(k for k in env if k.startswith("DISABLE_"))},
        "auto_seed": env["ALLOW_AUTO_SEED"],
        "seed_route": env["ALLOW_SEED_ROUTE"],
    })

    pids = [int(status["mongo_pid"]), int(status["api_pid"])]
    network_lines: list[str] = []
    for pid in pids:
        proc = subprocess.run(["lsof", "-Pan", "-p", str(pid), "-i"], text=True, capture_output=True, check=False)
        network_lines.extend(line for line in proc.stdout.splitlines()[1:] if line.strip())
    wildcard = [line for line in network_lines if "TCP *:" in line or "TCP [::]:" in line]
    non_loopback = [line for line in network_lines if "TCP " in line and "127.0.0.1" not in line]
    ck("network_boundary", not wildcard and not non_loopback and bool(network_lines), {
        "observed_lines": network_lines,
        "wildcard_listeners": wildcard,
        "non_loopback": non_loopback,
        "approved_ports": [27029, 8019],
        "sandbox_profile": "config/loopback-only.sb",
    })

    empty_start = state_digest(db)
    clean0 = row_cleanup(db)
    first = load_fixture(db)
    first_digest = first["state_digest"]
    clean1 = row_cleanup(db)
    second = load_fixture(db)
    second_digest = second["state_digest"]
    clean2 = row_cleanup(db)
    empty_end = state_digest(db)
    ck("fixture_reproducibility", empty_start == empty_end == EMPTY_STATE_DIGEST and first_digest == second_digest, {
        "starting_state_digest": empty_start,
        "first_loaded_state_digest": first_digest,
        "second_loaded_state_digest": second_digest,
        "ending_state_digest": empty_end,
        "fixture_sha256": first["fixture_sha256"],
        "cleanups": [clean0, clean1, clean2],
        "foundation_targets": ["loader", "evidence harness", "cleanup", "rollback"],
        "domain_fixture_scope": "PROHIBITED_NOT_IMPLEMENTED",
    })

    try:
        load_fixture(db, fail_after=1)
    except RuntimeError:
        pass
    partial = row_cleanup(db)
    repeated = row_cleanup(db)
    marker = RUNTIME / "fixture-interruption.marker"
    marker.unlink(missing_ok=True)
    interrupted_loader = subprocess.Popen(
        [sys.executable, str(ROOT / "fixture_loader.py"), "load", "--pause-after", "1"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    marker_seen = wait_for(marker, 10)
    os.killpg(interrupted_loader.pid, signal.SIGTERM)
    interrupted_exit = interrupted_loader.wait(timeout=10)
    interrupted_cleanup = row_cleanup(db)
    already_clean = row_cleanup(db)
    marker.unlink(missing_ok=True)
    ck("cleanup_failure_and_interruption", partial["zero_residue"] and repeated["zero_residue"] and marker_seen and interrupted_exit != 0 and interrupted_cleanup["zero_residue"] and already_clean["zero_residue"], {
        "partial_failure": partial,
        "repeated": repeated,
        "interrupted_process_pid": interrupted_loader.pid,
        "interruption_marker_seen": marker_seen,
        "interrupted_exit": interrupted_exit,
        "interrupted_cleanup": interrupted_cleanup,
        "already_clean": already_clean,
    })

    load_fixture(db)
    snapshot_result = write_snapshot(db)
    pre_rollback = state_digest(db)
    mutation = db[COLLECTION].update_one(
        {"_id": "stage2a-foundation-v1-marker", "owner": "ES-PKG-2026-004-V003"},
        {"$set": {"payload.value": 999, "rehearsal": "forced_failure"}},
    )
    forced_failure = state_digest(db)
    client.close()
    rollback_stop = orchestrate.stop()
    rollback_restart = orchestrate.start("full")
    client = mongo_client(env)
    db = client[env["DB_NAME"]]
    restored = restore_snapshot(db)
    post_rollback = state_digest(db)
    source_recovery = source_recovery_rehearsal(implementation_commit)
    ck("durable_rollback_recovery", mutation.modified_count == 1 and pre_rollback != forced_failure and pre_rollback == post_rollback and source_recovery["restored_matches"] and source_recovery["stage2a_absent_at_prechange_anchor"], {
        "snapshot": snapshot_result,
        "pre_rollback_digest": pre_rollback,
        "forced_failure_digest": forced_failure,
        "post_rollback_digest": post_rollback,
        "restore": restored,
        "process_stop": rollback_stop,
        "process_restart": rollback_restart,
        "source_recovery": source_recovery,
        "session_cache_disposition": "NOT_APPLICABLE_NO_EXTERNAL_SESSION_OR_CACHE_SERVICE; full process restart completed",
    })

    example_inputs = [ROOT / "example_command.py", ROOT / "execution-evidence-schema.json", ENV_FILE]
    passed_example = capture("foundation-example-pass", [sys.executable, str(ROOT / "example_command.py"), "pass"], 0, input_paths=example_inputs)
    failed_example = capture("foundation-example-intentional-fail", [sys.executable, str(ROOT / "example_command.py"), "intentional-fail"], 7, input_paths=example_inputs)
    schema = json.loads((ROOT / "execution-evidence-schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = []
    for record in (passed_example, failed_example):
        schema_errors.extend(str(x.message) for x in validator.iter_errors(record))
        core = dict(record)
        recorded_hash = core.pop("record_content_sha256")
        if hashlib.sha256((json.dumps(core, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()).hexdigest() != recorded_hash:
            schema_errors.append(f"record hash mismatch: {record['run_identifier']}")
        if dt.datetime.fromisoformat(str(record["utc_end"])) < dt.datetime.fromisoformat(str(record["utc_start"])):
            schema_errors.append(f"chronology mismatch: {record['run_identifier']}")
    blank = {name: "" for name in schema["required"]}
    blank_rejected = bool(list(validator.iter_errors(blank)))
    ck("evidence_capture_semantics", not schema_errors and blank_rejected and passed_example["result"] == failed_example["result"] == "PASS", {
        "pass_run": passed_example["run_identifier"],
        "intentional_fail_run": failed_example["run_identifier"],
        "input_hash_count_each": len(passed_example["input_artifact_hashes"]),
        "schema_errors": schema_errors,
        "semantically_empty_record_rejected": blank_rejected,
        "records_bound_to_implementation_commit": passed_example["commit_hash"] == failed_example["commit_hash"] == implementation_commit,
    })

    providers = provider_register(env)
    configured = [x for x in providers if x["configured"]]
    ck("provider_denial", not configured and all(x["attempt_count"] == 0 for x in providers), {
        "providers": len(providers),
        "configuration_names": len(PROVIDER_NAMES),
        "register": providers,
        "configured": [x["provider"] for x in configured],
        "attempt_count": 0,
        "attempt_count_basis": "full application ran under exact-port sandbox; provider configuration absent; provider-name negative tests denied; observed process sockets were approved loopback only",
    })

    final_owned_cleanup = row_cleanup(db)
    final_state_digest = state_digest(db)
    database_reset = drop_disposable_database(client, db)
    client.close()
    shutdown = orchestrate.stop()
    runtime_cleanup = cleanup_cli.purge_runtime()
    final_status = orchestrate.status()
    ck("controlled_shutdown", shutdown["ports_closed"] and shutdown["pid_files_absent"] and all(x["status"] == "STOPPED" for x in shutdown["processes"]), shutdown)
    ck("zero_residue", final_owned_cleanup["zero_residue"] and final_state_digest == EMPTY_STATE_DIGEST and database_reset["database_absent_after"] and runtime_cleanup["runtime_absent"] and not any(final_status[k] for k in ("mongo_alive", "mongo_port_open", "api_alive", "api_port_open")), {
        "starting_state_digest": empty_start,
        "ending_state_digest": final_state_digest,
        "owned_cleanup": final_owned_cleanup,
        "database_reset": database_reset,
        "runtime_cleanup": runtime_cleanup,
        "final_process_and_port_status": final_status,
    })

    artifacts.update({
        "implementation_commit": implementation_commit,
        "implementation_tree": implementation_tree,
        "environment": posture | {"ambient_attestation": attestation},
        "isolation_negative_tests": negative_results,
        "network_denials": denied_network,
        "interrupted_start": {"error": interrupted_error, "status": interrupted_status},
        "cold_start": start,
        "startup_inventory": startup_inventory,
        "network_inventory": {"observed_lines": network_lines, "wildcard": wildcard, "non_loopback": non_loopback},
        "fixture": next(x["detail"] for x in checks if x["check"] == "fixture_reproducibility"),
        "cleanup": next(x["detail"] for x in checks if x["check"] == "cleanup_failure_and_interruption"),
        "rollback": next(x["detail"] for x in checks if x["check"] == "durable_rollback_recovery"),
        "evidence_capture": next(x["detail"] for x in checks if x["check"] == "evidence_capture_semantics"),
        "shutdown": shutdown,
        "zero_residue": next(x["detail"] for x in checks if x["check"] == "zero_residue"),
    })
    ended = dt.datetime.now(dt.timezone.utc)
    failed = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_version": "2.0",
        "package_id": "ES-PKG-2026-004-V003",
        "validation": "PASS" if not failed else "FAIL",
        "started_utc": started.isoformat(),
        "ended_utc": ended.isoformat(),
        "checks": checks,
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "provider_attempt_count": 0,
        "provider_attempt_count_basis": "instrumented configuration denials, exact-port sandbox, full-process socket inventory",
        "production_access_count": 0,
        "production_access_count_basis": "loopback-only datastore/API and exact-port sandbox",
        "live_data_access_count": 0,
        "live_data_access_count_basis": "empty disposable database and owner-tagged synthetic fixture only",
        "cp3_suites_executed": 0,
        "golden_paths_executed": 0,
        "business_workflows_executed": 0,
        "fixture_digest": digest(fixture_data()),
        "artifacts": artifacts,
        "execution_status": "EXECUTION_NOT_AUTHORIZED",
    }
    (EVIDENCE / "FOUNDATION_VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (EVIDENCE / "FOUNDATION_VALIDATION.txt").write_text(
        f"validation={report['validation']}\nscore={report['pass_count']}/{report['check_count']}\nprovider_attempt_count=0\nproduction_access_count=0\nlive_data_access_count=0\ncp3_suites_executed=0\ngolden_paths_executed=0\nbusiness_workflows_executed=0\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except BaseException as exc:
        emergency: dict[str, object] = {"error_type": type(exc).__name__, "error": str(exc)}
        try:
            emergency["orchestrator_stop"] = orchestrate.stop()
        except Exception as stop_exc:
            emergency["orchestrator_stop_error"] = f"{type(stop_exc).__name__}: {stop_exc}"
        try:
            emergency["runtime_purge"] = cleanup_cli.purge_runtime()
        except Exception as purge_exc:
            emergency["runtime_purge_error"] = f"{type(purge_exc).__name__}: {purge_exc}"
        print(json.dumps({"emergency_cleanup": emergency}, indent=2), file=sys.stderr)
        raise
