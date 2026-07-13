# ECO 701: Microeconomic Theory
**Hunter College Economics**

Welcome to the course repository for ECO 701: Microeconomic Theory. This is an advanced undergraduate and Master's level course emphasizing constrained optimization, modern microeconomic theory, and interactive computational methods using Python and Jupyter Notebooks.

🌐 **Live Course Site & Slides:** [https://jhconning.github.io/hunter_eco701/](https://jhconning.github.io/hunter_eco701/)

## Course Structure
- **Syllabus & Ideas:** [`syllabus/`](syllabus/) — see [`IDEAS.md`](syllabus/IDEAS.md) for the 11-topic course sequence
- **Lectures & Slides (Marp):** [`slides/`](slides/)
- **Interactive Python Assignments:** [`notebooks/`](notebooks/)
- **Problem Sets:** [`ps/`](ps/)

*Note: Legacy materials from the 2018 iteration of this course can be found in the `legacy/` directory (not tracked in git — see `.gitignore`).*

## How `slides/` is organized

Each topic gets its own numbered folder matching `syllabus/IDEAS.md`'s
sequence, e.g. `slides/08_essentials-of-game-theory/`. Inside each topic:

- **`deck.md`** — the actual Marp slide deck. Hand-authored/redesigned,
  never auto-overwritten.
- **`media/`** — final images actually used in `deck.md`, meaningfully named
  (`nash-portrait.png`, not `slide017_pic0001.png`).
- **`raw/`** — mechanical extraction output from the source PowerPoint
  (text dump, table data, equation crops, Mathpix OCR results). Fully
  regeneratable — safe to delete and re-run the extraction pipeline; never
  hand-edited.
- **`source.yml`** — which original `.pptx` file and slide range this topic
  came from, and how confident that mapping is.

A shared Marp theme lives in `slides/_shared/eco701-theme.css` (registered
via `--theme-set` in the CI workflow) so every topic looks consistent — no
more per-file theme copies.

**Topics done so far:** `00_logistics` (front-matter, not part of the
11-topic sequence), `01_definitions-and-key-tools`,
`08_essentials-of-game-theory`. See [`TOPIC_PLAN.md`](TOPIC_PLAN.md) for the
proposed mapping of the remaining topics to the legacy slide decks — it's a
draft with open questions, not a finished plan. If you're picking this work
up cold, read [`HANDOFF.md`](HANDOFF.md) first.

<!-- TOC_START -->

*Last Deployed: 2026-05-03 21:29 EST*

## Deployed Presentations

- [ECO 701 Topic 1: Definitions and Key Tools](https://jhconning.github.io/hunter_eco701/slides/sl_1_intro.html) ([PDF](https://jhconning.github.io/hunter_eco701/slides/sl_1_intro.pdf)) *(Last edit: 2026-05-03 21:27)*
<!-- TOC_END -->
