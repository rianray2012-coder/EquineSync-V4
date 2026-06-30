import React, { useEffect, useState, useCallback } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard, Cat, UserCircle2, Users, GraduationCap, Dumbbell,
  Stethoscope, BedDouble, Pill, Trees, UtensilsCrossed, Package, Receipt,
  AlertTriangle, MessageSquare, BarChart3, Settings, ShieldAlert,
  LogOut, Crown, Sparkles, ListChecks, Map, ClipboardList, Wrench,
  FileText, HeartPulse, CalendarDays, Landmark, UsersRound, PenLine, Route, Smartphone, ShieldCheck, ClipboardCheck,
} from "lucide-react";
import { Logo } from "./Logo";
import { useAuth } from "../context/AuthContext";
import { ROLE_GROUPS } from "../lib/permissions";
import { api } from "../lib/api";

const NAV_SECTIONS = [
  {
    label: "Daily",
    items: [
      { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard, end: true },
      { to: "/today", label: "Today", icon: ListChecks },
      { to: "/my-work", label: "My Work", icon: ClipboardList, roles: ROLE_GROUPS.staff },
      { to: "/feed", label: "Feed Room", icon: UtensilsCrossed },
      { to: "/medications", label: "Medications", icon: Pill },
    ],
  },
  {
    label: "Care",
    items: [
      { to: "/horses", label: "Horses", icon: Cat },
      { to: "/health", label: "Health & Vet", icon: Stethoscope },
      { to: "/health-reminders", label: "Health Reminders", icon: HeartPulse, roles: ROLE_GROUPS.care },
      { to: "/health-documents", label: "Health Docs", icon: FileText, roles: ROLE_GROUPS.care },
      { to: "/health-care-logs", label: "Care Logs", icon: HeartPulse, roles: ROLE_GROUPS.care },
      { to: "/weight-trends", label: "Weight Trends", icon: HeartPulse, roles: ROLE_GROUPS.care },
      { to: "/stall-rest", label: "Stall Rest & Rehab", icon: BedDouble },
      { to: "/turnout", label: "Turnout & Pastures", icon: Trees },
    ],
  },
  {
    label: "Program",
    items: [
      { to: "/riders", label: "Riders", icon: UserCircle2 },
      { to: "/lessons", label: "Lessons", icon: GraduationCap },
      { to: "/training", label: "Training", icon: Dumbbell },
      { to: "/training-plans", label: "Training Plans", icon: ClipboardList, roles: ROLE_GROUPS.training },
      { to: "/shows", label: "Shows", icon: CalendarDays, roles: ROLE_GROUPS.training },
      { to: "/ride-gps", label: "Ride GPS", icon: Route, roles: ROLE_GROUPS.training },
      { to: "/performance-analytics", label: "Performance", icon: BarChart3, roles: ROLE_GROUPS.training },
    ],
  },
  {
    label: "Business",
    items: [
      { to: "/owners", label: "Owners", icon: Users },
      { to: "/owner-portal", label: "Owner Portal", icon: Crown, roles: ROLE_GROUPS.ownerPortal },
      { to: "/billing", label: "Billing", icon: Receipt, roles: ROLE_GROUPS.financial },
      { to: "/billing/subscription", label: "Subscription", icon: Sparkles, roles: ROLE_GROUPS.barnManage },
      { to: "/review-queue", label: "Review Queue", icon: ClipboardCheck, roles: ROLE_GROUPS.communication, reviewBadge: true },
      { to: "/financial-dashboard", label: "Financial Dashboard", icon: BarChart3, roles: ROLE_GROUPS.financial },
      { to: "/payments", label: "Payments", icon: Landmark, roles: ROLE_GROUPS.financial },
      { to: "/recurring-billing", label: "Recurring Billing", icon: Landmark, roles: ROLE_GROUPS.financial },
      { to: "/expenses", label: "Expenses", icon: Receipt, roles: ROLE_GROUPS.financial },
      { to: "/messaging", label: "Messaging", icon: MessageSquare },
      { to: "/group-messaging", label: "Group Messages", icon: MessageSquare, roles: ROLE_GROUPS.communication },
      { to: "/owner-updates", label: "Owner Updates", icon: PenLine, roles: ROLE_GROUPS.communication },
      { to: "/forms-signatures", label: "Forms", icon: PenLine, roles: ROLE_GROUPS.communication },
      { to: "/emergency-contacts", label: "Emergency Contacts", icon: AlertTriangle, roles: ROLE_GROUPS.communication },
      { to: "/emergency-workflows", label: "Emergency Workflows", icon: ShieldAlert, roles: ROLE_GROUPS.communication },
    ],
  },
  {
    label: "Operations",
    items: [
      { to: "/barn-locations", label: "Barn Locations", icon: Map, roles: ROLE_GROUPS.locationShare },
      { to: "/arena-schedule", label: "Arena Schedule", icon: CalendarDays, roles: ROLE_GROUPS.locationShare },
      { to: "/stall-map", label: "Stall Map", icon: Map, roles: ROLE_GROUPS.operations },
      { to: "/waitlist", label: "Waitlist", icon: ClipboardList, roles: ROLE_GROUPS.operations },
      { to: "/pasture-schedule", label: "Pasture Schedule", icon: Trees, roles: ROLE_GROUPS.operations },
      { to: "/inventory", label: "Inventory", icon: Package },
      { to: "/supply-inventory", label: "Supplies", icon: Package, roles: ROLE_GROUPS.operations },
      { to: "/equipment", label: "Equipment", icon: Wrench, roles: ROLE_GROUPS.operations },
      { to: "/staff", label: "Staff", icon: UsersRound, roles: ROLE_GROUPS.admin },
      { to: "/admin/review-queue", label: "Member Review", icon: UsersRound, roles: ROLE_GROUPS.admin, memberReviewBadge: true },
      { to: "/admin/billing", label: "Billing Admin", icon: Receipt, roles: ROLE_GROUPS.admin },
      { to: "/staff-tasks", label: "Staff Tasks", icon: ClipboardList, roles: ROLE_GROUPS.admin },
      { to: "/handoff-reports", label: "Handoff Reports", icon: FileText, roles: ROLE_GROUPS.admin },
      { to: "/time-clock", label: "Time Clock", icon: CalendarDays, roles: ROLE_GROUPS.admin },
      { to: "/incidents", label: "Incidents", icon: AlertTriangle },
    ],
  },
  {
    label: "Insights",
    items: [
      { to: "/reports", label: "Reports", icon: BarChart3, roles: ROLE_GROUPS.admin },
      { to: "/advanced-reports", label: "Advanced Reports", icon: BarChart3, roles: ROLE_GROUPS.reporting },
      { to: "/audit-log", label: "Audit Log", icon: ShieldCheck, roles: ROLE_GROUPS.admin },
      { to: "/ai-automation", label: "AI Automation", icon: Sparkles, roles: ROLE_GROUPS.admin },
      { to: "/integrations", label: "Integrations", icon: Wrench, roles: ROLE_GROUPS.integrations },
      { to: "/mobile-readiness", label: "Mobile Readiness", icon: Smartphone, roles: ROLE_GROUPS.integrations },
      { to: "/onboarding", label: "Barn Setup", icon: Sparkles, roles: ROLE_GROUPS.admin },
      { to: "/settings", label: "Settings", icon: Settings },
    ],
  },
];

