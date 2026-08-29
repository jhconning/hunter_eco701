# PLAN — Video 2 (Eco 701 series)

**Status: not started.**

1. Fill in `VIDEO_BRIEF_TEMPLATE.md` in this folder (it's pre-seeded with
   the known context from Episode 1's teaser — edit or override freely).
2. Hand it to a Claude session. It will read the source slides, resolve any
   open decisions left in §8, and write this file as a scene-by-scene
   storyboard — same shape as `../cobb_douglas_video/PLAN.md`.
3. From there: build one scene at a time, low-quality render + visual check
   before advancing. See `../cobb_douglas_video/README.md` for the concrete
   tools (`smoke_test.py` pattern, `qa_frames.py`, `manim.cfg`, single-frame
   `-s -n a,b` checks) — same tools apply to every episode.
