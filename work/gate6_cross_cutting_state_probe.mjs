import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3008";
const apiUrl = process.env.API_URL || "http://127.0.0.1:8002/api";
const outDir = path.resolve("outputs/gate6_cross_cutting_state_probe_2026-08-25");
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
const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
const page = await context.newPage();

page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) {
    result.console.push({ type: msg.type(), text: msg.text(), url: page.url() });
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

async function counts(ids) {
  const entries = {};
  for (const id of ids) entries[id] = await page.locator(`[data-testid="${id}"]`).count();
  return entries;
}

async function bodyText() {
  return page.locator("body").innerText({ timeout: 5000 }).catch(() => "");
}

async function clearAuth() {
  await page.goto(`${baseUrl}/login`, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    localStorage.removeItem("equine_token");
    localStorage.removeItem("equine_user");
    localStorage.removeItem("equine_task_completion_queue_v1");
    sessionStorage.clear();
  });
}

async function login(email) {
  await clearAuth();
  await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
  await page.getByTestId("login-email").fill(email);
  await page.getByTestId("login-password").fill("demo1234");
  await page.getByTestId("login-submit").click();
  await page.waitForLoadState("networkidle");
  await page.waitForSelector('[data-testid="sidebar"]', { timeout: 15000 });
  return page.evaluate(() => localStorage.getItem("equine_token"));
}

async function apiFetch(token, method, route, body) {
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
  try { json = text ? JSON.parse(text) : null; } catch {}
  return { status: r.status, ok: r.ok, text, json };
}

// BOOTSTRAPPING / PROTECTED REDIRECT
await clearAuth();
await page.goto(`${baseUrl}/today`, { waitUntil: "networkidle" });
result.observations.protectedRedirect = {
  url: page.url(),
  text: await bodyText(),
  testids: await counts(["login-page", "sidebar", "today-page", "forbidden-page"]),
};
await screenshot("01_protected_redirect_login");

// AUTHORIZED READY SHELL + NAV AUTHORITY
const adminToken = await login("admin@equinesync.com");
result.observations.adminReadyShell = {
  url: page.url(),
  testids: await counts([
    "sidebar",
    "global-search",
    "nav-dashboard",
    "nav-setup",
    "nav-horses",
    "nav-staff",
    "nav-documents",
    "nav-ai-drafts",
    "nav-billing",
  ]),
};
await screenshot("02_admin_ready_shell");

const ownerToken = await login("owner@equinesync.com");
result.observations.ownerNavigationAuthority = {
  url: page.url(),
  testids: await counts([
    "sidebar",
    "nav-my-horse",
    "nav-documents",
    "nav-ai-drafts",
    "nav-staff",
    "nav-owners",
    "nav-facility-settings",
  ]),
};
await screenshot("03_owner_navigation_authority");

// DENIED STATE
await page.goto(`${baseUrl}/forms-signatures`, { waitUntil: "networkidle" });
result.observations.ownerDeniedLegalRoute = {
  url: page.url(),
  text: await bodyText(),
  testids: await counts(["forbidden-page", "forms-signatures-page", "sidebar"]),
};
await screenshot("04_owner_denied_forms_signatures");

// SETUP READINESS ERROR STATE
await login("admin@equinesync.com");
await page.route("**/api/onboarding/readiness", async (route) => {
  await route.fulfill({
    status: 503,
    contentType: "application/json",
    body: JSON.stringify({ detail: "Gate 6 synthetic readiness outage" }),
  });
});
await page.goto(`${baseUrl}/setup/facility`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="setup-readiness-error"]', { timeout: 15000 });
result.observations.setupReadinessError = {
  url: page.url(),
  text: await bodyText(),
  testids: await counts(["setup-readiness-error", "forbidden-page", "sidebar"]),
};
await screenshot("05_setup_readiness_error");
await page.unroute("**/api/onboarding/readiness");

// PAGE-LEVEL LOADING + EMPTY + UNAVAILABLE STATES
await page.route("**/api/feature-modules/training-plans", async (route) => {
  await new Promise((resolve) => setTimeout(resolve, 1200));
  await route.fulfill({
    status: 200,
    contentType: "application/json",
    body: JSON.stringify({ records: [] }),
  });
});
await page.route("**/api/horses", async (route) => {
  await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify([]) });
});
await page.route("**/api/trainer/directory", async (route) => {
  await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ records: [] }) });
});
await page.goto(`${baseUrl}/training-plans`, { waitUntil: "domcontentloaded" });
await page.waitForSelector('[data-testid="training-plans-page"]', { timeout: 15000 });
const loadingText = await bodyText();
await screenshot("06_training_plans_loading");
await page.waitForSelector('[data-testid="training-plans-empty-add"]', { timeout: 15000 });
result.observations.trainingPlansLoadingAndEmpty = {
  url: page.url(),
  loadingTextObserved: /Loading training plans/i.test(loadingText),
  finalText: await bodyText(),
  testids: await counts(["training-plans-page", "training-plans-empty-add"]),
};
await screenshot("07_training_plans_empty");
await page.unroute("**/api/feature-modules/training-plans");
await page.unroute("**/api/horses");
await page.unroute("**/api/trainer/directory");

