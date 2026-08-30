import React, { useEffect, useMemo, useRef, useState } from "react";
import { Outlet, Navigate, useNavigate } from "react-router-dom";
import Sidebar from "./Sidebar";
import { AlertTriangle, Loader2, Menu, Search } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import NotificationsBell from "./NotificationsBell";
import { api } from "../lib/api";
import { getRoleNavigation } from "../lib/roleNavigation";

const MIN_SEARCH_LENGTH = 2;
const MAX_ENTITY_RESULTS = 6;

const normalize = (value) => String(value || "").toLowerCase();

const recordMatches = (record, fields, query) =>
  fields.some((field) => normalize(record[field]).includes(query));

const searchSources = [
  {
    key: "horses",
    label: "Horse",
    endpoint: "/horses",
    fields: ["name", "barn_name", "breed", "discipline", "stall"],
    title: (h) => h.name || "Unnamed horse",
    subtitle: (h) => [h.breed, h.discipline, h.stall].filter(Boolean).join(" · ") || "Horse record",
    to: (h) => `/horses/${h.id}`,
  },
  {
    key: "owners",
    label: "Owner",
    endpoint: "/owners",
    fields: ["full_name", "email", "phone"],
    title: (o) => o.full_name || o.email || "Owner",
    subtitle: (o) => [o.email, o.phone].filter(Boolean).join(" · ") || "Owner record",
    to: () => "/owners",
  },
  {
    key: "riders",
    label: "Rider",
    endpoint: "/riders",
    fields: ["full_name", "skill_level", "goals", "emergency_contact"],
    title: (r) => r.full_name || "Rider",
    subtitle: (r) => [r.skill_level, r.goals].filter(Boolean).join(" · ") || "Rider record",
    to: () => "/riders",
  },
];

