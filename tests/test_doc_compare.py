import pytest
from pathlib import Path
from src.my_doc_checker import download_docx, compare_docs

TEST_CASES = [
    ("Checking D1", "http://your-api.com/d1", "docs/d1.docx"),
    ("Checking D2", "http://your-api.com/d2", "docs/d2.docx"),
    ("Checking D3", "http://your-api.com/d3", "docs/d3.docx"),
]

@pytest.mark.parametrize("description, api_url, target_file", TEST_CASES)
def test_doc_comparison(description, api_url, target_file, tmp_path):
    output_file = tmp_path / "output.docx"
    evidence_file = tmp_path / f"evidence_{Path(target_file).stem}.pdf"

    download_docx(api_url, str(output_file))
    success, report = compare_docs(str(output_file), target_file, str(evidence_file))

    print(f"[{description}] Evidence PDF: {report}")
    assert success, f"{description} failed. See evidence: {report}"
