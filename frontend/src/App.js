import React, { useEffect, useState } from "react";
import "./App.css";
import "./index.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { Toaster } from "sonner";
import { ROLE_GROUPS, canAccessRole } from "./lib/permissions";

import AppShell from "./components/AppShell";
import Login from "./pages/Login";
import Landing from "./pages/Landing";
import Signup from "./pages/Signup";
import Enrollment from "./pages/Enrollment";
import Forbidden from "./pages/Forbidden";
import Horses from "./pages/Horses";
import HorseProfile from "./pages/HorseProfile";
import OwnerCareLedger from "./pages/OwnerCareLedger";
import Riders from "./pages/Riders";
import Owners from "./pages/Owners";
import Lessons from "./pages/Lessons";
import Training from "./pages/Training";
import Health from "./pages/Health";
import Medications from "./pages/Medications";
import Feed from "./pages/Feed";
import Billing from "./pages/Billing";
import Messaging from "./pages/Messaging";
import OwnerPortal from "./pages/OwnerPortal";
import Incidents from "./pages/Incidents";
import Inventory from "./pages/Inventory";
import Settings from "./pages/Settings";
import Onboarding from "./pages/Onboarding";
import AcceptInvite from "./pages/AcceptInvite";
import ResetPassword from "./pages/ResetPassword";
import VerifyEmail from "./pages/VerifyEmail";
import MonitoringProof from "./pages/MonitoringProof";
import Reports from "./pages/Reports";
import ReviewQueue from "./pages/ReviewQueue";
import AdminReviewQueue from "./pages/AdminReviewQueue";
import AdminBillingDashboard from "./pages/AdminBillingDashboard";
import Today from "./pages/Today";
import MyWork from "./pages/MyWork";
import Rehab from "./pages/Rehab";
import Turnout from "./pages/Turnout";
import StallMap from "./pages/StallMap";
import BarnLocations from "./pages/BarnLocations";
import ArenaSchedule from "./pages/ArenaSchedule";
import Waitlist from "./pages/Waitlist";
import PastureSchedule from "./pages/PastureSchedule";
import Equipment from "./pages/Equipment";
import HealthReminders from "./pages/HealthReminders";
import HealthDocuments from "./pages/HealthDocuments";
import HealthCareLogs from "./pages/HealthCareLogs";
import WeightTrends from "./pages/WeightTrends";
import Payments from "./pages/Payments";
import RecurringBilling from "./pages/RecurringBilling";
import Expenses from "./pages/Expenses";
import FinancialDashboard from "./pages/FinancialDashboard";
import FormsSignatures from "./pages/FormsSignatures";
import EmergencyContacts from "./pages/EmergencyContacts";
import EmergencyWorkflows from "./pages/EmergencyWorkflows";
import TrainingPlans from "./pages/TrainingPlans";
import Competitions from "./pages/Competitions";
import RideGps from "./pages/RideGps";
import PerformanceAnalytics from "./pages/PerformanceAnalytics";
import StaffScheduling from "./pages/StaffScheduling";
import HandoffReports from "./pages/HandoffReports";
import TimeClock from "./pages/TimeClock";
import AiAutomation from "./pages/AiAutomation";
import Integrations from "./pages/Integrations";
import MobileReadiness from "./pages/MobileReadiness";
import AuditLog from "./pages/AuditLog";
import SubscriptionBilling from "./pages/SubscriptionBilling";
import SubscriptionSuccess from "./pages/SubscriptionSuccess";
import RoleHome from "./pages/RoleHome";
import RoleIntake from "./pages/RoleIntake";
import { resolvePostLoginPath, SETUP_ROUTE } from "./lib/roleLanding";
import { api } from "./lib/api";
import DashboardResolver from "./features/dashboards/DashboardResolver";
import FacilityDashboard from "./features/dashboards/FacilityDashboard";
import ManagerDashboard from "./features/dashboards/ManagerDashboard";
import StaffDashboard from "./features/dashboards/StaffDashboard";
import TrainerDashboard from "./features/dashboards/TrainerDashboard";
import OwnerDashboard from "./features/dashboards/OwnerDashboard";
import GuardianDashboard from "./features/dashboards/GuardianDashboard";
import RiderDashboard from "./features/dashboards/RiderDashboard";
import ServiceProviderDashboard from "./features/dashboards/ServiceProviderDashboard";

