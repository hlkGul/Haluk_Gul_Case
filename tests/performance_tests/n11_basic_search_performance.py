from locust import HttpUser, task, between


class N11SearchUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://www.n11.com"

    def on_start(self):
        # 403 almamak icin user-agent ekledik
        self.client.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )

    @task
    def search_and_list_results(self):

        with self.client.get("/", name="/", catch_response=True) as r_home:
            if r_home.status_code != 200:
                r_home.failure(f"Unexpected status: {r_home.status_code}")
                return

        # to do: query parametry env den oku
        query = "telefon"
        with self.client.get(
            "/arama", params={"q": query}, name="/arama", catch_response=True
        ) as r_search:
            if r_search.status_code != 200:
                r_search.failure(f"Unexpected status: {r_search.status_code}")
                return
            body = r_search.text.lower()
            if query not in body and "arama" not in body:
                r_search.failure(
                    "Search results page content did not contain expected markers"
                )
