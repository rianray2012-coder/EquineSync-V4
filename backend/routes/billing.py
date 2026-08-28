"""routes/billing.py — invoice bookkeeping.

Extracted from routes/operations.py (Phase 3F) as a lift-and-shift of invoice
list/create + a mark-as-paid status flip.

Phase 9A update: invoice **create** now uses typed/normalized line items and is
server-authoritative on money — it computes `subtotal`/`discount`/`tax_rate`/
`tax_amount`/`total` from the line items and **ignores any client-supplied
total**. `/invoices/{id}/pay` remains bookkeeping-only (a status flip to
"paid"); list/scoping/audit behavior is unchanged.

Scope note: billing is intentionally **invoice bookkeeping only** — there is NO
payment processor (no Stripe/charges/subscriptions). A real payments integration
would be a separate, explicitly-scoped feature.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, ConfigDict

from core.tenancy import barn_filter, stamp_barn
from core import audit
from core.minor_safety import (
    DECISION_ALLOW,
    MINOR_STATUS_ADULT,
    MINOR_STATUS_MINOR_13_TO_17,
    MINOR_STATUS_UNDER_13,
    MINOR_STATUS_UNKNOWN,
    STUDENT_PROFILE_COLLECTION,
    WORKFLOW_PAYMENT,
    audit_safe_guardian_minor_metadata,
    guardian_minor_public_error_detail,
    guardian_minor_workflow_gate,
    load_guardian_minor_authority_rows,
    load_verified_guardian_linked_students,
    minor_status_for_student,
    normalize_minor_status,
    student_workflow_scope,
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


class LineItem(BaseModel):
    # extra="allow" preserves any legacy keys (e.g. a bare {"label","amount"})
    model_config = ConfigDict(extra="allow")
    description: Optional[str] = None
    label: Optional[str] = None        # legacy alias for description
    quantity: Optional[float] = None
    unit_amount: Optional[float] = None
    amount: Optional[float] = None


class InvoiceIn(BaseModel):
    owner_id: str
    horse_id: Optional[str] = None
    rider_id: Optional[str] = None
    student_profile_id: Optional[str] = None
    billing_agreement_id: Optional[str] = None
    guardian_guard_scope_reference: Optional[str] = None
    guardian_state_token: Optional[str] = None
    billing_policy_version: Optional[str] = None
    items: List[LineItem]
    # Accepted for backward-compatibility but IGNORED — the server computes the
    # authoritative total from the line items (Phase 9A).
    total: Optional[float] = None
    due_date: str
    status: str = "open"  # open, paid, overdue
    notes: Optional[str] = None
    discount: float = 0.0   # absolute amount, clamped to 0..subtotal
    tax_rate: float = 0.0   # percentage applied to (subtotal - discount)


_VALID_STATUS = {"open", "paid", "overdue"}
_FINANCIAL_ROLES = {"admin", "barn_manager"}


def _money(x) -> float:
    return round(float(x) + 0.0, 2)


def _line_amount(li: LineItem) -> float:
    """Resolve a single line's amount; legacy {amount} wins, else quantity×unit_amount."""
    for name, val in (("quantity", li.quantity), ("unit_amount", li.unit_amount), ("amount", li.amount)):
        if val is not None and float(val) < 0:
            raise HTTPException(422, f"Line item {name} cannot be negative")
    if li.amount is not None:
        amt = float(li.amount)
    elif li.quantity is not None and li.unit_amount is not None:
        amt = float(li.quantity) * float(li.unit_amount)
    else:
        raise HTTPException(422, "Each line item needs 'amount', or both 'quantity' and 'unit_amount'")
    return _money(amt)


def _normalize_line(li: LineItem) -> dict:
    d = li.model_dump(exclude_none=True)  # keeps legacy/extra keys
    d["amount"] = _line_amount(li)
    if d.get("description") is None and d.get("label") is not None:
        d["description"] = d["label"]  # mirror for clarity; original key preserved
    return d


