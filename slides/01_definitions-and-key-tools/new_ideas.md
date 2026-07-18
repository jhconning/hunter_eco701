# New Ideas: Definitions and Key Tools

Backlog of expansion ideas for this topic (not a plan). Items graduate out of
here into the deck, the notebook, or a problem set by deliberate decision.

## New slides / asides

- **Schelling segregation as a Nash equilibrium** (BFH sec 1.15) — DONE
  (2026-07-18) as a one-slide "postcard" (households on a circle, satisfied
  unless both neighbors are the other type, cascade to segregation, both
  segregated and integrated allocations are Nash) rather than the full
  multi-panel treatment — see `notebooks/topic01_schelling_segregation.ipynb`
  for the full walkthrough. The fuller treatment (step-by-step cascade,
  the random-matching results below, the sensitivity widget) is still a
  strong candidate for a dedicated Topic 9 slot if one opens, rather than
  squeezing more of it into Lecture 1.
- Nash biography aside — `slides/08_essentials-of-game-theory/media/`
  already has `nash-portrait.png` and a two-slide bio if ever wanted here.
- Equilibrium-selection caveats slide (BFH sec 1.17's three caveats:
  collective best responses, equilibrium selection, out-of-equilibrium
  dynamics) — currently presenter-notes only on the wrap slide.

## Notebook / interactive

