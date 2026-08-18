import React from "react";
import { Link, useSearchParams } from "react-router-dom";
import { AlertTriangle, ArrowRight, CheckCircle2, FileSignature } from "lucide-react";

import { Card, PageHeader, StatusPill } from "../components/Primitives";

const truncate = (value) => {
  const text = String(value || "").trim();
  if (!text) return null;
  return text.length > 18 ? `${text.slice(0, 18)}...` : text;
};

export default function DocusignCallback() {
  const [params] = useSearchParams();
  const error = params.get("error");
  const errorDescription = params.get("error_description");
  const codeRef = truncate(params.get("code"));
  const stateRef = truncate(params.get("state"));
  const hasConsentSignal = Boolean(codeRef) && !error;

  return (
    <div data-testid="docusign-callback-page" className="pb-20 lg:pb-8 max-w-3xl">
      <PageHeader
        eyebrow="Document signing"
        title="DocuSign connection received"
        subtitle="EquineSync received the DocuSign handoff. The integration can now be verified from the backend without showing credentials in the browser."
      />

      <Card hover={false} className="border-equine-saddle/40" data-testid="docusign-callback-summary">
        <div className="flex items-start gap-4 flex-wrap">
          <div className="rounded-full bg-equine-saddle/15 p-3 border border-equine-saddle/40">
            {error ? (
              <AlertTriangle className="w-5 h-5 text-equine-clay" />
            ) : hasConsentSignal ? (
              <CheckCircle2 className="w-5 h-5 text-equine-saddleDeep" />
            ) : (
              <FileSignature className="w-5 h-5 text-equine-saddleDeep" />
            )}
          </div>
          <div className="flex-1 min-w-[220px]">
            <div className="flex items-center gap-2 flex-wrap mb-2">
              <div className="font-display text-2xl text-equine-ink">
                {error ? "Consent needs attention" : hasConsentSignal ? "Consent handoff captured" : "Callback route is ready"}
              </div>
              <StatusPill tone={error ? "warning" : "success"} dot>
                {error ? "Attention" : "Ready"}
              </StatusPill>
            </div>
            <p className="text-[13.5px] text-equine-inkMuted leading-relaxed">
              {error
                ? "DocuSign returned an error instead of a consent code. Check the integration key, redirect URI, and selected DocuSign environment before retrying."
                : hasConsentSignal
                  ? "DocuSign returned a consent code. EquineSync does not display or store that code in this page; backend JWT verification remains the source of truth."
                  : "This page is available for DocuSign redirects. When the consent flow is retried, DocuSign should land here instead of an unreachable or generic page."}
            </p>

            <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-[12px] text-equine-inkMuted">
              <div data-testid="docusign-callback-code-ref">
                <span className="text-equine-inkSoft">Code ref:</span> {codeRef || "none"}
              </div>
              <div data-testid="docusign-callback-state-ref">
                <span className="text-equine-inkSoft">State ref:</span> {stateRef || "none"}
              </div>
            </div>

            {error && (
              <div
                data-testid="docusign-callback-error"
                className="mt-4 rounded-lg border border-equine-clay/30 bg-equine-clay/8 p-3 text-[12.5px] text-equine-inkMuted"
              >
                <div className="font-medium text-equine-ink mb-1">{error}</div>
                <div>{errorDescription || "No additional DocuSign error description was provided."}</div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 flex flex-wrap gap-3">
          <Link
            to="/integrations"
            data-testid="docusign-callback-go-integrations"
            className="inline-flex items-center gap-1.5 text-[12.5px] tracking-wide font-medium px-4 py-2 rounded-full bg-equine-navy text-white hover:bg-equine-navyLift transition-colors"
          >
            Review integrations <ArrowRight className="w-3.5 h-3.5" />
          </Link>
          <Link
            to="/forms-signatures"
            data-testid="docusign-callback-go-forms"
            className="inline-flex items-center gap-1.5 text-[12.5px] tracking-wide px-4 py-2 rounded-full border border-equine-graphite/40 text-equine-ink hover:border-equine-saddleDeep/40 hover:text-equine-saddleDeep transition-colors"
          >
            Forms and signatures
          </Link>
        </div>
      </Card>
    </div>
  );
}
