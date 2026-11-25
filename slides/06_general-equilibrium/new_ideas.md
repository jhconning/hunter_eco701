# New Ideas: General Equilibrium

**Topic 7 has not been started** — no `deck.md`, no `source.yml` yet (see
TOPIC_PLAN.md: `slidesI` 268-312 exchange + `slidesIIb` ~204-222
production/two-sector). This file exists solely to hold one conceptual note
planted ahead of time, so it surfaces when this topic actually gets built.

## Uniqueness/efficiency vs. multiplicity/path-dependence (planted 2026-07-18, from Topic 1)

Surfaced while building Topic 1's Schelling postcard slide and its companion
notebook (`notebooks/topic01_schelling_segregation.ipynb`), discussing why
its equilibria are so sensitive to history compared to the "clean"
unique-efficient outcomes competitive-market treatments usually deliver. See
`slides/01_definitions-and-key-tools/new_ideas.md` for the sibling entry and
full conversation context.

**Three claims worth keeping separate when teaching this** (colloquially run
together, but not the same strength of claim):
1. **Multiple equilibria** — the model just has more than one self-consistent
   resting point.
2. **Sensitivity to initial conditions** — *different* starting points lead
   to *different* equilibria.
3. **Path dependence** (the sharpest, and what the Schelling notebook
   actually demonstrates empirically) — even the *same* starting point can
   lead to different equilibria, depending only on the random order in
   which people happened to move. Two identical populations, identical
   preferences, identical starting arrangement — genuinely different
   societies, from luck in sequencing alone.

**The mechanism — the actual transferable lesson**: whether a model
delivers one unique, efficient equilibrium or a landscape of possible
(possibly bad) ones depends on the *sign of the strategic interaction*:
- **Strategic substitutes + negative feedback** (the textbook competitive
  market: price rises, quantity demanded falls, self-correcting) → tends to
  buy uniqueness and stability.
- **Strategic complements + positive feedback** (Assurance/Palanpur,
  Schelling, network effects, bank runs, information cascades) → tends to
  produce multiplicity and path dependence, since deviations are
  self-reinforcing rather than self-correcting.

Topic 1's deck already has half of this contrast built into its own
vocabulary: the Invisible Hand game is unique-and-efficient by construction;
Assurance is explicitly labeled "strategic complements" on the Palanpur
slide. Schelling is the same logic as Palanpur, just scaled from 2 players
to N players on a network.

**The caveat this topic should state with full rigor** (Topic 1 only
gestures at it): even canonical Arrow-Debreu general equilibrium theory does
*not* generically guarantee a unique equilibrium. The Sonnenschein-Mantel-
Debreu results show aggregate excess demand functions can be badly behaved
(almost any continuous function satisfying Walras' law can arise as one),
and multiple equilibria are entirely possible without extra structure (e.g.
gross substitutability). Textbook GE treatments get uniqueness by *assuming*
the regularity conditions that deliver it, not as a free byproduct of "being
neoclassical." This is the natural place to state that precisely, with the
actual math (SMD, gross substitutes or similar sufficient conditions for
uniqueness), rather than the hand-wave Topic 1 can afford.

**One-line version for students**: *uniqueness and efficiency aren't generic
properties of "the economy" — they're properties of models with
self-correcting feedback and no externalities. Introduce complementarity or
an externality and you can trade a single good answer for a landscape of
possible ones, some of which nobody would have chosen.*

**Suggested use when this topic is built**: forward-reference the Schelling
notebook from Topic 1 (students will have already seen it) as the intuition
-building example, then state the SMD uniqueness-failure result properly
when covering GE existence/uniqueness — closing the loop opened informally
in Lecture 1.
