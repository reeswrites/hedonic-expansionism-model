"""v2: suffering also fades on its own (rate d), and policies can bridge:
numb while S > s_numb, clean relief while thr < S <= s_numb, expand below thr."""
import itertools, numpy as np
T, DELTA, LAM, DLT = 100, 0.97, 1.5, 0.5
RHO_C, RHO_N, PSI = 0.25, 0.5, 0.05
g = lambda S: np.exp(-0.3 * S); p = lambda S: np.exp(-0.3 * S)

def sim(S0, s_numb, thr, mu, reb, d, clean_ok=True, numb_ok=True):
    S, L, c, V, pend, numbs = S0, 1.0, 1.0, 0.0, 0.0, 0
    for t in range(T):
        S += pend; pend = 0.0
        V += DELTA**t * (g(S)*c*L - LAM*S)
        if numb_ok and S > s_numb:
            S -= RHO_N*S; c *= (1-mu); pend = reb; numbs += 1
        elif clean_ok and S > thr:
            S -= RHO_C*S
        else:
            L += DLT*p(S)*c
        S -= d*S
        c += PSI*(1-c)
    return V, numbs

GRID = [0.1, 0.25, 0.5, 1, 2, 4, 6, 99]
def best(S0, mu, reb, d, clean_ok=True, numb_ok=True):
    out = []
    for sn, th in itertools.product(GRID, GRID[:-1]):
        if clean_ok and numb_ok and sn < th: continue
        if not numb_ok: sn = 99
        V, k = sim(S0, sn, th, mu, reb, d, clean_ok, numb_ok)
        out.append((V, sn, th, k))
    return max(out)

for d in [0.0, 0.03]:
    print(f"=== natural fading d={d}, S0=8")
    print(f"{'mu':>5} {'reb':>4} | {'best':>7} numb>S clean>S #numb | {'clean only':>10} {'numb only':>9} {'nothing':>8}")
    for mu, reb in [(0,0),(0.05,0),(0.15,0),(0.3,0),(0,0.3),(0.15,0.3),(0.3,1.0)]:
        V, sn, th, k = best(8, mu, reb, d)
        Vc = best(8, mu, reb, d, numb_ok=False)[0]
        Vn = best(8, mu, reb, d, clean_ok=False)
        V0 = sim(8, 99, 99, mu, reb, d)[0]
        print(f"{mu:>5} {reb:>4} | {V:7.1f} {sn:>6} {th:>6} {k:>4} | {Vc:10.1f} {Vn[0]:9.1f} {V0:8.1f}")
    print()
