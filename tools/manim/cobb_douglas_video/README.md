# Eco 701 video series — Episode 1: The Cobb-Douglas Production Function

3Blue1Brown-style Manim video for the producer-theory unit of Eco 701
(Masters micro, Hunter College CUNY). Built 2026-07-12 with Claude (Fable).

**Deliverable:** `renders\episode1_cobb_douglas_1080p30.mp4` — 7:48, 1080p30,
~21 MB, silent (paced for a voiceover recorded from `NARRATION.md`).
Full design history and as-built notes live in `PLAN.md`; this README is the
day-to-day guide: what the code is, how to render, and how to make edits.

---

## 1. The video at a glance

| Time | Scene file → class | Content |
|---|---|---|
| 0:00–0:17 | `s0_intro.py` → `Intro` | Series branding card + episode title |
| 0:17–1:21 | `s1_warmup.py` → `Warmup1D` | Univariate warm-up: π(q)=10q−10−q², live tangent flattens at the top (FOC), minimum counterexample, SOC |
| 1:21–2:41 | `s2_expression.py` → `Expression` | q = AK^αL^β symbol by symbol; homogeneity F(tK,tL)=t^{α+β}F(K,L); DRS/CRS/IRS number line; specialize to q=√(KL) |
| 2:41–4:32 | `s34_surface.py` → `SurfaceToIsoquants` | One continuous 3D scene: surface reveal + orbit → fixed-K slice (diminishing MP_L) → rising planes carve isoquants, projected to the floor → camera flattens overhead into the 2D isoquant map |
| 4:32–5:51 | `s5_mrts.py` → `MRTS` | Total differentiation → MRTS card → closed form (β/α)(K/L) → dot slides along q̄=4, readout falls 4.00→0.25 (diminishing MRTS) |
| 5:51–7:13 | `s6_homothetic.py` → `Homothetic` | Ray K=mL crosses every isoquant at the same slope (parallel stubs, ray sweeps); degree-0 proof; homothetic definition; expansion-path payoff + Lagrange tease |
| 7:13–7:48 | `s7_outro.py` → `Outro` | Five-line recap + closing branding card |

Running example everywhere: **A=1, α=β=½, q=√(KL)**, domain K,L ∈ [0.3, 9].
Axis convention (locked): **L on x, K on y, q on z** — the flattened 3D floor
*is* the standard 2D isoquant diagram.

## 2. How the code is organized

```
params.py        the economics: A, ALPHA, BETA, domain, QBARS, and closed
                 forms F(K,L), K_of_L(L,q̄), dK_dL, MRTS — single source of
                 truth; scenes never hard-code these
theme.py         the look and the shared machinery (see below)
s0…s7*.py        one file per beat; each holds ONE Scene class whose
                 construct() reads top-to-bottom in storyboard order
manim.cfg        makes bare `manim <file> <Scene>` render fast 480p15
smoke_test.py    toolchain check (LaTeX→dvisvgm, pango text, 3D, encoding)
math_check.py    sympy gate — re-derives all 19 on-screen formulas
qa_frames.py     dumps every Nth frame of an mp4 to PNGs (visual QA)
stitch.py        ffmpeg-concats the 7 scene mp4s into the episode
render.ps1       renders everything + stitches (-Final for 1080p30)
renders\         stitched deliverables — episode1_cobb_douglas_1080p30.mp4
                 (the final cut) and episode1_cobb_douglas_preview.mp4
                 (480p15, from a bare `.\render.ps1` — a fast scrub copy,
                 safe to delete/regenerate anytime)
media\           manim's output tree — not present until you render;
                 safe to delete anytime, fully regenerated
```

What `theme.py` provides (reused by every scene, and by future episodes):

- **Palette & conventions** — labor L blue, capital K green, output q yellow,
  tangents red, α teal, β purple; dark background `#171717`.
- **`colorize(MathTex(...))`** — applies those colors via
  `substrings_to_isolate`. ⚠ Read its docstring before writing new formulas:
  isolation breaks any LaTeX command containing the letters q/A/K/L, so no
  `\quad`/`\qquad`/`\sqrt` in colorized strings, and accents/scripts need
  braces — `\bar{q}`, `F_{K}`, never `\bar q`, `F_K`. (Violations surface as
  a misleading "dvisvgm"/"latex error converting to dvi" failure.)
- **`definition_card(title, formula, plain)`** — the rounded box used for
  every formal definition (isoquant, MRTS, homothetic).
- **Live-tangent machinery** — `moving_dot`, `moving_tangent`,
  `live_readout`: ValueTracker-driven dot + tangent + numeric readout, used
  in the warm-up, the MRTS slide, and reusable for any future curve-riding.
