"""
Notification dispatcher.

Phase 1 design (per /app/memory/TASK_ENGINE_ARCHITECTURE.md §5):
- TaskEvent rows are written by the engine inside the completion transaction.
- A polling loop in this module picks up un-dispatched events and fans them
  out to registered channel handlers (in-app inbox, email; push deferred).
- Per-user `notification_preferences` document gates each channel × category.
- Marks each event row with `dispatched_at` so we never double-send.

When MongoDB change streams become available (replica set), swap the poll
for `db.task_events.watch()` without touching the route layer.
"""
from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import re
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Response
from pydantic import BaseModel, Field, field_validator
import httpx

logger = logging.getLogger(__name__)

POLL_INTERVAL_SECONDS = int(os.environ.get("NOTIFY_POLL_SECONDS", "10"))
BATCH_SIZE = int(os.environ.get("NOTIFY_BATCH_SIZE", "50"))
MAX_DISPATCH_ATTEMPTS = int(os.environ.get("NOTIFY_MAX_ATTEMPTS", "3"))
EXPO_PUSH_SEND_URL = "https://exp.host/--/api/v2/push/send"
PUSH_TOKEN_COLLECTION = "push_device_tokens"
PUSH_SEND_COLLECTION = "push_send_attempts"
PUSH_PROOF_TITLE = "EquineSync"
PUSH_PROOF_BODY = "Urgent barn update. Please open EquineSync for details."
PUSH_PROOF_DATA = {"type": "founder_push_proof", "privacy": "generic"}

SMS_CONSENT_LANGUAGE = (
    "Yes, I agree to receive automated customer care and urgent operational "
    "text messages from EquineSync, including barn coordination, schedule or "
    "task reminders, invite/account setup reminders, support follow-up, and "
    "guardian/parent notices when applicable. Message frequency varies based "
    "on account activity and urgent operational needs. Message and data rates "
    "may apply. Reply STOP to opt out. Reply HELP for help."
)
SMS_HELP_MESSAGE = (
    "EquineSync: For help, sign in to EquineSync or contact support at "
    "https://app.equine-sync.com/support. Reply STOP to opt out."
)
SMS_OPTOUT_MESSAGE = (
    "EquineSync: You are opted out of SMS messages. Reply START to opt back in."
)
SMS_OPTIN_MESSAGE = (
    "EquineSync: You are now opted in to receive EquineSync customer care and "
    "urgent operational text messages. Message frequency varies. Message and "
    "data rates may apply. Reply HELP for help. Reply STOP to opt out."
)
PRIVACY_SAFE_PROOF_MESSAGE = (
    "EquineSync: A time-sensitive barn coordination update is available for "
    "your account. Please sign in to EquineSync for details. Reply STOP to opt "
    "out or HELP for help."
)

# Defaults: which event_type × category should ship by channel, when a user
# has no explicit preferences saved.
DEFAULT_INBOX_RULES = {
    # event_type -> set of categories (or "*" for all)
    "task.completed": {"medication", "farrier", "vet", "rehab"},
    "task.skipped":   {"medication", "vet"},
    "task.voided":    {"medication", "vet"},
}
DEFAULT_EMAIL_RULES = {
    # email is intentionally narrower to avoid noise
    "task.skipped":   {"medication"},
    "task.voided":    {"medication"},
}


# ---------- Pydantic models ----------

class NotificationPrefsIn(BaseModel):
    inbox_enabled: bool = True
    email_enabled: bool = True
    push_enabled: bool = False
    sms_enabled: bool = False
    sms_phone_number: Optional[str] = None
    digest_enabled: bool = True  # owner-only; ignored for non-owner accounts
    # event_type -> categories list ([] = none, ["*"] = all)
    inbox_rules: Optional[dict] = None
    email_rules: Optional[dict] = None


class PushTokenIn(BaseModel):
    expo_push_token: str = Field(..., min_length=20, max_length=256)
    platform: str = Field(..., min_length=2, max_length=32)
    device_id: Optional[str] = Field(default=None, max_length=128)
    permission_status: Optional[str] = Field(default=None, max_length=64)
    enabled: bool = True

    @field_validator("expo_push_token")
    @classmethod
    def valid_expo_token(cls, value):  # noqa: N805
        token = value.strip()
        if not (
            token.startswith("ExponentPushToken[")
            or token.startswith("ExpoPushToken[")
        ):
            raise ValueError("Invalid Expo push token")
        return token

    @field_validator("platform")
    @classmethod
    def normalize_platform(cls, value):  # noqa: N805
        platform = value.strip().lower()
        if platform not in {"ios", "android"}:
            raise ValueError("Unsupported push platform")
        return platform

    @field_validator("device_id", "permission_status")
    @classmethod
    def clean_optional_text(cls, value):  # noqa: N805
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None


