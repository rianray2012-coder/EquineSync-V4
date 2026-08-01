"""Synchronize the EquineSync Stripe sandbox catalog.

Examples:
    cd backend
    .venv/bin/python scripts/sync_stripe_catalog.py --environment sandbox --dry-run --json
    .venv/bin/python scripts/sync_stripe_catalog.py --environment sandbox --apply --manifest-output ../outputs/stripe_sandbox_catalog_manifest.json --json --strict
    .venv/bin/python scripts/sync_stripe_catalog.py --environment sandbox --verify --json --strict
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
load_dotenv(ROOT / ".env")
load_dotenv(BACKEND / ".env")

import stripe  # noqa: E402
from motor.motor_asyncio import AsyncIOMotorClient  # noqa: E402

from core.billing_provisioning import upsert_environment_catalog_rows  # noqa: E402
from core.mongo import mongo_client_kwargs  # noqa: E402
from core.stripe_catalog_sync import (  # noqa: E402
    CatalogPrice,
    CatalogProduct,
    build_stripe_catalog_definition,
    catalog_counts,
)
from core.stripe_config import StripeConfigurationError, configure_stripe_api_key  # noqa: E402


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    getter = getattr(obj, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(obj, key, default)


def _metadata(obj: Any) -> dict[str, str]:
    meta = _get(obj, "metadata", {}) or {}
    if hasattr(meta, "to_dict_recursive"):
        meta = meta.to_dict_recursive()
    elif hasattr(meta, "_data"):
        meta = getattr(meta, "_data")
    elif hasattr(meta, "items"):
        meta = dict(meta.items())
    return {str(k): str(v) for k, v in dict(meta).items()}


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if hasattr(value, "to_dict_recursive"):
        return value.to_dict_recursive()
    return value


def _operation(action: str, kind: str, code: str, lookup_key: str, object_id: str | None = None) -> dict[str, Any]:
    return {
        "action": action,
        "kind": kind,
        "code": code,
        "lookup_key": lookup_key,
        "object_id": object_id,
    }


def _blocker(kind: str, code: str, message: str) -> dict[str, str]:
    return {"kind": kind, "code": code, "message": message}


def _list_active_products() -> list[Any]:
    return list(stripe.Product.list(limit=100, active=True).auto_paging_iter())


def _list_prices_for_product(product_id: str) -> list[Any]:
    return list(stripe.Price.list(limit=100, active=True, product=product_id).auto_paging_iter())


def _product_code(product: CatalogProduct) -> tuple[str, str]:
    if product.catalog_kind == "plan":
        return "tier_code", product.code
    return "addon_code", product.code


def _find_product(product: CatalogProduct, products: list[Any]) -> tuple[Any | None, list[Any], str]:
    exact = [
        row for row in products
        if _metadata(row).get("equinesync_lookup_key") == product.lookup_key
        and _metadata(row).get("equinesync_catalog_environment") == product.metadata["equinesync_catalog_environment"]
    ]
    if exact:
        return exact[0], exact, "match"

    code_key, code_value = _product_code(product)
    adoptable = [
        row for row in products
        if _metadata(row).get("equinesync_managed") == "true"
        and _metadata(row).get(code_key) == code_value
        and _metadata(row).get("equinesync_catalog_environment") in {None, "", product.metadata["equinesync_catalog_environment"]}
    ]
    if adoptable:
        return adoptable[0], adoptable, "adopt"
    return None, [], "create"


def _matching_price_by_lookup(price: CatalogPrice) -> tuple[Any | None, list[Any]]:
    result = stripe.Price.list(limit=10, active=True, lookup_keys=[price.lookup_key])
    rows = list(result.auto_paging_iter())
    return (rows[0] if rows else None), rows


def _price_recurring_interval(price_obj: Any) -> str | None:
    recurring = _get(price_obj, "recurring", {}) or {}
    return _get(recurring, "interval")


def _find_adoptable_price(price: CatalogPrice, product_id: str) -> Any | None:
    for row in _list_prices_for_product(product_id):
        meta = _metadata(row)
        code_key = "tier_code" if price.catalog_kind == "plan" else "addon_code"
        if meta.get("equinesync_managed") != "true":
            continue
        if meta.get(code_key) != price.code:
            continue
        if _get(row, "unit_amount") != price.unit_amount_cents:
            continue
        if _get(row, "currency") != price.currency:
            continue
        if _price_recurring_interval(row) != price.recurring_interval:
            continue
        return row
    return None


def _verify_product(product: CatalogProduct, stripe_product: Any) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    meta = _metadata(stripe_product)
    if _get(stripe_product, "livemode") is not False:
        blockers.append(_blocker("product_livemode_not_false", product.code, product.lookup_key))
    if not _get(stripe_product, "active", False):
        blockers.append(_blocker("product_inactive", product.code, product.lookup_key))
    for key, expected in product.metadata.items():
        if meta.get(key) != expected:
            blockers.append(_blocker("product_metadata_mismatch", product.code, f"{key} expected {expected}"))
    return blockers


def _verify_price(price: CatalogPrice, stripe_price: Any, product_id: str) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    meta = _metadata(stripe_price)
    if _get(stripe_price, "livemode") is not False:
        blockers.append(_blocker("price_livemode_not_false", price.code, price.lookup_key))
    if not _get(stripe_price, "active", False):
        blockers.append(_blocker("price_inactive", price.code, price.lookup_key))
    if _get(stripe_price, "product") != product_id:
        blockers.append(_blocker("price_product_mismatch", price.code, price.lookup_key))
    if _get(stripe_price, "unit_amount") != price.unit_amount_cents:
        blockers.append(_blocker("price_amount_mismatch", price.code, price.lookup_key))
    if _get(stripe_price, "currency") != price.currency:
        blockers.append(_blocker("price_currency_mismatch", price.code, price.lookup_key))
    if _price_recurring_interval(stripe_price) != price.recurring_interval:
        blockers.append(_blocker("price_interval_mismatch", price.code, price.lookup_key))
    if _get(stripe_price, "lookup_key") != price.lookup_key:
        blockers.append(_blocker("price_lookup_key_mismatch", price.code, price.lookup_key))
    tax_behavior = _get(stripe_price, "tax_behavior")
    if tax_behavior not in {None, price.tax_behavior}:
        blockers.append(_blocker("price_tax_behavior_mismatch", price.code, price.lookup_key))
    for key, expected in price.metadata.items():
        if meta.get(key) != expected:
            blockers.append(_blocker("price_metadata_mismatch", price.code, f"{key} expected {expected}"))
    return blockers


def _create_product(product: CatalogProduct) -> Any:
    return stripe.Product.create(
        name=product.name,
        description=product.description,
        metadata=product.metadata,
        idempotency_key=f"equinesync-product-{product.lookup_key}",
    )


def _adopt_product(product: CatalogProduct, stripe_product: Any) -> Any:
    merged = {**_metadata(stripe_product), **product.metadata}
    return stripe.Product.modify(_get(stripe_product, "id"), metadata=merged)


def _create_price(price: CatalogPrice, product_id: str) -> Any:
    return stripe.Price.create(
        product=product_id,
        unit_amount=price.unit_amount_cents,
        currency=price.currency,
        recurring={"interval": price.recurring_interval},
        lookup_key=price.lookup_key,
        tax_behavior=price.tax_behavior,
        metadata=price.metadata,
        idempotency_key=f"equinesync-price-{price.lookup_key}",
    )


def _adopt_price(price: CatalogPrice, stripe_price: Any) -> Any:
    merged = {**_metadata(stripe_price), **price.metadata}
    return stripe.Price.modify(
        _get(stripe_price, "id"),
        lookup_key=price.lookup_key,
        metadata=merged,
    )


def _prove_sandbox_key() -> dict[str, Any]:
    resolved = configure_stripe_api_key(require_present=True, expected_mode="sandbox")
    balance = stripe.Balance.retrieve()
    livemode = _get(balance, "livemode")
    if livemode is not False:
        raise StripeConfigurationError("Stripe API key did not prove sandbox livemode=false.")
    return {
        "key_source": resolved.source if resolved else None,
        "key_mode": resolved.mode if resolved else None,
        "livemode": livemode,
    }


def _reconcile_stripe(definition, *, apply: bool) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "products": [],
        "prices": [],
        "blockers": [],
        "product_ids_by_lookup": {},
        "price_ids_by_lookup": {},
    }
    product_actions_by_lookup: dict[str, str] = {}
    active_products = _list_active_products()

    for product in definition.products:
        stripe_product, matches, action = _find_product(product, active_products)
        operation_action = action
        if len(matches) > 1:
            receipt["blockers"].append(_blocker("duplicate_product_match", product.code, product.lookup_key))
            continue
        if not stripe_product:
            if apply:
                stripe_product = _create_product(product)
                active_products.append(stripe_product)
                operation_action = "created"
            else:
                operation_action = "would_create"
            receipt["products"].append(_operation(
                operation_action,
                product.catalog_kind,
                product.code,
                product.lookup_key,
                _get(stripe_product, "id") if stripe_product else None,
            ))
        elif action == "adopt":
            if apply:
                stripe_product = _adopt_product(product, stripe_product)
                operation_action = "adopted"
            else:
                operation_action = "would_adopt"
            receipt["products"].append(_operation(
                operation_action,
                product.catalog_kind,
                product.code,
                product.lookup_key,
                _get(stripe_product, "id"),
            ))
        else:
            operation_action = "matched"
            receipt["products"].append(_operation("matched", product.catalog_kind, product.code, product.lookup_key, _get(stripe_product, "id")))

        if stripe_product:
            product_id = _get(stripe_product, "id")
            receipt["product_ids_by_lookup"][product.lookup_key] = product_id
            if operation_action != "would_adopt":
                receipt["blockers"].extend(_verify_product(product, stripe_product))
        product_actions_by_lookup[product.lookup_key] = operation_action

    for price in definition.prices:
        product_id = receipt["product_ids_by_lookup"].get(price.product_lookup_key)
        if not product_id:
            if product_actions_by_lookup.get(price.product_lookup_key) == "would_create":
                receipt["prices"].append(_operation(
                    "would_create",
                    price.catalog_kind,
                    price.code,
                    price.lookup_key,
                    None,
                ))
            else:
                receipt["blockers"].append(_blocker("price_product_missing", price.code, price.lookup_key))
            continue
        stripe_price, matches = _matching_price_by_lookup(price)
        if len(matches) > 1:
            receipt["blockers"].append(_blocker("duplicate_price_lookup_key", price.code, price.lookup_key))
            continue

        action = "matched"
        if not stripe_price:
            adoptable = _find_adoptable_price(price, product_id)
            if adoptable:
                if apply:
                    stripe_price = _adopt_price(price, adoptable)
                    action = "adopted"
                else:
                    stripe_price = adoptable
                    action = "would_adopt"
            else:
                if apply:
                    stripe_price = _create_price(price, product_id)
                    action = "created"
                else:
                    action = "would_create"

        receipt["prices"].append(_operation(
            action,
            price.catalog_kind,
            price.code,
            price.lookup_key,
            _get(stripe_price, "id") if stripe_price else None,
        ))
        if stripe_price:
            receipt["price_ids_by_lookup"][price.lookup_key] = _get(stripe_price, "id")
            if action != "would_adopt":
                receipt["blockers"].extend(_verify_price(price, stripe_price, product_id))

    return receipt


def _ids_for_mongo(definition, stripe_receipt) -> tuple[dict[str, dict[str, str | None]], dict[str, dict[str, str | None]]]:
    product_ids = stripe_receipt["product_ids_by_lookup"]
    price_ids = stripe_receipt["price_ids_by_lookup"]
    plan_ids: dict[str, dict[str, str | None]] = {}
    addon_ids: dict[str, dict[str, str | None]] = {}

    for product in definition.products:
        product_id = product_ids.get(product.lookup_key)
        if product.catalog_kind == "plan":
            plan_ids.setdefault(product.code, {})["product_id"] = product_id
        else:
            addon_ids.setdefault(product.code, {})["product_id"] = product_id

    for price in definition.prices:
        price_id = price_ids.get(price.lookup_key)
        if price.catalog_kind == "plan":
            row = plan_ids.setdefault(price.code, {})
            if price.cycle == "monthly":
                row["monthly_price_id"] = price_id
            elif price.cycle == "annual":
                row["annual_price_id"] = price_id
        else:
            addon_ids.setdefault(price.code, {})["price_id"] = price_id

    return plan_ids, addon_ids


async def _verify_mongo_rows(db, definition, stripe_receipt) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    plan_ids, addon_ids = _ids_for_mongo(definition, stripe_receipt)
    for code, ids in plan_ids.items():
        row = await db.plans.find_one({"tier_code": code}, {"_id": 0})
        sub_row = await db.subscription_plans.find_one({"plan_code": code}, {"_id": 0})
        if not row:
            blockers.append(_blocker("mongo_plan_missing", code, "plans row missing"))
        if not sub_row:
            blockers.append(_blocker("mongo_subscription_plan_missing", code, "subscription_plans row missing"))
        if row:
            for field, expected in (
                ("stripe_product_id", ids.get("product_id")),
                ("stripe_price_id_monthly", ids.get("monthly_price_id")),
                ("stripe_price_id_annual", ids.get("annual_price_id")),
            ):
                if expected and row.get(field) != expected:
                    blockers.append(_blocker("mongo_plan_id_mismatch", code, field))
            if row.get("stripe_catalog_environment") != definition.environment:
                blockers.append(_blocker("mongo_plan_environment_mismatch", code, "plans environment mismatch"))
            if row.get("stripe_catalog_ready") is not True:
                blockers.append(_blocker("mongo_plan_not_ready", code, "plans readiness false"))
        if sub_row:
            for field, expected in (
                ("stripe_product_id", ids.get("product_id")),
                ("stripe_monthly_price_id", ids.get("monthly_price_id")),
                ("stripe_annual_price_id", ids.get("annual_price_id")),
            ):
                if expected and sub_row.get(field) != expected:
                    blockers.append(_blocker("mongo_subscription_plan_id_mismatch", code, field))

    for code, ids in addon_ids.items():
        row = await db.subscription_addons.find_one({"addon_code": code}, {"_id": 0})
        if not row:
            blockers.append(_blocker("mongo_addon_missing", code, "subscription_addons row missing"))
            continue
        for field, expected in (
            ("stripe_product_id", ids.get("product_id")),
            ("stripe_price_id", ids.get("price_id")),
        ):
            if expected and row.get(field) != expected:
                blockers.append(_blocker("mongo_addon_id_mismatch", code, field))
        if row.get("stripe_catalog_environment") != definition.environment:
            blockers.append(_blocker("mongo_addon_environment_mismatch", code, "addon environment mismatch"))
        if row.get("stripe_catalog_ready") is not True:
            blockers.append(_blocker("mongo_addon_not_ready", code, "addon readiness false"))
    return blockers


async def _sync_mongo(db, definition, stripe_receipt, *, verified_at: str) -> dict[str, Any]:
    plan_ids, addon_ids = _ids_for_mongo(definition, stripe_receipt)
    await upsert_environment_catalog_rows(
        db,
        environment=definition.environment,
        plan_ids=plan_ids,
        addon_ids=addon_ids,
        ready=True,
        verified_at=verified_at,
        blockers=[],
    )
    return {
        "plans_upserted": len(plan_ids) + len(definition.local_only_plan_codes),
        "addons_upserted": len(addon_ids),
        "verified_at": verified_at,
    }


async def _run(args) -> tuple[int, dict[str, Any]]:
    if args.environment != "sandbox":
        return 2, {
            "status": "blocked",
            "determination": "BLOCKED_UNSUPPORTED_ENVIRONMENT",
            "blockers": [_blocker("unsupported_environment", args.environment, "This sync script is approved for sandbox only.")],
        }

    definition = build_stripe_catalog_definition(args.environment)
    receipt: dict[str, Any] = {
        "generated_at": _now_iso(),
        "mode": "apply" if args.apply else "verify" if args.verify else "dry-run",
        "environment": definition.environment,
        "definition_counts": catalog_counts(definition),
        "definition_blockers": [row.to_dict() for row in definition.blockers],
    }
    if definition.blockers:
        receipt["status"] = "blocked"
        receipt["blockers"] = [row.to_dict() for row in definition.blockers]
        return 2, receipt

    try:
        receipt["stripe_key"] = _prove_sandbox_key()
    except Exception as ex:
        receipt["status"] = "blocked"
        receipt["blockers"] = [_blocker("stripe_sandbox_key_not_proven", "stripe", str(ex))]
        return 2, receipt

    stripe_receipt = _reconcile_stripe(definition, apply=args.apply)
    receipt["stripe_reconciliation"] = {
        key: value
        for key, value in stripe_receipt.items()
        if key not in {"product_ids_by_lookup", "price_ids_by_lookup"}
    }
    blockers = list(stripe_receipt["blockers"])
    if args.verify:
        for row in receipt["stripe_reconciliation"].get("products") or []:
            if str(row.get("action", "")).startswith("would_"):
                blockers.append(_blocker("product_not_verified", row["code"], row["lookup_key"]))
        for row in receipt["stripe_reconciliation"].get("prices") or []:
            if str(row.get("action", "")).startswith("would_"):
                blockers.append(_blocker("price_not_verified", row["code"], row["lookup_key"]))

    mongo_summary = {"connected": False, "updates": None, "verification_blockers": []}
    mongo_url = os.environ.get("MONGO_URL")
    db_name = os.environ.get("DB_NAME") or "equinesync"
    if mongo_url:
        client = AsyncIOMotorClient(mongo_url, **mongo_client_kwargs(mongo_url))
        try:
            db = client[db_name]
            await db.command("ping")
            mongo_summary["connected"] = True
            if args.apply and not blockers:
                mongo_summary["updates"] = await _sync_mongo(db, definition, stripe_receipt, verified_at=_now_iso())
            if args.verify:
                mongo_blockers = await _verify_mongo_rows(db, definition, stripe_receipt)
                mongo_summary["verification_blockers"] = mongo_blockers
                blockers.extend(mongo_blockers)
        except Exception as ex:
            blockers.append(_blocker("mongo_unreachable", "mongo", str(ex)))
        finally:
            client.close()
    elif args.apply or args.verify:
        blockers.append(_blocker("mongo_missing", "mongo", "MONGO_URL is required for apply/verify."))

    receipt["mongo"] = mongo_summary
    receipt["blockers"] = blockers
    receipt["status"] = "blocked" if blockers else "ok"
    if args.apply and not blockers:
        receipt["determination"] = "stripe_sandbox_catalog_applied"
    elif args.verify and not blockers:
        receipt["determination"] = "stripe_sandbox_catalog_verified"
    elif not args.apply and not args.verify and not blockers:
        receipt["determination"] = "stripe_sandbox_catalog_dry_run_clean"
    else:
        receipt["determination"] = "stripe_sandbox_catalog_blocked"
    return (2 if blockers and args.strict else 0), receipt


def _parse_args():
    parser = argparse.ArgumentParser(description="Dry-run, apply, or verify the Stripe sandbox catalog.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Inspect Stripe and report planned changes without mutation.")
    mode.add_argument("--apply", action="store_true", help="Create/adopt missing sandbox Products/Prices and update Mongo rows.")
    mode.add_argument("--verify", action="store_true", help="Verify Stripe sandbox objects and Mongo rows.")
    parser.add_argument("--environment", default="sandbox", choices=["sandbox"], help="Catalog environment. Sandbox only.")
    parser.add_argument("--manifest-output", help="Write sanitized JSON receipt to this path.")
    parser.add_argument("--json", action="store_true", help="Print the sanitized JSON receipt.")
    parser.add_argument("--strict", action="store_true", help="Return non-zero when blockers are present.")
    return parser.parse_args()


def _print_text(receipt: dict[str, Any]) -> None:
    recon = receipt.get("stripe_reconciliation") or {}
    product_actions = {}
    for row in recon.get("products") or []:
        product_actions[row["action"]] = product_actions.get(row["action"], 0) + 1
    price_actions = {}
    for row in recon.get("prices") or []:
        price_actions[row["action"]] = price_actions.get(row["action"], 0) + 1
    print(f"status={receipt.get('status')}")
    print(f"determination={receipt.get('determination')}")
    print(f"environment={receipt.get('environment')}")
    print(f"definition_counts={receipt.get('definition_counts')}")
    print(f"product_actions={product_actions}")
    print(f"price_actions={price_actions}")
    print(f"mongo={receipt.get('mongo')}")
    blockers = receipt.get("blockers") or []
    print(f"blockers={len(blockers)}")
    for blocker in blockers:
        print(f"blocker {blocker.get('kind')} {blocker.get('code')}: {blocker.get('message')}")


def main() -> int:
    args = _parse_args()
    code, receipt = asyncio.run(_run(args))
    receipt = _jsonable(receipt)
    if args.manifest_output:
        out = Path(args.manifest_output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        _print_text(receipt)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