await page.route("**/api/feature-modules/training-plans", async (route) => {
  await route.fulfill({
    status: 500,
    contentType: "application/json",
    body: JSON.stringify({ detail: "Gate 6 synthetic training-plan outage" }),
  });
});
await page.goto(`${baseUrl}/training-plans`, { waitUntil: "networkidle" });
await page.waitForFunction(() => document.body.innerText.includes("Training plans unavailable"), null, { timeout: 15000 });
result.observations.trainingPlansUnavailable = {
  url: page.url(),
  text: await bodyText(),
  testids: await counts(["training-plans-page", "training-plans-empty-add"]),
};
await screenshot("08_training_plans_unavailable");
await page.unroute("**/api/feature-modules/training-plans");

// FAILED MUTATION / RETRY STATE
await page.goto(`${baseUrl}/today`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="today-page"]', { timeout: 15000 });
const laterExpand = page.locator('[data-testid="group-later_today"] button[aria-label="Expand group"]');
if (await laterExpand.count()) await laterExpand.first().click();
await page.waitForSelector('[data-testid="task-row-task_cross_state_retry"]', { timeout: 15000 });
await page.route("**/api/tasks/task_cross_state_retry/complete", async (route) => {
  await route.fulfill({
    status: 403,
    contentType: "application/json",
    body: JSON.stringify({ detail: "Gate 6 synthetic non-retryable failure" }),
  });
});
await page.getByTestId("complete-btn-task_cross_state_retry").click();
await page.waitForFunction(() => {
  const q = JSON.parse(localStorage.getItem("equine_task_completion_queue_v1") || "[]");
  return q.some((item) => item.task_id === "task_cross_state_retry" && item.state === "failed");
}, null, { timeout: 15000 });
await page.waitForTimeout(500);
result.observations.failedTaskSync = {
  url: page.url(),
  text: await bodyText(),
  testids: await counts([
    "today-page",
    "task-row-task_cross_state_retry",
    "sync-dot-failed",
    "sync-header-badge",
    "sync-retry-now",
  ]),
  queue: await page.evaluate(() => JSON.parse(localStorage.getItem("equine_task_completion_queue_v1") || "[]")),
};
await screenshot("09_failed_sync_retry_now");

await page.unroute("**/api/tasks/task_cross_state_retry/complete");
if ((await page.getByTestId("sync-retry-now").count()) > 0) {
  await page.getByTestId("sync-retry-now").click();
  await page.waitForFunction(() => {
    const q = JSON.parse(localStorage.getItem("equine_task_completion_queue_v1") || "[]");
    return q.some((item) => item.task_id === "task_cross_state_retry" && item.state === "synced");
  }, null, { timeout: 15000 });
  result.observations.retryNowRecovery = {
    url: page.url(),
    attempted: true,
    testids: await counts(["sync-dot-failed", "sync-header-badge", "sync-retry-now"]),
    queue: await page.evaluate(() => JSON.parse(localStorage.getItem("equine_task_completion_queue_v1") || "[]")),
  };
} else {
  result.observations.retryNowRecovery = {
    url: page.url(),
    attempted: false,
    reason: "sync-retry-now control not rendered after stable failed queue state",
    testids: await counts(["sync-dot-failed", "sync-header-badge", "sync-retry-now"]),
    queue: await page.evaluate(() => JSON.parse(localStorage.getItem("equine_task_completion_queue_v1") || "[]")),
  };
}
await screenshot("10_retry_now_recovered_or_missing");

// API authority/state checks that do not depend on browser console noise.
result.apiChecks.ownerDeniedFinancialRead = await apiFetch(ownerToken, "GET", "/admin/billing/subscriptions");
result.apiChecks.adminToday = await apiFetch(adminToken, "GET", "/tasks/today");

await browser.close();

const jsonPath = path.join(outDir, "probe-result.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  ok: true,
  resultPath: jsonPath,
  screenshots: result.screenshots,
  observations: {
    protectedRedirect: result.observations.protectedRedirect?.testids,
    adminReadyShell: result.observations.adminReadyShell?.testids,
    ownerNavigationAuthority: result.observations.ownerNavigationAuthority?.testids,
    ownerDeniedLegalRoute: result.observations.ownerDeniedLegalRoute?.testids,
    setupReadinessError: result.observations.setupReadinessError?.testids,
    trainingPlansLoadingAndEmpty: result.observations.trainingPlansLoadingAndEmpty,
    trainingPlansUnavailableText: /Training plans unavailable/.test(result.observations.trainingPlansUnavailable?.text || ""),
    failedTaskSync: {
      testids: result.observations.failedTaskSync?.testids,
      queueStates: result.observations.failedTaskSync?.queue?.map((item) => item.state),
    },
    retryNowRecovery: {
      testids: result.observations.retryNowRecovery?.testids,
      queueStates: result.observations.retryNowRecovery?.queue?.map((item) => item.state),
    },
  },
  apiChecks: Object.fromEntries(Object.entries(result.apiChecks).map(([k, v]) => [k, { status: v.status, ok: v.ok }])),
  consoleCount: result.console.length,
  pageErrorCount: result.pageErrors.length,
}, null, 2));
