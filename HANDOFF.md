# Handoff: Eco 701 slide modernization

Read this first if you're picking up this work in a fresh conversation. This
is the single living handoff for the project — there are no phase-specific
handoff files (a `PHASE4-HANDOFF.md` existed briefly in July 2026 and was
removed 2026-08-26; everything in it that was still true is folded in below).
The Marp-era version of this document — extraction-pipeline gotchas for the
original Topics 1/2/3/8, the old Marp theme and CI details — is archived at
[`docs/archive/HANDOFF-marp.md`](docs/archive/HANDOFF-marp.md). It's still
worth reading for the *why* behind existing content, but it is not the live
workflow.

Last rewritten 2026-08-26.

---

## 1. Purpose

Jonathan is modernizing Eco 701 (Master's Microeconomic Theory, Hunter
College) from a 2018 set of PowerPoint decks into Quarto/revealjs markdown
slides, organized around an 11-topic course sequence. The end goal is a live
course site on GitHub Pages with slides, companion Jupyter notebooks, and
problem sets all built from the same markdown source.

**This is not a fresh project.** A real repo (`jhconning/hunter_eco701`)
with a working GitHub Pages deploy pipeline existed before this
reorganization started, and five topics were fully built and deployed *in
Marp* before the move to Quarto.

The topic sequence itself is drafted in `syllabus/IDEAS.md`, which is
deliberately gitignored/private — don't link to it from anything
public-facing. [`TOPIC_PLAN.md`](TOPIC_PLAN.md) is the tracked, public
equivalent, and it also records which legacy slide ranges map onto which
topic and every structural decision made so far (including why Topic 8 was
dissolved and why `slidesIIb` supersedes `slidesII`).

### Why Quarto instead of Marp

The migration was decided after a full trial port of Topic 1, a
feature-showcase deck, and a working theme. Three reasons:

1. **Fragments on any element**, not just bullet lists. Marp's `*`-bullet
   trick broke as soon as a non-bulleted element followed the list; Quarto's
   `::: {.fragment}` wraps a blockquote, image, equation, or div.
2. **Richer layout primitives** — real columns, `.r-stack`, callouts.
3. **Native executable Python**, so a Plotly figure can be live and
   interactive on the slide rather than a static export.

The scratch evaluation folder (`slides/quarto-test/`) was deleted 2026-07-19
once every finding was captured here and in the theme. The one piece worth
keeping as an ongoing reference is
[`docs/quarto-feature-demo/quarto_demo.qmd`](docs/quarto-feature-demo/quarto_demo.qmd)
— a grab-bag demo of revealjs features (columns, callouts, fragments,
tabsets, live Plotly), not course content.

---

## 2. Where everything is

- **Repo root:** `Y:\Hunter\eco701\` (unified root matching eco331 model).
- **GitHub remote:** `jhconning/hunter_eco701`, remote name `hunter_eco701`
  (**not** `origin`).
- **Live site:** https://jhconning.github.io/hunter_eco701/ — deploys
  **only** on push to `main`, via `.github/workflows/deploy-myst.yml`.
- **Legacy source pptx:** `archive/slides/legacy/E701_F18 _slidesI.pptx` (337
  slides), `_slidesII.pptx` (258), `_slidesIIb.pptx` (224). Gitignored —
  reference material, not tracked. `slidesIIb` is the authoritative revision;
  don't extract from `slidesII`.
- **Python:** the `ecopy` mamba environment. Run scripts as
  `mamba run -n ecopy python <script>`.

---

## 3. Organization

Each topic is a folder under `slides/`, numbered to match the topic
sequence:

```
slides/
  _shared/eco701-revealjs.scss   <- the one shared Quarto theme (navy/serif/amber)
  _shared/eco701-theme.css       <- the old Marp theme; delete once every deck is migrated
  00_logistics/                  <- front matter, not one of the 11 numbered topics
  01_definitions-and-key-tools/  <- Topic 1
    deck.qmd                     <- hand-authored Quarto deck. THE deliverable. Never auto-overwritten.
    media/                       <- final images actually used by deck.qmd, meaningfully named
    raw/                         <- mechanical extraction output. Regeneratable. Never hand-edit.
    source.yml                   <- provenance: which pptx, which slide range, confidence, current format
    new_ideas.md                 <- backlog of expansion ideas. Not a plan.
    figs/                        <- notebook-generated candidate figures, staged for review (optional)
