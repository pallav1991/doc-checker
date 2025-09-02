import os
from pathlib import Path
from processer import process_file_on_server
from src.my_doc_checker import download_docx, compare_docs, generate_pdf_report
from src.verify_reports import verify_evidence_pdf, verify_summary_pdf
import hashlib
from datetime import datetime

# -------------------------------
# Configuration
# -------------------------------
TEST_CASES = [
    ("D1", "http://your-api.com/d1", "docs/d1.docx"),
    ("D2", "http://your-api.com/d2", "docs/d2.docx"),
    ("D3", "http://your-api.com/d3", "docs/d3.docx"),
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

test_results = []

WAIT_TIME_SECONDS = 10

# -------------------------------
# Run all tests
# -------------------------------
for name, api_url, target_file in TEST_CASES:
    print(f"\nRunning test: {name}")

    output_docx = OUTPUT_DIR / f"{name}_output.docx"
    evidence_pdf = OUTPUT_DIR / f"evidence_{name}.pdf"

    # Step 1: Trigger server processing BEFORE downloading
    process_api_url = f"http://your-api.com/process/{name}"  # adjust per your API
    payload = {"file_name": Path(target_file).name}  # optional payload
    process_file_on_server(process_api_url, payload=payload, wait_time=WAIT_TIME_SECONDS)


    # Step 2: Download processed file
    print(f"Downloading processed file {api_url} -> {output_docx}")
    download_docx(api_url, str(output_docx))

    # Step 3: Compare docs and generate evidence PDF
    success, pdf_file = compare_docs(str(output_docx), target_file, str(evidence_pdf))
    print(f"PDF Evidence generated: {pdf_file}")

    test_results.append({
        "name": name,
        "success": success,
        "evidence_pdf": pdf_file
    })

# -------------------------------
# Generate summary PDF
# -------------------------------
summary_pdf = OUTPUT_DIR / "summary_report.pdf"
logs = []

for result in test_results:
    if result["success"]:
        logs.append(f"✅ {result['name']}")
    else:
        logs.append(f"❌ {result['name']}")

# Add total/passed/failed counts for integrity
total = len(test_results)
passed = sum(1 for r in test_results if r["success"])
failed = total - passed
logs.append(f"Total: {total} | Passed: {passed} | Failed: {failed}")

# Compute summary integrity hash
combined_logs = "".join(logs)
summary_hash = hashlib.sha256(combined_logs.encode()).hexdigest()

# Generate PDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import red, green, black, blue

c = canvas.Canvas(str(summary_pdf), pagesize=A4)
width, height = A4
y = height - 2*cm

c.setFont("Helvetica-Bold", 14)
c.setFillColor(blue)
c.drawString(2*cm, y, "Document Comparison - Summary Report")
y -= 1*cm

c.setFont("Helvetica", 10)
c.setFillColor(black)
c.drawString(2*cm, y, f"Generated: {datetime.now()}")
y -= 1*cm

for line in logs:
    if y < 2*cm:
        c.showPage()
        y = height - 2*cm
        c.setFont("Helvetica", 10)

    if line.startswith("✅"):
        c.setFillColor(green)
    elif line.startswith("❌"):
        c.setFillColor(red)
    else:
        c.setFillColor(black)

    c.drawString(2*cm, y, line)
    y -= 0.6*cm

# Integrity page
c.showPage()
c.setFont("Helvetica-Bold", 12)
c.setFillColor(blue)
c.drawString(2*cm, height - 3*cm, "Integrity Code")
c.setFont("Helvetica", 10)
c.setFillColor(black)
c.drawString(2*cm, height - 4*cm, f"Summary Report SHA256: {summary_hash}")

c.save()
print(f"\n✅ Summary PDF generated: {summary_pdf}")

# -------------------------------
# Verify all PDFs
# -------------------------------
print("\nVerifying all PDFs...")

all_verified = True

for result in test_results:
    if not verify_evidence_pdf(result["evidence_pdf"]):
        all_verified = False

if not verify_summary_pdf(summary_pdf):
    all_verified = False

if all_verified:
    print("\n🎉 All evidence and summary PDFs verified successfully!")
else:
    print("\n⚠️ Some PDFs failed verification. Check the logs above.")
