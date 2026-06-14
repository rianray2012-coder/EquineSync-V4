// Phase 15.F — Subscription usage hook.
// ---------------------------------------------------------------------------
// Wraps GET /api/billing/usage and gracefully no-ops for users who lack the
// `barn:manage` capability — that's the source of truth on the backend, so we
// (a) avoid the API call entirely when the frontend can already tell the user
// is ineligible, and (b) silently swallow any 403 as a defense-in-depth fallback.
//
// The hook is intentionally tiny: one cached fetch per mount, plus a manual
// `refresh()` for callers that just created a resource and want the meter to
// update immediately (decision #5a).
import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "./api";
import { canManageBilling } from "./permissions";
import { useAuth } from "../context/AuthContext";

export function useSubscriptionUsage() {
  const { user } = useAuth();
  const eligible = canManageBilling(user);
  const [usage, setUsage] = useState(null);
  const [loading, setLoading] = useState(eligible);
  const [error, setError] = useState(null);
  const mounted = useRef(true);

  // Use a per-mount effect (NOT empty deps) so StrictMode's simulated
  // unmount/remount cycle doesn't leave `mounted.current = false`
  // permanently — that would silently skip every setState below.
  useEffect(() => {
    mounted.current = true;
    return () => { mounted.current = false; };
  });

  const fetchOnce = useCallback(async () => {
    if (!eligible) {
      setUsage(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    try {
      const { data } = await api.get("/billing/usage");
      if (!mounted.current) return;
      setUsage(data);
      setError(null);
    } catch (e) {
      if (!mounted.current) return;
      // 403 is treated identically to "not eligible" — no nag, no render.
      // Any other failure is surfaced to consumers via `error` so they can
      // choose to log it; default consumers just ignore and render nothing.
      if (e?.response?.status === 403) {
        setUsage(null);
        setError(null);
      } else {
        setError(e?.response?.data?.detail || "usage_fetch_failed");
      }
    } finally {
      if (mounted.current) setLoading(false);
    }
  }, [eligible]);

  useEffect(() => { fetchOnce(); }, [fetchOnce]);

  return { eligible, loading, error, usage, refresh: fetchOnce };
}
