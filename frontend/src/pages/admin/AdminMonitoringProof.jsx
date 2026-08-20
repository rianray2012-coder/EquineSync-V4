import React, { useMemo, useState } from "react";
import { captureWebMonitoringProof, sentryEnabled, sentryProofEnabled } from "../../monitoring";

const proofFromLocation = () => {
  try {
    return new URLSearchParams(window.location.search).get("proof") || "";
  } catch {
    return "";
  }
};

export default function AdminMonitoringProof() {
  const [result, setResult] = useState(null);
  const proofHash = useMemo(() => proofFromLocation(), []);
  const canSend = sentryEnabled && sentryProofEnabled && proofHash.length > 0;

  const sendProof = () => {
    const next = captureWebMonitoringProof({ proofHash, triggeredBy: "platform-admin-proof-route" });
    setResult(next);
  };

  return (
    <div className="max-w-3xl mx-auto" data-testid="admin-monitoring-proof-page">
      <div className="mb-6">
        <div className="text-[11px] tracking-[0.28em] uppercase text-equinesync-graphite/55 font-medium">
          Admin Portal · Monitoring
        </div>
        <h1 className="font-display text-3xl font-light text-equinesync-graphite mt-2">
          Monitoring Proof
        </h1>
      </div>

      <section className="bg-white rounded-xl border border-equinesync-graphite/10 p-5 space-y-4">
        <dl className="grid gap-3 text-[13px] text-equinesync-graphite/75">
          <div className="flex items-center justify-between gap-4">
            <dt>Sentry SDK</dt>
            <dd data-testid="monitoring-proof-sentry-enabled">{sentryEnabled ? "enabled" : "disabled"}</dd>
          </div>
          <div className="flex items-center justify-between gap-4">
            <dt>Proof gate</dt>
            <dd data-testid="monitoring-proof-gate">{sentryProofEnabled ? "enabled" : "disabled"}</dd>
          </div>
          <div className="flex items-center justify-between gap-4">
            <dt>Proof hash</dt>
            <dd className="font-mono text-[12px]" data-testid="monitoring-proof-hash">
              {proofHash || "missing"}
            </dd>
          </div>
        </dl>

        <button
          type="button"
          disabled={!canSend}
          onClick={sendProof}
          data-testid="monitoring-proof-send"
          className="inline-flex items-center px-4 py-2 rounded-lg bg-equinesync-graphite text-white text-[13px] disabled:opacity-45 disabled:cursor-not-allowed"
        >
          Send Proof Event
        </button>

        {result && (
          <div
            className="rounded-lg border border-equinesync-graphite/10 bg-equinesync-frost p-3 text-[13px] text-equinesync-graphite/75"
            data-testid="monitoring-proof-result"
          >
            {result.sent ? `sent proof_hash=${result.proofHash}` : `not sent: ${result.reason}`}
          </div>
        )}
      </section>
    </div>
  );
}
