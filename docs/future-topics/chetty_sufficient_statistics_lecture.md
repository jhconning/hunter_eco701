# Lecture: The Envelope Theorem in Action — Sufficient Statistics & Optimal Policy

**Course:** ECO 701 (Microeconomic Theory)  
**Topic:** How Micro Theory Frames Empirical Analysis (The Baily-Chetty Sufficient Statistics Approach)  
**Core Tool:** The Envelope Theorem applied to Social Welfare and Policy Evaluation

---

## 1. Pedagogical Motivation: The Two Poles of Applied Economics

In modern economics, there has long been a methodological divide between two distinct paradigms:

```
┌─────────────────────────────────────────┐             ┌─────────────────────────────────────────┐
│       1. FULLY STRUCTURAL MODELS        │             │     2. REDUCED-FORM CAUSAL INFERENCE    │
│                                         │             │                                         │
│ • Specify deep utility u(c, l; θ) and   │             │ • Use quasi-experiments (Diff-in-Diff,  │
│   production primitives.                │             │   RCTs, Regression Discontinuity).      │
│ • Estimate deep parameters θ.           │             │ • Identify causal treatment effects β.  │
│ • Simulate counterfactual policies.     │             │                                         │
│                                         │             │                                         │
│ [PRO]: Can make normative statements    │             │ [PRO]: Transparent, credible causal     │
│        about optimal policy.            │             │        identification.                  │
│ [CON]: Results highly sensitive to      │             │ [CON]: Cannot answer: "Is current       │
│        arbitrary functional forms.      │             │        benefit level optimal?"          │
└────────────────────┬────────────────────┘             └────────────────────┬────────────────────┘
                     │                                                       │
                     └──────────────────► ┌────────────────────────────────┐ ◄┘
                                          │  CHETTY'S SUFFICIENT           │
                                          │  STATISTICS APPROACH (2009)    │
                                          │                                │
                                          │ • Uses the Envelope Theorem to │
                                          │   derive policy rules in terms │
                                          │   of high-level elasticities.  │
                                          └────────────────────────────────┘
```

**The Central Question:** Can we determine the **optimal policy** (e.g., optimal tax rate $\tau^*$, optimal unemployment benefit $b^*$) using transparent reduced-form elasticities, *without* having to specify and estimate every unobservable parameter of the utility function?

**Raj Chetty's Answer (2009):** Yes. By exploiting the **Envelope Theorem**, private behavioral responses cancel out to the first order, allowing marginal welfare changes to be expressed as a function of **empirically observable sufficient statistics**.

---

## 2. Theoretical Foundations: Why the Envelope Theorem is the Magic Engine

Consider an agent who chooses an action $x \in \mathbb{R}^k$ (e.g., labor supply, job search effort, consumption) to maximize private utility subject to a policy variable $t$ (e.g., a tax rate or insurance benefit):

$$V(t) = \max_x u(x, t) \quad \text{s.t.} \quad g(x, t) \le 0$$

Let the Lagrangian be $\mathcal{L}(x, \lambda, t) = u(x, t) - \lambda g(x, t)$. At the interior optimum $x^*(t)$, the first-order condition requires:

$$\nabla_x \mathcal{L} = \nabla_x u(x^*, t) - \lambda \nabla_x g(x^*, t) = \mathbf{0}$$

Now, consider the total derivative of the agent's optimized welfare $V(t)$ with respect to policy $t$:

$$\frac{dV}{dt} = \underbrace{\left[ \nabla_x u(x^*, t) - \lambda \nabla_x g(x^*, t) \right]}_{= \mathbf{0} \text{ by FOC}} \cdot \frac{dx^*}{dt} + \left( \frac{\partial u}{\partial t} - \lambda \frac{\partial g}{\partial t} \right)$$

$$\implies \frac{dV}{dt} = \left. \frac{\partial \mathcal{L}}{\partial t} \right|_{x=x^*(t)}$$

### The Crucial Economic Implication
* When policy $t$ changes, the agent changes their behavior ($\frac{dx^*}{dt} \neq 0$).
* However, because the agent was already optimizing, this behavioral change has **zero first-order effect on their private utility**.
* **Why behavioral responses matter for society:** The behavioral response $\frac{dx^*}{dt}$ only impacts social welfare to the extent that it creates a **Fiscal Externality** on the government's budget constraint!

---