// Admin Portal (Admin-1)
import AdminLayout from "./pages/admin/AdminLayout";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminPlaceholder from "./pages/admin/AdminPlaceholder";
import AdminUsers from "./pages/admin/AdminUsers";
import AdminApprovals from "./pages/admin/AdminApprovals";
import AdminFacilities from "./pages/admin/AdminFacilities";
import AdminHorses from "./pages/admin/AdminHorses";
import AdminSubscriptions from "./pages/admin/AdminSubscriptions";
import AdminBilling from "./pages/admin/AdminBilling";
import AdminAuditLogs from "./pages/admin/AdminAuditLogs";
import AdminSupport from "./pages/admin/AdminSupport";
import AdminAlerts from "./pages/admin/AdminAlerts";
// Admin-7B
import AdminReports from "./pages/admin/AdminReports";
import AdminIntegrations from "./pages/admin/AdminIntegrations";
import AdminSettings from "./pages/admin/AdminSettings";
import AdminLogin from "./pages/admin/AdminLogin";
import AdminMonitoringProof from "./pages/admin/AdminMonitoringProof";

const Protected = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center text-equine-platinum/60">Loading…</div>;
  if (!user) return <Navigate to="/login" replace />;
  return children;
};

const RoleProtected = ({ roles, children }) => {
  const { user } = useAuth();
  if (!canAccessRole(user, roles)) return <Forbidden />;
  return children;
};

const SetupProtected = ({ children }) => {
  const { user } = useAuth();
  const [state, setState] = useState({ loading: true, readiness: null, error: null });

  useEffect(() => {
    let alive = true;
    if (!user) {
      setState({ loading: false, readiness: null, error: null });
      return () => { alive = false; };
    }
    setState({ loading: true, readiness: null, error: null });
    api.get("/onboarding/readiness")
      .then((response) => {
        if (alive) setState({ loading: false, readiness: response.data, error: null });
      })
      .catch((error) => {
        if (alive) setState({ loading: false, readiness: null, error });
      });
    return () => { alive = false; };
  }, [user]);

  if (!user) return <Navigate to="/login" replace />;
  if (state.loading) {
    return (
      <div className="min-h-[40vh] flex items-center justify-center text-equine-platinum/60">
        Checking setup readiness…
      </div>
    );
  }
  if (state.error?.response?.status === 403) {
    return <Navigate to={resolvePostLoginPath(user)} replace />;
  }
  if (state.error) {
    return (
      <div data-testid="setup-readiness-error" className="max-w-3xl mx-auto rounded-2xl border border-equine-rose/30 bg-equine-rose/8 p-5 text-equine-ivory">
        Setup readiness could not load. Please refresh and try again.
      </div>
    );
  }
  return React.isValidElement(children)
    ? React.cloneElement(children, { setupReadiness: state.readiness })
    : children;
};

const permit = (element, roles) => <RoleProtected roles={roles}>{element}</RoleProtected>;

const ROLE_DASHBOARD_ROLES = {
  facility: ["admin", "barn_owner"],
  manager: ["barn_manager"],
  staff: ["groom", "working_student"],
  trainer: ["trainer"],
  owner: ["horse_owner"],
  guardian: ["parent"],
  rider: ["rider"],
  serviceProvider: ["service_provider", "veterinarian", "farrier"],
};

