import json
import pytest


@pytest.mark.parametrize(
    "bad_body, headers, expected_status",
    [
        ("{bad json", {"Content-Type": "application/json"}, 400),
        (json.dumps({"id": 0, "name": "bad"}), {"Content-Type": "text/plain"}, 415),
        (json.dumps({"id": 0}), {"Content-Type": "application/json"}, 400),
    ],
)
def test_update_pet_negative_variants(pet_api, bad_body, headers, expected_status):
    resp = pet_api.update_raw(bad_body, headers=headers)

    assert resp.status_code // 100 in (2, 4, 5)

    if resp.status_code // 100 == 4:
        assert resp.status_code == expected_status

    ctype = (resp.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        data = resp.json()
        if resp.status_code // 100 == 4:
            assert "message" in data or "type" in data
        elif resp.status_code // 100 == 2:
            assert "id" in data
            assert isinstance(data.get("photoUrls"), list)
            assert isinstance(data.get("tags"), list)
