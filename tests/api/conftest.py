import os
import logging
import uuid
import pytest
from src.api.pet_api import PetAPI

pytestmark = pytest.mark.api


def pytest_sessionstart(session):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


# Mark all tests under tests/api as 'api' so `-m api` selects them
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/api/" in str(item.fspath):
            item.add_marker(pytest.mark.api)


_raw_base = os.getenv("PETSTORE_BASE_URL", "https://petstore.swagger.io/v2").rstrip("/")
if not _raw_base.endswith("/v2"):
    _raw_base = f"{_raw_base}/v2"
BASE_URL = _raw_base
API_KEY = os.getenv("PETSTORE_API_KEY")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def pet_api(base_url):
    return PetAPI(base_url, api_key=API_KEY)


@pytest.fixture()
def new_pet_payload():

    pet_id = int(uuid.uuid4().int % 1_000_000_000)
    return {
        "id": pet_id,
        "name": "Fluffy",
        "photoUrls": ["https://example.com/cat.jpg"],
        "status": "available",
        "category": {"id": 1, "name": "cats"},
        "tags": [{"id": 10, "name": "cute"}],
    }


@pytest.fixture()
def create_pet(pet_api: PetAPI, new_pet_payload):
    resp = pet_api.create(new_pet_payload)
    assert resp.status_code in (
        200,
        201,
    ), f"Failed to create pet: {resp.status_code} {resp.text}"
    created = resp.json()
    yield created
    try:
        pet_api.delete(created["id"])
    except Exception:
        pass
