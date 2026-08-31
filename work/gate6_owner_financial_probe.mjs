import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3007";
const apiUrl = process.env.API_URL || "http://127.0.0.1:8001/api";
const outDir = path.resolve("outputs/gate6_owner_financial_probe_2026-08-25");
fs.mkdirSync(outDir, { recursive: true });

const result = {
  timestamp: new Date().toISOString(),
  baseUrl,
  apiUrl,
  console: [],
  pageErrors: [],
  observations: {},
  apiChecks: {},
  screenshots: {},
};

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });

page.on("console", (msg) => {
  const type = msg.type();
  if (["error", "warning"].includes(type)) {
    result.console.push({ type, text: msg.text() });
  }
});
page.on("pageerror", (err) => {
  result.pageErrors.push(String(err?.stack || err?.message || err));
});

async function screenshot(name) {
  const file = path.join(outDir, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true });
  result.screenshots[name] = file;
}

async function visibleTestIds(ids) {
  const entries = {};
  for (const id of ids) {
    entries[id] = await page.locator(`[data-testid="${id}"]`).count();
  }
  return entries;
}

async function routeObservation(route, ids) {
  await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
  return {
    url: page.url(),
    title: await page.locator("h1, h2").first().innerText().catch(() => null),
    text: await page.locator("body").innerText({ timeout: 5000 }),
    testids: await visibleTestIds(ids),
  };
}

async function apiFetch(token, method, route, body) {
  const response = await page.evaluate(
    async ({ apiUrl, token, method, route, body }) => {
      const r = await fetch(`${apiUrl}${route}`, {
        method,
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
      const text = await r.text();
      let json = null;
      try {
        json = text ? JSON.parse(text) : null;
      } catch {
        json = null;
      }
      return { status: r.status, ok: r.ok, text, json };
    },
    { apiUrl, token, method, route, body },
  );
  return response;
}

await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
await page.getByTestId("login-email").fill("owner@equinesync.com");
await page.getByTestId("login-password").fill("demo1234");
await page.getByTestId("login-submit").click();
await page.waitForLoadState("networkidle");
await page.waitForSelector('[data-testid="sidebar"]', { timeout: 15000 });

const token = await page.evaluate(() => localStorage.getItem("equine_token"));

result.observations.afterLogin = {
  url: page.url(),
  testids: await visibleTestIds([
    "sidebar",
    "owner-portal-page",
    "owner-billing-card",
    "forbidden-page",
  ]),
};
await screenshot("01_owner_after_login");

await page.goto(`${baseUrl}/owner-portal`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="owner-billing-card"]', { timeout: 15000 });
result.observations.ownerPortalBilling = {
  url: page.url(),
  text: await page.locator('[data-testid="owner-billing-card"]').innerText({ timeout: 5000 }),
  testids: await visibleTestIds([
    "owner-portal-page",
    "owner-billing-card",
    "owner-balance",
    "owner-next-due",
    "owner-invoice-invoice-owner-open",
    "owner-invoice-invoice-other-owner-open",
    "invoice-expand-invoice-owner-open",
    "owner-invoice-detail-invoice-owner-open",
  ]),
};
await screenshot("02_owner_portal_billing");

const expand = page.getByTestId("invoice-expand-invoice-owner-open");
if (await expand.count()) {
  await expand.click();
  result.observations.ownerInvoiceExpanded = {
    testids: await visibleTestIds([
      "owner-invoice-detail-invoice-owner-open",
      "invoice-lines-invoice-owner-open",
      "invoice-breakdown-invoice-owner-open",
    ]),
    text: await page.locator('[data-testid="owner-invoice-detail-invoice-owner-open"]').innerText().catch(() => null),
  };
  await screenshot("03_owner_invoice_expanded");
}

const restrictedIds = [
  "forbidden-page",
  "billing-page",
  "payments-page",
  "financial-dashboard-page",
  "recurring-billing-page",
  "subscription-billing-page",
];
for (const route of ["/billing", "/payments", "/financial-dashboard", "/recurring-billing"]) {
  result.observations[`route:${route}`] = await routeObservation(route, restrictedIds);
  await screenshot(`route_${route.replaceAll("/", "_").replace(/^_/, "")}`);
}

result.observations["route:/billing/subscription"] = await routeObservation("/billing/subscription", [
  "forbidden-page",
  "subscription-billing-page",
  "subscription-status-card",
  "subscription-manage-stripe-btn",
  "subscription-plan-grid",
  "subscription-load-error",
]);
await screenshot("route_billing_subscription");

result.apiChecks.ownerInvoices = await apiFetch(token, "GET", "/invoices");
result.apiChecks.ownerPortalBilling = await apiFetch(token, "GET", "/owner-portal/billing");
result.apiChecks.prepareOwnerPayment = await apiFetch(
  token,
  "POST",
  "/owner-portal/billing/invoice-owner-open/prepare-payment",
);
result.apiChecks.ownerPayOwnInvoice = await apiFetch(token, "POST", "/invoices/invoice-owner-open/pay");
result.apiChecks.ownerPayOtherInvoice = await apiFetch(token, "POST", "/invoices/invoice-other-owner-open/pay");
result.apiChecks.refundEndpoint = await apiFetch(token, "POST", "/payments/refunds", { invoice_id: "invoice-owner-open" });
result.apiChecks.disputeEndpoint = await apiFetch(token, "POST", "/payments/disputes", { invoice_id: "invoice-owner-open" });
result.apiChecks.payoutEndpoint = await apiFetch(token, "GET", "/payouts");

await browser.close();

const jsonPath = path.join(outDir, "probe-result.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  ok: true,
  resultPath: jsonPath,
  screenshots: result.screenshots,
  observations: {
    afterLogin: result.observations.afterLogin,
    ownerPortalBilling: result.observations.ownerPortalBilling?.testids,
    ownerInvoiceExpanded: result.observations.ownerInvoiceExpanded?.testids,
    restrictedRoutes: Object.fromEntries(
      ["/billing", "/payments", "/financial-dashboard", "/recurring-billing", "/billing/subscription"]
        .map((route) => [route, result.observations[`route:${route}`]?.testids]),
    ),
  },
  apiChecks: Object.fromEntries(
    Object.entries(result.apiChecks).map(([key, value]) => [key, { status: value.status, ok: value.ok }]),
  ),
  consoleCount: result.console.length,
  pageErrorCount: result.pageErrors.length,
}, null, 2));
