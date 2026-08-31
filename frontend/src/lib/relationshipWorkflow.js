export const OWNER_WELLBEING_SIGNALS = [
  {
    id: "care_status",
    label: "Care Status",
    proof: "Approved care updates should show what changed without exposing internal staff notes.",
    nextStep: "Connect daily digest timeline to reviewed owner-visible records.",
  },
  {
    id: "request_path",
    label: "Request Path",
    proof: "Owner questions and follow-ups should use the reviewed request workflow.",
    nextStep: "Show submitted, seen, scheduled, completed, and declined-with-note states consistently.",
  },
  {
    id: "visibility_boundary",
    label: "Visibility Boundary",
    proof: "Owner, guardian, and rider views should explain what is hidden until facility approval.",
    nextStep: "Add plain-language visibility labels beside sensitive updates and documents.",
  },
  {
    id: "first_week",
    label: "First Week",
    proof: "New owners need a short checklist that explains what to expect before the barn shares records.",
    nextStep: "Introduce a first-week onboarding checklist after facility setup rules are verified.",
  },
];

export const TRAINER_WORKFLOW_SIGNALS = [
  {
    id: "today_command",
    label: "Today Command",
    proof: "Trainer work should prioritize assigned horses, lessons, recent training, and active plans.",
    nextStep: "Promote due work, blocked items, and reviewed owner-update drafts into a single daily queue.",
  },
  {
    id: "note_lifecycle",
    label: "Note Lifecycle",
    proof: "Training notes need draft, review, owner-visible, and internal-only boundaries before sharing.",
    nextStep: "Add governed note authoring only after backend review persistence is approved.",
  },
  {
    id: "rider_context",
    label: "Rider Context",
    proof: "Rider cards should summarize goals and lesson context without exposing unrelated owner data.",
    nextStep: "Expand rider context with permission-safe progress and attendance signals.",
  },
  {
    id: "calendar_mode",
    label: "Calendar Mode",
    proof: "Trainer scheduling should stay focused on lessons and assigned work, not facility admin.",
    nextStep: "Add a trainer calendar view after schedule permissions and collision rules are verified.",
  },
];

export const RELATIONSHIP_STATUS = {
  visible_now: "Visible now",
  review_needed: "Review needed",
  gated: "Gated",
  planned: "Planned",
};
