from __future__ import annotations

import os
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, ElementNotInteractableException


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.timeout = int(os.getenv("UI_WAIT", "15"))

    def open(self, url: str):
        self.driver.get(url)

        self.wait_document_ready()

        try:
            self.accept_cookies_if_present()
        except Exception:
            pass

        try:
            self.dismiss_ins_popup_if_present()
        except Exception:
            pass
        return self

    def wait_visible(self, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_clickable(self, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_present(self, locator: Tuple[str, str]):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def hover(self, locator: Tuple[str, str]):
        elem = self.wait_visible(locator)
        ActionChains(self.driver).move_to_element(elem).perform()
        return elem

    def click(self, locator: Tuple[str, str], scroll: bool = True, js_fallback: bool = True) -> bool:
        """Safe click helper: waits clickable, optionally scrolls into view, tries JS click if intercepted.
        Returns True on success, False otherwise.
        """
        try:
            el = self.wait_clickable(locator)
            if scroll:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            el.click()
            return True
        except ElementClickInterceptedException:
            if js_fallback:
                try:
                    el = self.wait_present(locator)
                    self.driver.execute_script("arguments[0].click();", el)
                    return True
                except Exception:
                    return False
            return False
        except (TimeoutException, ElementNotInteractableException):
            return False

    def wait_document_ready(self) -> bool:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True

    # Cookie banner kabul et 
    def accept_cookies_if_present(self) -> bool:
        try:
            els = self.driver.find_elements(By.ID, "wt-cli-accept-all-btn")
            if not els:
                return False
            btn = els[0]
            if not btn.is_displayed():
                return False
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            except Exception:
                pass
            try:
                btn.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    return False

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((By.ID, "wt-cli-accept-all-btn"))
                )
            except Exception:
                pass
            return True
        except Exception:
            return False

    # Insider responsive popup varsa kapat
    def dismiss_ins_popup_if_present(self) -> bool:
        try:
            banners = self.driver.find_elements(By.ID, "ins-responsive-banner")
            if not banners:
                return False
            banner = banners[0]
            if not banner.is_displayed():
                return False
            close_buttons = self.driver.find_elements(By.CSS_SELECTOR, "span.ins-close-button")
            if not close_buttons:
                return False
            btn = close_buttons[0]
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            except Exception:
                pass
            try:
                btn.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                except Exception:
                    return False

            try:
                WebDriverWait(self.driver, 5).until(
                    EC.invisibility_of_element_located((By.ID, "ins-responsive-banner"))
                )
            except Exception:
                pass
            return True
        except Exception:
            return False
