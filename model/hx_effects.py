"""Headline effects with error bars: seed noise and parameter spread (uses hx_stats.py).

Each effect is a difference in lifetime-average net value V (or gross pleasure) between two
policies in the combined model (hx_combined.py). Reported three ways:
  1. at default parameters: paired difference ± standard error over 20 seeds;
  2. as a share of the yardstick gap, default life -> expansionist life, at defaults;
  3. across 60 worlds with the invented parameters redrawn within 3x: the effect divided by
     that world's own yardstick gap (unit-free), with median, middle half and sign share.
Calibrated constants (loss aversion, the acquired-taste fit) are held fixed.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx_combined as H  # noqa: E402
import hx_stats as S  # noqa: E402

FIXED = {"LAM", "LOSS", "ACQ_A", "ACQ_SIG", "ACQ_a", "ACQ_L0"}
KEYS = [k for k, v in H.P.items() if isinstance(v, float) and k not in FIXED]
SWEEP_SEEDS = 3


def V(cfg):
    return lambda s: H.run(cfg, s)[0].mean()


def PL(cfg):
    return lambda s: H.run(cfg, s)[1]["pl"].mean()


def mean_diff(a, b, f=V, seeds=SWEEP_SEEDS):
    return np.mean([f(b)(s) - f(a)(s) for s in range(seeds)])


C5 = dict(feed=True)
CHRONIC = dict(feed=True, inflow=0.3)
EFFECTS = [
    ("Cutting craving, feed world (pleasure)", dict(C5, pi=1.0), dict(C5, pi=0.0), PL),
    ("Cutting craving, default life (pleasure)", dict(H.DEFAULT, pi=1.0), dict(H.DEFAULT, pi=0.0), PL),
    ("Cutting craving, feed world (value)", dict(C5, pi=1.0), dict(C5, pi=0.0), V),
    ("Adding calm 0.8, chronic distress, no craving", dict(CHRONIC, pi=0.0), dict(CHRONIC, pi=0.0, e=0.8), V),
    ("Adding calm 0.8, feed world, no craving", dict(C5, pi=0.0), dict(C5, pi=0.0, e=0.8), V),
    ("Vivid liking 0.2, feed world, no craving", dict(C5, pi=0.0), dict(C5, pi=0.0, vivid=0.2), V),
    ("Flatten 0.6 (choice kept), feed world", dict(C5, pi=0.0, e=0.8), dict(C5, pi=0.0, e=0.8, flat=0.6), V),
    ("Flatten 0.6 + careless choice, feed world", dict(C5, pi=0.0, e=0.8),
     dict(C5, pi=0.0, e=0.8, flat=0.6, flat_choice=1.0), V),
    ("No numbing source in the default life", dict(H.DEFAULT), dict(H.DEFAULT, numb=False), V),
]

if __name__ == "__main__":
    print(__doc__.split("\n")[0])
    gap = S.paired(V(H.DEFAULT), V(H.EXPANSIONIST))
    print("\nYardstick, default life -> expansionist life (value): " + S.fmt_paired(gap))
    print("Parameters redrawn: %d invented constants; held fixed: %s" % (len(KEYS), ", ".join(sorted(FIXED))))
    yard = lambda: mean_diff(H.DEFAULT, H.EXPANSIONIST)  # noqa: E731
    for i, (name, a, b, f) in enumerate(EFFECTS):
        r = S.paired(f(a), f(b))
        base = np.mean([f(a)(s) for s in range(20)])
        print("\n%s" % name)
        print("   defaults: " + S.fmt_paired(r, base if f is PL else None)
              + ("" if f is PL else ", %.0f%% of the yardstick gap" % (100 * r["diff"] / gap["diff"])))
        if f is PL:
            sw = S.sweep(H.P, lambda: mean_diff(a, b, PL) / np.mean([PL(a)(s) for s in range(SWEEP_SEEDS)]),
                         KEYS, seed=i)
            print("   across worlds, as share of baseline pleasure: " + S.fmt_sweep(sw, pct=True))
        else:
            sw = S.sweep(H.P, lambda: mean_diff(a, b), KEYS, scale=yard, seed=i)
            print("   across worlds, as share of that world's yardstick gap: " + S.fmt_sweep(sw, pct=True))
