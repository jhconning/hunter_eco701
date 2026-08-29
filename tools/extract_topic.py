"""
Step 1 of the topic-conversion pipeline: mechanical, free, fast.

Extracts text (bullets), tables, and regular picture shapes from a slide
range in a source .pptx, and writes a shape-type census so nothing silently
gets missed (this is what caught 3 un-extracted tables during the pilot).

Also DETECTS annotated diagrams automatically: any slide with a TABLE or
PICTURE plus a LINE, FREEFORM, or text-less AUTO_SHAPE (best-response
arrows, a circled equilibrium, a hand-drawn indifference curve, etc.) is
flagged as a diagram_candidate. Default policy (2026-07-15, Jonathan):
capture everything at full fidelity by default - a native Markdown table
recreation silently drops exactly this kind of annotation, which is
usually the pedagogical point, not decoration. Simplifying to a plain
table is a deliberate per-slide exception, not the default. See
render_diagram.py to batch-render every candidate this finds.

RECURSES INTO GROUP SHAPES. This matters: a shape nested inside a
PowerPoint GROUP reports left/top/width/height in the GROUP's own internal
child coordinate space, not slide-absolute coordinates (PowerPoint groups
carry a chOff/chExt transform) - python-pptx does not correct for this, so
naively cropping a nested equation/shape by its own reported position can
be wrong. The safe fix used here: whenever a GROUP contains an equation
(OLE object), a table, or a mix of anchor (table/picture) + annotation
(line/freeform/oval) content, the WHOLE GROUP is flagged as a diagram
candidate using the *group's own* shape_id - the group itself is a normal
top-level shape on the slide, so its own left/top/width/height ARE
slide-absolute and safe to crop directly. Individual nested equations are
therefore excluded from the plain "N equations, run render_equations.py"
count and handled via the group-level image capture instead.

Does NOT touch top-level equations (see render_equations.py) or call any
paid API.

Usage:
    mamba run -n ecopy python extract_topic.py \
        --source "Y:\Hunter\eco701\archive\slides\legacy\E701_F18 _slidesI.pptx" \
        --start 43 --end 102 \
        --out "Y:\Hunter\eco701\slides\02_constrained-optimization\raw"

Writes into --out:
    extracted.txt           - slide-by-slide text + table content, in reading order
    tables.json             - structured table data (same content as in extracted.txt)
    shape_census.json       - shape-type counts + OLE prog_ids for the range
    diagram_candidates.json - slides/groups needing render_diagram.py --batch
                              instead of a plain table or per-equation crop
    media/pic/              - regular picture shapes, sequentially named per slide
"""
import argparse
import json
import os
from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE_TYPE

ANNOTATION_TYPES = (MSO_SHAPE_TYPE.LINE, MSO_SHAPE_TYPE.FREEFORM)


def is_annotation_shape(shape):
    if shape.shape_type in ANNOTATION_TYPES:
        return True
    if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and not (
        shape.has_text_frame and shape.text_frame.text.strip()
    ):
        # A text-less auto-shape is very likely a circle/oval/highlight, not a
        # real content element - err inclusive: a false positive just means
        # one extra render, a false negative means silently lost annotation.
        return True
    return False


