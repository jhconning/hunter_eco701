# Quarto workflow and feature reference

Practical companion to [`HANDOFF.md`](../HANDOFF.md). The handoff explains the
project and its conventions; this file explains how to actually drive Quarto
day to day in VS Code, and what the format can do.

Live demonstrations of most of what's below:

- [`slides/demos/feature-tour.qmd`](../slides/demos/feature-tour.qmd) —
  presentation and layout features, plus the Marp→Quarto translations
- [`docs/quarto-feature-demo/quarto_demo.qmd`](quarto-feature-demo/quarto_demo.qmd) —
  callouts, three-column layouts, `.r-stack`, tabsets, Plotly sliders

Written 2026-08-27 against Quarto 1.9.38 and the VS Code Quarto extension
1.136.0.

---

## Part 1 — Workflow

### One-time setup

| Thing | Status here |
|---|---|
| Quarto CLI | Installed at `C:\Program Files\Quarto\bin\quarto`, v1.9.38 |
| VS Code Quarto extension | `quarto.quarto` — installed in **real VS Code**, *not* in Antigravity |
| Python env | `ecopy` (mamba). Decks with code cells need `jupyter: ecopy` in the YAML |
| Node | Only needed for `npx decktape` PDF export |

Antigravity has the Jupyter extensions but no Quarto extension, so slide work
belongs in real VS Code unless you install Quarto there from Open VSX.

**Open `Y:\Hunter\eco701` as the workspace root.** The decks' theme paths
(`../_shared/eco701-revealjs.scss`) and the `tools/` scripts both resolve from
the repo root. Launch Claude Code from there too — the working directory sets
the session's project key, so starting elsewhere splits the history.

### Two settings that matter

```json
"quarto.render.renderOnSave": true,
"quarto.render.previewType": "external"
```

The first is essential. The extension launches `quarto preview` with
`--no-watch-inputs` — it deliberately disables Quarto's own file watcher
because it intends to drive re-renders itself, and it only does that when
`renderOnSave` is on. Without it, the preview prints "Watching files for
changes" and then never updates when you save, which looks like a bug and
isn't. The second is optional: it previews in a real browser rather than the
VS Code webview, which renders more faithfully and can live on a second
monitor.

`editor: render-on-save: true` in a deck's own YAML does the same job
per-file if you'd rather not rely on an editor setting.

### Keybinding conflict, if `Ctrl+Shift+K` misbehaves

The `tianyishi.rmarkdown` extension binds `Ctrl+Shift+K` to an R Markdown
Knit with a broader `when` clause than Quarto's own binding, so it wins and
shells out to `Rscript` — which fails if R isn't on PATH. Disable that
extension, or override in `keybindings.json`:

```json
{ "key": "ctrl+shift+k", "command": "-rmarkdown.rmarkdown-core.Knit" },
{ "key": "ctrl+shift+k", "command": "quarto.preview", "when": "editorLangId == 'quarto'" }
```

### The editing loop

1. Open `deck.qmd`, press `Ctrl+Shift+K` (or Command Palette → *Quarto: Preview*).
2. Edit and save. With `renderOnSave` on, the preview re-renders and holds your
   slide position. Leave it running — you do not press anything again.
3. `Ctrl+Shift+F4` toggles the visual (WYSIWYG) editor. Handy for tables and
   pasted content, but it reformats the markdown on save, so expect diff churn
   if you round-trip a hand-formatted deck.
4. `Ctrl+Enter` runs the code cell under the cursor inline, notebook-style, with
   no full render.

When a change doesn't appear: YAML-header edits sometimes need the preview
restarted, and editing `_shared/eco701-revealjs.scss` may not trip the deck's
watcher — re-save the `.qmd` to force it.

### Render, verify, export

```bash
quarto render slides/01_definitions-and-key-tools/deck.qmd
```

```bash
mamba run -n ecopy python tools/verify_deck.py --topic 01_definitions-and-key-tools
```

```bash
npx -y decktape reveal --size "1280x720" slides/01_definitions-and-key-tools/deck.html deck.pdf
```

`verify_deck.py` renders, rasterizes every page and flags edge-bleed
heuristically. **0 flagged is not the same as correct** — it has missed a real
footer collision that sat just above the sampled band. Spot-check pages by eye.
To re-check one slide cheaply after a small fix:

```python
import fitz
doc = fitz.open("deck.pdf")
doc[page_num - 1].get_pixmap(dpi=150).save("check.png")
```

For a quick look without decktape, open the rendered HTML, append `?print-pdf`
to the URL and print to PDF from the browser. Decktape remains what CI uses and
what the committed artifact should come from.

### Performance

```yaml
execute:
  freeze: auto    # re-run a cell only when its source changes
  cache: true     # jupyter-cache, per cell
```

Without these, every save re-executes every Python cell in the deck.

### Building the MyST site locally (and the `subst` drive trap)

The slide decks are Quarto, but the *site shell* around them (front page, the
reading schedule, the TOC) is MyST -- `myst build --html`, driven by `myst.yml`.

