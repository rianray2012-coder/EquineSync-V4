// D-14 — six-month billing cycle helpers (pure functions, no network).
import {
  BILLING_CYCLES,
  CYCLE_LABEL,
  CYCLE_SUFFIX,
  annualSavingsPct,
  checkoutableCycles,
  effectiveCycle,
  firstAvailableCycle,
  isPlanCheckoutable,
  offeredCycles,
  planOffersCycle,
  priceForCycle,
  resolveCheckoutCycle,
  savingsPctForCycle,
} from "./subscriptionBilling";

const advancedBarn = {
  tier_code: "advanced_barn",
  monthly_price_cents: 14999,
  six_month_price_cents: 74999,
  annual_price_cents: 149900,
  has_monthly: true,
  has_six_month: true,
  has_annual: true,
};

const starterBarn = {
  tier_code: "starter_barn",
  monthly_price_cents: 6999,
  six_month_price_cents: null,
  annual_price_cents: 69900,
  has_monthly: true,
  has_six_month: false,
  has_annual: true,
};

const enterprise = { tier_code: "enterprise", contact_sales: true };

test("cycle table lists monthly, six_month, annual with labels and suffixes", () => {
  expect(BILLING_CYCLES).toEqual(["monthly", "six_month", "annual"]);
  expect(CYCLE_LABEL.six_month).toBe("6-month");
  expect(CYCLE_SUFFIX.six_month).toBe("/6 mo");
});

test("only plans with a six-month amount offer the term", () => {
  expect(offeredCycles(advancedBarn)).toEqual(["monthly", "six_month", "annual"]);
  expect(offeredCycles(starterBarn)).toEqual(["monthly", "annual"]);
  expect(offeredCycles(enterprise)).toEqual([]);
  expect(planOffersCycle(starterBarn, "six_month")).toBe(false);
  expect(priceForCycle(advancedBarn, "six_month")).toBe(74999);
});

test("a plan without the chosen term falls back to monthly, never annual", () => {
  expect(effectiveCycle(advancedBarn, "six_month")).toBe("six_month");
  expect(effectiveCycle(starterBarn, "six_month")).toBe("monthly");
  expect(effectiveCycle(starterBarn, "annual")).toBe("annual");
});

test("savings are computed against the same number of monthly payments", () => {
  // 6 x 149.99 = 899.94 vs 749.99 -> 17%
  expect(savingsPctForCycle(advancedBarn, "six_month")).toBe(17);
  expect(savingsPctForCycle(advancedBarn, "annual")).toBe(17);
  expect(annualSavingsPct(advancedBarn)).toBe(17);
  expect(savingsPctForCycle(advancedBarn, "monthly")).toBeNull();
  expect(savingsPctForCycle(starterBarn, "six_month")).toBeNull();
});

test("checkoutability follows the has_* flags per cycle", () => {
  expect(isPlanCheckoutable(advancedBarn, "six_month")).toBe(true);
  expect(isPlanCheckoutable(starterBarn, "six_month")).toBe(false);
  expect(isPlanCheckoutable(enterprise, "monthly")).toBe(false);
  expect(isPlanCheckoutable(advancedBarn)).toBe(true);
  expect(checkoutableCycles({ ...advancedBarn, has_six_month: false })).toEqual(["monthly", "annual"]);
  expect(firstAvailableCycle({ ...advancedBarn, has_monthly: false })).toBe("six_month");
  expect(firstAvailableCycle(enterprise)).toBeNull();
});

test("resolveCheckoutCycle keeps the pick when available and falls back monthly-first", () => {
  expect(resolveCheckoutCycle(advancedBarn, "six_month")).toBe("six_month");
  expect(resolveCheckoutCycle({ ...advancedBarn, has_six_month: false }, "six_month")).toBe("monthly");
  expect(resolveCheckoutCycle({ ...advancedBarn, has_six_month: false, has_monthly: false }, "six_month")).toBe("annual");
  expect(resolveCheckoutCycle(enterprise, "monthly")).toBeNull();
});
