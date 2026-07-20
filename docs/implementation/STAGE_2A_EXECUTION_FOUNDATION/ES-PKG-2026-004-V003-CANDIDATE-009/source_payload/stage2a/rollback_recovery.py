#!/usr/bin/env python3
"""Durable, owner-scoped Stage 2A datastore recovery operations."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from lib.control import RUNTIME, canonical, cleanup, digest, load_env, mongo_client, restore, snapshot, state_digest

SNAPSHOT = RUNTIME / "recovery" / "stage2a-owned-records.json"


def write_snapshot(db) -> dict[str, object]:
    rows = snapshot(db)
    core = {"owner": "ES-PKG-2026-004-V003", "synthetic_only": True, "rows": rows}
    payload = core | {"payload_sha256": digest(core)}
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_bytes(canonical(payload))
    return {
        "snapshot": ".runtime/recovery/stage2a-owned-records.json",
        "snapshot_sha256": digest(payload),
        "payload_sha256": payload["payload_sha256"],
        "row_count": len(rows),
        "state_digest": state_digest(db),
        "durable": True,
    }


def restore_snapshot(db) -> dict[str, object]:
    payload = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    if payload.get("owner") != "ES-PKG-2026-004-V003" or payload.get("synthetic_only") is not True:
        raise RuntimeError("recovery snapshot ownership or synthetic marker invalid")
    expected = payload.pop("payload_sha256", "")
    if expected != digest(payload):
        raise RuntimeError("recovery snapshot digest mismatch")
    result = restore(db, payload["rows"])
    return result | {"payload_sha256": expected, "durable": True}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["snapshot", "mutate", "restore", "digest", "cleanup"])
    args = parser.parse_args()
    env = load_env()
    client = mongo_client(env)
    db = client[env["DB_NAME"]]
    try:
        if args.action == "snapshot":
            result = write_snapshot(db)
        elif args.action == "mutate":
            before = state_digest(db)
            changed = db.stage2a_foundation.update_one(
                {"_id": "stage2a-foundation-v1-marker", "owner": "ES-PKG-2026-004-V003"},
                {"$set": {"payload.value": 999, "rehearsal": "forced_failure"}},
            )
            result = {"before": before, "after": state_digest(db), "modified": changed.modified_count}
        elif args.action == "restore":
            result = restore_snapshot(db)
        elif args.action == "cleanup":
            result = cleanup(db)
        else:
            result = {"state_digest": state_digest(db)}
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        client.close()