**On this machine that command fails when run through `Y:`**, with five
`file does not exist` errors pointing at files in
`_build/templates/site/myst/book-theme/` that are demonstrably present:

```
myst.yml 'files.0' file does not exist: Y:/.../book-theme/server.js
Cannot use invalid template.yml
```

The cause is not MyST, the repo, or the space in the folder name -- all three
were ruled out by testing the same minimal project in each configuration. `Y:`
is a **`subst` drive** mapped to the mirrored Google Drive folder, and MyST
1.10.1 cannot resolve its own extracted template files through a `subst`
mapping. The identical folder builds cleanly when reached through its real
path. Quarto, latexmk, decktape and Python are all unaffected -- this is a
MyST-only quirk, so the `Y:`-drive convention stands everywhere else.

The fix is to invoke MyST through the mapping's target. This wrapper resolves
it at runtime, so no machine-specific path is stored anywhere -- drop it in
your PowerShell profile:

```powershell
function Invoke-Myst {
    param([Parameter(ValueFromRemainingArguments=$true)]$Args)
    $drive = (Get-Location).Drive.Name
    $line  = subst | Where-Object { $_ -match "^${drive}:" }
    if ($line) {
        $target = ($line -split ' => ')[1]
        $real   = (Get-Location).Path -replace "^${drive}:", $target
    } else { $real = (Get-Location).Path }
    Push-Location $real
    try { & myst @Args } finally { Pop-Location }
}
```

Then `Invoke-Myst build --html` from anywhere in the repo, including from
`Y:`. CI is unaffected either way -- it runs on Ubuntu with no drive mapping,
and remains the build of record.

#### Viewing the site locally

`myst build --html` writes a JavaScript app to `_build/html/` that fetches
`index.json`, `schedule.json` and friends over HTTP. **Double-clicking
`_build/html/index.html` will not work** -- `file://` blocks those requests and
you get a blank or half-rendered page. Two ways to actually look at it:

**Live dev server, for editing.** The MyST equivalent of `quarto preview` --
hot reload, so save `schedule.md` or `README.md` and the browser updates:

```powershell
Invoke-Myst start
```

Serves at `http://localhost:3000`; `Ctrl+C` stops it.

**Serving the built output, to check exactly what CI will publish:**

```powershell
cd "Y:\Hunter\eco701\_build\html"; python -m http.server 8899
```

Then `http://localhost:8899/` for the front page and
`http://localhost:8899/schedule/` for the reading schedule. Note the trailing
slash -- built pages are directories, not `schedule.html`. (This one works from
`Y:` directly: it is Python serving already-built files, so the `subst` problem
does not arise.)

### Git hygiene

Commit `deck.qmd`, `media/`, `source.yml`, `figs/`. Never commit `deck.html`
or `deck_files/` — they're render output and are gitignored. Editing the
shared SCSS changes **every** deck, so re-render all of them before pushing.

### CI facts worth remembering

- The render loop is `find slides -mindepth 2 -maxdepth 2 -type f -name
  "deck.qmd"`. A file named `deck.qmd` two levels under `slides/` **will be
  built and published**; anything else is invisible to it. That's why the
  feature tour is `slides/demos/feature-tour.qmd`.
- The Marp step still globs `slides/` for `.md` files, which is why this
  document lives in `docs/` rather than beside the demo deck.
- `quarto-actions/setup@v2` runs with **no version pin** — CI always installs
  the latest Quarto while you're on 1.9.38. A deck that renders locally can
  break in CI after an upstream release.
- CI pip-installs a hardcoded list: `jupyter ipykernel plotly sympy matplotlib
  numpy pandas`. Import anything else in a live cell and CI fails where local
  succeeded. Extend that line in the same commit as the new import.
- Deploys happen **only** on push to `main`. PRs build but don't deploy. After
  merging, confirm a push-triggered run actually appeared — a dropped webhook
  once left the live site stale.

---

## Part 2 — Feature reference

### Slide structure

One `##` heading per slide, always paired with an explicit `---` separator.
A slide may have no heading at all. HTML comments and `$math$` carry over from
Marp unchanged. Set `html-math-method: katex` explicitly — Quarto defaults to
MathJax.

### Fragments

```markdown
::: {.incremental}
- builds
- one
- at a time
:::

::: {.fragment}
> Any block can be a fragment - this blockquote arrives after the list.
:::
```

- `[phrase]{.fragment .highlight-red}` — `-red` / `-green` / `-blue`, colors a
  phrase on click with no custom CSS
- Other styles: `.fade-up`, `.fade-out`, `.semi-fade-out`, `.grow`, `.shrink`,
  `.strike`
- `::: {.fragment fragment-index=1}` — decouples click order from source order,
  for when the punchline sits at the top of the slide
- `incremental: true` in the YAML makes every list staged, with
  `::: {.nonincremental}` as the opt-out. These decks use the opposite default;
  don't switch mid-course.

Apply `.incremental` where a list builds an argument. Leave reference material
— readings, grading, agendas — static.

