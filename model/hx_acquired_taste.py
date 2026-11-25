"""Acquired-taste mechanism for the hedonic-expansionism toy model.

Time is counted in slots (one slot = one possible use of a source; the
existing hx_model.py uses rho=0.3 recovery per unit rest, kept here).
One source with complexity K; exposures spaced g slots apart (g=0: massed).

State: S (familiarity / learning capital), h (fast freshness), m (slow novelty)
  positive factor (Berlyne learning):   G_K(S) = A_K (1 - exp(-S / sig_K))
  experienced liking of exposure n:     v_n   = l0 + G_K(S_n) * h_n * m_n
  exposure:   S += 1;  h *= (1 - a_K);  m *= (1 - d_K)
  rest g:     h = 1-(1-h)e^{-rho g};   m = 1-(1-m)e^{-eps g}
  complexity: A_K = A1 K/(1+K), sig_K = s1 (1+K), a_K = a0/(1+K), d_K = a_K/5

Satiation (negative factor) acts on the learned part only, so heavy massed
exposure returns liking to baseline l0 (Szpunar et al. 2004, Exp 2) and an
aversive source (l0<0) consumed too fast stays aversive.
"""
import numpy as np
from scipy.optimize import least_squares

RHO, EPS = 0.3, 0.005          # recovery per slot: freshness (hx_model), novelty [assumed]
A1, S1, A0 = 2.0, 1.0, 0.1     # overwritten by calibrate()
A1_MAX = 3.0                   # cap on learned gain, scale points [assumed]

# Szpunar, Schellenberg & Pliner 2004 (JEP:LMC 30:370), focused listening,
# liking minus unheard baseline on their rating scale.
#  Exp2 orchestral (K=2): peak 4.65 vs 3.50 at 8 exp; rose 0->2 (2-exp mean
#    not extracted: +0.70 assumed); 32 not different from baseline (+0.10 assumed)
#  Exp3 instrument tone sequences (K=1): peak 4.07 vs 3.54 at 4; 16 still
#    above baseline (+0.45 assumed)
#  Exp1 piano tone sequences (K=0): flat
DATA = [(2, 2, 0.70), (2, 8, 1.15), (2, 32, 0.10),
        (1, 4, 0.53), (1, 16, 0.45),
        (0, 4, 0.0), (0, 16, 0.0), (0, 64, 0.0)]


def params(K, gain=1.0):
    a = A0 / (1 + K)
    return gain * A1 * K / (1 + K), S1 * (1 + K), a, a / 5


def stream(K, l0, gap, N, gain=1.0):
    """Liking of exposures 1..N spaced `gap` slots apart (rating after exposure
    n reflects S=n, as in Szpunar's 'liking after n exposures')."""
    A, sig, a, d = params(K, gain)
    S, h, m, out = 0.0, 1.0, 1.0, []
    for _ in range(int(N)):
        S += 1; h *= 1 - a; m *= 1 - d
        out.append(l0 + A * (1 - np.exp(-S / sig)) * h * m)
        h = 1 - (1 - h) * np.exp(-RHO * gap); m = 1 - (1 - m) * np.exp(-EPS * gap)
    return np.array(out)


def calibrate():
    global A1, S1, A0
    def res(p):
        global A1, S1, A0
        A1, S1, A0 = p
        return [stream(K, 0, 0, n)[-1] - y for K, n, y in DATA]
    fit = least_squares(res, [2.0, 1.0, 0.1], bounds=([0, 0.05, 0], [A1_MAX, 50, 0.9]))
    A1, S1, A0 = fit.x
    return np.sqrt(np.mean(fit.fun ** 2))


RMSE = calibrate()


def steady(K, gap):
    """Steady-state h*m seen at an exposure when used every gap slots."""
    A, sig, a, d = params(K)
    h = m = 1.0
    for _ in range(20000):
        h = 1 - (1 - h * (1 - a)) * np.exp(-RHO * gap)
        m = 1 - (1 - m * (1 - d)) * np.exp(-EPS * gap)
    return h * (1 - a) * m * (1 - d)


# ------------------------------------------------- task 2: does trying pay off
def value_of_trying(K, l0, gap, H, o, delta=0.999):
    """Discounted gain from giving the new source one slot in every gap+1
    instead of an outside option worth o per slot, over H slots. A foresighted
    agent may stop any time (best prefix of the deterministic stream)."""
    N = max(1, int(H / (gap + 1)))
    v = stream(K, l0, gap, N)
    gains = (v - o) * delta ** ((gap + 1) * np.arange(N))
    pref = np.concatenate([[0], np.cumsum(gains)])
    return pref.max(), v


def n_breakeven(K, l0, o=0.0):
    """Exposures until the learned part alone beats o (no satiation)."""
    A, sig, *_ = params(K)
    return np.inf if A <= o - l0 else -sig * np.log(1 - (o - l0) / A)


# ---------------------------------------- task 3: spacing and average pleasure
def avg_rate(K, l0, gap, o, H=4000):
    v = stream(K, l0, gap, int(H / (gap + 1)))
    return (v.sum() + (H - len(v)) * o) / H, v


# --------------------------------------------- task 5: distress and sampling
def p_acquire(K, l0, gap, s, p0=0.6, c0=0.8, N=100, stress_gain=0.0):
    """Try w.p. p0(1-s); after every exposure with v<=0 continue w.p. c0(1-s),
    else the source is filed as a 'bad' and never resampled (Delaney, Jacobson
    & Moenig 2020, Lemma 2). Acquired = surviving the first N exposures.
    Returns (probability, k = number of unpleasant exposures among the first N)."""
    v = stream(K, l0, gap, N, gain=1 - stress_gain * s)
    k = int((v <= 0).sum())
    return p0 * (1 - s) * (c0 * (1 - s)) ** k, k


