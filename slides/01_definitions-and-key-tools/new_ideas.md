# New Ideas: Definitions and Key Tools

Backlog of expansion ideas for this topic (not a plan). Items graduate out of
here into the deck, the notebook, or a problem set by deliberate decision.

## New slides / asides

- **Preferences and choice unit** — DECIDED 2026-08-27, not yet drafted.
  Slots into the existing `Under the Hood: Optimization` section, straight
  after "Where Did Those Numbers Come From?" — that slide already asks where
  the payoff numbers came from, and this unit answers the deeper version of
  the question: what licenses writing a preference as a number at all. Order
  matters: the deck stays institutions-first and *earns* the axioms rather
  than opening with them, so this goes in the middle of Lecture 1-2, not at
  the front. Motivated by a coverage gap found comparing against Karna Basu's
  Fall 2025 section (his weeks 4-5 and both his exams test preference axioms,
  monotone transformations and diagram-reading; our sequence had none of it).
  Planned slides, roughly one per bullet:
    1. The primitive is choice: alternatives `X`, preference relation, strict
       preference and indifference as derived notions.
    2. Completeness and transitivity; the money-pump argument for why an
       intransitive agent is exploitable.
    3. Representation: `u` represents the ordering iff it preserves it.
       Finite case free; infinite case needs continuity (Debreu).
    4. Lexicographic preferences as the standard counterexample — rational,
       but no utility function represents them.
    5. Ordinality: any strictly increasing transformation is the same
       preferences. Callback to the deck's UPF/efficiency-vs-fairness slides,
       where the ordinal/cardinal distinction already does quiet work.
    6. Monotonicity and local nonsatiation: why the budget constraint binds
       and indifference curves are thin.
    7. Convexity, diminishing MRS, and why this is what makes first-order
       conditions sufficient — feeds directly into Topic 2.
    8. Indifference-curve zoo: well-behaved, perfect substitutes, Leontief,
       satiation, bads. Assessed as "describe these preferences in words."
    9. Closing the loop: the fishermen's-dilemma payoffs are ordinal, and
       pure-strategy Nash needs only the ranking; mixed strategies and
       expected utility need cardinal vNM utility — forward reference to
       Topic 5.
   10. Where the axioms fail: preference reversals, menu effects, endowment
       effect; and BFH's own point that preferences are social and shaped by
       institutions, which returns the unit to the topic's spine.
  Free student reference for this material: Osborne & Rubinstein,
  *Models in Microeconomic Theory*, ch. 1 and 4 (open access).

- **Schelling segregation as a Nash equilibrium** (BFH sec 1.15) — DONE
  (2026-07-18) as a one-slide "postcard" (households on a circle, satisfied
  unless both neighbors are the other type, cascade to segregation, both
  segregated and integrated allocations are Nash) rather than the full
  multi-panel treatment — see `notebooks/topic01_schelling_segregation.ipynb`
  for the full walkthrough. The fuller treatment (step-by-step cascade,
  the random-matching results below, the sensitivity widget) is still a
  strong candidate for a dedicated Topic 9 slot if one opens, rather than
  squeezing more of it into Lecture 1.
- **Nash biography aside** — DONE (2026-07-18): cannibalized from Topic 8
  (dissolved per TOPIC_PLAN.md) as a single text-only "Aside: Who Was John
  Nash?" slide, right after "Nash Equilibrium." Deliberately dropped both
  bg images (`nash-portrait.png`, `beautiful-mind-poster.png`) rather than
  reuse them — neither has documented licensing in Topic 8's `source.yml`,
  the portrait looks like an uncredited tribute-banner pulled from a news
  site, and the poster/book-cover are near-certainly copyrighted commercial
  art. **Flagged, not yet fixed: these same three images are still live on
  the currently-deployed `08_essentials-of-game-theory` deck** — worth
  addressing regardless of that topic's undecided archive/keep/cannibalize
  fate (see TOPIC_PLAN.md resolved decision 5), since it's a live-site
  copyright exposure independent of that question.
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

---

## Design note: why the opening lectures are strategic-interaction-first

Recorded 2026-08-28, from Jonathan. This is the rationale the rest of this
file's sequencing decisions should be judged against, not another backlog item.

**The principle.** The first few lectures exist to argue that economics studies
how *strategic actors interact*. Each actor optimizes subject to constraints
and derives a best-response function; the interesting question is then whether
the resulting equilibrium is efficient or otherwise desirable. Mechanism design
is framed as changing the rules of the game to steer toward a better outcome —
and **a competitive market is one such mechanism**, which makes "when does
self-interested behavior by individuals and firms produce an efficient
outcome?" a central question of the course rather than a background assumption.

