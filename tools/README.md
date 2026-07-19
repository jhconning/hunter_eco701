# Conversion pipeline

Run in this order for a new topic:

1. **`title_scan.py`** (optional, planning only) — cheap title-only scan to
   confirm a slide range before committing to it. Output should NOT be
   written under `slides/` (marp-cli will try to build any `.md` it finds
   there) - use a scratch path.

2. **`extract_topic.py`** — mechanical, free, fast. Pulls text, tables, and
   regular pictures for a slide range. Always check the printed shape
   census against what you expect before moving on - this is what catches
   silently-skipped content (it caught 3 missed tables during the pilot).
   It also writes `diagram_candidates.json` and prints a loud warning if it
   finds any table/picture with annotation shapes (arrows, ovals) layered
   on top - **treat that warning as a required step, not an FYI.**

3. **`render_equations.py`** — only if the shape census shows
   `EMBEDDED_OLE_OBJECT` shapes (legacy MathType/Equation Editor equations).
   Drives PowerPoint via COM automation to export crisp equation crops.
   Windows + PowerPoint + `pywin32` only. Safe to run alongside other
   PowerPoint work you have open (see the safety note in the script).

4. **`mathpix_ocr.py`** — only after checking how many equations there are
   (small real cost per call, against Jonathan's own Mathpix account).
   Needs `.env` at the repo root with `MATHPIX_APP_ID` / `MATHPIX_APP_KEY`.

5. **`render_diagram.py --candidates raw/diagram_candidates.json --out-dir
   raw/media/diagrams`** — **run this by default whenever step 2 reported
   any candidates, not just when one looks obviously important.** A native
   Markdown table recreation silently drops exactly the hand-drawn
   annotation (best-response arrows, circled equilibria) that usually IS
   the pedagogical point - see HANDOFF.md's "Table vs. diagram" note.
   Batch mode processes every candidate in one PowerPoint session. Use
   `--slide N --list` + `--shape-ids ... --out ...` (manual single-slide
   mode) only to hand-trim a crop the batch heuristic got too wide, or to
   capture a diagram the heuristic missed entirely.

None of these touch `slides/<topic>/deck.qmd` or `slides/<topic>/media/`
directly - those are hand-authored once the raw material has been reviewed.
See the root `HANDOFF.md` for the full redesign and Quarto-authoring
workflow (not just extraction) - this pipeline is unaffected by the
Marp-to-Quarto slide-engine move, since it only pulls raw content out of
the legacy pptx files.

## Setup

```
mamba install -n ecopy -c conda-forge python-pptx pillow requests pywin32
```

(pandoc, ImageMagick are NOT part of this pipeline - pandoc can't read
.pptx, and ImageMagick's WMF/EMF support proved unreliable on this machine;
PowerPoint's own COM-automated rendering replaced both.)
