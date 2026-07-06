import { CalendarDays, FileText, Stethoscope } from "lucide-react";

const providerCards = [
  {
    icon: CalendarDays,
    title: "Assigned Appointments",
    body: "No assigned appointments are available for this account.",
  },
  {
    icon: Stethoscope,
    title: "Shared Horses",
    body: "Horse details only appear after a facility grants provider access.",
  },
  {
    icon: FileText,
    title: "Shared Documents",
    body: "Documents shared by a facility will appear here.",
  },
];

export default function ServiceProviderDashboard() {
  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid="dashboard-service-provider">
      <div className="mb-10">
        <div className="text-[10px] uppercase tracking-[0.32em] text-equine-platinum/60 font-semibold mb-3">
          Provider Home
        </div>
        <h1 className="font-display text-4xl md:text-6xl text-equine-ink leading-tight">
          Service Provider Dashboard
        </h1>
        <p className="mt-4 text-equine-ink/65 text-base md:text-lg max-w-3xl leading-relaxed">
          Assigned appointments, shared horse context, and visit notes appear after a barn grants access.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        {providerCards.map((card) => {
          const Icon = card.icon;
          return (
            <section
              key={card.title}
              className="rounded-2xl border border-equine-cloud bg-white p-6 min-h-[180px]"
            >
              <div className="w-11 h-11 rounded-2xl bg-equine-navy/60 text-white flex items-center justify-center mb-5">
                <Icon className="w-5 h-5" strokeWidth={1.5} />
              </div>
              <h2 className="font-display text-2xl text-equine-ink">{card.title}</h2>
              <p className="mt-3 text-sm leading-relaxed text-equine-ink/55">{card.body}</p>
            </section>
          );
        })}
      </div>
    </div>
  );
}
