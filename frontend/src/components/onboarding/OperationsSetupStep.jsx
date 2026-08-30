import React, { useEffect, useMemo, useState } from "react";
import { api } from "../../lib/api";
import { toast } from "sonner";
import { Card } from "../Primitives";
import { CheckCircle2, Eye, Package, Plus, Trash2, Wrench } from "lucide-react";
import { Field, Select } from "./FormPrimitives";

const QUICK_MODULES = [
  {
    key: "stall-map",
    title: "Stall list",
    endpoint: "/feature-modules/stall-map",
    icon: CheckCircle2,
    fields: [
      { key: "stall_id", label: "Stall", required: true, placeholder: "Stall 12" },
      { key: "horse_name", label: "Horse", required: true, placeholder: "Horse name" },
      { key: "barn_area", label: "Barn area", placeholder: "Barn area" },
      { key: "status", label: "Status", kind: "select", opts: ["occupied", "open", "hold", "maintenance"] },
    ],
    display: (data) => `${data.stall_id || "Stall"} · ${data.horse_name || "Open"} · ${data.status || "occupied"}`,
  },
  {
    key: "pasture-schedule",
    title: "Pasture map",
    endpoint: "/feature-modules/pasture-schedule",
    icon: Eye,
    fields: [
      { key: "pasture", label: "Pasture", required: true, placeholder: "North Pasture" },
      { key: "group_name", label: "Group", placeholder: "Turnout group" },
      { key: "horse_names", label: "Horses", placeholder: "Horse names" },
      { key: "start_time", label: "Start", placeholder: "HH:MM" },
      { key: "end_time", label: "End", placeholder: "HH:MM" },
      { key: "status", label: "Status", kind: "select", opts: ["planned", "active", "weather_hold", "complete"] },
    ],
    display: (data) => `${data.pasture || "Pasture"} · ${data.group_name || "Group"} · ${data.status || "planned"}`,
  },
  {
    key: "supply-inventory",
    title: "Supplies",
    endpoint: "/feature-modules/supply-inventory",
    icon: Package,
    fields: [
      { key: "name", label: "Item", required: true, placeholder: "Timothy hay" },
      { key: "category", label: "Category", kind: "select", opts: ["feed", "hay", "bedding", "supplement", "medical", "other"] },
      { key: "quantity", label: "Quantity", type: "number" },
      { key: "unit", label: "Unit", placeholder: "bales / bags" },
      { key: "reorder_at", label: "Reorder at", type: "number" },
    ],
    display: (data) => `${data.name || "Supply"} · ${data.quantity || 0} ${data.unit || ""}`,
  },
  {
    key: "equipment",
    title: "Equipment",
    endpoint: "/feature-modules/equipment",
    icon: Wrench,
    fields: [
      { key: "name", label: "Item", required: true, placeholder: "Lesson saddle" },
      { key: "category", label: "Category", kind: "select", opts: ["tack", "equipment", "blanket", "vehicle", "tool"] },
      { key: "assigned_to", label: "Assigned to", placeholder: "School tack room" },
      { key: "condition", label: "Condition", kind: "select", opts: ["excellent", "good", "repair", "retired"] },
      { key: "location", label: "Location", placeholder: "Tack room A" },
    ],
    display: (data) => `${data.name || "Equipment"} · ${data.condition || "good"} · ${data.location || "Unassigned"}`,
  },
];

const defaultForm = (fields) =>
  fields.reduce((acc, field) => ({ ...acc, [field.key]: field.kind === "select" ? field.opts[0] : "" }), {});

