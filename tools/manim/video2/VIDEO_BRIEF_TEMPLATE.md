> **This is Video 2's working copy** of the series template
> (`../VIDEO_BRIEF_TEMPLATE.md`). Edit it in place — nothing below is final.
> **Known context:** Episode 1's outro teased this as *Constrained
> Optimization & the Method of Lagrange* (see
> `../cobb_douglas_video/PLAN.md` §9, and slides 63–79 of the F18 deck,
> already reviewed once). The working title below reflects that — treat it
> as a strong default, not a commitment; overwrite freely.

---

# Video brief template — Eco 701 series

Fill this out to start planning a new episode — in chat, or as an edited
copy of this file. This is the **input**; a planning session turns it into
that episode's `PLAN.md` storyboard, the way `manim_prompt1.md` became
Episode 1's `cobb_douglas_video/PLAN.md`.

**Lesson from Episode 1, worth internalizing before you fill this in:** the
original prompt was trimmed during editing and ended up saying "cover all
six" while only listing four beats, with dangling references to a removed
"Open decisions" section. Claude had to reconstruct the missing pieces from
the lecture slides before planning could start. Keep this file internally
consistent — if you cut something, remove every reference to it too, or
mark it explicitly as CUT rather than just deleting it silently.

---

## 1. Topic & scope
- **Working title:** Constrained Optimization & the Method of Lagrange (tentative)
- **One-sentence hook** (the question this episode answers):
- **Where it sits in the course** (unit, week, textbook chapter/section):
- **Target length:** (Episode 1 landed at ~8 min)
- **Prerequisite episodes** (what earlier videos this assumes the viewer saw): Episode 1 (Cobb-Douglas) — isoquants, MRTS, homotheticity

## 2. Source material
Point at exact files and, where possible, page/slide ranges — this saves a
research pass and keeps the video grounded in what was actually taught,
rather than a generic treatment of the topic:
- Lecture slides: `E701_F18 _slidesI.pdf`, slides 63–79 (substitution
  method, tangency/arbitrage argument, Lagrange FOCs, λ as marginal utility
  of income, welfare-max-subject-to-PPF) — already extracted once during
  Episode 1's planning; re-extract with `pypdf` if needed (poppler/pdftoppm
  is not available on this machine for direct PDF page rendering).
- Class notes / legacy files (e.g. `Eco701\legacy\...`):
- Textbook section (Nicholson & Snyder chapter):
- Anything from a past semester (recording, problem set, exam question)
  that should shape emphasis — see §4:

## 3. Content outline
Ordered list of concepts to cover. One line per item on why it's here.
Number them; if you trim later, renumber rather than leaving a gap that
reads as accidentally-missing content.
1.
2.
3.

## 4. Emphasis — this is yours, not the slides'
The slides say what must be covered; this section says how hard to lean on
each part. This is the one section a generic "read the slides, make a
video" pass can't produce on its own — it's your judgment as the instructor
who has watched students actually struggle with this material.
- **The one moment that should feel like the "aha"** (the emotional climax —
  see `../narration_rubric.md`'s emotional arc):
- **What students consistently get wrong, or ask about every semester**
  (misconceptions worth addressing head-on):
- **What to compress or skip entirely** (standard calculus, prior-course
  material, anything this audience already has cold):
- **What to slow down for** (the part that's genuinely subtle, even if it
  looks simple on the slide):

## 5. Running example
Lock ONE concrete numerical example, used throughout, and its safe domain
(stay away from boundaries and degeneracies — Episode 1 kept K, L away from
the axes because Cobb-Douglas isoquants are asymptotic there and K=0/L=0
breaks the derivatives). State it exactly enough that a `params.py` could be
written directly from this line:
- **Functional form / setup:** (candidate: reuse q=√(KL) with a budget
  constraint, so the running example carries over from Episode 1 — or pick
  a fresh one; open decision, see §8)
- **Numerical parameters:**
- **Domain:**

## 6. Narrative arc
Pick one (see `../narration_rubric.md`'s narrative-arc section for the full
list and examples): Mystery→Investigation→Resolution · Build Up→Payoff ·
Two Perspectives→Unity · Wrong→Less Wrong→Right · Specific→General ·
History as Narrative.
- **Chosen arc:** (candidate: Wrong→Less Wrong→Right — naive substitution
  method gets awkward as goods multiply → tangency/arbitrage argument →
  Lagrange as the general method; confirm or override)
- **Why it fits this topic, in one line:**

(The three-lens opening and translation climax are the series' standing
structure regardless of which arc you pick here — they compose, they don't
compete.)

## 7. Continuity with the series
- **What this episode assumes the viewer already has** (name the earlier
  episodes it leans on): Episode 1 — isoquants, MRTS, homotheticity,
  expansion paths along rays
- **What this episode should set up for the NEXT one** (Episode 1 ended by
  seeding homotheticity → expansion paths → the Lagrange tease — look for
  the equivalent thread here):
- **Branding/visual conventions to reuse:** `../cobb_douglas_video/theme.py`
  and `params.py` — see this series' README for the fork-not-share
  convention (copy them into this folder as your starting point when scene
  code begins, rather than importing across folders).

## 8. Open decisions
Anything genuinely unsure about — scene architecture, which examples to use,
whether to include an optional beat. List them explicitly; don't imply them
by omission. A planning session will either pick a sensible default and say
so, or ask directly if it materially changes the approach.
- Reuse Episode 1's q=√(KL) running example (continuity) or introduce a new
  one specific to consumer choice (e.g. Cobb-Douglas utility over two
  goods)?
- Single continuous scene for the tangency→Lagrange arc, or split like
  Episode 1's warm-up/build/payoff structure?

---

## What happens next

Hand this filled-in file to a Claude session (paste it, or point at its
path). It will read the source material in §2, resolve §8, and propose a
`PLAN.md` storyboard for review — same two-pass process as Episode 1: plan
first, approve or redirect, then build one scene at a time, checking each
render before moving on.
