---
title: deck
description: "ECO 701 Topic 3: Production Optimization"
author: "Jonathan Conning"
deploy: true
marp: true
math: katex
paginate: true
theme: eco701
size: 16:9
footer: 'Eco 701 - Micro Theory'
---

<!-- _class: divider -->

# Part I
# Production Technology and Cost Minimization

The production function, isoquants, and the Method of Lagrange applied to a firm's cost-minimizing choice of inputs

---

## The Production Function

A firm's production function gives the maximum output attainable from any combination of inputs — here capital $K$ and labor $L$:

$$q = F(K,L)$$

- $F(K,L)$ is the *maximum* amount of the good producible using $K$ units of capital and $L$ units of labor — anything less than the max is technically inefficient and never optimal to choose

---

## Marginal Physical Product

$$MP_K = \frac{\partial q}{\partial K} = F_K(K,L) \qquad\qquad MP_L = \frac{\partial q}{\partial L} = F_L(K,L)$$

- The additional output from employing one more unit of an input, holding the other input constant

---

## Diminishing Marginal Productivity

$$\frac{\partial MP_K}{\partial K} = F_{KK} < 0 \qquad\qquad \frac{\partial MP_L}{\partial L} = F_{LL} < 0 \qquad\qquad \frac{\partial MP_L}{\partial K} = F_{LK} > 0$$

- We generally assume diminishing marginal productivity in each input — it implies a downward-sloping demand for factors
- $F_{LK} > 0$: capital and labor are **complements** in most production functions — more of one raises the marginal product of the other

---

## Production Technology vs. Production Technique

- A **production technology** is like a recipe book — the full set of available techniques for producing any amount $q$ of output
- A **production technique** is like a single recipe: e.g. "combine 20 units of $K$ and 10 units of $L$" to make $q=10$ widgets
- An **isoquant map** summarizes the technology; a point on an isoquant is a technique

---

## From Discrete Techniques to a Smooth Isoquant

![center width:560](media/discrete-techniques-isoquant.png)

- A firm choosing between discrete techniques (1, 2, 3) can achieve any point *between* them by combining two techniques — e.g. technique 4 blends 2 and 3 — tracing out a convex isoquant

---

## The Smooth-Substitutability Assumption

![center width:560](media/smooth-isoquant-assumption.png)

- Economists often assume the full recipe book is known and smoothly substitutable, so the optimal technique depends only on factor prices
- More realistically, firms must *search and adapt* to reach a new technique — costly, and some firms are better at it than others

---

## The Isoquant Map

![center width:520](media/isoquant-map.png)

- Each isoquant represents a different output level — output rises moving northeast

---

## The Marginal Rate of Technical Substitution (RTS)

![center width:520](media/rts-diagram.png)

$$F(K,L) = \bar q \qquad\Longrightarrow\qquad F_K\,dK + F_L\,dL = 0 \qquad\Longrightarrow\qquad \frac{dK}{dL} = -\frac{F_L}{F_K}$$

- The slope of an isoquant is the **RTS** — the rate at which $L$ substitutes for $K$ holding output fixed. $RTS>0$ and diminishes as labor input increases

---

## Cost Minimization

Assume the firm has already chosen its output level $q$ and wants to produce it as cheaply as possible:

- Minimizing cost is a prerequisite for maximizing profit — a profit-maximizing firm never overpays for a given output
- Choosing $K$ and $L$ to minimize the cost of producing $q$ leads to a **derived demand** for each input, and from that a cost function $C(q)$

---

## Isocost Lines

![center width:460](media/isocost-tangency.png)

$$C = wL + rK \qquad\Longrightarrow\qquad K = \frac{C}{r} - \frac{w}{r}L$$

- Costs are represented by parallel **isocost lines** with slope $-w/r$ — higher lines mean higher total cost

---

## The Cost-Minimizing Choice

![center width:520](media/cost-minimizing-choice.png)

- The minimum cost of producing $q_0$ occurs at the **tangency** between the isoquant and the lowest attainable isocost line — the optimal choice is $(L^*, K^*)$

