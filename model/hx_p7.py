"""P7: liking, not wanting.

n sources with liking l_i and freshness h_i. Each period one source is used:
  used:   h -= ALPHA*h;  (depleting variant: l *= 1-BETA)
  rested: h += REC*(1-h)
Pleasure = l_j * h_j for the used source j.
Wanting w_i = v_i + s_i. v_i is a learned prediction of pleasure, updated only when i
is used (v_j += ETA*(l_j h_j - v_j)), so it lags freshness for unused sources.
s_i is incentive sensitization: s_j += SENS on use, s *= (1-DECAY) every period.
Each period, with probability pi the urge decides (argmax w); otherwise liking decides
(argmax l*h). Lower pi = urge surfing: the urge still arrives, it just doesn't steer.
"""
import numpy as np

ALPHA, REC, T, DELTA, ETA = 0.5, 0.3, 200, 0.99, 0.5

def run(l0, pi, sens, decay, beta=0.0, seed=0):
    rng = np.random.default_rng(seed)
    l = l0.copy(); h = np.ones_like(l); v = l0.copy(); s = np.zeros_like(l)
    V, uses, gaps = 0.0, np.zeros(len(l)), []
    draws = rng.random(T)                      # common random numbers across pi
    for t in range(T):
        best_liking = np.argmax(l * h)
        j = np.argmax(v + s) if draws[t] < pi else best_liking
        gaps.append((l * h)[best_liking] - (l * h)[j])
        V += DELTA**t * l[j] * h[j]
        uses[j] += 1
        rested = np.ones(len(l), bool); rested[j] = False
        h[j] -= ALPHA * h[j]; h[rested] += REC * (1 - h[rested])
        l[j] *= (1 - beta)
        v[j] += ETA * (l[j] * (h[j] / (1 - ALPHA)) - v[j])
        s[j] += sens; s *= (1 - decay)
    return V, uses.max() / T, np.mean(gaps[-50:])

if __name__ == "__main__":
    rng = np.random.default_rng(1)
    l0 = np.array([1.0, 0.9, 0.8, 0.7, 0.6])

    print("Value, lock-in (share of periods on one source), late per-period gap")
    print(f"{'sens':>5} {'pi':>5} | {'V':>7} {'lock':>5} {'gap':>5}")
    for sens in [0.0, 0.1, 0.3]:
        for pi in [1.0, 0.75, 0.5, 0.25, 0.1, 0.0]:
            V, lock, gap = np.mean([run(l0, pi, sens, 0.1, seed=s) for s in range(50)], axis=0)
            print(f"{sens:>5} {pi:>5} | {V:7.2f} {lock:5.2f} {gap:5.2f}")
        print()

    # Lock-in threshold: drift argument says the urge's favourite stays on top when
    # acting on it often enough that sensitization outpaces decay.
    print("Lock-in vs pi (sens=0.3, decay=0.1)")
    for pi in np.linspace(0, 1, 11):
        lock = np.mean([run(l0, pi, 0.3, 0.1, seed=s)[1] for s in range(50)])
        print(f"  pi={pi:.1f} lock={lock:.2f}")

    # Monotonicity check over random worlds: does V fall as pi rises?
    viol, total, worst = 0, 0, 0.0
    for k in range(300):
        l = rng.uniform(0.2, 1.0, rng.integers(2, 8))
        sens, decay = rng.uniform(0, 0.5), rng.uniform(0.02, 0.3)
        beta = rng.choice([0.0, 0.02])
        Vs = [np.mean([run(l, pi, sens, decay, beta, seed=s)[0] for s in range(10)])
              for pi in np.linspace(0, 1, 6)]
        diffs = np.diff(Vs)
        total += len(diffs); bad = diffs[diffs > 1e-9]
        viol += len(bad); worst = max(worst, bad.max() if len(bad) else 0)
    print(f"\nRandom worlds: V increased with more urge-steering in {viol}/{total} steps; "
          f"largest such increase {worst:.3f}")
