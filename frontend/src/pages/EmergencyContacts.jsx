import React, { useCallback, useEffect, useMemo, useState } from "react";
import { AlertTriangle, Phone, Plus, RefreshCw, Search, ShieldAlert } from "lucide-react";
import { toast } from "sonner";
import { api } from "../lib/api";
import { Card, Empty, PageHeader, StatusPill } from "../components/Primitives";
import QuickAddSheet from "../components/QuickAddSheet";

const ADD_FIELDS = [
  { key: "person_name", label: "Name", required: true, placeholder: "Owner name" },
  { key: "relationship", label: "Relationship", placeholder: "Owner" },
  { key: "phone", label: "Phone", required: true, placeholder: "Phone number" },
  { key: "horse_name", label: "Horse", placeholder: "Horse name" },
  { key: "priority", label: "Priority", type: "number", placeholder: "Number" },
  { key: "notes", label: "Notes", kind: "textarea", rows: 3, full: true },
];

export default function EmergencyContacts() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addOpen, setAddOpen] = useState(false);
  const [query, setQuery] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const r = await api.get("/feature-modules/emergency-contacts");
      setRecords(r.data.records || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not load emergency contacts.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return records.filter((record) => {
      const data = record.data || {};
      const haystack = [data.person_name, data.relationship, data.phone, data.horse_name, data.notes]
        .filter(Boolean).join(" ").toLowerCase();
      return !q || haystack.includes(q);
    }).sort((a, b) => (Number((a.data || {}).priority) || 999) - (Number((b.data || {}).priority) || 999));
  }, [records, query]);

  const archiveRecord = async (record) => {
    try {
      await api.delete(`/feature-modules/emergency-contacts/records/${record.id}`);
      toast.success("Archived");
      load();
    } catch (err) {
      toast.error(err?.response?.data?.detail || "Could not archive contact");
    }
  };

  return (
    <div data-testid="emergency-contacts-page">
      <PageHeader
        eyebrow="Communication"
        title="Emergency Contacts"
        subtitle="Keep horse-linked emergency contacts, calling order, authorization notes, and phone numbers ready for urgent workflows."
        action={
          <div className="flex items-center gap-3">
            <button onClick={load} className="btn-secondary inline-flex items-center gap-2" data-testid="emergency-refresh">
              <RefreshCw className="w-4 h-4" /> Refresh
            </button>
            <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="emergency-add">
              <Plus className="w-4 h-4" /> Add contact
            </button>
          </div>
        }
      />

      <Card hover={false} className="mb-6 p-4">
        <div className="relative">
          <Search className="w-4 h-4 text-equine-inkSoft absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search name, horse, relationship, phone, notes…"
            className="w-full bg-equine-soft border border-equine-hairline rounded-xl pl-9 pr-3 py-2.5 text-equine-ink outline-none focus:border-equine-brass"
            data-testid="emergency-search"
          />
        </div>
      </Card>

      {loading ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">Loading emergency contacts…</div></Card>
      ) : error ? (
        <Card hover={false}>
          <div className="py-10 text-center">
            <AlertTriangle className="w-6 h-6 mx-auto text-equine-clay mb-3" />
            <div className="text-equine-ink mb-2">Emergency contacts unavailable</div>
            <div className="text-[13px] text-equine-inkMuted">{error}</div>
          </div>
        </Card>
      ) : records.length === 0 ? (
        <Empty>
          <ShieldAlert strokeWidth={1.4} className="w-7 h-7 mx-auto mb-3 text-equine-champagne" />
          <div className="font-display text-2xl text-equine-ivory mb-1">No emergency contacts</div>
          <div className="text-[13px] text-equine-platinum/60 mb-4">Add a contact, phone number, and horse association.</div>
          <button onClick={() => setAddOpen(true)} className="btn-primary inline-flex items-center gap-2" data-testid="emergency-empty-add">
            <Plus className="w-4 h-4" /> Add first contact
          </button>
        </Empty>
      ) : filtered.length === 0 ? (
        <Card hover={false}><div className="py-10 text-center text-equine-inkSoft text-[13px]">No contacts match this search.</div></Card>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map((record) => {
            const data = record.data || {};
            return (
              <Card key={record.id} hover={false} data-testid={`emergency-contact-card-${record.id}`}>
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="min-w-0">
                    <div className="font-display text-2xl text-equine-ink truncate">{data.person_name}</div>
                    <div className="text-[12.5px] text-equine-inkMuted">{data.relationship || "Contact"} · {data.horse_name || "Horse TBD"}</div>
                  </div>
                  <StatusPill tone={Number(data.priority) === 1 ? "critical" : "warning"}>priority {data.priority || "—"}</StatusPill>
                </div>
                <a href={`tel:${data.phone || ""}`} className="inline-flex items-center gap-2 text-equine-navy hover:text-equine-saddle text-[14px] mb-3">
                  <Phone className="w-4 h-4" /> {data.phone}
                </a>
                {data.notes && <div className="text-[13px] text-equine-inkMuted leading-relaxed">{data.notes}</div>}
                <div className="hairline mt-4 pt-3 flex items-center justify-between gap-3">
                  <span className="text-[11px] text-equine-inkSoft truncate">{record.id}</span>
                  <button type="button" onClick={() => archiveRecord(record)} className="text-[12px] text-equine-clay hover:text-equine-ink">
                    Archive
                  </button>
                </div>
              </Card>
            );
          })}
        </div>
      )}

      <QuickAddSheet
        open={addOpen}
        onClose={() => setAddOpen(false)}
        title="Add emergency contact"
        eyebrow="Communication"
        fields={ADD_FIELDS}
        endpoint="/feature-modules/emergency-contacts/records"
        initialValues={{ priority: 1 }}
        transform={(form) => ({ data: form })}
        submitLabel="Save contact"
        testidPrefix="emergency-add"
        onCreated={load}
      />
    </div>
  );
}