export default function OperationsSetupStep({ onAnyChange }) {
  const [share, setShare] = useState(null);
  const [modules, setModules] = useState({});
  const [forms, setForms] = useState(() =>
    QUICK_MODULES.reduce((acc, mod) => ({ ...acc, [mod.key]: defaultForm(mod.fields) }), {})
  );
  const [saving, setSaving] = useState("");

  const load = () => {
    Promise.all([
      api.get("/barn-location-share").catch(() => ({ data: null })),
      ...QUICK_MODULES.map((mod) => api.get(mod.endpoint).catch(() => ({ data: { records: [] } }))),
    ]).then(([shareRes, ...moduleRows]) => {
      setShare(shareRes.data);
      setModules(
        QUICK_MODULES.reduce((acc, mod, index) => ({
          ...acc,
          [mod.key]: moduleRows[index].data?.records || [],
        }), {})
      );
    });
  };

  useEffect(() => { load(); }, []);

  const counts = useMemo(
    () => QUICK_MODULES.reduce((acc, mod) => acc + (modules[mod.key]?.length || 0), 0),
    [modules]
  );

  const updateField = (moduleKey, fieldKey, value) => {
    setForms((current) => ({
      ...current,
      [moduleKey]: { ...current[moduleKey], [fieldKey]: value },
    }));
    onAnyChange();
  };

  const createRecord = async (mod) => {
    const data = { ...forms[mod.key] };
    for (const field of mod.fields) {
      if (field.required && !data[field.key]) {
        toast.error(`${field.label} required`);
        return;
      }
      if (field.type === "number" && data[field.key] !== "") data[field.key] = Number(data[field.key]);
    }
    setSaving(mod.key);
    try {
      await api.post(`${mod.endpoint}/records`, { data });
      setForms((current) => ({ ...current, [mod.key]: defaultForm(mod.fields) }));
      load();
      toast.success("Added");
    } catch (error) {
      toast.error(error?.response?.data?.detail || "Could not add record");
    } finally {
      setSaving("");
    }
  };

  const removeRecord = async (mod, id) => {
    await api.delete(`${mod.endpoint}/records/${id}`);
    load();
  };

  const saveShare = async (enabled) => {
    const payload = {
      enabled,
      title: share?.title || "Barn Location Board",
      note: share?.note || "Current stall and pasture locations for the barn team and owners.",
    };
    setShare((current) => ({ ...(current || {}), ...payload }));
    onAnyChange();
    try {
      const result = await api.post("/barn-location-share", payload);
      setShare(result.data);
      toast.success(enabled ? "Sharing enabled" : "Sharing disabled");
    } catch {
      toast.error("Could not update sharing");
    }
  };

  return (
    <div data-testid="step-operations_setup">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5">
        <p className="text-equine-silver/70 text-[14px] md:max-w-2xl">
          Set up the operational boards that staff, trainers, and owners will use after launch.
        </p>
        <div className="rounded-xl bg-equine-soft border border-equine-graphite/40 px-4 py-3 min-w-[180px]">
          <div className="label-eyebrow">Operational records</div>
          <div className="font-display text-3xl text-equine-ivory mt-1">{counts}</div>
        </div>
      </div>

      <Card hover={false} className="!bg-equine-soft mb-5 border-equine-steel/40">
        <div className="flex flex-col lg:flex-row gap-4 lg:items-end justify-between">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
            <Field
              label="Share title"
              value={share?.title || "Barn Location Board"}
              onChange={(v) => { setShare((s) => ({ ...(s || {}), title: v })); onAnyChange(); }}
              testid="location-share-title"
            />
            <Field
              label="Share note"
              value={share?.note || ""}
              onChange={(v) => { setShare((s) => ({ ...(s || {}), note: v })); onAnyChange(); }}
              placeholder="Visible to staff, trainers, and owners"
              testid="location-share-note"
            />
          </div>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => saveShare(false)}
              data-testid="location-share-disable"
              className={`btn-secondary ${share?.enabled === false ? "!border-equine-lilac/70" : ""}`}
            >
              Private
            </button>
            <button
              type="button"
              onClick={() => saveShare(true)}
              data-testid="location-share-enable"
              className="btn-primary"
            >
              Share board
            </button>
          </div>
        </div>
        <div className="text-[12px] text-equine-platinum/60 mt-3">
          Current status: {share?.enabled ? "shared" : "private"} · {share?.share_path || "/barn-locations"}
        </div>
      </Card>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        {QUICK_MODULES.map((mod) => {
          const Icon = mod.icon;
          const rows = modules[mod.key] || [];
          return (
            <Card key={mod.key} hover={false} className="!bg-equine-card/80">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-9 h-9 rounded-xl bg-equine-steel/25 border border-equine-steel/40 flex items-center justify-center">
                  <Icon className="w-4 h-4 text-equine-lilac" />
                </div>
                <div>
                  <div className="font-display text-xl text-equine-ivory">{mod.title}</div>
                  <div className="text-[11.5px] text-equine-platinum/55">{rows.length} saved</div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                {mod.fields.map((field) => field.kind === "select" ? (
                  <Select
                    key={field.key}
                    label={field.label}
                    value={forms[mod.key]?.[field.key] || ""}
                    onChange={(v) => updateField(mod.key, field.key, v)}
                    options={field.opts.map((opt) => ({ v: opt, l: opt.replace("_", " ") }))}
                    testid={`${mod.key}-${field.key}`}
                  />
                ) : (
                  <Field
                    key={field.key}
                    label={field.label}
                    type={field.type}
                    value={forms[mod.key]?.[field.key] || ""}
                    onChange={(v) => updateField(mod.key, field.key, v)}
                    placeholder={field.placeholder}
                    testid={`${mod.key}-${field.key}`}
                  />
                ))}
              </div>

              <button
                type="button"
                onClick={() => createRecord(mod)}
                disabled={saving === mod.key}
                data-testid={`${mod.key}-quick-add`}
                className="btn-primary inline-flex items-center gap-2 mb-4"
              >
                <Plus className="w-4 h-4" /> {saving === mod.key ? "Adding..." : "Add"}
              </button>

              <div className="space-y-2">
                {rows.length === 0 && (
                  <div className="text-equine-platinum/55 text-sm py-2">No records yet.</div>
                )}
                {rows.slice(0, 4).map((row) => (
                  <div key={row.id} className="flex items-center justify-between py-2.5 px-3 rounded-lg bg-equine-soft border border-equine-graphite/40">
                    <div className="text-[13px] text-equine-silver truncate">{mod.display(row.data || {})}</div>
                    <button
                      type="button"
                      onClick={() => removeRecord(mod, row.id)}
                      data-testid={`${mod.key}-remove-${row.id}`}
                      className="text-equine-platinum/60 hover:text-equine-clay p-1.5 rounded"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
