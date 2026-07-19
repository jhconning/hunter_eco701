"""
Renders an arbitrary region of a slide - e.g. a table plus its overlaid
annotation shapes (best-response arrows, circled equilibria) - as a single
high-res PNG crop, using the same PowerPoint COM approach as
render_equations.py.

Use this whenever a diagram's pedagogical content is baked into hand-drawn
annotation that a native Markdown table or plain python-pptx extraction
can't capture. Default policy (2026-07-15, Jonathan): capture everything at
full fidelity by default - simplifying to a plain table/omitting annotation
is a deliberate per-slide exception, not the default. See HANDOFF.md's
"Table vs. diagram" note.

SAFETY: same as render_equations.py - does NOT call Application.Quit() on
an already-running PowerPoint instance. Check `tasklist | grep POWERPNT`
yourself first if unsure.

Usage:
    # Recommended: batch-render every diagram_candidates.json entry from
    # extract_topic.py in ONE PowerPoint session (much faster than
    # reopening PowerPoint per slide):
    mamba run -n ecopy python render_diagram.py --source "...\slidesI.pptx" \
        --candidates "...\02_constrained-optimization\raw\diagram_candidates.json" \
        --out-dir "...\02_constrained-optimization\raw\media\diagrams"

    # Manual single-slide mode - list shapes first to pick IDs by hand
    # (e.g. for a diagram extract_topic.py's heuristic didn't catch):
    mamba run -n ecopy python render_diagram.py --source "...\slidesI.pptx" \
        --slide 14 --list

    mamba run -n ecopy python render_diagram.py --source "...\slidesI.pptx" \
        --slide 14 --shape-ids 211972,211973,211974 \
        --out "...\08_essentials-of-game-theory\raw\media\diagrams\s014_diagram.png"
"""
import argparse
import json
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


def bbox_for_shape_ids(slide, wanted_ids):
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
        print(f"  WARNING: shape IDs not found: {missing}")
    if not lefts:
        return None
    return min(lefts), min(tops), max(rights), max(bottoms)


def crop_and_save(full_slide_png, bbox, slide_w_emu, slide_h_emu, export_width, export_height, out_path):
    left, top, right, bottom = bbox
    px_per_emu_x = export_width / slide_w_emu
    px_per_emu_y = export_height / slide_h_emu
    img = Image.open(full_slide_png)
    x0 = max(0, int(left * px_per_emu_x) - PAD)
    y0 = max(0, int(top * px_per_emu_y) - PAD)
    x1 = min(img.width, int(right * px_per_emu_x) + PAD)
    y1 = min(img.height, int(bottom * px_per_emu_y) + PAD)
    crop = img.crop((x0, y0, x1, y1))
    crop.save(out_path)
    print(f"  -> wrote {out_path} ({crop.width}x{crop.height})")


def open_powerpoint():
    already_running = True
    try:
        win32com.client.GetActiveObject("PowerPoint.Application")
    except Exception:
        already_running = False
    print("PowerPoint already running before this script:", already_running)
    app = win32com.client.Dispatch("PowerPoint.Application")
    return app, already_running


def close_powerpoint(app, pres, already_running):
    if pres is not None:
        pres.Close()
    if not already_running:
        app.Quit()
    else:
        print("PowerPoint was already running elsewhere - left the app open, only closed our window")


def run_batch(source, candidates_path, out_dir):
    with open(candidates_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    candidates = data["candidates"]
    if not candidates:
        print("No diagram candidates in", candidates_path, "- nothing to render.")
        return

    os.makedirs(out_dir, exist_ok=True)
    prs = Presentation(source)
    slide_w_emu, slide_h_emu = prs.slide_width, prs.slide_height
    export_height = int(EXPORT_WIDTH * slide_h_emu / slide_w_emu)

    app, already_running = open_powerpoint()
    pres = None
    try:
        pres = app.Presentations.Open(source, ReadOnly=True, Untitled=False, WithWindow=True)
        for cand in candidates:
            slide_num = cand["slide"]
            print(f"Slide {slide_num}: shapes {cand['shape_ids']}")
            slide = prs.slides[slide_num - 1]
            bbox = bbox_for_shape_ids(slide, set(cand["shape_ids"]))
            if bbox is None:
                print(f"  no matching shapes found on slide {slide_num}, skipping")
                continue
            full_png = os.path.join(out_dir, f"_slide{slide_num:03d}_full.png")
            pres.Slides(slide_num).Export(full_png, "PNG", EXPORT_WIDTH, export_height)
            out_path = os.path.join(out_dir, f"s{slide_num:03d}_diagram.png")
            crop_and_save(full_png, bbox, slide_w_emu, slide_h_emu, EXPORT_WIDTH, export_height, out_path)
            os.remove(full_png)
    finally:
        close_powerpoint(app, pres, already_running)

    print(f"Batch complete: {len(candidates)} candidate(s) processed from {candidates_path}")


def run_single(source, slide_num, shape_ids_str, out_path):
    prs = Presentation(source)
    slide_w_emu, slide_h_emu = prs.slide_width, prs.slide_height
    export_height = int(EXPORT_WIDTH * slide_h_emu / slide_w_emu)

    wanted_ids = set(int(x) for x in shape_ids_str.split(","))
    slide = prs.slides[slide_num - 1]
    bbox = bbox_for_shape_ids(slide, wanted_ids)
    if bbox is None:
        print("No matching shapes found - nothing to render.")
        return

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    app, already_running = open_powerpoint()
    pres = None
    full_png = os.path.join(os.path.dirname(out_path), f"_slide{slide_num:03d}_full.png")
    try:
        pres = app.Presentations.Open(source, ReadOnly=True, Untitled=False, WithWindow=True)
        pres.Slides(slide_num).Export(full_png, "PNG", EXPORT_WIDTH, export_height)
    finally:
        close_powerpoint(app, pres, already_running)

    crop_and_save(full_png, bbox, slide_w_emu, slide_h_emu, EXPORT_WIDTH, export_height, out_path)
    os.remove(full_png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--slide", type=int, help="1-indexed slide number (manual single-slide mode)")
    ap.add_argument("--list", action="store_true", help="List shapes on --slide and exit")
    ap.add_argument("--shape-ids", help="Comma-separated shape IDs (manual single-slide mode)")
    ap.add_argument("--out", help="Output PNG path (manual single-slide mode)")
    ap.add_argument("--candidates", help="Path to diagram_candidates.json (batch mode)")
    ap.add_argument("--out-dir", help="Output directory for batch mode")
    args = ap.parse_args()

    if args.list:
        if not args.slide:
            ap.error("--slide is required with --list")
        prs = Presentation(args.source)
        list_shapes(prs, args.slide)
        return

    if args.candidates:
        if not args.out_dir:
            ap.error("--out-dir is required with --candidates")
        run_batch(args.source, args.candidates, args.out_dir)
        return

    if not args.slide or not args.shape_ids or not args.out:
        ap.error("Use --candidates/--out-dir for batch mode, or --slide/--shape-ids/--out for a single diagram")
    run_single(args.source, args.slide, args.shape_ids, args.out)


if __name__ == "__main__":
    main()