export default function AppShell() {
  const [open, setOpen] = useState(false);
  const [searchValue, setSearchValue] = useState("");
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchState, setSearchState] = useState({ loading: false, error: false, records: [] });
  const { user } = useAuth();
  const navigate = useNavigate();
  const searchBoxRef = useRef(null);

  const navResults = useMemo(() => {
    const query = normalize(searchValue.trim());
    if (query.length < MIN_SEARCH_LENGTH) return [];
    return getRoleNavigation(user)
      .flatMap((section) => section.items || [])
      .filter((item) => normalize(item.label).includes(query))
      .slice(0, 4)
      .map((item) => ({
        key: `nav-${item.to}-${item.label}`,
        label: "Page",
        title: item.label,
        subtitle: "Open workspace page",
        to: item.to,
      }));
  }, [searchValue, user]);

  useEffect(() => {
    const query = normalize(searchValue.trim());
    if (query.length < MIN_SEARCH_LENGTH) {
      setSearchState({ loading: false, error: false, records: [] });
      return undefined;
    }

    let alive = true;
    setSearchState((current) => ({ ...current, loading: true, error: false }));

    const timer = window.setTimeout(async () => {
      const settled = await Promise.allSettled(
        searchSources.map(async (source) => {
          const response = await api.get(source.endpoint);
          return (Array.isArray(response.data) ? response.data : [])
            .filter((record) => recordMatches(record, source.fields, query))
            .slice(0, MAX_ENTITY_RESULTS)
            .map((record) => ({
              key: `${source.key}-${record.id || source.title(record)}`,
              label: source.label,
              title: source.title(record),
              subtitle: source.subtitle(record),
              to: source.to(record),
            }));
        }),
      );

      if (!alive) return;

      const availableRecords = settled
        .filter((result) => result.status === "fulfilled")
        .flatMap((result) => result.value);
      const hasFailure = settled.some((result) => result.status === "rejected");
      setSearchState({
        loading: false,
        error: hasFailure && availableRecords.length === 0,
        records: availableRecords.slice(0, MAX_ENTITY_RESULTS),
      });
    }, 180);

    return () => {
      alive = false;
      window.clearTimeout(timer);
    };
  }, [searchValue]);

  const searchQuery = searchValue.trim();
  const showSearchPanel = searchOpen && searchQuery.length >= MIN_SEARCH_LENGTH;
  const combinedResults = [...navResults, ...searchState.records];

  const closeSearch = () => {
    setSearchOpen(false);
    setSearchValue("");
  };

  const goTo = (path) => {
    navigate(path);
    closeSearch();
  };

  const handleSearchKeyDown = (event) => {
    if (event.key === "Escape") {
      closeSearch();
      return;
    }
    if (event.key === "Enter" && combinedResults[0]?.to) {
      event.preventDefault();
      goTo(combinedResults[0].to);
    }
  };

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
          <div className="relative flex items-center gap-3 flex-1 max-w-xl" ref={searchBoxRef}>
            <Search strokeWidth={1.5} className="w-4 h-4 text-equine-platinum/60" />
            <input
              value={searchValue}
              onChange={(event) => {
                setSearchValue(event.target.value);
                setSearchOpen(true);
              }}
              onFocus={() => setSearchOpen(true)}
              onKeyDown={handleSearchKeyDown}
              placeholder="Search pages, horses, owners, riders…"
              data-testid="global-search"
              role="combobox"
              aria-expanded={showSearchPanel}
              aria-controls="global-search-results"
              className="bg-transparent border-none outline-none text-[14px] text-equine-ivory placeholder:text-equine-platinum/40 flex-1 py-1"
            />
            {showSearchPanel && (
              <div
                id="global-search-results"
                data-testid="global-search-results"
                className="absolute left-0 right-0 top-full mt-3 rounded-lg border border-equine-graphite/70 bg-equine-black/95 shadow-2xl overflow-hidden z-50"
              >
                {searchState.loading && combinedResults.length === 0 ? (
                  <div data-testid="global-search-loading" className="flex items-center gap-2 px-4 py-3 text-[13px] text-equine-platinum/70">
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Searching…
                  </div>
                ) : searchState.error ? (
                  <div data-testid="global-search-unavailable" className="flex items-start gap-2 px-4 py-3 text-[13px] text-equine-clay">
                    <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
                    <span>Search could not be loaded. Try again in a moment.</span>
                  </div>
                ) : combinedResults.length === 0 ? (
                  <div data-testid="global-search-empty" className="px-4 py-3 text-[13px] text-equine-platinum/65">
                    No matches for “{searchQuery}”.
                  </div>
                ) : (
                  <div role="listbox" className="py-1">
                    {combinedResults.map((result) => (
                      <button
                        key={result.key}
                        type="button"
                        onMouseDown={(event) => event.preventDefault()}
                        onClick={() => goTo(result.to)}
                        data-testid={`global-search-result-${result.label.toLowerCase()}`}
                        className="w-full text-left px-4 py-3 hover:bg-equine-soft/70 focus:bg-equine-soft/70 focus:outline-none"
                      >
                        <div className="flex items-start justify-between gap-3">
                          <div className="min-w-0">
                            <div className="text-[14px] text-equine-ivory truncate">{result.title}</div>
                            <div className="text-[12px] text-equine-platinum/55 truncate">{result.subtitle}</div>
                          </div>
                          <span className="pill bg-equine-soft text-equine-platinum/75 border-equine-graphite/50 shrink-0">
                            {result.label}
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
          <NotificationsBell />
        </header>

        <MembershipBanners user={user} />

        <main className="flex-1 overflow-y-auto scrollbar-luxe px-5 lg:px-10 py-8 animate-fade-in">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

function MembershipBanners({ user }) {
  const banners = [];
  if (user?.role_status === "pending_review") {
    const isTrainer = user?.role === "trainer";
    banners.push({
      key: "pending",
      testId: "pending-review-banner",
      title: "Your account is awaiting verification.",
      body: isTrainer
        ? "Complete your trainer intake while EquineSync reviews your profile. Approved assigned-work context unlocks after review and workspace connection."
        : "We review trainer, barn, and service-provider accounts before expanding workspace access. You can complete your profile and explore in the meantime.",
    });
  } else if (user?.role_status === "rejected") {
    banners.push({
      key: "rejected",
      testId: "rejected-banner",
      title: "Application not approved.",
      body: user?.review_rejection_reason
        ? `Reason from our team: "${user.review_rejection_reason}". Please contact support if you'd like to discuss.`
        : "We weren't able to approve your professional account this time. Please contact support if you'd like to discuss.",
    });
  }

  // Trial countdown — only on trialing status (paid tier signup, no card yet).
  if (user?.subscription_status === "trialing" && user?.trial_expires_at) {
    const ms = new Date(user.trial_expires_at).getTime() - Date.now();
    const daysLeft = Math.max(0, Math.ceil(ms / (1000 * 60 * 60 * 24)));
    banners.push({
      key: "trial",
      testId: "trial-banner",
      title:
        daysLeft > 1
          ? `${daysLeft} days left on your free trial.`
          : daysLeft === 1
          ? "1 day left on your free trial."
          : "Your free trial has ended.",
      body: (
        <>
          {daysLeft > 0
            ? "Enjoying EquineSync? Add a payment method anytime to keep your access."
            : "Activate your membership to keep your tools and connections."}{" "}
          <a href="/dashboard?upgrade=1" className="underline text-white" data-testid="trial-banner-upgrade">
            Activate membership
          </a>
        </>
      ),
    });
  }

  if (user?.subscription_status === "cancelled") {
    banners.push({
      key: "cancelled",
      testId: "cancelled-banner",
      title: "Your membership is cancelled.",
      body: (
        <>
          You&apos;re back on the Free tier. You can resume your paid plan anytime.{" "}
          <a href="/dashboard?upgrade=1" className="underline text-white">Resume membership</a>
        </>
      ),
    });
  }

  if (!banners.length) return null;
  return (
    <div className="mx-5 lg:mx-10 mt-4 mb-2 space-y-2">
      {banners.map((b) => (
        <div
          key={b.key}
          className="bg-brand-slate border-l-4 border-brand-lilac p-4 flex items-start gap-3 text-brand-disabled text-sm tracking-wide rounded-r-md"
          data-testid={b.testId}
        >
          <span className="inline-block mt-0.5 w-2 h-2 rounded-full bg-brand-lilac" />
          <div>
            <div className="font-medium text-white mb-0.5">{b.title}</div>
            <div className="text-equine-platinum/85 text-[13px]">{b.body}</div>
          </div>
        </div>
      ))}
    </div>
  );
}
