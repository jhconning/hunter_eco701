"""
Pipeline tool (used alongside extract_topic.py): exports every slide in a
range as a full-resolution PNG, unconditionally - not just slides with OLE
equation objects (that's render_equations.py's narrower job).

Needed when a topic's diagrams are built from native PowerPoint drawing
shapes (GROUP/AUTO_SHAPE/FREEFORM/LINE) rather than embedded pictures or
Mathcad/Equation OLE objects - extract_topic.py's diagram_candidates.json
heuristic only looks for TABLE/PICTURE + annotation-shape combos, so it's
blind to this pattern entirely. First hit in 03_production-optimization
(isoquant maps, cost curves, expansion paths - all native-drawn). Full-slide
export + manual crop (in an image editor, or ad hoc with PIL) is the
fallback: see HANDOFF.md's gotchas for the general policy.

Requires: Windows + PowerPoint installed + pywin32.

SAFETY: same as render_equations.py - if PowerPoint is already running with
other work open, this does NOT call Application.Quit(), only closes the one
presentation window it opens itself.

Usage:
    mamba run -n ecopy python export_slide_pngs.py \
        --source "Y:\Hunter\eco701\archive\slides\legacy\E701_F18 _slidesIIb.pptx" \
        --start 162 --end 202 \
        --out "Y:\Hunter\eco701\slides\03_production-optimization\raw"

Writes into --out/media/slide_png/ (same location render_equations.py uses,
so slides already exported via that script's OLE-triggered path are just
overwritten with an identical render - harmless).
"""
import argparse
import os
import win32com.client
from pptx import Presentation

EXPORT_WIDTH = 2400  # px - matches render_equations.py's resolution


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--out", required=True, help="Output raw/ folder for this topic")
    args = ap.parse_args()

    slide_png_dir = os.path.join(args.out, "media", "slide_png")
    os.makedirs(slide_png_dir, exist_ok=True)

    prs = Presentation(args.source)
    slide_w_emu = prs.slide_width
    slide_h_emu = prs.slide_height
    export_height = int(EXPORT_WIDTH * slide_h_emu / slide_w_emu)

    indices = list(range(args.start, args.end + 1))
    print(f"Exporting slides {args.start}-{args.end} ({len(indices)} slides)")

    already_running = True
    try:
        win32com.client.GetActiveObject("PowerPoint.Application")
    except Exception:
        already_running = False
    print("PowerPoint already running before this script:", already_running)

    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = None
    try:
        pres = app.Presentations.Open(args.source, ReadOnly=True, Untitled=False, WithWindow=True)
        for idx in indices:
            slide = pres.Slides(idx)
            out_path = os.path.join(slide_png_dir, f"slide{idx:03d}.png")
            slide.Export(out_path, "PNG", EXPORT_WIDTH, export_height)
        print(f"Exported {len(indices)} full-slide PNGs to {slide_png_dir}")
    finally:
        if pres is not None:
            pres.Close()
        if not already_running:
            app.Quit()
        else:
            print("PowerPoint was already running elsewhere - left the app open, only closed our window")


if __name__ == "__main__":
    main()
