from __future__ import annotations

from src.ui.pages import HomePage


def test_home_page_opened(driver):

    page = HomePage(driver).open()
    assert page.is_opened(), "Insider home page title should contain 'Insider'"
    assert page.has_announce(), "Home page should contain announce element"

