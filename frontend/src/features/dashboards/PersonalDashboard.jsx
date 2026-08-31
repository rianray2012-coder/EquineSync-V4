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
import TrustWorkflowPanel from "../../components/TrustWorkflowPanel";
import OwnerWellbeingPanel from "../../components/OwnerWellbeingPanel";

const DASHBOARDS = {
  owner: {
    eyebrow: "Owner Home",
    title: "Horse Owner Dashboard",
    subtitle:
      "A calm home for horse updates, care visibility, requests, documents, and messages once your facility connection is active.",
    testId: "dashboard-owner",
    primary: { label: "Owner Portal Pending", to: null },
    cards: [
      ["My Horse", "Horse profile and care context stay gated until your facility approves visibility.", Heart],
      ["Daily Care", "Approved owner-visible care status appears without staff notes or internal payloads.", ShieldCheck],
      ["Requests", "Use the approved request workflow for care questions, scheduling needs, or barn follow-up.", ClipboardList],
      ["Documents", "Document access is provider-required until approved document workflows and signature status are connected.", FileText],
      ["Messages", "Keep barn-approved conversations in one place.", MessageSquare],
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
      ["Progress Notes", "Barn-approved progress notes and trainer summaries stay hidden until your facility shares them.", MessageSquare],
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
      ["Schedule", "Lesson and ride times stay pending until your barn or trainer publishes them.", CalendarDays],
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
        <div className="md:col-span-2 xl:col-span-3">
          <TrustWorkflowPanel roleKey={profile} testid={`${config.testId}-north-star`} />
          <OwnerWellbeingPanel profile={profile} testid={`${config.testId}-wellbeing-map`} />
        </div>
        {config.cards.map(([title, body, Icon]) => (
          <section
            key={title}
            className="rounded-2xl border border-equine-cloud bg-white p-6 min-h-[180px]"
          >
            <div className="w-11 h-11 rounded-2xl bg-equine-navy/60 text-white flex items-center justify-center mb-5">
              <Icon className="w-5 h-5" strokeWidth={1.5} />
            </div>
            <h2 className="font-display text-2xl text-equine-ink">{title}</h2>
            <p className="mt-3 text-sm leading-relaxed text-equine-ink/55">{body}</p>
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
