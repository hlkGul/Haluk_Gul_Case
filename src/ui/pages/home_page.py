from __future__ import annotations

from typing import TYPE_CHECKING
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

if TYPE_CHECKING:
    # only for type hints, avoid circular at runtime
    from .careers_page import CareersPage


class HomePage(BasePage):
    URL = "https://useinsider.com/"
    TITLE_KEYWORD = "Insider"

    COMPANY = (By.XPATH, '//a[normalize-space(text())="Company"]')
    CAREERS = (By.XPATH, '//a[contains(@href, "careers")]')
    ANNOUNCE = (By.ID, "announce")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self):
        return super().open(self.URL)

    def is_opened(self) -> bool:
        title = self.driver.title or ""
        return self.TITLE_KEYWORD.lower() in title.lower()

    def has_announce(self) -> bool:
        """Return True if the announce element is visible, False otherwise."""
        try:
            self.wait_visible(self.ANNOUNCE)
            return True
        except TimeoutException:
            return False

    def go_to_careers(self) -> "CareersPage":
        self.hover(self.COMPANY)
        self.click(self.CAREERS)
        from .careers_page import CareersPage

        return CareersPage(self.driver)
