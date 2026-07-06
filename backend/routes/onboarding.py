"""routes/onboarding.py — Onboarding wizard, barn setup, CSV import.

Phase-F extraction (Feb 20 2026). Single self-contained module; all
collaborators injected via build_router(). ONBOARDING_STEPS lives here
as the authoritative source — server.py re-imports it for the reports
and invites modules that also need to reference step ids.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr

from core.tenancy import barn_filter, resolve_barn_id
from core import audit


ONBOARDING_STEPS: List[Dict[str, Any]] = [
    {"id": "barn", "label": "Barn Profile", "required": True},
    {"id": "locations", "label": "Locations", "required": True},
    {"id": "owners", "label": "Owners & Clients", "required": True},
    {"id": "horses", "label": "Horse Profiles", "required": True},
    {"id": "riders", "label": "Riders", "required": False},
    {"id": "feed_templates", "label": "Feed Templates", "required": True},
    {"id": "inventory", "label": "Inventory", "required": False},
    {"id": "operations_setup", "label": "Operations & Sharing", "required": False},
    {"id": "staff", "label": "Team & Staff", "required": False},
    {"id": "schedules", "label": "Recurring Schedules", "required": False},
    {"id": "review", "label": "Review & Launch", "required": True},
]

BN16B_REQUIRED_STEP_IDS = (
    "barn",
    "locations",
    "owners",
    "horses",
    "feed_templates",
    "review",
)
BN16B_OPTIONAL_STEP_IDS = (
    "riders",
    "inventory",
    "operations_setup",
    "staff",
)
BN16B_DEFERRED_STEP_IDS = ("schedules",)
BN16B_COMPLETION_ROLES = {"admin", "barn_owner"}
BN16B_SETUP_ACCESS_ROLES = {"admin", "barn_owner", "barn_manager"}
_STEP_BY_ID = {step["id"]: step for step in ONBOARDING_STEPS}


class BarnSettings(BaseModel):
    name: Optional[str] = None
    facility_type: Optional[str] = None
    disciplines: Optional[List[str]] = []
    address: Optional[str] = None
    timezone: Optional[str] = "America/New_York"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    logo_url: Optional[str] = None
    banner_url: Optional[str] = None


class LocationIn(BaseModel):
    type: str
    name: str
    capacity: Optional[int] = 1
    notes: Optional[str] = None


class FeedTemplateIn(BaseModel):
    meal: str
    hay_type: Optional[str] = None
    hay_lbs: Optional[float] = 0
    grain_type: Optional[str] = None
    grain_lbs: Optional[float] = 0
    supplements: Optional[str] = None
    med_timing: Optional[str] = None
    instructions: Optional[str] = None


class InventoryIn(BaseModel):
    category: str
    name: str
    unit: str = "lbs"
    quantity: float = 0
    reorder_at: Optional[float] = 0
    vendor: Optional[str] = None
    cost_per_unit: Optional[float] = 0
    notes: Optional[str] = None


class RecurringScheduleIn(BaseModel):
    type: str
    name: str
    days_of_week: Optional[List[str]] = []
    time: Optional[str] = None
    location_id: Optional[str] = None
    notes: Optional[str] = None


class StaffInviteIn(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    permissions: Optional[List[str]] = []


class ProgressPatch(BaseModel):
    step_id: Optional[str] = None
    status: Optional[str] = None
    current_step: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


class CsvPreviewBody(BaseModel):
    kind: str
    csv_text: str


class CsvCommitBody(BaseModel):
    kind: str
    rows: List[Dict[str, Any]]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _deep_merge(base: dict, patch: dict) -> dict:
    """Recursively merge patch into base. dict values are merged, others replaced."""
    out = dict(base or {})
    for k, v in (patch or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _parse_csv(text: str) -> List[Dict[str, str]]:
    import csv
    import io
    reader = csv.DictReader(io.StringIO(text.strip()))
    return [{(k or "").strip().lower(): (v or "").strip() for k, v in row.items()}
            for row in reader]


def build_router(*, db, get_current_user, require_setup_role, roles: List[str],
                  list_collection, clean, new_id) -> APIRouter:
    router = APIRouter(tags=["onboarding"])

    # ---------- Wizard state ----------

    @router.get("/onboarding/steps")
    async def get_steps():
        return {"steps": ONBOARDING_STEPS}

    async def _ensure_progress(user) -> dict:
        doc = await db.onboarding_progress.find_one({"user_id": user["id"]}, {"_id": 0})
        if doc:
            step_ids = [s["id"] for s in ONBOARDING_STEPS]
            existing_steps = doc.get("steps") or {}
            normalized_steps = {sid: existing_steps.get(sid, "pending") for sid in step_ids}
            if normalized_steps != existing_steps:
                current_step = doc.get("current_step")
                if current_step not in step_ids:
                    current_step = ONBOARDING_STEPS[0]["id"]
                await db.onboarding_progress.update_one(
                    {"user_id": user["id"]},
                    {"$set": {
                        "steps": normalized_steps,
                        "current_step": current_step,
                        "barn_id": doc.get("barn_id") or resolve_barn_id(user),
                        "updated_at": _iso(_now_utc()),
                    }},
                )
                doc["steps"] = normalized_steps
                doc["current_step"] = current_step
                doc["barn_id"] = doc.get("barn_id") or resolve_barn_id(user)
            return doc
        doc = {
            "user_id": user["id"],
            "barn_id": resolve_barn_id(user),
            "steps": {s["id"]: "pending" for s in ONBOARDING_STEPS},
            "current_step": ONBOARDING_STEPS[0]["id"],
            "data": {},
            "completed": False,
            "created_at": _iso(_now_utc()),
            "updated_at": _iso(_now_utc()),
        }
        await db.onboarding_progress.insert_one(doc)
        doc.pop("_id", None)
        return doc

    async def _count_barn_docs(collection_name: str, barn_id: str) -> int:
        collection = getattr(db, collection_name)
        query = {"barn_id": barn_id}
        try:
            return await collection.count_documents(query)
        except AttributeError:
            rows = await collection.find(query, {"_id": 0, "id": 1}).to_list(1000)
            return len(rows)

    def _actor_role(user) -> str:
        return (user.get("role") or "").strip().lower()

    def _require_readiness_view(user) -> None:
        if _actor_role(user) not in BN16B_SETUP_ACCESS_ROLES:
            raise HTTPException(
                status_code=403,
                detail="Setup readiness requires a facility setup role.",
            )

    def _require_completion_role(user) -> None:
        if _actor_role(user) not in BN16B_COMPLETION_ROLES:
            raise HTTPException(
                status_code=403,
                detail="Setup completion requires a facility admin or barn owner role.",
            )

    def _step_label(step_id: str) -> str:
        return (_STEP_BY_ID.get(step_id) or {}).get("label") or step_id

    def _step_payload(step_id: str, *, status: str, required: bool = False,
                      deferred: bool = False, reason: Optional[str] = None) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "id": step_id,
            "label": _step_label(step_id),
            "status": status,
            "required": required,
            "deferred": deferred,
        }
        if reason:
            out["reason"] = reason
        return out

    async def _build_readiness(user) -> Dict[str, Any]:
        progress = await _ensure_progress(user)
        barn_id = resolve_barn_id(user)
        actor_role = _actor_role(user)
        steps = progress.get("steps") or {}

        barn = await db.barn.find_one({"id": barn_id}, {"_id": 0, "id": 1, "name": 1})
        counts = {
            "locations": await _count_barn_docs("locations", barn_id),
            "owners": await _count_barn_docs("owners", barn_id),
            "horses": await _count_barn_docs("horses", barn_id),
            "feed_templates": await _count_barn_docs("feed_templates", barn_id),
            "riders": await _count_barn_docs("riders", barn_id),
            "inventory": await _count_barn_docs("inventory", barn_id),
            "staff": await _count_barn_docs("staff_invites", barn_id),
        }

        required_statuses = {
            "barn": "complete" if (barn and (barn.get("name") or "").strip()) else "blocked",
            "locations": "complete" if counts["locations"] > 0 else "blocked",
            "owners": "complete" if counts["owners"] > 0 else "blocked",
            "horses": "complete" if counts["horses"] > 0 else "blocked",
            "feed_templates": "complete" if counts["feed_templates"] > 0 else "blocked",
            "review": "complete" if steps.get("review") == "complete" else "blocked",
        }
        required_reasons = {
            "barn": "Barn profile needs a saved name.",
            "locations": "Add at least one location.",
            "owners": "Add at least one owner or client.",
            "horses": "Add at least one horse profile.",
            "feed_templates": "Add at least one feed template.",
            "review": "Mark Review & Launch complete after checking setup.",
        }

        blockers = []
        required_steps = []
        for step_id in BN16B_REQUIRED_STEP_IDS:
            status = required_statuses[step_id]
            reason = None if status == "complete" else required_reasons[step_id]
            payload = _step_payload(step_id, status=status, required=True, reason=reason)
            required_steps.append(payload)
            if status != "complete":
                blockers.append({
                    "step_id": step_id,
                    "label": _step_label(step_id),
                    "reason": reason,
                    "severity": "blocker",
                })

        optional_steps = []
        optional_reason = "Optional setup item; does not block setup completion."
        for step_id in BN16B_OPTIONAL_STEP_IDS:
            status = "complete" if (steps.get(step_id) == "complete" or counts.get(step_id, 0) > 0) else "pending"
            optional_steps.append(_step_payload(step_id, status=status, reason=optional_reason))

        deferred_steps = [
            _step_payload(
                step_id,
                status="deferred",
                deferred=True,
                reason="Deferred until recurring schedule materialization is ready.",
            )
            for step_id in BN16B_DEFERRED_STEP_IDS
        ]

        required_completed = sum(1 for step in required_steps if step["status"] == "complete")
        can_finalize = actor_role in BN16B_COMPLETION_ROLES
        can_view = actor_role in BN16B_SETUP_ACCESS_ROLES
        return {
            "ok": True,
            "phase": "BN16B",
            "barn_id": barn_id,
            "user_id": user["id"],
            "actor_role": actor_role,
            "completion_scope": "barn",
            "can_view": can_view,
            "can_finalize": can_finalize,
            "can_complete": can_finalize and not blockers,
            "required_steps": required_steps,
            "optional_steps": optional_steps,
            "deferred_steps": deferred_steps,
            "blockers": blockers,
            "warnings": [],
            "progress": {
                "required_completed": required_completed,
                "required_total": len(BN16B_REQUIRED_STEP_IDS),
                "required_percent": round(100 * required_completed / len(BN16B_REQUIRED_STEP_IDS)),
            },
        }

    @router.get("/onboarding/progress")
    async def get_progress(user=Depends(get_current_user)):
        doc = await _ensure_progress(user)
        completed = sum(1 for v in doc.get("steps", {}).values() if v == "complete")
        doc["percent"] = round(100 * completed / len(ONBOARDING_STEPS))
        return doc

    @router.patch("/onboarding/progress")
    async def patch_progress(body: ProgressPatch, user=Depends(get_current_user)):
        doc = await db.onboarding_progress.find_one({"user_id": user["id"]})
        if not doc:
            await _ensure_progress(user)
            doc = await db.onboarding_progress.find_one({"user_id": user["id"]})
        update: Dict[str, Any] = {"updated_at": _iso(_now_utc())}
        if body.step_id and body.status:
            update[f"steps.{body.step_id}"] = body.status
        if body.current_step:
            update["current_step"] = body.current_step
        if body.data:
            existing = doc.get("data", {}) or {}
            update["data"] = _deep_merge(existing, body.data)
        await db.onboarding_progress.update_one({"user_id": user["id"]}, {"$set": update})
        fresh = await db.onboarding_progress.find_one({"user_id": user["id"]}, {"_id": 0})
        completed_steps = sum(1 for v in fresh.get("steps", {}).values() if v == "complete")
        fresh["percent"] = round(100 * completed_steps / len(ONBOARDING_STEPS))
        return fresh

    @router.get("/onboarding/readiness")
    async def get_readiness(user=Depends(get_current_user)):
        _require_readiness_view(user)
        return await _build_readiness(user)

    @router.post("/onboarding/complete")
    async def complete_onboarding(user=Depends(get_current_user)):
        _require_completion_role(user)
        readiness = await _build_readiness(user)
        if readiness["blockers"]:
            raise HTTPException(
                status_code=409,
                detail={
                    "message": "Setup is not ready to complete.",
                    "blockers": readiness["blockers"],
                    "progress": readiness["progress"],
                    "completion_scope": readiness["completion_scope"],
                },
            )
        await db.onboarding_progress.update_one(
            {"user_id": user["id"]},
            {"$set": {"completed": True, "completed_at": _iso(_now_utc())}},
        )
        return {"ok": True, "readiness": readiness}

    @router.post("/onboarding/reset")
    async def reset_onboarding(user=Depends(get_current_user)):
        await db.onboarding_progress.update_one(
            {"user_id": user["id"]},
            {"$set": {
                "barn_id": resolve_barn_id(user),
                "completed": False,
                "completed_at": None,
                "steps": {s["id"]: "pending" for s in ONBOARDING_STEPS},
                "current_step": ONBOARDING_STEPS[0]["id"],
                "updated_at": _iso(_now_utc()),
            }},
            upsert=True,
        )
        return {"ok": True}

    # ---------- Barn settings ----------

    @router.get("/barn")
    async def get_barn(user=Depends(get_current_user)):
        barn_id = resolve_barn_id(user)
        doc = await db.barn.find_one({"id": barn_id}, {"_id": 0})
        if not doc:
            doc = {"id": barn_id, "name": "", "facility_type": "boarding",
                   "disciplines": [], "address": "", "timezone": "America/New_York",
                   "contact_email": "", "contact_phone": "", "logo_url": "", "banner_url": ""}
        return doc

    @router.put("/barn")
    async def update_barn(body: BarnSettings, request: Request, user=Depends(get_current_user)):
        require_setup_role(user)
        barn_id = resolve_barn_id(user)
        doc = body.model_dump()
        doc["id"] = barn_id
        doc["updated_at"] = _iso(_now_utc())
        await db.barn.update_one({"id": barn_id}, {"$set": doc}, upsert=True)
        await audit.record(
            action="barn.settings.updated", user=user, request=request,
            resource_type="barn", resource_id=barn_id,
            metadata={"updated_fields": sorted(body.model_dump(exclude_unset=True).keys())},
        )
        return await db.barn.find_one({"id": barn_id}, {"_id": 0})

    # ---------- Locations ----------

    @router.get("/locations")
    async def list_locations(user=Depends(get_current_user)):
        return await list_collection("locations", barn_filter(user))

    @router.post("/locations")
    async def create_location(body: LocationIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        doc.update({"id": new_id(), "barn_id": resolve_barn_id(user), "created_at": _iso(_now_utc())})
        await db.locations.insert_one(doc)
        return clean(doc)

    @router.delete("/locations/{loc_id}")
    async def delete_location(loc_id: str, user=Depends(get_current_user)):
        await db.locations.delete_one(barn_filter(user, {"id": loc_id}))
        return {"ok": True}

    # ---------- Feed templates ----------

    @router.get("/feed-templates")
    async def list_feed_templates(user=Depends(get_current_user)):
        return await list_collection("feed_templates", barn_filter(user))

    @router.post("/feed-templates")
    async def create_feed_template(body: FeedTemplateIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        doc.update({"id": new_id(), "barn_id": resolve_barn_id(user), "created_at": _iso(_now_utc())})
        await db.feed_templates.insert_one(doc)
        return clean(doc)

    @router.delete("/feed-templates/{tid}")
    async def delete_feed_template(tid: str, user=Depends(get_current_user)):
        await db.feed_templates.delete_one(barn_filter(user, {"id": tid}))
        return {"ok": True}

    # ---------- Inventory ----------

    @router.get("/inventory")
    async def list_inventory(user=Depends(get_current_user)):
        items = await list_collection("inventory", barn_filter(user))
        for it in items:
            it["low_stock"] = (
                (it.get("reorder_at") or 0) > 0
                and (it.get("quantity") or 0) <= (it.get("reorder_at") or 0)
            )
        return items

    @router.post("/inventory")
    async def create_inventory(body: InventoryIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        doc.update({"id": new_id(), "barn_id": resolve_barn_id(user), "created_at": _iso(_now_utc())})
        await db.inventory.insert_one(doc)
        return clean(doc)

    @router.delete("/inventory/{iid}")
    async def delete_inventory(iid: str, user=Depends(get_current_user)):
        await db.inventory.delete_one(barn_filter(user, {"id": iid}))
        return {"ok": True}

    # ---------- Recurring Schedules ----------

    @router.get("/recurring-schedules")
    async def list_rs(user=Depends(get_current_user)):
        return await list_collection("recurring_schedules", barn_filter(user))

    @router.post("/recurring-schedules")
    async def create_rs(body: RecurringScheduleIn, user=Depends(get_current_user)):
        doc = body.model_dump()
        doc.update({"id": new_id(), "barn_id": resolve_barn_id(user), "created_at": _iso(_now_utc())})
        await db.recurring_schedules.insert_one(doc)
        return clean(doc)

    @router.delete("/recurring-schedules/{sid}")
    async def delete_rs(sid: str, user=Depends(get_current_user)):
        await db.recurring_schedules.delete_one(barn_filter(user, {"id": sid}))
        return {"ok": True}

    # ---------- Staff Invites (lightweight onboarding-side store) ----------

    @router.get("/staff-invites")
    async def list_invites(user=Depends(get_current_user)):
        return await list_collection("staff_invites", barn_filter(user))

    @router.post("/staff-invites")
    async def create_invite(body: StaffInviteIn, user=Depends(get_current_user)):
        require_setup_role(user)
        if body.role not in roles:
            raise HTTPException(400, "Invalid role")
        if await db.staff_invites.find_one(barn_filter(user, {"email": body.email.lower()})):
            raise HTTPException(409, "Already invited")
        if await db.users.find_one({"email": body.email.lower()}):
            raise HTTPException(409, "User already exists")
        doc = body.model_dump()
        doc["email"] = doc["email"].lower()
        doc.update({"id": new_id(), "status": "pending",
                    "barn_id": resolve_barn_id(user),
                    "invited_by": user["full_name"],
                    "created_at": _iso(_now_utc())})
        await db.staff_invites.insert_one(doc)
        return clean(doc)

    @router.delete("/staff-invites/{sid}")
    async def delete_invite(sid: str, user=Depends(get_current_user)):
        await db.staff_invites.delete_one(barn_filter(user, {"id": sid}))
        return {"ok": True}

    # ---------- CSV import ----------

    @router.post("/onboarding/csv-preview")
    async def csv_preview(body: CsvPreviewBody, user=Depends(get_current_user)):
        try:
            rows = _parse_csv(body.csv_text)
        except Exception as e:
            raise HTTPException(400, f"Invalid CSV: {e}")
        if not rows:
            return {"rows": [], "duplicates": [], "count": 0}

        duplicates: List[str] = []
        if body.kind == "horses":
            existing_names = {
                h["name"].lower()
                for h in await db.horses.find(barn_filter(user), {"_id": 0, "name": 1}).to_list(1000)
            }
            for r in rows:
                if (r.get("name") or "").lower() in existing_names:
                    duplicates.append(r.get("name"))
        elif body.kind == "owners":
            existing = {
                o.get("email", "").lower()
                for o in await db.owners.find(barn_filter(user), {"_id": 0, "email": 1}).to_list(1000)
            }
            for r in rows:
                if (r.get("email") or "").lower() in existing:
                    duplicates.append(r.get("email"))
        return {"rows": rows, "duplicates": duplicates, "count": len(rows)}

    @router.post("/onboarding/csv-commit")
    async def csv_commit(body: CsvCommitBody, user=Depends(get_current_user)):
        created = 0
        skipped = 0
        if body.kind == "horses":
            existing_names = {
                h["name"].lower()
                for h in await db.horses.find(barn_filter(user), {"_id": 0, "name": 1}).to_list(2000)
            }
            owners_map = {
                o.get("full_name", "").lower(): o["id"]
                for o in await db.owners.find(barn_filter(user), {"_id": 0}).to_list(2000)
            }

            def _maybe_int(v):
                try:
                    return int(float(v)) if v not in (None, "") else None
                except Exception:
                    return None

            def _maybe_float(v):
                try:
                    return float(v) if v not in (None, "") else None
                except Exception:
                    return None

            for r in body.rows:
                name = (r.get("name") or "").strip()
                if not name:
                    continue
                if name.lower() in existing_names:
                    skipped += 1
                    continue
                existing_names.add(name.lower())
                doc = {
                    "id": new_id(),
                    "barn_id": resolve_barn_id(user),
                    "name": name,
                    "barn_name": r.get("barn_name") or name,
                    "breed": r.get("breed"),
                    "age": _maybe_int(r.get("age")),
                    "color": r.get("color"),
                    "height_hands": _maybe_float(r.get("height_hands")),
                    "discipline": r.get("discipline"),
                    "stall": r.get("stall"),
                    "owner_id": (owners_map.get((r.get("owner") or "").lower())
                                 or owners_map.get((r.get("owner_name") or "").lower())),
                    "status": r.get("status") or "active",
                    "wellness_score": _maybe_int(r.get("wellness_score")) or 85,
                    "allergies": [a.strip() for a in (r.get("allergies") or "").split(";") if a.strip()],
                    "feed_plan": r.get("feed_plan"),
                    "turnout_group": r.get("turnout_group"),
                    "behavior_flags": [b.strip() for b in (r.get("behavior_flags") or "").split(";") if b.strip()],
                    "photo_url": r.get("photo_url"),
                    "created_at": _iso(_now_utc()),
                }
                await db.horses.insert_one(doc)
                created += 1
        elif body.kind == "owners":
            existing_emails = {
                o.get("email", "").lower()
                for o in await db.owners.find(barn_filter(user), {"_id": 0, "email": 1}).to_list(2000)
                if o.get("email")
            }
            for r in body.rows:
                name = (r.get("full_name") or r.get("name") or "").strip()
                email = (r.get("email") or "").strip().lower()
                if not name:
                    continue
                if email and email in existing_emails:
                    skipped += 1
                    continue
                if email:
                    existing_emails.add(email)
                doc = {
                    "id": new_id(),
                    "barn_id": resolve_barn_id(user),
                    "full_name": name,
                    "email": email or None,
                    "phone": r.get("phone"),
                    "horses": [],
                    "billing_preferences": r.get("billing_preferences"),
                    "emergency_contact": r.get("emergency_contact"),
                    "waiver_signed": (r.get("waiver_signed") or "").lower() in ("yes", "true", "1"),
                    "created_at": _iso(_now_utc()),
                }
                await db.owners.insert_one(doc)
                created += 1
        else:
            raise HTTPException(400, "Unsupported kind")
        return {"created": created, "skipped": skipped}

    @router.get("/onboarding/csv-template")
    async def csv_template(kind: str):
        templates = {
            "horses": "name,breed,age,color,height_hands,discipline,stall,owner,status,wellness_score,allergies,feed_plan,turnout_group,behavior_flags,photo_url\n",
            "owners": "full_name,email,phone,emergency_contact,billing_preferences,waiver_signed\n",
        }
        text = templates.get(kind)
        if not text:
            raise HTTPException(400, "Unknown template")
        return {"text": text, "filename": f"equinesync_{kind}_template.csv"}

    return router
