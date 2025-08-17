from itertools import cycle
from locust import HttpUser, task, between


class N11RoundRobinSearchUser(HttpUser):
    """Scenario: Repeated searches with different keywords (round-robin).

    Mirrors the basic structure: home (/) then search. Keywords come from env or default list.
    """

    wait_time = between(1, 2)
    host = "https://www.n11.com"

    def on_start(self):
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )
        pool = [
            "telefon",
            "bilgisayar",
            "kulaklık",
            "ayakkabı",
            "saat",
            "çanta",
            "kitap",
            "oyuncak",
            "televizyon",
            "buzdolabı",
        ]
        self._kw_iter = cycle(pool)

    @task
    def search_next_keyword(self):
        with self.client.get("/", name="/", catch_response=True) as r_home:
            if r_home.status_code != 200:
                r_home.failure(f"Unexpected status: {r_home.status_code}")
                return

        kw = next(self._kw_iter)
        with self.client.get(
            "/arama",
            params={"q": kw},
            name="/arama?rr",
            headers={"Referer": "https://www.n11.com/"},
            catch_response=True,
        ) as r_search:
            if r_search.status_code != 200:
                r_search.failure(
                    f"Unexpected status for '{kw}': {r_search.status_code}"
                )
                return
            body = r_search.text.lower()
            if kw.lower() not in body and "arama" not in body:
                r_search.failure(
                    f"Search results did not contain expected markers (kw='{kw}')"
                )
