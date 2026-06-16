/**
 * AdminLogin — Admin-7B dedicated entry route at /admin/portal/login.
 *
 * Uses the EXISTING `POST /api/auth/login` (no separate admin auth
 * backend, no admin password store, no MFA in this phase). After a
 * successful login we read the current user; if they have a valid
 * platform_role, they're redirected to /admin/portal/dashboard, else
 * AdminForbidden is rendered.
 *
 * Visual: graphite background, lilac accents, minimal — clearly a
 * platform surface, not the customer login.
 */
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ShieldCheck, AlertOctagon } from "lucide-react";
import { useAuth } from "../../context/AuthContext";
import { isPlatformAdmin } from "../../lib/permissions";
import AdminForbidden from "./AdminForbidden";

export default function AdminLogin() {
  const { login, user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [submitting, setSubmitting] = useState(false);

  // If already authenticated and platform_role valid → bounce to dashboard.
  useEffect(() => {
    if (!authLoading && user && isPlatformAdmin(user)) {
      navigate("/admin/portal/dashboard", { replace: true });
    }
  }, [authLoading, user, navigate]);

  // Authenticated but not platform → show forbidden right here so
  // they understand exactly why this entry point isn't open to them.
  if (!authLoading && user && !isPlatformAdmin(user)) {
    return <AdminForbidden user={user} />;
  }

  const submit = async (e) => {
    if (e?.preventDefault) e.preventDefault();
    setErr("");
    setSubmitting(true);
    try {
      const u = await login(email, password);
      // The AuthContext refresh happens inline; redirect resolves in
      // the useEffect above once `user` updates. But if the user we
      // just got back has no platform_role, render forbidden by
      // staying here — the useEffect will not fire navigate(...) and
      // the conditional above will catch it on next render.
      if (!isPlatformAdmin(u)) {
        // Force a state update so the forbidden branch renders.
        setSubmitting(false);
      }
    } catch (err2) {
      const d = err2?.response?.data?.detail;
      const msg =
        typeof d === "string"
          ? d
          : Array.isArray(d)
          ? d.map((x) => x?.msg).filter(Boolean).join(", ")
          : "Sign in failed";
      setErr(msg);
      setSubmitting(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-equinesync-graphite text-equinesync-frost flex items-center justify-center px-4"
      data-testid="admin-login-page"
    >
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div
            className="w-12 h-12 mx-auto rounded-full bg-equinesync-slate flex items-center justify-center"
            aria-hidden="true"
          >
            <ShieldCheck className="w-5 h-5 text-equinesync-lilac" strokeWidth={1.6} />
          </div>
          <div className="mt-5 text-[10px] tracking-[0.36em] uppercase text-equinesync-lilac">
            Equine·Sync
          </div>
          <h1 className="mt-2 font-display text-3xl tracking-tight font-light">
            Admin Portal
          </h1>
          <p className="mt-3 text-[13px] text-equinesync-frost/60 max-w-sm mx-auto">
            Platform administration access. Standard barn-admin accounts
            cannot sign in here — only users with a platform role.
          </p>
        </div>

        <form
          onSubmit={submit}
          data-testid="admin-login-form"
          className="rounded-2xl bg-equinesync-slate/40 backdrop-blur p-6 border border-white/5 space-y-4"
        >
          <div>
            <label
              htmlFor="admin-login-email"
              className="text-[11px] tracking-[0.22em] uppercase text-equinesync-frost/60"
            >
              Work email
            </label>
            <input
              id="admin-login-email"
              type="email"
              required
              autoFocus
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              data-testid="admin-login-email"
              className="mt-2 w-full rounded-lg bg-equinesync-graphite/60 border border-white/10 px-3.5 py-2.5 text-[14px] text-equinesync-frost placeholder-equinesync-frost/30 focus:outline-none focus:border-equinesync-lilac/40"
              placeholder="you@equinesync.app"
            />
          </div>
          <div>
            <label
              htmlFor="admin-login-password"
              className="text-[11px] tracking-[0.22em] uppercase text-equinesync-frost/60"
            >
              Password
            </label>
            <input
              id="admin-login-password"
              type="password"
              required
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              data-testid="admin-login-password"
              className="mt-2 w-full rounded-lg bg-equinesync-graphite/60 border border-white/10 px-3.5 py-2.5 text-[14px] text-equinesync-frost placeholder-equinesync-frost/30 focus:outline-none focus:border-equinesync-lilac/40"
              placeholder="••••••••"
            />
          </div>

          {err && (
            <div
              data-testid="admin-login-error"
              className="rounded-lg border border-white/10 bg-equinesync-graphite/60 px-3.5 py-2.5 text-[12.5px] text-equinesync-frost/85 inline-flex items-center gap-2"
            >
              <AlertOctagon className="w-3.5 h-3.5 text-equinesync-lilac" />
              {err}
            </div>
          )}

          <button
            type="submit"
            disabled={submitting}
            data-testid="admin-login-submit"
            className="w-full rounded-lg bg-equinesync-lilac text-equinesync-graphite font-medium px-4 py-2.5 text-[13px] tracking-wide hover:bg-equinesync-lilac/90 disabled:opacity-60"
          >
            {submitting ? "Signing in…" : "Sign in to Admin Portal"}
          </button>
        </form>

        <div className="mt-6 text-center text-[11.5px] tracking-wide text-equinesync-frost/45">
          Not a platform admin?{" "}
          <a
            href="/login"
            data-testid="admin-login-customer-link"
            className="text-equinesync-lilac hover:text-equinesync-frost"
          >
            Customer sign-in →
          </a>
        </div>
      </div>
    </div>
  );
}