- **Schelling circle simulation** — DONE (2026-07-18):
  `notebooks/topic01_schelling_segregation.ipynb`. Exactly reconstructs BFH's
  own 12-household, 3-swap example (verified by assertion against the
  book's specific swap sequence and named individuals), then goes further:
  a general random-matching simulator, classified by cluster count (not a
  segregation-index cutoff — an earlier pass used index > 1.8 as "full
  segregation" and got 0%, which was simply wrong: the book's own exact
  outcome has index 1.667, not near the theoretical max of 2, because a
  circle split into two same-type arcs always has four k_i=1 "boundary"
  households). Corrected, verified finding (300 random runs from the
  checkerboard, n=12): **27% land on exactly full segregation** (matching
  the book's outcome), **5% land on exactly the integrated ideal**, and the
  modal outcome (68%) is a *milder* version of the same phenomenon — two or
  three separate same-type neighborhoods per group rather than one giant
  one. Full segregation is common, not rare; full integration is the one
  that's genuinely hard to reach by chance. Interactive ipywidget (n, group
  share, tolerance threshold, seed) included for exploring this live in
  class.
- The **externality knob** demo (already prototyped as the notebook's last
  cell): slider on alpha in u_A = (15 - alpha*e_B)e_A - e_A^2/2 morphs
  commons over-use (alpha > 0) through invisible hand (alpha = 0) to
  public-goods under-provision (alpha < 0) — reuse live in class for Topic 1
  and again when Topic 9 opens.
- Payoff-matrix "game morpher": sliders on generic (w, x, y, z) with live
  best-response dots, showing the PD -> Assurance -> Invisible Hand
  boundaries as inequalities flip (BFH sec 1.16's transformation logic,
  generalized).

## Conceptual notes (bigger-picture connections)

- **Uniqueness/efficiency vs. multiplicity/path-dependence — the
  feedback-sign lesson** (surfaced 2026-07-18, discussing why Schelling's
  equilibria are so sensitive to history compared to the "clean"
  unique-efficient outcomes competitive-market treatments usually deliver).
  Full note, including the Sonnenschein-Mantel-Debreu caveat and a
  suggested use, saved in `slides/07_general-equilibrium/new_ideas.md`
  (Topic 7 doesn't exist yet — that file holds it until it does). Summary:
  - Three claims worth keeping separate: **multiple equilibria** (more than
    one resting point exists) vs. **sensitivity to initial conditions**
    (different starts → different ends) vs. **path dependence** (the
    sharpest — even the *same* start can lead to different ends, purely
    from the random order people happened to move; this is what the
    Schelling notebook's 300-run experiment actually demonstrates).
  - The mechanism: **strategic substitutes + negative feedback**
    (competitive markets, self-correcting) buys uniqueness and stability;
    **strategic complements + positive feedback** (Assurance/Palanpur,
    Schelling) produces multiplicity and path dependence instead. Topic 1
    already half-builds this contrast in (Invisible Hand = unique/efficient;
    Assurance is explicitly labeled "strategic complements" on the Palanpur
    slide) — Schelling is the same logic scaled to N players.
  - One-line student version: *uniqueness and efficiency aren't generic
    properties of "the economy" - they're properties of models with
    self-correcting feedback and no externalities. Introduce complementarity
    or an externality and you can trade a single good answer for a landscape
    of possible ones, some of which nobody would have chosen.*
  - Where it could land: a light one-or-two-sentence closing remark on "The
    Lecture in One Table" tying Invisible Hand -> Assurance -> Schelling
    together, **or** (leaning this way, Lecture 1 is already dense) held
    back entirely for Topic 7's GE existence/uniqueness treatment, where the
    SMD caveat can be stated with actual rigor instead of a hand-wave.

## Problem set ideas (PS1 candidates)

- **Drain the meadow: name that game** (BFH Checkpoint 1.18): build the
  payoff matrix from drained-meadow value 5, undrained 3, joint drain cost 1
  each, solo drain cost 3; find equilibria; classify the game; explain
  Hume's "thousand persons" remark.
- **Guilt as a payoff transformation** (Checkpoint 1.13): smallest guilt g
  subtracted from a defector-against-cooperator's payoff that destroys the
  dominant strategy; what if only one player feels it? (Bridges to BFH Ch. 2
  social preferences.)
- **Liability by the numbers** (Checkpoint 1.20) with the deck's cardinal
  payoffs 78/75/72/70 instead of BFH's ordinal 4/3/2/1.
- **When is cooperation not the best they can do?** (Checkpoint 1.12): if
  2w < x + y, show alternating defection beats mutual cooperation.
- **Derive the matrix** (post-Topic-2 PS): from u_A = (15 - e_B/4)e_A -
  e_A^2/2 derive best responses, Nash (12, 12), planner (10, 10), and the
  2x2 payoffs; verify the liability rule restores efficiency. (The figures
  notebook contains the full solution — don't hand that out.)
- Prove both the fully segregated and the ideal integrated allocations of
  the Schelling circle are Nash equilibria (the postcard slide asserts
  both; a PS question could ask students to verify k_i for each position
  by hand, or extend to the random-matching patchwork case).

## Course-level consolidation (pending decisions — affects TOPIC_PLAN.md)

Agreed direction from the 2026-07-16 brainstorm (Jonathan approved drafting
this deck; the TOPIC_PLAN/topic-8 restructuring below is proposed but NOT yet
ratified — do not edit TOPIC_PLAN.md without his explicit call):

- **Topic 1** (this deck) now owns the informal game-theory basics + Pareto /
  PPF / UPF + a first dose of FOC-level optimization via the continuous
  fisherman game.
- **Topic 2** should gain a short "games with continuous actions" application
  block (reaction curves done properly, Cournot as a problem-set twin) —
  slides not yet written.
- **Topic 8's lecture slot**: proposal is to dissolve it (its basics now live
  here; N-player/public-goods content goes to Topic 9 where it's used;
  repeated games/extensive form stay in optional Topic 8b), freeing a lecture
  for the crowded core. Alternative: rescope Topic 8 as "Game Theory II:
  repetition and cooperation" from 8b material. **Jonathan to decide.**
- **00_logistics deck** still cites the supplementary text as the "(2018
  draft)" — the assigned text is now Bowles & Halliday, *Microeconomics:
  Competition, Conflict, and Coordination* (OUP 2022). That deck is a
  faithful Fall-2018 conversion throughout, so updating one line piecemeal
  was deferred; fix when 00_logistics gets its semester refresh.
