# Phase 4 handoff: migrate Topic 2 to Quarto

> **This file is a one-time kickoff prompt, not a permanent doc.** It's meant
> to be read (or pasted) as the first thing in a fresh conversation about
> Phase 4, then deleted once that work is underway — its lasting content
> belongs in `HANDOFF.md` and `TOPIC_PLAN.md`, not in a phase-specific file
> like this one. (Same pattern this project already uses for superseded
> docs — see `docs/archive/`.)

## Start here

Read `HANDOFF.md` first — it's the living doc for this whole project
(Quarto authoring conventions, the extraction pipeline, known gotchas).
Read `TOPIC_PLAN.md` for the topic sequence and mapping to legacy slides.
Then come back to this file for what's specific to Phase 4.

The fold-in-Part-III decision below is **already resolved** (2026-07-19,
confirmed directly with Jonathan) — no need to re-raise it, just execute it.

## Status: Phases 0-3 done, merged, live

Topics `00_logistics` and `01_definitions-and-key-tools` are on Quarto
(`deck.qmd`) and deployed. Topic 8 was retired: its one non-duplicated
example (Opera/Football coordination game) was salvaged into Topic 1, the
rest archived to `docs/archive/08_essentials-of-game-theory/`. Topics
`02_constrained-optimization` and `03_production-optimization` are still
Marp (`deck.md`) — Phase 4 (this one) and Phase 5 respectively.

The full 6-phase plan (approved by Jonathan via Plan Mode) is at
`C:\Users\jonat\.claude\plans\sprightly-mixing-dusk.md` if you want the
original reasoning behind the phase ordering. The engagement's full history
(font-fidelity checks, the `.columns` bug, the decktape sandbox fix, the
Windows/Google-Drive file-lock saga, Topic 8's salvage decision) is in the
conversation transcript this handoff came from:
`C:\Users\jonat\.claude\projects\C--Users-jonat-My-Drive-Hunter-Eco-701\7f487dfe-57ae-42ac-ac13-b44f548efc81.jsonl`
— not required reading, but there if something here seems to assume
context you don't have.

## The Phase 4 task

Migrate `slides/02_constrained-optimization/deck.md` (Marp) to `deck.qmd`
(Quarto). This is **the largest remaining topic**: 52 slides, 570 lines,
23 media images (vs. 35 slides for Topic 3). Read its `source.yml` first —
it documents three sub-chunks (Mathematical Preliminaries; Tangency and
Lagrange Methods; Applications) and several real gotchas already solved
during the original Marp authoring (Mathcad OLE objects that are plots, not
equations; a duplicate-slide consolidation) — none of that needs redoing,
just carried forward faithfully into the port.

### Resolved: fold in the shelved Part III

**Decided 2026-07-19: fold it in.** A branch called `topic2-continuous-games`
exists on the remote, containing a fully-built, previously-reviewed
extension: continuous-action games via constrained optimization (Cournot
duopoly + a continuous-effort fisherman's-dilemma redux, both with FOC/SOC
derivations and new reaction-curve figures). It was built, PR'd (#5), then
closed without merging on Jonathan's explicit instruction at the time — its
future was left undecided, not rejected. Re-confirmed directly with
Jonathan on 2026-07-19 that it should be folded into this Quarto port
rather than abandoned (his call, not just the migration plan's original
recommendation carried through by default).

- As of 2026-07-19: the branch's diff against Topic 2's `deck.md` was a
  clean 136-line addition, and zero commits had touched that file on `main`
  since the branch diverged — should still be conflict-free, but re-check
  this (`git diff main hunter_eco701/topic2-continuous-games --stat --
  slides/02_constrained-optimization/`) since real time has passed and
  something could have changed.
- Treat the branch's content as source material to port to Quarto
  fragments/columns, not to copy verbatim — its `.md` bullets need the same
  `- ` → `::: {.incremental}` treatment as everything else, and apply the
  sequential-slides-not-tabsets convention throughout.
- Once folded in and the Quarto port is merged, delete the
  `topic2-continuous-games` branch for good — its content will have found
  a permanent home, nothing left to preserve it for.

## Established conventions (from Phases 1-3 — read `HANDOFF.md` for full detail)

- **One `##` heading + `---` per slide.** Title slide is auto-generated from
  YAML (`title`/`subtitle`/`author`/`institute`) — don't hand-author it.
- **`::: {.incremental}`** for bullet lists that build a sequential
  argument; **leave plain/static** for reference material (readings,
  grading, agendas) — staged reveal doesn't help there. Don't apply it
  reflexively to every list; think about whether *this* content benefits
  (demonstrated on both Topic 00 and the Topic 8 salvage).
- **`{.compact}`** on a slide's `##` heading when content that fit in Marp's
  layout doesn't fit at Quarto's base font size — this happened on Topic
  1's PPF slide (four bullets + image + closing blockquote). Don't
  reflexively add it everywhere; only when a real render shows genuine
  overflow. Given Topic 2 has 152 top-level equations and several dense
  worked examples per its `source.yml`, expect to need this more than once.
- **Bare/standalone images need `{fig-align="center"}`** — Quarto/revealjs
  doesn't center a lone image by default the way the shared theme centers
  tables. Bit the Opera/Football salvage; will likely bite Topic 2's many
  diagram images too.
- **`::: {.columns}` / `::: {.column width="NN%"}`** for side-by-side
  layouts (replaces Marp's `![bg right:NN% wNNN]`).
- **Tabsets don't survive to PDF** (only the default tab exports, confirmed
  and not fixable) — use sequential slides instead, never `.panel-tabset`
  for anything that needs to print.
- **`tools/verify_deck.py --topic 02_constrained-optimization`** is the
  verification loop: renders, rasterizes every page, flags edge-bleed
  heuristically. **0 flagged is not the same as correct** — it's caught
  real bugs before (a footer collision that sat a few px above the sampled
  edge band) that only showed up on an actual eyeball pass. Always
  spot-check a sample of rendered pages, not just the flag count.
- The Windows/Google-Drive `deck_files/` file-lock issue (WinError 5) is
  fixed — cleanup is best-effort and non-fatal now, you'll likely still see
  a harmless "(note: couldn't remove stray ...)" print. Ignore it.
- decktape's `--no-sandbox` flag is already in CI (`deploy-myst.yml`) — a
  hosted-runner requirement, already solved, nothing to redo.
- **Workflow**: branch fresh off `main`, commit, push, open a PR, watch CI
  to completion (`gh run watch <id> --exit-status`), **pause before
  merging** — don't merge without explicit go-ahead in that specific
  conversation. After merging, verify the *actual* push-triggered deploy run
  appears (`gh run list --json ... | jq 'select(.event=="push")'`) — a
  merge earlier in this project produced no push-triggered run at all (a
  dropped webhook delivery), silently leaving the live site stale; the fix
  was an empty commit (`git commit --allow-empty`) to force a fresh push.
  Don't assume merged == deployed; check the live site if anything looks
  off.

## Suggested first steps

1. Read `slides/02_constrained-optimization/deck.md`, `source.yml`, and
   `new_ideas.md` in full.
2. Ask Jonathan the Part III fold-in question above.
3. Branch (`quarto-migration-topic2` or similar), port the deck section by
   section (it's large — sub-chunk boundaries from `source.yml` are a
   natural place to check in, not necessarily as separate PRs).
4. Verify, spot-check by eye, PR, watch CI, pause for merge review.