```

Retired topics move to `docs/archive/<topic-folder>/` rather than staying
under `slides/`, which the CI build scans wholesale. See Topic 8's archival
note there for the pattern and the reasoning.

**As of 2026-08-27, `docs/archive/` and every `slides/*/raw/` folder are
gitignored** — kept on disk, dropped from the remote ahead of making the repo
public (365 of 469 tracked files, none of it student-facing, and `raw/` is
regeneratable via `tools/`). `docs/archive/HANDOFF-marp.md` is the single
tracked exception, since this file and others link to it. If you need the
archived Topic 8 deck or a topic's raw extraction output, look locally; they
are not in a fresh clone.

Before building or converting a topic, read the actual `source.yml` and
`deck.qmd` in `01_definitions-and-key-tools/` — the fully-migrated example
shows the pattern better than more prose here.

Elsewhere in the repo: `tools/` (extraction + verification scripts),
`notebooks/` (companion Jupyter notebooks), `docs/` (archive, feature demo,
future-topic notes), `archive/` (untracked reference material: the legacy pptx decks under
`archive/slides/legacy/`, past semesters, old notebooks) and `BH/`,
`exams/`, `ps/`, `readings/`, `syllabus/`.

### What reaches the live site

A deck is published only if its own YAML carries `deploy: true`. That single
test gates rendering, the decktape PDF export, the copy of the topic's
`media/`, and the README's deck index — so a deck marked `deploy: false` (or
carrying no `deploy` line) is a draft students never see, and dropping a live
deck back to `false` unpublishes it on the next push. Above it sits
`PUBLISH_SLIDES` in `.github/workflows/deploy-myst.yml`, a master switch that
suppresses every deck at once; it was `'false'` from 2026-08-28 (front page and
reading schedule only, while the decks were revised) and back to `'true'` as of
2026-08-30. Details in
[`course_publishing_workflow.md`](course_publishing_workflow.md) §3.

### Topic status (2026-08-26)

| Topic | Folder | State |
|---|---|---|
| 00 Logistics | `00_logistics/` | Quarto `deck.qmd`, deployed |
| 01 Definitions & key tools | `01_definitions-and-key-tools/` | Quarto `deck.qmd` (513 lines), deployed; **in draft** for enrichment with Bowles/Foley/Halliday Ch. 1 |
| 02 Constrained optimization | `02_constrained-optimization/` | Marp `deck.md` (570 lines, ~52 slides, 23 media), deployed, **awaiting port** |
| 03 Production optimization | `03_production-optimization/` | Marp `deck.md` (351 lines, ~35 slides, 15 media), deployed, **awaiting port** |
| 04–06 | — | Not started; need extraction from legacy pptx |
| 07 General equilibrium | `07_general-equilibrium/` | Not started; folder holds only `new_ideas.md` |
| 08 Essentials of game theory | `docs/archive/08_.../` | **Dissolved** 2026-07-18; lecture slot retired, content absorbed by Topic 1 |
| 08b Game theory II / oligopoly | — | Not started; explicitly optional |
| 09 Externalities & public goods | — | Not started; **no legacy source** — original content, absorbs old Topic 8's N-player material (`slidesI` 32–42) |
| 10 | — | Not started |
| 11 Framing analysis | — | Not started; **no legacy source** — original content |

---

## 4. Recent work

Newest first. Full detail for anything before July 2026 is in
`docs/archive/HANDOFF-marp.md` and the git log.

- **2026-08-26** — Removed the stale `PHASE4-HANDOFF.md`; rewrote this
  document as the single living handoff.
- **2026-08-25** — Deleted two stale branches, `marp-fragments` and
  `topic2-continuous-games` (neither merged, neither live). See §10 for the
  live consequence of the second deletion.
- **2026-07-19** — Quarto migration Phases 0–3, all merged and deployed:
  infrastructure and theme (PR #7), Topic 1 ported (PR #8), Topic 00 ported
  (PR #9), Topic 8 salvaged and archived (PR #10). Also: `--no-sandbox`
  added to decktape's Chromium for the hosted runner; scratch/POC files
  cleaned up and the Quarto feature demo relocated to `docs/`.
- **2026-07-18** — Topic 8's lecture slot dissolved once Topic 1's rework
  around Bowles/Halliday Ch. 1 had absorbed its content. Schelling postcard
  slide + notebook added; the course reframed for its actual audience
  (PR #4).
- **2026-07-16** — marp-cli pinned upgrade 3.0.2 → 4.2.3 (PR #3), since
  retired along with the rest of the Marp toolchain as decks migrate.

---

## 5. Authoring a `deck.qmd`

Two companions to this section, both added 2026-08-27:
[`docs/quarto_workflow.md`](docs/quarto_workflow.md) covers the VS Code editing
loop, the settings that make preview-on-save work, and a fuller feature
reference; [`slides/demos/feature-tour.qmd`](slides/demos/feature-tour.qmd)
demonstrates the same features in a real deck (deliberately *not* named
`deck.qmd`, so CI skips it). The conventions below remain the binding ones.

### Structural conventions

- One `##` heading per slide, always paired with an explicit `---`
  separator — both together, not relying on heading-level slide-breaking
  alone. This mirrors Marp's own one-`---`-per-slide shape, so a port stays
  close to mechanical.
- Marp `<!-- _class: lead/divider/compact -->` becomes a Quarto heading
  attribute: `## Heading {.divider}` / `{.compact}`, styled in
  `eco701-revealjs.scss`'s `scss:rules` block.
- Marp's title/lead slide becomes Quarto's auto-generated title slide, built
  from the `title` / `subtitle` / `author` / `institute` YAML. Don't
  hand-author a replica — not pixel-identical, but close, and far less work.
- Marp `![bg right:NN% wNNN](img)` (split background-image layout) becomes
  `::: {.columns}` / `::: {.column width="X%"}` with a plain `![](img)` in
  one column. Not a mechanical copy — it needs a per-slide judgment call on
  the split — but the visual result is a close match.
- A slide can have **no heading at all**. Pandoc is fine with heading-less
  content between `---` markers, which suits a bold-statement or pull-quote
  slide that isn't really a new topic.
- HTML comments (`<!-- ... -->`) carry over unchanged; Pandoc treats them as
  real comments, same as Marp. Keep using them for provenance and rationale
  notes that shouldn't render.
- Math (`$...$` / `$$...$$`) carries over unchanged. Set
  `html-math-method: katex` explicitly in the YAML — Quarto defaults to
  MathJax otherwise.
- **Bare/standalone images need `{fig-align="center"}`.** Quarto/revealjs
  doesn't center a lone image the way the shared theme centers tables.

### Fragments — the whole reason for the move

- `::: {.incremental}` around a list is roughly Marp's `*`-bullet trick, but
  works regardless of what follows it on the slide.
- `::: {.fragment}` around **any** block is the real upgrade — wrap a
  closing blockquote in its own `.fragment` and it arrives last, after an
  `.incremental` list finishes, which Marp could never do.
- reveal.js ships fragment *styles* beyond plain fade-in:
  `[text]{.fragment .highlight-red}` / `-green` / `-blue` colors a specific
  phrase on click, no custom CSS needed.
- **Don't apply `.incremental` reflexively.** Use it for lists that build a
  sequential argument; leave reference material (readings, grading, agendas)
  plain and static. Staged reveal doesn't help there.

### Tabsets — use sequential slides instead

`.panel-tabset` exports only its default tab to PDF. Tabby.js (the tab
library) hides every non-active panel via an inline style on page load, and
this is not fixable via CSS — a `@media print` override to force all panels
visible was tested and had zero effect, decktape doesn't evaluate print
media here, and the same limitation likely applies to Quarto's own
documented manual-print method, which doesn't touch Tabby's JS state either.

**Standing convention: if "show A, then B, then C" content needs to survive
to a printed PDF, use three sequential slides.** Reserve tabsets, if ever,
for genuinely live-presentation-only content — same category as speaker
notes.

### Executable Python cells

A `.qmd` can mix pre-generated static images (the `figs/` → review →
`media/` workflow in §8) with live executable ` ```{python} ` cells that run
at render time via the `ecopy` Jupyter kernel (`jupyter: ecopy` in the
YAML). Use live cells selectively, where interactivity is itself the
pedagogical point — a hoverable/zoomable Plotly reaction-curve graph, or a
Plotly slider with precomputed frames as the static-export-safe stand-in for
`ipywidgets.interact`. True `ipywidgets` interactivity needs a live kernel
and does not survive to the deployed static site; that pattern stays in the
companion notebooks, as it already does. Default to static images for
everything else.

---

## 6. The extraction pipeline (`tools/`)

Pulling raw content out of the legacy pptx files is completely independent
of which slide engine the output targets — the Quarto move changed nothing
here. [`tools/README.md`](tools/README.md) has the authoritative step order:

```
title_scan.py → extract_topic.py → render_equations.py (if needed)
              → mathpix_ocr.py (if needed)
              → render_diagram.py (if the shape census flagged candidates)
```

Then a human reads the raw output, catches gaps, and hand-writes `deck.qmd`.
That step is not automated and shouldn't be — see §11.

Setup: `mamba install -n ecopy -c conda-forge python-pptx pillow requests
pywin32`. Mathpix credentials live in `.env` at the repo root (gitignored).

---

## 7. Rendering and verification

```
quarto render deck.qmd     # -> deck.html + deck_files/
```

Quarto has **no built-in PDF export for revealjs** — confirmed in its own
docs and an open, unresolved upstream issue. The tool that fills the gap,
and the one CI uses, is **decktape**, a Puppeteer-based headless-Chrome
exporter for reveal.js presentations generally:

```
npx -y decktape reveal --size "1280x720" deck.html deck.pdf
```

`tools/verify_deck.py --topic 02_constrained-optimization` wraps this into
the standard verification loop: render, rasterize every page, flag
edge-bleed heuristically. **0 flagged is not the same as correct** — it has
missed real bugs (a footer collision sitting a few px above the sampled edge
band) that only an eyeball pass caught. Always spot-check a sample of
rendered pages, not just the flag count.

To re-check a single slide after a small fix — much cheaper than re-reading
a whole deck — extract that page as a PNG with PyMuPDF (`fitz`, already in
`ecopy`):

```python
import fitz
doc = fitz.open("deck.pdf")
doc[page_num - 1].get_pixmap(dpi=150).save("check.png")
```

Caveats:

- decktape captures each slide's fully-revealed end state, all fragments
  clicked through. Fine for layout and overflow; useless for confirming
  fragment *order*. Cross-check the compiled HTML for that — grep for
  `data-fragment-index`, `class="notes"` (speaker notes),
  `data-auto-animate` / `data-id="..."`, `data-code-line-numbers="..."`.
  None of these show up in a static PDF capture.
- `pdftoppm`/poppler isn't installed here, so the Read tool's `pages=`
  parameter won't work on these PDFs. Read a small deck whole, or use the
  PyMuPDF single-page trick above.
- The Windows/Google-Drive `deck_files/` file-lock issue (WinError 5) is
  fixed — cleanup is best-effort and non-fatal. A harmless
  `(note: couldn't remove stray ...)` print is expected; ignore it.
- decktape's `--no-sandbox` flag is already in CI. Nothing to redo there.

---

## 8. Code-generated figures (`notebooks/`)

Every topic folder can have `slides/<topic>/figs/` — a sibling of `media/`,
`raw/`, `source.yml` — holding notebook-generated *candidate* figures. It's
git-tracked, so a diff shows exactly what a regenerated figure would change,
but it is not where `deck.qmd` points its `![](...)` references.

Promotion procedure:

1. A notebook cell calls `savefig(fig, "name.png")` → lands in `figs/`.
2. Jonathan reviews it against what's currently live in `media/`. **Never
   swap automatically** — always a deliberate, individual decision.
3. If approved, copy into `media/` under the same filename `deck.qmd`
   already references: `cp figs/x.png media/x.png`.
4. Rebuild and verify before committing.
5. Commit the `media/` swap and, if the notebook changed, the regenerated
   `figs/` file together.

---

## 9. Known gotchas

### `.columns` — read before touching column layout

Quarto's base revealjs theme sets `div.column { display: inline-block;
width: 50% }` with **no logic for more than two columns**, and
`.columns { display: initial }`, which resets `display` to CSS's real
initial value — `inline`, not `block`. Combined with this theme's own
`h2 { display: inline-block }` rule (needed so the amber underline hugs the
heading text), a `.columns` block can end up sharing one inline formatting
context with the heading above it: content crowds the title instead of
starting a new line, and `margin-top` on `.columns` silently does nothing
(vertical margins have no effect on `display: inline` elements — spec
behavior, not a bug). The fix, already applied in `eco701-revealjs.scss`:

```scss
.reveal .columns {
  display: flex;
  margin-top: 0.8em;
}
```

If `.columns` ever looks wrong again, check `display` on `.columns` and on
any `display: inline-block` ancestor or sibling (especially a heading rule)
*before* assuming it's a width or spacing problem. Width and spacing were
both plausible-looking wrong guesses before the real cause was found.

### Content-fidelity gaps (Quarto vs. Marp)

1. **`\underbrace{X}_{\text{label}}` loses its label text** under Quarto's
   KaTeX setup here, unlike Marp's KaTeX. Likely a macro/version
   difference; not chased down. Avoid the construct, or verify the rendered
   slide directly.
2. **Content fit is not free when porting.** Font-size and layout numbers
   don't transfer 1:1 from the Marp theme. Budget a real re-verification
   pass per slide. Add `{.compact}` to a slide's `##` heading when content
   that fit in Marp genuinely overflows at Quarto's base font size — this
   hit Topic 1's PPF slide (four bullets + image + closing blockquote).
   Don't add it reflexively; only when a real render shows overflow.
3. **matplotlib's mathtext parser is stricter than KaTeX.** `\frac14` (no
   braces) works in slide text but throws inside a matplotlib label. Use the
   fully-braced `\frac{1}{4}` in any code-generated figure with embedded
   math.
4. **`.r-stack` needs a blank line between each stacked element.** Adjacent
   `![](...)` lines with no blank line get merged by Pandoc into one `<p>`
   with inline `<img>`s; `.r-stack`'s absolute-positioning CSS never applies
   because there's only one child to stack.

---

## 10. Git workflow and open decisions

### Workflow

Branch fresh off `main`, commit, push, open a PR, watch CI to completion
(`gh run watch <id> --exit-status`), then **pause before merging**. Never
merge, and never push to `main` directly, without Jonathan's explicit
go-ahead in that specific conversation. PRs build via CI but don't deploy;
only a push to `main` deploys.

After merging, verify that the push-triggered deploy run actually appears:

```
gh run list --json event,headSha,status | jq '.[] | select(.event=="push")'
```

An earlier merge in this project produced no push-triggered run at all — a
dropped webhook delivery — which silently left the live site stale. The fix
was an empty commit (`git commit --allow-empty`) to force a fresh push.
Don't assume merged means deployed; check the live site if anything looks
off.

### Open decision: the Topic 2 "Part III" continuous-games material

A branch named `topic2-continuous-games` held a fully-built, previously
reviewed extension to Topic 2: continuous-action games via constrained
optimization (Cournot duopoly plus a continuous-effort fisherman's-dilemma
redux, both with FOC/SOC derivations and new reaction-curve figures). It was
PR'd as **#5**, closed unmerged on Jonathan's instruction with its future
left undecided rather than rejected, then re-confirmed on 2026-07-19 as
something to fold into the Quarto port of Topic 2.

**That fold-in never happened, and the branch was deleted on 2026-08-25** as
part of a stale-branch cleanup. The content is not lost — closed PRs keep
their refs on GitHub:

```
git fetch hunter_eco701 refs/pull/5/head:topic2-part3   # head is 088599e
```

So this needs a fresh decision before Topic 2's port: recover and fold in,
or drop for good. If folding in, treat the branch content as source material
to port to Quarto fragments and columns, not to copy verbatim — its `- `
bullets need the same `::: {.incremental}` treatment as everything else, and
the sequential-slides-not-tabsets convention applies throughout. Its diff
against `deck.md` was a clean 136-line addition when last checked, but real
time has passed; re-check before assuming it's conflict-free.

### Housekeeping

- Local `main` may sit a commit behind the remote — the ToC bot commits
  `[skip ci]` changes directly. Fetch before branching.
- Several untracked files sit in the working tree: `docs/.obsidian/`,
  `kbasu/`, plus seven Google-Drive sync duplicates named `... (1).png` /
  `.md` / `.yml` under `docs/archive/08_essentials-of-game-theory/`. The
  duplicates are sync artifacts and safe to delete.

---

## 11. Source material for future topics

- **Bowles & Halliday (2022), *Microeconomics: Competition, Conflict, and
  Coordination*** — PDF at
  `Y:\E\ebooks\economics\bowleshalliday_final_2022.pdf` (1072 pages).
  Chapter 1, used for Topic 1, is pages 35–85; it's pre-extracted to
  `BH/chapter1_raw_extracted.txt`. The embedded PDF outline's page numbers
  are broken and non-monotonic — search page text directly rather than
  trusting `doc.get_toc()`.
- `BH/BowlesNotes.md` — notes from a prior course iteration, a useful head
  start for later chapters.
- `archive/slides/legacy/Bowles/` (2016 draft) and the rest of `BH/` (2018 PowerPoint
  chapters, syllabus, worksheets) are unrelated leftovers — ignore.

---

## 12. What doesn't scale

The mechanical extraction pipeline is fully scriptable and should just run.
The *redesign* — reorganizing content, writing real titles, verifying payoff
matrices by hand, deciding what to split, merge, or cut, choosing which
lists become `.incremental` and which images become `.columns` splits — is
judgment applied slide by slide. Budget real time for it per topic; don't
try to template it away.

---

## 13. Next steps (priority order)

1. **Finish Topic 01 enrichment** (immediate). Bowles/Foley/Halliday Ch. 1
   (pages 35–85) is pre-extracted to `BH/chapter1_raw_extracted.txt`.
   Brainstorm and hand-author new framing slides, verify Quarto rendering,
   commit and push.
2. **Port Topic 02 to Quarto** (next, and the largest single remaining
   port). Read its `source.yml` first — it documents three sub-chunks
   (Mathematical Preliminaries; Tangency and Lagrange Methods; Applications)
   and several gotchas already solved during the original Marp authoring,
   including Mathcad OLE objects that are plots rather than equations, and a
   duplicate-slide consolidation. None of that needs redoing, just carrying
   forward faithfully. With 152 top-level equations and several dense worked
   examples, expect to need `{.compact}` and `{fig-align="center"}` more
   than once. Settle the PR #5 question in §10 before starting. The
   sub-chunk boundaries are natural check-in points.
3. **Port Topic 03 to Quarto.** Same mechanical treatment, roughly two
   thirds the size, with companion notebooks and figures already in place.
4. **Extract and author Topics 04–07 and 08b.** Run the extraction pipeline
   per `tools/README.md`, hand-author the Quarto decks, build companion
   notebooks. Topics 4 and 5 are the coverage priority.
5. **Write Topics 09 and 11 from scratch** (deferred). No legacy PowerPoint
   source. Topic 9 needs N-player games (absorbing old Topic 8's material
   from `slidesI` 32–42), public goods, externalities, and the commons.
   Topic 11 needs original framing of how micro theory structures empirical
   work.
6. **Retire the Marp toolchain** once Topics 02 and 03 are ported: delete
   `slides/_shared/eco701-theme.css`, and update `README.md`, which still
   describes `slides/` in Marp terms (`deck.md`, `--theme-set`).

Every new or ported topic should render cleanly via `quarto render
deck.qmd`, rasterize without overflow via decktape / `verify_deck.py`, and
get at least one in-browser preview before it goes near `main`.