## 3. The Worked Model: The Baily-Chetty Optimal Unemployment Insurance

Let us apply this logic to one of the most celebrated models in modern public economics: the optimal design of unemployment insurance (Baily 1978; Chetty 2006, 2008, 2009).

### A. Environment & Setup
* **States of Nature:**
  * **Employed ($E$):** The worker earns wage $w$ and pays tax $\tau$. Consumption is:
    $$c_e = w - \tau$$
  * **Unemployed ($U$):** The worker receives government benefit $b$. Consumption is:
    $$c_u = b$$
* **Worker's Choice (Search Effort):**
  * The worker chooses search effort $e \in (0, 1)$, which represents the probability of finding a job.
  * Searching requires effort cost $\psi(e)$, where $\psi'(e) > 0$ and $\psi''(e) > 0$.
  * Utility function $u(c)$ exhibits risk aversion ($u'(c) > 0, u''(c) < 0$).

### B. The Worker's Optimization Problem
Given policy $(b, \tau)$, the worker chooses $e$ to maximize expected utility:

$$\max_{e \in (0, 1)} \quad \mathcal{U}(e; b, \tau) = e \cdot u(w - \tau) + (1-e) \cdot u(b) - \psi(e)$$

**First-Order Condition with respect to effort $e$:**
$$\frac{\partial \mathcal{U}}{\partial e} = \left[ u(w - \tau) - u(b) \right] - \psi'(e) = 0$$

$$\implies \psi'(e^*(b, \tau)) = u(c_e) - u(c_u)$$

*Intuition:* The worker exerts effort until the marginal cost of effort $\psi'(e)$ equals the net utility gain from finding a job vs. remaining on UI ($u(c_e) - u(c_u)$).

### C. The Government's Budget Constraint
The government must balance its budget in expectation:

$$\underbrace{e \cdot \tau}_{\text{Tax Revenue}} = \underbrace{(1-e) \cdot b}_{\text{Benefit Payouts}}$$

$$\implies \tau(b, e) = \frac{1-e}{e} b$$

---

## 4. Social Welfare Maximization & The Baily-Chetty Formula

The social planner chooses benefit $b$ to maximize the worker's expected utility, recognizing that taxes $\tau(b)$ must adjust to balance the budget:

$$\max_b \quad W(b) = e^*(b) u(w - \tau(b)) + (1-e^*(b)) u(b) - \psi(e^*(b))$$

### Step 1: Differentiate Social Welfare $W(b)$ with respect to $b$
$$\frac{dW}{db} = \underbrace{\left[ u(c_e) - u(c_u) - \psi'(e) \right]}_{= 0 \text{ by Worker's FOC (Envelope Theorem!)}} \cdot \frac{de^*}{db} + (1-e^*) u'(c_u) - e^* u'(c_e) \frac{d\tau}{db}$$

$$\frac{dW}{db} = (1-e^*) u'(c_u) - e^* u'(c_e) \frac{d\tau}{db}$$

### Step 2: Differentiate the Government Budget Constraint
Differentiating $e \tau = (1-e) b$ with respect to $b$:

$$e \frac{d\tau}{db} + \tau \frac{de}{db} = (1-e) - b \frac{de}{db}$$

$$e \frac{d\tau}{db} = (1-e) - (b + \tau) \frac{de}{db}$$

### Step 3: Substitute $e \frac{d\tau}{db}$ back into $\frac{dW}{db}$
$$\frac{dW}{db} = (1-e) u'(c_u) - u'(c_e) \left[ (1-e) - (b + \tau) \frac{de}{db} \right]$$

Divide the entire equation by $(1-e) u'(c_e)$:

$$\frac{1}{(1-e) u'(c_e)} \frac{dW}{db} = \underbrace{\frac{u'(c_u) - u'(c_e)}{u'(c_e)}}_{\text{Marginal Value of Insurance (Consumption Smoothing)}} + \underbrace{\frac{b + \tau}{1-e} \frac{de}{db}}_{\text{Marginal Cost of Moral Hazard (Fiscal Externality)}}$$

### Step 4: Express the Moral Hazard Term as an Elasticity
Notice that:
$$\frac{b + \tau}{1-e} = \frac{b + \frac{1-e}{e}b}{1-e} = \frac{b \left(1 + \frac{1-e}{e}\right)}{1-e} = \frac{b \left(\frac{1}{e}\right)}{1-e} = \frac{b}{e (1-e)}$$

