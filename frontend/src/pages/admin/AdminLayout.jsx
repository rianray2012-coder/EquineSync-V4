import React from "react";
import { Outlet, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { isPlatformAdmin } from "../../lib/permissions";
import AdminSidebar from "./AdminSidebar";
import AdminTopbar from "./AdminTopbar";
import AdminForbidden from "./AdminForbidden";

/**
 * Admin-1 — outer shell for the /admin/* namespace.
 *
 * Gating rules (must match backend require_platform_role):
 *   - Unauthenticated → kick to /login with a redirect-back hint.
 *   - Authenticated but no platform_role → render AdminForbidden (NOT
 *     a generic 404; the user should know exactly why they were blocked
 *     so they don't poke at the route trying to break in).
 *   - Authenticated with platform_role ∈ PLATFORM_ROLES → render the
 *     shell + nested route via <Outlet/>.
 *
 * The shell intentionally does not mount any data layer here — section
 * pages call their own endpoints. This keeps the layout cheap and
 * forces every section to declare its own loading/empty/error states.
 */
export default function AdminLayout() {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div
        className="min-h-screen flex items-center justify-center bg-equinesync-frost"
        data-testid="admin-layout-loading"
      >
        <div className="text-equinesync-graphite/60 text-sm tracking-wide">
          Loading admin portal…
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <Navigate
        to={`/login?redirect=${encodeURIComponent(location.pathname)}`}
        replace
      />
    );
  }

  if (!isPlatformAdmin(user)) {
    return <AdminForbidden user={user} />;
  }

  return (
    <div
      className="min-h-screen flex bg-equinesync-frost text-equinesync-graphite"
      data-testid="admin-layout-shell"
    >
      <AdminSidebar user={user} />
      <div className="flex-1 flex flex-col min-w-0">
        <AdminTopbar user={user} />
        <main className="flex-1 overflow-y-auto p-6 md:p-8" data-testid="admin-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
