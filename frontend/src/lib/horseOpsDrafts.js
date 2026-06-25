const DRAFT_PREFIX = "equinesync:horseops:draft:v1";

const safePart = (value) => String(value || "anon").replace(/[^a-zA-Z0-9_.-]/g, "_");

export const buildHorseOpsDraftKey = ({ userId, horseId, form }) => (
  `${DRAFT_PREFIX}:${safePart(userId)}:${safePart(horseId)}:${safePart(form)}`
);

export const loadHorseOpsDraft = (key) => {
  if (!key || typeof window === "undefined" || !window.localStorage) return null;
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
};

export const saveHorseOpsDraft = (key, value) => {
  if (!key || typeof window === "undefined" || !window.localStorage) return;
  try {
    window.localStorage.setItem(key, JSON.stringify({ ...value, saved_at: new Date().toISOString() }));
  } catch {
    // Field drafts are a convenience only; storage failures must never block care work.
  }
};

export const clearHorseOpsDraft = (key) => {
  if (!key || typeof window === "undefined" || !window.localStorage) return;
  try {
    window.localStorage.removeItem(key);
  } catch {
    // Ignore cleanup failures for the same reason saves are best-effort.
  }
};

