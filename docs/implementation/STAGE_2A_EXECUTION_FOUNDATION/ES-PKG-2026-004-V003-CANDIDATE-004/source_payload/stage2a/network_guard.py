#!/usr/bin/env python3
"""Instrument and deny every non-approved application network connection."""
from __future__ import annotations

import json
import socket
import threading
from pathlib import Path
from typing import Any

from lib.control import RUNTIME

LEDGER = RUNTIME / "network-guard.json"
APPROVED = {("127.0.0.1", 27029), ("localhost", 27029), ("127.0.0.1", 8019), ("localhost", 8019)}
_lock = threading.Lock()
_installed = False
_original_connect = socket.socket.connect
_original_connect_ex = socket.socket.connect_ex


def _initial() -> dict[str, Any]:
    return {
        "guard": "STAGE2A_APPLICATION_NETWORK_GUARD",
        "installed": True,
        "approved_endpoints": ["LOOPBACK_API_8019", "LOOPBACK_MONGODB_27029"],
        "unapproved_attempt_count": 0,
        "provider_or_external_attempt_count": 0,
        "attempts": [],
    }


def _write(value: dict[str, Any]) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    temporary = LEDGER.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(LEDGER)


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
        value["attempts"].append({
            "host_class": "UNAPPROVED_LOOPBACK" if parsed and parsed[0] in {"127.0.0.1", "localhost"} else "PROVIDER_OR_EXTERNAL",
            "port": parsed[1] if parsed else "NON_INET_ADDRESS",
            "denied": True,
        })
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
    _write(_initial())
    socket.socket.connect = _guarded_connect
    socket.socket.connect_ex = _guarded_connect_ex
    _installed = True


def ledger() -> dict[str, Any]:
    return json.loads(LEDGER.read_text(encoding="utf-8"))

