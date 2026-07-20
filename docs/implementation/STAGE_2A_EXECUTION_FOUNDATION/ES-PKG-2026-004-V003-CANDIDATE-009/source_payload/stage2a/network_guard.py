#!/usr/bin/env python3
"""Instrument and deny every non-approved application network connection."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import socket
import threading
import uuid
from pathlib import Path
from typing import Any

from lib.control import RUNTIME

LEDGER = RUNTIME / "network-guard.json"
APPROVED = {("127.0.0.1", 27029), ("localhost", 27029), ("127.0.0.1", 8019), ("localhost", 8019)}
_lock = threading.Lock()
_installed = False
_original_connect = socket.socket.connect
_original_connect_ex = socket.socket.connect_ex


def _canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _initial() -> dict[str, Any]:
    nonce = os.environ.get("STAGE2A_LAUNCH_NONCE", "")
    if not nonce:
        raise RuntimeError("network guard requires the orchestrator launch nonce")
    return {
        "schema_version": "2.0",
        "guard": "STAGE2A_APPLICATION_NETWORK_GUARD",
        "installed": True,
        "guard_session_id": uuid.uuid4().hex,
        "api_pid": os.getpid(),
        "api_process_group_id": os.getpgrp(),
        "launch_nonce_sha256": hashlib.sha256(nonce.encode()).hexdigest(),
        "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "approved_endpoints": ["LOOPBACK_API_8019", "LOOPBACK_MONGODB_27029"],
        "unapproved_attempt_count": 0,
        "provider_or_external_attempt_count": 0,
        "attempts": [],
        "provider_events": [],
        "event_count": 0,
        "event_chain_sha256": "0" * 64,
        "provider_registry_sha256": None,
    }


def _write(value: dict[str, Any]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    temporary = LEDGER.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(LEDGER)


def _append_event(value: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    sequence = int(value.get("event_count", 0)) + 1
    previous = str(value.get("event_chain_sha256", "0" * 64))
    core = {
        "schema_version": "1.0",
        "guard_session_id": value["guard_session_id"],
        "sequence": sequence,
        "utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "api_pid": value["api_pid"],
        "api_process_group_id": value["api_process_group_id"],
        "launch_nonce_sha256": value["launch_nonce_sha256"],
        **event,
        "previous_event_sha256": previous,
    }
    full = core | {"event_sha256": hashlib.sha256(_canonical(core)).hexdigest()}
    value["event_count"] = sequence
    value["event_chain_sha256"] = full["event_sha256"]
    return full


def _address_tuple(address: object) -> tuple[str, int] | None:
    if isinstance(address, tuple) and len(address) >= 2:
        try:
            return str(address[0]), int(address[1])
        except (TypeError, ValueError):
            return None
    return None


def _approved(address: object) -> bool:
    parsed = _address_tuple(address)
    return parsed in APPROVED if parsed else isinstance(address, (str, bytes, Path))


def _deny(address: object) -> None:
    parsed = _address_tuple(address)
    with _lock:
        try:
            value = json.loads(LEDGER.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            value = _initial()
        value["unapproved_attempt_count"] += 1
        value["provider_or_external_attempt_count"] += 1
        event = _append_event(value, {
            "event_type": "NETWORK_ATTEMPT_DENIED",
            "provider_id": "UNATTRIBUTED",
            "boundary_id": "UNATTRIBUTED_SOCKET_CONNECT",
            "host_class": "UNAPPROVED_LOOPBACK" if parsed and parsed[0] in {"127.0.0.1", "localhost"} else "PROVIDER_OR_EXTERNAL",
            "port": parsed[1] if parsed else "NON_INET_ADDRESS",
            "denied": True,
        })
        value["attempts"].append(event)
        _write(value)
    raise PermissionError("Stage 2A application network guard denied an unapproved endpoint")


def _guarded_connect(sock: socket.socket, address: object) -> None:
    if not _approved(address):
        _deny(address)
    return _original_connect(sock, address)


def _guarded_connect_ex(sock: socket.socket, address: object) -> int:
    if not _approved(address):
        _deny(address)
    return _original_connect_ex(sock, address)


def install() -> None:
    global _installed
    if _installed:
        return
    value = _initial()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    try:
        with LEDGER.open("x", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise RuntimeError("refusing to overwrite an existing network-guard session") from exc
    socket.socket.connect = _guarded_connect
    socket.socket.connect_ex = _guarded_connect_ex
    _installed = True


def ledger() -> dict[str, Any]:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def record_provider_capabilities(env: dict[str, str], registry_path: Path) -> None:
    """Emit one attributable runtime capability event for every registry row.

    Configuration values are never copied; only exact names and presence are
    recorded.  The registry is source-controlled and its hash is bound to the
    guard session.
    """
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    rows = registry.get("providers", [])
    with _lock:
        value = ledger()
        if value.get("provider_events"):
            raise RuntimeError("provider capability events already recorded for this guard session")
        value["provider_registry_sha256"] = _sha(registry_path)
        for row in rows:
            required = list(row["required_configuration_names"])
            present = sorted(name for name in required if (env.get(name) or "").strip())
            if present:
                raise RuntimeError("Stage 2A provider configuration unexpectedly present: " + ", ".join(present))
            missing = sorted(required)
            integration = row["integration_state"]
            state = row["unconfigured_state"]
            event_type = (
                "PREREQUISITE_EVALUATED"
                if integration == "PRESENT"
                else "INTEGRATION_ABSENCE_ATTESTED"
            )
            event = _append_event(value, {
                "event_type": event_type,
                "provider_id": row["provider_id"],
                "provider": row["provider"],
                "boundary_id": row["boundary_id"],
                "source_path": row["source_path"],
                "source_symbol": row["source_symbol"],
                "source_evidence_id": "S2A-SRC-" + hashlib.sha256(row["source_path"].encode()).hexdigest()[:12].upper(),
                "required_configuration_names": required,
                "present_configuration_names": [],
                "missing_configuration_names": missing,
                "configuration_state": "NOT_CONFIGURED",
                "integration_state": integration,
                "boundary_state": "NOT_EXERCISED_NO_TRIGGER" if integration == "PRESENT" else "NO_RUNTIME_BOUNDARY",
                "attempt_state": state,
                "reason_code": row["reason_code"],
                "attempted": 0,
                "succeeded": 0,
                "failed": 0,
                "skipped": 1 if state.startswith("SKIPPED_") else 0,
                "timed_out": 0,
                "unavailable": 1 if state.startswith("UNAVAILABLE_") else 0,
                "values_recorded": False,
            })
            value["provider_events"].append(event)
        _write(value)


def _verify_event_chain(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    events = sorted(
        list(value.get("provider_events", [])) + list(value.get("attempts", [])),
        key=lambda event: int(event.get("sequence", -1)),
    )
    previous = "0" * 64
    for expected_sequence, event in enumerate(events, 1):
        core = dict(event)
        recorded_hash = core.pop("event_sha256", "")
        if event.get("sequence") != expected_sequence:
            errors.append(f"event sequence mismatch at {expected_sequence}")
        if event.get("previous_event_sha256") != previous:
            errors.append(f"event chain predecessor mismatch at {expected_sequence}")
        calculated = hashlib.sha256(_canonical(core)).hexdigest()
        if calculated != recorded_hash:
            errors.append(f"event hash mismatch at {expected_sequence}")
        previous = str(recorded_hash)
    if value.get("event_count") != len(events) or value.get("event_chain_sha256") != previous:
        errors.append("ledger event count or chain head mismatch")
    return errors


def derive_provider_register(registry_path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Derive provider outcomes only from the active, process-bound ledger."""
    value = ledger()
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    identity = json.loads((RUNTIME / "api.pid").read_text(encoding="utf-8"))
    errors = _verify_event_chain(value)
    if value.get("guard") != "STAGE2A_APPLICATION_NETWORK_GUARD" or value.get("installed") is not True:
        errors.append("guard identity invalid")
    if value.get("provider_registry_sha256") != _sha(registry_path):
        errors.append("provider registry hash mismatch")
    for ledger_key, identity_key in (
        ("api_pid", "pid"),
        ("api_process_group_id", "process_group_id"),
        ("launch_nonce_sha256", "launch_nonce_sha256"),
    ):
        if value.get(ledger_key) != identity.get(identity_key):
            errors.append(f"guard process identity mismatch: {ledger_key}")
    expected = {row["provider_id"]: row for row in registry.get("providers", [])}
    events = value.get("provider_events", [])
    actual: dict[str, dict[str, Any]] = {}
    for event in events:
        provider_id = event.get("provider_id")
        if provider_id in actual:
            errors.append(f"duplicate provider event: {provider_id}")
        actual[str(provider_id)] = event
    if set(actual) != set(expected):
        errors.append(f"provider coverage mismatch missing={sorted(set(expected)-set(actual))} extra={sorted(set(actual)-set(expected))}")
    if value.get("provider_or_external_attempt_count") != len(value.get("attempts", [])):
        errors.append("network attempt total does not match attributable events")
    if any(event.get("provider_id") == "UNATTRIBUTED" for event in value.get("attempts", [])):
        errors.append("unattributed provider or external network attempt")
    rows: list[dict[str, Any]] = []
    for provider_id, spec in sorted(expected.items()):
        event = actual.get(provider_id, {})
        expected_event_type = "PREREQUISITE_EVALUATED" if spec["integration_state"] == "PRESENT" else "INTEGRATION_ABSENCE_ATTESTED"
        expected_boundary_state = "NOT_EXERCISED_NO_TRIGGER" if spec["integration_state"] == "PRESENT" else "NO_RUNTIME_BOUNDARY"
        state = event.get("attempt_state")
        expected_counts = {
            "attempted": 0,
            "succeeded": 0,
            "failed": 0,
            "skipped": 1 if str(state).startswith("SKIPPED_") else 0,
            "timed_out": 0,
            "unavailable": 1 if str(state).startswith("UNAVAILABLE_") else 0,
        }
        expected_event_keys = {
            "schema_version", "guard_session_id", "sequence", "utc", "api_pid",
            "api_process_group_id", "launch_nonce_sha256", "event_type", "provider_id",
            "provider", "boundary_id", "source_path", "source_symbol", "source_evidence_id",
            "required_configuration_names", "present_configuration_names",
            "missing_configuration_names", "configuration_state", "integration_state",
            "boundary_state", "attempt_state", "reason_code", "attempted", "succeeded",
            "failed", "skipped", "timed_out", "unavailable", "values_recorded",
            "previous_event_sha256", "event_sha256",
        }
        if set(event) != expected_event_keys:
            errors.append(f"{provider_id} event schema keys mismatch")
        for event_key, ledger_key in (
            ("guard_session_id", "guard_session_id"),
            ("api_pid", "api_pid"),
            ("api_process_group_id", "api_process_group_id"),
            ("launch_nonce_sha256", "launch_nonce_sha256"),
        ):
            if event.get(event_key) != value.get(ledger_key):
                errors.append(f"{provider_id} event {event_key} mismatch")
        try:
            event_utc = dt.datetime.fromisoformat(str(event.get("utc")))
            if event_utc.tzinfo is None or event_utc.utcoffset() != dt.timedelta(0):
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{provider_id} event UTC timestamp invalid")
        for field in ("provider", "boundary_id", "source_path", "source_symbol", "integration_state"):
            if event.get(field) != spec.get(field):
                errors.append(f"{provider_id} event {field} mismatch")
        required = list(spec["required_configuration_names"])
        if event.get("required_configuration_names") != required or event.get("present_configuration_names") != [] or event.get("missing_configuration_names") != sorted(required):
            errors.append(f"{provider_id} prerequisite measurement mismatch")
        if state != spec["unconfigured_state"]:
            errors.append(f"{provider_id} outcome state mismatch")
        if event.get("event_type") != expected_event_type:
            errors.append(f"{provider_id} event type mismatch")
        if event.get("configuration_state") != "NOT_CONFIGURED" or event.get("boundary_state") != expected_boundary_state:
            errors.append(f"{provider_id} configuration or boundary state mismatch")
        if event.get("reason_code") != spec["reason_code"]:
            errors.append(f"{provider_id} reason code mismatch")
        if event.get("source_evidence_id") != "S2A-SRC-" + hashlib.sha256(spec["source_path"].encode()).hexdigest()[:12].upper():
            errors.append(f"{provider_id} source evidence identity mismatch")
        if any(type(event.get(field)) is not int or event.get(field) != count for field, count in expected_counts.items()):
            errors.append(f"{provider_id} terminal outcome arithmetic mismatch")
        if event.get("values_recorded") is not False:
            errors.append(f"{provider_id} sensitive-value handling mismatch")
        rows.append({
            "provider_id": provider_id,
            "provider": spec["provider"],
            "boundary_id": spec["boundary_id"],
            "source_path": spec["source_path"],
            "source_symbol": spec["source_symbol"],
            "source_evidence_id": event.get("source_evidence_id"),
            "configuration_names": required,
            "configured": False,
            "integration_state": spec["integration_state"],
            "state": state,
            "attempt_count": event.get("attempted"),
            "attempted_count": event.get("attempted"),
            "succeeded_count": event.get("succeeded"),
            "failed_count": event.get("failed"),
            "skipped_count": event.get("skipped"),
            "timed_out_count": event.get("timed_out"),
            "unavailable_count": event.get("unavailable"),
            "event_sequence": event.get("sequence"),
            "event_sha256": event.get("event_sha256"),
            "guard_session_id": value.get("guard_session_id"),
            "measurement_basis": "PROCESS_BOUND_HASH_CHAINED_RUNTIME_CAPABILITY_EVENT",
            "global_unapproved_attempt_count": value.get("provider_or_external_attempt_count"),
        })
    if value.get("unapproved_attempt_count") != len(value.get("attempts", [])):
        errors.append("unapproved network attempt total does not match attempt events")
    if value.get("attempts"):
        errors.append("provider or external network attempts are prohibited in Stage 2A")
    if errors:
        raise RuntimeError("provider guard evidence invalid: " + "; ".join(errors))
    proof = {
        "guard_session_id": value["guard_session_id"],
        "api_pid": value["api_pid"],
        "api_process_group_id": value["api_process_group_id"],
        "launch_nonce_sha256": value["launch_nonce_sha256"],
        "provider_registry_sha256": value["provider_registry_sha256"],
        "provider_event_count": len(events),
        "network_attempt_event_count": len(value.get("attempts", [])),
        "unattributed_attempt_count": sum(1 for event in value.get("attempts", []) if event.get("provider_id") == "UNATTRIBUTED"),
        "event_chain_sha256": value["event_chain_sha256"],
        "event_chain_valid": True,
        "process_identity_bound": True,
    }
    return rows, proof
