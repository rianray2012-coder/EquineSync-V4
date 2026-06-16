/**
 * AdminSettings — Admin-7B read-only configuration inventory.
 *
 * Pure introspection from /admin/portal/settings. Returns booleans
 * and safe labels only — no raw env values, no secrets, no URLs
 * with credentials. Server-side gated to super_admin + platform_admin.
 */
import React, { useEffect, useState } from "react";
import {
  Settings as SettingsIcon, RefreshCcw, AlertOctagon,
  ShieldCheck, Mail, CreditCard, Globe, Clock,
} from "lucide-react";
import { api } from "../../lib/api";

const Pill = ({ truthy, trueLabel = "On", falseLabel = "Off", testid }) => (
  <span
    data-testid={testid}
    className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[11px] tracking-[0.18em] uppercase ${
      truthy
        ? "bg-equinesync-lilac/15 text-equinesync-slate"
        : "bg-equinesync-frost text-equinesync-graphite/60"
    }`}
  >
    {truthy ? trueLabel : falseLabel}
  </span>
);

const Row = ({ label, children, testid }) => (
  <div
    data-testid={testid}
    className="flex items-center justify-between py-2 border-b border-equinesync-graphite/5 last:border-0 gap-3"
  >
    <span className="text-[13px] text-equinesync-graphite/70">{label}</span>
    <span className="text-[13px] text-equinesync-graphite tabular-nums">{children}</span>
  </div>
);

const Card = ({ title, Icon, children, testid }) => (
  <div
    data-testid={testid}
    className="rounded-2xl border border-equinesync-graphite/10 bg-white p-6"
  >
    <div className="flex items-center gap-2">
      <Icon className="w-4 h-4 text-equinesync-slate" />
      <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
        {title}
      </div>
    </div>
    <div className="mt-4">{children}</div>
  </div>
);

export default function AdminSettings() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    api.get(`/admin/portal/settings`)
      .then((r) => {
        if (cancelled) return;
        setData(r.data);
        setErr(null);
        setLoading(false);
      })
      .catch((e) => {
        if (cancelled) return;
        setErr(e?.response?.data?.detail || "Failed to load settings.");
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [reloadKey]);

  return (
    <div className="max-w-5xl mx-auto" data-testid="admin-settings-page">
      <div className="mb-6 flex items-end justify-between flex-wrap gap-3">
        <div>
          <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
            Admin Portal · Settings
          </div>
          <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">
            Settings
          </h1>
          <p className="mt-2 text-[13.5px] text-equinesync-graphite/65 max-w-2xl">
            Read-only configuration inventory. No secrets, raw env values,
            URLs with credentials, or webhook secrets are exposed.
          </p>
        </div>
        <button
          type="button"
          onClick={() => setReloadKey((k) => k + 1)}
          data-testid="admin-settings-refresh"
          className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-equinesync-graphite/15 text-[12.5px] text-equinesync-graphite hover:bg-equinesync-frost"
        >
          <RefreshCcw className="w-3.5 h-3.5" /> Refresh
        </button>
      </div>

      {err && (
        <div
          data-testid="admin-settings-error"
          className="mb-4 rounded-lg border border-equinesync-graphite/15 bg-white p-4 text-[13px] text-equinesync-graphite/80"
        >
          <span className="inline-flex items-center gap-2">
            <AlertOctagon className="w-3.5 h-3.5" /> {err}
          </span>
        </div>
      )}

      {loading ? (
        <div
          data-testid="admin-settings-loading"
          className="rounded-2xl border border-equinesync-graphite/10 bg-white p-10 text-center text-[13px] text-equinesync-graphite/55"
        >
          Loading configuration…
        </div>
      ) : data && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          <Card title="Environment" Icon={SettingsIcon} testid="settings-env-card">
            <Row label="Environment" testid="settings-env-row">
              {data.environment}
            </Row>
            <Row label="Production">
              <Pill truthy={data.is_production} trueLabel="Yes" falseLabel="No" testid="settings-is-prod" />
            </Row>
            <Row label="Public app URL">
              <Pill
                truthy={data.public_app_url_configured}
                trueLabel="Configured"
                falseLabel="Not set"
                testid="settings-public-url"
              />
            </Row>
            <Row label="Health probe">
              <code className="text-[12px]">{data.health_probe}</code>
            </Row>
          </Card>

          <Card title="Feature flags" Icon={ShieldCheck} testid="settings-flags-card">
            <Row label="Email verification enforced">
              <Pill truthy={data.feature_flags.enforce_email_verification} testid="flag-email-verify" />
            </Row>
            <Row label="Login lockout enabled">
              <Pill truthy={data.feature_flags.login_lockout_enabled} testid="flag-lockout" />
            </Row>
            <Row label="Rate limiting enabled">
              <Pill truthy={data.feature_flags.rate_limit_enabled} testid="flag-rate-limit" />
            </Row>
            <Row label="Public seed route">
              <Pill truthy={data.feature_flags.allow_seed_route} trueLabel="Enabled" falseLabel="Blocked" testid="flag-seed-route" />
            </Row>
            <Row label="Auto-seed on startup">
              <Pill truthy={data.feature_flags.auto_seed_enabled} testid="flag-auto-seed" />
            </Row>
          </Card>

          <Card title="Billing" Icon={CreditCard} testid="settings-billing-card">
            <Row label="Stripe">
              <Pill
                truthy={data.billing.stripe_configured}
                trueLabel="Configured"
                falseLabel="Not configured"
                testid="settings-stripe-configured"
              />
            </Row>
            <Row label="Mode" testid="settings-billing-mode">
              {data.billing.billing_mode}
            </Row>
          </Card>

          <Card title="Email" Icon={Mail} testid="settings-email-card">
            <Row label="Resend">
              <Pill
                truthy={data.email.resend_configured}
                trueLabel="Configured"
                falseLabel="Not configured"
                testid="settings-resend-configured"
              />
            </Row>
          </Card>

          <Card title="Scheduler" Icon={Clock} testid="settings-scheduler-card">
            <Row label="Background jobs">
              <Pill
                truthy={data.scheduler.enabled}
                trueLabel="Enabled"
                falseLabel="Disabled"
                testid="settings-scheduler-enabled"
              />
            </Row>
          </Card>

          <Card title="CORS" Icon={Globe} testid="settings-cors-card">
            <Row label="Policy" testid="settings-cors-policy">{data.cors.policy}</Row>
            <Row label="Allowed origins">
              {data.cors.policy === "wildcard"
                ? <span className="text-equinesync-graphite/60">wildcard</span>
                : <span className="tabular-nums">{data.cors.count}</span>}
            </Row>
          </Card>

          <Card title="Auth policy" Icon={ShieldCheck} testid="settings-auth-card">
            <Row label="Max login attempts">{data.auth_policy.login_max_attempts}</Row>
            <Row label="Lockout (minutes)">{data.auth_policy.login_lockout_minutes}</Row>
            <Row label="Attempt window (minutes)">{data.auth_policy.login_attempt_window_minutes}</Row>
            <Row label="Email verify TTL (hours)">{data.auth_policy.email_verify_ttl_hours}</Row>
            <Row label="Password reset TTL (hours)">{data.auth_policy.password_reset_ttl_hours}</Row>
          </Card>
        </div>
      )}

      {data?._generated_at && (
        <div className="mt-6 text-[11.5px] text-equinesync-graphite/45 text-right">
          Snapshot generated {new Date(data._generated_at).toLocaleString()}
        </div>
      )}
    </div>
  );
}
