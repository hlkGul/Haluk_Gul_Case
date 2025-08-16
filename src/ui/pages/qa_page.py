from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class QAPage(BasePage):
    URL = "https://useinsider.com/careers/quality-assurance/"
    URL_KEY = "careers/quality-assurance"

    SEE_ALL_JOBS = (
        By.XPATH,
        '//a[normalize-space(text())="See all QA jobs"]',
    )

    def open(self):
        return super().open(self.URL)

    def is_opened(self) -> bool:
        return self.URL_KEY in (self.driver.current_url or "")

    def click_see_all_jobs(self) -> bool:
        return self.click(self.SEE_ALL_JOBS)
