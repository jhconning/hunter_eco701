"""
Step 2 of the topic-conversion pipeline: renders legacy OLE equation objects
(MathType/Equation Editor) as clean PNG crops, using PowerPoint's own
renderer via COM automation - avoids trying to decode the raw WMF/EMF images
directly, which is unreliable.

Requires: Windows + PowerPoint installed + pywin32 (`mamba install pywin32`).

SAFETY: if PowerPoint is already running with other work open, this script
does NOT call Application.Quit() - it only closes the one presentation
window it opens itself, so nothing else you have open gets disturbed.
Check `tasklist | grep POWERPNT` yourself first if unsure.

Usage:
    mamba run -n ecopy python render_equations.py \
        --source "Y:\Hunter\Eco 701\past\eco701_F18\slides\E701_F18 _slidesI.pptx" \
        --start 43 --end 102 \
        --out "Y:\Hunter\Eco 701\Eco701\slides\02_constrained-optimization\raw"

Writes into --out:
    media/slide_png/     - full-slide PNG exports (intermediate, used for cropping)
    media/eq/            - cropped equation images, ready for mathpix_ocr.py
"""
import argparse
import os
import win32com.client
from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

EXPORT_WIDTH = 2400  # px - high-res so cropped equations stay legible
PAD = 8  # px padding around cropped equation bounding boxes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--start", type=int, required=True)
    ap.add_argument("--end", type=int, required=True)
    ap.add_argument("--out", required=True, help="Output raw/ folder for this topic")
    args = ap.parse_args()

    slide_png_dir = os.path.join(args.out, "media", "slide_png")
    eq_dir = os.path.join(args.out, "media", "eq")
    os.makedirs(slide_png_dir, exist_ok=True)
    os.makedirs(eq_dir, exist_ok=True)

    prs = Presentation(args.source)
    slide_w_emu = prs.slide_width
    slide_h_emu = prs.slide_height
    export_height = int(EXPORT_WIDTH * slide_h_emu / slide_w_emu)

    ole_boxes = []
    for idx, slide in enumerate(prs.slides, start=1):
        if idx < args.start:
            continue
        if idx > args.end:
            break
        for shape in slide.shapes:
            if shape.shape_type == MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT:
                try:
                    prog_id = shape.ole_format.prog_id
                except Exception:
                    prog_id = "unknown"
                ole_boxes.append((idx, shape.shape_id, shape.left, shape.top, shape.width, shape.height, prog_id))

    print(f"Found {len(ole_boxes)} OLE (equation) shapes in slides {args.start}-{args.end}")
    if not ole_boxes:
        print("Nothing to render - exiting.")
        return

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
        slide_indices = sorted(set(b[0] for b in ole_boxes))
        for idx in slide_indices:
            slide = pres.Slides(idx)
            out_path = os.path.join(slide_png_dir, f"slide{idx:03d}.png")
            slide.Export(out_path, "PNG", EXPORT_WIDTH, export_height)
        print(f"Exported {len(slide_indices)} full-slide PNGs (only slides with equations)")
    finally:
        if pres is not None:
            pres.Close()
        if not already_running:
            app.Quit()
        else:
            print("PowerPoint was already running elsewhere - left the app open, only closed our window")

    px_per_emu_x = EXPORT_WIDTH / slide_w_emu
    px_per_emu_y = export_height / slide_h_emu

    for (idx, shape_id, left, top, width, height, prog_id) in ole_boxes:
        slide_png_path = os.path.join(slide_png_dir, f"slide{idx:03d}.png")
        img = Image.open(slide_png_path)
        x0 = max(0, int(left * px_per_emu_x) - PAD)
        y0 = max(0, int(top * px_per_emu_y) - PAD)
        x1 = min(img.width, int((left + width) * px_per_emu_x) + PAD)
        y1 = min(img.height, int((top + height) * px_per_emu_y) + PAD)
        crop = img.crop((x0, y0, x1, y1))
        fname = f"s{idx:03d}_eq_shape{shape_id}.png"
        crop.save(os.path.join(eq_dir, fname))
        print(f"  cropped {fname} ({prog_id})")

    print(f"-> wrote {len(ole_boxes)} equation crops to {eq_dir}")


if __name__ == "__main__":
    main()
