# ECO 701: Quarto → GitHub Pages → Brightspace publishing workflow

> **Philosophy:** keep 100% of course content (slides, notes, notebooks, problem
> sets, syllabus) in this Git-versioned repo, publish the student-facing parts
> automatically to GitHub Pages, and use **Brightspace** strictly as the
> administrative portal — roster, gradebook, quizzes, dropboxes, announcements.

Adapted 2026-08-27 from a generic ECO 100 draft to the setup that actually
exists in this repo. Companion documents: [`HANDOFF.md`](HANDOFF.md) for the
project and its conventions, [`docs/quarto_workflow.md`](docs/quarto_workflow.md)
for the day-to-day Quarto/VS Code loop.

**The publishing half of this is already built and running.** The sections
below describe it as it is, not as something to construct.

---

## 1. Architecture as it actually stands

```
 ┌──────────────────────────────────────────────────────────────────────┐
 │ LOCAL — Y:\Hunter\eco701\  (git repo, remote "hunter_eco701")         │
 │   slides/<NN_topic>/deck.qmd        Quarto revealjs decks             │
 │   slides/_shared/*.scss             one shared theme                  │
 │   slides/demos/feature-tour.qmd     authoring reference (not deployed)│
 │   notebooks/*.ipynb                 companion Jupyter notebooks       │
 │   tools/*.py                        extraction + verify_deck.py       │
 │   README.md + myst.yml              the site's front page and TOC     │
 │   exams/  ps/  grades/  archive/    NOT published — see §8            │
 └───────────────────────────────┬──────────────────────────────────────┘
                                 │  branch → PR → merge to main
                                 ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │ GITHUB ACTIONS — .github/workflows/deploy-myst.yml                    │
 │   1. regenerate README's "Deployed Presentations" index               │
 │      (lists every slides file carrying `deploy: true`)                │
 │   2. myst build --html            → site shell from README + myst.yml │
 │   3. copy slides/<topic>/media/   → build output                      │
 │   4. quarto render each slides/*/deck.qmd  (in place)                 │
 │   5. decktape each → deck.pdf                                         │
 │   6. marp-cli for the not-yet-ported Marp decks (02, 03)              │
 │   7. upload _build/html as the Pages artifact                         │
 └───────────────────────────────┬──────────────────────────────────────┘
                                 │  deploys ONLY on push to main
                                 ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │ GITHUB PAGES — https://jhconning.github.io/hunter_eco701/             │
 │   /slides/<NN_topic>/deck.html    live deck (chalkboard, Plotly)      │
 │   /slides/<NN_topic>/deck.pdf     handout export                      │
 │   Publicly reachable even though the SOURCE REPO IS PRIVATE           │
 └───────────────────────────────┬──────────────────────────────────────┘
                                 │  plain web links, configured once
                                 ▼
 ┌──────────────────────────────────────────────────────────────────────┐
 │ CUNY BRIGHTSPACE                                                      │
 │   Content: one link per week (or one hub link) → Pages URLs           │
 │   Quizzes, dropboxes, gradebook, announcements, official roster       │
 └──────────────────────────────────────────────────────────────────────┘
```

Verified live as of 2026-08-27 (all HTTP 200):

| Deck | HTML | PDF |
|---|---|---|
| 00 Logistics | `/slides/00_logistics/deck.html` | `/slides/00_logistics/deck.pdf` |
| 01 Definitions & Key Tools | `/slides/01_definitions-and-key-tools/deck.html` | …`/deck.pdf` |
| 02 Constrained Optimization | `/slides/02_constrained-optimization/deck.html` | …`/deck.pdf` |
| 03 Production Optimization | `/slides/03_production-optimization/deck.html` | …`/deck.pdf` |

All prefixed with `https://jhconning.github.io/hunter_eco701`.

---

## 2. Three things not to do

These are the places where the generic workflow would actively break this repo.

**Do not run `quarto publish gh-pages`.** It renders locally and force-pushes to
a `gh-pages` branch. This repo publishes through GitHub Actions with
`actions/deploy-pages` instead, and the stale `gh-pages` branch on the remote
(last touched 2026-05-04) is a leftover from an earlier setup. Running that
command would fight the Actions pipeline and could publish a half-built site
from your laptop. Publishing here means: **merge to `main`.**

