import fs from "node:fs";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = process.env.FRONTEND_URL || "http://127.0.0.1:3007";
const apiUrl = process.env.API_URL || "http://127.0.0.1:8001/api";
const outDir = path.resolve("outputs/gate6_wave2_ui_probe_2026-08-25");
fs.mkdirSync(outDir, { recursive: true });

const evidenceFile = path.join(outDir, "wave2-evidence.txt");
fs.writeFileSync(evidenceFile, "Gate 6 Wave 2 rendered task evidence fixture\n");

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

async function apiFetch(token, method, route, body) {
  return page.evaluate(
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
}

async function waitForApi(token, route, predicate, timeoutMs = 10000) {
  const start = Date.now();
  let latest = null;
  while (Date.now() - start < timeoutMs) {
    latest = await apiFetch(token, "GET", route);
    if (predicate(latest)) return latest;
    await page.waitForTimeout(400);
  }
  return latest;
}

await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
await page.getByTestId("login-email").fill("admin@equinesync.com");
await page.getByTestId("login-password").fill("demo1234");
await page.getByTestId("login-submit").click();
await page.waitForLoadState("networkidle");
await page.waitForSelector('[data-testid="sidebar"]', { timeout: 15000 });
const token = await page.evaluate(() => localStorage.getItem("equine_token"));

result.observations.afterLogin = {
  url: page.url(),
  testids: await visibleTestIds(["sidebar", "today-page", "lessons-page", "training-page"]),
};
await screenshot("01_after_login");

await page.goto(`${baseUrl}/today`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="today-page"]', { timeout: 15000 });
const laterExpand = page.locator('[data-testid="group-later_today"] button[aria-label="Expand group"]');
if (await laterExpand.count()) {
  await laterExpand.first().click();
}
await page.waitForSelector('[data-testid="task-row-task_wave2_ui"]', { timeout: 5000 });
result.observations.todayInitial = {
  url: page.url(),
  text: await page.locator("body").innerText({ timeout: 5000 }),
  testids: await visibleTestIds([
    "today-page",
    "task-row-task_wave2_ui",
    "task-evidence-label-task_wave2_ui",
    "task-evidence-input-task_wave2_ui",
    "task-evidence-summary-task_wave2_ui",
    "complete-btn-task_wave2_ui",
  ]),
};
await screenshot("02_today_task_evidence_initial");

await page.getByTestId("task-evidence-input-task_wave2_ui").setInputFiles(evidenceFile);
await page.waitForSelector('[data-testid="task-evidence-summary-task_wave2_ui"]', { timeout: 5000 });
result.observations.todayEvidenceSelected = {
  testids: await visibleTestIds(["task-evidence-summary-task_wave2_ui"]),
  text: await page.getByTestId("task-evidence-summary-task_wave2_ui").innerText(),
};
await screenshot("03_today_task_evidence_selected");

await page.getByTestId("complete-btn-task_wave2_ui").click();
result.apiChecks.taskCompletion = await waitForApi(
  token,
  "/tasks?start=2026-08-25T00:00:00Z&end=2026-08-26T00:00:00Z",
  (r) => r.ok && (r.json?.items || []).some((task) => task.id === "task_wave2_ui" && task.status === "completed"),
);
await screenshot("04_today_task_completed");

await page.goto(`${baseUrl}/handoff-reports`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="handoff-reports-page"]', { timeout: 15000 });
result.observations.handoffInitial = {
  url: page.url(),
  testids: await visibleTestIds([
    "handoff-reports-page",
    "handoff-reports-add",
    "handoff-report-card-handoff_wave2_ui",
    "handoff-link-summary",
  ]),
  text: await page.locator("body").innerText({ timeout: 5000 }),
};
await screenshot("05_handoff_summary");

await page.getByTestId("handoff-reports-add").click();
await page.waitForSelector('[data-testid="handoff-reports-add-sheet"]', { timeout: 5000 });
result.observations.handoffAddControls = {
  testids: await visibleTestIds([
    "handoff-reports-add-sheet",
    "handoff-reports-add-linked_task_ids",
    "handoff-reports-add-evidence_completion_ids",
    "handoff-reports-add-signoff_user_ids",
  ]),
};
await screenshot("06_handoff_add_link_controls");
await page.getByTestId("handoff-reports-add-cancel").click();

await page.goto(`${baseUrl}/lessons`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="lessons-page"]', { timeout: 15000 });
result.observations.lessonsInitial = {
  url: page.url(),
  testids: await visibleTestIds([
    "lesson-lesson_wave2_sub",
    "lesson-substitute-lesson_wave2_sub",
    "lesson-cancel-lesson_wave2_cancel",
  ]),
};
await screenshot("07_lessons_controls");

await page.getByTestId("lesson-substitute-lesson_wave2_sub").click();
await page.waitForSelector('[data-testid="lesson-substitute-sheet"]', { timeout: 5000 });
result.observations.lessonSubstituteControls = {
  testids: await visibleTestIds([
    "lesson-substitute-sheet",
    "lesson-substitute-trainer-id",
    "lesson-substitute-rider-id",
    "lesson-substitute-horse-id",
    "lesson-substitute-reason",
    "lesson-substitute-submit",
  ]),
};
await page.getByTestId("lesson-substitute-trainer-id").selectOption("trainer_sub");
await page.getByTestId("lesson-substitute-rider-id").selectOption("rider_sub");
await page.getByTestId("lesson-substitute-horse-id").selectOption("horse_sub");
await page.getByTestId("lesson-substitute-reason").fill("Rendered substitution proof.");
await screenshot("08_lesson_substitute_sheet");
await page.getByTestId("lesson-substitute-submit").click();
result.apiChecks.lessonSubstitution = await waitForApi(
  token,
  "/lessons",
  (r) => r.ok && (r.json || []).some((lesson) =>
    lesson.id === "lesson_wave2_sub"
    && lesson.substitution_state === "substituted"
    && lesson.substitute_trainer_id === "trainer_sub"
    && lesson.substitute_rider_id === "rider_sub"
    && lesson.substitute_horse_id === "horse_sub"
  ),
);

await page.getByTestId("lesson-cancel-lesson_wave2_cancel").click();
await page.waitForSelector('[data-testid="lesson-cancel-sheet"]', { timeout: 5000 });
result.observations.lessonCancelControls = {
  testids: await visibleTestIds([
    "lesson-cancel-sheet",
    "lesson-cancel-reason",
    "lesson-cancel-submit",
  ]),
};
await page.getByTestId("lesson-cancel-reason").fill("Rendered cancellation proof.");
await screenshot("09_lesson_cancel_sheet");
await page.getByTestId("lesson-cancel-submit").click();
result.apiChecks.lessonCancellation = await waitForApi(
  token,
  "/lessons",
  (r) => r.ok && (r.json || []).some((lesson) =>
    lesson.id === "lesson_wave2_cancel" && lesson.status === "cancelled"
  ),
);

await page.goto(`${baseUrl}/training`, { waitUntil: "networkidle" });
await page.waitForSelector('[data-testid="training-page"]', { timeout: 15000 });
result.observations.trainingInitial = {
  url: page.url(),
  testids: await visibleTestIds([
    "training-training_wave2_sub",
    "training-substitute-training_wave2_sub",
    "training-cancel-training_wave2_cancel",
  ]),
};
await screenshot("10_training_controls");

await page.getByTestId("training-substitute-training_wave2_sub").click();
await page.waitForSelector('[data-testid="training-substitute-sheet"]', { timeout: 5000 });
result.observations.trainingSubstituteControls = {
  testids: await visibleTestIds([
    "training-substitute-sheet",
    "training-substitute-trainer-id",
    "training-substitute-horse-id",
    "training-substitute-reason",
    "training-substitute-submit",
  ]),
};
await page.getByTestId("training-substitute-trainer-id").selectOption("trainer_sub");
await page.getByTestId("training-substitute-horse-id").selectOption("horse_sub");
await page.getByTestId("training-substitute-reason").fill("Rendered training substitution proof.");
await screenshot("11_training_substitute_sheet");
await page.getByTestId("training-substitute-submit").click();
result.apiChecks.trainingSubstitution = await waitForApi(
  token,
  "/training",
  (r) => r.ok && (r.json || []).some((session) =>
    session.id === "training_wave2_sub"
    && session.substitution_state === "substituted"
    && session.substitute_trainer_id === "trainer_sub"
    && session.substitute_horse_id === "horse_sub"
  ),
);

await page.getByTestId("training-cancel-training_wave2_cancel").click();
await page.waitForSelector('[data-testid="training-cancel-sheet"]', { timeout: 5000 });
result.observations.trainingCancelControls = {
  testids: await visibleTestIds([
    "training-cancel-sheet",
    "training-cancel-reason",
    "training-cancel-submit",
  ]),
};
await page.getByTestId("training-cancel-reason").fill("Rendered training cancellation proof.");
await screenshot("12_training_cancel_sheet");
await page.getByTestId("training-cancel-submit").click();
result.apiChecks.trainingCancellation = await waitForApi(
  token,
  "/training",
  (r) => r.ok && (r.json || []).some((session) =>
    session.id === "training_wave2_cancel" && session.status === "cancelled"
  ),
);

await browser.close();

const jsonPath = path.join(outDir, "probe-result.json");
fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  ok: true,
  resultPath: jsonPath,
  screenshots: result.screenshots,
  observations: {
    todayInitial: result.observations.todayInitial?.testids,
    todayEvidenceSelected: result.observations.todayEvidenceSelected,
    handoffInitial: result.observations.handoffInitial?.testids,
    handoffAddControls: result.observations.handoffAddControls?.testids,
    lessonSubstituteControls: result.observations.lessonSubstituteControls?.testids,
    lessonCancelControls: result.observations.lessonCancelControls?.testids,
    trainingSubstituteControls: result.observations.trainingSubstituteControls?.testids,
    trainingCancelControls: result.observations.trainingCancelControls?.testids,
  },
  apiChecks: Object.fromEntries(
    Object.entries(result.apiChecks).map(([key, value]) => [key, { status: value?.status, ok: value?.ok }]),
  ),
  consoleCount: result.console.length,
  pageErrorCount: result.pageErrors.length,
}, null, 2));
