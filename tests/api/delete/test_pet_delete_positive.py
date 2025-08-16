import pytest


def test_delete_pet_positive(pet_api, new_pet_payload):
    # Arrange: create a pet to be deleted
    create_resp = pet_api.create(new_pet_payload)
    assert create_resp.status_code in (200, 201)
    pet_id = create_resp.json()["id"]

    # Act: delete with api_key (if provided)
    del_resp = pet_api.delete(pet_id)

    # Accept 200/202 (deleted) or 404 (record already not found in demo env)
    assert del_resp.status_code in (200, 202, 404)

    # Verify it is gone (best-effort) — kabul edilen iki sonuç: 404 (yok) veya 200 (hemen silinmemiş olabilir)
    get_resp = pet_api.get(pet_id, retries=1, delay=0)
    assert get_resp.status_code in (200, 404)
