import hashlib
import re
from PyPDF2 import PdfReader

def verify_evidence_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    match = re.search(r"Integrity Code:\s*([0-9a-f]{64})", text)
    if not match:
        print(f"[{pdf_file}] ❌ Integrity hash not found.")
        return False
    embedded_hash = match.group(1)

    # Recompute hash based on lines (simplified)
    log_lines = [line.strip() for line in text.splitlines() if line.startswith("✅") or line.startswith("❌")]
    recomputed_hash = hashlib.sha256(("".join(log_lines)).encode()).hexdigest()

    if embedded_hash == recomputed_hash:
        print(f"[{pdf_file}] ✅ Verification successful.")
        return True
    else:
        print(f"[{pdf_file}] ❌ Verification failed!")
        return False


def verify_summary_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    match = re.search(r"Summary Report SHA256:\s*([0-9a-f]{64})", text)
    if not match:
        print(f"[{pdf_file}] ❌ Integrity hash not found.")
        return False
    embedded_hash = match.group(1)

    # Extract lines for hash recomputation
    log_lines = [line.strip() for line in text.splitlines() if line.startswith("✅") or line.startswith("❌")]
    total_match = re.search(r"Total Comparisons:\s*(\d+)", text)
    passed_match = re.search(r"✅ Passed:\s*(\d+)", text)
    failed_match = re.search(r"❌ Failed:\s*(\d+)", text)

    if not total_match or not passed_match or not failed_match:
        print(f"[{pdf_file}] ❌ Could not extract counts.")
        return False

    combined_logs = "".join(log_lines) + f"total:{total_match.group(1)}|passed:{passed_match.group(1)}|failed:{failed_match.group(1)}"
    recomputed_hash = hashlib.sha256(combined_logs.encode()).hexdigest()

    if embedded_hash == recomputed_hash:
        print(f"[{pdf_file}] ✅ Summary verification successful.")
        return True
    else:
        print(f"[{pdf_file}] ❌ Summary verification failed!")
        return False
