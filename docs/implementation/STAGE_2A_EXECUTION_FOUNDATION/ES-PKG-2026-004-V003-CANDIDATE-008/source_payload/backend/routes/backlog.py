"""routes/backlog.py — additive feature-backlog foundations.

The goal of this module is not to finish every advanced workflow in one pass.
It creates stable, audit-friendly collections, RBAC gates, module metadata,
CRUD shells, and integration readiness contracts so UI and deeper services can grow
without disturbing existing Emergent-built routes.
"""
from __future__ import annotations

import re
from html import escape
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.permissions import ADMIN_ROLES, STAFF_ROLES, can, require_permission
from storage import build_key, get_provider, validate_upload


DEFAULT_BARN_ID = "primary"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class FeatureRecordIn(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)


class CustomReportIn(BaseModel):
    name: str
    module_keys: List[str] = Field(default_factory=list)
    filters: Dict[str, Any] = Field(default_factory=dict)


class ReportExportIn(CustomReportIn):
    format: str = "xlsx"


class PayrollExportIn(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    staff_user_id: Optional[str] = None
    staff_name: Optional[str] = None


class CalendarExportIn(BaseModel):
    sources: List[str] = Field(default_factory=list)


class QuickBooksExportIn(BaseModel):
    include_expenses: bool = True
    include_invoices: bool = True


class PushPreviewIn(BaseModel):
    include_group_messages: bool = True
    include_owner_updates: bool = True


class DocumentScanUploadIn(BaseModel):
    filename: str
    mime_type: str
    byte_size: int
    document_type: str = "other"
    horse_name: Optional[str] = None
    linked_module: Optional[str] = "document-scans"
    notes: Optional[str] = None


class BarnLocationShareIn(BaseModel):
    enabled: bool = True
    title: str = "Barn Location Board"
    note: Optional[str] = None


class ArenaScheduleShareIn(BaseModel):
    enabled: bool = True
    title: str = "Arena Schedule"
    note: Optional[str] = None


def _module(
    key: str,
    group: str,
    label: str,
    collection: str,
    read: str,
    write: str,
    fields: List[Dict[str, Any]],
    features: List[str],
    placeholder: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "key": key,
        "group": group,
        "label": label,
        "collection": collection,
        "read_permission": read,
        "write_permission": write,
        "fields": fields,
        "features": features,
        "placeholder": placeholder,
    }


TEXT = "text"
DATE = "date"
NUMBER = "number"
SELECT = "select"
TEXTAREA = "textarea"


MODULES: Dict[str, Dict[str, Any]] = {
    "stall-map": _module(
        "stall-map", "Operations", "Stall Map", "stall_assignments",
        "operations:read", "operations:write",
        [
            {"key": "stall_id", "label": "Stall", "type": TEXT, "required": True},
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "barn_area", "label": "Barn area", "type": TEXT},
            {"key": "row", "label": "Row", "type": NUMBER},
            {"key": "column", "label": "Column", "type": NUMBER},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["occupied", "open", "hold", "maintenance"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Drag-and-drop ready row/column positions", "Occupancy status", "Barn area grouping"],
    ),
    "waitlist": _module(
        "waitlist", "Operations", "Waitlist", "waitlist_entries",
        "operations:read", "operations:write",
        [
            {"key": "client_name", "label": "Client", "type": TEXT, "required": True},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "service_type", "label": "Service", "type": SELECT, "options": ["board", "training", "lesson", "rehab"]},
            {"key": "priority", "label": "Priority", "type": SELECT, "options": ["low", "normal", "high"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["new", "contacted", "offered", "scheduled", "closed"]},
            {"key": "target_date", "label": "Target date", "type": DATE},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Priority queue", "Service category", "Move-in target date"],
    ),
    "pasture-schedule": _module(
        "pasture-schedule", "Operations", "Pasture Scheduling", "pasture_schedules",
        "operations:read", "operations:write",
        [
            {"key": "pasture", "label": "Pasture", "type": TEXT, "required": True},
            {"key": "group_name", "label": "Group", "type": TEXT},
            {"key": "horse_names", "label": "Horses", "type": TEXTAREA},
            {"key": "start_time", "label": "Start", "type": TEXT},
            {"key": "end_time", "label": "End", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["planned", "active", "weather_hold", "complete"]},
            {"key": "weather_rule", "label": "Weather rule", "type": TEXTAREA},
        ],
        ["Turnout block planning", "Group scheduling", "Weather-rule notes"],
    ),
    "arena-schedule": _module(
        "arena-schedule", "Operations", "Arena Schedule", "arena_schedule_blocks",
        "operations:read", "barn:manage",
        [
            {"key": "arena_name", "label": "Arena", "type": TEXT, "required": True},
            {"key": "title", "label": "Title", "type": TEXT, "required": True},
            {"key": "date", "label": "Date", "type": DATE, "required": True},
            {"key": "start_time", "label": "Start", "type": TEXT},
            {"key": "end_time", "label": "End", "type": TEXT},
            {"key": "rental_duration", "label": "Duration", "type": SELECT, "options": ["30_min", "1_hour", "half_day", "full_day"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["open", "requested", "reserved", "lesson", "maintenance", "private"]},
            {"key": "visibility", "label": "Visibility", "type": SELECT, "options": ["shared_with_owners", "staff_only"]},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "owner_name", "label": "Owner", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Owner-visible arena availability", "Rental duration tracking", "Approved request booking"],
    ),
    "equipment": _module(
        "equipment", "Operations", "Equipment & Tack", "equipment_items",
        "operations:read", "operations:write",
        [
            {"key": "name", "label": "Item", "type": TEXT, "required": True},
            {"key": "category", "label": "Category", "type": SELECT, "options": ["tack", "equipment", "blanket", "vehicle", "tool"]},
            {"key": "assigned_to", "label": "Assigned to", "type": TEXT},
            {"key": "condition", "label": "Condition", "type": SELECT, "options": ["excellent", "good", "repair", "retired"]},
            {"key": "location", "label": "Location", "type": TEXT},
            {"key": "serial_number", "label": "Serial / tag", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Assignment tracking", "Condition status", "Tag/serial capture"],
    ),
    "supply-inventory": _module(
        "supply-inventory", "Operations", "Supply Inventory", "supply_inventory_items",
        "operations:read", "operations:write",
        [
            {"key": "name", "label": "Item", "type": TEXT, "required": True},
            {"key": "category", "label": "Category", "type": SELECT, "options": ["feed", "hay", "bedding", "supplement", "medical", "other"]},
            {"key": "quantity", "label": "Quantity", "type": NUMBER},
            {"key": "unit", "label": "Unit", "type": TEXT},
            {"key": "reorder_at", "label": "Reorder at", "type": NUMBER},
            {"key": "vendor", "label": "Vendor", "type": TEXT},
            {"key": "location", "label": "Location", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["in_stock", "low", "ordered", "out"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Feed inventory tracking", "Hay/bedding/supplement stock", "Reorder workflow"],
    ),
    "health-reminders": _module(
        "health-reminders", "Health", "Vaccines & Coggins", "health_reminders",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "reminder_type", "label": "Type", "type": SELECT, "options": ["vaccine", "coggins", "dental", "deworming"]},
            {"key": "due_date", "label": "Due date", "type": DATE, "required": True},
            {"key": "provider", "label": "Provider", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["scheduled", "due", "complete", "expired"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Vaccination reminders", "Coggins expiration tracking", "Health due-date queue"],
    ),
    "health-documents": _module(
        "health-documents", "Health", "Health Documents", "health_documents",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "document_type", "label": "Type", "type": SELECT, "options": ["coggins", "vaccine", "vet_report", "insurance", "other"]},
            {"key": "document_url", "label": "File URL", "type": TEXT},
            {"key": "shared_with", "label": "Shared with", "type": TEXT},
            {"key": "expires_at", "label": "Expires", "type": DATE},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Storage-provider ready", "Owner sharing metadata", "Expiration tracking"],
        "Uploads use the existing storage abstraction when credentials are available.",
    ),
    "farrier-history": _module(
        "farrier-history", "Health", "Farrier History", "farrier_history",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "farrier_name", "label": "Farrier", "type": TEXT},
            {"key": "scheduled_at", "label": "Scheduled", "type": TEXT},
            {"key": "completed_at", "label": "Completed", "type": TEXT},
            {"key": "service_type", "label": "Service", "type": SELECT, "options": ["trim", "front_shoes", "full_set", "reset", "therapeutic"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["scheduled", "complete", "missed", "follow_up"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Farrier scheduling", "Service history", "Follow-up tracking"],
    ),
    "medication-logs": _module(
        "medication-logs", "Health", "Medication Administration Logs", "medication_administration_logs",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "medication_name", "label": "Medication", "type": TEXT, "required": True},
            {"key": "dosage", "label": "Dosage", "type": TEXT},
            {"key": "administered_at", "label": "Administered", "type": TEXT},
            {"key": "administered_by", "label": "Administered by", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["scheduled", "administered", "missed", "held"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Medication administration logs", "Missed/held medication tracking", "Care audit trail"],
    ),
    "injury-tracking": _module(
        "injury-tracking", "Health", "Injury & Lameness Tracking", "injury_lameness_cases",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "case_title", "label": "Case", "type": TEXT, "required": True},
            {"key": "severity", "label": "Severity", "type": SELECT, "options": ["watch", "mild", "moderate", "urgent"]},
            {"key": "observed_at", "label": "Observed", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["open", "monitoring", "vet_called", "resolved"]},
            {"key": "care_plan", "label": "Care plan", "type": TEXTAREA},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Injury tracking", "Lameness observations", "Health-risk alert input"],
    ),
    "weight-trends": _module(
        "weight-trends", "Health", "Weight & Body Condition", "weight_condition_entries",
        "health:read", "health:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "recorded_at", "label": "Date", "type": DATE, "required": True},
            {"key": "weight_lbs", "label": "Weight lbs", "type": NUMBER},
            {"key": "body_condition", "label": "Body condition", "type": NUMBER},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Trend-ready entries", "Body-condition scoring", "Health analytics input"],
    ),
    "payments": _module(
        "payments", "Financial", "Payments & Auto-Pay", "payment_profiles",
        "financial:read", "financial:write",
        [
            {"key": "owner_name", "label": "Owner", "type": TEXT, "required": True},
            {"key": "provider", "label": "Provider", "type": SELECT, "options": ["stripe", "manual"]},
            {"key": "autopay_status", "label": "Auto-pay", "type": SELECT, "options": ["not_enrolled", "invited", "enrolled", "paused"]},
            {"key": "customer_ref", "label": "Customer ref", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Stripe-ready provider refs", "Auto-pay enrollment structure", "Manual fallback"],
        "No payment credentials are stored here; live checkout is a later Stripe service integration.",
    ),
    "recurring-billing": _module(
        "recurring-billing", "Financial", "Recurring Billing", "recurring_billing_rules",
        "financial:read", "financial:write",
        [
            {"key": "name", "label": "Rule", "type": TEXT, "required": True},
            {"key": "owner_name", "label": "Owner", "type": TEXT},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "amount", "label": "Amount", "type": NUMBER, "required": True},
            {"key": "frequency", "label": "Frequency", "type": SELECT, "options": ["monthly", "weekly", "per_lesson", "custom"]},
            {"key": "next_run_date", "label": "Next run", "type": DATE},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["active", "paused", "draft"]},
        ],
        ["Recurring charge rules", "Invoice automation-ready", "Owner/horse association"],
    ),
    "expenses": _module(
        "expenses", "Financial", "Expenses", "expenses",
        "financial:read", "financial:write",
        [
            {"key": "vendor", "label": "Vendor", "type": TEXT, "required": True},
            {"key": "category", "label": "Category", "type": SELECT, "options": ["feed", "bedding", "labor", "vet", "farrier", "maintenance", "show", "other"]},
            {"key": "amount", "label": "Amount", "type": NUMBER, "required": True},
            {"key": "spent_at", "label": "Date", "type": DATE},
            {"key": "receipt_url", "label": "Receipt URL", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Expense capture", "Receipt/document reference", "P/L dashboard input"],
    ),
    "group-messaging": _module(
        "group-messaging", "Communication", "Group Messaging", "group_messages",
        "communication:read", "communication:write",
        [
            {"key": "subject", "label": "Subject", "type": TEXT, "required": True},
            {"key": "audience", "label": "Audience", "type": SELECT, "options": ["all_staff", "owners", "trainers", "custom"]},
            {"key": "body", "label": "Message", "type": TEXTAREA, "required": True},
            {"key": "channel", "label": "Channel", "type": SELECT, "options": ["in_app", "email", "push_ready"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["draft", "queued", "sent"]},
            {"key": "recipient_user_ids", "label": "Recipient user IDs", "type": TEXT, "placeholder": "Comma-separated user IDs for custom or guardian-visible messages"},
        ],
        ["Group announcements", "Push-ready channel metadata", "Owner/staff audience targeting"],
    ),
    "owner-updates": _module(
        "owner-updates", "Communication", "Photo & Video Updates", "owner_media_updates",
        "communication:read", "communication:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "owner_name", "label": "Owner", "type": TEXT},
            {"key": "caption", "label": "Caption", "type": TEXTAREA},
            {"key": "media_url", "label": "Media URL", "type": TEXT},
            {"key": "visibility", "label": "Visibility", "type": SELECT, "options": ["owner_only", "staff", "barn"]},
        ],
        ["Owner portal update stream", "Photo/video storage reference", "Visibility controls"],
    ),
    "forms-signatures": _module(
        "forms-signatures", "Communication", "Forms & Signatures", "digital_forms",
        "communication:read", "communication:write",
        [
            {"key": "form_name", "label": "Form", "type": TEXT, "required": True},
            {"key": "recipient_name", "label": "Recipient", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["draft", "sent", "signed", "expired"]},
            {"key": "signature_provider", "label": "Provider", "type": SELECT, "options": ["internal", "docusign_ready"]},
            {"key": "signed_at", "label": "Signed at", "type": DATE},
        ],
        ["Digital form tracking", "Signature-provider readiness", "Status workflow"],
    ),
    "emergency-contacts": _module(
        "emergency-contacts", "Communication", "Emergency Contacts", "emergency_contacts",
        "communication:read", "communication:write",
        [
            {"key": "person_name", "label": "Name", "type": TEXT, "required": True},
            {"key": "relationship", "label": "Relationship", "type": TEXT},
            {"key": "phone", "label": "Phone", "type": TEXT, "required": True},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "priority", "label": "Priority", "type": NUMBER},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Emergency workflow directory", "Horse/contact association", "Priority ordering"],
    ),
    "emergency-workflows": _module(
        "emergency-workflows", "Communication", "Emergency Workflows", "emergency_workflows",
        "communication:read", "communication:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "emergency_type", "label": "Type", "type": SELECT, "options": ["colic", "injury", "cast", "transport", "weather", "other"]},
            {"key": "primary_contact", "label": "Primary contact", "type": TEXT},
            {"key": "vet_status", "label": "Vet", "type": SELECT, "options": ["not_called", "called", "en_route", "on_site", "complete"]},
            {"key": "owner_status", "label": "Owner", "type": SELECT, "options": ["not_contacted", "left_message", "confirmed", "authorized"]},
            {"key": "workflow_status", "label": "Status", "type": SELECT, "options": ["open", "stabilizing", "resolved", "closed"]},
            {"key": "started_at", "label": "Started", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Emergency contact workflow", "Vet/owner status", "Resolution handoff notes"],
    ),
    "training-plans": _module(
        "training-plans", "Training", "Training Plans & Goals", "training_plans",
        "training:read", "training:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "trainer_name", "label": "Trainer", "type": TEXT},
            {"key": "goal", "label": "Goal", "type": TEXT, "required": True},
            {"key": "plan_notes", "label": "Plan", "type": TEXTAREA},
            {"key": "target_date", "label": "Target date", "type": DATE},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["planned", "active", "achieved", "paused"]},
        ],
        ["Training plans", "Trainer assignment workflow", "Goal tracking"],
    ),
    "competitions": _module(
        "competitions", "Training", "Competitions & Show Entries", "show_entries",
        "training:read", "training:write",
        [
            {"key": "show_name", "label": "Show", "type": TEXT, "required": True},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "rider_name", "label": "Rider", "type": TEXT},
            {"key": "start_date", "label": "Start", "type": DATE},
            {"key": "entry_status", "label": "Entry", "type": SELECT, "options": ["planning", "submitted", "accepted", "scratched"]},
            {"key": "results", "label": "Results", "type": TEXTAREA},
        ],
        ["Competition calendar", "Show-entry tracking", "Performance analytics input"],
    ),
    "ride-gps": _module(
        "ride-gps", "Mobile & Integrations", "Ride GPS", "ride_gps_tracks",
        "training:read", "training:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "rider_name", "label": "Rider", "type": TEXT},
            {"key": "started_at", "label": "Started", "type": TEXT},
            {"key": "distance_miles", "label": "Distance", "type": NUMBER},
            {"key": "duration_minutes", "label": "Minutes", "type": NUMBER},
            {"key": "track_url", "label": "Track URL", "type": TEXT},
        ],
        ["GPS ride structure", "Wearable-ready metrics", "Offline sync input"],
        "Native GPS capture is deferred to mobile app wiring.",
    ),
    "staff-scheduling": _module(
        "staff-scheduling", "Staff", "Staff Scheduling", "staff_shifts",
        "staff:read", "staff:write",
        [
            {"key": "staff_name", "label": "Staff", "type": TEXT, "required": True},
            {"key": "role", "label": "Role", "type": TEXT},
            {"key": "shift_start", "label": "Start", "type": TEXT, "required": True},
            {"key": "shift_end", "label": "End", "type": TEXT},
            {"key": "area", "label": "Area", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Staff scheduling", "Shift notes", "Payroll export source"],
    ),
    "staff-tasks": _module(
        "staff-tasks", "Staff", "Task Assignments", "staff_task_assignments",
        "staff:read", "staff:write",
        [
            {"key": "title", "label": "Task", "type": TEXT, "required": True},
            {"key": "assigned_to", "label": "Assigned to", "type": TEXT},
            {"key": "due_at", "label": "Due", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["open", "in_progress", "complete", "blocked"]},
            {"key": "handoff_notes", "label": "Handoff notes", "type": TEXTAREA},
        ],
        ["Assignment tracking", "Completion workflow", "Shift handoff reports"],
    ),
    "handoff-reports": _module(
        "handoff-reports", "Staff", "Shift Handoff Reports", "shift_handoff_reports",
        "staff:read", "staff:write",
        [
            {"key": "shift_date", "label": "Shift date", "type": DATE, "required": True},
            {"key": "outgoing_staff", "label": "Outgoing staff", "type": TEXT},
            {"key": "incoming_staff", "label": "Incoming staff", "type": TEXT},
            {"key": "area", "label": "Area", "type": TEXT},
            {"key": "summary", "label": "Summary", "type": TEXTAREA, "required": True},
            {"key": "open_items", "label": "Open items", "type": TEXTAREA},
            {"key": "priority", "label": "Priority", "type": SELECT, "options": ["low", "normal", "high"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["draft", "submitted", "reviewed"]},
        ],
        ["Shift notes", "Handoff reports", "Open task snapshot"],
    ),
    "time-clock": _module(
        "time-clock", "Staff", "Time Clock", "time_clock_entries",
        "staff:read", "staff:write",
        [
            {"key": "staff_name", "label": "Staff", "type": TEXT, "required": True},
            {"key": "clock_in", "label": "Clock in", "type": TEXT, "required": True},
            {"key": "clock_out", "label": "Clock out", "type": TEXT},
            {"key": "break_minutes", "label": "Break minutes", "type": NUMBER},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Time clock", "Payroll export basis", "Audit trail"],
    ),
    "ai-automation": _module(
        "ai-automation", "AI & Automation", "AI Automation", "automation_suggestions",
        "automation:read", "automation:write",
        [
            {"key": "suggestion_type", "label": "Type", "type": SELECT, "options": ["care_summary", "health_risk", "schedule_reminder", "owner_update", "billing_recommendation"]},
            {"key": "subject", "label": "Subject", "type": TEXT, "required": True},
            {"key": "summary", "label": "Summary", "type": TEXTAREA, "required": True},
            {"key": "confidence", "label": "Confidence", "type": NUMBER},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["draft", "reviewed", "approved", "dismissed"]},
        ],
        ["AI-generated care summaries", "Health-risk alerts", "Natural-language reporting"],
        "Generated text remains review-first and does not provide veterinary advice.",
    ),
    "integrations": _module(
        "integrations", "Mobile & Integrations", "Integration Readiness", "integration_connections",
        "integration:read", "integration:write",
        [
            {"key": "provider", "label": "Provider", "type": SELECT, "options": ["quickbooks", "stripe", "google_calendar", "push_notifications", "wearables", "document_scanning", "qr_horse_id"]},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["not_configured", "ready", "connected", "paused"]},
            {"key": "external_ref", "label": "External ref", "type": TEXT},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["QuickBooks readiness", "Google Calendar sync readiness", "Wearables/scanning/QR hooks"],
    ),
    "offline-sync": _module(
        "offline-sync", "Mobile & Integrations", "Offline Sync Queue", "offline_sync_queue",
        "integration:read", "integration:write",
        [
            {"key": "action_type", "label": "Action", "type": SELECT, "options": ["create", "update", "complete_task", "upload_document"]},
            {"key": "target_module", "label": "Target module", "type": TEXT, "required": True},
            {"key": "payload_summary", "label": "Payload summary", "type": TEXTAREA, "required": True},
            {"key": "captured_at", "label": "Captured", "type": TEXT},
            {"key": "sync_status", "label": "Status", "type": SELECT, "options": ["queued", "ready", "synced", "failed"]},
        ],
        ["Offline-ready queue shape", "Mobile replay workflow", "Audit-friendly sync state"],
        "This stores offline action metadata only. Native background sync and conflict resolution remain app-layer work.",
    ),
    "document-scans": _module(
        "document-scans", "Mobile & Integrations", "Document Scanning", "document_scan_jobs",
        "integration:read", "integration:write",
        [
            {"key": "document_type", "label": "Type", "type": SELECT, "options": ["receipt", "coggins", "waiver", "insurance", "other"]},
            {"key": "horse_name", "label": "Horse", "type": TEXT},
            {"key": "file_url", "label": "File URL", "type": TEXT, "required": True},
            {"key": "linked_module", "label": "Linked module", "type": TEXT},
            {"key": "scan_status", "label": "Status", "type": SELECT, "options": ["captured", "reviewed", "attached", "rejected"]},
            {"key": "notes", "label": "Notes", "type": TEXTAREA},
        ],
        ["Document scanning workflow", "Receipt/health doc intake", "Storage-provider handoff"],
        "Actual OCR, image cleanup, and file storage provider wiring are deferred to integration credentials.",
    ),
    "qr-horse-id": _module(
        "qr-horse-id", "Mobile & Integrations", "QR Horse Identification", "qr_horse_ids",
        "integration:read", "integration:write",
        [
            {"key": "horse_name", "label": "Horse", "type": TEXT, "required": True},
            {"key": "qr_code", "label": "QR code", "type": TEXT, "required": True},
            {"key": "profile_url", "label": "Profile URL", "type": TEXT},
            {"key": "stall_location", "label": "Stall/location", "type": TEXT},
            {"key": "status", "label": "Status", "type": SELECT, "options": ["draft", "printed", "active", "retired"]},
        ],
        ["QR horse identification", "Stall card workflow", "Mobile profile handoff"],
        "QR codes are deterministic text records here; printable image generation can be wired later.",
    ),
}

BACKLOG_AUDIT_COLLECTION = "backlog_audit_events"
BACKLOG_LOCATION_SHARE_COLLECTION = "barn_location_share_settings"
BACKLOG_ARENA_SHARE_COLLECTION = "arena_schedule_share_settings"
BACKLOG_COLLECTIONS = sorted({mod["collection"] for mod in MODULES.values()})
BACKLOG_SUPPORT_COLLECTIONS = [BACKLOG_AUDIT_COLLECTION, BACKLOG_LOCATION_SHARE_COLLECTION, BACKLOG_ARENA_SHARE_COLLECTION]
BACKLOG_RESET_COLLECTIONS = sorted({*BACKLOG_COLLECTIONS, *BACKLOG_SUPPORT_COLLECTIONS})


def _module_for(key: str) -> Dict[str, Any]:
    mod = MODULES.get(key)
    if not mod:
        raise HTTPException(404, "Unknown feature module")
    return mod


def _required_fields(mod: Dict[str, Any]) -> List[str]:
    return [f["key"] for f in mod["fields"] if f.get("required")]


def _exact_name_query(name: Optional[str]) -> Dict[str, str]:
    return {"$regex": f"^{re.escape(name or '')}$", "$options": "i"}


def _validate_record(mod: Dict[str, Any], data: Dict[str, Any]):
    if not isinstance(data, dict) or not data:
        raise HTTPException(422, "Record data is required")
    missing = [key for key in _required_fields(mod) if data.get(key) in (None, "")]
    if missing:
        raise HTTPException(422, f"Missing required field(s): {', '.join(missing)}")


def _base_doc(*, user: dict, new_id, data: Dict[str, Any], barn_id: str = DEFAULT_BARN_ID) -> Dict[str, Any]:
    now = _now_iso()
    return {
        "id": new_id(),
        "barn_id": user.get("barn_id") or barn_id,
        "data": data,
        "created_at": now,
        "updated_at": now,
        "created_by": user["id"],
        "updated_by": user["id"],
    }


def _safe_filename(value: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-").lower()
    return name or "equinesync-report"


def _matches_report_filters(record: Dict[str, Any], filters: Dict[str, Any]) -> bool:
    data = record.get("data") or {}
    for key, expected in filters.items():
        actual = record.get(key, data.get(key))
        if isinstance(expected, list):
            if actual not in expected:
                return False
        elif str(actual).lower() != str(expected).lower():
                return False
    return True


def _parse_datetime(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _payroll_hours(data: Dict[str, Any]) -> float:
    start = _parse_datetime(data.get("clock_in"))
    end = _parse_datetime(data.get("clock_out"))
    if not start or not end or end <= start:
        return 0.0
    try:
        break_minutes = float(data.get("break_minutes") or 0)
    except (TypeError, ValueError):
        break_minutes = 0.0
    return round(max(0.0, ((end - start).total_seconds() / 3600) - (break_minutes / 60)), 2)


def _ics_escape(value: Any) -> str:
    text = str(value or "")
    return text.replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")


def _calendar_stamp(value: Optional[str], *, all_day: bool = False, default_hours: int = 1) -> Dict[str, Any]:
    parsed = _parse_datetime(value)
    if parsed:
        if all_day:
            return {
                "start": parsed.date().isoformat(),
                "end": (parsed.date() + timedelta(days=1)).isoformat(),
                "ics_start": parsed.strftime("%Y%m%d"),
                "ics_end": (parsed + timedelta(days=1)).strftime("%Y%m%d"),
                "all_day": True,
            }
        end = parsed + timedelta(hours=default_hours)
        return {
            "start": parsed.isoformat(),
            "end": end.isoformat(),
            "ics_start": parsed.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "ics_end": end.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
            "all_day": False,
        }
    if value:
        safe_date = str(value)[:10]
        try:
            date_value = datetime.fromisoformat(safe_date).date()
        except ValueError:
            date_value = datetime.now(timezone.utc).date()
        return {
            "start": date_value.isoformat(),
            "end": (date_value + timedelta(days=1)).isoformat(),
            "ics_start": date_value.strftime("%Y%m%d"),
            "ics_end": (date_value + timedelta(days=1)).strftime("%Y%m%d"),
            "all_day": True,
        }
    now = datetime.now(timezone.utc)
    return {
        "start": now.isoformat(),
        "end": (now + timedelta(hours=default_hours)).isoformat(),
        "ics_start": now.strftime("%Y%m%dT%H%M%SZ"),
        "ics_end": (now + timedelta(hours=default_hours)).strftime("%Y%m%dT%H%M%SZ"),
        "all_day": False,
    }


def _calendar_event(*, source: str, record: Dict[str, Any], title: str, start: Optional[str], end: Optional[str] = None, all_day: bool = False, description: str = "") -> Dict[str, Any]:
    stamp = _calendar_stamp(start, all_day=all_day)
    if end:
        end_stamp = _calendar_stamp(end, all_day=all_day)
        stamp["end"] = end_stamp["end"] if all_day else end_stamp["start"]
        stamp["ics_end"] = end_stamp["ics_end"] if all_day else end_stamp["ics_start"]
    return {
        "uid": f"{source}-{record.get('id') or _safe_filename(title)}@equinesync.local",
        "source": source,
        "record_id": record.get("id"),
        "title": title,
        "description": description,
        **stamp,
    }


def _events_to_ics(events: List[Dict[str, Any]]) -> str:
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//EquineSync//Backlog Calendar Export//EN",
        "CALSCALE:GREGORIAN",
    ]
    generated = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for event in events:
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{_ics_escape(event.get('uid'))}",
            f"DTSTAMP:{generated}",
            f"SUMMARY:{_ics_escape(event.get('title'))}",
        ])
        if event.get("all_day"):
            lines.append(f"DTSTART;VALUE=DATE:{event.get('ics_start')}")
            lines.append(f"DTEND;VALUE=DATE:{event.get('ics_end')}")
        else:
            lines.append(f"DTSTART:{event.get('ics_start')}")
            lines.append(f"DTEND:{event.get('ics_end')}")
        if event.get("description"):
            lines.append(f"DESCRIPTION:{_ics_escape(event.get('description'))}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def _accounting_amount(value: Any) -> str:
    try:
        return f"{float(value or 0):.2f}"
    except (TypeError, ValueError):
        return "0.00"


def _accounting_label(value: Any) -> str:
    return str(value or "uncategorized").replace("_", " ").strip() or "uncategorized"


def _push_payload(*, source: str, record: Dict[str, Any], title: str, body: str, audience: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    clean_title = str(title or "EquineSync update").strip()[:80]
    clean_body = str(body or "Open EquineSync for the latest update.").strip()[:180]
    return {
        "source": source,
        "record_id": record.get("id"),
        "title": clean_title,
        "body": clean_body,
        "audience": str(audience or "custom").replace("_", " "),
        "delivery_status": "preview_only",
        "metadata": metadata or {},
    }


def _split_horse_names(value: Any) -> List[str]:
    return [name.strip() for name in str(value or "").replace("\n", ",").split(",") if name.strip()]


def _share_state(share: Dict[str, Any], *, owner_view: bool) -> Dict[str, Any]:
    enabled = bool((share or {}).get("enabled"))
    return {
        "enabled": enabled,
        "state": "published" if enabled else "private",
        "audience": "owner_parent" if owner_view else "staff",
        "source": "barn_admin_share_setting",
    }


def _share_payload(share: Dict[str, Any], *, owner_view: bool) -> Dict[str, Any]:
    if not owner_view:
        return dict(share or {})
    return {
        "id": (share or {}).get("id"),
        "enabled": bool((share or {}).get("enabled")),
        "title": (share or {}).get("title") or "",
        "note": (share or {}).get("note") or "",
        "share_path": (share or {}).get("share_path") or "",
        "updated_at": (share or {}).get("updated_at"),
    }


def _location_board_payload(*, share: Dict[str, Any], stalls: List[Dict[str, Any]], pastures: List[Dict[str, Any]], owner_view: bool = False) -> Dict[str, Any]:
    stall_rows = []
    horse_locations: Dict[str, Dict[str, Any]] = {}
    for record in stalls:
        data = record.get("data") or {}
        row = {
            "id": record.get("id"),
            "horse_name": data.get("horse_name") or "",
            "location_type": "stall",
            "stall_id": data.get("stall_id") or "",
            "barn_area": data.get("barn_area") or "",
            "row": data.get("row"),
            "column": data.get("column"),
            "status": data.get("status") or "occupied",
        }
        if not owner_view:
            row["notes"] = data.get("notes") or ""
        stall_rows.append(row)
        if row["horse_name"]:
            horse_locations[row["horse_name"]] = row

    pasture_rows = []
    for record in pastures:
        data = record.get("data") or {}
        horses = _split_horse_names(data.get("horse_names"))
        row = {
            "id": record.get("id"),
            "location_type": "pasture",
            "pasture": data.get("pasture") or "",
            "group_name": data.get("group_name") or "",
            "horse_names": horses,
            "start_time": data.get("start_time") or "",
            "end_time": data.get("end_time") or "",
            "status": data.get("status") or "planned",
        }
        if not owner_view:
            row["weather_rule"] = data.get("weather_rule") or ""
        pasture_rows.append(row)
        for horse_name in horses:
            if row["status"] in ("active", "planned", "weather_hold"):
                horse_locations[horse_name] = {
                    "horse_name": horse_name,
                    "location_type": "pasture",
                    "pasture": row["pasture"],
                    "group_name": row["group_name"],
                    "start_time": row["start_time"],
                    "end_time": row["end_time"],
                    "status": row["status"],
                }

    return {
        "share": _share_payload(share, owner_view=owner_view),
        "share_state": _share_state(share, owner_view=owner_view),
        "stalls": sorted(stall_rows, key=lambda item: (str(item.get("barn_area") or ""), str(item.get("stall_id") or ""))),
        "pastures": sorted(pasture_rows, key=lambda item: (str(item.get("pasture") or ""), str(item.get("start_time") or ""))),
        "horse_locations": sorted(horse_locations.values(), key=lambda item: str(item.get("horse_name") or "")),
        "stats": {
            "stalls": len(stall_rows),
            "pasture_blocks": len(pasture_rows),
            "horses_located": len(horse_locations),
        },
        "generated_at": _now_iso(),
    }


def _arena_schedule_payload(*, share: Dict[str, Any], records: List[Dict[str, Any]], owner_view: bool = False) -> Dict[str, Any]:
    blocks = []
    for record in records:
        data = record.get("data") or {}
        if owner_view and data.get("visibility", "shared_with_owners") != "shared_with_owners":
            continue
        row = {
            "id": record.get("id"),
            "arena_name": data.get("arena_name") or "",
            "title": data.get("title") or "",
            "date": data.get("date") or "",
            "start_time": data.get("start_time") or "",
            "end_time": data.get("end_time") or "",
            "rental_duration": data.get("rental_duration") or "",
            "status": data.get("status") or "open",
            "visibility": data.get("visibility") or "shared_with_owners",
            "horse_name": data.get("horse_name") or "",
            "source_request_id": data.get("source_request_id") or "",
        }
        if not owner_view:
            row["owner_name"] = data.get("owner_name") or ""
            row["notes"] = data.get("notes") or ""
        blocks.append(row)
    blocks = sorted(blocks, key=lambda item: (str(item.get("date") or ""), str(item.get("start_time") or ""), str(item.get("arena_name") or "")))
    return {
        "share": _share_payload(share, owner_view=owner_view),
        "share_state": _share_state(share, owner_view=owner_view),
        "blocks": blocks,
        "stats": {
            "blocks": len(blocks),
            "open": sum(1 for row in blocks if row.get("status") == "open"),
            "reserved": sum(1 for row in blocks if row.get("status") == "reserved"),
            "maintenance": sum(1 for row in blocks if row.get("status") == "maintenance"),
        },
        "generated_at": _now_iso(),
    }


def _qr_preview_matrix(code: str, size: int = 17) -> List[List[bool]]:
    source = code or "EquineSync"
    matrix: List[List[bool]] = []
    for y in range(size):
        row = []
        for x in range(size):
            finder = (
                (x < 5 and y < 5)
                or (x >= size - 5 and y < 5)
                or (x < 5 and y >= size - 5)
            )
            if finder:
                edge = x in (0, 4, size - 5, size - 1) or y in (0, 4, size - 5, size - 1)
                center = (1 <= x % (size - 5) <= 3) and (1 <= y % (size - 5) <= 3)
                row.append(edge or center)
                continue
            char = ord(source[(x + y * size) % len(source)])
            row.append(((char + x * 11 + y * 17) % 5) in (0, 2, 4))
        matrix.append(row)
    return matrix


def _stall_card_svg(data: Dict[str, Any]) -> str:
    horse_name = escape(str(data.get("horse_name") or "Horse"))
    qr_code = escape(str(data.get("qr_code") or "EQSYNC"))
    profile_url = escape(str(data.get("profile_url") or "Open EquineSync profile"))
    stall_location = escape(str(data.get("stall_location") or "Stall TBD"))
    matrix = _qr_preview_matrix(str(data.get("qr_code") or horse_name))
    cell = 10
    qr_origin_x = 210
    qr_origin_y = 92
    modules = []
    for y, row in enumerate(matrix):
        for x, on in enumerate(row):
            if on:
                modules.append(
                    f'<rect x="{qr_origin_x + x * cell}" y="{qr_origin_y + y * cell}" width="{cell}" height="{cell}" fill="#111827"/>'
                )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="360" viewBox="0 0 600 360" role="img" aria-label="EquineSync stall card for {horse_name}">
  <rect width="600" height="360" rx="20" fill="#fbfaf7"/>
  <rect x="20" y="20" width="560" height="320" rx="16" fill="#ffffff" stroke="#d6c7ae" stroke-width="2"/>
  <text x="48" y="70" font-family="Georgia, serif" font-size="22" fill="#7a5a2f" letter-spacing="3">EQUINESYNC</text>
  <text x="48" y="128" font-family="Georgia, serif" font-size="48" fill="#1f2937">{horse_name}</text>
  <text x="50" y="172" font-family="Arial, sans-serif" font-size="18" fill="#6b7280">Stall / location</text>
  <text x="50" y="205" font-family="Arial, sans-serif" font-size="30" font-weight="700" fill="#1f2937">{stall_location}</text>
  <text x="50" y="265" font-family="Arial, sans-serif" font-size="16" fill="#6b7280">Identifier</text>
  <text x="50" y="291" font-family="Arial, sans-serif" font-size="20" font-weight="700" fill="#1f2937">{qr_code}</text>
  <rect x="194" y="76" width="202" height="202" rx="14" fill="#ffffff" stroke="#d1d5db"/>
  {''.join(modules)}
  <text x="210" y="310" font-family="Arial, sans-serif" font-size="14" fill="#6b7280">{profile_url}</text>
  <text x="405" y="112" font-family="Arial, sans-serif" font-size="15" fill="#6b7280">Open this horse's</text>
  <text x="405" y="134" font-family="Arial, sans-serif" font-size="15" fill="#6b7280">EquineSync profile</text>
  <text x="405" y="170" font-family="Arial, sans-serif" font-size="12" fill="#9ca3af">Generated locally.</text>
  <text x="405" y="188" font-family="Arial, sans-serif" font-size="12" fill="#9ca3af">Replace preview grid with</text>
  <text x="405" y="206" font-family="Arial, sans-serif" font-size="12" fill="#9ca3af">a QR encoder when enabled.</text>
</svg>'''


def _clean_doc(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    return {k: v for k, v in doc.items() if k != "_id"}


def _dedupe(values: List[Optional[str]]) -> List[str]:
    seen = set()
    clean_values: List[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        clean_values.append(value)
    return clean_values


def _split_user_ids(value: Any) -> List[str]:
    if isinstance(value, list):
        raw_values = value
    else:
        raw_values = str(value or "").replace("\n", ",").split(",")
    return _dedupe([str(item).strip() for item in raw_values if str(item).strip()])


def _normalize_group_message_data(module_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if module_key != "group-messaging":
        return data
    normalized = dict(data)
    recipient_ids = _split_user_ids(normalized.get("recipient_user_ids"))
    if recipient_ids:
        normalized["recipient_user_ids"] = recipient_ids
    else:
        normalized.pop("recipient_user_ids", None)
    return normalized


def _normalize_digital_form_data(module_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    if module_key != "forms-signatures":
        return data
    normalized = dict(data)
    provider = str(normalized.get("signature_provider") or "internal").strip() or "internal"
    normalized["signature_provider"] = provider
    if provider == "internal":
        normalized["signature_scope"] = "local_acknowledgement_only"
        normalized["legal_signature_status"] = "not_legal_signature"
    elif provider == "docusign_ready":
        normalized["signature_scope"] = "provider_readiness_only"
        normalized["legal_signature_status"] = "provider_not_sent"
    return normalized


async def _owner_link_ids_for_user(db, user: Dict[str, Any], barn_id: str) -> List[str]:
    user_id = user.get("id")
    if not user_id:
        return []
    owner_docs = await db.owners.find(
        {
            "barn_id": barn_id,
            "$or": [
                {"user_id": user_id},
                {"owner_user_id": user_id},
                {"account_user_id": user_id},
                {"linked_user_id": user_id},
                {"user_ids": user_id},
            ],
        },
        {"_id": 0, "id": 1},
    ).to_list(50)
    return _dedupe([user_id] + [o.get("id") for o in owner_docs])


async def _owned_horse_ids_for_user(db, user: Dict[str, Any], barn_id: str) -> List[str]:
    user_id = user.get("id")
    owner_ids = await _owner_link_ids_for_user(db, user, barn_id)
    if not user_id and not owner_ids:
        return []
    clauses: List[Dict[str, Any]] = []
    if owner_ids:
        clauses.extend([
            {"owner_id": {"$in": owner_ids}},
            {"primary_owner_id": {"$in": owner_ids}},
            {"secondary_owner_ids": {"$in": owner_ids}},
        ])
    if user_id:
        clauses.extend([
            {"owner_user_id": user_id},
            {"owner_user_ids": user_id},
            {"guardian_user_id": user_id},
            {"guardian_user_ids": user_id},
            {"rider_user_id": user_id},
            {"rider_user_ids": user_id},
        ])
    horse_docs = await db.horses.find(
        {"barn_id": barn_id, "$or": clauses},
        {"_id": 0, "id": 1},
    ).to_list(500)
    return _dedupe([h.get("id") for h in horse_docs])


def _owner_account_clauses(owner_ids: List[str], user_id: Optional[str]) -> List[Dict[str, Any]]:
    clauses: List[Dict[str, Any]] = []
    if user_id:
        for field in (
            "owner_user_id",
            "payer_user_id",
            "recipient_user_id",
            "data.owner_user_id",
            "data.payer_user_id",
            "data.recipient_user_id",
            "data.shared_user_ids",
        ):
            clauses.append({field: user_id})
    if owner_ids:
        for field in (
            "owner_id",
            "primary_owner_id",
            "payer_owner_id",
            "recipient_owner_id",
            "data.owner_id",
            "data.primary_owner_id",
            "data.payer_owner_id",
            "data.recipient_owner_id",
        ):
            clauses.append({field: {"$in": owner_ids}})
    return clauses


def _owner_announcement_clauses(user: Dict[str, Any]) -> List[Dict[str, Any]]:
    user_id = user.get("id")
    if not user_id:
        return []
    targeted_fields = (
        "data.recipient_user_id",
        "data.recipient_user_ids",
        "data.owner_user_id",
        "data.owner_user_ids",
        "data.guardian_user_id",
        "data.guardian_user_ids",
        "data.parent_user_id",
        "data.parent_user_ids",
    )
    clauses = [{field: user_id} for field in targeted_fields]
    if user.get("role") == "horse_owner":
        clauses.append({"data.audience": "owners"})
    return clauses


def _owner_horse_context_clauses(owner_ids: List[str], horse_ids: List[str], user_id: Optional[str]) -> List[Dict[str, Any]]:
    clauses = _owner_account_clauses(owner_ids, user_id)
    if horse_ids:
        for field in ("horse_id", "data.horse_id"):
            clauses.append({field: {"$in": horse_ids}})
    return clauses


def _staff_shift_clauses(user_id: Optional[str]) -> List[Dict[str, Any]]:
    if not user_id:
        return []
    return [
        {"staff_user_id": user_id},
        {"data.staff_user_id": user_id},
        {"data.staff_user_ids": user_id},
    ]


def _staff_task_clauses(user_id: Optional[str]) -> List[Dict[str, Any]]:
    if not user_id:
        return []
    return [
        {"assigned_user_id": user_id},
        {"assigned_staff_user_id": user_id},
        {"data.assigned_user_id": user_id},
        {"data.assigned_to_user_id": user_id},
        {"data.assigned_staff_user_id": user_id},
        {"data.assigned_user_ids": user_id},
        {"data.assigned_staff_user_ids": user_id},
    ]


def _staff_handoff_clauses(user_id: Optional[str]) -> List[Dict[str, Any]]:
    if not user_id:
        return []
    return [
        {"data.incoming_staff_user_id": user_id},
        {"data.outgoing_staff_user_id": user_id},
        {"data.incoming_staff_user_ids": user_id},
        {"data.outgoing_staff_user_ids": user_id},
    ]


def _staff_time_clock_clauses(user_id: Optional[str]) -> List[Dict[str, Any]]:
    if not user_id:
        return []
    return [
        {"staff_user_id": user_id},
        {"data.staff_user_id": user_id},
    ]


async def _staff_user_lookup(db, user: Dict[str, Any], staff_user_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not staff_user_id:
        return None
    return await db.users.find_one(
        {
            "id": staff_user_id,
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "role": {"$in": sorted(STAFF_ROLES)},
        },
        {"_id": 0, "id": 1, "full_name": 1, "email": 1, "role": 1},
    )


async def _trainer_user_lookup(db, user: Dict[str, Any], trainer_user_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not trainer_user_id:
        return None
    return await db.users.find_one(
        {
            "id": trainer_user_id,
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "role": "trainer",
        },
        {"_id": 0, "id": 1, "full_name": 1, "email": 1, "role": 1},
    )


async def _horse_lookup(db, user: Dict[str, Any], horse_id: Optional[str]) -> Optional[Dict[str, Any]]:
    if not horse_id:
        return None
    return await db.horses.find_one(
        {"id": horse_id, "barn_id": user.get("barn_id") or DEFAULT_BARN_ID},
        {"_id": 0, "id": 1, "name": 1},
    )


RF8_STAFF_IDENTITY_FIELDS: Dict[str, List[tuple[str, str]]] = {
    "staff-scheduling": [("staff_user_id", "staff_name")],
    "staff-tasks": [("assigned_user_id", "assigned_to")],
    "handoff-reports": [("outgoing_staff_user_id", "outgoing_staff"), ("incoming_staff_user_id", "incoming_staff")],
    "time-clock": [("staff_user_id", "staff_name")],
}


async def _normalize_staff_identity_data(
    db,
    user: Dict[str, Any],
    module_key: str,
    data: Dict[str, Any],
    *,
    creating: bool = False,
) -> Dict[str, Any]:
    normalized = dict(data or {})
    identity_fields = RF8_STAFF_IDENTITY_FIELDS.get(module_key, [])

    if creating and identity_fields:
        missing_ids = [id_key for id_key, _ in identity_fields if not normalized.get(id_key)]
        if missing_ids:
            raise HTTPException(422, f"Missing required stable staff id field(s): {', '.join(missing_ids)}")

    for id_key, name_key in identity_fields:
        if creating and normalized.get(name_key) and not normalized.get(id_key):
            raise HTTPException(422, f"{name_key} requires {id_key}")

    async def apply_user_id(id_key: str, name_key: str) -> None:
        staff_user_id = normalized.get(id_key)
        if not staff_user_id:
            return
        staff_user = await _staff_user_lookup(db, user, staff_user_id)
        if not staff_user:
            raise HTTPException(422, f"Unknown staff user for {id_key}")
        normalized[id_key] = staff_user["id"]
        normalized[name_key] = staff_user.get("full_name") or staff_user.get("email") or staff_user["id"]

    for id_key, name_key in identity_fields:
        await apply_user_id(id_key, name_key)

    return normalized


async def _normalize_training_plan_identity_data(
    db,
    user: Dict[str, Any],
    module_key: str,
    data: Dict[str, Any],
    *,
    creating: bool = False,
) -> Dict[str, Any]:
    normalized = dict(data or {})
    if module_key != "training-plans":
        return normalized

    if creating:
        missing = [key for key in ("horse_id", "trainer_user_id") if not normalized.get(key)]
        if missing:
            raise HTTPException(422, f"Missing required stable training plan field(s): {', '.join(missing)}")

    horse_id = normalized.get("horse_id")
    if horse_id:
        horse = await _horse_lookup(db, user, horse_id)
        if not horse:
            raise HTTPException(422, "Unknown horse for training plan")
        normalized["horse_id"] = horse["id"]
        normalized["horse_name"] = horse.get("name") or horse["id"]

    trainer_user_id = normalized.get("trainer_user_id")
    if (user.get("role") or "").strip().lower() == "trainer":
        if trainer_user_id and trainer_user_id != user.get("id"):
            raise HTTPException(403, "Trainer can only assign their own trainer id")
        trainer_user_id = user.get("id")
        normalized["trainer_user_id"] = trainer_user_id
    if trainer_user_id:
        trainer = await _trainer_user_lookup(db, user, trainer_user_id)
        if not trainer:
            raise HTTPException(422, "Unknown trainer for training plan")
        normalized["trainer_user_id"] = trainer["id"]
        normalized["trainer_name"] = trainer.get("full_name") or trainer.get("email") or trainer["id"]

    return normalized


def _automation_draft(*, suggestion_type: str, subject: str, summary: str, confidence: float, generated_key: str) -> Dict[str, Any]:
    return {
        "suggestion_type": suggestion_type,
        "subject": subject,
        "summary": summary,
        "confidence": confidence,
        "status": "draft",
        "source": "deterministic_generator",
        "generated_key": generated_key,
    }


async def ensure_backlog_indexes(db):
    for mod in MODULES.values():
        coll = db[mod["collection"]]
        await coll.create_index([("barn_id", 1), ("created_at", -1)])
        await coll.create_index([("barn_id", 1), ("updated_at", -1)])
    await db[BACKLOG_AUDIT_COLLECTION].create_index([("barn_id", 1), ("created_at", -1)])
    await db[BACKLOG_AUDIT_COLLECTION].create_index([("record_id", 1), ("created_at", -1)])
    await db[BACKLOG_LOCATION_SHARE_COLLECTION].create_index([("barn_id", 1)], unique=True)
    await db[BACKLOG_ARENA_SHARE_COLLECTION].create_index([("barn_id", 1)], unique=True)


async def seed_starter_backlog(db, new_id, actor_id: Optional[str] = None):
    """Compatibility hook retained for older imports.

    Launch builds must not create starter backlog records. New barns start empty
    and use onboarding plus module-specific add flows.
    """
    return {"records_created": 0, "skipped": True}


def build_router(*, db, get_current_user, new_id) -> APIRouter:
    router = APIRouter(tags=["feature-backlog"])

    async def write_audit(
        *,
        action: str,
        user: dict,
        collection: str,
        record_id: Optional[str] = None,
        module_key: Optional[str] = None,
        before: Optional[Dict[str, Any]] = None,
        after: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        now = _now_iso()
        await db[BACKLOG_AUDIT_COLLECTION].insert_one({
            "id": new_id(),
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "action": action,
            "module_key": module_key,
            "collection": collection,
            "record_id": record_id,
            "actor_id": user.get("id"),
            "actor_name": user.get("full_name"),
            "actor_role": user.get("role"),
            "before": _clean_doc(before),
            "after": _clean_doc(after),
            "metadata": metadata or {},
            "created_at": now,
        })

    @router.get("/feature-modules")
    async def list_modules(user=Depends(get_current_user)):
        rows = []
        for mod in MODULES.values():
            if not can(user, mod["read_permission"]):
                continue
            count = await db[mod["collection"]].count_documents(
                {"barn_id": user.get("barn_id") or DEFAULT_BARN_ID, "archived_at": {"$exists": False}},
            )
            rows.append({k: v for k, v in mod.items() if k != "collection"} | {"record_count": count})
        return rows

    @router.get("/staff-portal/staff-directory")
    async def staff_portal_staff_directory(user=Depends(get_current_user)):
        require_permission(user, "staff:read")
        rows = await db.users.find(
            {
                "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
                "role": {"$in": sorted(STAFF_ROLES)},
            },
            {"_id": 0, "id": 1, "full_name": 1, "email": 1, "role": 1},
        ).sort("full_name", 1).to_list(500)
        return {"items": rows}

    @router.get("/feature-modules/{module_key}")
    async def get_module(module_key: str, user=Depends(get_current_user)):
        mod = _module_for(module_key)
        require_permission(user, mod["read_permission"])
        q = {"barn_id": user.get("barn_id") or DEFAULT_BARN_ID, "archived_at": {"$exists": False}}
        records = await db[mod["collection"]].find(q, {"_id": 0}).sort("updated_at", -1).to_list(500)
        return {
            "module": {k: v for k, v in mod.items() if k != "collection"},
            "records": records,
        }

    @router.post("/feature-modules/{module_key}/records")
    async def create_record(module_key: str, body: FeatureRecordIn, user=Depends(get_current_user)):
        mod = _module_for(module_key)
        require_permission(user, mod["write_permission"])
        data = await _normalize_staff_identity_data(db, user, module_key, body.data, creating=True)
        data = await _normalize_training_plan_identity_data(db, user, module_key, data, creating=True)
        data = _normalize_group_message_data(module_key, data)
        data = _normalize_digital_form_data(module_key, data)
        _validate_record(mod, data)
        doc = _base_doc(user=user, new_id=new_id, data=data)
        await db[mod["collection"]].insert_one(doc)
        clean = _clean_doc(doc)
        await write_audit(
            action="record_created",
            user=user,
            collection=mod["collection"],
            module_key=module_key,
            record_id=doc["id"],
            after=clean,
        )
        return clean

    @router.patch("/feature-modules/{module_key}/records/{record_id}")
    async def update_record(module_key: str, record_id: str, body: FeatureRecordIn, user=Depends(get_current_user)):
        mod = _module_for(module_key)
        require_permission(user, mod["write_permission"])
        existing = await db[mod["collection"]].find_one(
            {"id": record_id, "barn_id": user.get("barn_id") or DEFAULT_BARN_ID},
            {"_id": 0},
        )
        if not existing:
            raise HTTPException(404, "Record not found")
        data = await _normalize_staff_identity_data(db, user, module_key, {**(existing.get("data") or {}), **body.data})
        data = await _normalize_training_plan_identity_data(db, user, module_key, data)
        data = _normalize_group_message_data(module_key, data)
        data = _normalize_digital_form_data(module_key, data)
        _validate_record(mod, data)
        await db[mod["collection"]].update_one(
            {"id": record_id},
            {"$set": {"data": data, "updated_at": _now_iso(), "updated_by": user["id"]}},
        )
        updated = await db[mod["collection"]].find_one({"id": record_id}, {"_id": 0})
        await write_audit(
            action="record_updated",
            user=user,
            collection=mod["collection"],
            module_key=module_key,
            record_id=record_id,
            before=existing,
            after=updated,
            metadata={"updated_fields": sorted(body.data.keys())},
        )
        return updated

    @router.delete("/feature-modules/{module_key}/records/{record_id}")
    async def archive_record(module_key: str, record_id: str, user=Depends(get_current_user)):
        mod = _module_for(module_key)
        require_permission(user, mod["write_permission"])
        existing = await db[mod["collection"]].find_one(
            {"id": record_id, "barn_id": user.get("barn_id") or DEFAULT_BARN_ID},
            {"_id": 0},
        )
        if not existing:
            raise HTTPException(404, "Record not found")
        res = await db[mod["collection"]].update_one(
            {"id": record_id, "barn_id": user.get("barn_id") or DEFAULT_BARN_ID},
            {"$set": {"archived_at": _now_iso(), "updated_at": _now_iso(), "updated_by": user["id"]}},
        )
        if res.matched_count == 0:
            raise HTTPException(404, "Record not found")
        archived = await db[mod["collection"]].find_one({"id": record_id}, {"_id": 0})
        await write_audit(
            action="record_archived",
            user=user,
            collection=mod["collection"],
            module_key=module_key,
            record_id=record_id,
            before=existing,
            after=archived,
        )
        return {"ok": True, "archived": True}

    @router.post("/barn-location-share")
    async def update_barn_location_share(body: BarnLocationShareIn, user=Depends(get_current_user)):
        if user.get("role") not in ADMIN_ROLES:
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        existing = await db[BACKLOG_LOCATION_SHARE_COLLECTION].find_one({"barn_id": barn_id}, {"_id": 0})
        now = _now_iso()
        share = {
            "id": existing.get("id") if existing else new_id(),
            "barn_id": barn_id,
            "enabled": body.enabled,
            "title": body.title.strip() or "Barn Location Board",
            "note": body.note or "",
            "share_path": "/barn-locations",
            "created_at": existing.get("created_at") if existing else now,
            "updated_at": now,
            "created_by": existing.get("created_by") if existing else user["id"],
            "updated_by": user["id"],
        }
        await db[BACKLOG_LOCATION_SHARE_COLLECTION].update_one(
            {"barn_id": barn_id},
            {"$set": share},
            upsert=True,
        )
        await write_audit(
            action="barn_location_share_updated",
            user=user,
            collection=BACKLOG_LOCATION_SHARE_COLLECTION,
            record_id=share["id"],
            before=existing,
            after=share,
            metadata={"enabled": share["enabled"]},
        )
        return share

    @router.get("/barn-location-share")
    async def barn_location_share(user=Depends(get_current_user)):
        role = user.get("role")
        if role not in STAFF_ROLES and role not in ("horse_owner", "parent"):
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        share = await db[BACKLOG_LOCATION_SHARE_COLLECTION].find_one({"barn_id": barn_id}, {"_id": 0})
        if not share:
            share = {
                "id": "default",
                "barn_id": barn_id,
                "enabled": role in ADMIN_ROLES,
                "title": "Barn Location Board",
                "note": "",
                "share_path": "/barn-locations",
                "created_at": None,
                "updated_at": None,
            }
        if role in ("horse_owner", "parent") and not share.get("enabled"):
            raise HTTPException(403, "Barn location sharing is not enabled")

        q = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        stalls = await db.stall_assignments.find(q, {"_id": 0}).sort("data.stall_id", 1).to_list(500)
        pastures = await db.pasture_schedules.find(q, {"_id": 0}).sort("data.start_time", 1).to_list(500)
        owner_view = role in ("horse_owner", "parent")
        return _location_board_payload(share=share, stalls=stalls, pastures=pastures, owner_view=owner_view)

    @router.post("/arena-schedule-share")
    async def update_arena_schedule_share(body: ArenaScheduleShareIn, user=Depends(get_current_user)):
        if user.get("role") not in ADMIN_ROLES:
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        existing = await db[BACKLOG_ARENA_SHARE_COLLECTION].find_one({"barn_id": barn_id}, {"_id": 0})
        now = _now_iso()
        share = {
            "id": existing.get("id") if existing else new_id(),
            "barn_id": barn_id,
            "enabled": body.enabled,
            "title": body.title.strip() or "Arena Schedule",
            "note": body.note or "",
            "share_path": "/arena-schedule",
            "created_at": existing.get("created_at") if existing else now,
            "updated_at": now,
            "created_by": existing.get("created_by") if existing else user["id"],
            "updated_by": user["id"],
        }
        await db[BACKLOG_ARENA_SHARE_COLLECTION].update_one(
            {"barn_id": barn_id},
            {"$set": share},
            upsert=True,
        )
        await write_audit(
            action="arena_schedule_share_updated",
            user=user,
            collection=BACKLOG_ARENA_SHARE_COLLECTION,
            record_id=share["id"],
            before=existing,
            after=share,
            metadata={"enabled": share["enabled"]},
        )
        return share

    @router.get("/arena-schedule-share")
    async def arena_schedule_share(user=Depends(get_current_user)):
        role = user.get("role")
        if role not in STAFF_ROLES and role not in ("horse_owner", "parent"):
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        share = await db[BACKLOG_ARENA_SHARE_COLLECTION].find_one({"barn_id": barn_id}, {"_id": 0})
        if not share:
            share = {
                "id": "default",
                "barn_id": barn_id,
                "enabled": role in ADMIN_ROLES,
                "title": "Arena Schedule",
                "note": "",
                "share_path": "/arena-schedule",
                "created_at": None,
                "updated_at": None,
            }
        owner_view = role in ("horse_owner", "parent")
        if owner_view and not share.get("enabled"):
            raise HTTPException(403, "Arena schedule sharing is not enabled")

        q = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        records = await db.arena_schedule_blocks.find(q, {"_id": 0}).sort([("data.date", 1), ("data.start_time", 1)]).to_list(500)
        return _arena_schedule_payload(share=share, records=records, owner_view=owner_view)

    @router.get("/integrations/placeholders")
    async def integration_placeholders(user=Depends(get_current_user)):
        require_permission(user, "integration:read")
        return [
            {"provider": "stripe", "status": "credentials_required", "ready_for": ["checkout", "autopay", "webhooks"]},
            {"provider": "quickbooks", "status": "credentials_required", "ready_for": ["expense_export", "invoice_sync"]},
            {"provider": "google_calendar", "status": "credentials_required", "ready_for": ["lesson_sync", "show_calendar"]},
            {"provider": "push_notifications", "status": "app_token_required", "ready_for": ["owner_updates", "task_alerts"]},
            {"provider": "wearables", "status": "partner_required", "ready_for": ["vitals", "activity"]},
            {"provider": "qr_horse_id", "status": "internal_ready", "ready_for": ["horse_profile_link", "stall_card"]},
            {"provider": "document_scanning", "status": "storage_required", "ready_for": ["receipt_upload", "health_docs"]},
        ]

    @router.post("/integrations/{provider}/prepare")
    async def prepare_integration(provider: str, user=Depends(get_current_user)):
        require_permission(user, "integration:write")
        await write_audit(
            action="integration_prepare_requested",
            user=user,
            collection="integration_connections",
            module_key="integrations",
            metadata={"provider": provider},
        )
        return {
            "provider": provider,
            "status": "configuration_ready",
            "message": "Credentials and webhook configuration are required before live sync is enabled.",
        }

    @router.post("/integrations/google-calendar/export")
    async def export_google_calendar(body: CalendarExportIn, user=Depends(get_current_user)):
        require_permission(user, "integration:read")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        allowed_sources = {"competitions", "staff-scheduling", "health-reminders"}
        sources = body.sources or sorted(allowed_sources)
        invalid = [source for source in sources if source not in allowed_sources]
        if invalid:
            raise HTTPException(422, f"Unsupported calendar source(s): {', '.join(invalid)}")

        events: List[Dict[str, Any]] = []
        if "competitions" in sources:
            rows = await db.show_entries.find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).sort("data.start_date", 1).to_list(500)
            for record in rows:
                data = record.get("data") or {}
                if not data.get("start_date"):
                    continue
                detail = " · ".join(part for part in [
                    data.get("horse_name"),
                    data.get("rider_name"),
                    data.get("entry_status"),
                ] if part)
                events.append(_calendar_event(
                    source="competitions",
                    record=record,
                    title=f"Show: {data.get('show_name') or 'Competition'}",
                    start=data.get("start_date"),
                    all_day=True,
                    description=detail,
                ))

        if "staff-scheduling" in sources:
            rows = await db.staff_shifts.find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).sort("data.shift_start", 1).to_list(500)
            for record in rows:
                data = record.get("data") or {}
                if not data.get("shift_start"):
                    continue
                events.append(_calendar_event(
                    source="staff-scheduling",
                    record=record,
                    title=f"Shift: {data.get('staff_name') or 'Staff'}",
                    start=data.get("shift_start"),
                    end=data.get("shift_end"),
                    description=" · ".join(part for part in [data.get("area"), data.get("role"), data.get("notes")] if part),
                ))

        if "health-reminders" in sources:
            rows = await db.health_reminders.find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).sort("data.due_date", 1).to_list(500)
            for record in rows:
                data = record.get("data") or {}
                if not data.get("due_date"):
                    continue
                reminder_type = str(data.get("reminder_type") or "Health reminder").replace("_", " ")
                events.append(_calendar_event(
                    source="health-reminders",
                    record=record,
                    title=f"{data.get('horse_name') or 'Horse'}: {reminder_type}",
                    start=data.get("due_date"),
                    all_day=True,
                    description=" · ".join(part for part in [data.get("provider"), data.get("status"), data.get("notes")] if part),
                ))

        events.sort(key=lambda item: item.get("start") or "")
        filename = f"equinesync-google-calendar-{_now_iso()[:10]}.ics"
        manifest = {
            "status": "calendar_export_ready",
            "provider": "google_calendar",
            "filename": filename,
            "content_type": "text/calendar",
            "generated_at": _now_iso(),
            "sources": sources,
            "event_count": len(events),
            "events": events,
            "ics": _events_to_ics(events),
            "message": "Import this ICS file manually, or use the event manifest when OAuth calendar sync is configured.",
        }
        await write_audit(
            action="calendar_export_requested",
            user=user,
            collection="integration_connections",
            module_key="integrations",
            metadata={"provider": "google_calendar", "sources": sources, "event_count": len(events), "filename": filename},
        )
        return manifest

    @router.post("/integrations/quickbooks/export")
    async def export_quickbooks(body: QuickBooksExportIn, user=Depends(get_current_user)):
        require_permission(user, "financial:read")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        rows: List[Dict[str, Any]] = []

        if body.include_expenses:
            expenses = await db.expenses.find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).sort("data.spent_at", -1).to_list(1000)
            for record in expenses:
                data = record.get("data") or {}
                rows.append({
                    "source": "expense",
                    "transaction_type": "Expense",
                    "transaction_id": record.get("id"),
                    "transaction_date": data.get("spent_at") or record.get("created_at") or "",
                    "name": data.get("vendor") or "Vendor TBD",
                    "account": _accounting_label(data.get("category")),
                    "item": "",
                    "amount": _accounting_amount(data.get("amount")),
                    "status": "ready",
                    "memo": data.get("notes") or "",
                    "attachment_url": data.get("receipt_url") or "",
                })

        if body.include_invoices:
            invoices = await db.invoices.find({"barn_id": barn_id}, {"_id": 0}).sort("due_date", -1).to_list(1000)
            for invoice in invoices:
                if invoice.get("status") == "void":
                    continue
                rows.append({
                    "source": "invoice",
                    "transaction_type": "Invoice",
                    "transaction_id": invoice.get("id"),
                    "transaction_date": invoice.get("due_date") or invoice.get("created_at") or "",
                    "name": invoice.get("owner_name") or "Owner TBD",
                    "account": "accounts receivable",
                    "item": invoice.get("horse_name") or "Boarding services",
                    "amount": _accounting_amount(invoice.get("total")),
                    "status": invoice.get("status") or "open",
                    "memo": invoice.get("notes") or "",
                    "attachment_url": "",
                })

        rows.sort(key=lambda item: str(item.get("transaction_date") or ""), reverse=True)
        filename = f"equinesync-quickbooks-export-{_now_iso()[:10]}.csv"
        manifest = {
            "status": "quickbooks_export_ready",
            "provider": "quickbooks",
            "filename": filename,
            "content_type": "text/csv",
            "generated_at": _now_iso(),
            "filters": {
                "include_expenses": body.include_expenses,
                "include_invoices": body.include_invoices,
            },
            "columns": ["source", "transaction_type", "transaction_id", "transaction_date", "name", "account", "item", "amount", "status", "memo", "attachment_url"],
            "row_count": len(rows),
            "total_amount": _accounting_amount(sum(float(row["amount"]) for row in rows)),
            "rows": rows,
            "message": "Use this CSV-compatible manifest for review before configuring live QuickBooks sync.",
        }
        await write_audit(
            action="quickbooks_export_requested",
            user=user,
            collection="integration_connections",
            module_key="integrations",
            metadata={
                "provider": "quickbooks",
                "row_count": manifest["row_count"],
                "total_amount": manifest["total_amount"],
                "filename": filename,
            },
        )
        return manifest

    @router.post("/integrations/push-notifications/preview")
    async def preview_push_notifications(body: PushPreviewIn, user=Depends(get_current_user)):
        require_permission(user, "communication:read")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        payloads: List[Dict[str, Any]] = []

        if body.include_group_messages:
            messages = await db.group_messages.find(
                {
                    "barn_id": barn_id,
                    "archived_at": {"$exists": False},
                    "$or": [
                        {"data.channel": "push_ready"},
                        {"data.status": {"$in": ["queued", "sent"]}},
                    ],
                },
                {"_id": 0},
            ).sort("updated_at", -1).to_list(250)
            for record in messages:
                data = record.get("data") or {}
                recipient_ids = _split_user_ids(data.get("recipient_user_ids"))
                payloads.append(_push_payload(
                    source="group_messages",
                    record=record,
                    title=data.get("subject") or "Barn announcement",
                    body=data.get("body") or "",
                    audience=data.get("audience") or "custom",
                    metadata={
                        "channel": data.get("channel") or "in_app",
                        "message_status": data.get("status") or "draft",
                        "delivery_claim": "preview_only_no_external_delivery",
                        "recipient_user_ids": recipient_ids,
                        "recipient_count": len(recipient_ids),
                    },
                ))

        if body.include_owner_updates:
            updates = await db.owner_media_updates.find(
                {
                    "barn_id": barn_id,
                    "archived_at": {"$exists": False},
                    "data.visibility": "owner_only",
                },
                {"_id": 0},
            ).sort("created_at", -1).to_list(250)
            for record in updates:
                data = record.get("data") or {}
                horse_name = data.get("horse_name") or "your horse"
                payloads.append(_push_payload(
                    source="owner_media_updates",
                    record=record,
                    title=f"New update for {horse_name}",
                    body=data.get("caption") or "A new photo/video update is ready.",
                    audience="owners",
                    metadata={
                        "horse_name": data.get("horse_name"),
                        "owner_name": data.get("owner_name"),
                        "media_url": data.get("media_url"),
                    },
                ))

        filename = f"equinesync-push-preview-{_now_iso()[:10]}.json"
        manifest = {
            "status": "push_preview_ready",
            "provider": "push_notifications",
            "filename": filename,
            "content_type": "application/json",
            "generated_at": _now_iso(),
            "filters": {
                "include_group_messages": body.include_group_messages,
                "include_owner_updates": body.include_owner_updates,
            },
            "payload_count": len(payloads),
            "payloads": payloads,
            "message": "Preview only. APNs/FCM credentials and device tokens are required before live delivery is enabled.",
        }
        await write_audit(
            action="push_preview_requested",
            user=user,
            collection="integration_connections",
            module_key="integrations",
            metadata={
                "provider": "push_notifications",
                "payload_count": len(payloads),
                "filename": filename,
            },
        )
        return manifest

    @router.get("/integrations/qr-horse-id/{record_id}/stall-card")
    async def qr_horse_stall_card(record_id: str, user=Depends(get_current_user)):
        require_permission(user, "integration:read")
        record = await db.qr_horse_ids.find_one(
            {
                "id": record_id,
                "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
                "archived_at": {"$exists": False},
            },
            {"_id": 0},
        )
        if not record:
            raise HTTPException(404, "QR horse ID not found")
        data = record.get("data") or {}
        filename = f"{_safe_filename(data.get('horse_name') or data.get('qr_code') or 'horse')}-stall-card.svg"
        manifest = {
            "status": "stall_card_ready",
            "provider": "qr_horse_id",
            "filename": filename,
            "content_type": "image/svg+xml",
            "generated_at": _now_iso(),
            "record_id": record_id,
            "horse_name": data.get("horse_name"),
            "qr_code": data.get("qr_code"),
            "profile_url": data.get("profile_url"),
            "svg": _stall_card_svg(data),
            "message": "Printable stall-card SVG generated locally. A true QR encoder can replace the preview grid when a QR dependency is enabled.",
        }
        await write_audit(
            action="qr_stall_card_generated",
            user=user,
            collection="qr_horse_ids",
            module_key="qr-horse-id",
            record_id=record_id,
            after=record,
            metadata={"filename": filename, "horse_name": data.get("horse_name")},
        )
        return manifest

    @router.post("/integrations/document-scans/prepare-upload")
    async def prepare_document_scan_upload(body: DocumentScanUploadIn, user=Depends(get_current_user)):
        require_permission(user, "integration:write")
        validate_upload("document", body.mime_type, body.byte_size)
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        subject = body.horse_name or body.document_type or "document"
        key = build_key("default", "document", _safe_filename(subject), body.filename, barn_id=barn_id)
        intent = get_provider().prepare_upload(key=key, mime=body.mime_type, byte_size=body.byte_size)
        draft_record = {
            "document_type": body.document_type,
            "horse_name": body.horse_name or "",
            "file_url": intent.public_url,
            "linked_module": body.linked_module or "document-scans",
            "scan_status": "captured",
            "notes": body.notes or f"Prepared upload for {body.filename}.",
        }
        manifest = {
            "status": "upload_intent_ready",
            "provider": get_provider().name(),
            "storage_claim": "upload_intent_only_no_external_file_mutation_by_rf14",
            "filename": body.filename,
            "mime_type": body.mime_type,
            "byte_size": body.byte_size,
            "upload": {
                "media_id": intent.media_id,
                "upload_url": intent.upload_url,
                "upload_method": intent.upload_method,
                "public_url": intent.public_url,
                "storage_key": intent.storage_key,
                "expires_at": intent.expires_at,
            },
            "draft_record": draft_record,
            "message": "Upload intent only. Store through upload_url only when a real storage provider is configured, then save draft_record as the document scan.",
        }
        await write_audit(
            action="document_scan_upload_prepared",
            user=user,
            collection="document_scan_jobs",
            module_key="document-scans",
            metadata={
                "filename": body.filename,
                "mime_type": body.mime_type,
                "byte_size": body.byte_size,
                "provider": manifest["provider"],
                "storage_key": intent.storage_key,
            },
        )
        return manifest

    @router.post("/automation/generate-drafts")
    async def generate_automation_drafts(user=Depends(get_current_user)):
        require_permission(user, "automation:write")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        today_key = datetime.now(timezone.utc).date().isoformat()

        health_due = await db.health_reminders.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.status": {"$in": ["due", "expired"]},
        })
        open_injuries = await db.injury_lameness_cases.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.status": {"$in": ["open", "monitoring", "vet_called"]},
        })
        open_staff_tasks = await db.staff_task_assignments.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.status": {"$in": ["open", "in_progress", "blocked"]},
        })
        owner_updates = await db.owner_media_updates.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.visibility": "owner_only",
        })
        overdue_invoices = await db.invoices.count_documents({"barn_id": barn_id, "status": "overdue"})
        autopay_open = await db.payment_profiles.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.autopay_status": {"$in": ["not_enrolled", "invited"]},
        })
        active_plans = await db.training_plans.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.status": "active",
        })
        upcoming_shows = await db.show_entries.count_documents({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.entry_status": {"$in": ["planning", "submitted", "accepted"]},
        })

        candidates = [
            _automation_draft(
                suggestion_type="care_summary",
                subject="Daily barn care summary",
                summary=(
                    f"Draft summary: {active_plans} active training plan(s), {open_staff_tasks} open staff task(s), "
                    f"and {health_due} health reminder(s) due or expired. Review and edit before sharing."
                ),
                confidence=0.68,
                generated_key=f"{today_key}:care_summary",
            ),
            _automation_draft(
                suggestion_type="health_risk",
                subject="Health review queue",
                summary=(
                    f"Review-first alert: {health_due} reminder(s) are due/expired and {open_injuries} injury or lameness case(s) remain open. "
                    "This is an operational prompt only, not veterinary guidance."
                ),
                confidence=0.74 if health_due or open_injuries else 0.5,
                generated_key=f"{today_key}:health_risk",
            ),
            _automation_draft(
                suggestion_type="schedule_reminder",
                subject="Predictive scheduling reminders",
                summary=(
                    f"There are {open_staff_tasks} open staff task(s) and {upcoming_shows} upcoming show-entry workflow(s). "
                    "Review staffing, transport, and prep timing before approving reminders."
                ),
                confidence=0.64,
                generated_key=f"{today_key}:schedule_reminder",
            ),
            _automation_draft(
                suggestion_type="owner_update",
                subject="Owner update opportunity",
                summary=(
                    f"{owner_updates} owner-visible media update(s) are currently queued or shared. "
                    "Consider preparing a concise owner-facing recap for horses with recent work."
                ),
                confidence=0.61,
                generated_key=f"{today_key}:owner_update",
            ),
            _automation_draft(
                suggestion_type="billing_recommendation",
                subject="Smart billing review",
                summary=(
                    f"Billing review: {overdue_invoices} overdue invoice(s) and {autopay_open} owner payment profile(s) still not fully enrolled. "
                    "Review before sending reminders or changing billing status."
                ),
                confidence=0.7 if overdue_invoices or autopay_open else 0.52,
                generated_key=f"{today_key}:billing_recommendation",
            ),
        ]

        created = []
        skipped = []
        for data in candidates:
            existing = await db.automation_suggestions.find_one({
                "barn_id": barn_id,
                "archived_at": {"$exists": False},
                "data.generated_key": data["generated_key"],
            }, {"_id": 0})
            if existing:
                skipped.append(existing)
                continue
            doc = _base_doc(user=user, new_id=new_id, data=data)
            await db.automation_suggestions.insert_one(doc)
            created.append({k: v for k, v in doc.items() if k != "_id"})
        return {
            "created": len(created),
            "skipped": len(skipped),
            "records": created,
            "message": "Drafts generated for review. Nothing is sent or approved automatically.",
        }

    @router.get("/owner-portal/media-updates")
    async def owner_portal_media_updates(user=Depends(get_current_user)):
        role = user.get("role")
        q: Dict[str, Any] = {
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "archived_at": {"$exists": False},
        }
        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, q["barn_id"])
            horse_ids = await _owned_horse_ids_for_user(db, user, q["barn_id"])
            owner_clauses = _owner_horse_context_clauses(owner_ids, horse_ids, user.get("id"))
            if not owner_clauses:
                return []
            q.update({"data.visibility": "owner_only", "$or": owner_clauses})
        elif role not in ("admin", "barn_manager", "trainer"):
            raise HTTPException(403, "Permission denied")
        rows = await db.owner_media_updates.find(q, {"_id": 0}).sort("created_at", -1).to_list(100)
        return rows

    @router.get("/owner-portal/forms")
    async def owner_portal_forms(user=Depends(get_current_user)):
        role = user.get("role")
        q: Dict[str, Any] = {
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "archived_at": {"$exists": False},
            "data.status": {"$in": ["sent", "signed", "expired"]},
        }
        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, q["barn_id"])
            owner_clauses = _owner_account_clauses(owner_ids, user.get("id"))
            if not owner_clauses:
                return []
            q["$or"] = owner_clauses
        elif role not in ("admin", "barn_manager", "trainer"):
            raise HTTPException(403, "Permission denied")
        rows = await db.digital_forms.find(q, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return rows

    @router.post("/owner-portal/forms/{record_id}/sign")
    async def sign_owner_portal_form(record_id: str, user=Depends(get_current_user)):
        role = user.get("role")
        if role not in ("horse_owner", "parent"):
            raise HTTPException(403, "Permission denied")
        q: Dict[str, Any] = {
            "id": record_id,
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "archived_at": {"$exists": False},
            "data.status": "sent",
        }
        owner_ids = await _owner_link_ids_for_user(db, user, q["barn_id"])
        owner_clauses = _owner_account_clauses(owner_ids, user.get("id"))
        if not owner_clauses:
            raise HTTPException(404, "Form not found or not ready for signature")
        q["$or"] = owner_clauses
        existing = await db.digital_forms.find_one(q, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Form not found or not ready for signature")
        data = {
            **(existing.get("data") or {}),
            "status": "signed",
            "signed_at": datetime.now(timezone.utc).date().isoformat(),
            "signed_by": user["id"],
            "signed_by_name": user.get("full_name"),
            "signature_scope": "local_acknowledgement_only",
            "legal_signature_status": "not_legal_signature",
            "signed_claim": "local_acknowledgement_not_legal_signature",
        }
        await db.digital_forms.update_one(
            {"id": record_id},
            {"$set": {"data": data, "updated_at": _now_iso(), "updated_by": user["id"]}},
        )
        updated = await db.digital_forms.find_one({"id": record_id}, {"_id": 0})
        await write_audit(
            action="owner_form_signed",
            user=user,
            collection="digital_forms",
            module_key="forms-signatures",
            record_id=record_id,
            before=existing,
            after=updated,
        )
        return updated

    @router.get("/owner-portal/health-documents")
    async def owner_portal_health_documents(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        q: Dict[str, Any] = {
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
        }
        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, barn_id)
            horse_ids = await _owned_horse_ids_for_user(db, user, barn_id)
            share_clauses = _owner_horse_context_clauses(owner_ids, horse_ids, user.get("id"))
            if not share_clauses:
                return []
            q["$or"] = share_clauses
        elif role not in ("admin", "barn_manager", "trainer", "veterinarian"):
            raise HTTPException(403, "Permission denied")
        rows = await db.health_documents.find(q, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return rows

    @router.get("/owner-portal/health-summary")
    async def owner_portal_health_summary(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        reminder_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        weight_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}

        if role in ("horse_owner", "parent"):
            horse_ids = await _owned_horse_ids_for_user(db, user, barn_id)
            if not horse_ids:
                return {"reminders": [], "weight_entries": []}
            horse_filter = {"$in": horse_ids}
            reminder_q["$or"] = [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}]
            weight_q["$or"] = [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}]
        elif role not in ("admin", "barn_manager", "trainer", "veterinarian"):
            raise HTTPException(403, "Permission denied")

        reminders = await db.health_reminders.find(reminder_q, {"_id": 0}).sort("data.due_date", 1).to_list(100)
        weight_entries = await db.weight_condition_entries.find(weight_q, {"_id": 0}).sort("data.recorded_at", -1).to_list(100)
        return {"reminders": reminders, "weight_entries": weight_entries}

    @router.get("/owner-portal/emergency")
    async def owner_portal_emergency(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        contact_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        workflow_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, barn_id)
            horse_ids = await _owned_horse_ids_for_user(db, user, barn_id)
            contact_clauses = _owner_horse_context_clauses(owner_ids, horse_ids, user.get("id"))
            workflow_clauses = _owner_horse_context_clauses(owner_ids, horse_ids, user.get("id"))
            if not contact_clauses and not workflow_clauses:
                return {"contacts": [], "workflows": []}
            contact_q["$or"] = contact_clauses
            workflow_q["$or"] = workflow_clauses
        elif role not in ("admin", "barn_manager", "trainer", "veterinarian"):
            raise HTTPException(403, "Permission denied")
        contacts = await db.emergency_contacts.find(contact_q, {"_id": 0}).sort("data.priority", 1).to_list(100)
        workflows = await db.emergency_workflows.find(workflow_q, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return {"contacts": contacts, "workflows": workflows}

    @router.get("/owner-portal/training-performance")
    async def owner_portal_training_performance(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        plan_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        show_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        ride_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        legacy_training_q: Dict[str, Any] = {"barn_id": barn_id}

        if role in ("horse_owner", "parent"):
            horse_ids = await _owned_horse_ids_for_user(db, user, barn_id)
            if not horse_ids:
                return {"plans": [], "shows": [], "rides": [], "ride_logs": []}
            horse_filter = {"$in": horse_ids}
            plan_q["$or"] = [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}]
            show_q["$or"] = [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}]
            ride_q["$or"] = [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}]
            legacy_training_q = {
                "barn_id": barn_id,
                "$or": [{"horse_id": horse_filter}, {"data.horse_id": horse_filter}],
            }
        elif role not in ("admin", "barn_manager", "trainer"):
            raise HTTPException(403, "Permission denied")

        plans = await db.training_plans.find(plan_q, {"_id": 0}).sort("updated_at", -1).to_list(100)
        shows = await db.show_entries.find(show_q, {"_id": 0}).sort("data.start_date", 1).to_list(100)
        rides = await db.ride_gps_tracks.find(ride_q, {"_id": 0}).sort("data.started_at", -1).to_list(100)
        ride_logs = await db.training.find(legacy_training_q, {"_id": 0}).sort("date", -1).to_list(100)
        return {"plans": plans, "shows": shows, "rides": rides, "ride_logs": ride_logs}

    @router.get("/owner-portal/billing")
    async def owner_portal_billing(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        invoice_q: Dict[str, Any] = {"barn_id": barn_id}
        payment_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        recurring_q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}

        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, barn_id)
            invoice_clauses = _owner_account_clauses(owner_ids, user.get("id"))
            if not invoice_clauses:
                return {"invoices": [], "payment_profiles": [], "recurring_rules": [], "payment_provider": "stripe_ready"}
            invoice_q["$or"] = invoice_clauses
            payment_q["$or"] = invoice_clauses
            recurring_q["$or"] = invoice_clauses
        elif role not in ("admin", "barn_manager"):
            raise HTTPException(403, "Permission denied")

        invoices = await db.invoices.find(invoice_q, {"_id": 0}).sort("due_date", -1).to_list(100)
        payment_profiles = await db.payment_profiles.find(payment_q, {"_id": 0}).sort("updated_at", -1).to_list(50)
        recurring_rules = await db.recurring_billing_rules.find(recurring_q, {"_id": 0}).sort("data.next_run_date", 1).to_list(100)
        return {
            "invoices": invoices,
            "payment_profiles": payment_profiles,
            "recurring_rules": recurring_rules,
            "payment_provider": "stripe_ready",
        }

    @router.post("/owner-portal/billing/{invoice_id}/prepare-payment")
    async def prepare_owner_portal_payment(invoice_id: str, user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        invoice_q: Dict[str, Any] = {"id": invoice_id, "barn_id": barn_id}
        if role in ("horse_owner", "parent"):
            owner_ids = await _owner_link_ids_for_user(db, user, barn_id)
            invoice_clauses = _owner_account_clauses(owner_ids, user.get("id"))
            if not invoice_clauses:
                raise HTTPException(404, "Invoice not found")
            invoice_q["$or"] = invoice_clauses
        elif role not in ("admin", "barn_manager"):
            raise HTTPException(403, "Permission denied")

        invoice = await db.invoices.find_one(invoice_q, {"_id": 0})
        if not invoice:
            raise HTTPException(404, "Invoice not found")
        await write_audit(
            action="payment_prepare_requested",
            user=user,
            collection="invoices",
            record_id=invoice["id"],
            after=invoice,
            metadata={"provider": "stripe", "amount": invoice.get("total") or 0},
        )
        return {
            "invoice_id": invoice["id"],
            "provider": "stripe",
            "status": "configuration_ready",
            "amount": invoice.get("total") or 0,
            "message": "Stripe checkout credentials are required before live payment collection is enabled.",
        }

    @router.get("/owner-portal/announcements")
    async def owner_portal_announcements(user=Depends(get_current_user)):
        role = user.get("role")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        q: Dict[str, Any] = {
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "data.status": "sent",
            "data.audience": {"$in": ["owners", "custom"]},
        }
        if role in ("horse_owner", "parent"):
            clauses = _owner_announcement_clauses(user)
            if not clauses:
                return []
            q["$or"] = clauses
        elif role not in ("admin", "barn_manager", "trainer"):
            raise HTTPException(403, "Permission denied")
        rows = await db.group_messages.find(q, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return rows

    @router.get("/staff-portal/my-work")
    async def staff_portal_my_work(user=Depends(get_current_user)):
        if user.get("role") not in STAFF_ROLES:
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        user_id = user.get("id")
        base_q = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        shift_clauses = _staff_shift_clauses(user_id)
        task_clauses = _staff_task_clauses(user_id)
        handoff_clauses = _staff_handoff_clauses(user_id)
        time_clauses = _staff_time_clock_clauses(user_id)
        if not any([shift_clauses, task_clauses, handoff_clauses, time_clauses]):
            return {"shifts": [], "tasks": [], "handoffs": [], "time_entries": []}
        shifts = await db.staff_shifts.find(
            {**base_q, "$or": shift_clauses},
            {"_id": 0},
        ).sort("data.shift_start", 1).to_list(50)
        tasks = await db.staff_task_assignments.find(
            {**base_q, "$or": task_clauses},
            {"_id": 0},
        ).sort("data.due_at", 1).to_list(100)
        handoffs = await db.shift_handoff_reports.find(
            {**base_q, "$or": handoff_clauses},
            {"_id": 0},
        ).sort("updated_at", -1).to_list(25)
        time_entries = await db.time_clock_entries.find(
            {**base_q, "$or": time_clauses},
            {"_id": 0},
        ).sort("data.clock_in", -1).to_list(25)
        return {
            "shifts": shifts,
            "tasks": tasks,
            "handoffs": handoffs,
            "time_entries": time_entries,
        }

    @router.patch("/staff-portal/tasks/{record_id}/status")
    async def staff_portal_task_status(record_id: str, body: FeatureRecordIn, user=Depends(get_current_user)):
        if user.get("role") not in STAFF_ROLES:
            raise HTTPException(403, "Permission denied")
        status = body.data.get("status")
        if status not in {"open", "in_progress", "blocked", "complete"}:
            raise HTTPException(422, "Invalid task status")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        q: Dict[str, Any] = {
            "id": record_id,
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
        }
        if user.get("role") not in ("admin", "barn_manager"):
            staff_clauses = _staff_task_clauses(user.get("id"))
            if not staff_clauses:
                raise HTTPException(404, "Task not found")
            q["$or"] = staff_clauses
        existing = await db.staff_task_assignments.find_one(q, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Task not found")
        data = {**(existing.get("data") or {}), "status": status}
        if status == "complete":
            data["completed_at"] = _now_iso()
            data["completed_by_user_id"] = user.get("id")
            data["completed_by_name"] = user.get("full_name")
        await db.staff_task_assignments.update_one(
            {"id": record_id},
            {"$set": {"data": data, "updated_at": _now_iso(), "updated_by": user["id"]}},
        )
        updated = await db.staff_task_assignments.find_one({"id": record_id}, {"_id": 0})
        await write_audit(
            action="staff_task_status_updated",
            user=user,
            collection="staff_task_assignments",
            module_key="staff-tasks",
            record_id=record_id,
            before=existing,
            after=updated,
            metadata={"status": status},
        )
        return updated

    @router.post("/staff-portal/time-clock/clock-in")
    async def staff_portal_clock_in(user=Depends(get_current_user)):
        if user.get("role") not in STAFF_ROLES:
            raise HTTPException(403, "Permission denied")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        time_clauses = _staff_time_clock_clauses(user.get("id"))
        if not time_clauses:
            raise HTTPException(403, "Permission denied")
        existing = await db.time_clock_entries.find_one({
            "barn_id": barn_id,
            "archived_at": {"$exists": False},
            "$or": time_clauses,
            "data.clock_out": {"$in": [None, ""]},
        }, {"_id": 0})
        if existing:
            return existing
        doc = _base_doc(
            user=user,
            new_id=new_id,
            data={
                "staff_user_id": user.get("id"),
                "staff_name": user.get("full_name"),
                "clock_in": _now_iso(),
                "clock_out": "",
                "break_minutes": 0,
                "notes": "Staff portal clock-in.",
            },
        )
        await db.time_clock_entries.insert_one(doc)
        clean = _clean_doc(doc)
        await write_audit(
            action="staff_clocked_in",
            user=user,
            collection="time_clock_entries",
            module_key="time-clock",
            record_id=doc["id"],
            after=clean,
        )
        return clean

    @router.post("/staff-portal/time-clock/{record_id}/clock-out")
    async def staff_portal_clock_out(record_id: str, user=Depends(get_current_user)):
        if user.get("role") not in STAFF_ROLES:
            raise HTTPException(403, "Permission denied")
        q = {
            "id": record_id,
            "barn_id": user.get("barn_id") or DEFAULT_BARN_ID,
            "archived_at": {"$exists": False},
            "$or": _staff_time_clock_clauses(user.get("id")),
        }
        if not q["$or"]:
            raise HTTPException(403, "Permission denied")
        existing = await db.time_clock_entries.find_one(q, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Time entry not found")
        data = {**(existing.get("data") or {}), "clock_out": _now_iso()}
        await db.time_clock_entries.update_one(
            {"id": record_id},
            {"$set": {"data": data, "updated_at": _now_iso(), "updated_by": user["id"]}},
        )
        updated = await db.time_clock_entries.find_one({"id": record_id}, {"_id": 0})
        await write_audit(
            action="staff_clocked_out",
            user=user,
            collection="time_clock_entries",
            module_key="time-clock",
            record_id=record_id,
            before=existing,
            after=updated,
        )
        return updated

    @router.post("/staff-portal/payroll-export")
    async def staff_payroll_export(body: PayrollExportIn, user=Depends(get_current_user)):
        require_permission(user, "staff:read")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        q: Dict[str, Any] = {"barn_id": barn_id, "archived_at": {"$exists": False}}
        if body.staff_user_id:
            q["data.staff_user_id"] = body.staff_user_id
        if body.staff_name:
            q["data.staff_name"] = _exact_name_query(body.staff_name)

        start_at = _parse_datetime(body.start_date)
        end_at = _parse_datetime(body.end_date)
        records = await db.time_clock_entries.find(q, {"_id": 0}).sort("data.clock_in", -1).to_list(1000)
        rows: List[Dict[str, Any]] = []
        for record in records:
            data = record.get("data") or {}
            clock_in = _parse_datetime(data.get("clock_in"))
            if start_at and (not clock_in or clock_in < start_at):
                continue
            if end_at and (not clock_in or clock_in > end_at):
                continue
            rows.append({
                "staff_name": data.get("staff_name") or "",
                "clock_in": data.get("clock_in") or "",
                "clock_out": data.get("clock_out") or "",
                "break_minutes": data.get("break_minutes") or 0,
                "hours": f"{_payroll_hours(data):.2f}",
                "notes": data.get("notes") or "",
                "entry_id": record.get("id"),
            })

        filename = f"equinesync-payroll-export-{_now_iso()[:10]}.csv"
        manifest = {
            "status": "payroll_export_ready",
            "filename": filename,
            "content_type": "text/csv",
            "generated_at": _now_iso(),
            "filters": {
                "start_date": body.start_date,
                "end_date": body.end_date,
                "staff_user_id": body.staff_user_id,
                "staff_name": body.staff_name,
            },
            "columns": ["staff_name", "clock_in", "clock_out", "break_minutes", "hours", "notes", "entry_id"],
            "row_count": len(rows),
            "total_hours": round(sum(float(row["hours"]) for row in rows), 2),
            "rows": rows,
        }
        await write_audit(
            action="payroll_export_requested",
            user=user,
            collection="time_clock_entries",
            module_key="time-clock",
            metadata={
                "row_count": manifest["row_count"],
                "total_hours": manifest["total_hours"],
                "filters": manifest["filters"],
                "filename": filename,
            },
        )
        return manifest

    @router.get("/audit/backlog")
    async def backlog_audit_log(user=Depends(get_current_user)):
        if user.get("role") not in ADMIN_ROLES:
            raise HTTPException(403, "Permission denied")
        rows = await db[BACKLOG_AUDIT_COLLECTION].find(
            {"barn_id": user.get("barn_id") or DEFAULT_BARN_ID},
            {"_id": 0},
        ).sort("created_at", -1).to_list(250)
        return rows

    @router.get("/reports/backlog-dashboard")
    async def backlog_dashboard(user=Depends(get_current_user)):
        require_permission(user, "reporting:read")
        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        revenue_rows = await db.invoices.find({"barn_id": barn_id}, {"_id": 0, "total": 1, "status": 1}).to_list(1000)
        expenses = await db.expenses.find({"barn_id": barn_id}, {"_id": 0}).to_list(1000)
        stall_rows = await db.stall_assignments.find({"barn_id": barn_id}, {"_id": 0}).to_list(500)
        health_due = await db.health_reminders.count_documents({"barn_id": barn_id, "data.status": {"$in": ["due", "expired"]}})
        revenue_total = sum(float(r.get("total") or 0) for r in revenue_rows if r.get("status") != "void")
        expense_total = sum(float((r.get("data") or {}).get("amount") or 0) for r in expenses)
        occupied = sum(1 for s in stall_rows if (s.get("data") or {}).get("status") == "occupied")
        return {
            "occupancy": {"occupied": occupied, "total_stalls": len(stall_rows)},
            "financial": {"revenue": revenue_total, "expenses": expense_total, "profit_loss": revenue_total - expense_total},
            "health": {"due_or_expired": health_due},
            "exports": {"excel": "export_ready", "pdf": "export_ready"},
        }

    @router.post("/reports/custom-builder")
    async def custom_report(body: CustomReportIn, user=Depends(get_current_user)):
        require_permission(user, "reporting:write")
        selected = [_module_for(k) for k in body.module_keys]
        return {
            "name": body.name,
            "module_keys": body.module_keys,
            "filters": body.filters,
            "columns": ["id", "created_at", "updated_at", "created_by", "data"],
            "status": "definition_valid",
            "collections": [m["collection"] for m in selected],
            "export_formats": ["xlsx", "pdf"],
        }

    @router.post("/reports/export")
    async def export_report(body: ReportExportIn, user=Depends(get_current_user)):
        require_permission(user, "reporting:read")
        export_format = (body.format or "xlsx").lower()
        if export_format not in ("xlsx", "pdf"):
            raise HTTPException(422, "Export format must be xlsx or pdf")
        if not body.module_keys:
            raise HTTPException(422, "Choose at least one data source")

        barn_id = user.get("barn_id") or DEFAULT_BARN_ID
        selected = []
        for module_key in body.module_keys:
            mod = _module_for(module_key)
            require_permission(user, mod["read_permission"])
            selected.append(mod)

        rows: List[Dict[str, Any]] = []
        for mod in selected:
            records = await db[mod["collection"]].find(
                {"barn_id": barn_id, "archived_at": {"$exists": False}},
                {"_id": 0},
            ).sort("updated_at", -1).to_list(250)
            for record in records:
                if not _matches_report_filters(record, body.filters):
                    continue
                rows.append({
                    "module_key": mod["key"],
                    "module_label": mod["label"],
                    "collection": mod["collection"],
                    "id": record.get("id"),
                    "created_at": record.get("created_at"),
                    "updated_at": record.get("updated_at"),
                    "created_by": record.get("created_by"),
                    "updated_by": record.get("updated_by"),
                    "data": record.get("data") or {},
                })

        download_format = "csv" if export_format == "xlsx" else "json"
        filename = f"{_safe_filename(body.name)}-{_now_iso()[:10]}.{download_format}"
        manifest = {
            "name": body.name,
            "status": "export_manifest_ready",
            "format": export_format,
            "download_format": download_format,
            "filename": filename,
            "content_type": "text/csv" if download_format == "csv" else "application/json",
            "generated_at": _now_iso(),
            "module_keys": body.module_keys,
            "filters": body.filters,
            "columns": ["module_key", "module_label", "collection", "id", "created_at", "updated_at", "created_by", "updated_by", "data"],
            "row_count": len(rows),
            "rows": rows,
            "message": "Use this manifest for spreadsheet/PDF generation; no third-party export service is required to preview the data.",
        }
        await write_audit(
            action="report_export_requested",
            user=user,
            collection=BACKLOG_AUDIT_COLLECTION,
            metadata={
                "format": export_format,
                "module_keys": body.module_keys,
                "row_count": len(rows),
                "filename": filename,
            },
        )
        return manifest

    return router
