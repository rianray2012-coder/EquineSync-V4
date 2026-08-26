import Constants from 'expo-constants';
import * as Device from 'expo-device';
import * as Notifications from 'expo-notifications';
import * as SecureStore from 'expo-secure-store';
import { StatusBar } from 'expo-status-bar';
import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  LogBox,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import { captureNativeMonitoringProof, sentryEnabled, sentryProofEnabled } from './monitoring';

LogBox.ignoreAllLogs(true);

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowBanner: true,
    shouldShowList: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

type HealthState =
  | { status: 'checking' }
  | { status: 'pass'; message: string; details: string[] }
  | { status: 'fail'; message: string; details: string[] };

type SessionUser = {
  id: string;
  email: string;
  full_name?: string;
  role?: string;
  barn_id?: string;
  facility_status?: string;
};

type SessionState = {
  token: string;
  refreshToken: string;
  expiresAt: number;
  user: SessionUser;
};

type AccountContext = {
  active_context?: {
    account_id?: string;
    account_type?: string;
    barn_id?: string;
    role?: string;
    role_status?: string;
    membership_status?: string;
    relationship_type?: string;
    is_primary?: boolean;
  } | null;
  available_contexts?: Array<{
    account_id?: string;
    account_type?: string;
    barn_id?: string;
    role?: string;
    role_status?: string;
    membership_status?: string;
    relationship_type?: string;
    is_primary?: boolean;
  }>;
  platform_context?: boolean;
  platform_role?: string | null;
  requested_context_found?: boolean | null;
};

type AuthResponse = {
  token: string;
  refresh_token: string;
  expires_in_seconds: number;
  user: SessionUser;
};

type PushRegistrationResponse = {
  ok: boolean;
  provider: string;
  platform: string;
  enabled: boolean;
  token_hash: string;
};

type PushProofResponse = {
  ok: boolean;
  provider: string;
  purpose: string;
  token_hash: string;
  message: string;
};

type AiDraftQueueResponse = {
  jobs: Array<{
    id: string;
    status: string;
    review_status?: string;
    draft_only: boolean;
    review_required: boolean;
    source_type: string;
  }>;
};

declare const process: {
  env?: Record<string, string | undefined>;
};

const APP_ENV = process.env?.EXPO_PUBLIC_APP_ENV ?? 'native-dev';
const SENTRY_PROOF_HASH = process.env?.EXPO_PUBLIC_SENTRY_PROOF_HASH ?? '';
const configuredApiBaseUrl = (process.env?.EXPO_PUBLIC_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '');
const API_BASE_URL =
  Platform.OS === 'android'
    ? configuredApiBaseUrl.replace('localhost', '10.0.2.2').replace('127.0.0.1', '10.0.2.2')
    : configuredApiBaseUrl;
const SESSION_KEY = 'equinesync.native.session.v1';
const PUSH_DEVICE_KEY = 'equinesync.native.push.device.v1';
const SERVICE_PROVIDER_ROLES = ['service_provider', 'veterinarian', 'farrier'];
const STAFF_ROLES = ['groom', 'working_student'];
const EAS_PROJECT_ID =
  ((Constants.expoConfig?.extra as { eas?: { projectId?: string } } | undefined)?.eas?.projectId
    ?? Constants.easConfig?.projectId
    ?? '').trim();

type RoleHome = {
  key: string;
  title: string;
  subtitle: string;
  status: 'allowed' | 'deferred' | 'denied';
};

function normalizeRole(role?: string | null) {
  return String(role ?? '').trim().toLowerCase();
}

function labelFor(value?: string | null) {
  const cleaned = String(value ?? '').replace(/_/g, ' ').trim();
  return cleaned || 'unknown';
}

function nativeLandingFor(user?: SessionUser | null, context?: AccountContext | null) {
  const role = normalizeRole(context?.active_context?.role ?? user?.role);
  const accountType = context?.active_context?.account_type;
  const membershipStatus = normalizeRole(context?.active_context?.membership_status);

  if (context?.platform_context) return 'Platform Admin Console';
  if (!role) return 'Unassigned Role Review';
  if (membershipStatus && !['active', 'pending_review'].includes(membershipStatus)) {
    return 'Membership Review';
  }
  if (role === 'admin' || role === 'barn_owner') return 'Facility Dashboard';
  if (role === 'barn_manager') return 'Manager Dashboard';
  if (role === 'trainer') return 'Trainer Operating Center';
  if (STAFF_ROLES.includes(role)) return 'Staff Work Queue';
  if (role === 'horse_owner' && accountType === 'individual_owner') return 'Individual Owner Home';
  if (role === 'horse_owner') return 'Owner Dashboard';
  if (role === 'parent') return 'Guardian Dashboard';
  if (role === 'rider') return 'Rider Dashboard';
  if (SERVICE_PROVIDER_ROLES.includes(role)) return 'Service Provider Center';
  return 'Settings And Support';
}

