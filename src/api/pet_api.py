from __future__ import annotations

import time
import logging
import requests
from typing import Optional


class PetAPI:
    def __init__(self, base_url: str, api_key: str | None = None):
        self.base = base_url.rstrip("/")
        self.api_key = api_key
        self.log = logging.getLogger(self.__class__.__name__)

    def _auth_headers(self) -> dict:
        return {"api_key": self.api_key} if self.api_key else {}

    def get(
        self, pet_id: int, retries: int = 6, delay: float = 0.5
    ) -> requests.Response:
        """GET /pet/{id} with small retry for public demo flakiness"""
        self.log.info("GET /pet/%s", pet_id)
        last: Optional[requests.Response] = None
        for _ in range(retries):
            last = requests.get(f"{self.base}/pet/{pet_id}")
            if last.status_code == 200:
                return last
            time.sleep(delay)
        return last

    def find_by_status(self, status: str) -> requests.Response:
        """GET /pet/findByStatus"""
        self.log.info("GET /pet/findByStatus status=%s", status)
        return requests.get(f"{self.base}/pet/findByStatus", params={"status": status})

    def create(self, payload: dict) -> requests.Response:
        """POST /pet"""
        self.log.info("POST /pet id=%s", payload.get("id"))
        return requests.post(f"{self.base}/pet", json=payload)

    def create_raw(
        self, body: str | bytes, headers: Optional[dict] = None
    ) -> requests.Response:
        """POST /pet with custom body/headers (for negative tests such as wrong Content-Type)."""
        self.log.info("POST /pet (raw)")
        return requests.post(f"{self.base}/pet", data=body, headers=headers or {})

    def update(self, payload: dict) -> requests.Response:
        """PUT /pet"""
        self.log.info("PUT /pet id=%s", payload.get("id"))
        return requests.put(f"{self.base}/pet", json=payload)

    def update_raw(
        self, body: str | bytes, headers: Optional[dict] = None
    ) -> requests.Response:
        """PUT /pet with custom body/headers (for negative tests)."""
        self.log.info("PUT /pet (raw)")
        return requests.put(f"{self.base}/pet", data=body, headers=headers or {})

    def delete(self, pet_id: int) -> requests.Response:
        """DELETE /pet/{id}"""
        self.log.info("DELETE /pet/%s", pet_id)
        return requests.delete(
            f"{self.base}/pet/{pet_id}", headers=self._auth_headers()
        )