**Do not add a root `_quarto.yml` website project** without deciding to migrate
the whole site. Right now the site shell is built by **MyST** (`myst.yml`,
`myst build --html`) and the decks are rendered *individually, in place*, so
relative `media/` paths resolve against each deck's own folder. A root
`_quarto.yml` with `project: type: website` changes what `quarto render` does
to every deck and where output lands — it would break both the CI loop and the
local `verify_deck.py` loop. Migrating MyST → Quarto website is a reasonable
future project; it is not a config file you drop in.

**Do not rename or renumber topic folders mid-semester.** Every Brightspace link
is a URL into `/slides/<folder-name>/deck.html`. Rename the folder and every
link a student clicks 404s, silently, with no redirect. This repo has already
dissolved one topic (08) and reserved 08b — so decide numbering *before* a link
goes into Brightspace, and if a rename is truly unavoidable mid-term, leave a
redirect stub at the old path (§7).

---

## 3. Publishing a deck: the actual checklist

1. Branch off `main` — never commit to `main` directly.
2. Create or edit `slides/<NN_topic>/deck.qmd`. It must be named exactly
   `deck.qmd` and sit exactly two levels under `slides/` — CI's render loop is
   `find slides -mindepth 2 -maxdepth 2 -type f -name "deck.qmd"`. Anything else
   is invisible to the build (which is why `slides/demos/feature-tour.qmd` never
   deploys).
3. In its YAML, include the front-matter keys the site index reads:
   ```yaml
   description: "ECO 701 Topic N: Human-readable title"
   deploy: true
   ```
   The README's "Deployed Presentations" list is regenerated on every push from
   files carrying `deploy: true`, using `description` as the link text. A deck
   without it still renders and deploys — it just never appears in the index.
   Use `deploy: false` to be explicit about anything that should stay unlisted.
4. Put images in `slides/<NN_topic>/media/` and reference them relatively.
   CI mirrors that folder into the build; nested `raw/media/` is deliberately
   excluded.
5. Verify locally:
   ```bash
   mamba run -n ecopy python tools/verify_deck.py --topic NN_topic
   ```
   0 flags is not the same as correct — spot-check pages by eye.
6. Push, open a PR, watch CI (`gh run watch <id> --exit-status`). PRs build but
   do not deploy.
7. Merge only with explicit go-ahead. Then confirm a **push-triggered** run
   actually fired:
   ```bash
   gh run list --json event,headSha,status | jq '.[] | select(.event=="push")'
   ```
   A dropped webhook once left the live site stale after a merge; the fix was
   `git commit --allow-empty` to force a fresh push.

---

## 4. Deck YAML for this course

The generic draft's sample used `theme: default` and `math: mathjax`. Use the
project's own header instead — shared theme, KaTeX, chalkboard on:

```yaml
---
title: "Microeconomic Theory"
subtitle: "Topic N: ..."
author: "Jonathan Conning"
institute: "Hunter College, Dept. of Economics"
description: "ECO 701 Topic N: ..."
deploy: true
format:
  revealjs:
    theme: [default, ../_shared/eco701-revealjs.scss]
    slide-number: true
    footer: "Eco 701 - Micro Theory"
    html-math-method: katex
    chalkboard: true
    width: 1280
    height: 720
jupyter: ecopy          # only if the deck has executable cells
execute:
  freeze: auto
---
```

`html-math-method: katex` is deliberate — Quarto defaults to MathJax, and this
theme's sizing is tuned against KaTeX. Authoring conventions (fragments,
columns, overflow classes, the tabsets ban) are in
[`docs/quarto_workflow.md`](docs/quarto_workflow.md); the live demonstration is
`slides/demos/feature-tour.qmd`.

---

## 5. The course hub page (recommended)

Option B from the original draft — one page students bookmark — is the right
default for a 13-lecture Master's course, and it costs one file.

Because the site shell is MyST, not Quarto, the hub is a plain Markdown file
added to the MyST TOC rather than a `schedule.qmd`:

1. Create `schedule.md` at the repo root.
2. Register it in `myst.yml`:
   ```yaml
   project:
     toc:
       - file: README.md
       - file: schedule.md
   ```
3. Give it one row per lecture:

   ```markdown
   | Week | Topic | Slides | PDF | Notebook | Reading | Due |
   |------|-------|--------|-----|----------|---------|-----|
   | 1 | Definitions & key tools | [live](slides/01_definitions-and-key-tools/deck.html) | [pdf](slides/01_definitions-and-key-tools/deck.pdf) | [Schelling](notebooks/topic01_schelling_segregation.html) | BFH Ch. 1 | — |
   ```

