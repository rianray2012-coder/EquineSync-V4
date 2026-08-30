import {
  CalendarDays,
  ClipboardList,
  FileText,
  Heart,
  MessageSquare,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { Link } from "react-router-dom";

const DASHBOARDS = {
  owner: {
    eyebrow: "Owner Home",
    title: "Horse Owner Dashboard",
    subtitle:
      "A calm home for horse updates, care visibility, requests, documents, and messages once your facility connection is active.",
    testId: "dashboard-owner",
    primary: { label: "Facility Connection Pending", to: null },
    cards: [
      ["My Horse", "Your horse profile, barn connection, and approved care visibility will appear here.", Heart],
      ["Daily Care", "Published care status appears without internal staff notes or private operating payloads.", ShieldCheck],
      ["Requests", "Care questions, scheduling needs, and barn follow-up will route through the approved request workflow.", ClipboardList],
      ["Documents", "Policies, waivers, and signed forms will appear after document workflows are connected.", FileText],
      ["Messages", "Barn-approved conversations stay attached to your account context.", MessageSquare],
    ],
  },
  guardian: {
    eyebrow: "Guardian Home",
    title: "Guardian Dashboard",
    subtitle:
      "Track the minor rider experience through barn-approved schedule, notes, documents, requests, and emergency context.",
    testId: "dashboard-guardian",
    primary: { label: "View Rider Overview", to: null },
    cards: [
      ["Rider Overview", "Minor rider details appear after your barn connects the rider profile.", Heart],
      ["Schedule", "Lesson and ride times appear here when the barn publishes them.", CalendarDays],
      ["Progress Notes", "Barn-approved progress notes and trainer summaries will appear here.", MessageSquare],
      ["Documents", "Waivers, policies, and signed forms stay in the approved document workflow.", FileText],
      ["Requests", "Use requests for barn-approved follow-up and rider support.", ClipboardList],
    ],
  },
  rider: {
    eyebrow: "Rider Home",
    title: "Rider Dashboard",
    subtitle:
      "A focused space for lessons, schedule, goals, progress notes, documents, and barn announcements as your program comes online.",
    testId: "dashboard-rider",
    primary: { label: "View Schedule", to: null },
    cards: [
      ["Schedule", "Your barn or trainer will publish lesson and ride times here.", CalendarDays],
      ["Lessons", "Lesson plans, prep notes, and trainer feedback appear after program setup.", ClipboardList],
      ["Goals", "Track approved goals and next steps without changing formal lesson enrollment.", Sparkles],
      ["Documents", "Waivers, policies, and signed forms stay in the approved document workflow.", FileText],
      ["Messages", "Keep barn-approved conversations close.", MessageSquare],
    ],
  },
};

export default function PersonalDashboard({ profile }) {
  const config = DASHBOARDS[profile] || DASHBOARDS.owner;

  return (
    <div className="max-w-6xl mx-auto pb-20 lg:pb-8" data-testid={config.testId}>
      <header className="mb-10">
        <div className="label-eyebrow mb-3">{config.eyebrow}</div>
        <h1 className="font-display text-4xl md:text-6xl text-equine-ink leading-tight">
          {config.title}
        </h1>
        <p className="mt-4 text-equine-ink/65 text-base md:text-lg max-w-3xl leading-relaxed">
          {config.subtitle}
        </p>
      </header>

      <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
        {config.cards.map(([title, body, Icon]) => (
          <section
            key={title}
            className="rounded-2xl border border-equine-cloud bg-white p-6 min-h-[180px] shadow-[0_10px_24px_-20px_rgba(35,39,52,0.28)]"
          >
            <div className="w-11 h-11 rounded-2xl bg-equine-lavender text-equine-navy flex items-center justify-center mb-5">
              <Icon className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
            <p className="mt-3 text-sm leading-relaxed text-equine-inkMuted">{body}</p>
          </section>
        ))}
      </div>

      <div className="mt-7 flex flex-wrap gap-3">
        {config.primary.to ? (
          <Link to={config.primary.to} className="btn-primary inline-flex items-center gap-2">
            <Heart className="w-4 h-4" />
            {config.primary.label}
          </Link>
        ) : (
          <button
            type="button"
            disabled
            className="btn-secondary inline-flex items-center gap-2 opacity-70 cursor-not-allowed"
          >
            <Heart className="w-4 h-4" />
            {config.primary.label}
          </button>
        )}
        <Link to="/messaging" className="btn-secondary inline-flex items-center gap-2">
          <MessageSquare className="w-4 h-4" />
          Messages
        </Link>
      </div>
    </div>
  );
}
