"""Does cutting craving raise pleasure over time, or just even it out?

Uses the combined model (hx_combined.py). "Craving" enters in up to three ways:
  steering   pi: the share of free choices the urge (cached value + sensitization, salience-
             weighted) makes instead of predicted liking. This is what claim 5 already tested.
  tension    the strongest unmet urge each period (wanting minus liking, for sources not chosen)
             is felt as suffering, weighted by tau (opt-in; 0 in the combined model).
  inflation  sensitized wanting raises the reference point of a kind of good, so the same
             pleasure feels like less (weight rc; opt-in).
"Cutting craving" at level c means: urge steers with probability c; with "felt" craving, tension
and inflation also scale by c. "Urge surfing only" lowers steering but leaves felt urges intact.

Reported per policy (8 seeds, 300 periods): net value V, gross pleasure (felt yields, carryover,
anticipation), suffering (felt distress + tension), within-life SD of V (evenness), share of
periods below zero, and growth: mean pleasure in the last 100 periods minus the first 100.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx_combined as H  # noqa: E402

SEEDS = 8


def stats(cfg):
    out = [H.run(cfg, s) for s in range(SEEDS)]
    V = np.array([o[0] for o in out]); pl = np.array([o[1]["pl"] for o in out])
    su = np.array([o[1]["su"] for o in out])
    return dict(V=V.mean(), pl=pl.mean(), su=su.mean(), sd=V.std(axis=1).mean(),
                sdp=pl.std(axis=1).mean(), neg=(V < 0).mean(),
                grow=(pl[:, -100:].mean(1) - pl[:, :100].mean(1)).mean(),
                skill=np.mean([o[1]["uses"].get("skill", 0) + o[1]["uses"].get("sensitizing", 0) for o in out]),
                feed=np.mean([o[1]["uses"].get("feed", 0) for o in out]))


def row(label, r):
    print("   %-34s V %6.3f  pleasure %6.3f  suffering %6.3f  SD(V) %5.2f  SD(pl) %5.2f  neg %4.0f%%  "
          "growth %+6.3f  skill uses %5.1f  feed %5.1f" % (label, r["V"], r["pl"], r["su"], r["sd"], r["sdp"],
                                                           100 * r["neg"], r["grow"], r["skill"], r["feed"]))


if __name__ == "__main__":
    print(__doc__.split("\n")[0])
    LEVELS = [1.0, 0.75, 0.5, 0.25, 0.0]
    worlds = [("C5 world (feed present)", dict(feed=True)),
              ("default life", dict(H.DEFAULT))]

    print("\nK1. Steering only (claim 5 as run): what the gain is made of")
    for wn, w in worlds:
        print("  " + wn)
        for c in LEVELS:
            row("urge steers %.2f" % c, stats(dict(w, pi=c)))

    print("\nK2. Craving also felt: unmet-urge tension tau, reference inflation rc")
    for tau, rc in [(0.2, 0.0), (0.5, 0.0), (0.0, 0.3), (0.5, 0.3)]:
        print("  tau=%.1f rc=%.1f (C5 world)" % (tau, rc))
        for c in [1.0, 0.5, 0.0]:
            row("craving %.2f (felt scales too)" % c, stats(dict(feed=True, pi=c, tension=tau * c, ref_infl=rc * c)))
        row("urge surfing only (pi 0, felt full)", stats(dict(feed=True, pi=0.0, tension=tau, ref_infl=rc)))

    print("\nK3. Without the feed and the salience bias (does steering still matter?)")
    for c in [1.0, 0.0]:
        row("flat salience, no feed, steers %.2f" % c, stats(dict(pi=c, sal="flat", feed=False)))
        row("  + tension 0.5 felt", stats(dict(pi=c, sal="flat", feed=False, tension=0.5 * c)))
