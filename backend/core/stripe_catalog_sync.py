"""Environment-aware Stripe catalog definitions for controlled sync scripts."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

from core.billing_provisioning import ADDON_PRICE_CATALOG, PLAN_CATALOG


CATALOG_VERSION = "2026-07-31"
CATALOG_SOURCE = "docs/PRICING_PLAN_ADDENDUM.md#updated-2026-06-19"
DEFAULT_CURRENCY = "usd"
DEFAULT_TAX_BEHAVIOR = "unspecified"


@dataclass(frozen=True)
class CatalogProduct:
    catalog_kind: str
    code: str
    lookup_key: str
    name: str
    description: str
    metadata: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CatalogPrice:
    catalog_kind: str
    code: str
    cycle: str
    lookup_key: str
    product_lookup_key: str
    unit_amount_cents: int
    currency: str
    recurring_interval: str
    tax_behavior: str
    metadata: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CatalogBlocker:
    code: str
    kind: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class StripeCatalogDefinition:
    environment: str
    products: list[CatalogProduct]
    prices: list[CatalogPrice]
    local_only_plan_codes: list[str]
    contact_sales_plan_codes: list[str]
    blockers: list[CatalogBlocker]

    def to_dict(self) -> dict[str, Any]:
        return {
            "environment": self.environment,
            "products": [row.to_dict() for row in self.products],
            "prices": [row.to_dict() for row in self.prices],
            "local_only_plan_codes": list(self.local_only_plan_codes),
            "contact_sales_plan_codes": list(self.contact_sales_plan_codes),
            "blockers": [row.to_dict() for row in self.blockers],
        }


def normalize_catalog_environment(environment: str | None) -> str:
    env = (environment or "sandbox").strip().lower()
    aliases = {
        "dev": "sandbox",
        "development": "sandbox",
        "test": "sandbox",
        "testing": "sandbox",
        "local": "sandbox",
        "prod": "live",
        "production": "live",
    }
    env = aliases.get(env, env)
    if env not in {"sandbox", "live"}:
        raise ValueError("Stripe catalog environment must be sandbox or live.")
    return env


def product_lookup_key(environment: str, catalog_kind: str, code: str) -> str:
    return f"equinesync.{normalize_catalog_environment(environment)}.{catalog_kind}.{code}"


def price_lookup_key(environment: str, catalog_kind: str, code: str, cycle: str) -> str:
    return f"{product_lookup_key(environment, catalog_kind, code)}.{cycle}"


def _metadata(
    *,
    environment: str,
    catalog_kind: str,
    code: str,
    lookup_key: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, str]:
    payload = {
        "equinesync_managed": "true",
        "equinesync_catalog_environment": environment,
        "equinesync_catalog_version": CATALOG_VERSION,
        "equinesync_catalog_kind": catalog_kind,
        "equinesync_lookup_key": lookup_key,
        "equinesync_source": CATALOG_SOURCE,
    }
    if catalog_kind == "plan":
        payload["tier_code"] = code
    else:
        payload["addon_code"] = code
    for key, value in (extra or {}).items():
        if value is not None:
            payload[key] = str(value)
    return payload


def _addon_name(addon_code: str) -> str:
    return " ".join(part.capitalize() for part in addon_code.split("_"))


def _valid_amount(value: Any) -> bool:
    return isinstance(value, int) and value > 0


def build_stripe_catalog_definition(environment: str = "sandbox") -> StripeCatalogDefinition:
    env = normalize_catalog_environment(environment)
    products: list[CatalogProduct] = []
    prices: list[CatalogPrice] = []
    blockers: list[CatalogBlocker] = []
    local_only_plan_codes: list[str] = []
    contact_sales_plan_codes: list[str] = []

    for tier in PLAN_CATALOG:
        code = tier["tier_code"]
        if not tier.get("stripe_provisioned") and not tier.get("contact_sales"):
            local_only_plan_codes.append(code)
            continue

        p_lookup = product_lookup_key(env, "plan", code)
        products.append(CatalogProduct(
            catalog_kind="plan",
            code=code,
            lookup_key=p_lookup,
            name=f"EquineSync {tier['name']} ({env})",
            description=tier["description"],
            metadata=_metadata(
                environment=env,
                catalog_kind="plan",
                code=code,
                lookup_key=p_lookup,
                extra={"contact_sales": str(bool(tier.get("contact_sales"))).lower()},
            ),
        ))

        if tier.get("contact_sales"):
            contact_sales_plan_codes.append(code)
            continue

        monthly_amount = tier.get("monthly_price_cents")
        annual_amount = tier.get("annual_price_cents")
        if not _valid_amount(monthly_amount):
            blockers.append(CatalogBlocker(
                code=code,
                kind="plan_missing_monthly_amount",
                message="Self-service plan is missing a positive monthly amount.",
            ))
        if not _valid_amount(annual_amount):
            blockers.append(CatalogBlocker(
                code=code,
                kind="plan_missing_annual_amount",
                message="Self-service plan is missing a positive annual amount.",
            ))
        for cycle, interval, amount in (
            ("monthly", "month", monthly_amount),
            ("annual", "year", annual_amount),
        ):
            if not _valid_amount(amount):
                continue
            lookup = price_lookup_key(env, "plan", code, cycle)
            prices.append(CatalogPrice(
                catalog_kind="plan",
                code=code,
                cycle=cycle,
                lookup_key=lookup,
                product_lookup_key=p_lookup,
                unit_amount_cents=int(amount),
                currency=DEFAULT_CURRENCY,
                recurring_interval=interval,
                tax_behavior=DEFAULT_TAX_BEHAVIOR,
                metadata=_metadata(
                    environment=env,
                    catalog_kind="plan",
                    code=code,
                    lookup_key=lookup,
                    extra={
                        "billing_cycle": cycle,
                        "interval": interval,
                        "unit_amount_cents": amount,
                        "currency": DEFAULT_CURRENCY,
                    },
                ),
            ))

    for addon_code, cfg in ADDON_PRICE_CATALOG.items():
        amount = cfg.get("unit_amount_cents")
        currency = (cfg.get("currency") or DEFAULT_CURRENCY).lower()
        interval = cfg.get("interval") or "month"
        if not _valid_amount(amount) or currency != DEFAULT_CURRENCY or interval not in {"month", "year"}:
            blockers.append(CatalogBlocker(
                code=addon_code,
                kind="addon_missing_canonical_terms",
                message="Add-on requires positive amount, usd currency, and month/year interval.",
            ))
            continue

        p_lookup = product_lookup_key(env, "addon", addon_code)
        products.append(CatalogProduct(
            catalog_kind="addon",
            code=addon_code,
            lookup_key=p_lookup,
            name=f"EquineSync {_addon_name(addon_code)} ({env})",
            description=f"EquineSync add-on: {_addon_name(addon_code)}.",
            metadata=_metadata(
                environment=env,
                catalog_kind="addon",
                code=addon_code,
                lookup_key=p_lookup,
                extra={
                    "limit_field": cfg.get("limit_field"),
                    "quantity_field": cfg.get("quantity_field"),
                },
            ),
        ))
        lookup = price_lookup_key(env, "addon", addon_code, "monthly" if interval == "month" else "annual")
        prices.append(CatalogPrice(
            catalog_kind="addon",
            code=addon_code,
            cycle="monthly" if interval == "month" else "annual",
            lookup_key=lookup,
            product_lookup_key=p_lookup,
            unit_amount_cents=int(amount),
            currency=currency,
            recurring_interval=interval,
            tax_behavior=DEFAULT_TAX_BEHAVIOR,
            metadata=_metadata(
                environment=env,
                catalog_kind="addon",
                code=addon_code,
                lookup_key=lookup,
                extra={
                    "billing_cycle": "monthly" if interval == "month" else "annual",
                    "interval": interval,
                    "unit_amount_cents": amount,
                    "currency": currency,
                    "limit_field": cfg.get("limit_field"),
                    "quantity_field": cfg.get("quantity_field"),
                },
            ),
        ))

    return StripeCatalogDefinition(
        environment=env,
        products=products,
        prices=prices,
        local_only_plan_codes=local_only_plan_codes,
        contact_sales_plan_codes=contact_sales_plan_codes,
        blockers=blockers,
    )


def catalog_counts(definition: StripeCatalogDefinition) -> dict[str, int]:
    plan_products = [p for p in definition.products if p.catalog_kind == "plan"]
    addon_products = [p for p in definition.products if p.catalog_kind == "addon"]
    plan_prices = [p for p in definition.prices if p.catalog_kind == "plan"]
    addon_prices = [p for p in definition.prices if p.catalog_kind == "addon"]
    return {
        "products": len(definition.products),
        "plan_products": len(plan_products),
        "addon_products": len(addon_products),
        "prices": len(definition.prices),
        "plan_prices": len(plan_prices),
        "addon_prices": len(addon_prices),
        "contact_sales_products": len(definition.contact_sales_plan_codes),
        "local_only_plans": len(definition.local_only_plan_codes),
        "blockers": len(definition.blockers),
    }


def object_lookup_map(rows: Iterable[CatalogProduct | CatalogPrice]) -> dict[str, CatalogProduct | CatalogPrice]:
    return {row.lookup_key: row for row in rows}