---

## The Expansion Path

![center width:480](media/expansion-path.png)

- The **expansion path** is the locus of cost-minimizing tangencies as output rises — it traces out how input use grows with $q$, and the minimum cost at each $q$ is exactly $TC(q)$

---

## Solving It: The Lagrangian

Minimize total cost given $F(K,L) = q_0$:

$$L(K,L,\lambda) = wL + vK + \lambda\big[q_0 - F(K,L)\big]$$

First-order conditions:

$$\frac{\partial L}{\partial L} = w - \lambda F_L = 0 \qquad \frac{\partial L}{\partial K} = v - \lambda F_K = 0 \qquad \frac{\partial L}{\partial \lambda} = q_0 - F(K,L) = 0$$

---

## The Tangency Condition

Dividing the first two FOCs:

$$\frac{w}{v} = \frac{F_L}{F_K} = \frac{MP_L}{MP_K} = RTS(L \text{ for } K)$$

Cross-multiplying instead:

$$\frac{F_K}{v} = \frac{F_L}{w}$$

- The firm equates the RTS to the ratio of factor prices — marginal productivity per dollar spent must be equal across inputs

---

## The Multiplier as Marginal Cost

$$\frac{w}{F_L} = \frac{v}{F_K} = \lambda$$

- Each side is dollars spent per extra unit of output from that input — $\left(\frac{\$/L}{q/L}\right) \to \left(\frac{\$}{L}\right)\cdot\left(\frac{L}{q}\right) \to \left(\frac{\$}{q}\right)$, i.e. dollars **per unit of output**
- $\lambda$ is exactly the **marginal cost** of output: how much extra cost is incurred by relaxing the output constraint slightly

---

## Derived Demand and the Cost Function

Solving the FOCs and the constraint together gives the **derived demand** for each input:

$$L^*(w,v,q_0) \qquad\qquad K^*(w,v,q_0)$$

Substituting back into the objective gives the **cost function**:

$$C(v,w,q) = \min_{K,L} \; vK + wL \quad\text{s.t.}\quad F(K,L) = q$$

$$\Longrightarrow\qquad C(v,w,q) = vK^*(w,v,q) + wL^*(w,v,q)$$

- Exactly analogous to the expenditure function $E(p_1,p_2,U)$ from consumer theory — plug the derived demands back into the objective

---

## Average and Marginal Cost

$$\text{average cost} = AC(v,w,q) = \frac{C(v,w,q)}{q}$$

$$\text{marginal cost} = MC(v,w,q) = \frac{\partial C(v,w,q)}{\partial q}$$

---

## Cobb-Douglas: Derived Demand and Cost Function

For $F(K,L) = K^\alpha L^\beta$, the tangency condition $\frac{w}{v} = \frac{F_L}{F_K} = \frac{\beta}{\alpha}\frac{K}{L}$ gives $K = \frac{\alpha}{\beta}\frac{w}{v}L$. Substituting into $F(K,L)=q$ and solving:

$$L^* = q^{\frac{1}{\alpha+\beta}}\left(\frac{\beta}{\alpha}\right)^{\frac{\alpha}{\alpha+\beta}} v^{\alpha/(\alpha+\beta)} w^{-\alpha/(\alpha+\beta)} \qquad K^* = q^{\frac{1}{\alpha+\beta}}\left(\frac{\alpha}{\beta}\right)^{\frac{\beta}{\alpha+\beta}} v^{-\beta/(\alpha+\beta)} w^{\beta/(\alpha+\beta)}$$

Substituting back:

$$C(v,w,q) = B\, q^{\frac{1}{\alpha+\beta}} v^{\frac{\alpha}{\alpha+\beta}} w^{\frac{\beta}{\alpha+\beta}}, \qquad B = (\alpha+\beta)\,\alpha^{-\alpha/(\alpha+\beta)}\beta^{-\beta/(\alpha+\beta)}$$

- With $\alpha+\beta=1$ (constant returns to scale), cost is exactly **linear** in $q$ — the case examined next
