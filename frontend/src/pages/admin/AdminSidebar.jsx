import React, { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import {
  LayoutDashboard, Users, Building2, Heart, ShieldCheck, CreditCard,
  Receipt, KeyRound, LifeBuoy, Bell, BarChart3, Plug, Settings, ScrollText,
  Menu, X, ArrowLeftRight,
} from "lucide-react";
import { canSeeAdminSection, getPlatformRole } from "../../lib/permissions";

// Section key → icon + label + route. Order matches the master spec.
const NAV = [
  { key: "dashboard",     label: "Dashboard",     path: "/admin/dashboard",     Icon: LayoutDashboard },
  { key: "users",         label: "Users",         path: "/admin/users",         Icon: Users },
  { key: "facilities",    label: "Facilities",    path: "/admin/facilities",    Icon: Building2 },
  { key: "horses",        label: "Horses",        path: "/admin/horses",        Icon: Heart },
  { key: "approvals",     label: "Approvals",     path: "/admin/approvals",     Icon: ShieldCheck },
  { key: "subscriptions", label: "Subscriptions", path: "/admin/subscriptions", Icon: CreditCard },
  { key: "billing",       label: "Billing",       path: "/admin/billing",       Icon: Receipt },
  { key: "permissions",   label: "Permissions",   path: "/admin/permissions",   Icon: KeyRound },
  { key: "support",       label: "Support",       path: "/admin/support",       Icon: LifeBuoy },
  { key: "alerts",        label: "Alerts",        path: "/admin/alerts",        Icon: Bell },
  { key: "reports",       label: "Reports",       path: "/admin/reports",       Icon: BarChart3 },
  { key: "integrations",  label: "Integrations",  path: "/admin/integrations",  Icon: Plug },
  { key: "settings",      label: "Settings",      path: "/admin/settings",      Icon: Settings },
  { key: "audit_logs",    label: "Audit Logs",    path: "/admin/audit-logs",    Icon: ScrollText },
];

const ROLE_LABEL = {
  super_admin: "Super Admin",
  platform_admin: "Platform Admin",
  support_admin: "Support Admin",
  billing_admin: "Billing Admin",
  read_only_auditor: "Read-only Auditor",
};

export default function AdminSidebar({ user }) {
  const [open, setOpen] = useState(false);
  const platformRole = getPlatformRole(user);

  const items = NAV.filter((n) => canSeeAdminSection(user, n.key));

  return (
    <>
      {/* Mobile toggle */}
      <button
        type="button"
        className="md:hidden fixed top-3 left-3 z-50 inline-flex items-center justify-center w-10 h-10 rounded-lg bg-equinesync-slate text-equinesync-frost shadow"
        onClick={() => setOpen((o) => !o)}
        data-testid="admin-sidebar-toggle"
        aria-label="Toggle admin navigation"
      >
        {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
      </button>

      {/* Backdrop on mobile when open */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-equinesync-graphite/40 md:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <aside
        data-testid="admin-sidebar"
        className={`fixed md:static top-0 left-0 h-full md:h-auto md:min-h-screen w-72 bg-equinesync-graphite text-equinesync-frost flex flex-col z-40 transform ${
          open ? "translate-x-0" : "-translate-x-full"
        } md:translate-x-0 transition-transform duration-200`}
      >
        {/* Brand block */}
        <div className="px-6 pt-7 pb-5 border-b border-white/5">
          <div className="text-[10px] tracking-[0.32em] uppercase text-equinesync-lilac">
            Equine·Sync
          </div>
          <div className="font-display text-xl tracking-tight text-equinesync-frost mt-1">
            Admin Portal
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-0.5" data-testid="admin-sidebar-nav">
          {items.map(({ key, label, path, Icon }) => (
            <NavLink
              key={key}
              to={path}
              data-testid={`admin-nav-${key}`}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13.5px] tracking-wide transition-colors ${
                  isActive
                    ? "bg-equinesync-slate text-equinesync-frost"
                    : "text-equinesync-frost/65 hover:text-equinesync-frost hover:bg-equinesync-slate/60"
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" strokeWidth={1.6} />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        {/* Footer — back to app + role pill */}
        <div className="px-3 pb-5 pt-3 border-t border-white/5 space-y-2">
          <Link
            to="/dashboard"
            data-testid="admin-back-to-app"
            className="flex items-center gap-2 text-[11.5px] tracking-wide text-equinesync-lilac hover:text-equinesync-frost px-3 py-2 rounded-lg hover:bg-equinesync-slate/40"
          >
            <ArrowLeftRight className="w-3.5 h-3.5" />
            <span>Back to Equine·Sync</span>
          </Link>
          <div
            data-testid="admin-platform-role-pill"
            className="px-3 py-2 rounded-lg bg-equinesync-slate/60 text-[11px] tracking-[0.18em] uppercase text-equinesync-lilac"
          >
            {ROLE_LABEL[platformRole] || platformRole || "—"}
          </div>
        </div>
      </aside>
    </>
  );
}
