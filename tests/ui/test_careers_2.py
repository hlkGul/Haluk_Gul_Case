from __future__ import annotations

from src.ui.pages import HomePage


def test_visit_careers_and_blocks(driver):
    # Home → Company hover → Careers
    careers = HomePage(driver).open().go_to_careers()

    # Careers page yüklendi mi?
    assert careers.is_opened(), "Careers page should be opened (URL contains 'careers')"

    # Bloklar görünüyor mu?
    assert careers.blocks_visible(), "Locations, Teams, Life at Insider blocks should be visible"
