import React from "react";
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
import Forbidden from "./pages/Forbidden";
import Dashboard from "./pages/Dashboard";
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
import SupplyInventory from "./pages/SupplyInventory";
import HealthReminders from "./pages/HealthReminders";
import HealthDocuments from "./pages/HealthDocuments";
import HealthCareLogs from "./pages/HealthCareLogs";
import WeightTrends from "./pages/WeightTrends";
import Payments from "./pages/Payments";
import RecurringBilling from "./pages/RecurringBilling";
import Expenses from "./pages/Expenses";
import FinancialDashboard from "./pages/FinancialDashboard";
import GroupMessaging from "./pages/GroupMessaging";
import OwnerUpdates from "./pages/OwnerUpdates";
import FormsSignatures from "./pages/FormsSignatures";
import EmergencyContacts from "./pages/EmergencyContacts";
import EmergencyWorkflows from "./pages/EmergencyWorkflows";
import TrainingPlans from "./pages/TrainingPlans";
import Competitions from "./pages/Competitions";
import RideGps from "./pages/RideGps";
import PerformanceAnalytics from "./pages/PerformanceAnalytics";
import StaffScheduling from "./pages/StaffScheduling";
import StaffTasks from "./pages/StaffTasks";
import HandoffReports from "./pages/HandoffReports";
import TimeClock from "./pages/TimeClock";
import AiAutomation from "./pages/AiAutomation";
import Integrations from "./pages/Integrations";
import AdvancedReports from "./pages/AdvancedReports";
import MobileReadiness from "./pages/MobileReadiness";
import AuditLog from "./pages/AuditLog";
import SubscriptionBilling from "./pages/SubscriptionBilling";
import SubscriptionSuccess from "./pages/SubscriptionSuccess";

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

