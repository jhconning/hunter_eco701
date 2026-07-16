# Topic Plan: Mapping the 2018 Slides to the 11-Topic Sequence

This maps the 11-topic sequence in [`syllabus/IDEAS.md`](syllabus/IDEAS.md) onto
slide ranges in the three legacy decks (`legacy/slides/E701_F18 _slidesI.pptx`,
`_slidesII.pptx`, `_slidesIIb.pptx`), based on a lightweight title-only scan of
all 819 original slides plus the two topics already converted in detail.

**This is a draft for Jonathan's review.** Several slide-range mappings below
are inferred from slide titles alone, not verified by reading full slide
content. The four structural open questions from the first draft of this
document were resolved by Jonathan on 2026-07-13 (see below) — remaining
uncertainty is now just about exact slide boundaries, not about what to do.

## Resolved decisions (2026-07-13)

1. **`slidesII` vs `slidesIIb`: resolved.** `slidesIIb` is the tightened
   revision and is now the authoritative source for anything in that range.
   `slidesII` is archived/reference-only — don't extract from it going
   forward.

2. **`slidesI` slides 32-42: resolved.** Confirmed as a continuation of
   Topic 8 (mixed strategies, N-player generalization). Not yet extracted —
   see `slides/08_essentials-of-game-theory/source.yml`.

3. **The ~70 unmapped Game Theory II / oligopoly slides: resolved.** These
   become **Topic 8b** — kept as an isolated, explicitly optional topic in
   case there's time to cover it this semester, not merged into Topic 8
   proper and not silently dropped. See the mapping table below.

4. **Topic 9 ("Externalities and public goods"): resolved.** No 2018 source
   material exists for this — it needs original slides written from
   scratch. Keep it as a real topic slot in the sequence; the actual
   slide-writing is deferred to a future date, not blocked on anything here.

## Proposed mapping (draft)

| # | Topic (from IDEAS.md) | Status | Proposed source | Confidence |
|---|---|---|---|---|
| 1 | Definitions and key tools | **Done** (`01_definitions-and-key-tools/`) | `slidesI` ~20-31 (inferred, not verified) | Low — verify against source |
| 2 | Constrained optimization (Lagrange, Kuhn-Tucker) | **Done** (`02_constrained-optimization/`) | `slidesI` 43-102 | High — clean, contiguous, well-titled block |
| 3 | Production optimization (cost min, profit max, duality) | Not started | `slidesIIb` ~162-202 | Medium — confirm exact boundary |
| 4 | Consumption optimization | Not started | `slidesI` 114-209 (utility max/demand) **+** 241-251 (labor supply, non-contiguous) | Medium |
| 5 | Consumption over time and uncertainty | Not started | `slidesI` 313-337 (intertemporal) **+** `slidesIIb` ~88-117 (risk/uncertainty, non-contiguous, different file) | Medium |
| 6 | Household Economics (farm household) | Not started | `slidesI` 252-267 | High — clean, contiguous, matches description closely |
| 7 | General Equilibrium | Not started | `slidesI` 268-312 (exchange) **+** `slidesIIb` ~204-222 (production/two-sector, non-contiguous, different file) | Medium |
| 8 | Essentials of Game Theory | **Done** (`08_essentials-of-game-theory/`), partial | `slidesI` 10-20 done; 32-42 confirmed as continuation, not yet extracted | High |
| 8b | *(not in IDEAS.md — optional/isolated)* Game Theory II: extensive form, repeated games, oligopoly | Not started, deliberately deferred | `slidesIIb` ~15-80 (Games in Extensive Form through "Other applications", before Principal Agent content starts at ~81) | Medium — confirm exact boundary |
| 9 | Externalities and public goods | Deferred | No 2018 source material — needs original slides, future date | N/A |
| 10 | Asymmetric Information (Moral Hazard, Principal-Agent) | Not started | `slidesIIb` ~82-159 | Medium — confirm exact boundary |
| 11 | How micro theory frames empirical analysis | Not started | No match found | None — likely needs new material |

**Topic 8b** is intentionally kept separate from Topic 8 rather than merged
or dropped: it preserves genuinely rich material (Samaritan's Dilemma,
subgame perfection, Ultimatum/Dictator games, Tit-for-Tat, Cournot/
Stackelberg) in case there's time to cover it this semester, without
committing to it or letting it bloat Topic 8's core scope.

## How this was produced

A lightweight python-pptx scan pulled just the title (or first text line) of
all 819 slides across the three decks — no images, tables, or equations, just
enough to eyeball topic boundaries. This is NOT the same as the full
extraction pipeline used for Topics 1 and 8 (which pulls text, tables, images,
renders equations via PowerPoint COM automation, and OCRs them via Mathpix) —
that full pipeline should only be run on a slide range once its topic
assignment is confirmed here, since it's the expensive step (Mathpix has
per-call cost, COM automation takes real time per slide).