class SmsConsentIn(BaseModel):
    sms_enabled: bool
    phone_number: Optional[str] = None
    source: str = "contact_preferences"


class SmsProofSendIn(BaseModel):
    phone_number: Optional[str] = None
    message: Optional[str] = None


# ---------- helpers ----------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat()


def _new_id() -> str:
    import uuid
    return str(uuid.uuid4())


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _redact_token_hash(token: str) -> str:
    return _token_hash(token)[:12]


def _expo_ticket_diagnostics(ticket: object) -> dict:
    if not isinstance(ticket, dict):
        return {}

    details = ticket.get("details")
    diagnostics = {
        "ticket_error": ticket.get("message") or ticket.get("error"),
    }
    if isinstance(details, dict):
        diagnostics["ticket_details_error"] = details.get("error")
    return {key: value for key, value in diagnostics.items() if value}




def _hash_value(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _normalize_phone(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    raw = value.strip()
    if raw.startswith("+"):
        digits = "+" + re.sub(r"\D", "", raw)
    else:
        digits_only = re.sub(r"\D", "", raw)
        if len(digits_only) == 10:
            digits = "+1" + digits_only
        elif len(digits_only) == 11 and digits_only.startswith("1"):
            digits = "+" + digits_only
        else:
            digits = "+" + digits_only
    if not re.fullmatch(r"\+1\d{10}", digits):
        raise HTTPException(400, "Use a valid US mobile number")
    return digits


def _twiml(message: str) -> Response:
    escaped = (
        message.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return Response(
        content=f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{escaped}</Message></Response>',
        media_type="application/xml",
    )


def _is_sms_configured() -> bool:
    has_account = bool(os.environ.get("TWILIO_ACCOUNT_SID"))
    has_sender = bool(os.environ.get("TWILIO_MESSAGING_SERVICE_SID"))
    has_auth_token = bool(os.environ.get("TWILIO_AUTH_TOKEN"))
    has_api_key = bool(
        os.environ.get("TWILIO_API_KEY_SID")
        and os.environ.get("TWILIO_API_KEY_SECRET")
    )
    return has_account and has_sender and (has_api_key or has_auth_token)


def _twilio_basic_auth() -> tuple[str, str]:
    api_key = os.environ.get("TWILIO_API_KEY_SID")
    api_secret = os.environ.get("TWILIO_API_KEY_SECRET")
    if api_key and api_secret:
        return api_key, api_secret
    return os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"]


def _sms_send_enabled() -> bool:
    return os.environ.get("TWILIO_SMS_ENABLED", "false").lower() == "true"


def _safe_sms_body(body: str) -> str:
    lowered = body.lower()
    blocked_terms = (
        "diagnosis",
        "medication dose",
        "credit card",
        "payment method",
        "contract",
        "minor",
        "ssn",
        "social security",
    )
    if any(term in lowered for term in blocked_terms):
        raise HTTPException(400, "SMS body contains blocked sensitive-detail terms")
    if "reply stop" not in lowered or "help" not in lowered:
        raise HTTPException(400, "SMS body must include STOP and HELP instructions")
    if not body.startswith("EquineSync:"):
        raise HTTPException(400, "SMS body must start with EquineSync brand name")
    return body


def _rule_matches(rules: Optional[dict], event_type: str, category: Optional[str]) -> bool:
    if not rules:
        return False
    cats = rules.get(event_type)
    if cats is None:
        return False
    if cats == "*" or "*" in cats:
        return True
    return bool(category and category in cats)


async def _get_user_prefs(db, user_id: str) -> dict:
    rec = await db.notification_preferences.find_one({"user_id": user_id}, {"_id": 0})
    defaults = {
        "user_id": user_id,
        "inbox_enabled": True,
        "email_enabled": True,
        "push_enabled": False,
        "sms_enabled": False,
        "sms_phone_number": None,
        "sms_phone_hash": None,
        "sms_consent_status": "not_opted_in",
        "sms_consent_source": None,
        "sms_consent_language": SMS_CONSENT_LANGUAGE,
        "digest_enabled": True,
        "inbox_rules": DEFAULT_INBOX_RULES,
        "email_rules": DEFAULT_EMAIL_RULES,
    }
    if rec:
        # Merge in any new defaults that were added after this row was first saved.
        for k, v in defaults.items():
            rec.setdefault(k, v)
        return rec
    return defaults


# ---------- channel handlers ----------

async def _deliver_inbox(db, recipient_user_id: str, event: dict):
    """Append to per-user inbox."""
    doc = {
        "id": _new_id(),
        "user_id": recipient_user_id,
        "event_id": event["id"],
        "event_type": event.get("event_type"),
        "category": event.get("category"),
        "title": (event.get("payload_snapshot") or {}).get("title") or event.get("event_type"),
        "summary": _summarize(event),
        "task_id": event.get("task_id"),
        "subject_horse_ids": event.get("subject_horse_ids", []),
        "occurred_at": event.get("occurred_at"),
        "read_at": None,
        "created_at": _iso(_now()),
    }
    await db.notifications.insert_one(doc)


def _summarize(event: dict) -> str:
    snap = event.get("payload_snapshot") or {}
    title = snap.get("title") or event.get("event_type")
    et = event.get("event_type")
    outcome = snap.get("outcome")
    if et == "task.completed":
        return f"{title} marked done"
    if et == "task.skipped":
        if outcome == "refused":
            return f"{title} — horse refused"
        return f"{title} skipped"
    if et == "task.voided":
        return f"Completion of {title} reverted"
    if et == "task.created":
        return f"{title} scheduled"
    if et == "task.reassigned":
        return f"{title} reassigned"
    return title


async def _deliver_email(db, recipient_user_id: str, event: dict, mailer):
    """Send an email digest entry (very lightweight in P1)."""
    if mailer is None:
        return
    user = await db.users.find_one({"id": recipient_user_id}, {"_id": 0, "email": 1, "full_name": 1})
    if not user:
        return
    try:
        subject = f"Equine-Sync · {_summarize(event)}"
        body_text = f"Hi {user.get('full_name','there')},\n\n{_summarize(event)}\n\n— Equine-Sync"
        # Use the existing render+send pipeline; fall back to plain text body.
        mailer["send"](
            to=user["email"],
            subject=subject,
            html=(
                f"<p>Hi {user.get('full_name','there')},</p>"
                f"<p>{_summarize(event)}</p>"
                f'<p style="font-family:Georgia,serif">— '
                f'<span style="color:#232734">Equine-</span>'
                f'<span style="color:#6E5A99">Sync</span></p>'
            ),
            text=body_text,
        )
    except Exception:
        logger.exception("notification email failed for user=%s", recipient_user_id)


# ---------- core dispatch ----------

async def _candidate_recipients(db, event: dict) -> list[str]:
    """Resolve who should receive an event.

    Phase 1 single-tenant heuristics:
    - The actor (if present) gets no self-notification.
    - Same-barn non-actor admins/barn_managers receive inbox events by default.
    - Horse owners receive curated events only (filtered by category match).
    """
    actor = event.get("actor_user_id")
    barn_id = event.get("barn_id") or event.get("tenant_id")
    recipients = set()
    # Staff/admins
    staff_q = {"role": {"$in": ["admin", "barn_manager"]}}
    if barn_id:
        staff_q["barn_id"] = barn_id
    staff = await db.users.find(
        staff_q, {"_id": 0, "id": 1},
    ).to_list(100)
    for u in staff:
        recipients.add(u["id"])
    # Horse owners whose horses are subjects of this event — curated categories only
    subjects = event.get("subject_horse_ids") or []
    if subjects and event.get("category") in {"medication", "farrier", "vet", "rehab", "feed"}:
        horse_q = {"id": {"$in": subjects}}
        if barn_id:
            horse_q["barn_id"] = barn_id
        horses = await db.horses.find(
            horse_q, {"_id": 0, "owner_id": 1},
        ).to_list(200)
        owner_ids = [h.get("owner_id") for h in horses if h.get("owner_id")]
        if owner_ids:
            owner_q = {"id": {"$in": owner_ids}, "role": "horse_owner"}
            if barn_id:
                owner_q["barn_id"] = barn_id
            owner_users = await db.users.find(
                owner_q,
                {"_id": 0, "id": 1},
            ).to_list(200)
            for u in owner_users:
                recipients.add(u["id"])
    recipients.discard(actor)
    return list(recipients)


async def _dispatch_event(db, event: dict, mailer):
    recipients = await _candidate_recipients(db, event)
    channels_used = []
    for uid in recipients:
        prefs = await _get_user_prefs(db, uid)
        cat = event.get("category")
        et = event.get("event_type")
        inbox_ok = prefs.get("inbox_enabled") and _rule_matches(
            prefs.get("inbox_rules"), et, cat,
        )
        email_ok = prefs.get("email_enabled") and _rule_matches(
            prefs.get("email_rules"), et, cat,
        )
        if inbox_ok:
            await _deliver_inbox(db, uid, event)
            channels_used.append("inbox")
        if email_ok:
            await _deliver_email(db, uid, event, mailer)
            channels_used.append("email")
    await db.task_events.update_one(
        {"id": event["id"]},
        {"$set": {
            "dispatched_at": _iso(_now()),
            "dispatched_channels": list(set(channels_used)),
            "recipient_count": len(recipients),
        }},
    )


async def drain_once(db, mailer=None) -> int:
    """One pass: dispatch up to BATCH_SIZE undispatched events. Returns count.

    Transient-error tolerance (Batch C, Feb 2026): events that raise during
    dispatch are retried up to MAX_DISPATCH_ATTEMPTS times across polling
    cycles. Only after the cap do we mark them dispatched-with-error, so a
    momentary DB hiccup or email-provider blip no longer permanently drops
    an in-app notification.
    """
    cursor = db.task_events.find(
        {"dispatched_at": {"$exists": False}},
        {"_id": 0},
    ).sort("occurred_at", 1).limit(BATCH_SIZE)
    events = await cursor.to_list(BATCH_SIZE)
    for ev in events:
        try:
            await _dispatch_event(db, ev, mailer)
        except Exception:
            attempts = int(ev.get("dispatch_attempts") or 0) + 1
            logger.exception(
                "Notification dispatch failed for event=%s (attempt %d/%d)",
                ev.get("id"), attempts, MAX_DISPATCH_ATTEMPTS,
            )
            if attempts >= MAX_DISPATCH_ATTEMPTS:
                # Cap reached — finalise so we don't loop forever.
                await db.task_events.update_one(
                    {"id": ev["id"]},
                    {"$set": {
                        "dispatched_at": _iso(_now()),
                        "dispatched_channels": ["error"],
                        "dispatch_attempts": attempts,
                    }},
                )
            else:
                # Leave dispatched_at unset so the next poll picks it up again.
                await db.task_events.update_one(
                    {"id": ev["id"]},
                    {"$set": {
                        "dispatch_attempts": attempts,
                        "last_attempt_at": _iso(_now()),
                    }},
                )
    return len(events)


async def start_dispatcher(db, mailer=None):
    """Background loop. Cancelable via task cancellation."""
    await ensure_indexes(db)
    await asyncio.sleep(8)  # let server settle after startup
    while True:
        try:
            n = await drain_once(db, mailer)
            if n:
                logger.info("Notifications: dispatched %d events", n)
        except Exception:
            logger.exception("Notification loop failed")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


async def ensure_indexes(db):
    await db.notifications.create_index([("user_id", 1), ("created_at", -1)])
    await db.notifications.create_index([("user_id", 1), ("read_at", 1)])
    await db.notification_preferences.create_index([("user_id", 1)], unique=True)
    await db[PUSH_TOKEN_COLLECTION].create_index(
        [("user_id", 1), ("token_hash", 1)],
        unique=True,
    )
    await db[PUSH_TOKEN_COLLECTION].create_index([("user_id", 1), ("enabled", 1)])
    await db[PUSH_SEND_COLLECTION].create_index([("user_id", 1), ("created_at", -1)])
    await db.sms_consent_records.create_index([("user_id", 1), ("created_at", -1)])
    await db.sms_consent_records.create_index([("phone_hash", 1), ("created_at", -1)])
    await db.sms_delivery_events.create_index([("message_sid", 1), ("created_at", -1)])
    await db.sms_delivery_events.create_index([("phone_hash", 1), ("created_at", -1)])


# ---------- router ----------

def build_router(db, get_current_user) -> APIRouter:
    router = APIRouter()

    @router.get("/notifications")
    async def list_notifications(user=Depends(get_current_user),
                                  unread_only: bool = False, limit: int = 50):
        q = {"user_id": user["id"]}
        if unread_only:
            q["read_at"] = None
        items = await db.notifications.find(q, {"_id": 0}).sort("created_at", -1).limit(min(limit, 200)).to_list(min(limit, 200))
        unread = await db.notifications.count_documents({"user_id": user["id"], "read_at": None})
        return {"items": items, "unread": unread}

    @router.post("/notifications/{notif_id}/read")
    async def mark_read(notif_id: str, user=Depends(get_current_user)):
        r = await db.notifications.update_one(
            {"id": notif_id, "user_id": user["id"]},
            {"$set": {"read_at": _iso(_now())}},
        )
        if r.matched_count == 0:
            raise HTTPException(404, "Notification not found")
        return {"ok": True}

    @router.post("/notifications/read-all")
    async def mark_all_read(user=Depends(get_current_user)):
        await db.notifications.update_many(
            {"user_id": user["id"], "read_at": None},
            {"$set": {"read_at": _iso(_now())}},
        )
        return {"ok": True}

    @router.get("/notifications/preferences")
    async def get_prefs(user=Depends(get_current_user)):
        return await _get_user_prefs(db, user["id"])

    @router.put("/notifications/preferences")
    async def put_prefs(body: NotificationPrefsIn, user=Depends(get_current_user)):
        doc = body.model_dump(exclude_unset=True)
        doc["user_id"] = user["id"]
        doc["updated_at"] = _iso(_now())
        # Fill any missing fields with defaults so the doc is complete.
        existing = await _get_user_prefs(db, user["id"])
        for key in ("inbox_enabled", "email_enabled", "push_enabled",
                     "digest_enabled", "inbox_rules", "email_rules",
                     "sms_enabled", "sms_phone_number", "sms_phone_hash",
                     "sms_consent_status", "sms_consent_source",
                     "sms_consent_language"):
            doc.setdefault(key, existing.get(key))
        await db.notification_preferences.update_one(
            {"user_id": user["id"]}, {"$set": doc}, upsert=True,
        )
        return doc



    @router.put("/notifications/sms-consent")
    async def put_sms_consent(body: SmsConsentIn, user=Depends(get_current_user)):
        phone_e164 = _normalize_phone(body.phone_number) if body.sms_enabled else None
        if body.sms_enabled and not phone_e164:
            raise HTTPException(400, "Phone number is required for SMS opt-in")
        now = _iso(_now())
        status = "opted_in" if body.sms_enabled else "opted_out"
        source = (body.source or "contact_preferences")[:80]
        phone_hash = _hash_value(phone_e164)
        pref_update = {
            "user_id": user["id"],
            "sms_enabled": body.sms_enabled,
            "sms_phone_number": phone_e164,
            "sms_phone_hash": phone_hash,
            "sms_consent_status": status,
            "sms_consent_source": source,
            "sms_consent_language": SMS_CONSENT_LANGUAGE,
            "sms_consent_updated_at": now,
            "updated_at": now,
        }
        await db.notification_preferences.update_one(
            {"user_id": user["id"]}, {"$set": pref_update}, upsert=True,
        )
        await db.sms_consent_records.insert_one({
            "id": _new_id(),
            "user_id": user["id"],
            "role": user.get("role"),
            "barn_id": user.get("barn_id"),
            "phone_hash": phone_hash,
            "status": status,
            "source": source,
            "consent_language": SMS_CONSENT_LANGUAGE,
            "created_at": now,
        })
        return {
            "ok": True,
            "sms_enabled": body.sms_enabled,
            "sms_consent_status": status,
            "sms_phone_hash": phone_hash,
            "sms_consent_language": SMS_CONSENT_LANGUAGE,
        }

    @router.post("/notifications/sms/inbound")
    async def sms_inbound(
        From: str = Form(...),  # noqa: N803 - Twilio form key
        Body: str = Form(""),  # noqa: N803 - Twilio form key
        MessageSid: str = Form(""),  # noqa: N803 - Twilio form key
    ):
        phone_e164 = _normalize_phone(From)
        body = (Body or "").strip().upper()
        now = _iso(_now())
        phone_hash = _hash_value(phone_e164)
        await db.sms_delivery_events.insert_one({
            "id": _new_id(),
            "message_sid": MessageSid,
            "direction": "inbound",
            "phone_hash": phone_hash,
            "keyword": body[:20],
            "created_at": now,
        })
        if body in {"STOP", "STOPALL", "UNSUBSCRIBE", "CANCEL", "END", "QUIT"}:
            await db.notification_preferences.update_many(
                {"sms_phone_hash": phone_hash},
                {"$set": {
                    "sms_enabled": False,
                    "sms_consent_status": "opted_out",
                    "sms_consent_updated_at": now,
                    "updated_at": now,
                }},
            )
            await db.sms_consent_records.insert_one({
                "id": _new_id(),
                "phone_hash": phone_hash,
                "status": "opted_out",
                "source": "twilio_keyword",
                "keyword": body,
                "created_at": now,
            })
            return _twiml(SMS_OPTOUT_MESSAGE)
        if body in {"START", "YES", "UNSTOP"}:
            await db.notification_preferences.update_many(
                {"sms_phone_hash": phone_hash},
                {"$set": {
                    "sms_enabled": True,
                    "sms_consent_status": "opted_in",
                    "sms_consent_source": "twilio_keyword",
                    "sms_consent_language": SMS_OPTIN_MESSAGE,
                    "sms_consent_updated_at": now,
                    "updated_at": now,
                }},
            )
            await db.sms_consent_records.insert_one({
                "id": _new_id(),
                "phone_hash": phone_hash,
                "status": "opted_in",
                "source": "twilio_keyword",
                "keyword": body,
                "consent_language": SMS_OPTIN_MESSAGE,
                "created_at": now,
            })
            return _twiml(SMS_OPTIN_MESSAGE)
        if body == "HELP":
            return _twiml(SMS_HELP_MESSAGE)
        return Response(content="", media_type="application/xml")

    @router.post("/notifications/sms/status")
    async def sms_status_callback(
        MessageSid: str = Form(""),  # noqa: N803 - Twilio form key
        MessageStatus: str = Form(""),  # noqa: N803 - Twilio form key
        To: str = Form(""),  # noqa: N803 - Twilio form key
        ErrorCode: str = Form(""),  # noqa: N803 - Twilio form key
    ):
        phone_e164 = _normalize_phone(To) if To else None
        await db.sms_delivery_events.insert_one({
            "id": _new_id(),
            "message_sid": MessageSid,
            "direction": "status_callback",
            "status": MessageStatus,
            "phone_hash": _hash_value(phone_e164),
            "error_code": ErrorCode or None,
            "created_at": _iso(_now()),
        })
        return {"ok": True}

    @router.post("/notifications/sms/proof-send")
    async def sms_proof_send(body: SmsProofSendIn, user=Depends(get_current_user)):
        if user.get("role") not in ("admin", "platform_admin"):
            raise HTTPException(403, "Admin only")
        if not _sms_send_enabled() or not _is_sms_configured():
            raise HTTPException(409, "Twilio SMS sending is not enabled/configured")
        phone_e164 = _normalize_phone(body.phone_number)
        message = _safe_sms_body(body.message or PRIVACY_SAFE_PROOF_MESSAGE)
        now = _iso(_now())
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_user, auth_secret = _twilio_basic_auth()
        data = {
            "To": phone_e164,
            "MessagingServiceSid": os.environ["TWILIO_MESSAGING_SERVICE_SID"],
            "Body": message,
        }
        if os.environ.get("TWILIO_STATUS_CALLBACK_URL"):
            data["StatusCallback"] = os.environ["TWILIO_STATUS_CALLBACK_URL"]
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json",
                data=data,
                auth=(auth_user, auth_secret),
            )
        if resp.status_code >= 400:
            await db.sms_delivery_events.insert_one({
                "id": _new_id(),
                "direction": "outbound_proof",
                "status": "provider_error",
                "phone_hash": _hash_value(phone_e164),
                "body_hash": _hash_value(message),
                "provider_status": resp.status_code,
                "created_at": now,
            })
            raise HTTPException(502, "Twilio provider send failed")
        payload = resp.json()
        await db.sms_delivery_events.insert_one({
            "id": _new_id(),
            "message_sid": payload.get("sid"),
            "direction": "outbound_proof",
            "status": payload.get("status"),
            "phone_hash": _hash_value(phone_e164),
            "body_hash": _hash_value(message),
            "created_at": now,
        })
        return {
            "ok": True,
            "message_sid_hash": _hash_value(payload.get("sid")),
            "phone_hash": _hash_value(phone_e164),
            "status": payload.get("status"),
        }

    @router.post("/notifications/push-token")
    async def register_push_token(body: PushTokenIn, user=Depends(get_current_user)):
        await ensure_indexes(db)
        now = _iso(_now())
        token_hash = _token_hash(body.expo_push_token)
        doc = {
            "user_id": user["id"],
            "barn_id": user.get("barn_id"),
            "role": user.get("role"),
            "provider": "expo",
            "platform": body.platform,
            "device_id": body.device_id,
            "permission_status": body.permission_status,
            "expo_push_token": body.expo_push_token,
            "token_hash": token_hash,
            "token_hash_short": token_hash[:12],
            "enabled": body.enabled,
            "privacy_policy": "generic_previews_only",
            "updated_at": now,
        }
        await db[PUSH_TOKEN_COLLECTION].update_one(
            {"user_id": user["id"], "token_hash": token_hash},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True,
        )
        return {
            "ok": True,
            "provider": "expo",
            "platform": body.platform,
            "enabled": body.enabled,
            "token_hash": token_hash[:12],
        }

    @router.post("/notifications/push-token/disable")
    async def disable_push_tokens(user=Depends(get_current_user)):
        now = _iso(_now())
        result = await db[PUSH_TOKEN_COLLECTION].update_many(
            {"user_id": user["id"], "enabled": True},
            {"$set": {"enabled": False, "disabled_at": now, "updated_at": now}},
        )
        return {"ok": True, "disabled_count": result.modified_count}

    @router.post("/notifications/push-proof/send-me")
    async def send_push_proof_to_self(user=Depends(get_current_user)):
        if user.get("role") not in ("admin", "barn_manager"):
            raise HTTPException(403, "Admin/Manager only")
        token_doc = await db[PUSH_TOKEN_COLLECTION].find_one(
            {"user_id": user["id"], "provider": "expo", "enabled": True},
            sort=[("updated_at", -1)],
        )
        if not token_doc:
            raise HTTPException(404, "No enabled Expo push token registered")

        payload = {
            "to": token_doc["expo_push_token"],
            "sound": "default",
            "title": PUSH_PROOF_TITLE,
            "body": PUSH_PROOF_BODY,
            "data": PUSH_PROOF_DATA,
        }
        now = _iso(_now())
        record = {
            "id": _new_id(),
            "user_id": user["id"],
            "token_hash": token_doc.get("token_hash"),
            "provider": "expo",
            "purpose": "founder_push_proof",
            "privacy_policy": "generic_previews_only",
            "created_at": now,
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.post(EXPO_PUSH_SEND_URL, json=payload)
            provider_payload = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
            ticket = provider_payload.get("data") if isinstance(provider_payload, dict) else None
            ticket_status = ticket.get("status") if isinstance(ticket, dict) else None
            record.update(
                {
                    "http_status": response.status_code,
                    "provider_ok": response.status_code < 400 and ticket_status in (None, "ok"),
                    "provider_response_shape": "json" if provider_payload else "non_json",
                    "ticket_status": ticket_status,
                    "ticket_id_present": bool(isinstance(ticket, dict) and ticket.get("id")),
                    **_expo_ticket_diagnostics(ticket),
                }
            )
            await db[PUSH_SEND_COLLECTION].insert_one(record)
            if response.status_code >= 400:
                raise HTTPException(502, "Expo push provider rejected proof send")
            if ticket_status and ticket_status != "ok":
                raise HTTPException(502, "Expo push proof ticket returned an error")
        except HTTPException:
            raise
        except Exception:
            logger.exception(
                "Expo push proof failed for user=%s token_hash=%s",
                user.get("id"),
                token_doc.get("token_hash_short"),
            )
            record.update({"provider_ok": False, "error": "send_failed"})
            await db[PUSH_SEND_COLLECTION].insert_one(record)
            raise HTTPException(502, "Expo push proof failed")

        return {
            "ok": True,
            "provider": "expo",
            "purpose": "founder_push_proof",
            "token_hash": token_doc.get("token_hash_short") or _redact_token_hash(token_doc["expo_push_token"]),
            "message": PUSH_PROOF_BODY,
        }

    @router.post("/notifications/drain")
    async def manual_drain(user=Depends(get_current_user)):
        if user.get("role") not in ("admin", "barn_manager"):
            raise HTTPException(403, "Admin/Manager only")
        n = await drain_once(db)
        return {"drained": n}

    return router
