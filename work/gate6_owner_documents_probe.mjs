import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3007";
const outDir = path.resolve("outputs/gate6_owner_documents_probe_2026-08-25");
fs.mkdirSync(outDir, { recursive: true });

const result = {
  timestamp: new Date().toISOString(),
  baseUrl,
  console: [],
  pageErrors: [],
  observations: {},
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

await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
await page.getByTestId("login-email").fill("owner@equinesync.com");
await page.getByTestId("login-password").fill("demo1234");
await page.getByTestId("login-submit").click();
await page.waitForLoadState("networkidle");
await page.waitForSelector('[data-testid="sidebar"]', { timeout: 15000 });

result.observations.afterLogin = {
  url: page.url(),
  titleText: await page.locator("body").innerText({ timeout: 5000 }),
  testids: await visibleTestIds([
    "sidebar",
    "owner-portal-page",
    "owner-documents-page",
    "health-documents-page",
    "forbidden-page",
  ]),
};
await screenshot("01_owner_after_login");

const navDocs = page.getByTestId("nav-documents");
result.observations.navDocuments = {
  count: await navDocs.count(),
  href: await navDocs.first().getAttribute("href").catch(() => null),
  text: await navDocs.first().innerText().catch(() => null),
};

if (await navDocs.count()) {
  await navDocs.first().click();
  await page.waitForLoadState("networkidle");
  result.observations.afterNavDocumentsClick = {
    url: page.url(),
    text: await page.locator("body").innerText({ timeout: 5000 }),
    testids: await visibleTestIds([
      "owner-portal-page",
      "owner-documents-page",
      "owner-documents-list",
      "owner-document-card-doc-owner-rendered",
      "owner-document-card-form-owner-rendered",
      "health-documents-page",
      "forbidden-page",
    ]),
  };
  await screenshot("02_after_owner_documents_nav_click");
}

await page.goto(`${baseUrl}/documents`, { waitUntil: "networkidle" });
result.observations.directDocumentsRoute = {
  url: page.url(),
  text: await page.locator("body").innerText({ timeout: 5000 }),
  testids: await visibleTestIds([
    "owner-portal-page",
    "health-documents-page",
    "forbidden-page",
    "health-documents-add",
    "health-documents-search",
  ]),
};
await screenshot("03_owner_direct_documents_route");

await page.goto(`${baseUrl}/owner-portal`, { waitUntil: "networkidle" });
result.observations.ownerPortalDocumentControls = {
  url: page.url(),
  hasDocumentLibraryText: await page.getByText(/document library|documents|waiver|coggins|insurance/i).count(),
  testids: await visibleTestIds([
    "owner-portal-page",
    "owner-timeline-card",
    "owner-arena-schedule-card",
  ]),
};
await screenshot("04_owner_portal");

await page.goto(`${baseUrl}/owner-documents`, { waitUntil: "networkidle" });
result.observations.directOwnerDocumentsRoute = {
  url: page.url(),
  text: await page.locator("body").innerText({ timeout: 5000 }),
  testids: await visibleTestIds([
    "owner-documents-page",
    "owner-documents-list",
    "owner-document-card-doc-owner-rendered",
    "owner-document-card-form-owner-rendered",
    "health-documents-page",
    "forbidden-page",
  ]),
};
await screenshot("05_owner_documents_route");

await browser.close();

const jsonPath = path.join(outDir, "probe-result.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  ok: true,
  resultPath: jsonPath,
  screenshots: result.screenshots,
  observations: {
    afterLoginUrl: result.observations.afterLogin?.url,
    navDocuments: result.observations.navDocuments,
    afterNavDocumentsClickUrl: result.observations.afterNavDocumentsClick?.url,
    directDocumentsRoute: {
      url: result.observations.directDocumentsRoute?.url,
      testids: result.observations.directDocumentsRoute?.testids,
    },
    directOwnerDocumentsRoute: {
      url: result.observations.directOwnerDocumentsRoute?.url,
      testids: result.observations.directOwnerDocumentsRoute?.testids,
    },
    ownerPortalDocumentControls: result.observations.ownerPortalDocumentControls,
    consoleCount: result.console.length,
    pageErrorCount: result.pageErrors.length,
  },
}, null, 2));