def compute_money(items, discount, tax_rate):
    """Pure, server-authoritative money math over already-normalized line items.

    Shared by the invoice create path (9A) and the recurring-charge materializer
    (9B-2) so both compute identical numbers. ``items`` is a list of dicts each
    carrying a numeric ``amount``. Returns
    ``(subtotal, discount, tax_rate, tax_amount, total)``.
    """
    if discount is not None and float(discount) < 0:
        raise HTTPException(422, "Discount cannot be negative")
    if tax_rate is not None and float(tax_rate) < 0:
        raise HTTPException(422, "Tax rate cannot be negative")
    subtotal = _money(sum(float(li["amount"]) for li in items))
    disc = _money(min(float(discount or 0), subtotal))  # clamp 0..subtotal
    rate = float(tax_rate or 0)
    tax_amount = _money((subtotal - disc) * rate / 100.0)
    total = _money(subtotal - disc + tax_amount)
    return subtotal, disc, rate, tax_amount, total


def _compute_invoice(body: InvoiceIn):
    """Server-authoritative totals. Returns (items, subtotal, discount, tax_rate, tax_amount, total)."""
    items = [_normalize_line(li) for li in body.items]
    if not items:
        raise HTTPException(422, "An invoice needs at least one line item")
    subtotal, discount, tax_rate, tax_amount, total = compute_money(items, body.discount, body.tax_rate)
    return items, subtotal, discount, tax_rate, tax_amount, total


async def ensure_billing_indexes(db) -> None:
    """Phase 9B-2: partial unique index preventing duplicate recurring invoices.

    Enforces one invoice per ``(barn_id, recurring_charge_id, period_key)`` for
    materializer-generated invoices only (``source="recurring"``). Additive and
    idempotent — legacy/manual invoices have no ``source`` field and are excluded
    by the partial filter, so they never conflict.
    """
    await db.invoices.create_index(
        [("barn_id", 1), ("recurring_charge_id", 1), ("period_key", 1)],
        name="uniq_recurring_invoice_period",
        unique=True,
        partialFilterExpression={"source": "recurring"},
    )


