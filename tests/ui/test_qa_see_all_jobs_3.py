from __future__ import annotations


def test_qa_see_all_jobs_and_filter(qa_open_positions_filtered):
    opp = qa_open_positions_filtered
    assert opp.has_job_list(), "Jobs list should be present"
