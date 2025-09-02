✅ Workflow Summary
Store reference docs in docs/.
Run pytest -v tests/test_doc_compare.py.
Each test generates evidence PDF in tmp_path → includes color-coded results + integrity hash.
conftest.py automatically verifies individual evidence PDFs and the summary report.
src/verify_reports.py can also be used standalone for verification.




🔹 How to Run
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Make sure your reference docs are in the `docs/` directory.
3. Run the script:
```bash
python run_all_tests.py
```
4. Outputs:
- Individual evidence PDFs: `output/evidence_D1.pdf`, `output/evidence_D2.pdf`, etc.
- Summary report PDF: `output/summary_report.pdf`
- Verification results: printed in the console


✅ This script gives you a fully automated workflow without using pytest.
- Downloads files, compares docs, generates color-coded PDFs, computes integrity hashes, and verifies everything.
- Can easily be scheduled, run on CI/CD, or used manually.