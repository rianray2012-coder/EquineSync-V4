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
from evidence_capture import capture, redact_output, sensitive_output_matches, validate_record_semantics
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
STARTUP_ORACLE_PATH = ROOT / "startup-side-effect-oracle.json"


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

    startup_attempt_events: list[dict[str, object]] = []

    def measured_start(attempt_id: str, profile: str, failpoint: str | None = None) -> dict[str, object]:
        began = dt.datetime.now(dt.timezone.utc)
        event: dict[str, object] = {
            "attempt_id": attempt_id, "profile": profile, "attempted": 1,
            "succeeded": 0, "failed": 0, "skipped": 0, "timed_out": 0, "unavailable": 0,
        }
        try:
            result = orchestrate.start(profile, failpoint)
        except TimeoutError as exc:
            event.update({"state": "TIMED_OUT", "timed_out": 1, "error_type": type(exc).__name__})
            raise
        except (FileNotFoundError, ModuleNotFoundError) as exc:
            event.update({"state": "UNAVAILABLE", "unavailable": 1, "error_type": type(exc).__name__})
            raise
        except Exception as exc:
            event.update({"state": "FAILED", "failed": 1, "error_type": type(exc).__name__})
            raise
        else:
            event.update({"state": "SUCCEEDED", "succeeded": 1})
            return result
        finally:
            event["utc_start"] = began.isoformat()
            event["utc_end"] = dt.datetime.now(dt.timezone.utc).isoformat()
            startup_attempt_events.append(event)

    def startup_summary() -> dict[str, object]:
        states = ("attempted", "succeeded", "failed", "skipped", "timed_out", "unavailable")
        totals = {state: sum(int(event[state]) for event in startup_attempt_events) for state in states}
        totals["arithmetic_valid"] = totals["attempted"] == totals["succeeded"] + totals["failed"] + totals["timed_out"] + totals["unavailable"]
        totals["events"] = deepcopy(startup_attempt_events)
        return totals

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
        measured_start("S2A-START-001-INTERRUPTED_FAILPOINT", "full", "after_datastore_ready")
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

    start = measured_start("S2A-START-002-COLD_FULL_APPLICATION", "full")
    startup_attempt_events.append({
        "attempt_id": "S2A-START-ALT-FOUNDATION-PROFILE", "profile": "foundation",
        "attempted": 0, "succeeded": 0, "failed": 0, "skipped": 1, "timed_out": 0, "unavailable": 0,
        "state": "SKIPPED_NOT_SELECTED_FULL_APPLICATION_REQUIRED",
        "utc_start": dt.datetime.now(dt.timezone.utc).isoformat(), "utc_end": dt.datetime.now(dt.timezone.utc).isoformat(),
    })
    ck("cold_start_full_application", start["profile"] == "full" and start["health"].get("status") == "ok", start)
    status = orchestrate.status()
    ck("process_identity", status["mongo_alive"] and status["api_alive"] and status["mongo_port_open"] and status["api_port_open"] and status["mongo_listener_identity_verified"] and status["api_listener_identity_verified"] and status["mongo_foreign_listener_pid"] is None and status["api_foreign_listener_pid"] is None, status)

    client = mongo_client(env)
    db = client[env["DB_NAME"]]
    startup_inventory = database_inventory(db)
    startup_documents = sum(int(x["document_count"]) for x in startup_inventory["collections"])
    startup_oracle = json.loads(STARTUP_ORACLE_PATH.read_text(encoding="utf-8"))
    startup_log_path = RUNTIME / "logs/api.log"
    startup_log = startup_log_path.read_text(encoding="utf-8", errors="replace")
    required_log_markers = {marker: marker in startup_log for marker in startup_oracle["startup_log_required_markers"]}
    prohibited_log_markers = {marker: marker in startup_log for marker in startup_oracle["startup_log_prohibited_markers"]}
    network_guard = json.loads((RUNTIME / "network-guard.json").read_text(encoding="utf-8"))
    startup_oracle_match = (
        startup_inventory["digest"] == startup_oracle["expected_database_inventory_sha256"]
        and len(startup_inventory["collections"]) == startup_oracle["expected_collection_count"]
        and startup_documents == startup_oracle["expected_document_count"]
    )
    startup_attempt_summary = startup_summary()
    ck("startup_side_effect_inventory", startup_oracle_match and all(required_log_markers.values()) and not any(prohibited_log_markers.values()) and network_guard["provider_or_external_attempt_count"] == 0 and startup_attempt_summary["arithmetic_valid"], {
        "profile": "full EquineSync application",
        "profile_control": env["STAGE2A_STARTUP_PROFILE"],
        "catalog_materialization": "DISABLED_BY_STAGE2A_WRAPPER",
        "collections_with_index_metadata": len(startup_inventory["collections"]),
        "startup_document_writes": startup_documents,
        "inventory_digest": startup_inventory["digest"],
        "oracle_id": startup_oracle["oracle_id"],
        "oracle_match": startup_oracle_match,
        "startup_log_sha256": file_sha(startup_log_path),
        "required_log_markers": required_log_markers,
        "prohibited_log_markers": prohibited_log_markers,
        "network_guard": network_guard,
        "attempt_outcomes": startup_attempt_summary,
        "disabled_side_effect_paths": {"skipped": 7, "basis": "six disabled background categories plus billing catalog materialization disabled by the controlled wrapper"},
        "known_side_effect_paths": startup_oracle["known_side_effect_paths"],
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
    rollback_restart = measured_start("S2A-START-003-ROLLBACK_RESTART", "full")
    startup_attempt_summary.clear()
    startup_attempt_summary.update(startup_summary())
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
    passed_example = capture("foundation-example-pass", [sys.executable, str(ROOT / "example_command.py"), "pass"], 0, input_paths=example_inputs, required_meaning=["stage2a foundation example: pass"])
    failed_example = capture("foundation-example-intentional-fail", [sys.executable, str(ROOT / "example_command.py"), "intentional-fail"], 7, input_paths=example_inputs, required_meaning=["stage2a foundation example: intentional-fail"])
    schema = json.loads((ROOT / "execution-evidence-schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = []
    for record in (passed_example, failed_example):
        schema_errors.extend(str(x.message) for x in validator.iter_errors(record))
        schema_errors.extend(validate_record_semantics(record, ROOT))
    def rehash(record: dict[str, object]) -> dict[str, object]:
        value = deepcopy(record); value.pop("record_content_sha256", None)
        return value | {"record_content_sha256": hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()).hexdigest()}
    contradictory = deepcopy(passed_example); contradictory["actual_result"]["exit_status"] = 9
    reverse = deepcopy(passed_example); reverse["utc_start"], reverse["utc_end"] = reverse["utc_end"], reverse["utc_start"]
    bad_stream = deepcopy(passed_example); bad_stream["evidence_file_hashes"]["stdout"] = "0" * 64
    weak_meaning = deepcopy(passed_example); weak_meaning["required_meaning"] = ["pass"]
    semantic_negative_results = {
        "contradictory_exit_rejected": bool(validate_record_semantics(rehash(contradictory), ROOT)),
        "reverse_chronology_rejected": bool(validate_record_semantics(rehash(reverse), ROOT)),
        "stream_hash_mismatch_rejected": bool(validate_record_semantics(rehash(bad_stream), ROOT)),
        "weak_substring_meaning_rejected": bool(validate_record_semantics(rehash(weak_meaning), ROOT)),
    }
    redaction_probes = [
        "operation=evidence-check api_key=synthetic-sensitive result=pass\n",
        "\"password\": \"correct horse battery staple\"\n",
        "password=correct horse battery staple\n",
        "bearer=supersecret\n",
    ]
    redacted_values = [redact_output(value) for value in redaction_probes]
    redacted_probe, redaction_replacements = redacted_values[0]
    semantic_negative_results["sensitive_value_redacted"] = redaction_replacements == 1 and "api_key=<REDACTED>" in redacted_probe and all(count >= 1 and not sensitive_output_matches(redacted) for redacted, count in redacted_values)
    semantic_negative_results["required_meaning_preserved"] = "operation=evidence-check" in redacted_probe and "result=pass" in redacted_probe
    blank = {name: "" for name in schema["required"]}
    blank_rejected = bool(list(validator.iter_errors(blank)))
    ck("evidence_capture_semantics", not schema_errors and blank_rejected and all(semantic_negative_results.values()) and passed_example["result"] == failed_example["result"] == "PASS", {
        "pass_run": passed_example["run_identifier"],
        "intentional_fail_run": failed_example["run_identifier"],
        "input_hash_count_each": len(passed_example["input_artifact_hashes"]),
        "schema_errors": schema_errors,
        "semantically_empty_record_rejected": blank_rejected,
        "semantic_negative_tests": semantic_negative_results,
        "records_bound_to_implementation_commit": passed_example["commit_hash"] == failed_example["commit_hash"] == implementation_commit,
    })

    final_network_guard = json.loads((RUNTIME / "network-guard.json").read_text(encoding="utf-8"))
    providers = provider_register(env, final_network_guard)
    configured = [x for x in providers if x["configured"]]
    provider_outcomes_valid = all(
        x["attempted_count"] == x["succeeded_count"] == x["failed_count"] == x["timed_out_count"] == x["unavailable_count"] == 0
        and x["skipped_count"] == 1 and x["state"] == "SKIPPED_NOT_CONFIGURED"
        for x in providers
    )
    provider_totals = {
        state: sum(int(row[f"{state}_count"]) for row in providers)
        for state in ("attempted", "succeeded", "failed", "skipped", "timed_out", "unavailable")
    }
    ck("provider_denial", not configured and provider_outcomes_valid and final_network_guard["provider_or_external_attempt_count"] == 0, {
        "providers": len(providers),
        "configuration_names": len(PROVIDER_NAMES),
        "register": providers,
        "configured": [x["provider"] for x in configured],
        "attempt_count": provider_totals["attempted"],
        "outcome_totals": provider_totals,
        "network_guard": final_network_guard,
        "attempt_count_basis": "application-level socket instrumentation measured zero provider/external attempts; every provider was explicitly classified SKIPPED_NOT_CONFIGURED; exact-port sandbox and process socket inventory independently corroborated zero external activity",
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
        "process_identity": status,
        "startup_inventory": startup_inventory,
        "startup_oracle": startup_oracle,
        "startup_log_review": {"sha256": next(x["detail"] for x in checks if x["check"] == "startup_side_effect_inventory")["startup_log_sha256"], "required_markers": required_log_markers, "prohibited_markers": prohibited_log_markers},
        "application_network_guard": final_network_guard,
        "provider_measurement": next(x["detail"] for x in checks if x["check"] == "provider_denial"),
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
        "provider_attempt_count": provider_totals["attempted"],
        "provider_attempt_count_basis": "application-level socket instrumentation measured zero provider/external attempts; every provider has an explicit skipped state; exact-port sandbox and full-process socket inventory independently corroborated zero",
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
        f"validation={report['validation']}\nscore={report['pass_count']}/{report['check_count']}\nprovider_attempt_count={report['provider_attempt_count']}\nproduction_access_count=0\nlive_data_access_count=0\ncp3_suites_executed=0\ngolden_paths_executed=0\nbusiness_workflows_executed=0\n",
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
