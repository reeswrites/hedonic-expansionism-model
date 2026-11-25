"""Hedonic expansionism: three updates.
 1. Concave grief mirror (P5/P6): b*(gamma), mixed/S-shaped grief, optimal finite breadth.
 2. Soft bottleneck (P4): diminishing returns within each action -> interior, monotone x*(S).
 3. Opponent-process rebound (P4b): rebound grows with use, decays with disuse; lock-in and spacing.
"""
import numpy as np
from math import comb, log, ceil
from scipy.interpolate import RegularGridInterpolator

# ---------------------------------------------------------------- 1. grief
def Ef(n, q, f):
    """E f(X/n), X ~ Bin(n,q), exact finite sum."""
    return sum(comb(n, j) * q**j * (1 - q)**(n - j) * f(j / n) for j in range(n + 1))

def bstar(f, q=0.05, k=3, lam=2.0):
    """Bundle (k strands, bonus b, lost as a unit, grief f(1)=1 per strand-scale k)
    beats k separate sources iff k(1-q)b > lam*k*(q f(1) - E f(X/k))."""
    return lam * (q * f(1.0) - Ef(k, q, f)) / (1 - q)

def mc_check(f, b, q=0.05, k=3, lam=2.0, sims=400000, seed=0):
    rng = np.random.default_rng(seed)
    lost = rng.random(sims) < q
    vb = np.where(lost, 0, k * (1 + b)) - lam * k * f(lost.astype(float))
    ls = rng.random((sims, k)) < q
    vs = (~ls).sum(1) - lam * k * f(ls.sum(1) / k)
    return vb.mean() - vs.mean()

def part1():
    q, k, lam = 0.05, 3, 2.0
    print("=== 1. b*(gamma), f(s)=s^gamma, q=.05 k=3 lam=2  (bundle wins iff b > b*)")
    print(f"{'gamma':>6} {'b*':>9} {'MC(bundle-spread) at b=b*+.01':>30} {'E f(X/n) n=1,3,10,30':>34}")
    for gm in (0.5, 1, 1.5, 2, 3):
        f = lambda s, gm=gm: np.power(s, gm)
        b = bstar(f, q, k, lam)
        eg = " ".join(f"{Ef(n, q, f):.4f}" for n in (1, 3, 10, 30))
        print(f"{gm:>6} {b:9.4f} {mc_check(f, b + 0.01):30.4f}   {eg}")
    print("closed form check gamma=2: lam*q*(k-1)/k =", lam * q * (k - 1) / k)
    # mixed: concave for small losses, convex for large
    print("\n--- mixed grief f(s) = w*sqrt(s) + (1-w)*s^3 (concave small, convex large)")
    print(f"{'w':>5} {'b*(k=3)':>8} {'argmin_n E f(X/n), n<=40':>26} {'rare-loss n~1/argmin f(s)/s':>28}")
    s = np.linspace(1e-4, 1, 100000)
    for w in (0.0, 0.02, 0.05, 0.1, 0.2, 0.5):
        f = lambda x, w=w: w * np.sqrt(x) + (1 - w) * np.power(x, 3)
        eg = [Ef(n, q, f) for n in range(1, 41)]
        smin = s[np.argmin(f(s) / s)]
        print(f"{w:>5} {bstar(f, q, k, lam):8.4f} {int(np.argmin(eg)) + 1:>26} {1 / smin:28.1f}")
    print("\n--- logistic S-curve f(s)=(sig(c(s-m))-sig(-cm))/(sig(c(1-m))-sig(-cm)), m=.3")
    for c in (4, 8, 16):
        sg = lambda x: 1 / (1 + np.exp(-x))
        f = lambda x, c=c: (sg(c * (x - .3)) - sg(-c * .3)) / (sg(c * .7) - sg(-c * .3))
        eg = [Ef(n, q, f) for n in range(1, 41)]
        print(f"  c={c:>2}  b*={bstar(f, q, k, lam):.4f}  best n={int(np.argmin(eg)) + 1}"
              f"  E f: n=1 {eg[0]:.4f} n=3 {eg[2]:.4f} n=10 {eg[9]:.4f} n=40 {eg[39]:.4f}")

# ---------------------------------------------------------------- 2. soft bottleneck
T, DELTA, LAM, DL, KAPPA, RHO, P0 = 100, 0.97, 1.5, 0.5, 0.02, 0.3, 0.9
SMAX, LMAX = 10.0, 30.0
SG, LG = np.linspace(0, SMAX, 81), np.linspace(0, LMAX, 81)
ACTS = np.linspace(0, 1, 21)
gS = lambda S: np.exp(-0.25 * S)
pS = lambda S: P0 * np.exp(-0.25 * S)

