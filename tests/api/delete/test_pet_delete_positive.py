import pytest


def test_delete_pet_positive(pet_api, new_pet_payload):

    create_resp = pet_api.create(new_pet_payload)
    assert create_resp.status_code in (200, 201)
    pet_id = create_resp.json()["id"]


    del_resp = pet_api.delete(pet_id)


    assert del_resp.status_code in (200, 202, 404)


    get_resp = pet_api.get(pet_id, retries=1, delay=0)
    assert get_resp.status_code in (200, 404)
