"""Hedonic expansionism, claim P4 ("find the bottleneck"): relief vs expansion sequencing.

State (S, L): S >= 0 suffering, L = effective liking stock (sum l_i h_i u_i).
Per period effort 1 split r (relief) / 1-r (expansion).
  S' = S * (1 - rho * r) + sigma               (proportional relief: phi(S) = rho*S, phi(0)=0)
  L' = (1-kappa) L + Delta * p(S) * (1-r)      (expected expansion; kappa = habituation, keeps baseline bounded)
  [behavioral-activation variant: S' also reduced by psi * S * (1-r)]
Flow u = g(S) L - lam S;  V = sum_t delta^t u_t.
Policies: DP-optimal, greedy (myopic marginal rule = theorem), relief-first, expansion-first, fixed 50/50.
"""
import numpy as np
from scipy.interpolate import RegularGridInterpolator

T, DELTA, LAM, DELTA_L, KAPPA, RHO, P0 = 100, 0.97, 1.5, 0.5, 0.02, 0.3, 0.9
SMAX, LMAX = 10.0, 30.0
SG = np.linspace(0, SMAX, 121)
LG = np.linspace(0, LMAX, 121)
ACTS = np.linspace(0, 1, 11)

def lin(k):  return lambda S: np.clip(1 - k * S, 0.0, 1.0)
def expo(k): return lambda S: np.exp(-k * S)
def sig(k, s0):
    c = 1 + np.exp(-k * s0)
    return lambda S: c / (1 + np.exp(k * (S - s0)))

SHAPES = {
    "linear":  (lin(0.09),      lin(0.09)),
    "exp":     (expo(0.25),     expo(0.25)),
    "sigmoid": (sig(1.2, 4.0),  sig(1.2, 4.0)),
}

def make_model(g, pshape, rho=RHO, psi=0.0, sigma=0.0):
    p = lambda S: P0 * pshape(S)
    def step(S, L, r):
        S2 = np.clip(S * (1 - rho * r) - psi * S * (1 - r) + sigma, 0, SMAX)
        L2 = np.clip((1 - KAPPA) * L + DELTA_L * p(S) * (1 - r), 0, LMAX)
        return S2, L2
    flow = lambda S, L: g(S) * L - LAM * S
    return dict(g=g, p=p, step=step, flow=flow, rho=rho, psi=psi)

def solve_dp(m):
    SS, LL = np.meshgrid(SG, LG, indexing="ij")
    V = np.zeros_like(SS); pol = []
    for t in reversed(range(T)):
        f = RegularGridInterpolator((SG, LG), V, bounds_error=False, fill_value=None)
        best = np.full_like(SS, -np.inf); barg = np.zeros_like(SS)
        for a in ACTS:
            S2, L2 = m["step"](SS, LL, a)
            q = m["flow"](SS, LL) + DELTA * f(np.stack([S2, L2], -1))
            better = q > best; best = np.where(better, q, best); barg = np.where(better, a, barg)
        V = best; pol.append(RegularGridInterpolator((SG, LG), barg, method="nearest",
                                                      bounds_error=False, fill_value=None))
    return pol[::-1]

def greedy_r(m, S, L, h=1e-4):
    """Theorem's marginal rule: relief iff MR(S,L) > ME(S,L)."""
    g = m["g"]; gp = (g(S + h) - g(max(S - h, 0))) / (S + h - max(S - h, 0))
    MR = (m["rho"] * S - m["psi"] * 0) * (LAM - gp * L)          # phi(S) * (lam + L|g'|)
    ME = DELTA_L * m["p"](S) * g(S) + m["psi"] * S * (LAM - gp * L)  # expansion (+ BA relief)
    return 1.0 if MR > ME else 0.0

def rollout(m, S0, policy, L0=1.0):
    S, L, V, rs = S0, L0, 0.0, []
    for t in range(T):
        r = float(policy(t, S, L)); rs.append(r)
        V += DELTA ** t * m["flow"](S, L)
        S, L = m["step"](S, L, r)
    return V, np.array(rs), S, L

def policies(m, pol):
    return {
        "optimal":   lambda t, S, L: pol[t]([[S, L]])[0],
        "greedy":    lambda t, S, L: greedy_r(m, S, L),
        "reliefFst": lambda t, S, L: 1.0 if S > 0.1 else 0.0,
        "expandFst": lambda t, S, L: 0.0 if t < T // 2 else 1.0,
        "fixed50":   lambda t, S, L: 0.5,
    }

def threshold(m, L=1.0):
    for S in np.linspace(0.001, SMAX, 5000):
        if greedy_r(m, S, L) == 1.0: return S
    return np.inf

def run(label, m):
    pol = solve_dp(m)
    print(f"\n=== {label} | greedy S*(L=1)={threshold(m,1.0):.2f}  S*(L=10)={threshold(m,10.0):.2f}")
    print(f"{'S0':>4} {'policy':>10} {'V':>9}  r_t at t=0,2,5,10,20,40,80   S_end  L_end")
    for S0 in (8.0, 3.0, 0.5):
        for name, f in policies(m, pol).items():
            V, rs, S, L = rollout(m, S0, f)
            sel = " ".join(f"{rs[i]:.1f}" for i in (0, 2, 5, 10, 20, 40, 80))
            print(f"{S0:>4} {name:>10} {V:9.1f}  {sel}   {S:5.2f} {L:6.2f}")

if __name__ == "__main__":
    for nm, (g, p) in SHAPES.items():
        run(f"{nm} g & p", make_model(g, p))
    flat = lambda S: np.ones_like(np.asarray(S, float))
    run("FAIL flat g & p (exp shapes removed)", make_model(flat, flat))
    run("FAIL chronic pain: rho=0.01 (exp)", make_model(*SHAPES["exp"], rho=0.01))
    run("FAIL behavioral activation psi=0.25 (exp)", make_model(*SHAPES["exp"], psi=0.25))
    run("stressor inflow sigma=0.5 (exp)", make_model(*SHAPES["exp"], sigma=0.5))
