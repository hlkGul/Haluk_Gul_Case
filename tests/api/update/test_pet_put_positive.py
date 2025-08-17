import pytest


def test_update_pet_positive(pet_api):
    payload = {
        "id": 5,
        "category": {"id": 0, "name": "street"},
        "name": "updated-five",
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "tag"}],
        "status": "sold",
    }

    update_resp = pet_api.update(payload)
    assert update_resp.status_code in (200, 201)

    ctype = (update_resp.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        updated = update_resp.json()
        assert updated.get("id") == 5
        assert updated.get("name") == payload["name"]
        assert updated.get("status") == payload["status"]

def test_update_pet_idempotent_payload(pet_api, new_pet_payload):
    
    create_resp = pet_api.create(new_pet_payload)
    assert create_resp.status_code in (200, 201)

    pet = create_resp.json()
    pet_id = pet["id"]

    update_resp = pet_api.update(pet)
    assert update_resp.status_code in (200, 201)

    updated = update_resp.json()
    assert updated["id"] == pet_id
    assert updated["name"] == pet["name"]
    assert updated["status"] == pet["status"]
    assert isinstance(updated.get("photoUrls"), list)
    assert isinstance(updated.get("tags"), list)

    del_resp = pet_api.delete(pet_id)
    assert del_resp.status_code in (200, 404)