- **`PACE` + `PacedScene`/`PacedThreeDScene`** — every scene inherits from
  these; `wait()` durations are multiplied by `PACE` (currently 4.0) while
  `play()` motion is untouched. Retiming the whole episode = one number.
  (The 3D scene's ambient-rotation *rate* was tuned for stretched waits — if
  you change PACE a lot, revisit `rate=-0.016` in s34.)
- **`branding_card(...)` / `example_badge()`** — series branding and the
  "running example" chip.

**Matched-cut geometry (important):** the video cuts from the 3D scene's
overhead view (S34) to freshly built 2D scenes (S5, then S6) with no visible
seam. That works because S5/S6 rebuild the map with exactly
`Axes(x_length=y_length=5.6)` shifted so the origin sits at screen
`(-2.81, -2.76)` — the flattened 3D floor at zoom 0.8. If you move or resize
the map in ONE of these three scenes, make the same change in all three.

## 3. Environment & rendering

Everything runs in the `ecopy` conda env (manim 0.20.1, ffmpeg, sympy;
LaTeX = TinyTeX with dvisvgm). In an interactive shell:

```powershell
mamba activate ecopy
cd "Y:\Hunter\eco701\tools\manim\cobb_douglas_video"
```

(Non-interactive shells don't have mamba on PATH — use
`& "$env:USERPROFILE\miniforge3\condabin\mamba.bat" run -n ecopy <cmd>`.)

| Task | Command | Time |
|---|---|---|
| Preview one scene (480p15, auto-open) | `manim -p s5_mrts.py MRTS` | 30–90 s |
| Check ONE moment as a PNG | `manim -p -s -n 0,5 s5_mrts.py MRTS` | seconds |
| Full preview episode + stitch | `.\render.ps1` | ~10 min |
| Final 1080p30 episode + stitch | `.\render.ps1 -Final` | ~25 min |
| Re-stitch after re-rendering one scene | `python stitch.py <media_dir> 1080p30 renders\episode1_cobb_douglas_1080p30.mp4` | seconds |
| Verify the math | `python math_check.py` | seconds |
| Dump frames for close inspection | `python qa_frames.py <video.mp4> <out_dir> <every_n>` | seconds |

`-s` renders only the last frame; `-n a,b` runs only animation indices a…b
(each `self.play` *and* `self.wait` is one index) — together they give you a
single-frame layout check of any moment without rendering video.
`manim.cfg` defaults bare runs to fast 480p15; `render.ps1 -Final` overrides
with `--resolution 1920,1080 --fps 30`.

## 4. Editing workflow (moving things around)

The loop for notes like *"at 0:21 the equation is blocked by the title —
move it down a bit"*:

1. **Timestamp → file** with the table in §1 (0:21 → `s1_warmup.py`).
2. **Find the element** — variables are semantic: `title`, `formula`, `card`,
   `readout`, `inset`, `lvl_labels`… Its position is one chained call.
3. **Nudge it** with the standard idioms:
   ```python
   formula.to_corner(UR, buff=0.6).shift(DOWN * 0.85)   # the 0:21 fix
   card.move_to(np.array([4.15, 2.0, 0]))               # absolute placement
   note.next_to(card, DOWN, buff=0.22)                  # relative (rides along)
   ```
   Screen coordinates: x ∈ [−7.1, 7.1], y ∈ [−4, 4], origin at center.
   Elements placed with `next_to` follow their anchor automatically.
4. **Check just that moment**: `manim -p -s -n 0,6 s1_warmup.py Warmup1D`
   (bisect on the second number until the PNG shows your moment).
5. **Live nudging (optional, 2D scenes):** insert `self.interactive_embed()`
   right after the moment in `construct()`, run
   `manim --renderer=opengl -p s1_warmup.py Warmup1D`, and type
   `formula.shift(DOWN*0.3)` in the IPython prompt to see it move in real
   time; copy the numbers back into the file and remove the embed line.
   (The OpenGL renderer is quirky with the 3D scene's fixed-in-frame HUD —
   for `s34_surface.py` stick to step 4.)
6. **Rebuild the deliverable**: re-render only the scenes you touched at
   final quality, then re-stitch (or just run `.\render.ps1 -Final`).

VS Code: open this folder, set the interpreter to `ecopy`, run the commands
in the integrated terminal. The **Manim Sideview** extension (marketplace)
gives render-on-save with an in-editor preview panel if you prefer that to
the terminal loop.

Equally valid: hand Claude the list of tweaks in timestamp form — each is a
one-line edit, verified with frame dumps, with one re-stitch at the end.

## 5. Layout-debugging gotchas (learned the hard way)

- Colorized MathTex: the `\quad`/`\sqrt`/`\bar q`/`F_K` rules in §2 — the
  error message will blame dvisvgm, not your string.
