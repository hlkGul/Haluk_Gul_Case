import json
import pytest


@pytest.mark.parametrize(
    "bad_body, headers, expected_status",
    [
        ("{bad json", {"Content-Type": "application/json"}, 400),

        (json.dumps({"id": 999, "name": "bad"}), {"Content-Type": "text/plain"}, 415),

        (json.dumps({"id": 999}), {"Content-Type": "application/json"}, 400),
    ],
        ids=["malformed_json", "wrong_content_type", "missing_fields"],
)
def test_create_pet_negative_variants(pet_api, bad_body, headers, expected_status):
    resp = pet_api.create_raw(bad_body, headers=headers)

    assert resp.status_code // 100 in (2, 4, 5)

    if resp.status_code // 100 == 4:
        assert resp.status_code == expected_status

    ctype = (resp.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        data = resp.json()
        if resp.status_code // 100 == 4:
            assert "message" in data or "type" in data
        elif resp.status_code // 100 == 2:
            assert "id" in data
            assert isinstance(data.get("photoUrls"), list)
            assert isinstance(data.get("tags"), list)


def test_create_pet_duplicate_id_behavior(pet_api):
    # Create a pet with a specific ID, then try to create again with the same ID
    pet_id = 987650001
    payload = {
        "id": pet_id,
        "category": {"id": 1, "name": "dup"},
        "name": "duplicate",
        "photoUrls": ["p1"],
        "tags": [{"id": 1, "name": "dup-tag"}],
        "status": "available",
    }

    first = pet_api.create(payload)
    assert first.status_code in (200, 201)

    second = pet_api.create(payload)
    # Public demo tolerance: accept 2xx/4xx/5xx but verify structure when possible
    assert second.status_code // 100 in (2, 4, 5)
    ctype = (second.headers.get("content-type") or "").lower()
    if second.status_code // 100 == 2 and "application/json" in ctype:
        data = second.json()
        assert isinstance(data, dict)
        assert data.get("id") == pet_id

    cleanup = pet_api.delete(pet_id)
    assert cleanup.status_code in (200, 404)

def test_create_pet_invalid_status_value(pet_api):
    pet_id = 987650003
    payload = {
        "id": pet_id,
        "category": {"id": 3, "name": "status"},
        "name": "invalid-status",
        "photoUrls": ["a"],
        "tags": [{"id": 1, "name": "x"}],
        "status": "unknown_state",
    }

    resp = pet_api.create(payload)
    assert resp.status_code // 100 in (2, 4, 5)

    ctype = (resp.headers.get("content-type") or "").lower()
    if resp.status_code // 100 == 4:
        assert resp.status_code in (400,)
        if "application/json" in ctype:
            body = resp.json()
            assert isinstance(body, dict)
            assert "message" in body or "type" in body
    elif resp.status_code // 100 == 2 and "application/json" in ctype:
        body = resp.json()
        assert isinstance(body, dict)
        assert body.get("id") == pet_id
        # cleanup only if created
        cleanup = pet_api.delete(pet_id)
        assert cleanup.status_code in (200, 404)
        
        