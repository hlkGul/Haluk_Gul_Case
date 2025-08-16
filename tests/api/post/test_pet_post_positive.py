import pytest


def test_create_pet_positive(pet_api):
    payload = {
        "id": 5,
        "category": {"id": 0, "name": "street"},
        "name": "comar",
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "comcom"}],
        "status": "available",
    }


    resp = pet_api.create(payload)
    assert resp.status_code in (200, 201)
    body = resp.json()


    assert body["id"] == payload["id"]
    assert body["name"] == payload["name"]
    assert body["status"] == payload["status"]
    assert isinstance(body.get("photoUrls"), list)
    assert isinstance(body.get("category"), dict)
    assert isinstance(body.get("tags"), list)

    del_resp = pet_api.delete(payload["id"])  
    assert del_resp.status_code in (200, 404)