const BN17D_DIRECT_ROUTE_ROLES = {
  barnOperations: ["admin", "barn_owner", "barn_manager", "trainer", "groom", "working_student"],
  horseDirectory: ["admin", "barn_owner", "barn_manager", "trainer", "groom", "working_student"],
  facilityDirectory: ["admin", "barn_owner"],
  trainingWorkflow: ["admin", "barn_owner", "barn_manager", "trainer"],
  careWorkflow: ["admin", "barn_owner", "barn_manager", "trainer", "groom", "working_student"],
  inventoryWorkflow: ["admin", "barn_owner", "barn_manager"],
  operationalMessaging: ["admin", "barn_owner", "barn_manager", "trainer", "groom", "working_student"],
  checkoutReturn: [
    "admin",
    "barn_owner",
    "barn_manager",
    "trainer",
    "groom",
    "working_student",
    "horse_owner",
    "parent",
    "rider",
    "service_provider",
    "veterinarian",
    "farrier",
  ],
  accountSettings: [
    "admin",
    "barn_owner",
    "barn_manager",
    "trainer",
    "groom",
    "working_student",
    "horse_owner",
    "parent",
    "rider",
    "service_provider",
    "veterinarian",
    "farrier",
  ],
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Toaster position="top-right" theme="dark" />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/enroll" element={<Enrollment />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/signup/success" element={<Navigate to="/billing/success" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/accept-invite" element={<AcceptInvite />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/verify-email" element={<VerifyEmail />} />
            <Route path="/monitoring-proof" element={<MonitoringProof />} />
            <Route
              path="/owner/horses/:horseId"
              element={
                <Protected>
                  {permit(<OwnerCareLedger />, ["horse_owner", "admin", "barn_manager"])}
                </Protected>
              }
            />

            {/* Admin Portal (Admin-1) — own shell + platform_role gate.
                Namespace is /admin/portal/* (NOT /admin/*) so it never
                shadows the legacy barn-admin pages at /admin/billing
                (Phase 15.E) and /admin/review-queue (Phase 13). The
                regression test
                backend/tests/test_admin_portal_admin1.py::test_no_app_js_admin_path_collision
                enforces this invariant. */}
            <Route path="/admin/portal" element={<AdminLayout />}>
              <Route index element={<Navigate to="/admin/portal/dashboard" replace />} />
              <Route path="dashboard" element={<AdminDashboard />} />
              <Route path="users" element={<AdminUsers />} />
              <Route path="approvals" element={<AdminApprovals />} />
              <Route path="facilities" element={<AdminFacilities />} />
              <Route path="horses" element={<AdminHorses />} />
              <Route path="subscriptions" element={<AdminSubscriptions />} />
              <Route path="billing" element={<AdminBilling />} />
              <Route path="permissions" element={<AdminPlaceholder section="Permissions" description="Read-only role × capability matrix from the backend." />} />
              <Route path="support" element={<AdminSupport />} />
              <Route path="alerts" element={<AdminAlerts />} />
              <Route path="reports" element={<AdminReports />} />
              <Route path="integrations" element={<AdminIntegrations />} />
              <Route path="settings" element={<AdminSettings />} />
              <Route path="audit-logs" element={<AdminAuditLogs />} />
              <Route path="monitoring-proof" element={<AdminMonitoringProof />} />
            </Route>
            {/* Admin-7B — dedicated admin login route. Uses existing
                /api/auth/login under the hood; no separate admin auth
                backend, no admin password store. Sits OUTSIDE
                AdminLayout so the gate redirect can land here without
                a loop. */}
            <Route path="/admin/portal/login" element={<AdminLogin />} />

            <Route element={<Protected><AppShell /></Protected>}>
              <Route path="/dashboard" element={<DashboardResolver />} />
              <Route path="/dashboard/facility" element={permit(<FacilityDashboard />, ROLE_DASHBOARD_ROLES.facility)} />
              <Route path="/dashboard/manager" element={permit(<ManagerDashboard />, ROLE_DASHBOARD_ROLES.manager)} />
              <Route path="/dashboard/staff" element={permit(<StaffDashboard />, ROLE_DASHBOARD_ROLES.staff)} />
              <Route path="/dashboard/trainer" element={permit(<TrainerDashboard />, ROLE_DASHBOARD_ROLES.trainer)} />
              <Route path="/dashboard/owner" element={permit(<OwnerDashboard />, ROLE_DASHBOARD_ROLES.owner)} />
              <Route path="/dashboard/guardian" element={permit(<GuardianDashboard />, ROLE_DASHBOARD_ROLES.guardian)} />
              <Route path="/dashboard/rider" element={permit(<RiderDashboard />, ROLE_DASHBOARD_ROLES.rider)} />
              <Route path="/dashboard/service-provider" element={permit(<ServiceProviderDashboard />, ROLE_DASHBOARD_ROLES.serviceProvider)} />
              <Route path="/role-intake/:profile" element={<RoleIntake />} />
              <Route path="/role-home/:profile" element={<RoleHome />} />
              <Route path="/intake/facility-founder" element={<Navigate to="/role-intake/barn-owner" replace />} />
              <Route path="/intake/manager" element={<Navigate to="/role-intake/manager" replace />} />
              <Route path="/intake/staff" element={<Navigate to="/role-intake/staff" replace />} />
              <Route path="/intake/trainer" element={<Navigate to="/role-intake/trainer" replace />} />
              <Route path="/intake/owner" element={<Navigate to="/role-intake/owner" replace />} />
              <Route path="/intake/guardian" element={<Navigate to="/role-intake/guardian" replace />} />
              <Route path="/intake/rider" element={<Navigate to="/role-intake/rider" replace />} />
              <Route path="/today" element={permit(<Today />, BN17D_DIRECT_ROUTE_ROLES.barnOperations)} />
              <Route path="/my-work" element={permit(<MyWork />, ROLE_GROUPS.staff)} />
              <Route path="/barn-board" element={<Navigate to="/today" replace />} />
              <Route path="/setup/facility" element={<SetupProtected><Onboarding /></SetupProtected>} />
              <Route path="/onboarding" element={<Navigate to={SETUP_ROUTE} replace />} />
              <Route path="/horses" element={permit(<Horses />, BN17D_DIRECT_ROUTE_ROLES.horseDirectory)} />
              <Route path="/horses/:id" element={permit(<HorseProfile />, BN17D_DIRECT_ROUTE_ROLES.horseDirectory)} />
              <Route path="/riders" element={permit(<Riders />, BN17D_DIRECT_ROUTE_ROLES.facilityDirectory)} />
              <Route path="/owners" element={permit(<Owners />, BN17D_DIRECT_ROUTE_ROLES.facilityDirectory)} />
              <Route path="/lessons" element={permit(<Lessons />, BN17D_DIRECT_ROUTE_ROLES.trainingWorkflow)} />
              <Route path="/training" element={permit(<Training />, BN17D_DIRECT_ROUTE_ROLES.trainingWorkflow)} />
              <Route path="/health" element={permit(<Health />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/stall-rest" element={permit(<Rehab />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/rehab" element={<Navigate to="/stall-rest" replace />} />
              <Route path="/medications" element={permit(<Medications />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/turnout" element={permit(<Turnout />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/stall-map" element={permit(<StallMap />, ROLE_GROUPS.operations)} />
              <Route path="/barn-locations" element={permit(<BarnLocations />, ROLE_GROUPS.locationShare)} />
              <Route path="/arena-schedule" element={permit(<ArenaSchedule />, ROLE_GROUPS.locationShare)} />
              <Route path="/waitlist" element={permit(<Waitlist />, ROLE_GROUPS.operations)} />
              <Route path="/pasture-schedule" element={permit(<PastureSchedule />, ROLE_GROUPS.operations)} />
              <Route path="/feed" element={permit(<Feed />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/inventory" element={permit(<Inventory />, BN17D_DIRECT_ROUTE_ROLES.inventoryWorkflow)} />
              <Route path="/supply-inventory" element={<Navigate to="/inventory" replace />} />
              <Route path="/equipment" element={permit(<Equipment />, ROLE_GROUPS.operations)} />
              <Route path="/health-reminders" element={permit(<HealthReminders />, ROLE_GROUPS.care)} />
              <Route path="/health-documents" element={permit(<HealthDocuments />, ROLE_GROUPS.care)} />
              <Route path="/health-care-logs" element={permit(<HealthCareLogs />, ROLE_GROUPS.care)} />
              <Route path="/weight-trends" element={permit(<WeightTrends />, ROLE_GROUPS.care)} />
              <Route path="/billing" element={permit(<Billing />, ROLE_GROUPS.financial)} />
              <Route path="/billing/subscription" element={permit(<SubscriptionBilling />, ROLE_GROUPS.subscriptionBilling)} />
              <Route path="/billing/success" element={permit(<SubscriptionSuccess />, BN17D_DIRECT_ROUTE_ROLES.checkoutReturn)} />
              <Route path="/review-queue" element={permit(<ReviewQueue />, ROLE_GROUPS.communication)} />
              <Route path="/admin/review-queue" element={permit(<AdminReviewQueue />, ROLE_GROUPS.admin)} />
              <Route path="/admin/billing" element={permit(<AdminBillingDashboard />, ROLE_GROUPS.admin)} />
              <Route path="/payments" element={permit(<Payments />, ROLE_GROUPS.financial)} />
              <Route path="/recurring-billing" element={permit(<RecurringBilling />, ROLE_GROUPS.financial)} />
              <Route path="/expenses" element={permit(<Expenses />, ROLE_GROUPS.financial)} />
              <Route path="/financial-dashboard" element={permit(<FinancialDashboard />, ROLE_GROUPS.financial)} />
              <Route path="/incidents" element={permit(<Incidents />, BN17D_DIRECT_ROUTE_ROLES.careWorkflow)} />
              <Route path="/shows" element={permit(<Competitions />, ROLE_GROUPS.training)} />
              <Route path="/documents" element={permit(<HealthDocuments />, ROLE_GROUPS.care)} />
              <Route path="/maintenance" element={permit(<Equipment />, ROLE_GROUPS.operations)} />
              <Route path="/staff" element={permit(<StaffScheduling />, ROLE_GROUPS.admin)} />
              <Route path="/staff-tasks" element={<Navigate to="/today" replace />} />
              <Route path="/handoff-reports" element={permit(<HandoffReports />, ROLE_GROUPS.admin)} />
              <Route path="/time-clock" element={permit(<TimeClock />, ROLE_GROUPS.admin)} />
              <Route path="/messaging" element={permit(<Messaging />, BN17D_DIRECT_ROUTE_ROLES.operationalMessaging)} />
              <Route path="/group-messaging" element={<Navigate to="/messaging" replace />} />
              <Route path="/owner-updates" element={<Navigate to="/review-queue" replace />} />
              <Route path="/forms-signatures" element={permit(<FormsSignatures />, ROLE_GROUPS.communication)} />
              <Route path="/emergency-contacts" element={permit(<EmergencyContacts />, ROLE_GROUPS.communication)} />
              <Route path="/emergency-workflows" element={permit(<EmergencyWorkflows />, ROLE_GROUPS.communication)} />
              <Route path="/training-plans" element={permit(<TrainingPlans />, ROLE_GROUPS.training)} />
              <Route path="/competitions" element={permit(<Competitions />, ROLE_GROUPS.training)} />
              <Route path="/ride-gps" element={permit(<RideGps />, ROLE_GROUPS.training)} />
              <Route path="/performance-analytics" element={permit(<PerformanceAnalytics />, ROLE_GROUPS.training)} />
              <Route path="/ai-automation" element={permit(<AiAutomation />, ROLE_GROUPS.admin)} />
              <Route path="/integrations" element={permit(<Integrations />, ROLE_GROUPS.integrations)} />
              <Route path="/mobile-readiness" element={permit(<MobileReadiness />, ROLE_GROUPS.integrations)} />
              <Route path="/advanced-reports" element={<Navigate to="/reports" replace />} />
              <Route path="/audit-log" element={permit(<AuditLog />, ROLE_GROUPS.admin)} />
              <Route path="/reports" element={permit(<Reports />, ROLE_GROUPS.admin)} />
              <Route path="/owner-portal" element={permit(<OwnerPortal />, ROLE_GROUPS.ownerPortal)} />
              <Route path="/settings" element={permit(<Settings />, BN17D_DIRECT_ROUTE_ROLES.accountSettings)} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
