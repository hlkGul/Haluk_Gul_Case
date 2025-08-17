from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class CareersPage(BasePage):
    URL_KEY = "careers"
    LOCATIONS = (By.ID, "career-our-location")
    TEAMS = (By.ID, "career-find-our-calling")
    LIFE_AT_INSIDER = (By.XPATH, '//section[@data-id="a8e7b90"]')

    def is_opened(self) -> bool:
        self.log.info("Careers page opened successfully")
        return self.URL_KEY in (self.driver.current_url or "")

    def blocks_visible(self) -> bool:
        try:
            self.wait_visible(self.LOCATIONS)
            self.wait_visible(self.TEAMS)
            self.wait_visible(self.LIFE_AT_INSIDER)
            self.log.info("Teams, life and location fields are displayed on the career page")
            return True
        except TimeoutException:
            return False