function roleHomesFor(user?: SessionUser | null, context?: AccountContext | null): RoleHome[] {
  const role = normalizeRole(context?.active_context?.role ?? user?.role);
  const platformContext = Boolean(context?.platform_context);

  const homes = [
    {
      key: 'platform',
      title: 'Platform Admin Console',
      subtitle: 'Platform-level oversight, configuration, and support boundaries.',
      allowed: platformContext,
    },
    {
      key: 'facility',
      title: 'Facility Dashboard',
      subtitle: 'Facility owner and barn owner operations, setup, staff, and facility context.',
      allowed: !platformContext && (role === 'admin' || role === 'barn_owner'),
    },
    {
      key: 'manager',
      title: 'Manager Dashboard',
      subtitle: 'Daily operations, barn team coordination, and facility tasks.',
      allowed: role === 'barn_manager',
    },
    {
      key: 'trainer',
      title: 'Trainer Operating Center',
      subtitle: 'Assigned horses, lessons, training plans, and rider context.',
      allowed: role === 'trainer',
    },
    {
      key: 'staff',
      title: 'Staff Work Queue',
      subtitle: 'Assigned work, barn tasks, and safe daily handoff context.',
      allowed: STAFF_ROLES.includes(role),
    },
    {
      key: 'owner',
      title: 'Owner Dashboard',
      subtitle: 'Owner-safe horse context, updates, documents, and billing visibility.',
      allowed: role === 'horse_owner',
    },
    {
      key: 'guardian',
      title: 'Guardian Dashboard',
      subtitle: 'Guardian-safe minor/rider context and approved communication boundaries.',
      allowed: role === 'parent',
    },
    {
      key: 'rider',
      title: 'Rider Dashboard',
      subtitle: 'Rider-safe lessons, goals, and personal training context.',
      allowed: role === 'rider',
    },
    {
      key: 'provider',
      title: 'Service Provider Center',
      subtitle: 'Grant-scoped shared horses and provider-authored visit notes.',
      allowed: SERVICE_PROVIDER_ROLES.includes(role),
    },
  ];

  return homes.map(({ allowed, ...home }) => ({
    ...home,
    status: allowed ? 'allowed' : 'denied',
  }));
}

function sessionFromAuthResponse(payload: AuthResponse): SessionState {
  return {
    token: payload.token,
    refreshToken: payload.refresh_token,
    expiresAt: Date.now() + payload.expires_in_seconds * 1000,
    user: payload.user,
  };
}

function friendlyError(error: unknown) {
  if (error instanceof Error && error.message) {
    return error.message;
  }
  return 'The request could not be completed.';
}

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
  });
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = typeof payload?.detail === 'string' ? payload.detail : `API returned ${response.status}`;
    throw new Error(detail);
  }

  return payload as T;
}

async function saveSession(session: SessionState) {
  await SecureStore.setItemAsync(SESSION_KEY, JSON.stringify(session));
}

async function readStoredSession() {
  const raw = await SecureStore.getItemAsync(SESSION_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as SessionState;
  } catch {
    await SecureStore.deleteItemAsync(SESSION_KEY);
    return null;
  }
}

async function clearStoredSession() {
  await SecureStore.deleteItemAsync(SESSION_KEY);
}

