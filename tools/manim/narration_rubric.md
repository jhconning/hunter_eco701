# Narration rubric — Eco 701 video series

Aesthetic ground rules for scripting and recording every episode, distilled
from Grant Sanderson's narration mechanics (Essence of Linear Algebra, ch. 1)
and adapted for a Masters micro course. Apply to `NARRATION.md` rewrites and
to every future episode's script. The test for any line: *if the animation
already says it, the voice shouldn't.*

---

## The six rules

### 1. Open with the three lenses
Every episode names its perspectives up front, and the ending returns to
them. For this series the standing buckets are:
**algebra** (expressions you manipulate) · **geometry** (objects you look at)
· **economics** (trade-offs somebody faces).
One sentence installs the frame — *"three ways to hold a production function:
as a formula, as a surface, as a map of trade-offs"* — and the climax cashes
it in (rule 6).

### 2. Cue → silence → name
The animation argues; the voice christens. For every major reveal:
- **Cue** (≤ 6 words): *"Watch the tangent as we climb."*
- **Silence** while the animation plays — written into the script as a stage
  direction with a duration: `[SILENCE — dot slides, readout falls, ~4s]`.
- **Name** what was just seen: *"Flat. That flatness is the first-order
  condition."*
Never explain first and let the animation merely confirm.

**The 2-second rule:** after every major shift, draw, or color change, two
full seconds minimum of silence before the next sentence. The big reveals
(a surface materializing, a slice projecting, a camera flatten, a ray sweep)
get their entire animation in silence.

### 3. Don't read the math
Symbols live on screen, in color; meaning lives in the voice.
- Bad: *"F-K dK plus F-L dL equals zero."*
- Good: *"Whatever the new labor adds, the lost capital must take away
  exactly — gains cancel losses. Written down, that's this equation."*
**Grad-level exception:** the *first formal definition* of a new object
(isoquant, MRTS, homothetic…) gets one slow, precise reading while its
definition card is on screen. That is the rigor beat — once per object,
never again.

### 4. Office-hours register
One-on-one, not lecture hall. Contractions, direct address, and grounding
phrases before every formal move:
*"Before the calculus, let's settle on what this slope is measuring."*
*"It's worth making sure we're all on the same page about…"*
*"Let's just settle in on one curve."*
Cut performative fillers on sight: "as we can clearly see", "it is obvious
that", "note that", "simply".

### 5. Breath-length assertions
One idea per sentence; every sentence speakable in one comfortable breath.
Scripts are written one assertion per line so overlong sentences are visible.
Read the script aloud before recording — anything you stumble on gets split.
Long chains become ladders:
*"F is homogeneous of degree r. Then its partials are homogeneous of degree
r minus one. So their ratio — the MRTS — doesn't scale at all."*

### 6. End on the translation climax
The final beat of every episode explicitly walks the loop between lenses for
the central object — the skill being taught is translation, not any single
representation:
*"The algebra says the ratio is homogeneous of degree zero. The picture says
every isoquant is the same curve at a different scale. The economics says a
bigger firm is a scaled copy of a smaller one — same recipe, more of it."*

---

## Narrative arc (planning-stage decision, one per episode)

Rules 1–6 above govern **delivery** — how any given sentence lands. This is
about **structure** — the dramatic shape of the whole episode. Pick one arc
deliberately, during planning, before storyboarding (see
`VIDEO_BRIEF_TEMPLATE.md` §6):

- **Mystery → Investigation → Resolution** — open with a puzzling result,
  investigate why it's true, reveal the principle, generalize it.
- **Build Up → Payoff** — introduce simple pieces, combine them, land a
  result the pieces alone didn't predict.
  *(Episode 1: the homogeneity computation in S2 is the build-up; the
  homotheticity payoff in S6 cashes it in.)*
- **Two Perspectives → Unity** — show a concept two ways, reveal they're the
  same thing.
- **Wrong → Less Wrong → Right** — a naive approach, why it fails, the
  refinement, the correct method.
  *(Good fit for Lagrange: substitution method gets awkward as goods
  multiply → the tangency/arbitrage argument → Lagrange as the general
  method.)*
- **Specific → General** — solve one concrete case, notice the pattern,
  abstract it.
- **History as Narrative** — frame the problem as historically encountered.

Whichever arc you pick, hold it against the **emotional arc**: curiosity
(open) → confusion (the hard part is genuinely hard) → partial clarity
(progress) → aha (the climax) → satisfaction (recap). If a storyboard jumps
straight from curiosity to satisfaction with no confusion in between, the
payoff won't land — the video needs an honest "this is the tricky part" beat
somewhere in the middle.

**This composes with, it doesn't replace, rules 1 and 6.** The three-lens
opening and the translation climax are this *series'* standing structural
signature, present in every episode regardless of which arc above wraps
around it. Episode 1's arc was Build-Up→Payoff, with Two-Perspectives→Unity
folded into its closing translation climax — arc and house style stacked,
not competing.

---

## Script format conventions

- One assertion per line; blank line = breath, `[beat]` = short pause.
- Stage directions in brackets, always with a duration for silences:
  `[ON SCREEN: definition card]`, `[SILENCE — flatten plays, ~5s]`.
- **Word budget:** conversational pace ≈ 140 wpm ≈ **2.4 words per second of
  hold**. Annotate each beat with its hold length (from the render) and keep
  the word count under budget — the slack *is* the pacing.
- Emphasis sparingly: CAPS for the one stressed word in a sentence, at most
  once per beat.
- Timestamps at scene level (from the final stitch) plus animation-moment
  markers inside scenes, so silences land on the actual frames.

## Recording checklist

1. Full read-aloud pass; split anything that doesn't fit one breath.
2. Check every `[SILENCE]` against the rendered scene (qa_frames.py or just
   scrub the mp4) — durations must match real animation timings.
3. Record close-mic, conversational volume — office hours, not stage.
4. After each reveal: count two full seconds before speaking. When in doubt,
   longer — the video's holds were stretched (`theme.PACE`) to absorb it.
5. If a passage needs more room, do NOT talk faster — stretch that scene's
   `wait()`s (or PACE) and re-render. Words never race animations.

## Calibration for this audience

Grant writes for a broad audience; Econ 701 is Masters students who know
multivariable calculus. Keep his *pacing* but not his caution: use precise
notation on screen (definition cards carry the rigor), name the textbook's
terminology once (e.g. Nicholson's "RTS"), draw the consumer-theory analogy
(MRS, indifference curves) whenever it's one sentence, and never re-derive
basic calculus aloud — cue it, show it, name it.