Setting up this framework before the machinery gives students the big picture
and the key tradeoffs up front, so they don't get lost in details without
seeing the larger questions. Bowles & Halliday take a similar approach, which
is why axiomatic preferences and supply-and-demand appear late in their book.

**What the ordering buys.** It makes the competitive market a *member of a
class* rather than the unmarked default. In the conventional sequence, perfect
competition is the background against which everything else is an exception:
monopoly is a deviation, externalities a failure, asymmetric information a
wrinkle. Here the First Welfare Theorem is instead a result about one
particular mechanism, interesting precisely because it states conditions — and
every later topic reads as a variation in the rules rather than an exception to
nature (externalities as a missing property right, asymmetric information as a
missing message, monopoly as a different number of players). That framing is
what makes Topic 11 coherent rather than tacked on, and what lets general
equilibrium in the late weeks answer a question students have carried since
week 1.

**Why monopoly and Cournot belong early, in this deck's tail.** The sequence
monopoly → duopoly → N firms → N to infinity varies exactly one rule of the
game (how many actors) and watches the equilibrium move. The competitive
outcome therefore arrives as the *limit of a game we built*, in week 2, rather
than as an axiom in week 11. Running the continuous commons game alongside it
makes the lesson cut both ways: more players drives one system toward
efficiency and the other away from it, with identical mathematics — so whether
"more competition" is good depends on the sign of the externality. The slides
for the continuous-game half of this already exist in PR #5 (recoverable at
`refs/pull/5/head`, commit `088599e`, local branch `pr5-continuous-games`);
what is missing is linear monopoly as the N=1 on-ramp and the N-firm limit.

**Two things this ordering has to protect.**

1. *Pay the promissory note on payoffs.* With the preferences and choice unit
   deferred to the consumption block, "utility" floats free for several weeks
   and students compute best responses fluently while staying vague about what
   a payoff is. The fix is not to front-load the axioms but to say plainly, in
   week 2, that payoffs are being treated as ordinal rankings, that
   pure-strategy Nash needs only the ordering, and that where the numbers come
   from is a later lecture — then honor it when that lecture arrives. This
   turns a deferral into a structure students can see rather than a gap they
   suspect.
2. *State the roadmap more than once.* Students arriving from a conventional
   intermediate course will be waiting for supply and demand and may read its
   absence as omission rather than design. The existing "The Method — and the
   Road Ahead" slide does this once; it wants a one-line callback when the
   consumption block opens and again when general equilibrium arrives.

**Where we diverge from BFH, and why students should be told.** BFH defer both
preferences and competition, but stay largely at the intermediate mathematical
level. This course defers the same two things while running Lagrange,
Kuhn--Tucker and duality in the weeks straight after this deck. So BFH supplies
the framing and the games; Nicholson/Snyder supplies machinery BFH
deliberately does not. Saying that explicitly in week 1 stops the two books
from looking like they disagree about what the course is.

---

## Design note: the AI-era thread ("same tools, new markets")

Recorded 2026-08-28, from a framing discussion with Jonathan. Companion to the
strategic-interaction-first note above — this is the *contemporary-relevance*
layer on top of that arc. Nothing here is drafted into slides yet.

**The claim, sized honestly.** New technologies are creating new types of
markets and mechanisms, and the toolkit of this course — constrained
optimization, best response, equilibrium, mechanism design, plus numerical
cousins like gradient descent — will keep being useful even where the
applications are new or surprising. The historical pattern to invoke: spectrum
auctions (1994), kidney exchange, the ad auctions that fund the internet,
matching platforms. Each wave of technology created a coordination problem and
the answer was mechanism design, not new physics. Claim agentic AI as the next
*instance*, not an exception.

**The Jordan anchor.** Michael I. Jordan's argument that the "AI era" will be
a large distributed engineering and mechanism-design challenge rather than the
emergence of a centralized superintelligence. Two citations:

- Jordan (2018), "Artificial Intelligence — The Revolution Hasn't Happened
  Yet" (Harvard Data Science Review) — the origin statement.
- Jordan (2025), "A Collectivist, Economic Perspective on AI"
  (arXiv:2507.06268) — post-LLM, much more concrete, cite as primary.
  Position paper, not peer-reviewed; always "Jordan argues."

New in the 2025 paper and course-usable:
- **LLMs as "collectivist artifacts"** — an LLM aggregates the contributions
  of millions of humans; his reframe "an LLM to a person seems irresistible,
  [but] an LLM to a culture is equally valid." Recasts "is it intelligent?"
  as "what kind of collective institution is it?" — exactly this deck's
  institutions-first opening.
