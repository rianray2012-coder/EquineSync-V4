// Phase 15.C — Stripe Checkout return page
// ---------------------------------------------------------------------------
// Stripe redirects to /billing/success?session_id=... after a successful
// subscription checkout. The webhook (`checkout.session.completed`) is what
// actually wires the subscription into the DB; this page just gives the user a
// gracious landing while that propagates, polling `/api/subscriptions/me`.
import React, { useCallback, useEffect, useRef, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { CheckCircle2, ArrowRight, RefreshCw } from "lucide-react";

import { api } from "../lib/api";
import { Card, PageHeader, StatusPill } from "../components/Primitives";
import { BrandLoader } from "../components/BrandLoader";
import { STATUS_LABEL, STATUS_TONE } from "../lib/subscriptionBilling";

export default function SubscriptionSuccess() {
  const [params] = useSearchParams();
  const sessionId = params.get("session_id");
  const [sub, setSub] = useState(null);
  const [loading, setLoading] = useState(true);
  const [polls, setPolls] = useState(0);
  const stopped = useRef(false);

  // Poll /subscriptions/me up to 6 times (12s) — webhooks usually land
  // within 1-3s in test mode, but we give it room. We DON'T require a
  // subscription to be present; we just give it a chance.
  const fetchOnce = useCallback(async () => {
    try {
      const { data } = await api.get("/subscriptions/me");
      if (stopped.current) return;
      if (data?.subscription) setSub(data.subscription);
    } catch {
      /* keep polling */
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      await fetchOnce();
      setLoading(false);
    })();
    const id = setInterval(async () => {
      if (cancelled) return;
      setPolls((n) => {
        if (n >= 5) {
          clearInterval(id);
          return n;
        }
        return n + 1;
      });
      await fetchOnce();
    }, 2000);
    return () => {
      cancelled = true;
      stopped.current = true;
      clearInterval(id);
    };
  }, [fetchOnce]);

  if (loading) {
    return (
      <div data-testid="subscription-success-page" className="pb-20 lg:pb-8">
        <BrandLoader label="Finalizing your subscription…" />
      </div>
    );
  }

  const planTier = sub?.plan_tier_code;
  const status = sub?.status;

  return (
    <div data-testid="subscription-success-page" className="pb-20 lg:pb-8 max-w-3xl">
      <PageHeader
        eyebrow="All set"
        title="Welcome to your subscription"
        subtitle="Stripe accepted your payment. Your facility tools are unlocking right now."
      />

      <Card hover={false} className="border-equine-saddle/40" data-testid="success-summary-card">
        <div className="flex items-start gap-4 flex-wrap">
          <div className="rounded-full bg-equine-saddle/15 p-3 border border-equine-saddle/40">
            <CheckCircle2 className="w-5 h-5 text-equine-saddleDeep" />
          </div>
          <div className="flex-1 min-w-[220px]">
            <div className="font-display text-2xl text-equine-ink mb-1">
              {planTier ? (
                <>You&apos;re on <span className="capitalize">{planTier}</span></>
              ) : (
                <>You&apos;re subscribed</>
              )}
            </div>
            <p className="text-[13.5px] text-equine-inkMuted leading-relaxed">
              {sub
                ? "Your plan is active. Manage payment methods, cycle, and cancellation any time from the Subscription page."
                : "We\u2019re still confirming the final details with Stripe \u2014 this usually takes a few seconds. You can keep using the app meanwhile."}
            </p>
            {status && (
              <div className="mt-3" data-testid="success-status-pill">
                <StatusPill tone={STATUS_TONE[status] || "neutral"} dot>
                  {STATUS_LABEL[status] || status}
                </StatusPill>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/billing/subscription"
            data-testid="success-go-billing"
            className="inline-flex items-center gap-1.5 text-[12.5px] tracking-wide font-medium px-4 py-2 rounded-full bg-equine-navy text-white hover:bg-equine-navyLift transition-colors"
          >
            Manage subscription <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/dashboard"
            data-testid="success-go-dashboard"
            className="inline-flex items-center gap-1.5 text-[12.5px] tracking-wide px-4 py-2 rounded-full border border-equine-graphite/40 text-equine-ink hover:border-equine-saddleDeep/40 hover:text-equine-saddleDeep transition-colors"
          >
            Back to dashboard
          </Link>
        </div>

        {!sub && polls < 5 && (
          <div className="mt-5 flex items-center gap-2 text-[11.5px] text-equine-inkSoft" data-testid="success-polling">
            <RefreshCw className="w-3 h-3 animate-spin" /> Waiting for Stripe webhook confirmation…
          </div>
        )}
        {sessionId && (
          <div className="mt-3 text-[10.5px] text-equine-inkSoft font-mono" data-testid="success-session-ref">
            Session ref: {sessionId.slice(0, 18)}…
          </div>
        )}
      </Card>
    </div>
  );
}
