import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.ui.pages import QAPage, OpenPositionsPage

pytestmark = pytest.mark.ui

# Ensure all tests in this folder are marked as 'ui'
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/ui/" in str(item.fspath):
            item.add_marker(pytest.mark.ui)

def _create_driver(browser: str):
    browser = (browser or "chrome").lower()
    if browser == "chrome":
        options = ChromeOptions()
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver
    elif browser == "firefox":
        options = FirefoxOptions()
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("-headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        try:
            driver.maximize_window()
        except Exception:
            pass
        return driver
    else:
        raise ValueError(f"Unsupported browser: {browser}")


@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--browser") or os.getenv("BROWSER", "chrome")


@pytest.fixture()
def driver(browser_name):
    drv = _create_driver(browser_name)
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=os.getenv("BROWSER", "chrome"), help="chrome or firefox")


@pytest.fixture()
def qa_open_positions_filtered(driver):
    """Common pre-steps: go to QA page, click CTA, ensure Open Positions loaded and apply filters.
    Basit ve yeniden kullanılabilir.
    """
    qa = QAPage(driver).open()
    assert qa.is_opened(), "QA page should be opened"
    assert qa.click_see_all_jobs(), "'See all QA jobs' click failed"

    opp = OpenPositionsPage(driver)
    assert opp.is_loaded(), "Filters should load"

    # Department otomatik olarak QA olana kadar metni bekle (dinamik)
    WebDriverWait(driver, int(os.getenv("UI_WAIT", "15"))).until(
        EC.text_to_be_present_in_element(OpenPositionsPage.DEPARTMENT_FILTER, "Quality Assurance")
    )
    
    time.sleep(2)

    assert opp.filter_by_location(["Istanbul, Turkey", "Istanbul, Turkiye"]), "Select Istanbul failed"
    assert opp.filter_by_department("Quality Assurance"), "Select Department Failed"
    time.sleep(2)

    return opp