def approx_value(K, l0, gap, H, o, delta=0.999):
    """Closed-form approximation, analogue of p*dP*(1-delta^H)/(1-delta) > k:
    dP = l0 + A_K*phi(g) - o (steady gain per use), cost k = early shortfall
    over n_be exposures, gain starts after n_be uses."""
    A, sig, *_ = params(K)
    dP = l0 + A * steady(K, gap) - o
    nb = n_breakeven(K, l0, o)
    if dP <= 0 or not np.isfinite(nb):
        return 0.0
    D = delta ** (gap + 1)
    Nuse = H / (gap + 1)
    cost = nb * (o - l0) / 2          # linearised early shortfall
    gain = D ** nb * dP * (1 - D ** max(Nuse - nb, 0)) / (1 - D)
    return max(gain - cost, 0.0)


if __name__ == "__main__":
    print(f"Calibration: A1={A1:.2f} s1={S1:.2f} a0={A0:.3f} RMSE={RMSE:.3f} pts")
    for K, n, y in DATA:
        print(f"  K={K} n={n:2d} data={y:+.2f} model={stream(K, 0, 0, n)[-1]:+.2f}")
    for K in [1, 2, 4, 8]:
        v = stream(K, 0, 0, 200)
        print(f"  massed K={K}: peak n={np.argmax(v)+1} v={v.max():.2f} v@32={v[31]:.2f}"
              f"  A_K={params(K)[0]:.2f} sig={params(K)[1]:.1f} a={params(K)[2]:.3f}")

    O = 0.5
    print(f"\nTask 2: value of trying, outside option o={O}, delta=.999/slot")
    print("  K   l0  n_be  v*(g=3)  val(g3,H1000) val(g0,H1000) val(g3,H50) val(g3,H200)")
    for K in [1, 2, 4, 8]:
        for l0 in [-0.5, -1.0, -2.0]:
            vstar = l0 + params(K)[0] * steady(K, 3)
            print(f"  {K} {l0:+.1f} {n_breakeven(K, l0, O):5.1f}  {vstar:+.2f}"
                  f"  {value_of_trying(K, l0, 3, 1000, O)[0]:7.1f}"
                  f"  {value_of_trying(K, l0, 0, 1000, O)[0]:7.1f}"
                  f"  {value_of_trying(K, l0, 3, 50, O)[0]:7.1f}"
                  f"  {value_of_trying(K, l0, 3, 200, O)[0]:7.1f}")

    print("  approx vs exact (g3,H1000):", [(K, l0, round(approx_value(K, l0, 3, 1000, O), 1),
          round(value_of_trying(K, l0, 3, 1000, O)[0], 1)) for K, l0 in [(2, -0.5), (4, -0.5), (4, -1.0), (8, -1.0)]])

    print(f"\nTask 3: average pleasure per slot vs gap, K=2, o={O}")
    for l0 in [0.5, -0.5]:
        rows = []
        for g in [0, 1, 2, 3, 5, 8, 12, 20, 40]:
            r, v = avg_rate(2, l0, g, O)
            rows.append((g, r, l0 + params(2)[0] * steady(2, g)))
        best = max(rows, key=lambda x: x[1])
        print(f"  l0={l0:+.1f} rate " + " ".join(f"g{g}:{r:.3f}" for g, r, _ in rows)
              + f"  best g={best[0]}")
        print(f"         v*   " + " ".join(f"g{g}:{x:+.2f}" for g, _, x in rows))

    print("\nTask 3b: steady liking l0 + A_K h*m*(g); negative = stuck aversive")
    for K in [1, 2, 4]:
        for l0 in [-0.5, -1.0]:
            print(f"  K={K} l0={l0} " + " ".join(f"g{g}:{l0 + params(K)[0] * steady(K, g):+.2f}"
                                                 for g in [0, 0.5, 1, 2, 3, 5, 10]))
    for K, l0 in [(2, -0.5), (2, -1.0), (4, -1.0)]:
        print(f"  P(acquire) K={K} l0={l0} by gap: " + " ".join(
            f"g{g}:{p_acquire(K, l0, g, 0)[0]:.2f}(k={p_acquire(K, l0, g, 0)[1]})"
            for g in [0, 0.5, 1, 3, 8]))

    print("\nTask 4: complexity, l0=0, gap=3")
    for K in [0.5, 1, 2, 4, 8]:
        v = stream(K, 0, 3, 600)
        pk = int(np.argmax(v))
        print(f"  K={K}: v1={v[0]:.2f} peak n={pk+1} v={v[pk]:.2f} v@50={v[49]:.2f}"
              f" v@200={v[199]:.2f} v@600={v[-1]:.2f} late/peak={v[-1]/v[pk]:.2f}"
              f" cum20={v[:20].sum():.1f} cum600={v.sum():.0f}")

    print("\nTask 5: P(acquire) vs distress s (gap=3); k = unpleasant exposures")
    for sg in [0.0, 0.5]:
        print(f"  stress_gain={sg} (learned gain scaled by 1-{sg}*s)")
        for K, l0 in [(2, -0.5), (2, -1.0), (4, -1.0), (8, -2.0)]:
            row = "  ".join(f"s={s:.2f}:{p_acquire(K, l0, 3, s, stress_gain=sg)[0]:.3f}"
                            f"(k={p_acquire(K, l0, 3, s, stress_gain=sg)[1]})"
                            for s in [0, .25, .5, .75])
            print(f"   K={K} l0={l0:+.1f}  {row}")