def model(beta):
    h = lambda x: np.power(np.clip(x, 0, 1), beta)       # h(0)=0, h(1)=1: beta=1 is the old linear model
    def step(S, L, x):
        S2 = np.clip(S * (1 - RHO * h(x)), 0, SMAX)
        L2 = np.clip((1 - KAPPA) * L + DL * pS(S) * h(1 - x), 0, LMAX)
        return S2, L2
    return h, step

flow = lambda S, L: gS(S) * L - LAM * S

def ratio(S, L):
    """R = MR/ME (old single-crossing ratio; S* is where R=1)."""
    gp = -0.25 * gS(S)
    return (RHO * S * (LAM - gp * L)) / (DL * pS(S) * gS(S))

def x_greedy(S, L, beta):
    if beta >= 1: return float(ratio(S, L) > 1)
    z = ratio(S, L) ** (1 / (1 - beta))
    return z / (1 + z)

def solve_dp(step):
    SS, LL = np.meshgrid(SG, LG, indexing="ij"); V = np.zeros_like(SS); pol = []
    for t in reversed(range(T)):
        f = RegularGridInterpolator((SG, LG), V, bounds_error=False, fill_value=None)
        best = np.full_like(SS, -np.inf); arg = np.zeros_like(SS)
        for a in ACTS:
            S2, L2 = step(SS, LL, a)
            qv = flow(SS, LL) + DELTA * f(np.stack([S2, L2], -1))
            m = qv > best; best = np.where(m, qv, best); arg = np.where(m, a, arg)
        V = best; pol.append(RegularGridInterpolator((SG, LG), arg, method="nearest",
                                                     bounds_error=False, fill_value=None))
    return pol[::-1]

def rollout(step, S0, pol, L0=1.0):
    S, L, V = S0, L0, 0.0
    for t in range(T):
        x = float(pol(t, S, L)); V += DELTA**t * flow(S, L); S, L = step(S, L, x)
    return V

def part2():
    print("\n=== 2. soft bottleneck: h(x)=x^beta within each action (beta=1 is old linear)")
    Sstar = next(S for S in np.linspace(.01, SMAX, 5000) if ratio(S, 1.0) > 1)
    print(f"old threshold S*(L=1) = {Sstar:.2f}  (R=MR/ME=1 there)")
    Ss = (0.5, 1, Sstar, 3, 5, 8)
    print(f"{'beta':>5} | x*(S) greedy closed form at S=" + " ".join(f"{s:4.2f}" for s in Ss)
          + " | DP x*(t=0,L=1) same S | V(S0=8): opt  greedy  bangbang | V(S0=3)")
    for beta in (1.0, 0.9, 0.7, 0.5):
        h, step = model(beta); pol = solve_dp(step)
        xg = " ".join(f"{x_greedy(s, 1.0, beta):4.2f}" for s in Ss)
        xs = np.array([pol[0]([[s, 1.0]])[0] for s in SG]); viol = int((np.diff(xs) < -1e-9).sum())
        cross = SG[np.argmax(xs >= 0.5)]
        xd = " ".join(f"{pol[0]([[s, 1.0]])[0]:4.2f}" for s in Ss)
        P = {"opt": lambda t, S, L: pol[t]([[S, L]])[0],
             "greedy": lambda t, S, L: x_greedy(S, L, beta),
             "bang": lambda t, S, L: x_greedy(S, L, 1.0)}
        v8 = [rollout(step, 8.0, P[k]) for k in P]; v3 = [rollout(step, 3.0, P[k]) for k in P]
        print(f"{beta:>5} | {xg} | {xd} | {v8[0]:6.1f} {v8[1]:6.1f} {v8[2]:6.1f} |"
              f" {v3[0]:6.1f} {v3[1]:6.1f} {v3[2]:6.1f} | DP monotone violations {viol}, DP x*=1/2 at S={cross:.2f}")

# ---------------------------------------------------------------- 3. opponent-process rebound
TH, RN, D, MU, PSI, RC = 2.0, 0.5, 0.03, 0.15, 0.05, 0.25
C = 1 - (1 - RN) * (1 - D)                 # old loop condition: r >= TH*C

SHOCK, PER = 3.0, 10      # recurring life stressors: S += SHOCK every PER periods

def sim3(S0, r0, g, eps, policy, m=1, T3=150, clean=False, shock=SHOCK):
    """policy: 'nothing' | 'habit' (numb iff S>TH) | 'stop' (numb iff S>TH and it cannot
    lock in: r0*a_next < TH*C) | 'spaced' (numb iff S>TH and >= m periods since last use).
    Not numbing -> clean relief if clean and S>TH, else expand liking."""
    S, L, c, a, V, pend, last, uses = S0, 1.0, 1.0, 0.0, 0.0, 0.0, -10**9, 0
    for t in range(T3):
        S += pend + (shock if t > 0 and t % PER == 0 else 0.0); pend = 0.0
        V += DELTA**t * (gS(S) * c * L - LAM * S)
        a_next_use = (1 - eps) * a + g
        use = S > TH and (policy == "habit" or
                          (policy == "stop" and r0 * a_next_use < TH * C) or
                          (policy == "spaced" and t - last >= m))
        if use:
            S -= RN * S; c *= 1 - MU; a = a_next_use; pend = r0 * a; last = t; uses += 1
        else:
            a = (1 - eps) * a
            if clean and S > TH: S -= RC * S
            else: L += DL * pS(S) * c
        S -= D * S; c += PSI * (1 - c)
    return V, uses, a