- Dim a plotted curve with `curve.set_stroke(opacity=0.2)`. `set_opacity()`
  also sets *fill* opacity and turns open curves into ugly filled lobes.
- `Surface(checkerboard_colors=None)` crashes — omit the kwarg entirely
  (`set_fill_by_value` overrides the checkerboard anyway).
- Text (Pango) that looks letter-cramped in 480p frame dumps is usually fine
  — confirm at 1080p before "fixing" it.
- The definition cards auto-size to their text; after changing card text,
  re-check the right edge (`card.get_right()[0]` ≤ ~6.9) — several cards use
  a `scale_to_fit_width` / left-shift guard for this.
- **Style convention, not yet retrofitted:** prefer `TransformMatchingTex`
  over sequential `FadeOut`/`Write` (or `Write`-after-`Write`) when one
  formula becomes the next — it preserves visual continuity ("transform,
  don't replace"). S2's three-line homogeneity derivation currently
  `Write()`s each line in turn rather than morphing; a candidate polish pass
  for Episode 1, and worth doing by default in future episodes' scene code.

## 6. Remaining work & next episodes

- **Voiceover — recording method discussed, not yet chosen.** Style rules
  for the script itself: `..\narration_rubric.md` (cue→silence→name, don't
  read the math, translation climax, narrative-arc selection — governs
  every episode, lives at the series root). The *recording tool* is a
  separate open question; options surveyed, cheapest/simplest first:
  1. **Per-scene WAV + mux script** (free). Record one take per scene in
     any recorder at all (Audacity, even Windows' built-in recorder), name
     them `s0.wav`…`s7.wav`, and a small ffmpeg script places each at its
     known scene-start offset (§1's table) and muxes with the video.
     Deterministic, free, re-runs cleanly whenever a scene gets re-rendered.
     Not written yet — ask for `mix_narration.py` if this is the route.
  2. **DaVinci Resolve** (free). Drop the mp4 on a timeline and record
     voiceover against the moving picture on an armed audio track — the
     most precise "record to picture" experience (you see the waveform
     land under the frames), free forever, steeper first-hour learning
     curve than the options below.
  3. **Audacity** (free, simplest). Play the video muted, record
     scene-by-scene with a label track for markers, mux via option 1's
     script. Sync is by ear/timestamp rather than against visible video.
  4. **Descript** (~$16–24/mo). Record over the picture, then edit the
     *transcript* — deleting text deletes the matching audio, one-click
     filler-word removal, AI noise cleanup ("Studio Sound"), direct mp4
     export. Best re-take forgiveness across a multi-episode series; least
     frame-precise for hitting the `[SILENCE]` windows exactly.
  5. **`manim-voiceover`** (pip add-on; confirmed compatible with our manim
     0.20.1 as of its June-2026 0.4.0 release — earlier releases pinned an
     older manim). Narration text moves *into* the scene code as
     `with self.voiceover(text="..."):` blocks around each animation.
     `RecorderService` runs in the same terminal process as the render:
     you hold the `r` key to record each block (listen back with `l`,
     retake with `r`, accept with `a`), it caches each clip by its exact
     text (unchanged lines never re-record on a later run), and it times
     the animation to your *actual* recorded speech
     (`run_time=tracker.duration`) instead of the fixed `PACE` multiplier —
     this inverts today's architecture: voice becomes the clock, not the
     other way around. Install: `mamba install -n ecopy sox pyaudio` then
     `pip install "manim-voiceover[recorder]"` (pip-only; not on
     conda-forge). Structurally the right long-term choice for a
     multi-episode series, but retrofitting Episode 1 means converting
     roughly 60 `NARRATION.md` lines into voiceover blocks and giving up
     the locked 7:48 cut. A one-scene pilot (convert just S1, preview with
     free TTS before committing your own voice) was offered but not run.

  **Where this was left:** option 1 (WAV + mux) for finishing Episode 1 as
  it stands; `manim-voiceover` is worth adopting starting with Video 2,
  since there's no existing cut to disturb there and the payoff compounds
  across every future episode.
- **Video 2 — tentatively Constrained Optimization & the Method of
  Lagrange:** has its own folder now, `..\video2\`, pre-seeded with a
  `VIDEO_BRIEF_TEMPLATE.md` that already carries this context (slides 63–79
  of the F18 deck, tangency/arbitrage argument, Lagrange FOCs, λ
  interpretation — the content anchor identified in this file's §9). Copy
  `theme.py`/`params.py` into that folder as a starting point when scene
  code begins (see `..\README.md`'s fork-not-share convention) rather than
  importing them from here.
- Housekeeping: `media\` trees (here and in the session scratchpad) are
  regenerable caches — delete freely.