Define the **elasticity of the unemployment rate ($u_r = 1-e$) with respect to the benefit level $b$**:
$$\varepsilon_{u_r, b} = \frac{d(1-e)}{db} \frac{b}{1-e} = - \frac{de}{db} \frac{b}{1-e}$$

Substituting this into our welfare equation:
$$\frac{b + \tau}{1-e} \frac{de}{db} = - \frac{1}{e} \varepsilon_{u_r, b}$$

Setting $\frac{dW}{db} = 0$ for the optimal benefit $b^*$, we obtain the exact **Baily-Chetty Condition**:

$$\boxed{\frac{u'(c_u) - u'(c_e)}{u'(c_e)} = \frac{\varepsilon_{u_r, b}}{e}}$$

---

## 5. The Taylor Approximation: The "Sufficient Statistics" Representation

Using a second-order Taylor expansion of $u(c_u)$ around $c_e$:
$$u'(c_u) \approx u'(c_e) + u''(c_e)(c_u - c_e) = u'(c_e) - u''(c_e)(c_e - c_u)$$

$$\frac{u'(c_u) - u'(c_e)}{u'(c_e)} \approx - \frac{u''(c_e) c_e}{u'(c_e)} \cdot \frac{c_e - c_u}{c_e} = \gamma \cdot \frac{\Delta c}{c_e}$$

where:
* $\gamma = - \frac{c_e u''(c_e)}{u'(c_e)}$ is the **Coefficient of Relative Risk Aversion**.
* $\frac{\Delta c}{c_e} = \frac{c_e - c_u}{c_e}$ is the **percentage drop in consumption upon becoming unemployed**.

This yields the iconic **Baily-Chetty Sufficient Statistics Formula**:

$$\boxed{\underbrace{\gamma \cdot \frac{\Delta c}{c_e}}_{\text{Social Benefit of Insurance}} = \underbrace{\frac{\varepsilon_{u_r, b}}{e}}_{\text{Social Cost of Moral Hazard}}}$$

### Why this is a revolutionary bridge:
To test whether the existing unemployment benefit $b$ is optimal, the policy economist does **NOT** need to write down or calibrate a complex structural model of search costs $\psi(e)$. They only need to estimate three empirical numbers:
1. $\frac{\Delta c}{c_e}$: Estimated directly from household survey data (e.g., PSID or bank transaction data).
2. $\varepsilon_{u_r, b}$: Estimated from a state-level policy change in UI benefits using Diff-in-Diff or Regression Discontinuity.
3. $\gamma$: Taken from standard micro estimates of risk aversion ($\approx 1$ to $3$).

---

## 6. Numerical Simulation & Interactive Jupyter Notebook Architecture

To prove to students that this theoretical formula matches the true optimum of a structural model, we implement the full structural model in Python.

### Simulation Specifications:
* **Utility:** CRRA utility $u(c) = \frac{c^{1-\gamma}}{1-\gamma}$ (or $\ln(c)$ if $\gamma=1$).
* **Effort Cost:** $\psi(e) = \frac{k}{1+\theta} e^{1+\theta}$ (e.g. quadratic $\theta=1$).
* **Parameters:** $w = 100$, $k = 80$, $\gamma = 2.0$.

See accompanying interactive notebook: `notebooks/topic13_chetty_sufficient_statistics.ipynb`.

---

## 7. Classroom Discussion Questions & Problem Set Exercises

1. **The Role of Liquidity vs. Moral Hazard (Chetty 2008):**
   * *Question:* What if the duration elasticity $\varepsilon_{u_r, b}$ is driven by **liquidity constraints** (workers need money to pay rent while searching for a well-matched job) rather than **moral hazard** (workers slacking off)?
   * *Discussion:* Chetty (2008, *JPE*) showed that if UI acts as liquidity, the fiscal externality is much smaller, justifying even higher UI benefits!
2. **Private Savings & Intertemporal Choice:**
   * *Exercise:* If workers can self-insure through precautionary savings $s$ (connecting back to Lecture 7), how does the consumption drop $\frac{\Delta c}{c_e}$ change? Why does the sufficient statistics formula still hold?
3. **The Carbon Tax Analog:**
   * *Exercise:* How does the Envelope Theorem apply to calculating the deadweight loss and optimal rate of a Pigouvian Carbon Tax (Lecture 9)? What is the "fiscal externality" in that context?
