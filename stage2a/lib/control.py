"""Fail-closed Stage 2A configuration, datastore, and hashing controls."""
from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Mapping
from urllib.parse import urlparse

PACKAGE_ID = "ES-PKG-2026-004-V003"
OWNER = PACKAGE_ID
DB_NAME = "equinesync_stage2a_synthetic"
COLLECTION = "stage2a_foundation"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
RUNTIME = ROOT / ".runtime"
EVIDENCE = ROOT / "evidence" / "latest"
FIXTURE = ROOT / "fixtures" / "foundation-v1.json"
ENV_FILE = ROOT / "config" / "stage2a.env"

ALLOWED_NAMES = {
    "APP_ENV", "STAGE2A_DISPOSABLE", "STAGE2A_SYNTHETIC_ONLY", "MONGO_URL", "DB_NAME",
    "STAGE2A_STARTUP_PROFILE",
    "STAGE2A_API_HOST", "STAGE2A_API_PORT", "STAGE2A_MONGO_PORT", "ALLOW_AUTO_SEED",
    "ALLOW_SEED_ROUTE", "DISABLE_TASK_MATERIALIZER", "DISABLE_NOTIFICATIONS",
    "DISABLE_OWNER_DIGEST", "DISABLE_OWNER_WEEKLY_RECAP", "DISABLE_AUTO_NUDGES",
    "DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER", "NO_PROXY", "HTTP_PROXY", "HTTPS_PROXY",
    "ALL_PROXY", "PATH", "TMPDIR", "LANG", "LC_ALL", "PYTHONPATH",
}
PROVIDER_NAMES = {
    "STRIPE_API_KEY": "Stripe", "STRIPE_SECRET_KEY": "Stripe", "STRIPE_WEBHOOK_SECRET": "Stripe",
    "RESEND_API_KEY": "Resend", "SENDGRID_API_KEY": "SendGrid", "TWILIO_AUTH_TOKEN": "Twilio",
    "AWS_ACCESS_KEY_ID": "Object storage", "AWS_SECRET_ACCESS_KEY": "Object storage",
    "OPENAI_API_KEY": "External AI", "GOOGLE_API_KEY": "External AI", "GEMINI_API_KEY": "External AI",
    "CLOUDFLARE_API_TOKEN": "Cloudflare", "RENDER_API_KEY": "Render", "VERCEL_TOKEN": "Vercel",
    "DOCUSIGN_INTEGRATION_KEY": "DocuSign", "ANALYTICS_WRITE_KEY": "Analytics",
    "STORAGE_ACCESS_KEY_ID": "Object storage", "STORAGE_SECRET_ACCESS_KEY": "Object storage",
    "EMERGENT_LLM_KEY": "External AI",
}
PROHIBITED_AMBIENT_NAMES = set(PROVIDER_NAMES) | {
    "JWT_SECRET", "DATABASE_URL", "PRODUCTION_DATABASE_URL",
    "EQUINESYNC_DEMO_PASSWORD", "SEED_DEMO_CLIENT_PASSWORD",
    "SEED_DEMO_EXTRA_OWNER_PASSWORD",
}
DISABLE_FLAGS = {
    "DISABLE_TASK_MATERIALIZER", "DISABLE_NOTIFICATIONS", "DISABLE_OWNER_DIGEST",
    "DISABLE_OWNER_WEEKLY_RECAP", "DISABLE_AUTO_NUDGES", "DISABLE_SUBSCRIPTION_EMAIL_DISPATCHER",
}


class IsolationError(RuntimeError):
    pass


