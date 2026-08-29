"""Single source of truth for the running example and domain.

Video 1: q = F(K, L) = A * K**ALPHA * L**BETA with A=1, ALPHA=BETA=0.5 (CRS).
Domain kept away from the axes: Cobb-Douglas isoquants are asymptotic to them
and K=0 / L=0 breaks derivatives.
"""

A = 1.0
ALPHA = 0.5
BETA = 0.5

DOM_MIN = 0.3
DOM_MAX = 9.0

# Isoquant family levels shown in the video (all interior to the domain).
QBARS = [1.0, 2.0, 3.0, 4.0]


def F(K, L, A_=A, a=ALPHA, b=BETA):
    """Output q = A K^a L^b."""
    return A_ * K**a * L**b


def K_of_L(L, qbar, A_=A, a=ALPHA, b=BETA):
    """Solve F(K,L)=qbar for K: the qbar-isoquant as a function of L."""
    return (qbar / (A_ * L**b)) ** (1.0 / a)


def dK_dL(L, qbar):
    """Slope of the isoquant K(L) at given L (negative number)."""
    K = K_of_L(L, qbar)
    return -(BETA / ALPHA) * (K / L)


def MRTS(K, L):
    """MRTS_{L,K} = F_L/F_K = (beta/alpha) * (K/L), reported positive."""
    return (BETA / ALPHA) * (K / L)
