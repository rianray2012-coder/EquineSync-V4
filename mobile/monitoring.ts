import * as Sentry from '@sentry/react-native';
import type { ComponentType } from 'react';

const sentryEnv = process.env.EXPO_PUBLIC_SENTRY_ENVIRONMENT
  || process.env.EXPO_PUBLIC_APP_ENV
  || (typeof __DEV__ !== 'undefined' && __DEV__ ? 'development' : 'production');

const sensitiveKeyPattern = /(authorization|cookie|password|token|secret|api[_-]?key|stripe|docusign|storage)/i;

const scrub = (value: unknown): unknown => {
  if (Array.isArray(value)) {
    return value.map(scrub);
  }

  if (!value || typeof value !== 'object') {
    return value;
  }

  return Object.fromEntries(
    Object.entries(value).map(([key, inner]) => [
      key,
      sensitiveKeyPattern.test(key) ? '[Filtered]' : scrub(inner),
    ]),
  );
};

export const sentryEnabled = Boolean(process.env.EXPO_PUBLIC_SENTRY_DSN);
export const sentryProofEnabled = process.env.EXPO_PUBLIC_SENTRY_PROOF_ENABLED === 'true';

if (sentryEnabled) {
  Sentry.init({
    dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
    environment: sentryEnv,
    release: process.env.EXPO_PUBLIC_SENTRY_RELEASE,
    sendDefaultPii: false,
    tracesSampleRate: Number(process.env.EXPO_PUBLIC_SENTRY_TRACES_SAMPLE_RATE || 0.2),
    replaysSessionSampleRate: Number(process.env.EXPO_PUBLIC_SENTRY_REPLAY_SESSION_SAMPLE_RATE || 0),
    replaysOnErrorSampleRate: Number(process.env.EXPO_PUBLIC_SENTRY_REPLAY_ON_ERROR_SAMPLE_RATE || 1.0),
    beforeSend(event) {
      event.extra = scrub(event.extra || {}) as typeof event.extra;
      event.contexts = scrub(event.contexts || {}) as typeof event.contexts;
      return event;
    },
  });

  Sentry.setTag('service', 'equinesync-mobile');
}

export const wrapWithSentry = <T extends ComponentType<any>>(Component: T): T => {
  if (!sentryEnabled) {
    return Component;
  }

  return Sentry.wrap(Component) as T;
};

export const captureNativeMonitoringProof = (proofHash?: string, platform?: string) => {
  if (!sentryEnabled || !sentryProofEnabled) {
    return {
      sent: false,
      reason: sentryEnabled ? 'proof_disabled' : 'sentry_disabled',
    };
  }

  const safeProofHash = String(proofHash || process.env.EXPO_PUBLIC_SENTRY_PROOF_HASH || 'missing-proof-hash').slice(0, 64);

  Sentry.withScope((scope) => {
    scope.setTag('service', 'equinesync-mobile');
    scope.setTag('proof_hash', safeProofHash);
    if (platform) {
      scope.setTag('platform', platform);
    }
    scope.setLevel('info');
    Sentry.captureMessage('EquineSync native Sentry proof event');
  });

  return {
    sent: true,
    proofHash: safeProofHash,
  };
};
