from __future__ import annotations

from src.ui.pages import OpenPositionsPage


def test_qa_positions_department_location_contains(qa_open_positions_filtered):
    opp = qa_open_positions_filtered
    cards = opp.iter_job_cards()
    assert cards, "No job cards found"
    for c in cards:
        dept = c.find_element(*OpenPositionsPage.ITEM_DEPARTMENT).text.strip()
        loc = c.find_element(*OpenPositionsPage.ITEM_LOCATION).text.strip()
        assert "Quality Assurance" in dept, f"Department mismatch: {dept}"
        assert "Istanbul, Turkiye" in loc, f"Location mismatch: {loc}"
