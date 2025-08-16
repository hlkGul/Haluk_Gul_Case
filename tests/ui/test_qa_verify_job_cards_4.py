from __future__ import annotations

from src.ui.pages import OpenPositionsPage


def test_qa_positions_department_location_contains(qa_open_positions_filtered):
    opp = qa_open_positions_filtered

    # Tüm kartlarda Title ve Department 'Quality Assurance' içermeli,
    # Location 'Istanbul, Turkey/Turkiye/İstanbul, Türkiye' içermeli.
    cards = opp.iter_job_cards()
    assert cards, "No job cards found"
    for c in cards:
        dept = c.find_element(*OpenPositionsPage.ITEM_DEPARTMENT).text.strip()
        loc = c.find_element(*OpenPositionsPage.ITEM_LOCATION).text.strip()
        assert "Quality Assurance" in dept, f"Department mismatch: {dept}"
        assert any(v in loc for v in ("Istanbul, Turkey", "Istanbul, Turkiye", "İstanbul, Türkiye")), f"Location mismatch: {loc}"
