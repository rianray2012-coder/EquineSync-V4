from __future__ import annotations

from core.auth import create_token


BARN_ID = "barn_gate6_billing"


def _auth_headers(user_id: str, role: str, barn_id: str = BARN_ID):
    return {
        "Authorization": f"Bearer {create_token(user_id, role, barn_id)}",
        "Content-Type": "application/json",
    }


def _seed_billing_authority_fixture(db):
    db.barns.insert_one({"id": BARN_ID, "name": "Gate 6 Billing Barn", "status": "active"})
    db.users.insert_many([
        {
            "id": "billing_admin",
            "email": "billing_admin@example.test",
            "full_name": "Billing Admin",
            "role": "admin",
            "barn_id": BARN_ID,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
        {
            "id": "billing_manager",
            "email": "billing_manager@example.test",
            "full_name": "Billing Manager",
            "role": "barn_manager",
            "barn_id": BARN_ID,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
        {
            "id": "owner_one",
            "email": "owner_one@example.test",
            "full_name": "Owner One",
            "role": "horse_owner",
            "barn_id": BARN_ID,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
        {
            "id": "owner_two",
            "email": "owner_two@example.test",
            "full_name": "Owner Two",
            "role": "horse_owner",
            "barn_id": BARN_ID,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
    ])
    db.invoices.insert_many([
        {
            "id": "invoice-owner-one",
            "barn_id": BARN_ID,
            "owner_id": "owner_one",
            "items": [{"description": "Board", "amount": 1200}],
            "subtotal": 1200,
            "discount": 0,
            "tax_rate": 0,
            "tax_amount": 0,
            "total": 1200,
            "due_date": "2026-09-01",
            "status": "open",
        },
        {
            "id": "invoice-owner-two",
            "barn_id": BARN_ID,
            "owner_id": "owner_two",
            "items": [{"description": "Training", "amount": 900}],
            "subtotal": 900,
            "discount": 0,
            "tax_rate": 0,
            "tax_amount": 0,
            "total": 900,
            "due_date": "2026-09-05",
            "status": "open",
        },
        {
            "id": "invoice-manager",
            "barn_id": BARN_ID,
            "owner_id": "manager_account",
            "items": [{"description": "Farrier", "amount": 180}],
            "subtotal": 180,
            "discount": 0,
            "tax_rate": 0,
            "tax_amount": 0,
            "total": 180,
            "due_date": "2026-09-06",
            "status": "open",
        },
        {
            "id": "invoice-other-barn",
            "barn_id": "other_barn",
            "owner_id": "owner_one",
            "items": [{"description": "Hidden", "amount": 1}],
            "subtotal": 1,
            "discount": 0,
            "tax_rate": 0,
            "tax_amount": 0,
            "total": 1,
            "due_date": "2026-09-07",
            "status": "open",
        },
    ])


def test_gate6_owner_cannot_mark_own_invoice_paid(client, isolated_app_database):
    _seed_billing_authority_fixture(isolated_app_database)

    response = client.post(
        "/api/invoices/invoice-owner-one/pay",
        headers=_auth_headers("owner_one", "horse_owner"),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Financial role required"
    assert isolated_app_database.invoices.find_one({"id": "invoice-owner-one"})["status"] == "open"


def test_gate6_owner_cannot_mark_another_owner_invoice_paid(client, isolated_app_database):
    _seed_billing_authority_fixture(isolated_app_database)

    response = client.post(
        "/api/invoices/invoice-owner-two/pay",
        headers=_auth_headers("owner_one", "horse_owner"),
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Financial role required"
    assert isolated_app_database.invoices.find_one({"id": "invoice-owner-two"})["status"] == "open"


def test_gate6_cross_barn_invoice_pay_still_404_without_mutation(client, isolated_app_database):
    _seed_billing_authority_fixture(isolated_app_database)

    response = client.post(
        "/api/invoices/invoice-other-barn/pay",
        headers=_auth_headers("owner_one", "horse_owner"),
    )

    assert response.status_code == 404
    assert isolated_app_database.invoices.find_one({"id": "invoice-other-barn"})["status"] == "open"


def test_gate6_admin_and_manager_retain_bookkeeping_mark_paid(client, isolated_app_database):
    _seed_billing_authority_fixture(isolated_app_database)

    admin_response = client.post(
        "/api/invoices/invoice-owner-one/pay",
        headers=_auth_headers("billing_admin", "admin"),
    )
    manager_response = client.post(
        "/api/invoices/invoice-manager/pay",
        headers=_auth_headers("billing_manager", "barn_manager"),
    )

    assert admin_response.status_code == 200, admin_response.text
    assert admin_response.json()["status"] == "paid"
    assert manager_response.status_code == 200, manager_response.text
    assert manager_response.json()["status"] == "paid"
    assert isolated_app_database.invoices.find_one({"id": "invoice-owner-one"})["paid_at"]
    assert isolated_app_database.invoices.find_one({"id": "invoice-manager"})["paid_at"]


def test_gate6_owner_invoice_reads_remain_owner_scoped(client, isolated_app_database):
    _seed_billing_authority_fixture(isolated_app_database)

    response = client.get("/api/invoices", headers=_auth_headers("owner_one", "horse_owner"))

    assert response.status_code == 200, response.text
    ids = {invoice["id"] for invoice in response.json()}
    assert ids == {"invoice-owner-one"}
