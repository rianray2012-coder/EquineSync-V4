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

LogBox.ignoreAllLogs(true);

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

declare const process: {
  env?: Record<string, string | undefined>;
};

const APP_ENV = process.env?.EXPO_PUBLIC_APP_ENV ?? 'native-dev';
const configuredApiBaseUrl = (process.env?.EXPO_PUBLIC_API_BASE_URL ?? 'http://localhost:8000').replace(/\/$/, '');
const API_BASE_URL =
  Platform.OS === 'android'
    ? configuredApiBaseUrl.replace('localhost', '10.0.2.2').replace('127.0.0.1', '10.0.2.2')
    : configuredApiBaseUrl;
const SESSION_KEY = 'equinesync.native.session.v1';
const SERVICE_PROVIDER_ROLES = ['service_provider', 'veterinarian', 'farrier'];
const STAFF_ROLES = ['groom', 'working_student'];

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

function titleFor(value?: string | null) {
  return labelFor(value).replace(/\b\w/g, (letter) => letter.toUpperCase());
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

export default function App() {
  const [health, setHealth] = useState<HealthState>({ status: 'checking' });
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [session, setSession] = useState<SessionState | null>(null);
  const [accountContext, setAccountContext] = useState<AccountContext | null>(null);
  const [contextStatus, setContextStatus] = useState('Waiting for signed-in session.');
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

  const statusColor = health.status === 'pass' ? '#1f8a5b' : health.status === 'fail' ? '#b42318' : '#5f6b7a';
  const canSignIn = email.trim().length > 3 && password.length > 0 && !authBusy && !restoreBusy;
  const activeContext = accountContext?.active_context ?? null;
  const roleHomes = roleHomesFor(session?.user, accountContext);
  const selectedLanding = nativeLandingFor(session?.user, accountContext);
  const allowedHome = roleHomes.find((home) => home.status === 'allowed');
  const availableContextCount = accountContext?.available_contexts?.length ?? 0;

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

          <View style={styles.panel}>
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

          <View style={styles.panel}>
            <View style={styles.statusHeader}>
              <Text style={styles.panelLabel}>Role Context</Text>
              {session && !accountContext ? <ActivityIndicator /> : <View style={[styles.statusDot, { backgroundColor: accountContext ? '#1f8a5b' : '#9aa3a0' }]} />}
            </View>

            {session ? (
              <View style={styles.roleDetails}>
                <Text style={styles.healthMessage}>{selectedLanding}</Text>
                <Text style={styles.detail}>role={labelFor(activeContext?.role ?? session.user.role)}</Text>
                <Text style={styles.detail}>account={labelFor(activeContext?.account_type)}</Text>
                <Text style={styles.detail}>membership={labelFor(activeContext?.membership_status)}</Text>
                <Text style={styles.detail}>contexts={availableContextCount}</Text>
                <Text style={styles.caption}>{contextStatus}</Text>

                <View style={styles.roleHomeList}>
                  {roleHomes.map((home) => (
                    <View key={home.key} style={[styles.roleHome, home.status === 'allowed' ? styles.allowedRoleHome : styles.deniedRoleHome]}>
                      <View style={styles.roleHomeHeader}>
                        <Text style={styles.roleHomeTitle}>{home.title}</Text>
                        <Text style={[styles.statusPill, home.status === 'allowed' ? styles.allowedPill : styles.deniedPill]}>
                          {titleFor(home.status)}
                        </Text>
                      </View>
                      <Text style={styles.caption}>{home.subtitle}</Text>
                    </View>
                  ))}
                </View>

                <View style={styles.deniedBox}>
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
  roleDetails: {
    gap: 10,
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
