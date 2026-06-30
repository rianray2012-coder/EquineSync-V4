import React from "react";
import { Link, Navigate, useParams } from "react-router-dom";
import {
  CalendarDays,
  ClipboardList,
  FileText,
  Heart,
  Cat,
  MessageSquare,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { resolvePostLoginPath } from "../lib/roleLanding";

const PROFILES = {
  rider: {
    eyebrow: "Rider Home",
    title: "Your riding day",
    subtitle: "Lessons, goals, trainer notes, and requests stay centered on your progress.",
    cards: [
      ["Next Lesson", "Trainer, horse, arena, and preparation notes.", CalendarDays],
      ["Riding Goals", "Current goals, milestones, and suggested focus.", Sparkles],
      ["Trainer Notes", "Recent lesson summary and practice focus.", MessageSquare],
    ],
    primary: { to: "/lessons", label: "Open lessons" },
  },
  guardian: {
    eyebrow: "Rider Overview",
    title: "Family riding hub",
    subtitle: "Minor rider progress, schedule, documents, billing, and approvals in one place.",
    cards: [
      ["Next Lesson", "Rider, trainer, horse, time, and location.", CalendarDays],
      ["Guardian Tasks", "Documents, schedule confirmations, and approvals.", ClipboardList],
      ["Billing & Documents", "Invoices, waivers, and signed forms.", FileText],
    ],
    primary: { to: "/lessons", label: "Open rider schedule" },
  },
  owner: {
    eyebrow: "My Horse",
    title: "Horse-first owner portal",
    subtitle: "Daily care status, updates, requests, health, training, and documents start here.",
    cards: [
      ["Horse Status Today", "Feed, water, turnout, stall care, medications, and exceptions.", Heart],
      ["Recent Updates", "Care notes, trainer updates, and approved media.", MessageSquare],
      ["Upcoming Care", "Vet, farrier, dental, vaccines, and bodywork.", CalendarDays],
    ],
    primary: { to: "/owner-portal", label: "Open owner portal" },
  },
};

export default function RoleHome() {
  const { profile } = useParams();
  const { user } = useAuth();
  const config = PROFILES[profile];

  if (!config) return <Navigate to={resolvePostLoginPath(user)} replace />;

  return (
    <div
      className="max-w-5xl mx-auto pb-20 lg:pb-8"
      data-testid={`role-home-${profile}`}
    >
      <header className="mb-8">
        <div className="label-eyebrow mb-3">{config.eyebrow}</div>
        <h1 className="font-display text-4xl md:text-5xl text-equine-ivory">
          {config.title}
        </h1>
        <p className="mt-3 max-w-2xl text-equine-platinum/70 text-[15px] leading-relaxed">
          {config.subtitle}
        </p>
      </header>

      <div className="grid md:grid-cols-3 gap-5">
        {config.cards.map(([title, body, Icon]) => (
          <section
            key={title}
            className="rounded-2xl bg-equine-card border border-equine-hairline p-5"
          >
            <div className="w-10 h-10 rounded-xl bg-equine-navy/70 flex items-center justify-center mb-4">
              <Icon className="w-5 h-5 text-equine-brassLight" strokeWidth={1.5} />
            </div>
            <h2 className="font-display text-2xl text-equine-ivory">{title}</h2>
            <p className="mt-2 text-[13px] leading-relaxed text-equine-platinum/65">
              {body}
            </p>
          </section>
        ))}
      </div>

      <div className="mt-7 flex flex-wrap gap-3">
        <Link
          to={config.primary.to}
          className="btn-primary inline-flex items-center gap-2"
          data-testid={`role-home-primary-${profile}`}
        >
          <Cat className="w-4 h-4" />
          {config.primary.label}
        </Link>
        <Link
          to="/messaging"
          className="btn-secondary inline-flex items-center gap-2"
          data-testid={`role-home-messages-${profile}`}
        >
          <ShieldCheck className="w-4 h-4" />
          Messages
        </Link>
      </div>
    </div>
  );
}
