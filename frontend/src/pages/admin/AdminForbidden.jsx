import React from "react";
import { Link } from "react-router-dom";
import { Lock, ArrowLeft } from "lucide-react";
import { Logo } from "../../components/Logo";

/**
 * Admin-1 — explicit 403 screen for the /admin/* namespace.
 *
 * Rendered when an authenticated user is missing `platform_role`. The
 * page is intentionally calm and clear so an existing `role="admin"`
 * (barn admin) user understands why they're blocked: platform-admin is
 * a SEPARATE trust boundary.
 */
export default function AdminForbidden({ user }) {
  return (
    <div
      className="min-h-screen w-full bg-equinesync-graphite text-equinesync-frost flex flex-col"
      data-testid="admin-forbidden"
    >
      <header className="px-6 md:px-12 py-6 max-w-5xl mx-auto w-full">
        <Logo onNavy />
      </header>
      <div className="flex-1 flex items-center justify-center px-6 pb-20">
        <div className="max-w-md text-center">
          <div
            className="w-14 h-14 mx-auto rounded-full bg-equinesync-slate flex items-center justify-center mb-6"
            aria-hidden="true"
          >
            <Lock className="w-6 h-6 text-equinesync-lilac" strokeWidth={1.6} />
          </div>
          <h1 className="font-display text-3xl md:text-4xl font-light text-equinesync-frost">
            Platform admin access required.
          </h1>
          <p className="mt-4 text-[14px] text-equinesync-frost/70 leading-relaxed">
            The Admin Portal is a separate trust boundary from your barn-level
            admin role.{" "}
            {user?.email ? (
              <>
                <span className="text-equinesync-lilac">{user.email}</span>{" "}
                doesn&apos;t carry a platform role yet.
              </>
            ) : (
              "Your account doesn't carry a platform role yet."
            )}{" "}
            Reach out to a Super Admin if you believe this is a mistake.
          </p>
          <Link
            to="/dashboard"
            data-testid="admin-forbidden-back"
            className="mt-8 inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-equinesync-lilac/15 text-equinesync-frost hover:bg-equinesync-lilac/25 transition-colors text-[13px] tracking-wide"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Equine·Sync
          </Link>
        </div>
      </div>
    </div>
  );
}