async function getOrCreatePushDeviceId() {
  const stored = await SecureStore.getItemAsync(PUSH_DEVICE_KEY);
  if (stored) return stored;
  const next = `${Platform.OS}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
  await SecureStore.setItemAsync(PUSH_DEVICE_KEY, next);
  return next;
}

export default function App() {
  const [health, setHealth] = useState<HealthState>({ status: 'checking' });
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [session, setSession] = useState<SessionState | null>(null);
  const [accountContext, setAccountContext] = useState<AccountContext | null>(null);
  const [contextStatus, setContextStatus] = useState('Waiting for signed-in session.');
  const [monitoringProofStatus, setMonitoringProofStatus] = useState('Monitoring proof not sent.');
  const [pushStatus, setPushStatus] = useState('Push proof not started.');
  const [pushTokenHash, setPushTokenHash] = useState('');
  const [pushBusy, setPushBusy] = useState(false);
  const [aiDraftStatus, setAiDraftStatus] = useState('AI draft review path not checked.');
  const [aiDraftCount, setAiDraftCount] = useState<number | null>(null);
  const [aiDraftBusy, setAiDraftBusy] = useState(false);
  const [authStatus, setAuthStatus] = useState('Checking stored session...');
  const [authBusy, setAuthBusy] = useState(false);
  const [restoreBusy, setRestoreBusy] = useState(true);

  const healthUrl = useMemo(() => `${API_BASE_URL}/api/health`, []);

  const checkHealth = useCallback(async () => {
    setHealth({ status: 'checking' });

    try {
      const payload = await apiRequest<{
        status?: string;
        service?: string;
        database?: string;
        config?: { environment?: string };
      }>('/api/health');

      if (payload?.status !== 'ok') {
        setHealth({
          status: 'fail',
          message: 'API health check failed',
          details: [`status=${String(payload?.status ?? 'unknown')}`],
        });
        return;
      }

      setHealth({
        status: 'pass',
        message: 'API health check passed',
        details: [
          `service=${String(payload?.service ?? 'unknown')}`,
          `environment=${String(payload?.config?.environment ?? 'unknown')}`,
          `database=${String(payload?.database ?? 'unknown')}`,
        ],
      });
    } catch (error) {
      setHealth({
        status: 'fail',
        message: 'API health check failed',
        details: [friendlyError(error)],
      });
    }
  }, []);

  const fetchAccountContext = useCallback(async (token: string) => {
    setContextStatus('Loading role context...');
    try {
      const context = await apiRequest<AccountContext>('/api/account/context', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setAccountContext(context);
      setContextStatus('Role context confirmed.');
      return context;
    } catch (error) {
      setAccountContext(null);
      setContextStatus(`Role context unavailable: ${friendlyError(error)}`);
      return null;
    }
  }, []);

  const refreshSession = useCallback(async (refreshToken: string) => {
    const payload = await apiRequest<AuthResponse>('/api/auth/refresh', {
      method: 'POST',
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    const nextSession = sessionFromAuthResponse(payload);
    await saveSession(nextSession);
    setSession(nextSession);
    await fetchAccountContext(nextSession.token);
    setAuthStatus('Session restored.');
    return nextSession;
  }, [fetchAccountContext]);

  const restoreSession = useCallback(async () => {
    setRestoreBusy(true);
    try {
      const stored = await readStoredSession();
      if (!stored?.refreshToken) {
        setSession(null);
        setAuthStatus('No saved session yet.');
        return;
      }
      await refreshSession(stored.refreshToken);
    } catch (error) {
      await clearStoredSession();
      setSession(null);
      setAuthStatus(`Stored session cleared: ${friendlyError(error)}`);
    } finally {
      setRestoreBusy(false);
    }
  }, [refreshSession]);

  useEffect(() => {
    void checkHealth();
    void restoreSession();
  }, [checkHealth, restoreSession]);

  const signIn = useCallback(async () => {
    setAuthBusy(true);
    setAuthStatus('Signing in...');
    try {
      const payload = await apiRequest<AuthResponse>('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: email.trim().toLowerCase(), password }),
      });
      const nextSession = sessionFromAuthResponse(payload);
      await saveSession(nextSession);
      setSession(nextSession);
      await fetchAccountContext(nextSession.token);
      setPassword('');
      setAuthStatus('Signed in.');
    } catch (error) {
      setAuthStatus(`Sign-in failed: ${friendlyError(error)}`);
    } finally {
      setAuthBusy(false);
    }
  }, [email, password, fetchAccountContext]);

  const checkCurrentUser = useCallback(async () => {
    if (!session) return;
    setAuthBusy(true);
    setAuthStatus('Checking current user...');
    try {
      const user = await apiRequest<SessionUser>('/api/auth/me', {
        headers: { Authorization: `Bearer ${session.token}` },
      });
      const nextSession = { ...session, user };
      await saveSession(nextSession);
      setSession(nextSession);
      await fetchAccountContext(nextSession.token);
      setAuthStatus('Current user confirmed.');
    } catch (error) {
      setAuthStatus(`Current-user check failed: ${friendlyError(error)}`);
    } finally {
      setAuthBusy(false);
    }
  }, [session, fetchAccountContext]);

  const signOut = useCallback(async () => {
    setAuthBusy(true);
    setAuthStatus('Signing out...');
    try {
      if (session?.token && session?.refreshToken) {
        await apiRequest<{ ok: boolean }>('/api/auth/logout', {
          method: 'POST',
          headers: { Authorization: `Bearer ${session.token}` },
          body: JSON.stringify({ refresh_token: session.refreshToken }),
        });
      }
    } catch (error) {
      setAuthStatus(`Remote sign-out warning: ${friendlyError(error)}`);
    } finally {
      await clearStoredSession();
      setSession(null);
      setAccountContext(null);
      setAuthBusy(false);
      setAuthStatus('Signed out locally.');
      setContextStatus('Waiting for signed-in session.');
    }
  }, [session]);

  const sendMonitoringProof = useCallback(() => {
    const result = captureNativeMonitoringProof(SENTRY_PROOF_HASH, Platform.OS);
    setMonitoringProofStatus(
      result.sent
        ? `Monitoring proof sent: ${result.proofHash}`
        : `Monitoring proof not sent: ${result.reason}`,
    );
  }, []);

  const registerPushNotifications = useCallback(async () => {
    if (!session?.token) return;
    setPushBusy(true);
    setPushStatus('Requesting notification permission...');
    try {
      if (!Device.isDevice) {
        throw new Error('Physical device required for push proof.');
      }
      if (!EAS_PROJECT_ID) {
        throw new Error('EAS project ID missing from app config.');
      }
      if (Platform.OS === 'android') {
        await Notifications.setNotificationChannelAsync('default', {
          name: 'EquineSync',
          importance: Notifications.AndroidImportance.DEFAULT,
        });
      }

      const currentPermission = await Notifications.getPermissionsAsync();
      const finalPermission =
        currentPermission.status === 'granted'
          ? currentPermission
          : await Notifications.requestPermissionsAsync();
      if (finalPermission.status !== 'granted') {
        throw new Error(`Notification permission ${finalPermission.status}.`);
      }

      const token = await Notifications.getExpoPushTokenAsync({ projectId: EAS_PROJECT_ID });
      const deviceId = await getOrCreatePushDeviceId();
      const response = await apiRequest<PushRegistrationResponse>('/api/notifications/push-token', {
        method: 'POST',
        headers: { Authorization: `Bearer ${session.token}` },
        body: JSON.stringify({
          expo_push_token: token.data,
          platform: Platform.OS,
          device_id: deviceId,
          permission_status: finalPermission.status,
          enabled: true,
        }),
      });
      setPushTokenHash(response.token_hash);
      setPushStatus(`Expo push token registered: ${response.token_hash}`);
    } catch (error) {
      setPushStatus(`Push registration failed: ${friendlyError(error)}`);
    } finally {
      setPushBusy(false);
    }
  }, [session]);

  const disablePushNotifications = useCallback(async () => {
    if (!session?.token) return;
    setPushBusy(true);
    setPushStatus('Disabling push tokens...');
    try {
      const response = await apiRequest<{ ok: boolean; disabled_count: number }>('/api/notifications/push-token/disable', {
        method: 'POST',
        headers: { Authorization: `Bearer ${session.token}` },
      });
      setPushStatus(`Push disabled: ${response.disabled_count} token(s).`);
    } catch (error) {
      setPushStatus(`Push disable failed: ${friendlyError(error)}`);
    } finally {
      setPushBusy(false);
    }
  }, [session]);

  const sendPushProof = useCallback(async () => {
    if (!session?.token) return;
    setPushBusy(true);
    setPushStatus('Sending Founder-only push proof...');
    try {
      const response = await apiRequest<PushProofResponse>('/api/notifications/push-proof/send-me', {
        method: 'POST',
        headers: { Authorization: `Bearer ${session.token}` },
      });
      setPushTokenHash(response.token_hash);
      setPushStatus(`Push proof sent: ${response.message}`);
    } catch (error) {
      setPushStatus(`Push proof failed: ${friendlyError(error)}`);
    } finally {
      setPushBusy(false);
    }
  }, [session]);

  const checkAiDraftQueue = useCallback(async () => {
    if (!session?.token) return;
    setAiDraftBusy(true);
    setAiDraftStatus('Checking draft-only review queue...');
    try {
      const response = await apiRequest<AiDraftQueueResponse>('/api/ai/draft-jobs?limit=5', {
        headers: { Authorization: `Bearer ${session.token}` },
      });
      setAiDraftCount(response.jobs.length);
      setAiDraftStatus(`Draft queue reachable: ${response.jobs.length} visible draft(s).`);
    } catch (error) {
      setAiDraftCount(null);
      setAiDraftStatus(`Draft queue unavailable: ${friendlyError(error)}`);
    } finally {
      setAiDraftBusy(false);
    }
  }, [session]);

  const statusColor = health.status === 'pass' ? '#1f8a5b' : health.status === 'fail' ? '#b42318' : '#5f6b7a';
  const canSignIn = email.trim().length > 3 && password.length > 0 && !authBusy && !restoreBusy;
  const activeContext = accountContext?.active_context ?? null;
  const roleHomes = roleHomesFor(session?.user, accountContext);
  const selectedLanding = nativeLandingFor(session?.user, accountContext);
  const allowedHome = roleHomes.find((home) => home.status === 'allowed');
  const deniedProofHome = roleHomes.find((home) => home.status === 'denied');
  const availableContextCount = accountContext?.available_contexts?.length ?? 0;
  const authPanel = (
    <View style={[styles.panel, !session && styles.priorityPanel]}>
      <View style={styles.statusHeader}>
        <Text style={styles.panelLabel}>Auth Session</Text>
        {authBusy || restoreBusy ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: session ? '#1f8a5b' : '#9aa3a0' }]} />}
      </View>

      {session ? (
        <View style={styles.authDetails}>
          <Text style={styles.healthMessage}>Signed in</Text>
          <Text style={styles.detail}>email={session.user.email}</Text>
          <Text style={styles.detail}>role={session.user.role ?? 'unknown'}</Text>
          <Text style={styles.detail}>barn={session.user.barn_id ?? 'primary'}</Text>
          <Text style={styles.detail}>facility={session.user.facility_status ?? 'unknown'}</Text>
          <View style={styles.buttonRow}>
            <Pressable accessibilityRole="button" disabled={authBusy} onPress={checkCurrentUser} style={styles.button}>
              <Text style={styles.buttonText}>Check Me</Text>
            </Pressable>
            <Pressable accessibilityRole="button" disabled={authBusy} onPress={signOut} style={[styles.button, styles.secondaryButton]}>
              <Text style={styles.secondaryButtonText}>Sign Out</Text>
            </Pressable>
          </View>
          {sentryProofEnabled ? (
            <View style={styles.monitoringProof}>
              <Text style={styles.detail} testID="monitoring-proof-sdk">
                sentry={sentryEnabled ? 'enabled' : 'disabled'}
              </Text>
              <Text style={styles.detail} testID="monitoring-proof-hash">
                proof={SENTRY_PROOF_HASH || 'missing'}
              </Text>
              <Pressable
                accessibilityLabel="Send Monitoring Proof"
                accessibilityRole="button"
                disabled={!sentryEnabled || !SENTRY_PROOF_HASH}
                onPress={sendMonitoringProof}
                style={[styles.button, (!sentryEnabled || !SENTRY_PROOF_HASH) && styles.disabledButton]}
                testID="monitoring-proof-send"
              >
                <Text style={styles.buttonText}>Send Monitoring Proof</Text>
              </Pressable>
              <Text style={styles.caption} testID="monitoring-proof-result">
                {monitoringProofStatus}
              </Text>
            </View>
          ) : null}
        </View>
      ) : (
        <View style={styles.authDetails}>
          <TextInput
            accessibilityLabel="Email"
            autoCapitalize="none"
            autoComplete="email"
            inputMode="email"
            onChangeText={setEmail}
            placeholder="Email"
            style={styles.input}
            testID="auth-email-input"
            textContentType="username"
            value={email}
          />
          <TextInput
            accessibilityLabel="Password"
            autoCapitalize="none"
            autoComplete="password"
            onChangeText={setPassword}
            placeholder="Password"
            secureTextEntry
            style={styles.input}
            testID="auth-password-input"
            textContentType="password"
            value={password}
          />
          <Pressable accessibilityLabel="Sign In" accessibilityRole="button" disabled={!canSignIn} onPress={signIn} style={[styles.button, !canSignIn && styles.disabledButton]} testID="auth-sign-in-button">
            <Text style={styles.buttonText}>Sign In</Text>
          </Pressable>
        </View>
      )}
      <Text style={styles.caption}>{authStatus}</Text>
    </View>
  );

  return (
    <View style={styles.shell}>
      <StatusBar style="dark" />
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.keyboard}>
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
          <View style={styles.header}>
            <Text style={styles.kicker}>Native Foundation</Text>
            <Text style={styles.title}>EquineSync</Text>
            <Text style={styles.subtitle}>React Native / Expo internal evidence track</Text>
          </View>

          {!session ? authPanel : null}

          <View style={styles.panel}>
            <Text style={styles.panelLabel}>Environment</Text>
            <Text style={styles.value}>{APP_ENV}</Text>
            <Text style={styles.caption}>First target is native-dev/staging. Production writes remain blocked.</Text>
          </View>

          <View style={styles.panel}>
            <Text style={styles.panelLabel}>API Target</Text>
            <Text style={styles.value}>{API_BASE_URL}</Text>
            <Text style={styles.caption}>Health endpoint: /api/health</Text>
          </View>

          <View style={styles.panel}>
            <View style={styles.statusHeader}>
              <Text style={styles.panelLabel}>Health Check</Text>
              {health.status === 'checking' ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: statusColor }]} />}
            </View>
            <Text style={[styles.healthMessage, { color: statusColor }]}>{health.status === 'checking' ? 'Checking API health...' : health.message}</Text>
            {health.status !== 'checking' &&
              health.details.map((detail) => (
                <Text key={detail} style={styles.detail}>
                  {detail}
                </Text>
              ))}
            <Pressable accessibilityRole="button" onPress={checkHealth} style={styles.button}>
              <Text style={styles.buttonText}>Recheck</Text>
            </Pressable>
          </View>

          {session ? authPanel : null}

          {session ? (
            <View style={styles.panel} testID="push-proof-panel">
              <View style={styles.statusHeader}>
                <Text style={styles.panelLabel}>Push Notifications</Text>
                {pushBusy ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: pushTokenHash ? '#1f8a5b' : '#9aa3a0' }]} />}
              </View>
              <Text style={styles.healthMessage}>Expo Push Proof</Text>
              <Text style={styles.detail} testID="push-proof-provider">
                provider=expo
              </Text>
              <Text style={styles.detail} testID="push-proof-platform">
                platform={Platform.OS}
              </Text>
              <Text style={styles.detail} testID="push-proof-policy">
                policy=generic_previews_only
              </Text>
              <Text style={styles.detail} testID="push-proof-token-hash">
                token_hash={pushTokenHash || 'not_registered'}
              </Text>
              <View style={styles.buttonRow}>
                <Pressable
                  accessibilityLabel="Register Push Token"
                  accessibilityRole="button"
                  disabled={pushBusy}
                  onPress={registerPushNotifications}
                  style={[styles.button, pushBusy && styles.disabledButton]}
                  testID="push-register-button"
                >
                  <Text style={styles.buttonText}>Register Push</Text>
                </Pressable>
                <Pressable
                  accessibilityLabel="Send Push Proof"
                  accessibilityRole="button"
                  disabled={pushBusy || !pushTokenHash}
                  onPress={sendPushProof}
                  style={[styles.button, (pushBusy || !pushTokenHash) && styles.disabledButton]}
                  testID="push-proof-send-button"
                >
                  <Text style={styles.buttonText}>Send Proof</Text>
                </Pressable>
              </View>
              <Pressable
                accessibilityLabel="Disable Push Notifications"
                accessibilityRole="button"
                disabled={pushBusy}
                onPress={disablePushNotifications}
                style={[styles.button, styles.secondaryButton, pushBusy && styles.disabledButton]}
                testID="push-disable-button"
              >
                <Text style={styles.secondaryButtonText}>Disable Push</Text>
              </Pressable>
              <Text style={styles.caption} testID="push-proof-result">
                {pushStatus}
              </Text>
            </View>
          ) : null}

          {session ? (
            <View style={styles.panel} testID="ai-draft-review-panel">
              <View style={styles.statusHeader}>
                <Text style={styles.panelLabel}>AI Draft Review</Text>
                {aiDraftBusy ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: aiDraftCount !== null ? '#1f8a5b' : '#9aa3a0' }]} />}
              </View>
              <Text style={styles.healthMessage}>Mobile-Safe Review Path</Text>
              <Text style={styles.detail} testID="ai-draft-boundary">
                boundary=draft_only_review_required
              </Text>
              <Text style={styles.detail} testID="ai-draft-official-save">
                official_save=blocked
              </Text>
              <Text style={styles.detail} testID="ai-draft-visible-count">
                visible_drafts={aiDraftCount === null ? 'not_checked' : aiDraftCount}
              </Text>
              <Pressable
                accessibilityLabel="Check AI Draft Queue"
                accessibilityRole="button"
                disabled={aiDraftBusy}
                onPress={checkAiDraftQueue}
                style={[styles.button, aiDraftBusy && styles.disabledButton]}
                testID="ai-draft-check-button"
              >
                <Text style={styles.buttonText}>Check Draft Queue</Text>
              </Pressable>
              <Text style={styles.caption} testID="ai-draft-result">
                {aiDraftStatus}
              </Text>
            </View>
          ) : null}

          <View style={styles.panel}>
            <View style={styles.statusHeader}>
              <Text style={styles.panelLabel}>Role Context</Text>
              {session && !accountContext ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: accountContext ? '#1f8a5b' : '#9aa3a0' }]} />}
            </View>

            {session ? (
              <View style={styles.roleDetails}>
                <Text style={styles.healthMessage}>{selectedLanding}</Text>
                <Text style={styles.detail} testID="role-context-role">
                  role={labelFor(activeContext?.role ?? session.user.role)}
                </Text>
                <Text style={styles.detail} testID="role-context-account">
                  account={labelFor(activeContext?.account_type)}
                </Text>
                <Text style={styles.detail} testID="role-context-membership">
                  membership={labelFor(activeContext?.membership_status)}
                </Text>
                <Text style={styles.detail}>contexts={availableContextCount}</Text>
                <Text style={styles.caption}>{contextStatus}</Text>

                <View style={styles.roleProofStrip} testID="role-proof-strip">
                  <Text style={styles.proofText} testID="role-proof-membership">
                    membership={labelFor(activeContext?.membership_status)}
                  </Text>
                  <Text style={styles.proofText} testID="role-proof-denied">
                    DENIED{deniedProofHome ? ` ${deniedProofHome.title}` : ''}
                  </Text>
                </View>

                <View style={styles.roleHomeList}>
                  {roleHomes.map((home) => (
                    <View
                      accessibilityLabel={`${home.title} ${home.status === 'allowed' ? 'ALLOWED' : 'DENIED'}`}
                      key={home.key}
                      style={[styles.roleHome, home.status === 'allowed' ? styles.allowedRoleHome : styles.deniedRoleHome]}
                      testID={`role-home-${home.key}`}
                    >
                      <View style={styles.roleHomeHeader}>
                        <Text style={styles.roleHomeTitle}>{home.title}</Text>
                        <Text
                          accessibilityLabel={`role-home-${home.key}-${home.status === 'allowed' ? 'ALLOWED' : 'DENIED'}`}
                          style={[styles.statusPill, home.status === 'allowed' ? styles.allowedPill : styles.deniedPill]}
                          testID={`role-home-${home.key}-${home.status}-status`}
                        >
                          {home.status === 'allowed' ? 'ALLOWED' : 'DENIED'}
                        </Text>
                      </View>
                      <Text style={styles.caption}>{home.subtitle}</Text>
                    </View>
                  ))}
                </View>

                <View accessibilityLabel="Denied-Access Guard DENIED" style={styles.deniedBox} testID="denied-access-guard">
                  <Text style={styles.deniedTitle}>Denied-Access Guard</Text>
                  <Text style={styles.caption}>
                    Cross-role homes remain unavailable unless the backend returns that role in the active account context.
                    {allowedHome ? ` Current allowed home: ${allowedHome.title}.` : ' No role home is currently allowed.'}
                  </Text>
                </View>

              </View>
            ) : (
              <Text style={styles.caption}>Sign in to resolve backend-authoritative role and membership context.</Text>
            )}
          </View>

          <View style={styles.boundary}>
            <Text style={styles.boundaryTitle}>Current Boundary</Text>
            <Text style={styles.boundaryText}>
              Internal role-routing evidence only. Workflow actions, live provider behavior, native billing, production writes, and full offline claims stay deferred until the governance-to-product audit closes.
            </Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  shell: {
    flex: 1,
    backgroundColor: '#f6f7f2',
  },
  keyboard: {
    flex: 1,
  },
  content: {
    flexGrow: 1,
    gap: 14,
    padding: 22,
    paddingTop: Platform.OS === 'ios' ? 58 : 22,
  },
  header: {
    gap: 6,
    paddingTop: 16,
    paddingBottom: 8,
  },
  kicker: {
    color: '#5d6f64',
    fontSize: 13,
    fontWeight: '700',
    letterSpacing: 0,
    textTransform: 'uppercase',
  },
  title: {
    color: '#18231c',
    fontSize: 34,
    fontWeight: '800',
    letterSpacing: 0,
  },
  subtitle: {
    color: '#59645d',
    fontSize: 16,
    lineHeight: 22,
  },
  panel: {
    gap: 8,
    borderColor: '#dfe5dd',
    borderRadius: 8,
    borderWidth: 1,
    backgroundColor: '#ffffff',
    padding: 16,
  },
  priorityPanel: {
    borderColor: '#b8d4c4',
  },
  panelLabel: {
    color: '#536158',
    fontSize: 13,
    fontWeight: '700',
    letterSpacing: 0,
    textTransform: 'uppercase',
  },
  value: {
    color: '#16231b',
    fontSize: 17,
    fontWeight: '700',
  },
  caption: {
    color: '#6b756e',
    fontSize: 14,
    lineHeight: 20,
  },
  statusHeader: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statusDot: {
    borderRadius: 8,
    height: 16,
    width: 16,
  },
  healthMessage: {
    color: '#16231b',
    fontSize: 18,
    fontWeight: '800',
  },
  detail: {
    color: '#4e5b53',
    fontSize: 14,
  },
  authDetails: {
    gap: 10,
  },
  monitoringProof: {
    backgroundColor: '#f8faf7',
    borderColor: '#dfe5dd',
    borderRadius: 8,
    borderWidth: 1,
    gap: 8,
    marginTop: 4,
    padding: 10,
  },
  roleDetails: {
    gap: 10,
  },
  roleProofStrip: {
    backgroundColor: '#f8faf7',
    borderColor: '#dfe5dd',
    borderRadius: 8,
    borderWidth: 1,
    gap: 6,
    padding: 10,
  },
  proofText: {
    color: '#25352b',
    fontSize: 14,
    fontWeight: '800',
  },
  input: {
    backgroundColor: '#fbfcfa',
    borderColor: '#cfd9d2',
    borderRadius: 8,
    borderWidth: 1,
    color: '#16231b',
    fontSize: 16,
    minHeight: 46,
    paddingHorizontal: 12,
    paddingVertical: 10,
  },
  buttonRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    marginTop: 4,
  },
  button: {
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: '#1f6f4a',
    borderRadius: 8,
    minHeight: 44,
    paddingHorizontal: 18,
    paddingVertical: 12,
  },
  disabledButton: {
    backgroundColor: '#98a39d',
  },
  secondaryButton: {
    backgroundColor: '#ffffff',
    borderColor: '#9fb2a8',
    borderWidth: 1,
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 15,
    fontWeight: '800',
  },
  secondaryButtonText: {
    color: '#1f6f4a',
    fontSize: 15,
    fontWeight: '800',
  },
  roleHomeList: {
    gap: 8,
    marginTop: 2,
  },
  roleHome: {
    borderRadius: 8,
    borderWidth: 1,
    gap: 6,
    padding: 12,
  },
  allowedRoleHome: {
    backgroundColor: '#eef8f1',
    borderColor: '#92c7aa',
  },
  deniedRoleHome: {
    backgroundColor: '#f8faf7',
    borderColor: '#dfe5dd',
  },
  roleHomeHeader: {
    alignItems: 'center',
    flexDirection: 'row',
    gap: 8,
    justifyContent: 'space-between',
  },
  roleHomeTitle: {
    color: '#16231b',
    flex: 1,
    fontSize: 15,
    fontWeight: '800',
  },
  statusPill: {
    borderRadius: 999,
    fontSize: 11,
    fontWeight: '800',
    overflow: 'hidden',
    paddingHorizontal: 9,
    paddingVertical: 4,
    textTransform: 'uppercase',
  },
  allowedPill: {
    backgroundColor: '#1f8a5b',
    color: '#ffffff',
  },
  deniedPill: {
    backgroundColor: '#e6ece8',
    color: '#536158',
  },
  deniedBox: {
    backgroundColor: '#fffaf0',
    borderColor: '#e2c470',
    borderRadius: 8,
    borderWidth: 1,
    gap: 6,
    padding: 12,
  },
  deniedTitle: {
    color: '#4b3b12',
    fontSize: 14,
    fontWeight: '800',
  },
  boundary: {
    borderColor: '#c8d7cf',
    borderRadius: 8,
    borderWidth: 1,
    gap: 8,
    padding: 16,
  },
  boundaryTitle: {
    color: '#223329',
    fontSize: 16,
    fontWeight: '800',
  },
  boundaryText: {
    color: '#4f5d55',
    fontSize: 14,
    lineHeight: 21,
  },
});
