#!/usr/bin/env python3
"""Idempotent, fail-closed Stage 2A datastore and runtime cleanup."""
from __future__ import annotations

import argparse
import json
import shutil

import orchestrate
from lib.control import OWNER, ROOT, RUNTIME, cleanup, drop_disposable_database, load_env, mongo_client


def purge_runtime() -> dict[str, object]:
    status = orchestrate.status()
    if any(status[key] for key in ("mongo_alive", "mongo_port_open", "api_alive", "api_port_open")):
        raise RuntimeError("runtime purge refused while a controlled process or port is active")
    if not RUNTIME.exists():
        return {"runtime_absent": True, "removed": False}
    marker = RUNTIME / ".owner.json"
    value = json.loads(marker.read_text(encoding="utf-8")) if marker.is_file() else {}
    if value != {"owner": OWNER, "disposable": True}:
        raise RuntimeError("runtime purge refused: ownership marker missing or invalid")
    if RUNTIME.parent.resolve() != ROOT.resolve():
        raise RuntimeError("runtime purge refused: path boundary mismatch")
    shutil.rmtree(RUNTIME)
    return {"runtime_absent": not RUNTIME.exists(), "removed": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["rows", "drop-database", "purge-runtime"])
    args = parser.parse_args()
    if args.action == "purge-runtime":
        result = purge_runtime()
    else:
        env = load_env()
        client = mongo_client(env)
        try:
            db = client[env["DB_NAME"]]
            result = cleanup(db) if args.action == "rows" else drop_disposable_database(client, db)
        finally:
            client.close()
    print(json.dumps(result, indent=2, sort_keys=True))
