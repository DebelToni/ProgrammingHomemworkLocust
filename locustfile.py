"""Locust load-testing script aimed at exercising https://example.org."""

from __future__ import annotations

import random

from locust import HttpUser, between, task


class ExampleOrgUser(HttpUser):
    host = "https://example.org"
    wait_time = between(0.5, 2.0)

    @task(5)
    def homepage(self) -> None:
        self.client.get("/", name="GET /")

    @task(3)
    def index_html(self) -> None:
        self.client.get("/index.html", name="GET /index.html")

    @task(2)
    def homepage_with_query(self) -> None:
        query = random.choice(["loadtest", "docs", "tutorial"])
        self.client.get("/", params={"ref": query}, name="GET /?ref")
