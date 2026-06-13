import React, { useEffect, useRef, useState } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../lib/api";
import { Logo } from "../components/Logo";
import { Check, Loader2, ArrowRight } from "lucide-react";

const MAX_ATTEMPTS = 8;
const INTERVAL_MS = 2000;

export default function SignupSuccess() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const sessionId = params.get("session_id");
  const [state, setState] = useState("checking"); // checking | paid | expired | failed | unknown
  const [tier, setTier] = useState(null);
  const attemptsRef = useRef(0);

  useEffect(() => {
    if (!sessionId) return;
    let cancelled = false;

    const poll = async () => {
      if (cancelled) return;
      attemptsRef.current += 1;
      try {
        const { data } = await api.get(`/membership/checkout/status/${sessionId}`);
        if (cancelled) return;
        setTier(data.tier);
        if (data.payment_status === "paid") {
          setState("paid");
          return;
        }
        if (data.status === "expired") {
          setState("expired");
          return;
        }
        if (attemptsRef.current >= MAX_ATTEMPTS) {
          setState("unknown");
          return;
        }
        setTimeout(poll, INTERVAL_MS);
      } catch (e) {
        if (cancelled) return;
        if (attemptsRef.current >= MAX_ATTEMPTS) {
          setState("failed");
          return;
        }
        setTimeout(poll, INTERVAL_MS);
      }
    };
    poll();
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  return (
    <div className="min-h-screen w-full bg-equine-navyDeep text-white font-sans" data-testid="signup-success-page">
      <header className="px-6 md:px-12 py-6 max-w-5xl mx-auto">
        <Logo onNavy />
      </header>
      <div className="max-w-xl mx-auto px-6 py-20">
        <div className="bg-equine-navy/60 border border-white/10 rounded-2xl p-10 text-center">
          {state === "checking" && (
            <>
              <Loader2 className="w-10 h-10 text-equine-saddle animate-spin mx-auto mb-5" />
              <h1 className="font-display text-3xl text-white mb-2">Confirming your payment…</h1>
              <p className="text-white/60 text-[14px]">This usually takes just a moment.</p>
            </>
          )}
          {state === "paid" && (
            <>
              <div className="w-12 h-12 mx-auto rounded-full bg-equine-saddle/20 border border-equine-saddle/40 flex items-center justify-center mb-5">
                <Check className="w-6 h-6 text-equine-saddle" />
              </div>
              <h1 className="font-display text-3xl text-white mb-2" data-testid="success-paid-title">
                Welcome to Equine Sync.
              </h1>
              <p className="text-white/65 text-[14px] mb-2">
                Your membership is active{tier ? ` (${tier.replace("_", " / ")})` : ""}. You&apos;re all set.
              </p>
              {user?.role_status === "pending_review" && (
                <p className="text-equine-saddle text-[13px] mt-3" data-testid="success-pending-note">
                  Our team will verify your professional credentials shortly. You can explore in the meantime.
                </p>
              )}
              <button
                onClick={() => navigate("/dashboard")}
                className="mt-8 bg-equine-saddle text-equine-navyDeep hover:bg-white transition-colors px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                data-testid="success-go-dashboard"
              >
                Enter your dashboard <ArrowRight className="w-4 h-4" />
              </button>
            </>
          )}
          {state === "expired" && (
            <>
              <h1 className="font-display text-3xl text-white mb-2">Checkout expired</h1>
              <p className="text-white/65 text-[14px]">The session timed out. You can try again at any time.</p>
              <Link
                to="/signup"
                className="mt-7 inline-block bg-white text-equine-navyDeep hover:bg-equine-saddle transition-colors px-7 py-3 text-[13px] tracking-wide font-medium rounded-full"
                data-testid="success-retry"
              >
                Try again
              </Link>
            </>
          )}
          {state === "failed" && (
            <>
              <h1 className="font-display text-3xl text-white mb-2">We couldn&apos;t confirm your payment</h1>
              <p className="text-white/65 text-[14px]">Please check your email — Stripe will confirm shortly.</p>
              <button
                onClick={() => navigate("/dashboard")}
                className="mt-7 bg-white text-equine-navyDeep hover:bg-equine-saddle transition-colors px-7 py-3 text-[13px] tracking-wide font-medium rounded-full inline-flex items-center gap-2"
                data-testid="success-go-dashboard"
              >
                Go to dashboard <ArrowRight className="w-4 h-4" />
              </button>
            </>
          )}
          {state === "unknown" && (
            <>
              <h1 className="font-display text-3xl text-white mb-2">Hmm — we lost track of the session.</h1>
              <p className="text-white/65 text-[14px]">
                If you completed payment, your subscription will activate within a few minutes.
              </p>
              <button
                onClick={() => navigate("/dashboard")}
                className="mt-7 bg-white text-equine-navyDeep hover:bg-equine-saddle transition-colors px-7 py-3 text-[13px] tracking-wide font-medium rounded-full"
                data-testid="success-go-dashboard"
              >
                Continue
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
