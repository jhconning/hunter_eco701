import sys
import pypdf

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pdf_path = sys.argv[1] if len(sys.argv) > 1 else 'ps/F26/ps1_handout_v2.pdf'
reader = pypdf.PdfReader(pdf_path)
for i, page in enumerate(reader.pages):
    lines = [line.strip() for line in page.extract_text().splitlines() if line.strip()]
    first_few = " | ".join(lines[:3]) if lines else "EMPTY"
    last_few = " | ".join(lines[-2:]) if lines else "EMPTY"
    print(f"Page {i+1:02d} ({len(lines)} lines): First: {first_few[:70]} ... Last: {last_few[:50]}")

