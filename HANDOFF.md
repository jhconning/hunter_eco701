# Handoff: Eco 701 slide modernization

Read this first if you're picking up this work in a fresh conversation.
Originally written 2026-07-13; rewritten 2026-07-19 for the move from Marp
to Quarto + revealjs. The Marp-era version of this file (extraction-pipeline
gotchas for Topics 1/2/3/8, the original Marp theme/CI details) is archived
at [`docs/archive/HANDOFF-marp.md`](docs/archive/HANDOFF-marp.md) — still
worth reading for the *why* behind existing content, but not the live
workflow anymore.

## What this project is

Jonathan is modernizing Eco 701 (Master's Microeconomic Theory) from old
PowerPoint slides into Quarto/revealjs markdown slides, organized around the
11-topic course sequence (originally drafted in `syllabus/IDEAS.md` — that
file is gitignored/private by deliberate choice, so don't link to it from
anything public-facing; [`TOPIC_PLAN.md`](TOPIC_PLAN.md) is the tracked,
public equivalent). The end goal is a live course site (GitHub Pages) with
slides, notes, and problem sets all built from the same markdown source.

**This is NOT a fresh project** — a real repo (`jhconning/hunter_eco701`)
already existed with a working GitHub Pages deploy pipeline before this
reorganization started, and 5 topics were fully built and deployed *in
Marp* before the move to Quarto (see "Migration status" below).

## Migration status (2026-07-19)

The slide engine is moving from Marp to Quarto + revealjs — better fragment
support (any element, not just bullet lists — see "Fragments" below),
richer layout primitives (columns, tabsets, `.r-stack`), and native
interactive Python (Plotly) embedding. The evaluation that led to this
decision (a full trial port of Topic 1, a feature-showcase deck, and a
working theme) originally lived in the scratch folder `slides/quarto-test/`;
its real output (the theme, this document's own gotchas section) was
folded in here and at `slides/_shared/eco701-revealjs.scss` back when the
migration was first evaluated, and the scratch folder itself was deleted
2026-07-19 once every finding was captured. The one part of it worth
keeping as an ongoing reference — `quarto_demo.qmd`, a grab-bag demo of
revealjs features (columns, callouts, fragments, tabsets, live Plotly,
etc.), not course content — now lives at
[`docs/quarto-feature-demo/quarto_demo.qmd`](docs/quarto-feature-demo/quarto_demo.qmd).

**As of this writing, migration is in progress.** Check each topic's
`source.yml` for its actual current format (`deck.md` = still Marp,
`deck.qmd` = migrated). Topics 4-7, 8b, 9-11 have no source material
converted yet at all (per `TOPIC_PLAN.md`) — those get authored directly in
Quarto from the start, no migration involved.

## Where everything is

- **Repo root:** `Y:\Hunter\Eco 701\Eco701\` (note: no space — do not confuse
  with `Y:\Hunter\Eco 701\past\` or the top-level `Y:\Hunter\Eco 701\slides\`,
  which are unrelated old folders that happen to be nearby)
- **GitHub remote:** `jhconning/hunter_eco701`, remote name `hunter_eco701`
  (not `origin`)
- **Live site:** https://jhconning.github.io/hunter_eco701/ — deploys ONLY on
  push to `main`. Never push to `main` directly without Jonathan's explicit
  go-ahead; work on a branch and open a PR (PRs build via CI but don't
  deploy).
- **Legacy source pptx files:** `legacy/slides/E701_F18 _slidesI.pptx` (337
  slides), `_slidesII.pptx` (258 slides), `_slidesIIb.pptx` (224 slides).
  This folder is gitignored — it's reference material, not tracked.

## Architecture

Each topic is a folder under `slides/`, numbered to match `IDEAS.md`:

```
slides/
  _shared/eco701-revealjs.scss   <- the one shared Quarto theme (navy/serif/amber)
  _shared/eco701-theme.css       <- the old Marp theme - remove once every deck is migrated
  00_logistics/                   <- front-matter, not one of the 11 numbered topics
  01_definitions-and-key-tools/   <- IDEAS.md Topic 1
    deck.qmd                      <- hand-authored Quarto deck. THE deliverable. Never auto-overwritten.
    media/                        <- final images actually used in deck.qmd, meaningfully named
    raw/                          <- mechanical extraction output. Regeneratable. Never hand-edit.
    source.yml                    <- provenance: which pptx, which slide range, confidence level, current format
    new_ideas.md                  <- backlog of expansion ideas (new slides, viz, problem sets) - not a plan
    figs/                         <- notebook-generated candidate figures, staged for review (optional) -
                                      see "Code-generated figures" below for the promotion procedure
```

Retired topics move to `docs/archive/<topic-folder>/` rather than staying
under `slides/` (which the CI build scans wholesale) - see Topic 8's own
archival note there for the pattern and the reasoning behind it.

Read the actual `source.yml` and `deck.qmd` in `01_definitions-and-key-tools/`
for a concrete, fully-migrated example before building or converting a new
topic — it shows the pattern better than more prose here.

## The extraction pipeline (`tools/`) — unchanged by the Quarto move

Pulling raw content out of the legacy pptx files is completely independent
of which slide engine the output targets. See
[`tools/README.md`](tools/README.md) for the authoritative step order (same
as always: `title_scan.py` → `extract_topic.py` → `render_equations.py` (if
needed) → `mathpix_ocr.py` (if needed) → `render_diagram.py` (if the shape
census flagged candidates)). Then a human (you) reads the raw output, catches
gaps, and hand-writes `deck.qmd` — that step is not automated and shouldn't
be; see "What doesn't scale" at the end of this file.

Setup: `mamba install -n ecopy -c conda-forge python-pptx pillow requests
pywin32`. Mathpix credentials live in `.env` at the repo root (gitignored).

## Authoring a deck.qmd

### Structural conventions (Marp → Quarto, if porting existing content)

- One `##` heading per slide, always paired with an explicit `---`
  separator (both together, not relying on heading-level slide-breaking
  alone) — mirrors Marp's own one-`---`-per-slide shape, so a port stays
  close to mechanical.
- Marp `<!-- _class: lead/divider/compact -->` → Quarto heading attribute
  `## Heading {.divider}` / `{.compact}`, styled in
  `eco701-revealjs.scss`'s `scss:rules` block. Marp's title/lead slide →
  Quarto's auto-generated title slide (from `title:`/`subtitle:`/
  `author:`/`institute:` YAML) rather than hand-building a replica — not
  pixel-identical but close, and much less work.
- Marp `![bg right:NN% wNNN](img)` (split background-image layout) → Quarto
  `::: {.columns}` / `::: {.column width="X%"}` with a plain `![](img)` in
  one column. Not a mechanical copy — needs a per-slide judgment call on
  the split, but the visual result is a close match.
- A slide can have **no heading at all** — Pandoc is fine with heading-less
  content between `---` markers (useful for a bold-statement/pull-quote
  style slide that isn't really a new topic heading).
- HTML comments (`<!-- ... -->`) carry over unchanged — Pandoc treats them
  as real comments, same as Marp. Keep using them for provenance/rationale
  notes that shouldn't render.
- Math (`$...$`/`$$...$$`) carries over unchanged. Set `html-math-method:
  katex` explicitly in the YAML (Quarto defaults to MathJax otherwise).

### Fragments (the whole reason for the Quarto move)

- `::: {.incremental}` around a list ≈ Marp's `*`-bullet trick, but works
  regardless of what follows on the slide (Marp's version broke if a
  non-bulleted element, like a blockquote, came after the list).
- `::: {.fragment}` around **any** block (blockquote, image, equation, div)
  is the real upgrade — wrap a closing blockquote in its own `.fragment` and
  it arrives last, after an `.incremental` list finishes, which Marp could
  never do.
- reveal.js ships fragment *styles* beyond plain fade-in:
  `[text]{.fragment .highlight-red}` / `-green` / `-blue` — click to color a
  specific phrase, no custom CSS needed.

### Tabsets — use sequential slides instead, not `.panel-tabset`

`.panel-tabset` only exports its default tab to the PDF — Tabby.js (the tab
library) hides every non-active panel via inline style on page load, and
this is not fixable via CSS (a `@media print` override to force all panels
visible was tested and had zero effect; decktape doesn't evaluate print
media here, and the same limitation likely applies to Quarto's own
documented manual-print method too, since it doesn't touch Tabby's JS state
either). **Standing convention: if the "show A, then B, then C" content
needs to survive to a printed PDF, use three separate sequential slides
instead of a tabset.** Reserve tabsets (if ever) for genuinely
live-presentation-only content, same category as speaker notes.

### Executable Python cells (Plotly, etc.)

A `.qmd` can mix pre-generated static images (the existing `figs/` → review
→ `media/` promotion workflow below, unchanged) with live executable code
cells (` ```{python} `) that run at render time via the `ecopy` Jupyter
kernel (`jupyter: ecopy` in the YAML). Use live cells selectively, where
interactivity is itself the pedagogical point (e.g. a hoverable/zoomable
Plotly reaction-curve graph, or a Plotly slider with precomputed frames as
the static-export-safe stand-in for `ipywidgets.interact` — true
`ipywidgets` interactivity needs a live kernel and does not survive to the
deployed static site, so that pattern stays in the companion Jupyter
notebooks, same as it already does today). Default to static images for
everything else.

## Rendering and verification

```
quarto render deck.qmd     # -> deck.html + deck_files/
```

Quarto has **no built-in PDF export for revealjs** (confirmed via its own
docs and an open, unresolved upstream GitHub issue asking for one). The tool
that fills this gap — and the one CI uses — is **decktape**, a
Puppeteer-based headless-Chrome exporter built for reveal.js presentations
generally (not Quarto-specific; it also has an adapter for bespoke.js, the
engine Marp's own compiled output uses under the hood):

```
npx -y decktape reveal --size "1280x720" deck.html deck.pdf
```

To re-check a single slide after a small fix (much cheaper than re-reading
a whole deck), extract just that page as a PNG with PyMuPDF (`fitz`,
already in `ecopy`):

```python
import fitz
doc = fitz.open("deck.pdf")
doc[page_num - 1].get_pixmap(dpi=150).save("check.png")
```

Caveats:
- decktape captures each slide's fully-revealed end state (all fragments
  "clicked through") — fine for checking layout/overflow, useless for
  confirming fragment *order* is right. Cross-check the compiled HTML
  directly for that (`grep` for `data-fragment-index`, `class="notes"` for
  speaker notes, `data-auto-animate`/`data-id="..."` for auto-animate,
  `data-code-line-numbers="..."` for progressive code reveal — all things a
  static PDF capture can't show visually).
- `pdftoppm`/poppler isn't installed here, so the Read tool's `pages=`
  parameter won't work on these PDFs — read the whole PDF at once for a
  small deck, or use the PyMuPDF single-page trick above for anything
  larger.

## `.columns` gotcha — read before touching column layout

Quarto's base revealjs theme sets `div.column { display: inline-block;
width: 50% }` with **no logic for more than two columns**, and
`.columns { display: initial }`, which resets `display` to CSS's real
initial value — `inline`, not `block`. Combined with this theme's own
`h2 { display: inline-block }` rule (needed so the amber underline hugs the
heading text), a `.columns` block can end up sharing one inline formatting
context with the heading above it: content crowds the title instead of
starting a new line, and `margin-top` on `.columns` silently does nothing
(vertical margins are specified to have no effect on `display: inline`
elements — this isn't a bug, it's spec behavior). The fix, already applied
in `eco701-revealjs.scss`:

```scss
.reveal .columns {
  display: flex;
  margin-top: 0.8em;
}
```

If `.columns` ever looks wrong again, check `display` on `.columns` and any
`display: inline-block` ancestor/sibling (especially a heading rule) before
assuming it's a width or spacing problem — width/spacing were both
plausible-looking wrong guesses before the real cause was found.

## Known content-fidelity gaps (Quarto vs. Marp)

1. **`\underbrace{X}_{\text{label}}` loses its label text** under Quarto's
   KaTeX setup here, unlike Marp's KaTeX. Likely a macro/version
   difference; not chased down further. Avoid this construct, or verify the
   rendered slide directly if used.
2. **Content fit is not free when porting.** Font-size/layout numbers don't
   transfer 1:1 from the old Marp theme — budget a real re-verification
   pass per slide (same discipline as the `tools/verify_deck.py` overflow
   check, just against Quarto's layout model instead of Marp's).
3. **matplotlib's own mathtext parser is stricter than KaTeX** — `\frac14`
   (no braces) works in KaTeX-rendered slide text but throws inside a
   matplotlib figure label; use the fully-braced `\frac{1}{4}` in any
   code-generated figure with embedded math.
4. **`.r-stack` needs a blank line between each stacked image/element.**
   Adjacent `![](...)` lines with no blank line between them get merged by
   Pandoc into one `<p>` with inline `<img>`s — `.r-stack`'s
   absolute-positioning CSS never applies, since there's only one child to
   stack. Always separate stacked elements with a blank line.

## Code-generated figures (`notebooks/`) — unchanged by the Quarto move

Every topic folder can have a `slides/<topic>/figs/` directory — a sibling
of `media/`, `raw/`, `source.yml` — holding notebook-generated *candidate*
figures. Git-tracked (so a diff shows exactly what a regenerated figure
would change) but not where `deck.qmd` points its `![](...)` references.

**Promotion procedure:**
1. Notebook cell calls `savefig(fig, "name.png")` → lands in `figs/`.
2. Jonathan reviews it against what's currently live in `media/`. **Never
   swap automatically** — always a deliberate, individual decision.
3. If approved: copy into `media/` under the same filename `deck.qmd`
   already references — `cp figs/x.png media/x.png`.
4. Rebuild + verify before committing.
5. Commit the `media/` swap and, if the notebook changed, the regenerated
   `figs/` file together.

## Source material for future topics (unaffected by the slide-engine move)

- **Bowles & Halliday (2022), "Microeconomics: Competition, Conflict, and
  Coordination"** — PDF at `Y:\E\ebooks\economics\bowleshalliday_final_2022.pdf`
  (1072 pages). Chapter 1 (used for Topic 1) is pages 35-85 — the embedded
  PDF outline's page numbers are broken/non-monotonic, so search page text
  directly rather than trusting `doc.get_toc()`.
- `BH\BowlesNotes.md` — old notes from a prior course iteration, a useful
  head start for later chapters.
- `legacy/Bowles/` (2016 draft) and the rest of `BH/` (old 2018 PowerPoint
  chapters, syllabus, worksheets) are unrelated leftover material — ignore.

## What doesn't scale (don't try to automate this part)

The mechanical extraction pipeline is fully scriptable and should just run.
The *redesign* — reorganizing content, writing real titles, verifying
payoff matrices by hand, deciding what to split/merge/cut, choosing which
lists become `.incremental` and which images become `.columns` splits — is
judgment applied slide-by-slide. Budget real time for this per topic; don't
try to template it away.
