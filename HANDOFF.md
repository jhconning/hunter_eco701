# Handoff: Eco 701 slide modernization

Read this first if you're picking up this work in a fresh conversation.
Written 2026-07-13.

## What this project is

Jonathan is modernizing Eco 701 (Master's Microeconomic Theory) from old
PowerPoint slides into Marp markdown slides, organized around the 11-topic
course sequence in [`syllabus/IDEAS.md`](syllabus/IDEAS.md). The end goal is
a live course site (GitHub Pages) with slides, notes, and problem sets all
built from the same markdown source.

**This is NOT a fresh project** — a real repo (`jhconning/hunter_eco701`)
already existed with a working GitHub Pages deploy pipeline and one topic
built (using a "Neobeam" Marp theme) before this reorganization started. If
you're exploring this repo cold, don't assume the `git log` before
2026-07-13 reflects this conversation's work — it doesn't.

## Where everything is

- **Repo root:** `Y:\Hunter\Eco 701\Eco701\` (note: no space — do not confuse
  with `Y:\Hunter\Eco 701\past\` or the top-level `Y:\Hunter\Eco 701\slides\`,
  which are unrelated old folders that happen to be nearby)
- **GitHub remote:** `jhconning/hunter_eco701`, remote name `hunter_eco701`
  (not `origin`)
- **Live site:** https://jhconning.github.io/hunter_eco701/ — deploys ONLY on
  push to `main`. Never push to `main` directly without Jonathan's explicit
  go-ahead; work on a branch and open a PR (PRs build via CI but don't
  deploy — see the CI section below).
- **Legacy source pptx files:** `legacy/slides/E701_F18 _slidesI.pptx` (337
  slides), `_slidesII.pptx` (258 slides), `_slidesIIb.pptx` (224 slides).
  This folder is gitignored — it's reference material, not tracked.
- **Current branch as of this handoff:** `topic-reorg`, open as
  [PR #1](https://github.com/jhconning/hunter_eco701/pull/1), CI green, not
  yet merged. Check `git log`/`gh pr view 1` to see if it's since been
  merged or changed.

## Architecture

Each topic is a folder under `slides/`, numbered to match `IDEAS.md`:

```
slides/
  _shared/eco701-theme.css       <- the one shared Marp theme (navy/serif/amber)
  00_logistics/                   <- front-matter, not one of the 11 numbered topics
  01_definitions-and-key-tools/   <- IDEAS.md Topic 1
  08_essentials-of-game-theory/   <- IDEAS.md Topic 8
    deck.md                       <- hand-authored Marp deck. THE deliverable. Never auto-overwritten.
    media/                        <- final images actually used in deck.md, meaningfully named
    raw/                          <- mechanical extraction output. Regeneratable. Never hand-edit.
      extracted.txt                  (NOT .md - marp-cli would otherwise try to build it as a deck)
      tables.json
      shape_census.json
      mathpix.json
      media/eq/, media/pic/, media/slide_png/
    source.yml                    <- provenance: which pptx, which slide range, confidence level
```

Read the actual `source.yml` and `deck.md` in `01_definitions-and-key-tools/`
and `08_essentials-of-game-theory/` for concrete examples before building a
new topic — they show the pattern better than more prose here.

## The conversion pipeline (`tools/`)

See [`tools/README.md`](tools/README.md) for the authoritative step order.
Summary: `title_scan.py` (planning, optional) → `extract_topic.py` (text/
tables/pictures, free/fast) → `render_equations.py` (PowerPoint COM, only if
there are OLE equations) → `mathpix_ocr.py` (paid API, only after you know
the equation count). Then a human (you) reads the raw output, catches gaps,
and hand-writes `deck.md` — that step is NOT automated and shouldn't be;
see "What doesn't scale" below.

Setup: `mamba install -n ecopy -c conda-forge python-pptx pillow requests
pywin32`. Mathpix credentials live in `.env` at the repo root
(`MATHPIX_APP_ID`, `MATHPIX_APP_KEY`) — gitignored, already populated as of
this handoff.

## What to do next

1. **Get Jonathan's answers to the open questions in
   [`TOPIC_PLAN.md`](TOPIC_PLAN.md)** before converting more topics — the
   slidesII/IIb overlap especially, since it affects which file to treat as
   the source for ~5 of the remaining 9 topics.
2. Topic 2 (Constrained Optimization, `slidesI` 43-102) has the highest
   confidence mapping and is a clean contiguous range — a reasonable next
   pick if Jonathan wants to keep moving before all TOPIC_PLAN.md questions
   are resolved.
3. For each new topic: run the pipeline, review the raw output *including
   the shape census* (don't skip this — it's what caught 3 missed tables
   during the pilot), redesign into `deck.md` with real pedagogical judgment
   (split overflowing slides, merge redundant ones, write real titles — see
   the git history of `08_essentials-of-game-theory/deck.md`'s predecessor
   pilot for what "good" looks like), verify locally with `marp` CLI +
   `pdftoppm` rasterization (see "Verifying a build" below), then commit to
   a branch and open a PR.

## Gotchas discovered the hard way (don't rediscover these)

- **Pandoc cannot read `.pptx`** — only writes it. Don't reach for it as a
  pptx extraction tool.
- **python-pptx's `shape.has_text_frame`/image-blip walk silently skips
  native PowerPoint tables** (`shape.has_table`) unless you check for them
  explicitly. This is why `extract_topic.py` handles tables as a distinct
  case and prints a shape-type census every run — always look at that
  census before trusting the extraction is complete.
- **Legacy equations are MathType/Equation Editor OLE objects
  (`Equation.DSMT4`), not modern OOXML math** — no free LaTeX conversion
  exists. The working solution is rendering via PowerPoint COM automation
  (crisp, since it's PowerPoint's own renderer) then Mathpix OCR — both
  came back near-perfect in testing. Don't waste time on WMF/EMF decoding;
  ImageMagick's WMF support was unreliable on this machine.
- **PowerPoint COM automation safety:** `win32com.client.Dispatch` attaches
  to an *already-running* PowerPoint instance rather than starting a new
  one. Always check with `GetActiveObject` first and only call
  `app.Quit()` if you started it yourself — see `render_equations.py`'s
  safety check. Getting this wrong could close Jonathan's other unsaved
  PowerPoint work.
- **marp-cli's directory-mode build does not copy referenced local images
  into its output** — it only transforms `.md` → `.html`/`.pdf`, leaving
  relative `<img>` paths that break once deployed unless something
  separately copies the media folders. The CI workflow's "Copy topic media
  folders to build" step handles this generically for any topic folder.
- **marp-cli will try to build *any* `.md` file it finds under `slides/`**,
  including non-deck files. This is why raw extraction text is saved as
  `.txt`, not `.md`.
- **The CI's `environment: github-pages` binding was on the whole
  build-and-deploy job**, which caused GitHub's environment protection
  rules to reject the entire job (not just deploy steps) on every PR —
  meaning PRs could never actually validate a build before this handoff's
  fix split it into separate `build` (unrestricted) and `deploy`
  (environment-gated, push-to-main only) jobs. If you see PR CI runs
  failing instantly (~3s) with an environment-protection annotation, this
  is the failure mode to check for.
- **Local marp-cli here is v4.2.3; CI's Docker image pins v3.0.2.** Don't
  fully trust a local build as proof the CI build will pass. Rather than
  install Docker (daemon wasn't running when needed), `npx --yes
  @marp-team/marp-cli@3.0.2 ...` runs the *exact* pinned version locally in
  seconds — use this to verify against the real toolchain instead of the
  newer globally-installed `marp` command.
- **Raw HTML in deck.md is NOT rendered by marp-core v3.9.1 (the version
  behind CI's pinned v3.0.2) unless `html: true` is set in frontmatter** —
  without it, literal `<div>`/`<p>`/`<br>` tags print as escaped visible
  text instead of becoming real elements. This bit us for real: a
  `<div class="people-row"><img ...>` block for a bio-aside slide rendered
  as broken text under the real CI toolchain despite looking fine locally
  on v4.2.3 (which is more lenient). **Prefer Marp's native syntax over raw
  HTML wherever one exists** — `![bg right w:500](path)` for background/
  layout images instead of `<img>` + flexbox, `> text` (blockquote) instead
  of `<p class="...">` for styled asides, plain paragraphs instead of
  `<br>` for spacing. Marp's image directives (`bg`, `left`/`right`,
  `vertical`, `w:`/`h:`) are core parser features, not raw HTML, so they
  don't have this problem. Only reach for `html: true` if there's truly no
  native equivalent.

## What doesn't scale (don't try to automate this part)

The mechanical extraction pipeline is fully scriptable and should just run.
The *redesign* — reorganizing content, writing real titles, catching that
slide 14 was actually a different game than slides 12/15, verifying payoff
matrices by hand, deciding what to split/merge/cut — is judgment applied
slide-by-slide. Budget real time for this per topic; don't try to template
it away.
