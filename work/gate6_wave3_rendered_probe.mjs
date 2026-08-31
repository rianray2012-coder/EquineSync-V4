import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3008";
const apiUrl = process.env.API_URL || "http://127.0.0.1:8002/api";
const outDir = path.resolve("outputs/gate6_wave3_rendered_probe_2026-08-25");
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

async function login(email) {
  await page.goto(`${baseUrl}/login`, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    localStorage.removeItem("equine_token");
    localStorage.removeItem("equine_user");
    sessionStorage.clear();
  });
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
  try {
    json = text ? JSON.parse(text) : null;
  } catch {
    json = null;
  }
  return { status: r.status, ok: r.ok, text, json };
}

async function bodyText() {
  return page.locator("body").innerText({ timeout: 5000 });
}

const ownerToken = await login("owner@equinesync.com");
result.observations.ownerAfterLogin = {
  url: page.url(),
  testids: await visibleTestIds(["sidebar", "owner-portal-page", "owner-documents-page", "forbidden-page"]),
};
await screenshot("01_owner_after_login");

await page.goto(`${baseUrl}/owner-documents`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="owner-documents-page"]', { timeout: 15000 });
result.observations.ownerDocuments = {
  url: page.url(),
  text: await bodyText(),
  testids: await visibleTestIds([
    "owner-documents-page",
    "owner-documents-list",
    "owner-document-card-doc-wave3-owner",
    "owner-document-card-form-wave3-owner",
    "owner-document-card-doc-wave3-other",
    "owner-document-card-form-wave3-other",
    "forbidden-page",
  ]),
};
await screenshot("02_owner_documents");

result.apiChecks.ownerDocuments = await apiFetch(ownerToken, "GET", "/owner-portal/documents");
result.observations.ownerDocumentApiSafety = {
  ids: (result.apiChecks.ownerDocuments.json?.documents || []).map((doc) => doc.id),
  liveSigningEnabled: result.apiChecks.ownerDocuments.json?.live_signing_enabled,
  providerLiveActivation: result.apiChecks.ownerDocuments.json?.provider_live_activation,
  leakedPrivateKeys: (result.apiChecks.ownerDocuments.json?.documents || []).flatMap((doc) =>
    [
      "provider_envelope_id",
      "provider_signature_id",
      "provider_certificate_ref",
      "signed_document_url",
      "staff_notes",
      "required_signer_user_ids",
    ].filter((key) => Object.prototype.hasOwnProperty.call(doc, key)),
  ),
};

await page.goto(`${baseUrl}/forms-signatures`, { waitUntil: "networkidle" });
result.observations.ownerFormsDirect = {
  url: page.url(),
  text: await bodyText(),
  testids: await visibleTestIds(["forms-signatures-page", "forbidden-page"]),
};
await screenshot("03_owner_forms_direct_forbidden");

const adminToken = await login("admin@equinesync.com");
await page.goto(`${baseUrl}/forms-signatures`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="forms-signatures-page"]', { timeout: 15000 });
result.observations.adminFormsSignatures = {
  url: page.url(),
  text: await bodyText(),
  testids: await visibleTestIds([
    "forms-signatures-page",
    "document-workflow-foundation",
    "document-template-add",
    "document-request-add",
    "forms-add",
    "forms-list",
    "form-row-form-wave3-provider-ready",
  ]),
  liveSendButtonCount: await page.locator("button").filter({ hasText: /send envelope|send for signature|send legal/i }).count(),
  readinessTextCount: await page.getByText(/credentials needed|credentials ready|no signing link is generated|provider readiness|Envelope sending appears only/i).count(),
};
await screenshot("04_admin_forms_signatures");
result.apiChecks.signatureProviders = await apiFetch(adminToken, "GET", "/document-signatures/providers");

const providerToken = await login("farrier@equinesync.com");
await page.goto(`${baseUrl}/dashboard/service-provider`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="dashboard-service-provider"]', { timeout: 15000 });
result.observations.providerDashboard = {
  url: page.url(),
  text: await bodyText(),
  testids: await visibleTestIds([
    "dashboard-service-provider",
    "provider-stat-grants",
    "provider-stat-horses",
    "provider-stat-farrier",
    "provider-shared-horses",
    "provider-farrier-records",
    "provider-recent-visit-notes",
  ]),
};
await screenshot("05_provider_dashboard");
result.apiChecks.providerOperatingCenter = await apiFetch(providerToken, "GET", "/service-provider/operating-center");
result.apiChecks.providerVisitDenied = await apiFetch(providerToken, "POST", "/service-provider/visit-notes", {
  horse_id: "wave3_unrelated_horse",
  category: "farrier",
  title: "Should be denied",
});

await login("admin@equinesync.com");
await page.goto(`${baseUrl}/ai-automation`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="ai-draft-review-page"], [data-testid="ai-automation-page"], [data-testid="forbidden-page"], [data-testid="setup-readiness-error"]', { timeout: 15000 })
  .catch(() => null);
result.observations.aiDraftReview = {
  url: page.url(),
  text: await bodyText(),
  testids: await visibleTestIds([
    "ai-automation-page",
    "ai-automation-generate",
    "ai-automation-add",
    "ai-draft-review-page",
    "ai-draft-create-card",
    "ai-draft-source-type",
    "ai-draft-source-text",
    "ai-draft-create",
  ]),
};
await screenshot("06_ai_draft_review");
result.apiChecks.aiDraftInline = await apiFetch(adminToken, "POST", "/ai/draft-jobs", {
  source_type: "voice_transcript",
  source_text: "Draft only Wave 3 rendered route proof. Do not save official records.",
  requested_output: "draft_records",
});

const aiJobId = result.apiChecks.aiDraftInline.json?.job?.id;
if (aiJobId) {
  result.apiChecks.aiDraftReview = await apiFetch(adminToken, "POST", `/ai/draft-jobs/${aiJobId}/review`, {
    action: "approved_no_save",
    note: "Rendered Wave 3 proof: approved no save.",
  });
}

await browser.close();

const jsonPath = path.join(outDir, "probe-result.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  ok: true,
  resultPath: jsonPath,
  screenshots: result.screenshots,
  observations: {
    ownerDocuments: result.observations.ownerDocuments?.testids,
    ownerDocumentApiSafety: result.observations.ownerDocumentApiSafety,
    ownerFormsDirect: result.observations.ownerFormsDirect?.testids,
    adminFormsSignatures: {
      testids: result.observations.adminFormsSignatures?.testids,
      liveSendButtonCount: result.observations.adminFormsSignatures?.liveSendButtonCount,
      readinessTextCount: result.observations.adminFormsSignatures?.readinessTextCount,
    },
    providerDashboard: result.observations.providerDashboard?.testids,
    aiDraftReview: result.observations.aiDraftReview?.testids,
  },
  apiChecks: Object.fromEntries(
    Object.entries(result.apiChecks).map(([key, value]) => [key, { status: value.status, ok: value.ok }]),
  ),
  consoleCount: result.console.length,
  pageErrorCount: result.pageErrors.length,
}, null, 2));
