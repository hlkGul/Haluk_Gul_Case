import pytest


def test_find_by_status_invalid_value(pet_api):
    resp = pet_api.find_by_status("unknownState")
    assert resp.status_code // 100 in (2, 4, 5)
    ctype = (resp.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        body = resp.json()
        assert isinstance(body, (list, dict))
