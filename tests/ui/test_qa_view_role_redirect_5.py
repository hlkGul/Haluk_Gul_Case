from __future__ import annotations
from src.ui.pages import OpenPositionsPage
import logging


def test_view_role_opens_lever(qa_open_positions_filtered):
    opp: OpenPositionsPage = qa_open_positions_filtered
    assert (
        opp.click_any_view_role_and_verify_new_tab()
    ), "View Role should open Lever application form in a new tab"
    logging.getLogger("UI").info("Lever Application form page displayed in new tab")
