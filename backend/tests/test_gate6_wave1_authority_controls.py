from __future__ import annotations

from core.auth import create_token


def _auth_headers(user_id: str, role: str = "admin", barn_id: str = "barn_wave1"):
    return {
        "Authorization": f"Bearer {create_token(user_id, role, barn_id)}",
        "Content-Type": "application/json",
    }


def _seed_admin(db, user_id: str = "wave1_admin", barn_id: str = "barn_wave1"):
    db.barns.insert_one({"id": barn_id, "name": "Wave 1 Barn", "status": "active"})
    db.users.insert_one({
        "id": user_id,
        "email": f"{user_id}@example.test",
        "full_name": "Wave One Admin",
        "role": "admin",
        "barn_id": barn_id,
        "email_verified": True,
        "account_status": "active",
        "role_status": "active",
    })
    return _auth_headers(user_id, barn_id=barn_id)


def _arena_payload(**overrides):
    data = {
        "arena_name": "Indoor",
        "title": "Private use",
        "date": "2026-09-10",
        "start_time": "10:00",
        "end_time": "11:00",
        "status": "reserved",
        "visibility": "staff_only",
    }
    data.update(overrides)
    return {"data": data}


def test_gate6_wave1_authority_controls(client, isolated_app_database):
    headers = _seed_admin(isolated_app_database)

    first = client.post("/api/feature-modules/arena-schedule/records", headers=headers, json=_arena_payload())
    assert first.status_code == 200, first.text
    assert first.json()["data"]["conflict_state"] == "clear"

    unclassified = client.post(
        "/api/feature-modules/arena-schedule/records",
        headers=headers,
        json=_arena_payload(title="Unclassified overlap"),
    )
    assert unclassified.status_code == 409
    assert unclassified.json()["detail"]["code"] == "calendar_conflict_review_required"

    isolated_app_database.service_requests.insert_one({
        "id": "arena_request_conflict",
        "barn_id": "barn_wave1",
        "horse_id": "horse_request",
        "horse_name": "Request Horse",
        "type": "arena_use",
        "requested_by": "owner_wave1",
        "requester_name": "Owner Wave",
        "status": "pending",
        "requested_date": "2026-09-10",
        "requested_time": "10:00",
        "rental_duration": "1_hour",
        "arena_name": "Indoor",
    })
    service_request_approval = client.post(
        "/api/service-requests/arena_request_conflict/approve",
        headers=headers,
    )
    assert service_request_approval.status_code == 409
    assert service_request_approval.json()["detail"]["code"] == "calendar_conflict_review_required"

    group = client.post(
        "/api/feature-modules/arena-schedule/records",
        headers=headers,
        json=_arena_payload(title="Group lesson", booking_mode="group_lesson"),
    )
    assert group.status_code == 200, group.text
    assert group.json()["data"]["conflict_state"] == "allowed_overlap"

    override = client.post(
        "/api/feature-modules/arena-schedule/records",
        headers=headers,
        json=_arena_payload(
            title="Manager override",
            conflict_override_reason="Trainer confirmed capacity and shared-arena safety.",
        ),
    )
    assert override.status_code == 200, override.text
    assert override.json()["data"]["conflict_state"] == "override_accepted"

    isolated_app_database.riders.insert_one({
        "id": "rider_wave1",
        "barn_id": "barn_wave1",
        "full_name": "Wave Rider",
        "minor_status": "adult",
    })
    isolated_app_database.horses.insert_one({
        "id": "horse_wave1",
        "barn_id": "barn_wave1",
        "name": "Wave Horse",
        "status": "active",
        "safety_stop_active": True,
    })

    lesson = client.post(
        "/api/lessons",
        headers=headers,
        json={
            "rider_id": "rider_wave1",
            "horse_id": "horse_wave1",
            "start_time": "2026-09-10T10:00:00Z",
        },
    )
    assert lesson.status_code == 409
    assert lesson.json()["detail"] == "Safety Stop blocks lesson/training participation"

    training = client.post(
        "/api/training",
        headers=headers,
        json={
            "horse_id": "horse_wave1",
            "date": "2026-09-10T10:00:00Z",
            "discipline": "flatwork",
        },
    )
    assert training.status_code == 409
    assert training.json()["detail"] == "Safety Stop blocks lesson/training participation"

    isolated_app_database.horses.insert_many([
        {"id": "horse_target", "barn_id": "barn_wave1", "name": "Target", "status": "active", "owner_id": "owner_old"},
        {"id": "horse_source", "barn_id": "barn_wave1", "name": "Duplicate", "status": "active"},
    ])

    passport = client.post(
        "/api/horses/horse_target/passport",
        headers=headers,
        json={"passport_number": "P-123", "microchip_number": "985141000000001"},
    )
    assert passport.status_code == 200, passport.text
    assert passport.json()["lifecycle_state"] == "passport_recorded"

    correction = client.post(
        "/api/horses/horse_target/corrections",
        headers=headers,
        json={"reason": "Founder Wave 1 regression", "updates": {"breed": "Warmblood"}},
    )
    assert correction.status_code == 200, correction.text
    assert correction.json()["status"] == "applied"
    assert isolated_app_database.horses.find_one({"id": "horse_target"})["breed"] == "Warmblood"

    merge = client.post(
        "/api/horses/horse_target/merge",
        headers=headers,
        json={"source_horse_id": "horse_source", "reason": "Duplicate profile"},
    )
    assert merge.status_code == 200, merge.text
    source = isolated_app_database.horses.find_one({"id": "horse_source"})
    assert source["lifecycle_state"] == "merged"
    assert source["merged_into_horse_id"] == "horse_target"

    transfer = client.post(
        "/api/horses/horse_target/transfer",
        headers=headers,
        json={"to_owner_id": "owner_new", "reason": "Sale paperwork complete"},
    )
    assert transfer.status_code == 200, transfer.text
    assert transfer.json()["status"] == "pending"
    target = isolated_app_database.horses.find_one({"id": "horse_target"})
    assert target["transfer_state"] == "pending"
    assert target["pending_owner_id"] == "owner_new"

    assert isolated_app_database.horse_lifecycle_events.count_documents({"horse_id": "horse_target"}) == 4
