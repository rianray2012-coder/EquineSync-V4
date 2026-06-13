import React, { useState } from "react";
import { Outlet, Navigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import { Menu, Search } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import NotificationsBell from "./NotificationsBell";

export default function AppShell() {
  const [open, setOpen] = useState(false);
  const { user } = useAuth();

  if (!user) return <Navigate to="/login" replace />;

  return (
    <div className="flex h-screen bg-equine-black text-equine-ivory">
      {/* Mobile overlay */}
      {open && (
        <div className="fixed inset-0 bg-black/60 z-30 lg:hidden" onClick={() => setOpen(false)} />
      )}
      <div className={`fixed lg:static inset-y-0 left-0 z-40 transform ${open ? "translate-x-0" : "-translate-x-full"} lg:translate-x-0 transition-transform duration-300`}>
        <Sidebar onNavigate={() => setOpen(false)} />
      </div>

      <div className="flex-1 flex flex-col min-w-0">
        <header className="glass sticky top-0 z-20 px-5 lg:px-10 py-4 flex items-center gap-4">
          <button
            className="lg:hidden p-2 -ml-2 rounded-lg hover:bg-equine-soft"
            onClick={() => setOpen(true)}
            data-testid="mobile-menu-btn"
            aria-label="Open menu"
          >
            <Menu strokeWidth={1.5} />
          </button>
          <div className="flex items-center gap-3 flex-1 max-w-xl">
            <Search strokeWidth={1.5} className="w-4 h-4 text-equine-platinum/60" />
            <input
              placeholder="Search horses, riders, vets…"
              data-testid="global-search"
              className="bg-transparent border-none outline-none text-[14px] text-equine-ivory placeholder:text-equine-platinum/40 flex-1 py-1"
            />
          </div>
          <NotificationsBell />
        </header>

        {user?.role_status === "pending_review" && (
          <div
            className="mx-5 lg:mx-10 mt-4 mb-2 bg-equine-navy border-l-4 border-equine-lilac p-4 flex items-start gap-3 text-equine-platinum text-sm font-body tracking-wide rounded-r-md"
            data-testid="pending-review-banner"
          >
            <span className="inline-block mt-0.5 w-2 h-2 rounded-full bg-equine-lilac" />
            <div>
              <div className="font-medium text-white mb-0.5">Your account is awaiting verification.</div>
              <div className="text-equine-platinum/85 text-[13px]">
                We review every trainer, barn and service provider before unlocking the
                full directory experience. You can complete your profile and explore in the meantime.
              </div>
            </div>
          </div>
        )}

        <main className="flex-1 overflow-y-auto scrollbar-luxe px-5 lg:px-10 py-8 animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
