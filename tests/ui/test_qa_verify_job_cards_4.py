from __future__ import annotations
from src.ui.pages import OpenPositionsPage
import logging


def test_qa_positions_department_location_contains(qa_open_positions_filtered):
    opp = qa_open_positions_filtered
    pairs = opp.get_job_cards_texts()
    assert pairs, "No job cards found"
    expected_dept = "Quality Assurance"
    expected_loc = "Istanbul, Turkiye"
    for dept, loc in pairs:
        assert expected_dept in dept, f"Department mismatch: {dept}"
        assert expected_loc in loc, f"Location mismatch: {loc}"
    logging.getLogger("UI").info(
        "Verified %d cards with expected dept and location", len(pairs)
    )
