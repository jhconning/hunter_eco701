# Topic 5 plan: Choice over Time and under Uncertainty

Draft 2, 2026-11-08. For class 9 (Mon Nov 9). Readings: NS 17 (time), NS 7 (uncertainty).

**Built 2026-11-08** as `deck.qmd` (33 pages), with two changes from this plan, at
Jonathan's request: (1) a **saver** with income (80, 20) runs alongside the borrower all
through Part I, with figures for both (r = 0: both at (50, 50); r = 25%: borrower
(42, 52.5), saver (48, 60)), an Edgeworth box where borrower and saver clear the credit
market, and a two-panel interest-rate slider; (2) the **monopoly lender and insurer moved to
the end** (Part IV, "Turning the Problem Around"), presented as the dual: maximize profit
subject to the client's participation = minimize the cost of the client's utility. The slide
order in the deck supersedes the sequence below.

Changes from draft 1 (Jonathan's choices): simpler examples, now one set of numbers for
the whole deck; present bias dropped; risk-sharing math added; monopoly lender kept;
budgets written with prices; comparison table built up column by column; the three
Lagrangians shown side by side.

## The one idea the deck should carry

Topic 5 adds no new mathematics. It renames the goods in Topic 4's problem: the two goods
become two dates, then two states of the world. Every budget is written in Topic 4's form,
**price × quantity = value of what you start with**:

| | Topic 4: two goods | Part I: two dates | Part II: two states |
|---|---|---|---|
| Goods | $x$, $y$ | $c_1$ (today), $c_2$ (tomorrow) | $c_g$ (good state), $c_b$ (bad state) |
| Utility | $u(x,y)$ | $u(c_1) + \delta\,u(c_2)$ | $\pi\,u(c_g) + (1-\pi)\,u(c_b)$ |
| Prices | $p_x$, $p_y$ | $p_1 = 1$, $p_2 = \tfrac{1}{1+r}$ | $p_g$, $p_b$ |
| Budget | $p_x x + p_y y = I$ | $p_1 c_1 + p_2 c_2 = p_1 m_1 + p_2 m_2$ | $p_g c_g + p_b c_b = p_g m_g + p_b m_b$ |
| Tangency | $MRS = p_x/p_y$ | $\dfrac{u'(c_1)}{\delta u'(c_2)} = \dfrac{p_1}{p_2} = 1+r$ | $\dfrac{\pi u'(c_g)}{(1-\pi)u'(c_b)} = \dfrac{p_g}{p_b}$ |
| Benchmark | | $\delta(1+r)=1 \Rightarrow c_1 = c_2$ (smoothing) | $p_s = \pi_s \Rightarrow c_g = c_b$ (full insurance) |

**Built up gradually:** the opening slide shows only the Topic 4 column with the other two
greyed out; Part I fills in the dates column; Part II fills in the states column; the
closing slide shows the whole table.

**Writing the budget with prices.** $p_2 = 1/(1+r)$ is what one dollar of consumption
tomorrow costs today (a bond that pays \$1 next period). The right side is the value of the
endowment, as in labor supply ($24w + y$). So the time budget is Topic 4's budget with an
endowment, not a new object. The usual "present value" form $c_1 + \tfrac{c_2}{1+r} =
m_1 + \tfrac{m_2}{1+r}$ follows by substituting $p_1 = 1$ and $p_2 = 1/(1+r)$.

Two points to make in words:

1. **Two separate things are discounted.** Utility is discounted by $\delta$ (impatience, a
   preference). Money is discounted by $p_2 = 1/(1+r)$ (the time value of money, a price).
   The Euler equation compares them. The table keeps them in different rows.
2. **Smoothing over time and insurance across states are the same result.** Both come from
   concave $u$ with each good's price equal to its weight in utility.

## The three Lagrangians, side by side (one slide)

$$
\begin{aligned}
\mathcal{L} &= u(x,y) + \lambda\,[\,I - p_x x - p_y y\,] \\
\mathcal{L} &= u(c_1) + \delta\,u(c_2) + \lambda\,[\,p_1 m_1 + p_2 m_2 - p_1 c_1 - p_2 c_2\,] \\
\mathcal{L} &= \pi\,u(c_g) + (1-\pi)\,u(c_b) + \lambda\,[\,p_g m_g + p_b m_b - p_g c_g - p_b c_b\,]
\end{aligned}
$$

First-order conditions in three matching rows: $u_x = \lambda p_x$; $u'(c_1) = \lambda p_1$,
$\delta u'(c_2) = \lambda p_2$; $\pi u'(c_g) = \lambda p_g$, $(1-\pi) u'(c_b) = \lambda p_b$.
Dividing gives the tangency row of the table. In each, $\lambda$ is the marginal utility of a
dollar of wealth (Topic 2's shadow price).

## Continuity hooks into Topics 2-4

- **Log utility is Cobb-Douglas.** $\ln c_1 + \delta \ln c_2$ ranks bundles the same way as
  $c_1 c_2^{\delta}$ (Topic 4: "utility is only a ranking"). The Topic 4 demand formula gives
  the answer at once: spend share $\tfrac{1}{1+\delta}$ of wealth today. For states the shares
  are $\pi$ and $1-\pi$.
- **The endowment budget line is labor supply again.** A rise in $r$ rotates the line around
  the endowment, as a wage rise rotated the labor supply line. Borrower vs saver = net buyer
  vs net seller. The income effect's sign depends on which side of the endowment you are.
- **Borrowing constraints are Kuhn-Tucker.** Add $c_1 \le m_1$. If it binds, the Euler
  equation fails and its multiplier $\mu$ measures the value of credit.
- **Fisher separation = farm-household separation.** With a perfect credit market, choose
  investment to maximize present value, then consume. When credit fails, separation fails:
  the hand-off to next week's farm household.
- **Efficiency vs distribution (Topic 1).** The monopoly lender and the competitive market
  give the same smooth consumption path; they differ only in who gets the surplus.

## One set of numbers for the whole deck (checked)

Log utility, $\delta = 1$, $\pi = 1/2$ throughout. The endowment is always **(20, 80)**:
20 today and 80 tomorrow, or 20 in drought and 80 in rain.

**Part I: time**
- **Base case, $r = 0$** ($p_1 = p_2 = 1$, so this is exactly Topic 4 with equal prices).
  Wealth 100; $c_1 = c_2 = 50$. She borrows 30 today and repays 30. Utility $\ln 2500$.
- **Interest rate rises to $r = 25\%$** ($p_2 = 0.8$). Wealth $20 + 0.8 \times 80 = 84$;
  $c_1 = 42$, $c_2 = 52.5$. The borrower is worse off ($42 \times 52.5 = 2205 < 2500$).
  Consumption now rises over time because $\delta(1+r) > 1$.
- **No borrowing allowed** (base case): $c_1 = 20$, $c_2 = 80$; $\mu = u'(20) - u'(80) =
  0.05 - 0.0125 = 0.0375$, the utility value of one more dollar of credit.
- **Monopoly lender** (kept from 2018, slidesI 334-336, simplified to two periods). The
  lender ($r = 0$) chooses $(c_1, c_2)$ to maximize profit $100 - c_1 - c_2$, subject to the
  client doing no worse than with no loan: $\ln c_1 + \ln c_2 \ge \ln 20 + \ln 80$. The FOCs
  give $c_1 = c_2$ (the contract smooths consumption: "when in doubt, smooth it out"). The
  participation constraint gives $c^2 = 1600$, so $c = 40$: the client borrows 20, repays 40,
  and the lender earns 20. Compared with the competitive market's $c = 50$: same smoothing,
  same efficiency, all the surplus to the lender. This replaces the 2018 three-period
  version (income $(y_0, y_1, y_2)$, $c = 42.3$).

**Part II: uncertainty** (same numbers, renamed)
- **No insurance:** expected value 50; expected utility $\tfrac12\ln 20 + \tfrac12\ln 80 =
  \ln 40$. Certainty equivalent 40, risk premium 10.
- **Fair insurance market** ($p_g = p_b = 1/2$): wealth 50; $c_g = c_b = 50$. Full insurance,
  the same numbers as the time base case.
- **Monopoly insurer:** offers a sure 40, keeps 10 in expectation. Same algebra and same
  answer as the monopoly lender.

**Part III: risk sharing** (two farmers, no insurer)
- Farmer A has (20, 80) and farmer B has (80, 20): their harvests are hit by different
  shocks. Total income is 100 in each state.
- Pareto problem: maximize $\theta\,EU_A + (1-\theta)\,EU_B$ subject to $c_{As} + c_{Bs} =
  100$ in each state $s$. FOC: $u'(c_{As})/u'(c_{Bs}) = (1-\theta)/\theta$, **the same in every
  state**. With log utility, $c_{As} = \theta \times 100$: each farmer's consumption is a fixed
  share of the total and does not depend on her own harvest. With equal weights both eat 50
  in both states: full insurance from pooling alone.
- If total income itself varies (a drought hits both), consumption still moves with the
  total: pooling insures individual shocks, not shared ones. This is the testable prediction
  in Townsend (1994) and Udry (1994).

Draft 1's drought farm ($0 or $100, $u = \sqrt{c}$) and car-insurance example
($\ln W$, maximum premium $5{,}426$) are dropped from the deck; they can go to a problem set.

## Proposed slide sequence (about 26 slides; one class)

**Opener (3)**
1. *Optimization: From Goods to Dates and States.* The table with only the Topic 4 column
   filled in. Message: same problem, renamed.
2. *Three questions*: How do we value the future? How do we value risk? What can credit,
   insurance and sharing do about each?
3. *The three Lagrangians, side by side* (above). Shown here as a preview, or held until the
   start of Part II; decide when building.

**Part I: Choice over time (NS 17), about 11 slides**
4. Goods dated by time: an apple today is a different good from an apple tomorrow.
5. Two kinds of discounting: $\delta$ (a preference) vs $p_2 = 1/(1+r)$ (a price).
6. The budget written with prices: two period budgets with saving collapse into one; the
   price form, then the present-value form. Figure: endowment (20, 80), slope $-(1+r)$.
7. Lagrangian and the Euler equation; table's dates column filled in.
8. Log utility is Cobb-Douglas: the base case with the Topic 4 formula ($c_1 = c_2 = 50$).
9. Does consumption rise over time? $\delta(1+r)$ vs 1, whatever the income path.
10. Interactive: slider on $r$, budget line rotating around the endowment (reuse Topic 4's
    `price_slider` helper).
11. An interest-rate rise: substitution vs income effect; borrower vs saver (2018 slide 325
    two-panel figure); the numbers 50/50 to 42/52.5. Callback to the wage-rise slide.
12. Permanent vs temporary income changes.
13. Credit constraints as a Kuhn-Tucker corner ($\mu = 0.0375$).
14. The monopoly lender: Lagrangian with a participation constraint; $c = 40$; same
    efficiency, different distribution. Preview of Topic 10 contracts.
15. Investment and Fisher separation; when it fails (hand-off to Topic 6).

**Part II: Choice under uncertainty (NS 7), about 8 slides**
16. Lotteries, expected value, fair games; the $490/$510 vs $0/$1000 coin toss.
17. Expected utility; concavity = risk aversion. Figure: chord vs curve, CE 40, premium 10.
18. States of the world and contingent claims (Arrow): any asset is a bundle of claims.
19. Expected-utility indifference curves: slope $\pi u'(c_g)/((1-\pi)u'(c_b))$, equal to
    $\pi/(1-\pi)$ on the certainty line; effect of changing $\pi$ (2018 figure).
20. The budget with contingent-claim prices; fair prices $p_s = \pi_s$. States column filled in.
21. Full insurance at fair prices: same numbers as slide 8, shown side by side.
22. The monopoly insurer: same answer as the monopoly lender.
23. Interactive (optional): slider on $p_g/p_b$.

**Part III: Risk sharing, about 3 slides**
24. Two farmers pooling: the Pareto problem and its FOC (above).
25. Evidence: Townsend (1994), Udry (1994): much pooling, short of full; insurance within
    networks. Index insurance take-up (Cole et al. 2013) and insurance raising risky
    investment (Karlan et al. 2014).
26. Three questions, answered: the full table. Preview of Topic 6.

## What to drop or move from the 2018 slides

- **Present bias** (slidesIIb 87, 121, 127; Thaler slides in slidesI 318-319): dropped.
- **Monopoly lender**: kept, cut from three periods to two, uses the deck's numbers.
- **Extending to T periods**: one line on slide 9, not its own slide.
- **Mathcad animations**: replaced with Plotly sliders.

## Build notes

- Figures notebook `notebooks/topic05_time_uncertainty_figures.ipynb`, same style as topic04
  (navy and amber palette, dark axes).
- Deck at `slides/05_time-and-uncertainty/deck.qmd`, with the header and `price_slider`
  helper copied from Topic 4; `source.yml` pointing at slidesI 313-336 and slidesIIb 88-120.
- Notation: we use $c_1, c_2$ and $c_g, c_b$ throughout; check NS ch. 7 and 17 and add a
  one-line note if the book uses $C_0, C_1$ or $W_g, W_b$.
- Pacing risk: two chapters in one class. If it runs long, slide 25 and the Fisher slide move
  to the start of class 10 (farm household), where they also fit.