def extract_blip_image(shape, slide_part, idx, media_pic_dir, pic_counter):
    el = shape._element
    if len(el.findall(".//" + qn("p:oleObj"))) > 0:
        return pic_counter  # OLE preview image, not a standalone picture
    fnames = []
    for blip in el.findall(".//" + qn("a:blip")):
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
        fnames.append(fname)
    return pic_counter, fnames


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
    diagram_candidates = []
    grouped_diagram_ids = set()  # group shape_ids already queued this slide
    equation_review_slides = []  # slides with BOTH equations and annotation shapes -
                                  # ambiguous whether they're one geometric diagram or
                                  # unrelated content sharing a slide; needs a human look,
                                  # not an automatic grouping guess

    for idx, slide in enumerate(prs.slides, start=1):
        if idx < args.start:
            continue
        if idx > args.end:
            break

        lines.append(f"\n---\n\n## Slide {idx}\n")
        slide_part = slide.part

        anchor_shapes = []       # top-level tables/pictures
        annotation_shapes = []   # top-level lines/freeforms/text-less auto-shapes
        slide_equation_ids = []  # top-level equations, tracked separately (see review_needed below)
        grouped_diagram_ids = set()

        def handle_text(shape):
            if shape.has_text_frame and shape.text_frame.text.strip():
                for para in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in para.runs)
                    if text.strip():
                        indent = "  " * para.level
                        lines.append(f"{indent}- {text}")

        def inspect_group(group_shape):
            """Returns True if this group's contents mean it should be
            captured whole (equation inside, or anchor+annotation mixed)."""
            has_ole = False
            has_anchor = False
            has_annotation = False
            for child in group_shape.shapes:
                handle_text(child)
                ct = str(child.shape_type)
                shape_type_counts[ct] = shape_type_counts.get(ct, 0) + 1
                if child.shape_type == MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT:
                    has_ole = True
                    lines.append(f"[EQUATION shape {child.shape_id}, inside GROUP "
                                  f"{group_shape.shape_id}: see diagram_candidates.json - "
                                  f"whole group will be rendered as one image, not cropped individually]")
                elif child.has_table:
                    has_anchor = True
                    rows = [[c.text.replace("\n", " / ") for c in r.cells] for r in child.table.rows]
                    tables.append({"slide": idx, "shape_id": child.shape_id,
                                    "in_group": group_shape.shape_id, "rows": rows})
                elif child.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    has_anchor = True
                elif is_annotation_shape(child):
                    has_annotation = True
                elif child.shape_type == MSO_SHAPE_TYPE.GROUP:
                    # nested group-in-group - recurse; treat as its own candidate
                    if inspect_group(child):
                        grouped_diagram_ids.add(child.shape_id)
            return has_ole or (has_anchor and has_annotation)

        for shape in slide.shapes:
            st = str(shape.shape_type)
            shape_type_counts[st] = shape_type_counts.get(st, 0) + 1

            handle_text(shape)

            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                if inspect_group(shape):
                    grouped_diagram_ids.add(shape.shape_id)
                continue

            if is_annotation_shape(shape):
                annotation_shapes.append(shape.shape_id)

            if shape.has_table:
                rows = [[c.text.replace("\n", " / ") for c in r.cells] for r in shape.table.rows]
                tables.append({"slide": idx, "shape_id": shape.shape_id, "rows": rows})
                anchor_shapes.append(shape.shape_id)
                lines.append(f"[TABLE shape {shape.shape_id}: see tables.json - "
                              f"check diagram_candidates.json before using this as a plain table]")
                continue

            if shape.shape_type == MSO_SHAPE_TYPE.EMBEDDED_OLE_OBJECT:
                try:
                    prog_id = shape.ole_format.prog_id
                except Exception:
                    prog_id = "unknown"
                ole_progids[prog_id] = ole_progids.get(prog_id, 0) + 1
                slide_equation_ids.append(shape.shape_id)
                lines.append(f"[EQUATION shape {shape.shape_id} ({prog_id}): run render_equations.py]")
                continue

            result = extract_blip_image(shape, slide_part, idx, media_pic_dir, pic_counter)
            if isinstance(result, tuple):
                pic_counter, fnames = result
                for fname in fnames:
                    anchor_shapes.append(shape.shape_id)
                    lines.append(f"![Image](media/pic/{fname}) "
                                  f"[check diagram_candidates.json before treating as final]")
            else:
                pic_counter = result

        if anchor_shapes and annotation_shapes:
            diagram_candidates.append({
                "slide": idx,
                "shape_ids": anchor_shapes + annotation_shapes,
                "anchor_shape_ids": anchor_shapes,
                "annotation_shape_ids": annotation_shapes,
            })
        if slide_equation_ids and annotation_shapes:
            # Equations aren't treated as auto-batchable "anchors" like tables/pictures -
            # deciding which specific equations belong with which annotation shapes (a
            # real geometric diagram) vs. are just unrelated content sharing the slide
            # needs a human look, not a guessed grouping.
            equation_review_slides.append({
                "slide": idx,
                "equation_shape_ids": slide_equation_ids,
                "annotation_shape_ids": annotation_shapes,
            })
        for gid in grouped_diagram_ids:
            diagram_candidates.append({
                "slide": idx,
                "shape_ids": [gid],
                "anchor_shape_ids": [gid],
                "annotation_shape_ids": [],
                "note": "GROUP shape - rendered whole because nested shape positions "
                        "aren't reliably absolute; see module docstring",
            })

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

    with open(os.path.join(args.out, "diagram_candidates.json"), "w", encoding="utf-8") as f:
        json.dump({"source_file": os.path.basename(args.source), "candidates": diagram_candidates}, f, indent=2)

    with open(os.path.join(args.out, "equation_review_needed.json"), "w", encoding="utf-8") as f:
        json.dump({"source_file": os.path.basename(args.source), "slides": equation_review_slides}, f, indent=2)

    n_grouped = sum(1 for c in diagram_candidates if not c["annotation_shape_ids"] and len(c["shape_ids"]) == 1)
    print(f"Extracted slides {args.start}-{args.end} from {os.path.basename(args.source)}")
    print(f"  {pic_counter} pictures, {len(tables)} tables, {sum(ole_progids.values())} top-level equations")
    print(f"  shape census: {shape_type_counts}")
    if diagram_candidates:
        print(f"  *** {len(diagram_candidates)} DIAGRAM CANDIDATE(S) detected on slides: "
              f"{[c['slide'] for c in diagram_candidates]} "
              f"({n_grouped} are whole-GROUP captures - equations/mixed content nested in a "
              f"group, excluded from the top-level equation count above) ***")
        print(f"      Default policy: capture these with render_diagram.py --batch, "
              f"don't reduce to a plain table/skip without a deliberate reason.")
    if equation_review_slides:
        print(f"  *** {len(equation_review_slides)} slide(s) have BOTH equations AND annotation "
              f"shapes together: {[s['slide'] for s in equation_review_slides]} ***")
        print(f"      These need a human look (see equation_review_needed.json) - it's ambiguous "
              f"whether the equations are part of one geometric diagram with the annotation "
              f"(capture together via render_diagram.py) or unrelated content sharing a slide "
              f"(fine to crop equations individually via render_equations.py).")
    print(f"  -> wrote extracted.txt, tables.json, shape_census.json, "
          f"diagram_candidates.json, equation_review_needed.json to {args.out}")


if __name__ == "__main__":
    main()
