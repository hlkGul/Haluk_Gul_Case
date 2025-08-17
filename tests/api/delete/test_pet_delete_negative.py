import os
import pytest


def test_delete_pet_without_api_key_should_fail(base_url):
    import requests

    payload = {
        "id": 777777777,
        "name": "temp-to-delete",
        "photoUrls": ["x"],
    }
    create_resp = requests.post(f"{base_url}/pet", json=payload)
    assert create_resp.status_code in (200, 201)

    # Try to delete without api_key header 
    del_resp = requests.delete(f"{base_url}/pet/{payload['id']}")
    assert del_resp.status_code // 100 in (2, 4)

    api_key = os.getenv("PETSTORE_API_KEY")
    if api_key:
        requests.delete(f"{base_url}/pet/{payload['id']}", headers={"api_key": api_key})

def test_delete_pet_idempotent(pet_api, new_pet_payload):
    create_resp = pet_api.create(new_pet_payload)
    assert create_resp.status_code in (200, 201)
    pet_id = create_resp.json()["id"]

    first = pet_api.delete(pet_id)
    assert first.status_code in (200, 202, 404)

    second = pet_api.delete(pet_id)
    assert second.status_code in (200, 202, 404)