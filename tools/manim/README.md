# Eco 701 video series

3Blue1Brown-style Manim videos for Eco 701 (Masters micro, Hunter College
CUNY). Each episode lives in its own folder with its own README/PLAN/scenes;
shared conventions live here at the series root.

## Episodes
- `cobb_douglas_video/` — **Video 1: The Cobb-Douglas Production Function.**
  Built and rendered; narration script written and ready to record (see
  that folder's own `README.md` and `NARRATION.md`).
- `video2/` — **tentatively Constrained Optimization & the Method of
  Lagrange** (Episode 1's own teaser; not committed). Planning stage — see
  `video2/VIDEO_BRIEF_TEMPLATE.md`, pre-seeded with what's already known.
- `video3/` — topic not yet chosen. Planning stage — see
  `video3/VIDEO_BRIEF_TEMPLATE.md`, currently blank.

Folder names don't need to match final titles — `cobb_douglas_video` earned
its name after the fact; `video2`/`video3` are placeholders until each
episode's title is settled, and there's no obligation to rename them later.

Every episode folder is seeded with the same four files from day one, filled
in progressively as the episode moves through its lifecycle:
`VIDEO_BRIEF_TEMPLATE.md` (planning input) → `PLAN.md` (storyboard, once
planned) → `NARRATION.md` (script, once scenes exist) → `README.md` (code
map, once built). A folder's current stage is always visible from which of
these are still stubs.

## Code reuse across episodes: fork, don't share

`theme.py` and `params.py`'s pattern are designed to be reused, but each
episode keeps its **own copy** rather than importing across folders. When
you start scene code for a new episode, copy the most recent episode's
`theme.py`/`params.py` into the new folder as a starting point, then diverge
as needed. This is deliberate: a live shared import means tuning a color or
a card layout for Video 3 could silently shift Video 1's already-rendered,
already-delivered look the next time it's rendered. A few things should stay
identical across episodes by convention (not enforcement), for visual
continuity across the series: the palette, `branding_card`,
`definition_card`, and `PacedScene`/`PacedThreeDScene`. Anything
episode-specific is free to diverge locally.

## Shared docs — read these before planning a new episode
- **`VIDEO_BRIEF_TEMPLATE.md`** — fill this out to start planning any new
  episode. It's the input to a planning session, the same way
  `manim_prompt1.md` (historical — Episode 1's original brief, now
  superseded by this template for every episode after it) was the input
  that became Episode 1's `PLAN.md`.
- **`narration_rubric.md`** — the series' narration style rules: delivery
  mechanics (cue→silence→name, don't read the math, breath-length lines)
  plus narrative-arc selection. Applies to every episode's script.

## Starting a new episode
1. Fill out `VIDEO_BRIEF_TEMPLATE.md` for the new topic — source slides,
   content outline, and critically §4 (what to emphasize, which is your
   call, not the slides').
2. Hand it to a Claude session. It researches the source material, resolves
   any open decisions, and proposes a `PLAN.md` storyboard — share the plan
   before writing code, per Episode 1's two-pass process.
3. Build incrementally: one scene at a time, low-quality render + visual
   check before advancing. See `cobb_douglas_video/README.md` for the
   concrete render/test loop — the same tools (`smoke_test.py` pattern,
   `qa_frames.py`, `manim.cfg`, `-s -n a,b` single-frame checks) apply to
   every episode.
4. Write the narration script against `narration_rubric.md`.
5. Record narration, final render, stitch. The recording *method* (as
   opposed to the script style) is a separate, still-open decision — see
   `cobb_douglas_video/README.md` §6 for the options surveyed (a free
   WAV+mux script, DaVinci Resolve, Audacity, Descript, or `manim-voiceover`
   — the last is worth adopting starting with whichever episode is built
   next, since it has no existing cut to disturb).
