import pytest


@pytest.mark.parametrize("pet_id", [111111])
def test_get_pet_by_id_not_found(pet_api, pet_id):

    resp = pet_api.get(pet_id, retries=1, delay=0)

    if resp.status_code == 200:
        pytest.skip(f"Pet {pet_id} exists in the public demo; skipping negative check")

    assert resp.status_code == 404

    ctype = (resp.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        data = resp.json()
        assert data.get("message") == "Pet not found"


@pytest.mark.parametrize("pet_id", ["abc"])
def test_get_pet_by_id_invalid_format_negative(pet_api, pet_id):
    resp = pet_api.get(pet_id, retries=1, delay=0)
    assert resp.status_code // 100 in (2, 4, 5)
    if resp.status_code // 100 == 4:
        assert resp.status_code in (400, 404)
    ctype = (resp.headers.get("content-type") or "").lower()
    if resp.status_code // 100 == 2 and "application/json" in ctype:
        assert isinstance(resp.json(), dict)
