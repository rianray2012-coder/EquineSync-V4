import * as Sentry from "@sentry/react";

const dsn = process.env.REACT_APP_SENTRY_DSN;
const environment = process.env.REACT_APP_SENTRY_ENVIRONMENT || process.env.NODE_ENV || "production";
const release = process.env.REACT_APP_SENTRY_RELEASE;
const apiUrl = process.env.REACT_APP_BACKEND_URL;

export const sentryEnabled = Boolean(dsn);

const sensitiveKeyPattern = /(authorization|cookie|password|token|secret|api[_-]?key|stripe|docusign|storage)/i;

const scrub = (value) => {
  if (Array.isArray(value)) return value.map(scrub);
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(
    Object.entries(value).map(([key, inner]) => [
      key,
      sensitiveKeyPattern.test(key) ? "[Filtered]" : scrub(inner),
    ]),
  );
};

const sampleTrace = (context) => {
  const name = context?.name || "";
  if (name.includes("/health")) return 0;
  if (name.includes("/billing") || name.includes("/subscription") || name.includes("/checkout")) return 1.0;
  return Number(process.env.REACT_APP_SENTRY_TRACES_SAMPLE_RATE || 0.2);
};

if (sentryEnabled) {
  Sentry.init({
    dsn,
    environment,
    release,
    integrations: [
      Sentry.browserTracingIntegration(),
      Sentry.replayIntegration({
        maskAllText: true,
        blockAllMedia: true,
      }),
    ],
    tracesSampler: sampleTrace,
    tracePropagationTargets: [
      "localhost",
      /^https:\/\/api\.equine-sync\.com\/api/,
      ...(apiUrl ? [apiUrl] : []),
    ],
    replaysSessionSampleRate: Number(process.env.REACT_APP_SENTRY_REPLAY_SESSION_SAMPLE_RATE || 0),
    replaysOnErrorSampleRate: Number(process.env.REACT_APP_SENTRY_REPLAY_ON_ERROR_SAMPLE_RATE || 1.0),
    beforeSend(event) {
      event.extra = scrub(event.extra || {});
      event.contexts = scrub(event.contexts || {});
      return event;
    },
  });
  Sentry.setTag("service", "equinesync-web");
}

export const reactRootErrorHandler = sentryEnabled ? Sentry.reactErrorHandler() : undefined;
