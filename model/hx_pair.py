"""Two people choosing what to do together, over months.

Each of A and B has a liking l[i] (0-10) for N activities, correlated across them by rho
(taste overlap), and freshness h[i] per activity (habituates with use, recovers with rest).

A's value from a joint activity i:  m*lA*hA + kappaA*m*lB*hB + b - coord
From doing their own thing in the same room (parallel): m_par*lA*hA (own pick) + kappa*0.5*lB*hB + 0.6*b
From doing their own thing alone (solo): lA*hA
Learning through valuing: after a joint activity, each person's liking moves toward the
partner's if the partner likes it more: l += eta*(l_partner - l)+.

Strategies:
  solo        each alone, own favourite (freshness-weighted)
  overlap     joint activity that maximises the pair's combined value now
  turns       alternate: A's favourite, then B's favourite, jointly
  compromise  joint activity with the best minimum raw liking (maximin)
  parallel    together, each doing their own favourite
  mixed       each period, best of all joint activities and parallel, by combined value
  expand      like mixed, but also counts the value of taste gained (future-minded)
"""
import numpy as np

N, T, DELTA = 12, 200, 0.99
M, M_PAR, B, COORD = 1.3, 1.1, 1.0, 0.3
ALPHA, REC = 0.5, 0.3

def make_tastes(rho, rng):
    z = rng.normal(size=(2, N))
    a = z[0]; b = rho * z[0] + np.sqrt(max(0, 1 - rho**2)) * z[1]
    return np.clip(5 + 2 * a, 0, 10), np.clip(5 + 2 * b, 0, 10)

def run(strategy, rho, kA, kB, eta, seed):
    rng = np.random.default_rng(seed)
    lA, lB = make_tastes(rho, rng)
    hA, hB = np.ones(N), np.ones(N)
    VA = VB = 0.0
    for t in range(T):
        jointA = M * lA * hA + kA * M * lB * hB + B - COORD
        jointB = M * lB * hB + kB * M * lA * hA + B - COORD
        a_fav, b_fav = np.argmax(lA * hA), np.argmax(lB * hB)
        parA = M_PAR * lA[a_fav] * hA[a_fav] + kA * 0.5 * lB[b_fav] * hB[b_fav] + 0.6 * B
        parB = M_PAR * lB[b_fav] * hB[b_fav] + kB * 0.5 * lA[a_fav] * hA[a_fav] + 0.6 * B
        gain = eta * (np.clip(lB - lA, 0, None) + np.clip(lA - lB, 0, None))  # taste each would gain
        if strategy == "solo":
            choice, va, vb = ("sep", a_fav, b_fav), lA[a_fav] * hA[a_fav], lB[b_fav] * hB[b_fav]
        elif strategy == "parallel":
            choice, va, vb = ("sep", a_fav, b_fav), parA, parB
        else:
            if strategy == "overlap":
                i = np.argmax(jointA + jointB)
            elif strategy == "turns":
                i = a_fav if t % 2 == 0 else b_fav
            elif strategy == "compromise":
                i = np.argmax(np.minimum(lA * hA, lB * hB))
            elif strategy in ("mixed", "expand"):
                score = jointA + jointB + (gain * 20 if strategy == "expand" else 0)
                i = np.argmax(score)
                if parA + parB > score[i]:
                    choice, va, vb = ("sep", a_fav, b_fav), parA, parB
                    i = None
            if i is not None:
                choice, va, vb = ("joint", i, i), jointA[i], jointB[i]
        VA += DELTA**t * va; VB += DELTA**t * vb
        # freshness
        usedA = np.zeros(N, bool); usedB = np.zeros(N, bool)
        usedA[choice[1]] = True; usedB[choice[2]] = True
        hA[usedA] -= ALPHA * hA[usedA]; hA[~usedA] += REC * (1 - hA[~usedA])
        hB[usedB] -= ALPHA * hB[usedB]; hB[~usedB] += REC * (1 - hB[~usedB])
        # learning through valuing, only from joint activities
        if choice[0] == "joint":
            i = choice[1]; dA, dB = lB[i] - lA[i], lA[i] - lB[i]
            if dA > 0: lA[i] += eta * dA
            if dB > 0: lB[i] += eta * dB
    liked = lambda l: np.sum(l >= 6)
    overlap = np.corrcoef(lA, lB)[0, 1]
    return VA, VB, liked(lA) + liked(lB), overlap

STRATS = ["solo", "parallel", "compromise", "turns", "overlap", "mixed", "expand"]

def table(rho, kA, kB, eta, seeds=40):
    out = {}
    for s in STRATS:
        r = np.array([run(s, rho, kA, kB, eta, sd) for sd in range(seeds)])
        out[s] = r.mean(axis=0)
    return out

if __name__ == "__main__":
    for kappa in [0.0, 0.5]:
        for eta in [0.0, 0.05]:
            print(f"=== mudita {kappa}, learning through valuing {eta}")
            print(f"{'overlap':>8} | " + " ".join(f"{s:>10}" for s in STRATS))
            for rho in [-0.3, 0.0, 0.5, 0.9]:
                res = table(rho, kappa, kappa, eta)
                print(f"{rho:>8} | " + " ".join(f"{(res[s][0]+res[s][1])/2:10.0f}" for s in STRATS))
            print()

    print("=== tastes after 200 periods (mudita 0.5, learning 0.05): liked activities (>=6, both people) / taste overlap")
    print(f"{'start':>8} | " + " ".join(f"{s:>12}" for s in STRATS))
    for rho in [0.0, 0.5]:
        res = table(rho, 0.5, 0.5, 0.05)
        print(f"{rho:>8} | " + " ".join(f"{res[s][2]:5.1f} / {res[s][3]:4.2f}" for s in STRATS))
    r0 = np.array([make_tastes(0.0, np.random.default_rng(s)) for s in range(40)])
    print(f"  (at start, overlap 0: liked {np.mean([np.sum(a>=6)+np.sum(b>=6) for a,b in r0]):.1f})")

    print("\n=== unequal mudita: A has 0.5, B has 0 (learning 0.05, overlap 0): value A / B")
    res = table(0.0, 0.5, 0.0, 0.05)
    for s in STRATS:
        print(f"  {s:>10}: A {res[s][0]:6.0f}  B {res[s][1]:6.0f}")
