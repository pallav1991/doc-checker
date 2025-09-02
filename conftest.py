import pytest
from src.verify_reports import verify_evidence_pdf, verify_summary_pdf

test_results = []

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == "call":
        test_results.append({
            "name": item.name,
            "description": item.nodeid,
            "outcome": result.outcome
        })

def pytest_sessionfinish(session, exitstatus):
    # Optionally verify all generated PDFs here
    for test in test_results:
        evidence_file = f"output/evidence_{test['name'].split('_')[-1]}.pdf"
        verify_evidence_pdf(evidence_file)

    # Verify summary
    summary_file = "output/summary_report.pdf"
    verify_summary_pdf(summary_file)
