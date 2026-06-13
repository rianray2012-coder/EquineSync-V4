import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Copy, Map as MapIcon, RefreshCw, Share2, Trees } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { ADMIN_ROLES } from "../lib/permissions";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";

const toneFor = {
  occupied: "success",
  open: "info",
  hold: "warning",
  maintenance: "critical",
  planned: "info",
  active: "success",
  weather_hold: "warning",
  complete: "neutral",
};

const labelFor = (value) => String(value || "").replace(/_/g, " ");

export default function BarnLocations() {
  const { user } = useAuth();
  const canPublish = ADMIN_ROLES.includes(user?.role);
  const [board, setBoard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [note, setNote] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/barn-location-share");
      setBoard(r.data);
      setNote(r.data?.share?.note || "");
    } catch (err) {
      setError(err?.response?.data?.detail || "Barn locations are not available.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const pastureByName = useMemo(() => {
    const map = new Map();
    (board?.pastures || []).forEach((row) => {
      const key = row.pasture || "Pasture TBD";
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(row);
    });
    return Array.from(map.entries());
  }, [board]);

  const publish = async (enabled) => {
    setSaving(true);
    try {
      await api.post("/barn-location-share", {
        enabled,
        title: board?.share?.title || "Barn Location Board",
        note,
      });
      toast.success(enabled ? "Barn locations shared" : "Barn location sharing paused");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not update sharing");
    } finally {
      setSaving(false);
    }
  };

  const copyLink = async () => {
    const path = board?.share?.share_path || "/barn-locations";
    const url = `${window.location.origin}${path}`;
    try {
      await navigator.clipboard.writeText(url);
      toast.success("Share link copied");
    } catch {
      toast.error("Could not copy link");
    }
  };

  return (
    <div data-testid="barn-locations-page">
      <PageHeader
        eyebrow="Operations"
        title={board?.share?.title || "Barn Location Board"}
        subtitle="Read-only stall list and pasture map for everyone approved to see where horses are located."
        action={
          <div className="flex items-center gap-3">
            <button onClick={copyLink} className="btn-secondary inline-flex items-center gap-2" data-testid="barn-locations-copy">
              <Copy className="w-4 h-4" /> Copy link
            </button>
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="barn-locations-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
          </div>
        }
      />

      {canPublish && (
        <Card hover={false} className="mb-6 border-equine-brass/30 bg-equine-brass/5" data-testid="barn-locations-share-controls">
          <div className="flex flex-col xl:flex-row xl:items-end gap-4">
            <div className="flex-1">
              <div className="label-eyebrow-muted mb-1.5">Owner note</div>
              <textarea
                value={note}
                onChange={(event) => setNote(event.target.value)}
                rows={2}
                placeholder="Note: Please check this board before turning horses out."
                className="w-full bg-white border border-equine-cloud rounded-lg px-3 py-2.5 text-[13px] text-equine-ink outline-none focus:border-equine-brass"
                data-testid="barn-locations-note"
              />
            </div>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => publish(true)}
                disabled={saving}
                className="btn-primary inline-flex items-center gap-2 disabled:opacity-60"
                data-testid="barn-locations-publish"
              >
                <Share2 className="w-4 h-4" /> Publish
              </button>
              <button
                type="button"
                onClick={() => publish(false)}
                disabled={saving}
                className="btn-secondary disabled:opacity-60"
                data-testid="barn-locations-pause"
              >
                Pause sharing
              </button>
            </div>
          </div>
        </Card>
      )}

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading barn locations...</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Location board unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : !board ? (
        <Empty>
          <MapIcon strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No location board yet</div>
          <div className="text-[13px] text-equine-platinum/60">A barn owner can publish the shared location board here.</div>
        </Empty>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <Metric label="Sharing" value={board.share?.enabled ? "Live" : "Paused"} tone={board.share?.enabled ? "success" : "warning"} />
            <Metric label="Horses located" value={board.stats?.horses_located || 0} />
            <Metric label="Stalls" value={board.stats?.stalls || 0} />
            <Metric label="Pasture blocks" value={board.stats?.pasture_blocks || 0} />
          </div>

          {board.share?.note && (
            <Card hover={false} className="mb-6">
              <div className="label-eyebrow-muted mb-2">Barn note</div>
              <div className="text-[14px] text-equine-inkMuted leading-relaxed">{board.share.note}</div>
            </Card>
          )}

          <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
            <Card hover={false} className="xl:col-span-2" data-testid="barn-location-horse-list">
              <div className="label-eyebrow mb-2">Horse locations</div>
              <h2 className="font-display text-3xl text-equine-ink mb-5">Current list</h2>
              <div className="space-y-3">
                {(board.horse_locations || []).map((row) => (
                  <div key={`${row.horse_name}-${row.location_type}`} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="font-display text-2xl text-equine-ink">{row.horse_name}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">
                          {row.location_type === "pasture"
                            ? `${row.pasture || "Pasture"} · ${row.group_name || "Group TBD"}`
                            : `${row.stall_id || "Stall TBD"} · ${row.barn_area || "Barn area TBD"}`}
                        </div>
                      </div>
                      <StatusPill tone={toneFor[row.status] || "info"}>{labelFor(row.status)}</StatusPill>
                    </div>
                    {row.location_type === "pasture" && (
                      <div className="text-[12px] text-equine-inkSoft mt-2">{row.start_time || "—"} to {row.end_time || "—"}</div>
                    )}
                  </div>
                ))}
                {(board.horse_locations || []).length === 0 && <SoftEmpty text="No horse locations shared yet." />}
              </div>
            </Card>

            <Card hover={false} className="xl:col-span-3" data-testid="barn-location-stall-list">
              <div className="label-eyebrow mb-2">Stall list</div>
              <h2 className="font-display text-3xl text-equine-ink mb-5">Barn layout</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                {(board.stalls || []).map((row) => (
                  <div key={row.id} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="font-display text-2xl text-equine-ink">{row.stall_id || "Stall TBD"}</div>
                        <div className="text-[12.5px] text-equine-inkMuted">{row.horse_name || "Open"} · {row.barn_area || "Barn area TBD"}</div>
                      </div>
                      <StatusPill tone={toneFor[row.status] || "neutral"}>{labelFor(row.status)}</StatusPill>
                    </div>
                    <div className="text-[12px] text-equine-inkSoft mt-2">Grid R{row.row || "—"} C{row.column || "—"}</div>
                  </div>
                ))}
                {(board.stalls || []).length === 0 && <SoftEmpty text="No stalls shared yet." />}
              </div>
            </Card>
          </div>

          <Card hover={false} className="mt-6" data-testid="barn-location-pasture-map">
            <div className="flex items-center justify-between gap-4 mb-5">
              <div>
                <div className="label-eyebrow mb-2">Pasture map</div>
                <h2 className="font-display text-3xl text-equine-ink">Turnout by pasture</h2>
              </div>
              <Trees className="w-5 h-5 text-equine-brass" />
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
              {pastureByName.map(([pasture, rows]) => (
                <div key={pasture} className="rounded-xl border border-equine-hairline bg-equine-soft/55 p-4">
                  <div className="font-display text-2xl text-equine-ink mb-3">{pasture}</div>
                  <div className="space-y-3">
                    {rows.map((row) => (
                      <div key={row.id} className="rounded-lg border border-equine-hairline bg-white/55 p-3">
                        <div className="flex items-start justify-between gap-3 mb-1">
                          <div className="text-[13px] text-equine-ink">{row.group_name || "Group TBD"}</div>
                          <StatusPill tone={toneFor[row.status] || "info"}>{labelFor(row.status)}</StatusPill>
                        </div>
                        <div className="text-[12px] text-equine-inkMuted">{row.start_time || "—"} to {row.end_time || "—"}</div>
                        <div className="text-[12.5px] text-equine-ink mt-2">{row.horse_names?.join(", ") || "No horses listed"}</div>
                        {row.weather_rule && <div className="text-[11.5px] text-equine-inkSoft mt-2">{row.weather_rule}</div>}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
              {pastureByName.length === 0 && <SoftEmpty text="No pasture blocks shared yet." />}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}

const Metric = ({ label, value, tone }) => (
  <div className="rounded-lg border border-equine-cloud bg-white/70 p-4">
    <div className="label-eyebrow-muted mb-2">{label}</div>
    <div className="flex items-end justify-between gap-3">
      <div className="font-display text-4xl text-equine-ink leading-none">{value}</div>
      {tone && <StatusPill tone={tone}>{String(value).toLowerCase()}</StatusPill>}
    </div>
  </div>
);

const SoftEmpty = ({ text }) => (
  <div className="rounded-xl border border-dashed border-equine-cloud bg-white/45 py-8 text-center text-[13px] text-equine-inkMuted">
    {text}
  </div>
);
