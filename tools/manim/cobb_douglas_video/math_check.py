"""Symbolic verification of every formula shown on screen (PLAN.md §7 gate)."""
import sympy as sp

K, L, t, A, a, b, qb, m = sp.symbols("K L t A alpha beta qbar m", positive=True)
F = A * K**a * L**b

checks = []

def check(name, expr_true):
    ok = bool(sp.simplify(expr_true))
    checks.append((name, ok))
    print(f"{'PASS' if ok else 'FAIL'}  {name}")

# S1: profit warm-up  pi(q) = 10q - 10 - q^2, q* = 5, SOC < 0
q = sp.Symbol("q")
pi = 10 * q - 10 - q**2
qstar = sp.solve(sp.diff(pi, q), q)[0]
check("S1: FOC gives q* = 5", sp.Eq(qstar, 5))
check("S1: SOC pi'' = -2 < 0", sp.diff(pi, q, 2) < 0)
g = q**2 - 10 * q + 20
check("S1: counterexample min at x=5 (g''>0)",
      sp.Eq(sp.solve(sp.diff(g, q), q)[0], 5) and sp.diff(g, q, 2) > 0)

# S2: homogeneity F(tK,tL) = t^(a+b) F(K,L)
check("S2: homogeneity of degree a+b",
      sp.Eq(sp.simplify(F.subs({K: t * K, L: t * L})), sp.simplify(t**(a + b) * F)))
Fex = sp.sqrt(K * L)
check("S2: F(1,4)=2 and F(2,8)=4 (CRS check)",
      sp.Eq(Fex.subs({K: 1, L: 4}), 2) and sp.Eq(Fex.subs({K: 2, L: 8}), 4))

# S3: slice at K=4 -> q = 2 sqrt(L), MP_L = dq/dL = 1/sqrt(L) diminishing
slice_q = Fex.subs(K, 4)
check("S3: slice K=4 is 2*sqrt(L)", sp.Eq(slice_q, 2 * sp.sqrt(L)))
MPL = sp.diff(slice_q, L)
check("S3: MP_L = 1/sqrt(L) > 0, decreasing",
      sp.Eq(MPL, 1 / sp.sqrt(L)) and sp.simplify(sp.diff(MPL, L)) < 0)
# code used m = 0.5*F(4,L)/L for the tangent slope
check("S3: tangent slope formula 0.5*q/L equals dq/dL",
      sp.Eq(sp.simplify(sp.Rational(1, 2) * slice_q / L), MPL))

# S4: isoquant K(L) = qbar^2 / L solves sqrt(KL) = qbar
check("S4: isoquant closed form", sp.Eq(Fex.subs(K, qb**2 / L), qb))

# S5: partials, tidy forms, MRTS
FK, FL = sp.diff(F, K), sp.diff(F, L)
check("S5: F_K = a*A*K^(a-1)*L^b = a*q/K", sp.Eq(sp.simplify(FK), sp.simplify(a * F / K)))
check("S5: F_L = b*A*K^a*L^(b-1) = b*q/L", sp.Eq(sp.simplify(FL), sp.simplify(b * F / L)))
MRTS = sp.simplify(FL / FK)
check("S5: MRTS = (b/a)(K/L)", sp.Eq(MRTS, (b / a) * (K / L)))
# implicit slope along isoquant equals -MRTS
Kiso = qb**2 / L
slope = sp.diff(Kiso, L)
check("S5: dK/dL along isoquant = -K/L (a=b case)",
      sp.Eq(sp.simplify(slope), sp.simplify(-(Kiso / L))))
check("S5: readout MRTS = K/L = qbar^2/L^2 (4 at L=2, 0.25 at L=8, qbar=4)",
      sp.Eq((Kiso / L).subs({qb: 4, L: 2}), 4)
      and sp.Eq((Kiso / L).subs({qb: 4, L: 8}), sp.Rational(1, 4)))
# diminishing MRTS along the isoquant
check("S5: MRTS falls along isoquant", sp.simplify(sp.diff(Kiso / L, L)) < 0)

# S6: homotheticity — MRTS invariant to scaling; crossings; stub slope
check("S6: MRTS(tK,tL) = MRTS(K,L)",
      sp.Eq(sp.simplify(MRTS.subs({K: t * K, L: t * L})), MRTS))
Lcross = sp.solve(sp.Eq(m * L, qb**2 / L), L)[0]
check("S6: ray-isoquant crossing at L = qbar/sqrt(m)", sp.Eq(Lcross, qb / sp.sqrt(m)))
check("S6: slope at crossing = -m (parallel stubs)",
      sp.Eq(sp.simplify(slope.subs(L, Lcross)), -m))
# general theorem: partials of degree-r homogeneous F are homogeneous of degree r-1
r = a + b
check("S6: F_K homogeneous of degree r-1",
      sp.Eq(sp.simplify(FK.subs({K: t * K, L: t * L})), sp.simplify(t**(r - 1) * FK)))

n_fail = sum(1 for _, ok in checks if not ok)
print(f"\n{len(checks) - n_fail}/{len(checks)} checks passed")
raise SystemExit(1 if n_fail else 0)