def load_env() -> dict[str, str]:
    if (REPO / "backend/.env").exists():
        raise IsolationError("backend/.env is prohibited for the Stage 2A isolated profile")
    prohibited = sorted(name for name in PROHIBITED_AMBIENT_NAMES if (os.environ.get(name) or "").strip())
    if prohibited:
        raise IsolationError(
            "prohibited ambient configuration names present: " + ", ".join(prohibited)
        )
    values: dict[str, str] = {}
    for raw in ENV_FILE.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        key, value = raw.split("=", 1)
        values[key] = value
    for key in ("PATH", "TMPDIR", "LANG", "LC_ALL"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    values["PYTHONPATH"] = str(ROOT)
    return values


def ambient_name_attestation() -> dict[str, object]:
    """Record names and counts only; values are never returned."""
    present = sorted(name for name in PROHIBITED_AMBIENT_NAMES if (os.environ.get(name) or "").strip())
    return {
        "prohibited_names_present": present,
        "prohibited_name_count": len(present),
        "values_recorded": False,
    }


def validate_env(env: Mapping[str, str]) -> dict[str, object]:
    unknown = sorted(set(env) - ALLOWED_NAMES)
    configured_providers = sorted(name for name in PROVIDER_NAMES if (env.get(name) or "").strip())
    errors: list[str] = []
    if unknown: errors.append("environment allowlist violation: " + ", ".join(unknown))
    if configured_providers: errors.append("provider credentials/configuration present: " + ", ".join(configured_providers))
    if env.get("APP_ENV") != "stage2a": errors.append("APP_ENV must equal stage2a")
    if env.get("STAGE2A_DISPOSABLE") != "1": errors.append("disposable marker absent")
    if env.get("STAGE2A_SYNTHETIC_ONLY") != "1": errors.append("synthetic-only marker absent")
    if env.get("STAGE2A_STARTUP_PROFILE") != "CONTROLLED_ZERO_DOCUMENT_WRITES":
        errors.append("controlled zero-document-write startup profile absent")
    if env.get("DB_NAME") != DB_NAME: errors.append("datastore identity mismatch")
    parsed = urlparse(env.get("MONGO_URL", ""))
    if parsed.scheme != "mongodb" or parsed.hostname not in {"127.0.0.1", "localhost"} or parsed.port != 27029:
        errors.append("MongoDB must be loopback port 27029")
    if env.get("STAGE2A_API_HOST") != "127.0.0.1" or env.get("STAGE2A_API_PORT") != "8019":
        errors.append("foundation API must be loopback port 8019")
    if any(env.get(flag, "").lower() != "true" for flag in DISABLE_FLAGS):
        errors.append("all background/provider disable flags must be true")
    if env.get("ALLOW_AUTO_SEED", "").lower() != "false" or env.get("ALLOW_SEED_ROUTE", "").lower() != "false":
        errors.append("seed paths must be disabled")
    for proxy in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY"):
        if env.get(proxy) != "http://127.0.0.1:9": errors.append(f"{proxy} must use deny proxy")
    if errors: raise IsolationError("; ".join(errors))
    return {
        "status": "PASS", "environment": "stage2a", "datastore": DB_NAME,
        "mongo_endpoint_class": "LOOPBACK_ONLY", "api_endpoint_class": "LOOPBACK_ONLY",
        "provider_credentials_present": configured_providers, "unknown_names": unknown,
    }


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fixture_data() -> dict[str, object]:
    value = json.loads(FIXTURE.read_text(encoding="utf-8"))
    if value.get("synthetic_only") is not True or value.get("owner") != OWNER or value.get("collection") != COLLECTION:
        raise IsolationError("fixture ownership or synthetic marker invalid")
    return value


def mongo_client(env: Mapping[str, str]):
    validate_env(env)
    from pymongo import MongoClient
    client = MongoClient(env["MONGO_URL"], serverSelectionTimeoutMS=2000, connectTimeoutMS=2000)
    client.admin.command("ping")
    return client


def controlled_documents(db) -> list[dict[str, object]]:
    docs = list(db[COLLECTION].find({"owner": OWNER, "synthetic": True}, {"_id": 1, "kind": 1, "sequence": 1, "synthetic": 1, "owner": 1, "payload": 1}))
    return sorted(docs, key=lambda x: str(x["_id"]))


def state_digest(db) -> str:
    return digest(controlled_documents(db))


def database_inventory(db) -> dict[str, object]:
    collections = []
    for name in sorted(db.list_collection_names()):
        indexes = []
        for index_name, spec in sorted(db[name].index_information().items()):
            indexes.append({
                "name": index_name,
                "keys": [[str(k), int(v)] for k, v in spec.get("key", [])],
                "unique": bool(spec.get("unique", False)),
                "sparse": bool(spec.get("sparse", False)),
            })
        collections.append({
            "name": name,
            "document_count": db[name].count_documents({}),
            "indexes": indexes,
        })
    return {"database": db.name, "collections": collections, "digest": digest(collections)}


def drop_disposable_database(client, db) -> dict[str, object]:
    validate_env(load_env())
    if db.name != DB_NAME:
        raise IsolationError("database reset refused: datastore identity mismatch")
    before = database_inventory(db)
    client.drop_database(DB_NAME)
    remaining = DB_NAME in client.list_database_names()
    if remaining:
        raise IsolationError("database reset failed: disposable database remains")
    return {
        "database": DB_NAME,
        "before_digest": before["digest"],
        "before_collections": len(before["collections"]),
        "database_absent_after": True,
        "ending_inventory_digest": digest([]),
    }


def cleanup(db) -> dict[str, object]:
    if db.name != DB_NAME: raise IsolationError("cleanup refused: datastore identity mismatch")
    before = db[COLLECTION].count_documents({"owner": OWNER, "synthetic": True})
    result = db[COLLECTION].delete_many({"owner": OWNER, "synthetic": True})
    after = db[COLLECTION].count_documents({"owner": OWNER, "synthetic": True})
    return {"owned_before": before, "deleted": result.deleted_count, "owned_after": after, "zero_residue": after == 0}


def load_fixture(
    db,
    *,
    fail_after: int | None = None,
    pause_after: int | None = None,
    interruption_marker: Path | None = None,
) -> dict[str, object]:
    if db.name != DB_NAME: raise IsolationError("fixture load refused: datastore identity mismatch")
    fixture = fixture_data(); inserted = 0
    for row in fixture["records"]:
        db[COLLECTION].replace_one({"_id": row["_id"], "owner": OWNER}, row, upsert=True)
        inserted += 1
        if pause_after is not None and inserted >= pause_after:
            if interruption_marker is not None:
                interruption_marker.parent.mkdir(parents=True, exist_ok=True)
                interruption_marker.write_text(str(inserted), encoding="utf-8")
            time.sleep(300)
        if fail_after is not None and inserted >= fail_after:
            raise RuntimeError("intentional Stage 2A partial-load failure")
    return {"fixture_id": fixture["fixture_id"], "records": inserted, "state_digest": state_digest(db), "fixture_sha256": file_sha(FIXTURE)}


def snapshot(db) -> list[dict[str, object]]:
    return controlled_documents(db)


def restore(db, rows: list[dict[str, object]]) -> dict[str, object]:
    cleanup(db)
    for row in rows:
        db[COLLECTION].insert_one(row)
    return {"restored": len(rows), "state_digest": state_digest(db)}


def provider_register(env: Mapping[str, str] | None = None) -> list[dict[str, object]]:
    values = {} if env is None else env
    return [
        {
            "provider": p,
            "configuration_names": sorted(k for k,v in PROVIDER_NAMES.items() if v == p),
            "configured": any(bool((values.get(k) or "").strip()) for k,v in PROVIDER_NAMES.items() if v == p),
            "attempt_count": 0,
            "attempt_count_basis": "no provider module is invoked; exact-port sandbox denies every non-approved socket; process socket inventory contains approved loopback endpoints only",
            "control": "credential excluded; exact-port loopback sandbox; deny proxy; process socket inventory",
        }
        for p in sorted(set(PROVIDER_NAMES.values()))
    ]
