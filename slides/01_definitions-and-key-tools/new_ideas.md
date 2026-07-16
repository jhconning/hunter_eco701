# New Ideas: Definitions and Key Tools

Backlog of expansion ideas for this topic (not a plan). Items graduate out of
here into the deck, the notebook, or a problem set by deliberate decision.

## New slides / asides

- **Schelling segregation as a Nash equilibrium** (BFH sec 1.15) — cut from the
  lecture for time. Strongest candidate for reinstatement if a slot opens, or
  as a Topic 9 aside: uncoordinated moves by integration-preferring households
  reach a fully segregated Nash equilibrium; both segregated *and* integrated
  allocations are equilibria (multiple equilibria + path dependence in one
  story).
- Nash biography aside — `slides/08_essentials-of-game-theory/media/`
  already has `nash-portrait.png` and a two-slide bio if ever wanted here.
- Equilibrium-selection caveats slide (BFH sec 1.17's three caveats:
  collective best responses, equilibrium selection, out-of-equilibrium
  dynamics) — currently presenter-notes only on the wrap slide.

## Notebook / interactive

- **Schelling circle simulation** — 12 households on a clock face, random
  dissatisfied-pair swaps, watch integration collapse to segregation;
  ipywidgets "step" button. Natural companion to the existing
  `topic01_definitions_key_tools_figures.ipynb`.
- The **externality knob** demo (already prototyped as the notebook's last
  cell): slider on alpha in u_A = (15 - alpha*e_B)e_A - e_A^2/2 morphs
  commons over-use (alpha > 0) through invisible hand (alpha = 0) to
  public-goods under-provision (alpha < 0) — reuse live in class for Topic 1
  and again when Topic 9 opens.
- Payoff-matrix "game morpher": sliders on generic (w, x, y, z) with live
  best-response dots, showing the PD -> Assurance -> Invisible Hand
  boundaries as inequalities flip (BFH sec 1.16's transformation logic,
  generalized).

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
  the Schelling circle are Nash equilibria (if segregation gets a slot
  anywhere).

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