const REVIEW_ROLES = ["admin", "barn_manager", "trainer"];

export default function Sidebar({ onNavigate }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const canReview = REVIEW_ROLES.includes(user?.role);
  const [pendingCount, setPendingCount] = useState(0);

  const refreshPending = useCallback(() => {
    if (!canReview) return;
    api
      .get("/owner-updates?status=pending_review")
      .then((r) => setPendingCount(Array.isArray(r.data) ? r.data.length : 0))
      .catch(() => {});
  }, [canReview]);

  useEffect(() => {
    if (!canReview) return;
    refreshPending();
    const t = setInterval(refreshPending, 60000);
    const onChange = () => refreshPending();
    window.addEventListener("owner-updates-changed", onChange);
    return () => {
      clearInterval(t);
      window.removeEventListener("owner-updates-changed", onChange);
    };
  }, [canReview, refreshPending]);

  return (
    <aside className="h-full w-[290px] bg-equine-navy border-r border-equine-navyDeep flex flex-col text-equine-platinum/90" data-testid="sidebar">
      {/* Header */}
      <div className="px-6 pt-7 pb-5 border-b border-white/[0.08]">
        <Logo onNavy />
      </div>

      {/* Nav sections */}
      <nav className="flex-1 overflow-y-auto scrollbar-luxe py-4 px-3">
        {NAV_SECTIONS.map((sec, si) => (
          <div key={sec.label} className={si > 0 ? "mt-5" : ""}>
            <div className="px-3 pb-2 text-[9.5px] tracking-[0.28em] uppercase text-equine-brassLight/70 font-semibold">{sec.label}</div>
            {sec.items.filter((item) => !item.roles || item.roles.includes(user?.role)).map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  onClick={onNavigate}
                  data-testid={`nav-${item.label.toLowerCase().replace(/[^a-z]+/g, '-')}`}
                  className={({ isActive }) =>
                    `relative group flex items-center gap-3.5 px-3.5 py-2.5 rounded-xl mb-0.5 transition-all duration-200 tap-44 ${
                      isActive
                        ? "nav-active-rail bg-gradient-to-r from-equine-brass/20 via-equine-saddle/8 to-transparent text-white border border-white/10"
                        : "text-equine-platinum/80 hover:bg-white/[0.04] hover:text-white border border-transparent"
                    }`
                  }
                >
                  {({ isActive }) => (
                    <>
                      <Icon strokeWidth={1.5} className={`w-[18px] h-[18px] transition-colors ${isActive ? "text-equine-brassLight" : "group-hover:text-equine-brassLight/90"}`} />
                      <span className="text-[13.5px] tracking-wide flex-1">{item.label}</span>
                      {item.reviewBadge && pendingCount > 0 && (
                        <span
                          data-testid="review-queue-badge"
                          className="min-w-[18px] h-[18px] px-1.5 rounded-full bg-equine-brassLight text-equine-navy text-[10.5px] font-semibold flex items-center justify-center"
                        >
                          {pendingCount > 9 ? "9+" : pendingCount}
                        </span>
                      )}
                      {isActive && <span className="w-1 h-1 rounded-full bg-equine-brassLight shadow-[0_0_10px_rgba(194,205,236,0.9)]" />}
                    </>
                  )}
                </NavLink>
              );
            })}
          </div>
        ))}
      </nav>

      {/* User & sign out */}
      <div className="px-3 pb-5 pt-4 border-t border-white/[0.08]">
        {user && (
          <div className="px-3 py-2.5 rounded-xl bg-white/[0.04] mb-2 flex items-center gap-3 border border-white/[0.08]">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-equine-brassLight to-equine-saddle flex items-center justify-center font-display text-lg text-equine-navy shadow-inner">
              {user.full_name?.[0]}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-[13px] text-white truncate">{user.full_name}</div>
              <div className="text-[9.5px] uppercase tracking-[0.22em] text-equine-brassLight/80 mt-0.5">{user.role.replace(/_/g, ' ')}</div>
            </div>
          </div>
        )}
        <button
          onClick={() => { logout(); navigate("/login"); }}
          data-testid="logout-btn"
          className="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-equine-platinum/70 hover:text-equine-clay hover:bg-white/[0.04] transition-colors tap-44"
        >
          <LogOut strokeWidth={1.5} className="w-[18px] h-[18px]" />
          <span className="text-[13px]">Sign out</span>
        </button>
      </div>
    </aside>
  );
}
