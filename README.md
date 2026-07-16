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
`08_essentials-of-game-theory`, and `02_constrained-optimization` (all three
sub-chunks, complete end to end). See [`TOPIC_PLAN.md`](TOPIC_PLAN.md) for
the mapping of the remaining topics to the legacy slide decks. If you're
picking this work up cold, read [`HANDOFF.md`](HANDOFF.md) first.

## `notebooks/`

Companion Jupyter notebooks, two per topic so far:

- [`topic02_constrained_optimization_figures.ipynb`](notebooks/topic02_constrained_optimization_figures.ipynb)
  regenerates the deck's static figures directly from their underlying
  formulas (matplotlib), plus a few `ipywidgets`/`plotly` demos for live
  in-class use. Proof-of-concept status — see `HANDOFF.md` for what's
  decided vs. still open.
- [`topic02_constrained_optimization_numerical.ipynb`](notebooks/topic02_constrained_optimization_numerical.ipynb)
  goes further: it *sets up and solves* every major constrained-optimization
  example from the deck as running code (symbolic Lagrangians via `sympy`,
  numerical solves via `scipy.optimize`), including a genuine corner
  solution, the multi-constraint Earthquake Relief problem solved two ways,
  and a numerical check of the shadow-price interpretation of $\lambda$.

<!-- TOC_START -->

*Last Deployed: 2026-07-16 09:00 EST*

## Deployed Presentations

- [ECO 701: Welcome & Course Logistics](https://jhconning.github.io/hunter_eco701/slides/00_logistics/deck.html) ([PDF](https://jhconning.github.io/hunter_eco701/slides/00_logistics/deck.pdf)) *(Last edit: 2026-07-15 11:25)*
- [ECO 701 Topic 1: Definitions and Key Tools](https://jhconning.github.io/hunter_eco701/slides/01_definitions-and-key-tools/deck.html) ([PDF](https://jhconning.github.io/hunter_eco701/slides/01_definitions-and-key-tools/deck.pdf)) *(Last edit: 2026-07-15 11:25)*
- [ECO 701 Topic 2: Constrained Optimization](https://jhconning.github.io/hunter_eco701/slides/02_constrained-optimization/deck.html) ([PDF](https://jhconning.github.io/hunter_eco701/slides/02_constrained-optimization/deck.pdf)) *(Last edit: 2026-07-16 09:00)*
- [ECO 701 Topic 8: Essentials of Game Theory](https://jhconning.github.io/hunter_eco701/slides/08_essentials-of-game-theory/deck.html) ([PDF](https://jhconning.github.io/hunter_eco701/slides/08_essentials-of-game-theory/deck.pdf)) *(Last edit: 2026-07-15 12:51)*
<!-- TOC_END -->
