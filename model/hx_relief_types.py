"""Does relief-first survive when some relief numbs?

State: suffering S, liking stock L, capacity c in (0,1] (how much liking registers).
Each period one unit of effort goes to relief or expansion.
  clean relief  : S -= rho_c * S              (security, rest, support, equanimity)
  numbing relief: S -= rho_n * S, faster, but c *= (1 - mu) and next period S += rebound
  expansion     : L += Delta * p(S) * c        (numbness also blocks learning)
Pleasure P = g(S) * c * L. Value V = sum delta^t (P - lam * S). Capacity recovers slowly.
Policies: relieve while S > threshold (share n of relief is numbing), else expand.
"""
import itertools, numpy as np

T, DELTA, LAM, DLT = 100, 0.97, 1.5, 0.5
RHO_C, RHO_N, PSI = 0.25, 0.5, 0.05
g = lambda S: np.exp(-0.3 * S)
p = lambda S: np.exp(-0.3 * S)

def simulate(S0, n, thr, mu, rebound, relief_ok=True):
    S, L, c, V, pending = S0, 1.0, 1.0, 0.0, 0.0
    for t in range(T):
        S += pending; pending = 0.0
        V += DELTA ** t * (g(S) * c * L - LAM * S)
        if relief_ok and S > thr:
            S -= (1 - n) * RHO_C * S + n * RHO_N * S
            c *= (1 - mu * n)
            pending = rebound * n
        else:
            L += DLT * p(S) * c
        c += PSI * (1 - c)
    return V

THRS = [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]
SHARES = [0.0, 0.25, 0.5, 0.75, 1.0]

def best(S0, mu, reb, shares):
    return max((simulate(S0, n, th, mu, reb), n, th) for n, th in itertools.product(shares, THRS))

print("Best policy per scenario (searching numbing share n and switch threshold)")
print(f"{'S0':>4} {'mu':>5} {'reb':>4} | {'best V':>7} n*   thr* | {'clean only':>10} {'numb only':>9} {'no relief':>9}")
for S0 in [8.0, 3.0]:
    for mu, reb in [(0, 0), (0.05, 0), (0.15, 0), (0, 0.3), (0.05, 0.3), (0.15, 0.3)]:
        V, n, th = best(S0, mu, reb, SHARES)
        Vc = best(S0, mu, reb, [0.0])[0]
        Vn = best(S0, mu, reb, [1.0])[0]
        V0 = simulate(S0, 0, 0, mu, reb, relief_ok=False)
        print(f"{S0:>4} {mu:>5} {reb:>4} | {V:7.1f} {n:<4} {th:<4} | {Vc:10.1f} {Vn:9.1f} {V0:9.1f}")
    print()

# When only numbing relief exists: is it better than nothing, and how far to push it?
print("Only numbing available (S0=8): best threshold vs no relief")
for mu in [0.0, 0.05, 0.15, 0.3]:
    for reb in [0.0, 0.3, 1.0]:
        V, n, th = best(8.0, mu, reb, [1.0])
        V0 = simulate(8.0, 0, 0, mu, reb, relief_ok=False)
        print(f"  mu={mu:<4} rebound={reb:<4} numb best={V:7.1f} (stop at S={th})  no relief={V0:7.1f}")
