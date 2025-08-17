from __future__ import annotations

from typing import Iterable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class OpenPositionsPage(BasePage):
    LOCATION_FILTER = (By.ID, "select2-filter-by-location-container")
    DEPARTMENT_FILTER = (By.ID, "select2-filter-by-department-container")
    JOB_LIST = (By.ID, "jobs-list")
    JOB_ITEMS = (By.CSS_SELECTOR, "#jobs-list > div")
    ITEM_DEPARTMENT = (By.CSS_SELECTOR, ".position-department")
    ITEM_LOCATION = (By.CSS_SELECTOR, ".position-location")
    VIEW_ROLE_BTN = (By.CSS_SELECTOR, "a.btn.btn-navy[target='_blank']")

    def is_loaded(self) -> bool:
        try:
            self.wait_clickable(self.LOCATION_FILTER)
            self.wait_clickable(self.DEPARTMENT_FILTER)
            return True
        except TimeoutException:
            return False

    def _select2_select(self, trigger_locator: tuple[str, str], option_xpath: str) -> bool:
        try:

            if not self.click(trigger_locator):
                return False

            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, "//li[@role='option']"))
            )

            option_el = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable((By.XPATH, option_xpath))
            )
            option_el.click()
            return True
        except TimeoutException:
            return False

    def filter_by_location(self, texts: Iterable[str]) -> bool:
        # Accept multiple acceptable texts (e.g., 'Turkey' vs 'Turkiye')
        conditions = " or ".join([f"normalize-space()='{t}'" for t in texts])
        option_xpath = f"//li[@role='option' and ({conditions})]"
        return self._select2_select(self.LOCATION_FILTER, option_xpath)

    def filter_by_department(self, text: str) -> bool:
        option_xpath = f"//li[@role='option' and normalize-space()='{text}']"
        return self._select2_select(self.DEPARTMENT_FILTER, option_xpath)

    def has_job_list(self) -> bool:
        try:
            self.wait_present(self.JOB_LIST)
            return True
        except TimeoutException:
            return False

    def iter_job_cards(self):
        self.wait_present(self.JOB_LIST)
        return self.driver.find_elements(*self.JOB_ITEMS)

    def get_filtered_jobs_delay_seconds(self) -> float:
        """Read data-animate-delay from #jobs-list as seconds (numeric). Returns 2.0s as safe default."""
        try:
            el = self.driver.find_element(*self.JOB_LIST)
            val = (
                el.get_attribute("data-animate-delay")
                or el.get_attribute("data_animate_delay")
                or el.get_attribute("data-animated-delay")
            )
            v = (str(val).strip() if val is not None else "")
            return float(v) if v else 2.0
        except Exception:
            return 2.0

    
    def click_any_view_role_and_verify_new_tab(self) -> bool:
        cards = self.iter_job_cards()
        if not cards:
            return False
        card = cards[0]
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        except Exception:
            pass

        original_handles = list(self.driver.window_handles)
        try:

            link = card.find_element(By.CSS_SELECTOR, "a[href*='jobs.lever.co']")
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
            except Exception:
                pass
            try:
                link.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", link)

            # Yeni sekme açılmasını ya da mevcut sekmede Lever URL’e gitmesini bekle
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: len(d.window_handles) > len(original_handles) or d.current_url.startswith("https://jobs.lever.co/")
            )
            if len(self.driver.window_handles) > len(original_handles):
                new_handle = next(h for h in self.driver.window_handles if h not in original_handles)
                self.driver.switch_to.window(new_handle)

            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.current_url.startswith("https://jobs.lever.co/")
            )
            return True
        except TimeoutException:
            return False
        except Exception:
            return False

