"""
Step 1 of the topic-conversion pipeline: mechanical, free, fast.

Extracts text (bullets), tables, and regular picture shapes from a slide
range in a source .pptx, and writes a shape-type census so nothing silently
gets missed (this is what caught 3 un-extracted tables during the pilot).

Does NOT touch equations (see render_equations.py) or call any paid API.

Usage:
    mamba run -n ecopy python extract_topic.py \
        --source "Y:\Hunter\Eco 701\past\eco701_F18\slides\E701_F18 _slidesI.pptx" \
        --start 43 --end 102 \
        --out "Y:\Hunter\Eco 701\Eco701\slides\02_constrained-optimization\raw"

Writes into --out:
    extracted.txt        - slide-by-slide text + table content, in reading order
    tables.json          - structured table data (same content as in extracted.txt)
    shape_census.json    - shape-type counts + OLE prog_ids for the range
    media/pic/           - regular picture shapes, sequentially named per slide
"""
import argparse
import json
import os
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE_TYPE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="Path to source .pptx")
    ap.add_argument("--start", type=int, required=True, help="First slide number (1-indexed, inclusive)")
    ap.add_argument("--end", type=int, required=True, help="Last slide number (1-indexed, inclusive)")
    ap.add_argument("--out", required=True, help="Output raw/ folder for this topic")
    args = ap.parse_args()

    media_pic_dir = os.path.join(args.out, "media", "pic")
    os.makedirs(media_pic_dir, exist_ok=True)

    prs = Presentation(args.source)

    lines = []
    tables = []
    shape_type_counts = {}
    ole_progids = {}
    pic_counter = 0

    for idx, slide in enumerate(prs.slides, start=1):
        if idx < args.start:
            continue
        if idx > args.end:
            break

        lines.append(f"\n---\n\n## Slide {idx}\n")
        slide_part = slide.part

        for shape in slide.shapes:
            st = str(shape.shape_type)
            shape_type_counts[st] = shape_type_counts.get(st, 0) + 1

            if shape.has_text_frame and shape.text_frame.text.strip():
                for para in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in para.runs)
                    if text.strip():
                        indent = "  " * para.level
                        lines.append(f"{indent}- {text}")

            if shape.has_table:
                rows = [[c.text.replace("\n", " / ") for c in r.cells] for r in shape.table.rows]
                tables.append({"slide": idx, "shape_id": shape.shape_id, "rows": rows})
                lines.append(f"[TABLE shape {shape.shape_id}: see tables.json]")
                continue

            if shape.shape_type == MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT:
                try:
                    prog_id = shape.ole_format.prog_id
                except Exception:
                    prog_id = "unknown"
                ole_progids[prog_id] = ole_progids.get(prog_id, 0) + 1
                lines.append(f"[EQUATION shape {shape.shape_id} ({prog_id}): run render_equations.py]")
                continue

            el = shape._element
            is_ole_container = len(el.findall(".//" + qn("p:oleObj"))) > 0
            if is_ole_container:
                continue

            blips = el.findall(".//" + qn("a:blip"))
            for blip in blips:
                rId = blip.get(qn("r:embed"))
                if not rId:
                    continue
                try:
                    part = slide_part.rels[rId].target_part
                except KeyError:
                    continue
                ext = part.partname.ext
                pic_counter += 1
                fname = f"s{idx:03d}_pic{pic_counter:02d}.{ext}"
                with open(os.path.join(media_pic_dir, fname), "wb") as f:
                    f.write(part.blob)
                lines.append(f"![Image](media/pic/{fname})")

    with open(os.path.join(args.out, "extracted.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(os.path.join(args.out, "tables.json"), "w", encoding="utf-8") as f:
        json.dump({"source_file": os.path.basename(args.source), "tables": tables}, f, indent=2)

    with open(os.path.join(args.out, "shape_census.json"), "w", encoding="utf-8") as f:
        json.dump({
            "source_file": os.path.basename(args.source),
            "slide_range": [args.start, args.end],
            "shape_type_counts": shape_type_counts,
            "ole_prog_ids": ole_progids,
            "images_extracted": pic_counter,
        }, f, indent=2)

    print(f"Extracted slides {args.start}-{args.end} from {os.path.basename(args.source)}")
    print(f"  {pic_counter} pictures, {len(tables)} tables, {sum(ole_progids.values())} equations")
    print(f"  shape census: {shape_type_counts}")
    print(f"  -> wrote extracted.txt, tables.json, shape_census.json to {args.out}")


if __name__ == "__main__":
    main()
