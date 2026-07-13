# Topic Plan: Mapping the 2018 Slides to the 11-Topic Sequence

This maps the 11-topic sequence in [`syllabus/IDEAS.md`](syllabus/IDEAS.md) onto
slide ranges in the three legacy decks (`legacy/slides/E701_F18 _slidesI.pptx`,
`_slidesII.pptx`, `_slidesIIb.pptx`), based on a lightweight title-only scan of
all 819 original slides plus the two topics already converted in detail.

**This is a draft for Jonathan's review, not a finished plan.** Several things
below are inferred from slide titles alone, not verified by reading full slide
content — and a few real problems surfaced that need a decision before work
continues.

## Open questions (please resolve before we convert more topics)

1. **`slidesII` vs `slidesIIb` overlap.** These two files cover nearly the same
   ground in nearly the same order (Game Theory II, Cournot/Stackelberg,
   principal-agent, risk-sharing, moral hazard, production/cost theory,
   Edgeworth box, GE prices). `slidesIIb` (224 slides) is 34 slides shorter
   than `slidesII` (258 slides) and appears to skip `slidesII`'s own
   recap slides (`slidesII` slides 3-23 are literally captioned "The next
   several slides repeat earlier material"). **Working hypothesis: `slidesIIb`
   is a tightened revision of `slidesII` and should be the authoritative
   source, with `slidesII` kept only for reference.** Confirm before we use
   either as a source.

2. **Slides 1-42 of `slidesI` feed two different new topics, and we've only
   partly touched them.** Topic 1 (done) drew from roughly slides 20-31
   (Pareto/PPF/UPF/basic coordination games — this mapping is an inference,
   not verified against the actual source file). Topic 8 (done) drew from
   slides 10-20 (formal Nash equilibrium treatment). That leaves slides
   32-42 (mixed strategies, N-player generalization, "two alternative
   equilibrium concepts") not yet reviewed — likely belongs in Topic 8 as
   a continuation, but should be checked rather than assumed.

3. **A meaningful chunk of the old material doesn't map to any of the 11
   topics as currently described**: extensive-form games, repeated games
   (Tit-for-Tat, Grim strategy), the Ultimatum/Dictator/Samaritan's Dilemma
   games, and Cournot/Stackelberg oligopoly (`slidesII`/`slidesIIb` roughly
   slides 24-95) aren't mentioned in any of Topic 1-11's descriptions in
   `IDEAS.md`. Either this is deliberately being dropped from the modernized
   course (a leaner 14-lecture arc than the original), or it needs an
   explicit home (an expanded Topic 8, a new Topic 12, etc.) — worth an
   explicit decision rather than silently including or dropping it.

4. **Topic 9 ("Externalities and public goods") has no obvious match** in the
   title scan of any of the three decks. This topic may need slides written
   from scratch rather than converted from 2018 material — flagging so it
   doesn't get missed as "not started yet" vs. "no source material exists."

## Proposed mapping (draft)

| # | Topic (from IDEAS.md) | Status | Proposed source | Confidence |
|---|---|---|---|---|
| 1 | Definitions and key tools | **Done** (`01_definitions-and-key-tools/`) | `slidesI` ~20-31 (inferred, not verified) | Low — verify against source |
| 2 | Constrained optimization (Lagrange, Kuhn-Tucker) | Not started | `slidesI` 43-102 | High — clean, contiguous, well-titled block |
| 3 | Production optimization (cost min, profit max, duality) | Not started | `slidesIIb` ~162-202 (or `slidesII` 190-237) | Medium — pending Q1 above |
| 4 | Consumption optimization | Not started | `slidesI` 114-209 (utility max/demand) **+** 241-251 (labor supply, non-contiguous) | Medium |
| 5 | Consumption over time and uncertainty | Not started | `slidesI` 313-337 (intertemporal) **+** `slidesIIb` ~88-117 (risk/uncertainty, non-contiguous, different file) | Medium |
| 6 | Household Economics (farm household) | Not started | `slidesI` 252-267 | High — clean, contiguous, matches description closely |
| 7 | General Equilibrium | Not started | `slidesI` 268-312 (exchange) **+** `slidesIIb` ~204-222 (production/two-sector, non-contiguous, different file) | Medium |
| 8 | Essentials of Game Theory | **Done** (`08_essentials-of-game-theory/`), partial | `slidesI` 10-20 done; 32-42 not yet reviewed (see Q2) | High for what's done |
| 9 | Externalities and public goods | Not started | No match found (see Q4) | None — likely needs new material |
| 10 | Asymmetric Information (Moral Hazard, Principal-Agent) | Not started | `slidesIIb` ~82-159 | Medium — pending Q1 |
| 11 | How micro theory frames empirical analysis | Not started | No match found | None — likely needs new material |

**Not mapped to any topic above** (pending decision, see Q3):
`slidesII`/`slidesIIb` extensive-form games, repeated games, Ultimatum/Dictator/
Samaritan's Dilemma, Cournot/Stackelberg oligopoly (~70 slides).

## How this was produced

A lightweight python-pptx scan pulled just the title (or first text line) of
all 819 slides across the three decks — no images, tables, or equations, just
enough to eyeball topic boundaries. This is NOT the same as the full
extraction pipeline used for Topics 1 and 8 (which pulls text, tables, images,
renders equations via PowerPoint COM automation, and OCRs them via Mathpix) —
that full pipeline should only be run on a slide range once its topic
assignment is confirmed here, since it's the expensive step (Mathpix has
per-call cost, COM automation takes real time per slide).
