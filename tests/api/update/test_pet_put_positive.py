import pytest


def test_update_pet_positive(pet_api, new_pet_payload):

    create_resp = pet_api.create(new_pet_payload)
    assert create_resp.status_code in (200, 201)

    pet = create_resp.json()
    pet_id = pet["id"]

    pet["name"] = "updated-name"
    pet["status"] = "sold"

    update_resp = pet_api.update(pet)
    assert update_resp.status_code in (200, 201)

    updated = update_resp.json()
    assert updated["id"] == pet_id
    assert updated["name"] == "updated-name"
    assert updated["status"] == "sold"


    del_resp = pet_api.delete(pet_id)
    assert del_resp.status_code in (200, 404)
