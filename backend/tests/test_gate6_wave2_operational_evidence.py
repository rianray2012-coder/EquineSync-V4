from __future__ import annotations

from core.auth import create_token


def _auth_headers(user_id: str = "wave2_admin", role: str = "admin", barn_id: str = "barn_wave2"):
    return {
        "Authorization": f"Bearer {create_token(user_id, role, barn_id)}",
        "Content-Type": "application/json",
    }


def _seed_wave2(db):
    barn_id = "barn_wave2"
    user_id = "wave2_admin"
    db.barns.insert_one({"id": barn_id, "name": "Wave 2 Barn", "status": "active"})
    db.users.insert_many([
        {
            "id": user_id,
            "email": "wave2_admin@example.test",
            "full_name": "Wave Two Admin",
            "role": "admin",
            "barn_id": barn_id,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
        {
            "id": "trainer_original",
            "email": "trainer_original@example.test",
            "full_name": "Original Trainer",
            "role": "trainer",
            "barn_id": barn_id,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
        {
            "id": "trainer_sub",
            "email": "trainer_sub@example.test",
            "full_name": "Substitute Trainer",
            "role": "trainer",
            "barn_id": barn_id,
            "email_verified": True,
            "account_status": "active",
            "role_status": "active",
        },
    ])
    db.riders.insert_many([
        {"id": "rider_original", "barn_id": barn_id, "full_name": "Original Rider", "minor_status": "adult"},
        {"id": "rider_sub", "barn_id": barn_id, "full_name": "Substitute Rider", "minor_status": "adult"},
    ])
    db.horses.insert_many([
        {"id": "horse_original", "barn_id": barn_id, "name": "Original Horse", "status": "active"},
        {"id": "horse_sub", "barn_id": barn_id, "name": "Substitute Horse", "status": "active"},
    ])
    return _auth_headers(user_id=user_id, barn_id=barn_id)


def test_gate6_wave2_operational_evidence(client, isolated_app_database):
    headers = _seed_wave2(isolated_app_database)

    isolated_app_database.tasks.insert_one({
        "id": "task_wave2",
        "tenant_id": "default",
        "barn_id": "barn_wave2",
        "category": "care",
        "title": "Wrap leg and upload photo",
        "linked_horse_ids": ["horse_original"],
        "linked_location_id": None,
        "assignee_user_id": "wave2_admin",
        "assignee_role": None,
        "scheduled_at": "2026-09-15T14:00:00+00:00",
        "window_start": "2026-09-15T13:30:00+00:00",
        "window_end": "2026-09-15T16:00:00+00:00",
        "priority": "standard",
        "status": "scheduled",
        "payload": {},
        "notes": None,
        "created_at": "2026-09-15T13:00:00+00:00",
        "updated_at": "2026-09-15T13:00:00+00:00",
    })

    completion = client.post(
        "/api/tasks/task_wave2/complete",
        headers=headers,
        json={
            "client_completion_id": "wave2-completion-001",
            "outcome": "done",
            "payload_actual": {"media_ids": ["media_payload"]},
            "media_ids": ["media_direct", "media_payload"],
            "evidence_attachments": [
                {
                    "type": "document",
                    "document_url": "https://example.invalid/wave2-evidence.pdf",
                    "label": "Bandage photo packet",
                }
            ],
            "notes": "Evidence attached at completion.",
        },
    )
    assert completion.status_code == 200, completion.text
    completion_doc = completion.json()["completion"]
    assert completion_doc["media_ids"] == ["media_direct", "media_payload"]
    assert completion_doc["evidence_attachments"][0]["label"] == "Bandage photo packet"
    assert isolated_app_database.task_evidence.count_documents({
        "task_id": "task_wave2",
        "completion_id": completion_doc["id"],
    }) == 3
    task_event = isolated_app_database.task_events.find_one({"task_id": "task_wave2"})
    assert task_event["payload_snapshot"]["media_ids"] == ["media_direct", "media_payload"]
    assert task_event["payload_snapshot"]["evidence_attachment_count"] == 1

    handoff = client.post(
        "/api/feature-modules/handoff-reports/records",
        headers=headers,
        json={
            "data": {
                "shift_date": "2026-09-15",
                "outgoing_staff_user_id": "wave2_admin",
                "incoming_staff_user_id": "trainer_sub",
                "summary": "Wrapped leg; evidence attached for incoming staff.",
                "linked_task_ids": ["task_wave2"],
                "evidence_completion_ids": [completion_doc["id"]],
                "signoff_user_ids": ["wave2_admin"],
                "status": "submitted",
            }
        },
    )
    assert handoff.status_code == 200, handoff.text
    handoff_doc = handoff.json()
    assert handoff_doc["data"]["handoff_state"] == "submitted"
    assert handoff_doc["data"]["linked_task_ids"] == ["task_wave2"]
    assert isolated_app_database.shift_handoff_links.count_documents({
        "handoff_report_id": handoff_doc["id"],
    }) == 3

    lesson_cancel = client.post(
        "/api/lessons",
        headers=headers,
        json={
            "rider_id": "rider_original",
            "horse_id": "horse_original",
            "trainer_id": "trainer_original",
            "start_time": "2026-09-16T10:00:00+00:00",
        },
    )
    assert lesson_cancel.status_code == 200, lesson_cancel.text
    lesson_cancelled = client.post(
        f"/api/lessons/{lesson_cancel.json()['id']}/cancel",
        headers=headers,
        json={"reason": "Storm closure"},
    )
    assert lesson_cancelled.status_code == 200, lesson_cancelled.text
    assert lesson_cancelled.json()["status"] == "cancelled"
    assert isolated_app_database.lesson_training_events.count_documents({
        "record_id": lesson_cancel.json()["id"],
        "event_type": "lesson.cancelled",
    }) == 1

    lesson_sub = client.post(
        "/api/lessons",
        headers=headers,
        json={
            "rider_id": "rider_original",
            "horse_id": "horse_original",
            "trainer_id": "trainer_original",
            "start_time": "2026-09-16T11:00:00+00:00",
        },
    )
    assert lesson_sub.status_code == 200, lesson_sub.text
    lesson_subbed = client.post(
        f"/api/lessons/{lesson_sub.json()['id']}/substitute",
        headers=headers,
        json={
            "substitute_trainer_id": "trainer_sub",
            "substitute_horse_id": "horse_sub",
            "substitute_rider_id": "rider_sub",
            "reason": "Original horse needs rest day.",
        },
    )
    assert lesson_subbed.status_code == 200, lesson_subbed.text
    lesson_subbed_doc = lesson_subbed.json()
    assert lesson_subbed_doc["trainer_id"] == "trainer_original"
    assert lesson_subbed_doc["horse_id"] == "horse_original"
    assert lesson_subbed_doc["rider_id"] == "rider_original"
    assert lesson_subbed_doc["substitution_state"] == "substituted"
    assert lesson_subbed_doc["substitute_trainer_id"] == "trainer_sub"
    assert lesson_subbed_doc["substitute_horse_id"] == "horse_sub"
    assert lesson_subbed_doc["substitute_rider_id"] == "rider_sub"

    training_cancel = client.post(
        "/api/training",
        headers=headers,
        json={
            "horse_id": "horse_original",
            "trainer_id": "trainer_original",
            "date": "2026-09-17T09:00:00+00:00",
            "discipline": "flatwork",
        },
    )
    assert training_cancel.status_code == 200, training_cancel.text
    training_cancelled = client.post(
        f"/api/training/{training_cancel.json()['id']}/cancel",
        headers=headers,
        json={"reason": "Arena footing closed"},
    )
    assert training_cancelled.status_code == 200, training_cancelled.text
    assert training_cancelled.json()["status"] == "cancelled"

    training_sub = client.post(
        "/api/training",
        headers=headers,
        json={
            "horse_id": "horse_original",
            "trainer_id": "trainer_original",
            "date": "2026-09-17T10:00:00+00:00",
            "discipline": "conditioning",
        },
    )
    assert training_sub.status_code == 200, training_sub.text
    training_subbed = client.post(
        f"/api/training/{training_sub.json()['id']}/substitute",
        headers=headers,
        json={
            "substitute_trainer_id": "trainer_sub",
            "substitute_horse_id": "horse_sub",
            "reason": "Trainer swap approved by manager.",
        },
    )
    assert training_subbed.status_code == 200, training_subbed.text
    training_subbed_doc = training_subbed.json()
    assert training_subbed_doc["trainer_id"] == "trainer_original"
    assert training_subbed_doc["horse_id"] == "horse_original"
    assert training_subbed_doc["substitution_state"] == "substituted"
    assert training_subbed_doc["substitute_trainer_id"] == "trainer_sub"
    assert training_subbed_doc["substitute_horse_id"] == "horse_sub"
    assert isolated_app_database.lesson_training_events.count_documents({}) == 4
