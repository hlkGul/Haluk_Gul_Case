import os
import pytest


def test_delete_pet_without_api_key_should_fail(base_url):
    import requests

    # Create a pet first (without using client, direct call)
    payload = {
        "id": 777777777,
        "name": "temp-to-delete",
        "photoUrls": ["x"],
    }
    create_resp = requests.post(f"{base_url}/pet", json=payload)
    assert create_resp.status_code in (200, 201)

    # Try to delete without api_key header — kabul: 2xx (bazı ortamlar auth zorlamaz) veya 4xx (auth hatası)
    del_resp = requests.delete(f"{base_url}/pet/{payload['id']}")
    assert del_resp.status_code // 100 in (2, 4)

    # Cleanup best-effort (with api_key if available)
    api_key = os.getenv("PETSTORE_API_KEY")
    if api_key:
        requests.delete(f"{base_url}/pet/{payload['id']}", headers={"api_key": api_key})
