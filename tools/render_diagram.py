"""
Renders an arbitrary region of a slide - e.g. a table plus its overlaid
annotation shapes (best-response arrows, circled equilibria) - as a single
high-res PNG crop, using the same PowerPoint COM approach as
render_equations.py.

Use this whenever a diagram's pedagogical content is baked into hand-drawn
annotation that a native Markdown table or plain python-pptx extraction
can't capture. See HANDOFF.md's "Table vs. diagram" note for the decision
rule on when a table conversion loses real content.

SAFETY: same as render_equations.py - does NOT call Application.Quit() on
an already-running PowerPoint instance. Check `tasklist | grep POWERPNT`
yourself first if unsure.

Usage:
    # Step 1: list shapes on a slide to find the ones that make up the
    # diagram (the table AND every arrow/circle/line shape drawn over it):
    mamba run -n ecopy python render_diagram.py --source "...\slidesI.pptx" \
        --slide 14 --list

    # Step 2: render the union bounding box of those shape IDs as one
    # cropped, high-res image:
    mamba run -n ecopy python render_diagram.py --source "...\slidesI.pptx" \
        --slide 14 --shape-ids 211972,211973,211974,211975,211976,211977,211978,211979,211980 \
        --out "...\08_essentials-of-game-theory\raw\media\diagrams\s014_diagram.png"
"""
import argparse
import os
import win32com.client
from PIL import Image
from pptx import Presentation

EXPORT_WIDTH = 2400  # px - high-res so the crop stays legible
PAD = 12  # px padding around the cropped region


def list_shapes(prs, slide_num):
    slide = prs.slides[slide_num - 1]
    print(f"Shapes on slide {slide_num}:")
    for shape in slide.shapes:
        text = ""
        if shape.has_text_frame and shape.text_frame.text.strip():
            text = shape.text_frame.text.strip().split("\n")[0][:40]
        print(f"  id={shape.shape_id:6d}  type={str(shape.shape_type):28s}  "
              f"left={shape.left:8d} top={shape.top:8d} w={shape.width:8d} h={shape.height:8d}  {text}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--slide", type=int, required=True, help="1-indexed slide number")
    ap.add_argument("--list", action="store_true", help="List shapes on the slide and exit")
    ap.add_argument("--shape-ids", help="Comma-separated shape IDs to include in the crop")
    ap.add_argument("--out", help="Output PNG path")
    args = ap.parse_args()

    prs = Presentation(args.source)

    if args.list:
        list_shapes(prs, args.slide)
        return

    if not args.shape_ids or not args.out:
        ap.error("--shape-ids and --out are required unless using --list")

    wanted_ids = set(int(x) for x in args.shape_ids.split(","))
    slide = prs.slides[args.slide - 1]

    lefts, tops, rights, bottoms = [], [], [], []
    found_ids = set()
    for shape in slide.shapes:
        if shape.shape_id in wanted_ids:
            found_ids.add(shape.shape_id)
            lefts.append(shape.left)
            tops.append(shape.top)
            rights.append(shape.left + shape.width)
            bottoms.append(shape.top + shape.height)

    missing = wanted_ids - found_ids
    if missing:
        print(f"WARNING: shape IDs not found on slide {args.slide}: {missing}")
    if not lefts:
        print("No matching shapes found - nothing to render.")
        return

    left, top = min(lefts), min(tops)
    right, bottom = max(rights), max(bottoms)

    slide_w_emu = prs.slide_width
    slide_h_emu = prs.slide_height
    export_height = int(EXPORT_WIDTH * slide_h_emu / slide_w_emu)

    already_running = True
    try:
        win32com.client.GetActiveObject("PowerPoint.Application")
    except Exception:
        already_running = False
    print("PowerPoint already running before this script:", already_running)

    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = None
    slide_png_path = os.path.join(os.path.dirname(args.out), f"_slide{args.slide:03d}_full.png")
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    try:
        pres = app.Presentations.Open(args.source, ReadOnly=True, Untitled=False, WithWindow=True)
        pres.Slides(args.slide).Export(slide_png_path, "PNG", EXPORT_WIDTH, export_height)
    finally:
        if pres is not None:
            pres.Close()
        if not already_running:
            app.Quit()
        else:
            print("PowerPoint was already running elsewhere - left the app open, only closed our window")

    px_per_emu_x = EXPORT_WIDTH / slide_w_emu
    px_per_emu_y = export_height / slide_h_emu

    img = Image.open(slide_png_path)
    x0 = max(0, int(left * px_per_emu_x) - PAD)
    y0 = max(0, int(top * px_per_emu_y) - PAD)
    x1 = min(img.width, int(right * px_per_emu_x) + PAD)
    y1 = min(img.height, int(bottom * px_per_emu_y) + PAD)
    crop = img.crop((x0, y0, x1, y1))
    crop.save(args.out)
    os.remove(slide_png_path)
    print(f"-> wrote {args.out} ({crop.width}x{crop.height})")


if __name__ == "__main__":
    main()
