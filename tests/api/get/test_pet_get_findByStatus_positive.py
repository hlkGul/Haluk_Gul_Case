import pytest


@pytest.mark.parametrize(
    "status", ["available", "pending", "sold"], ids=["available", "pending", "sold"]
)
def test_find_by_status_basic(pet_api, status):
    resp = pet_api.find_by_status(status)
    assert resp.status_code == 200
    ctype = (resp.headers.get("content-type") or "").lower()
    assert "application/json" in ctype
    data = resp.json()
    assert isinstance(data, list)
    if data and isinstance(data[0], dict) and "status" in data[0]:
        assert all(
            item.get("status") == status for item in data if isinstance(item, dict)
        )