def build_router(*, db, get_current_user, list_collection, clean, new_id) -> APIRouter:
    router = APIRouter(tags=["billing"])

    def _minor_status_from_age(age) -> str:
        try:
            years = int(age)
        except (TypeError, ValueError):
            return MINOR_STATUS_UNKNOWN
        if years < 13:
            return MINOR_STATUS_UNDER_13
        if years < 18:
            return MINOR_STATUS_MINOR_13_TO_17
        return MINOR_STATUS_ADULT

    async def _student_from_profile_id(user, student_profile_id):
        if not student_profile_id:
            return None
        return await db[STUDENT_PROFILE_COLLECTION].find_one(
            barn_filter(user, {"id": student_profile_id}),
            {"_id": 0},
        )

    async def _student_from_rider(user, rider: Optional[Dict[str, Any]]):
        if not rider:
            return None
        if rider.get("student_profile_id"):
            linked = await _student_from_profile_id(user, rider["student_profile_id"])
            if linked:
                return linked
            return {
                "id": rider["student_profile_id"],
                "barn_id": user.get("barn_id") or "primary",
                "minor_status": MINOR_STATUS_UNKNOWN,
            }
        minor_status = normalize_minor_status(rider.get("minor_status") or MINOR_STATUS_UNKNOWN)
        if minor_status == MINOR_STATUS_UNKNOWN and rider.get("age") is not None:
            minor_status = _minor_status_from_age(rider.get("age"))
        student = {
            "id": f"rider:{rider.get('id')}",
            "barn_id": rider.get("barn_id") or user.get("barn_id") or "primary",
            "birthdate": rider.get("birthdate"),
            "minor_status": minor_status,
        }
        student["minor_status"] = minor_status_for_student(student)
        return student

    async def _student_from_horse(user, horse_id):
        if not horse_id:
            return None
        horse = await db.horses.find_one(barn_filter(user, {"id": horse_id}), {"_id": 0})
        if not horse or not horse.get("rider_id"):
            return None
        rider = await db.riders.find_one(barn_filter(user, {"id": horse["rider_id"]}), {"_id": 0})
        return await _student_from_rider(user, rider)

    def _remember_student(students: list[Dict[str, Any]], seen: set[str], student: Optional[Dict[str, Any]]) -> None:
        if not student:
            return
        student_id = str(student.get("id") or "").strip()
        if student_id and student_id not in seen:
            students.append(student)
            seen.add(student_id)

    async def _students_for_payment_subjects(user, invoice_doc: dict) -> list[Dict[str, Any]]:
        students: list[Dict[str, Any]] = []
        seen: set[str] = set()
        _remember_student(students, seen, await _student_from_profile_id(user, invoice_doc.get("student_profile_id")))
        if invoice_doc.get("rider_id"):
            rider = await db.riders.find_one(barn_filter(user, {"id": invoice_doc["rider_id"]}), {"_id": 0})
            _remember_student(students, seen, await _student_from_rider(user, rider))
        _remember_student(students, seen, await _student_from_horse(user, invoice_doc.get("horse_id")))
        barn_id = user.get("barn_id") or invoice_doc.get("barn_id") or "primary"
        owner_id = str(invoice_doc.get("owner_id") or "").strip()
        if owner_id:
            owner = await db.users.find_one(barn_filter(user, {"id": owner_id}), {"_id": 0})
            _remember_student(students, seen, await _student_from_rider(user, owner if owner and owner.get("student_profile_id") else None))
            guardian_links = await load_verified_guardian_linked_students(
                db,
                barn_id=barn_id,
                guardian_user_id=owner_id,
            )
            for linked in guardian_links:
                _remember_student(students, seen, linked.get("student"))
        return students

    def _payment_scope_reference(students: list[Dict[str, Any]], invoice_doc: dict) -> str:
        explicit = str(invoice_doc.get("guardian_guard_scope_reference") or "").strip()
        if explicit:
            return explicit
        agreement = str(invoice_doc.get("billing_agreement_id") or "").strip()
        if agreement:
            return f"billing_agreement:{agreement}"
        guarded = [student for student in students if minor_status_for_student(student) != MINOR_STATUS_ADULT]
        if len(guarded) == 1:
            scoped = student_workflow_scope(guarded[0].get("id"), WORKFLOW_PAYMENT)
            if scoped:
                return scoped
        return f"invoice:{invoice_doc['id']}"

    async def _enforce_payment_guard(*, user, request: Request, invoice_doc: dict, action: str) -> Optional[Dict[str, Any]]:
        students = await _students_for_payment_subjects(user, invoice_doc)
        if not students:
            return
        barn_id = user.get("barn_id") or invoice_doc.get("barn_id") or "primary"
        scope_reference = _payment_scope_reference(students, invoice_doc)
        if all(minor_status_for_student(student) == MINOR_STATUS_ADULT for student in students):
            links, consents = [], []
        else:
            links, consents = await load_guardian_minor_authority_rows(
                db,
                barn_id=barn_id,
                student_profile_ids=[student.get("id") for student in students],
                workflow=WORKFLOW_PAYMENT,
            )
        expected_state_token = invoice_doc.get("guardian_guard_state_token")
        if action == "invoice.pay" and not expected_state_token and not all(
            minor_status_for_student(student) == MINOR_STATUS_ADULT for student in students
        ):
            expected_state_token = "__missing_guardian_guard_state_token__"
        gate = guardian_minor_workflow_gate(
            workflow=WORKFLOW_PAYMENT,
            students=students,
            guardian_links=links,
            workflow_consents=consents,
            barn_id=barn_id,
            scope_reference=scope_reference,
            policy_version=invoice_doc.get("guardian_guard_policy_version") or "billing-payment-v1",
            expected_state_token=expected_state_token,
            action=action,
        )
        if gate["decision"] == DECISION_ALLOW:
            invoice_doc["guardian_guard_scope_reference"] = scope_reference
            invoice_doc["guardian_guard_state_token"] = gate.get("state_token")
            return gate
        await audit.record(
            action="invoice.guardian_minor_payment_blocked",
            user=user,
            request=request,
            resource_type="invoice",
            resource_id=invoice_doc.get("id"),
            outcome="denied",
            status_code=403,
            metadata=audit_safe_guardian_minor_metadata(gate),
            _db=db,
        )
        raise HTTPException(status_code=403, detail=guardian_minor_public_error_detail(gate))

    # ---------------- Invoices ----------------

    @router.get("/invoices")
    async def list_invoices(user=Depends(get_current_user)):
        # Phase 7D-1: owner-scope — a horse_owner sees ONLY their own invoices
        # (still barn-scoped). Staff keep the full barn-scoped list (unchanged).
        extra = {"owner_id": user["id"]} if user.get("role") == "horse_owner" else {}
        return await list_collection("invoices", barn_filter(user, extra), sort_field="due_date")

    @router.post("/invoices")
    async def create_invoice(body: InvoiceIn, request: Request, user=Depends(get_current_user)):
        if body.status not in _VALID_STATUS:
            raise HTTPException(422, f"Invalid status; must be one of {sorted(_VALID_STATUS)}")
        items, subtotal, discount, tax_rate, tax_amount, total = _compute_invoice(body)
        invoice_id = new_id()
        doc = {
            "id": invoice_id,
            "owner_id": body.owner_id,
            "horse_id": body.horse_id,
            "rider_id": body.rider_id,
            "student_profile_id": body.student_profile_id,
            "billing_agreement_id": body.billing_agreement_id,
            "items": items,
            "subtotal": subtotal,
            "discount": discount,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "total": total,  # server-computed; client-supplied total ignored
            "due_date": body.due_date,
            "status": body.status,
            "notes": body.notes,
            "created_at": _iso(_now_utc()),
            "guardian_guard_scope_reference": body.guardian_guard_scope_reference,
            "guardian_guard_state_token": body.guardian_state_token,
            "guardian_guard_policy_version": body.billing_policy_version or "billing-payment-v1",
        }
        stamp_barn(user, doc)
        await _enforce_payment_guard(user=user, request=request, invoice_doc=doc, action="invoice.create")
        await db.invoices.insert_one(doc)
        return clean(doc)

    @router.post("/invoices/{invoice_id}/pay")
    async def pay_invoice(invoice_id: str, request: Request, user=Depends(get_current_user)):
        # Phase 4B-4: scope by id + barn so a cross-barn invoice 404s (no
        # existence leak / no mutation). Idempotent "set status=paid" preserved.
        scope = barn_filter(user, {"id": invoice_id})
        existing = await db.invoices.find_one(scope, {"_id": 0})
        if not existing:
            raise HTTPException(404, "Invoice not found")
        if user.get("role") not in _FINANCIAL_ROLES:
            raise HTTPException(403, "Financial role required")
        await _enforce_payment_guard(user=user, request=request, invoice_doc=existing, action="invoice.pay")
        await db.invoices.update_one(
            scope,
            {"$set": {
                "status": "paid",
                "paid_at": _iso(_now_utc()),
                "guardian_guard_scope_reference": existing.get("guardian_guard_scope_reference"),
                "guardian_guard_state_token": existing.get("guardian_guard_state_token"),
            }},
        )
        await audit.record(
            action="invoice.paid", user=user, request=request,
            resource_type="invoice", resource_id=invoice_id,
            metadata={"amount": existing.get("total")},
        )
        return await db.invoices.find_one(scope, {"_id": 0})

    return router