- **The broken search-era contract** — creators supplied content in exchange
  for visibility/traffic; "the LLM becomes the endpoint rather than an
  intermediary." A missing-market / broken-implicit-contract problem stated
  in course vocabulary.
- **Three uncertainty sources, three disciplines** — sampling (statistics),
  information asymmetry (economics), provenance (CS), to be handled jointly
  at algorithm-design level. Quotable for epistemic humility: "We do not have
  the equivalent of Maxwell's equations as a guide. We are winging it."
- **Worked mechanisms**: three-way music market (United Masters:
  musicians-listeners-brands, brands pay artists directly); three-layer data
  market with *priced privacy* (platforms contractually guarantee noise
  levels, users shop privacy-utility menus — second-degree screening in new
  clothes); statistical contract theory (incentive-compatible hypothesis
  testing); prediction-powered inference as an *audit/reputation* mechanism
  disciplining foundation-model providers.
- **Appendix B curricular claim** — education should blend computational,
  inferential and economic thinking (mechanism design, matching, contracts,
  auctions alongside algorithms). Nearly this course's thesis; cite once in
  week 1, sparingly (self-congratulation risk).
- Caution: "collectivist" in the title reads politically to some students;
  his use is technical (intelligence as socially constituted, design for
  collective welfare). One disarming sentence if assigned. Pairs with Hayek
  (1945) "The Use of Knowledge in Society" — dispersed knowledge and
  aggregation mechanisms, seventy years apart; "AI as central planner" is
  the socialist calculation debate redux.

**Example bank, mapped to the sequence** (tier 1 = published/checkable,
tier 2 = emerging, label as such on any slide):

- *Weeks 1-2, best response & Nash* (tier 1): an LLM agent told to "get the
  best price" is a literal best-response computer; two negotiating = the game
  on the board. **GANs**: generator vs discriminator is a continuous zero-sum
  game, training = searching for Nash by alternating gradient steps; training
  instability = best-response dynamics failing to converge — same picture as
  cycling reaction-curve dynamics in the fisherman/Cournot diagram.
- *Week 2, Cournot* (tier 1): **algorithmic collusion** — Calvano, Calzolari,
  Denicolò & Pastorello (AER 2020): Q-learning pricing agents in repeated
  Bertrand learn supracompetitive prices without communicating. Real-world
  hook: RealPage rent-pricing litigation. Makes repeated games (Topic 8b)
  feel urgent. Also: iterated best response = coordinate descent on a game;
  gradient descent and tatonnement are cousins.
- *Weeks 3-5, optimization* (tier 1): gradient descent belongs in the math
  toolkit slides — Lagrange/KKT give conditions, gradient descent is how
  machines find the point. Safe-RL/alignment training literally uses
  Lagrangian methods: the constraint enters as a multiplier, the multiplier
  is the price of the constraint. (`docs/Gradient Descent.md` is the seed.)
- *Week 6, preferences* (tier 1): RLHF's reward model is a *learned utility
  function* elicited from pairwise comparisons — ordinality made concrete.
- *Week 13, commons* (tier 1/2): recommender attention externalities;
  congestion on shared compute; **model collapse as a commons problem**
  (models training on model-generated text degrade the shared data commons).
- *Week 14, information* (tier 1): **RLHF/alignment as principal-agent** —
  unobservable internal computation, reward model as incentive scheme,
  reward hacking = Goodhart + Holmström-Milgrom multitasking ("specification
  gaming" and the multitask agency problem are the same theorem). Ad
  auctions/position auctions as the trillion-dollar proof the toolkit pays.
  Jordan-group statistical contract theory as a reading pointer.
- *Tier 2 throughout*: agent-to-agent commerce, data markets at scale, AI
  negotiators — present as open questions the toolkit is positioned to
  attack, never as facts.

**Delivery: "AI-era postcards."** Reuse the deck's existing postcard format
(cf. the Schelling postcard): one clearly-badged slide per topic, a running
thread rather than a dedicated AI lecture. The badge does the epistemic work —
postcards are dispatches, not theorems. Date-stamp each ("as of Fall 2026").

**Guardrails.** Claim the *structure* transfers, never that the conclusions
do ("reward hacking is a multitasking agency problem" is safe; "economics
solves alignment" is not). No mind-language — "computes a best response," not
"wants." Let Jordan carry the big thesis with attribution. One honest
counterweight slide late in the course: where the analogies strain (agents
without stable preferences; equilibria that learning dynamics never reach).