Then Brightspace needs exactly **one** link, pointing at
`https://jhconning.github.io/hunter_eco701/schedule.html`, and everything else
is maintained here.

---

## 6. Brightspace integration

### Option A — a link per week

**Content** → the week's module → **Upload/Create** → **Create a Link**:

- **Title:** `Topic 1 — Definitions and Key Tools (slides)`
- **URL:** the Pages `deck.html` URL

**Check "Open as External Resource."** This is the opposite of the generic
draft's advice, and the reason matters: a reveal.js deck embedded in
Brightspace's content iframe loses keyboard control (arrows, `F`, `S`, and the
chalkboard's `C`/`B` go to Brightspace, not the deck), cannot go properly
fullscreen, and renders in a letterboxed panel. Slides belong in their own tab.
Static pages — a syllabus, the schedule hub — embed fine.

Add a second link to the `deck.pdf` beside each deck. Students want something
printable and annotatable, and it is the accessible fallback if a browser
struggles with the live deck.

### Option B — one hub link

A single prominent **"Course Materials & Schedule"** link on the Brightspace
homepage pointing at `schedule.html` (§5). Students bookmark it; Brightspace is
then used only for graded work and grades. Lowest maintenance of any option,
and the one to prefer unless the department requires weekly modules.

### Either way

Configure links **once**. Every subsequent content change propagates on merge to
`main` with no LMS editing. Announcements, due dates, and anything grade-bearing
stay in Brightspace — one authoritative place for deadlines avoids the classic
failure where the site and the LMS disagree about when something is due.

---

## 7. Stable URLs

Brightspace links are only as good as the paths behind them.

- Fix topic folder names **before** the first link is published, and treat them
  as permanent for the semester.
- If a rename is unavoidable, leave a stub at the old path so nothing 404s:
  ```html
  <!-- slides/08_old-name/index.html -->
  <meta http-equiv="refresh" content="0; url=../08b_new-name/deck.html">
  ```
- Prefer adding a *new* numbered folder over renumbering existing ones.
- Consider a CI link-check step (e.g. `lychee`) over the built `_build/html` so
  a broken internal link fails the PR rather than a student's click.

---

## 8. What must never reach the published site

**The repo is private; the Pages site is public.** Those are independent
settings, and the site is reachable by anyone with the URL — no CUNY login, no
GitHub account. The publication boundary is `_build/html`: anything the workflow
copies there is world-readable.

Currently gitignored (never committed, therefore never published):
`archive/`, `grades/`, `exams/`, `ps/`, `readings/`, `BH/`, `canvas/`,
`kbasu/`, `syllabus/IDEAS.md`.

**Gap worth closing:** `exams/`, `ps/`, and `readings/` are empty scaffolding
today, tracked by nothing — but they are *not* in `.gitignore`. The moment real
exam keys, problem-set solutions, or copyrighted PDFs land there, a routine
`git add -A` commits them, and a later build step could publish them. Two safe
patterns:

```gitignore
# solutions and assessment material - never publish
exams/
ps/solutions/
readings/
```

or keep a `private/` directory, gitignored wholesale, for anything with an
answer key in it. Either way, decide before the first exam is written, not
after.

Distribute solutions and exams through Brightspace's dropbox/quiz tools, which
are behind the CUNY login, or hand them out in class.

---

## 9. Assessments in Brightspace

Question banks are worth keeping here in Markdown under version control, then
exporting — the same single-source logic as the slides.

- Brightspace imports question libraries as **CSV** (simple multiple choice,
  true/false, short answer) or as a **QTI package** (full fidelity, all question
  types). CSV is far easier to generate from Markdown; QTI is what you need for
  anything with images or complex math.
- Verify the exact CSV column layout against *your* Brightspace version before
  investing in a converter — D2L has changed it between releases, and CUNY may
  be a release behind. Import one hand-made row first.
- Math in Brightspace quizzes is a genuine constraint. It has its own equation
  editor and does not render KaTeX from imported text. For a theory course, that
  argues for keeping graded problem sets as dropbox submissions (students upload
  a PDF) and reserving Brightspace quizzes for concept checks.
- A converter script belongs in `tools/`, alongside the extraction pipeline,
  with its output gitignored.

