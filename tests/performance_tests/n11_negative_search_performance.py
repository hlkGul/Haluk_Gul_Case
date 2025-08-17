from locust import HttpUser, task, between


class N11NegativeSearchUser(HttpUser):
    """Scenario: Non-existing keyword search (negative).

    Structure mirrors the basic test: home (/) -> search (/arama?q=...).
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

    @task
    def search_non_existing(self):
        # 1) Home
        with self.client.get("/", name="/", catch_response=True) as r_home:
            if r_home.status_code != 200:
                r_home.failure(f"Unexpected status: {r_home.status_code}")
                return

        query = "olmayanurun"
        with self.client.get(
            "/arama",
            params={"q": query},
            name="/arama?neg",
            headers={"Referer": "https://www.n11.com/"},
            catch_response=True,
        ) as r_search:
            if r_search.status_code != 200:
                r_search.failure(f"Unexpected status: {r_search.status_code}")
                return
            body = r_search.text.lower()
            if (
                "arama" not in body
                and "bulunamad" not in body  # matches bulunamadı/bulunamadi
                and "sonuc" not in body
                and "sonuç" not in body
            ):
                r_search.failure(
                    "Negative search page did not contain expected markers"
                )
