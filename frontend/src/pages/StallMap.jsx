import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Grip, Map as MapIcon, Plus, RefreshCw } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const GRID_ROWS = 4;
const GRID_COLS = 6;

const ADD_FIELDS = [
  { key: "stall_id", label: "Stall", required: true, placeholder: "A-01" },
  { key: "horse_name", label: "Horse", required: true, placeholder: "Valentino", full: true },
  { key: "barn_area", label: "Barn area", placeholder: "Main Barn" },
  { key: "row", label: "Row", type: "number", placeholder: "1" },
  { key: "column", label: "Column", type: "number", placeholder: "1" },
  { key: "status", label: "Status", kind: "select", opts: ["occupied", "open", "hold", "maintenance"] },
  { key: "notes", label: "Notes", kind: "textarea", full: true, rows: 3 },
];

const statusTone = {
  occupied: "success",
  open: "info",
  hold: "warning",
  maintenance: "critical",
};

const clamp = (n, min, max) => Math.max(min, Math.min(max, Number(n) || min));

const slotKey = (row, column) => `${row}:${column}`;

export default function StallMap() {
  const [module, setModule] = useState(null);
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [dragId, setDragId] = useState(null);
  const [savingId, setSavingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/stall-map");
      setModule(r.data.module);
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load stall map.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const positioned = useMemo(() => {
    const map = new Map();
    records.forEach((record) => {
      const data = record.data || {};
      const row = clamp(data.row, 1, GRID_ROWS);
      const column = clamp(data.column, 1, GRID_COLS);
      const key = slotKey(row, column);
      if (!map.has(key)) map.set(key, []);
      map.get(key).push(record);
    });
    return map;
  }, [records]);

  const stats = useMemo(() => {
    const counts = { occupied: 0, open: 0, hold: 0, maintenance: 0 };
    records.forEach((record) => {
      const status = (record.data || {}).status || "occupied";
      counts[status] = (counts[status] || 0) + 1;
    });
    return counts;
  }, [records]);

  const moveRecord = async (record, row, column) => {
    const data = record.data || {};
    const nextRow = clamp(row, 1, GRID_ROWS);
    const nextColumn = clamp(column, 1, GRID_COLS);
    if (Number(data.row) === nextRow && Number(data.column) === nextColumn) return;
    setSavingId(record.id);
    setRecords((prev) => prev.map((item) => (
      item.id === record.id
        ? { ...item, data: { ...(item.data || {}), row: nextRow, column: nextColumn } }
        : item
    )));
    try {
      await api.patch(`/feature-modules/stall-map/records/${record.id}`, {
        data: { row: nextRow, column: nextColumn },
      });
      toast.success("Stall moved");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not move stall");
      load();
    } finally {
      setSavingId(null);
    }
  };

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/stall-map/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive stall");
    }
  };

  const dropOn = (row, column) => {
    const record = records.find((item) => item.id === dragId);
    setDragId(null);
    if (record) moveRecord(record, row, column);
  };

  const cells = [];
  for (let row = 1; row <= GRID_ROWS; row += 1) {
    for (let column = 1; column <= GRID_COLS; column += 1) {
      const items = positioned.get(slotKey(row, column)) || [];
      cells.push({ row, column, items });
    }
  }

  return (
    <div data-testid="stall-map-page">
      <PageHeader
        eyebrow={module?.group || "Operations"}
        title="Stall Map"
        subtitle="Drag stalls between grid positions, track occupancy, and keep the barn layout audit-friendly without changing existing horse records."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="stall-map-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="stall-map-add">
              <Plus className="w-4 h-4" /> Add stall
            </button>
          </div>
        }
      />

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {Object.entries(stats).map(([status, count]) => (
          <Card key={status} hover={false} className="p-4">
            <div className="label-eyebrow-muted mb-2 capitalize">{status}</div>
            <div className="flex items-end justify-between gap-3">
              <div className="font-display text-4xl text-equine-ink leading-none">{count}</div>
              <StatusPill tone={statusTone[status] || "neutral"}>{status.replace(/_/g, " ")}</StatusPill>
            </div>
          </Card>
        ))}
      </div>

      {loading ? (
        <Card hover={false}>
          <div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading stall map…</div>
        </Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Stall map unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <MapIcon strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No stalls mapped yet</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add the first stall, then arrange it on the barn grid.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="stall-map-empty-add">
            <Plus className="w-4 h-4" /> Add first stall
          </button>
        </Empty>
      ) : (
        <Card hover={false} className="overflow-hidden" data-testid="stall-grid-card">
          <div className="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-6 gap-3">
            {cells.map((cell) => (
              <div
                key={slotKey(cell.row, cell.column)}
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => dropOn(cell.row, cell.column)}
                data-testid={`stall-cell-${cell.row}-${cell.column}`}
                className={`min-h-[148px] rounded-xl border border-equine-hairline bg-equine-soft/50 p-3 transition-colors ${
                  dragId ? "ring-1 ring-equine-brass/50 bg-equine-brass/10" : ""
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="text-[10px] uppercase tracking-[0.2em] text-equine-inkSoft">R{cell.row} C{cell.column}</div>
                  <div className="text-[10px] text-equine-inkSoft">{cell.items.length || "open"}</div>
                </div>
                <div className="space-y-2">
                  {cell.items.map((record) => {
                    const data = record.data || {};
                    const status = data.status || "occupied";
                    return (
                      <div
                        key={record.id}
                        draggable
                        onDragStart={() => setDragId(record.id)}
                        onDragEnd={() => setDragId(null)}
                        data-testid={`stall-card-${record.id}`}
                        className={`rounded-lg border border-equine-hairline bg-equine-card p-3 shadow-sm ${
                          savingId === record.id ? "opacity-60" : ""
                        }`}
                      >
                        <div className="flex items-start gap-2">
                          <Grip className="w-3.5 h-3.5 text-equine-inkSoft mt-1 flex-shrink-0" />
                          <div className="min-w-0 flex-1">
                            <div className="font-display text-xl text-equine-ink leading-none truncate">{data.stall_id}</div>
                            <div className="text-[12.5px] text-equine-inkMuted truncate mt-1">{data.horse_name}</div>
                            <div className="flex items-center gap-2 flex-wrap mt-2">
                              <StatusPill tone={statusTone[status] || "neutral"}>{status}</StatusPill>
                              {data.barn_area && <span className="text-[11px] text-equine-inkSoft">{data.barn_area}</span>}
                            </div>
                          </div>
                        </div>
                        <div className="mt-3 flex items-center justify-between gap-2">
                          <div className="flex items-center gap-1">
                            <MoveButton label="Move up" icon={ArrowUp} onClick={() => moveRecord(record, cell.row - 1, cell.column)} disabled={cell.row === 1} />
                            <MoveButton label="Move left" icon={ArrowLeft} onClick={() => moveRecord(record, cell.row, cell.column - 1)} disabled={cell.column === 1} />
                            <MoveButton label="Move right" icon={ArrowRight} onClick={() => moveRecord(record, cell.row, cell.column + 1)} disabled={cell.column === GRID_COLS} />
                            <MoveButton label="Move down" icon={ArrowDown} onClick={() => moveRecord(record, cell.row + 1, cell.column)} disabled={cell.row === GRID_ROWS} />
                          </div>
                          <button
                            type="button"
                            onClick={() => archiveRecord(record)}
                            className="text-[11px] text-equine-clay hover:text-equine-ink"
                            data-testid={`stall-archive-${record.id}`}
                          >
                            Archive
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add stall"
        eyebrow="Operations"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/stall-map/records"
        initialValues={{ row: 1, column: 1, status: "occupied" }}
        transform={(form) => ({ data: form })}
        submitLabel="Save stall"
        testidPrefix="stall-map-add"
        onCreated={load}
      />
    </div>
  );
}

const MoveButton = ({ label, icon: Icon, onClick, disabled }) => (
  <button
    type="button"
    onClick={onClick}
    disabled={disabled}
    aria-label={label}
    title={label}
    className="w-7 h-7 rounded-md border border-equine-hairline bg-equine-soft text-equine-inkMuted hover:text-equine-ink hover:bg-equine-card disabled:opacity-30 disabled:pointer-events-none inline-flex items-center justify-center"
  >
    <Icon className="w-3.5 h-3.5" />
  </button>
);