def lockin_t(r0, g, eps, T3=150):
    """start of the final unbroken run of uses under habit (None if the run doesn't reach T3)."""
    S, a, pend, run_start, prev = 8.0, 0.0, 0.0, None, False
    for t in range(T3):
        S += pend + (SHOCK if t > 0 and t % PER == 0 else 0.0); pend = 0.0
        use = S > TH
        if use:
            if not prev: run_start = t
            S -= RN * S; a = (1 - eps) * a + g; pend = r0 * a
        else: a = (1 - eps) * a
        S -= D * S; prev = use
    return run_start if prev else None

def m_min(r0, g, eps):
    """smallest spacing m with r0*g/(1-(1-eps)^m) < TH*C (peak rebound cannot re-trigger)."""
    x = 1 - r0 * g / (TH * C)
    if x <= 0: return np.inf
    if eps >= 1: return 1
    return max(1, ceil(log(x) / log(1 - eps) + 1e-12))

def part3():
    print(f"\n=== 3. growing rebound r_t=r0*a_t, a'=(1-eps)a+g*used.  TH*C={TH*C:.3f}")
    print(f"lock-in check (habit, S0=8, shocks +{SHOCK} every {PER}): loop permanent iff r0*g/eps > TH*C")
    print(f"{'r0':>4} {'g':>4} {'eps':>5} {'r0g/eps':>7} {'perm?':>5} {'uses/150':>8} {'a_end':>6} {'g/eps':>5} {'m_min':>5} {'first t of last unbroken run':>28}")
    cases = [(0.5, 1, 1), (1.2, 1, 1), (0.5, 0.3, 0.3), (0.5, 0.3, 0.05), (0.5, 0.2, 0.03),
             (0.6, 0.6, 0.2)]          # (r0,1,1) = old constant-rebound model
    for r0, g, eps in cases:
        V, u, a = sim3(8, r0, g, eps, "habit"); lock = lockin_t(r0, g, eps)
        print(f"{r0:>4} {g:>4} {eps:>5} {r0*g/eps:7.2f} {str(r0*g/eps > TH*C):>5} {u:8d} {a:6.2f} {g/eps:5.2f} {m_min(r0, g, eps):>5} {str(lock):>28}")
    print("\nvalue, S0=8 (no clean relief | with clean relief available)")
    print(f"{'r0':>4} {'g':>4} {'eps':>5} {'m_min':>5} | {'nothing':>7} {'habit':>7} {'stop':>7} {'spaced':>7} {'sp m=1':>7} | "
          f"{'clean':>7} {'habit':>7} {'stop':>7} {'spaced':>7}")
    for r0, g, eps in cases:
        mm = m_min(r0, g, eps); ms = 10**6 if mm == np.inf else mm
        row = [sim3(8, r0, g, eps, "nothing")[0], sim3(8, r0, g, eps, "habit")[0],
               sim3(8, r0, g, eps, "stop")[0], sim3(8, r0, g, eps, "spaced", ms)[0],
               sim3(8, r0, g, eps, "spaced", 1)[0]]
        rc = [sim3(8, r0, g, eps, "nothing", clean=True)[0], sim3(8, r0, g, eps, "habit", clean=True)[0],
              sim3(8, r0, g, eps, "stop", clean=True)[0], sim3(8, r0, g, eps, "spaced", ms, clean=True)[0]]
        print(f"{r0:>4} {g:>4} {eps:>5} {str(mm):>5} | " + " ".join(f"{v:7.1f}" for v in row)
              + " | " + " ".join(f"{v:7.1f}" for v in rc))
    print("\nspacing sweep r0=.5 g=.3 eps=.05 (m_min=%s): m, V(no clean), V(clean fallback), uses, a*(m)" % m_min(.5, .3, .05))
    for m in (1, 2, 3, 4, 6, 10, 20):
        V, u, a = sim3(8, .5, .3, .05, "spaced", m); Vc = sim3(8, .5, .3, .05, "spaced", m, clean=True)[0]
        print(f"  m={m:>2} V={V:7.1f} Vclean={Vc:7.1f} uses={u:3d} a*(m)={.3/(1-.95**m):.2f}  r0*a*={.5*.3/(1-.95**m):.2f}")

if __name__ == "__main__":
    part1(); part3(); part2()
