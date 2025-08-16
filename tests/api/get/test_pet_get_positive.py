import pytest

@pytest.mark.parametrize("pet_id", [1])
def test_get_pet_by_id_parametric(pet_api, pet_id):

    resp = pet_api.get(pet_id)
    assert resp.status_code == 200
    body = resp.json()

    assert isinstance(body, dict)
    assert "id" in body
    assert "name" in body
    assert "status" in body