---

## 10. Getting notebooks to students

This needs a decision — currently the notebooks are **not** published anywhere
students can reach.

`notebooks/*.ipynb` are tracked in the repo, but the repo is private, so a
GitHub blob link fails for students, and the CI workflow does not copy notebooks
into `_build/html`. Three options, cheapest first:

1. **Render to HTML in CI** — add a step that runs
   `quarto render notebooks/*.ipynb --to html` into `_build/html/notebooks/`.
   Read-only, zero infrastructure, works for anything that is "read this worked
   example."
2. **Colab** — needs a *public* mirror repo, since Colab cannot read a private
   one. Good if you want students editing and running code with no local setup.
3. **JupyterLite** — a full in-browser Python environment published as part of
   the static site. No server, no accounts, students can edit and run. Heaviest
   first load, and package availability is limited, but it keeps everything on
   your own site and works for `ipywidgets.interact`-style content that cannot
   survive in a slide.

Option 1 now, option 3 when a notebook genuinely needs interactivity.

---

## 11. Semester hygiene

- **Tag each offering:** `git tag fall2026 && git push hunter_eco701 fall2026`.
  A tag makes any past semester's exact materials recoverable, which matters
  when a student disputes a grade or you want to see what you actually covered.
- Keep `TOPIC_PLAN.md` current — it is the public-facing record of the topic
  sequence and every structural decision (`syllabus/IDEAS.md` is private).
- At semester end, add a dated entry to `HANDOFF.md` §4 so the next pickup knows
  what changed.
- Retired material goes to `docs/archive/<topic>/`, out of `slides/`, which CI
  scans wholesale.

---

## 12. Working with an AI assistant on this repo

Antigravity is the daily driver but has **no Quarto extension** — slide work
belongs in real VS Code (or install Quarto there from Open VSX). Prompts that
match this repo's actual tooling:

| Task | Prompt |
|---|---|
| New deck | *"Create `slides/04_<topic>/deck.qmd` using the ECO 701 YAML header and shared theme, with `description` and `deploy: true` set."* |
| Port a Marp deck | *"Port `slides/02_constrained-optimization/deck.md` to Quarto per HANDOFF.md §5 — `---` separators, class syntax, column layouts — then verify with `tools/verify_deck.py`."* |
| Extract from legacy pptx | *"Run the extraction pipeline in `tools/README.md` for Topic 5 against `archive/slides/legacy/E701_F18 _slidesIIb.pptx`."* |
| Build the hub | *"Generate `schedule.md` from `TOPIC_PLAN.md` with the week/topic/slides/PDF/notebook table, and register it in `myst.yml`."* |
| Check a deck | *"Render Topic 1, decktape it, and rasterize pages 5–10 so I can eyeball the fit."* |
| Brightspace CSV | *"Convert the questions in `ps/topic4.md` to a Brightspace question-import CSV in `tools/out/` — do not commit the output."* |

---

## 13. Quick reference

```bash
quarto preview slides/01_definitions-and-key-tools/deck.qmd
```

```bash
quarto render slides/01_definitions-and-key-tools/deck.qmd
```

```bash
mamba run -n ecopy python tools/verify_deck.py --topic 01_definitions-and-key-tools
```

```bash
npx -y decktape reveal --size "1280x720" slides/01_definitions-and-key-tools/deck.html deck.pdf
```

Single self-contained file for a classroom with no internet:

```bash
quarto render slides/01_definitions-and-key-tools/deck.qmd -M embed-resources:true
```

---

## 14. Open decisions

1. **`exams/` and `ps/` gitignore policy** (§8) — settle before the first exam
   exists.
2. **Notebook delivery** (§10) — render-to-HTML in CI is the low-cost default.
3. **Hub page vs. weekly links** (§5, §6) — hub recommended; weekly modules only
   if the department expects them.
4. **MyST or Quarto for the site shell** — MyST works and is not urgent to
   change, but running one system rather than two would simplify CI. A real
   migration, not a config tweak.
5. **The stale `gh-pages` branch** — from 2026-05-04, unused by the current
   Actions pipeline. Confirm nothing points at it, then delete.
6. **Retire the Marp path** once Topics 02–03 are ported: drop the two marp-cli
   steps from the workflow, delete `slides/_shared/eco701-theme.css`, and update
   `README.md`, which still describes `slides/` in Marp terms.