const permit = (element, roles) => <RoleProtected roles={roles}>{element}</RoleProtected>;

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <AuthProvider>
          <Toaster position="top-right" theme="dark" />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/signup/success" element={<Navigate to="/billing/success" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/accept-invite" element={<AcceptInvite />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/verify-email" element={<VerifyEmail />} />
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
              <Route path="permissions" element={<AdminPlaceholder section="Permissions" phase="Admin-7" description="Read-only role × capability matrix from the backend." />} />
              <Route path="support" element={<AdminSupport />} />
              <Route path="alerts" element={<AdminAlerts />} />
              <Route path="reports" element={<AdminReports />} />
              <Route path="integrations" element={<AdminIntegrations />} />
              <Route path="settings" element={<AdminSettings />} />
              <Route path="audit-logs" element={<AdminAuditLogs />} />
            </Route>
            {/* Admin-7B — dedicated admin login route. Uses existing
                /api/auth/login under the hood; no separate admin auth
                backend, no admin password store. Sits OUTSIDE
                AdminLayout so the gate redirect can land here without
                a loop. */}
            <Route path="/admin/portal/login" element={<AdminLogin />} />

            <Route element={<Protected><AppShell /></Protected>}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/today" element={<Today />} />
              <Route path="/my-work" element={permit(<MyWork />, ROLE_GROUPS.staff)} />
              <Route path="/barn-board" element={<Navigate to="/today" replace />} />
              <Route path="/onboarding" element={permit(<Onboarding />, ROLE_GROUPS.admin)} />
              <Route path="/horses" element={<Horses />} />
              <Route path="/horses/:id" element={<HorseProfile />} />
              <Route path="/riders" element={<Riders />} />
              <Route path="/owners" element={<Owners />} />
              <Route path="/lessons" element={<Lessons />} />
              <Route path="/training" element={<Training />} />
              <Route path="/health" element={<Health />} />
              <Route path="/stall-rest" element={<Rehab />} />
              <Route path="/rehab" element={<Navigate to="/stall-rest" replace />} />
              <Route path="/medications" element={<Medications />} />
              <Route path="/turnout" element={<Turnout />} />
              <Route path="/stall-map" element={permit(<StallMap />, ROLE_GROUPS.operations)} />
              <Route path="/barn-locations" element={permit(<BarnLocations />, ROLE_GROUPS.locationShare)} />
              <Route path="/arena-schedule" element={permit(<ArenaSchedule />, ROLE_GROUPS.locationShare)} />
              <Route path="/waitlist" element={permit(<Waitlist />, ROLE_GROUPS.operations)} />
              <Route path="/pasture-schedule" element={permit(<PastureSchedule />, ROLE_GROUPS.operations)} />
              <Route path="/feed" element={<Feed />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/supply-inventory" element={permit(<SupplyInventory />, ROLE_GROUPS.operations)} />
              <Route path="/equipment" element={permit(<Equipment />, ROLE_GROUPS.operations)} />
              <Route path="/health-reminders" element={permit(<HealthReminders />, ROLE_GROUPS.care)} />
              <Route path="/health-documents" element={permit(<HealthDocuments />, ROLE_GROUPS.care)} />
              <Route path="/health-care-logs" element={permit(<HealthCareLogs />, ROLE_GROUPS.care)} />
              <Route path="/weight-trends" element={permit(<WeightTrends />, ROLE_GROUPS.care)} />
              <Route path="/billing" element={permit(<Billing />, ROLE_GROUPS.financial)} />
              <Route path="/billing/subscription" element={permit(<SubscriptionBilling />, ROLE_GROUPS.barnManage)} />
              <Route path="/billing/success" element={<SubscriptionSuccess />} />
              <Route path="/review-queue" element={permit(<ReviewQueue />, ROLE_GROUPS.communication)} />
              <Route path="/admin/review-queue" element={permit(<AdminReviewQueue />, ROLE_GROUPS.admin)} />
              <Route path="/admin/billing" element={permit(<AdminBillingDashboard />, ROLE_GROUPS.admin)} />
              <Route path="/payments" element={permit(<Payments />, ROLE_GROUPS.financial)} />
              <Route path="/recurring-billing" element={permit(<RecurringBilling />, ROLE_GROUPS.financial)} />
              <Route path="/expenses" element={permit(<Expenses />, ROLE_GROUPS.financial)} />
              <Route path="/financial-dashboard" element={permit(<FinancialDashboard />, ROLE_GROUPS.financial)} />
              <Route path="/incidents" element={<Incidents />} />
              <Route path="/shows" element={permit(<Competitions />, ROLE_GROUPS.training)} />
              <Route path="/documents" element={permit(<HealthDocuments />, ROLE_GROUPS.care)} />
              <Route path="/maintenance" element={permit(<Equipment />, ROLE_GROUPS.operations)} />
              <Route path="/staff" element={permit(<StaffScheduling />, ROLE_GROUPS.admin)} />
              <Route path="/staff-tasks" element={permit(<StaffTasks />, ROLE_GROUPS.admin)} />
              <Route path="/handoff-reports" element={permit(<HandoffReports />, ROLE_GROUPS.admin)} />
              <Route path="/time-clock" element={permit(<TimeClock />, ROLE_GROUPS.admin)} />
              <Route path="/messaging" element={<Messaging />} />
              <Route path="/group-messaging" element={permit(<GroupMessaging />, ROLE_GROUPS.communication)} />
              <Route path="/owner-updates" element={permit(<OwnerUpdates />, ROLE_GROUPS.communication)} />
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
              <Route path="/advanced-reports" element={permit(<AdvancedReports />, ROLE_GROUPS.reporting)} />
              <Route path="/audit-log" element={permit(<AuditLog />, ROLE_GROUPS.admin)} />
              <Route path="/reports" element={permit(<Reports />, ROLE_GROUPS.admin)} />
              <Route path="/owner-portal" element={permit(<OwnerPortal />, ROLE_GROUPS.ownerPortal)} />
              <Route path="/settings" element={<Settings />} />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