### Layout, and the Marp habits it replaces

| Marp | Quarto |
|---|---|
| `![bg right](img)` | `::: {.columns}` + `::: {.column width="40%"}` |
| `![bg](img)` | `## Title {background-image="img"}` |
| `![bg right:40%](img)` | `::: {.column width="40%"}` |
| `![w:400](img)` | `![](img){width="400"}` |
| `![bg opacity:.3](img)` | `{background-image="img" background-opacity="0.3"}` |
| — | `![](img){.absolute top="80" left="40" width="350"}` |

```markdown
::: {.columns}
::: {.column width="55%"}
text
:::

::: {.column width="45%"}
![](media/ppf.png)
:::
:::
```

Marp's `bg` images sit *behind* the text; Quarto columns *reflow* content
beside it. The width split is a judgment call per slide, not a mechanical
translation of `:40%`.

Other slide-level attributes: `background-color`, `background-size`,
`background-position`, `background-video`, `background-iframe`.

Also available: `.r-stack` for stacked, same-position builds — and it needs a
**blank line between each stacked element**, or Pandoc merges them into one
`<p>` and the stacking CSS never applies.

### Overflow

Reach for these in order: `{.smaller}` (built in) → `{.compact}` (this
project's class) → splitting the slide, which is usually the honest answer.
`{.scrollable}` exists but **does not survive the PDF export** — decktape
captures only the visible region, so anything scrolled out of view is missing
from the handout.

### Tabsets — don't

`.panel-tabset` exports only its default tab to PDF. Tabby.js hides
non-active panels via an inline style at load, and no `@media print` override
fixes it. **Standing convention: use sequential slides.** Reserve tabsets, if
ever, for live-only content, same category as speaker notes.

### Executable Python

```` markdown
```{python}
#| echo: false
import plotly.graph_objects as go
fig = go.Figure(...)
fig.update_layout(width=1020, height=380)
fig
```
````

Deck YAML needs `jupyter: ecopy`.

| Cell option | Effect |
|---|---|
| `#\| echo: false` | hide source, show output — the usual choice for slides |
| `#\| include: false` | run it, show nothing — imports and setup |
| `#\| output: false` | show source, suppress output |
| `#\| warning: false`, `message: false` | suppress noise |
| `#\| fig-align: center` | center the figure |
| `#\| code-line-numbers: "\|1-3\|5"` | reveal code in stages |

Set them deck-wide under `execute:` in the YAML and override per cell.

Plotly does not stretch to the slide on its own — set an explicit `width` in
the deck's 1280-wide coordinate space.

### What "interactive" actually means on GitHub Pages

Python runs **at render time**, locally or in CI. The figure ships as JSON plus
`plotly.js`.

- **Works on the static site:** hover, zoom, pan, legend toggle, and any
  slider or dropdown over *precomputed* frames.
- **Does not work:** `ipywidgets.interact`, or anything that must re-run Python
  after page load. That needs a live kernel and belongs in the companion
  notebooks.
- **Pyodide** is the escape hatch — `quarto add r-wasm/quarto-live` for
  in-browser executable Python cells, or `quarto add quarto-ext/shinylive` for
  a client-side Shiny app. Both work on static hosting. Costs: 10–30 MB first
  load, limited package availability (numpy/pandas/matplotlib fine, scipy
  heavy, geopandas painful), and a blank slide in the decktape PDF. Reserve it
  for the one or two slides where students genuinely manipulate the model.

### Presentation-time features

- **Chalkboard** — `chalkboard: true` in the deck YAML. `C` draws over the
  slide, `B` opens a blank board, `Del` clears, `D` downloads annotations as
  JSON. Note `B` was reveal's blackout key.
- **Speaker notes** — `::: {.notes}`, opened with `S`. Never render on the main
  screen, never reach the PDF.
- **Auto-animate** — `## Title {auto-animate="true"}` on two consecutive slides
  with matching `data-id` on an element; reveal morphs between them. Good for
  adding a term to an equation or zooming into a constraint.

Keys: `→`/`Space` advance, `F` fullscreen, `S` speaker view, `O` or `Esc`
overview grid, `.` blackout, `Alt`+click zoom, `?` full help. Type a slide
number then `Enter` to jump.

### Known content gotchas

1. `\underbrace{X}_{\text{label}}` **loses its label** under this KaTeX setup.
   Avoid it, or verify the rendered slide.
2. Content fit doesn't transfer 1:1 from Marp — budget a re-verification pass
   per slide when porting.
3. matplotlib's mathtext is stricter than KaTeX: `\frac14` renders in slide
   text but throws inside a figure label. Write `\frac{1}{4}` in figure code.
4. `.r-stack` elements need blank lines between them.
5. A bare image needs `{fig-align="center"}` — Quarto doesn't center a lone
   image the way the shared theme centers tables.
6. `.columns` had a real `display: inline` bug against this theme's
   `h2 { display: inline-block }`; the fix is already in the SCSS. If column
   layout looks wrong again, check `display` before suspecting widths — see
   `HANDOFF.md` §9.
