import React from "react";
import { Search } from "lucide-react";
import { getPlatformRole } from "../../lib/permissions";

/**
 * Admin-1 — command bar / topbar.
 *
 * The search box is intentionally non-functional in Admin-1 (no global
 * search backend yet). Rendered for layout fidelity + so the testing
 * agent can confirm it exists. Admin-2 will wire it to the cross-entity
 * search endpoint.
 */
export default function AdminTopbar({ user }) {
  const platformRole = getPlatformRole(user);
  return (
    <header
      data-testid="admin-topbar"
      className="border-b border-equinesync-graphite/10 bg-white sticky top-0 z-20"
    >
      <div className="px-4 md:px-8 h-14 flex items-center gap-4">
        {/* Search command placeholder */}
        <div className="flex-1 flex items-center gap-2 max-w-xl md:ml-12 ml-12">
          <div className="relative w-full">
            <Search
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-equinesync-graphite/40"
              strokeWidth={1.6}
            />
            <input
              type="text"
              placeholder="Search"
              disabled
              data-testid="admin-topbar-search"
              className="w-full pl-9 pr-3 py-2 rounded-lg bg-equinesync-frost border border-equinesync-graphite/10 text-[13px] text-equinesync-graphite placeholder:text-equinesync-graphite/30 disabled:cursor-not-allowed disabled:opacity-60"
            />
          </div>
        </div>

        {/* Identity */}
        <div className="flex items-center gap-3" data-testid="admin-topbar-identity">
          <div className="hidden sm:flex flex-col text-right leading-tight">
            <div className="text-[13px] font-medium text-equinesync-graphite">
              {user?.full_name || user?.email || "—"}
            </div>
            <div className="text-[10.5px] tracking-[0.18em] uppercase text-equinesync-graphite/55">
              {platformRole || "no platform role"}
            </div>
          </div>
          <div
            className="w-9 h-9 rounded-full bg-equinesync-lilac/40 text-equinesync-graphite flex items-center justify-center text-[13px] font-medium"
            aria-hidden="true"
          >
            {(user?.full_name || user?.email || "?").slice(0, 1).toUpperCase()}
          </div>
        </div>
      </div>
    </header>
  );
}
