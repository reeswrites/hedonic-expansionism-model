"""Toy model of hedonic expansionism: checks the propositions numerically."""
import numpy as np

T = 1.0          # time available per period
alpha = 0.6      # habituation per unit of use
rho = 0.3        # recovery per unit of rest

def steady_fresh(u):
    # h' = h - alpha*u*h + rho*(1-h)*(1-u) -> fixed point
    return rho * (1 - u) / (alpha * u + rho * (1 - u))

def P_star(n, ell=1.0):
    u = T / n  # even split of time across n sources (u = share of each source's period)
    return T * ell * steady_fresh(u)

print("P2 breadth: steady-state pleasure vs number of renewing sources")
for n in [1, 2, 3, 5, 10, 20, 50, 100]:
    print(f"  n={n:3d}  P*={P_star(n):.3f}  marginal={P_star(n+1)-P_star(n):.4f}")

# P1: depleting sources (liking decays with cumulative use), no expansion
def run(n, kind, periods=200, beta=0.02, gamma=0.01, cap=3.0):
    ell = np.ones(n); h = np.ones(n); out = []
    u = T / n
    for t in range(periods):
        p = (ell * h * u).sum()
        out.append(p)
        h = h - alpha * u * h + rho * (1 - h) * (1 - u)
        if kind == "depleting":
            ell = ell * (1 - beta * u)
        elif kind == "skill":
            ell = ell + gamma * u * (cap - ell)
    return np.array(out)

print("\nP1 fixed liking set, no expansion (pleasure at t=1,50,200)")
for kind in ["depleting", "renewing", "skill"]:
    r = run(5, kind)
    print(f"  {kind:9s} {r[0]:.3f} {r[49]:.3f} {r[-1]:.3f}")

# P5: resilience. Each source lost w.p. q per period. Grief = f(share lost).
rng = np.random.default_rng(0)
q = 0.05
def expected_grief(n, f, sims=200000):
    lost = rng.random((sims, n)) < q
    share = lost.sum(1) / n
    return f(share).mean()
print("\nP5 expected grief from losses, linear vs convex grief")
for n in [1, 3, 10]:
    lin = expected_grief(n, lambda s: s)
    cvx = expected_grief(n, lambda s: s**2)
    print(f"  n={n:2d}  linear={lin:.4f}  convex(s^2)={cvx:.4f}")

# P6: thick bundle vs spread. One bundle of k strands with superadditive bonus,
# or k separate sources. Bundle lost as a unit.
def bundle_value(k, bonus, lam=2.0, sims=200000):
    lost = rng.random(sims) < q
    pleasure_b = np.where(lost, 0, k * (1 + bonus))
    grief_b = np.where(lost, 1.0, 0) ** 2 * k  # whole share lost at once
    lost_s = rng.random((sims, k)) < q
    pleasure_s = (~lost_s).sum(1)
    grief_s = (lost_s.sum(1) / k) ** 2 * k
    return (pleasure_b - lam * grief_b).mean(), (pleasure_s - lam * grief_s).mean()
print("\nP6 bundle vs spread (k=3 strands, lambda=2)")
for bonus in [0.0, 0.05, 0.2]:
    b, s = bundle_value(3, bonus)
    print(f"  bonus={bonus:.2f}  bundle={b:.3f}  spread={s:.3f}")
