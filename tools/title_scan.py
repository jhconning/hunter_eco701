"""
Planning tool: cheap title-only scan across a whole deck (or several), used
to eyeball topic boundaries before committing to a slide range. No images,
no tables, no OCR - just the first text line of every slide.

Usage:
    mamba run -n ecopy python title_scan.py \
        --source "Y:\Hunter\Eco 701\past\eco701_F18\slides\E701_F18 _slidesI.pptx" \
                 "Y:\Hunter\Eco 701\past\eco701_F18\slides\E701_F18 _slidesII.pptx" \
        --out scratch_title_scan.txt

This is intentionally NOT written into slides/ - keep its output in a
scratch location outside the repo (or delete it after use); it's a planning
aid, not a deliverable, and marp-cli will otherwise try to build any stray
.md file it finds under slides/.
"""
import argparse
import os
from pptx import Presentation


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", nargs="+", required=True, help="One or more .pptx paths")
    ap.add_argument("--out", required=True, help="Output .txt path (NOT under slides/)")
    args = ap.parse_args()

    lines = []
    for path in args.source:
        name = os.path.basename(path)
        prs = Presentation(path)
        lines.append(f"\n\n==================== {name} ====================")
        for idx, slide in enumerate(prs.slides, start=1):
            title_text = None
            for shape in slide.shapes:
                if shape.has_text_frame and shape.is_placeholder:
                    try:
                        ph_type = shape.placeholder_format.type
                    except Exception:
                        ph_type = None
                    if ph_type is not None and "TITLE" in str(ph_type):
                        t = shape.text_frame.text.strip()
                        if t:
                            title_text = t.replace("\n", " / ")
                            break
            if title_text is None:
                for shape in slide.shapes:
                    if shape.has_text_frame and shape.text_frame.text.strip():
                        title_text = shape.text_frame.text.strip().split("\n")[0]
                        break
            if title_text is None:
                title_text = "(no text found)"
            lines.append(f"{idx:4d}  {title_text[:100]}")

    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", args.out)


if __name__ == "__main__":
    main()
