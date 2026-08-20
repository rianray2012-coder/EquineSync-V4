import React, { useMemo, useState } from "react";
import { captureWebMonitoringProof, sentryEnabled, sentryProofEnabled } from "../monitoring";

const expectedProofHash = process.env.REACT_APP_SENTRY_PROOF_HASH || "";

const queryProofHash = () => {
  try {
    return new URLSearchParams(window.location.search).get("proof") || "";
  } catch {
    return "";
  }
};

export default function MonitoringProof() {
  const [result, setResult] = useState(null);
  const proofHash = useMemo(() => queryProofHash(), []);
  const proofMatches = proofHash && expectedProofHash && proofHash === expectedProofHash;
  const canSend = sentryEnabled && sentryProofEnabled && proofMatches;

  const sendProof = () => {
    setResult(captureWebMonitoringProof({ proofHash, triggeredBy: "temporary-proof-route" }));
  };

  return (
    <main className="min-h-screen bg-equinesync-frost text-equinesync-graphite flex items-center justify-center p-6">
      <section className="w-full max-w-xl bg-white border border-equinesync-graphite/10 rounded-xl p-6 space-y-4">
        <div>
          <p className="text-[11px] uppercase tracking-[0.28em] text-equinesync-graphite/55">
            EquineSync Monitoring
          </p>
          <h1 className="font-display text-3xl font-light mt-2">Proof Event</h1>
        </div>
        <dl className="grid gap-2 text-[13px]">
          <div className="flex justify-between gap-4">
            <dt>Sentry SDK</dt>
            <dd data-testid="monitoring-proof-sentry-enabled">{sentryEnabled ? "enabled" : "disabled"}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt>Proof gate</dt>
            <dd data-testid="monitoring-proof-gate">{sentryProofEnabled ? "enabled" : "disabled"}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt>Proof match</dt>
            <dd data-testid="monitoring-proof-match">{proofMatches ? "matched" : "not matched"}</dd>
          </div>
        </dl>
        <button
          type="button"
          disabled={!canSend}
          onClick={sendProof}
          data-testid="monitoring-proof-send"
          className="px-4 py-2 rounded-lg bg-equinesync-graphite text-white text-[13px] disabled:opacity-45 disabled:cursor-not-allowed"
        >
          Send Proof Event
        </button>
        {result && (
          <div
            className="rounded-lg border border-equinesync-graphite/10 bg-equinesync-frost p-3 text-[13px]"
            data-testid="monitoring-proof-result"
          >
            {result.sent ? `sent proof_hash=${result.proofHash}` : `not sent: ${result.reason}`}
          </div>
        )}
      </section>
    </main>
  );
}
