"""Does the Buddhist package expand liking or flatten it?

hx_craving.py showed that cutting craving raises pleasure, but there "no craving" just means
choosing by predicted liking: an ideal chooser, not an equanimous one. Contemplative traditions
pair less craving with two further changes that pull in opposite directions:
  flatten  equanimity (upekkha) evens out liking: each felt yield is pulled toward the agent's
           running average of unflattened yield, y' = (1 - f) y + f ybar. Highs drop and lows
           (and shortfalls against the reference) rise. It does shift choices somewhat: relief is
           exempt, and curiosity and social-battery terms are added after flattening, so
           they weigh relatively more. E4 adds the stronger version, where indifference
           also makes choice careless (a random pick with probability f).
  vivid    the jhana-teacher claim: with less grasping, liking itself is more vivid;
           positive felt yields are multiplied by (1 + v).
  calm     the model's existing equanimity e: distress is felt and captures attention less.
Each is coupled to craving: at craving level c the knobs are f(1-c), v(1-c), e(1-c), so they
grow as craving falls. All sizes are invented; the point is which direction wins and where
the break-even sits.

Reported per policy (8 seeds, 300 periods): net value V, gross pleasure, suffering,
peaks (mean 90th percentile of per-period pleasure), troughs (10th percentile), within-life
SD of pleasure, share of periods below zero, spread of liking (SD of felt yields across uses),
and growth (mean pleasure, last 100 periods minus first 100).
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
    spread = np.mean([np.std(o[1]["other_y"] + o[1]["feed_y"]) for o in out])
    return dict(V=V.mean(), pl=pl.mean(), su=su.mean(), p90=np.percentile(pl, 90, axis=1).mean(),
                p10=np.percentile(pl, 10, axis=1).mean(), sdp=pl.std(axis=1).mean(), neg=(V < 0).mean(),
                spread=spread, grow=(pl[:, -100:].mean(1) - pl[:, :100].mean(1)).mean())


def row(label, r):
    print("   %-30s V %6.3f  pleasure %6.3f  suffering %5.3f  peaks %5.2f  troughs %5.2f  SD(pl) %4.2f  "
          "neg %3.0f%%  liking spread %4.2f  growth %+6.3f" % (label, r["V"], r["pl"], r["su"], r["p90"], r["p10"],
                                                               r["sdp"], 100 * r["neg"], r["spread"], r["grow"]))


def cut(w, c, f=0.0, v=0.0, e=0.0, careless=0.0):
    """World w at craving level c, with flattening f, vividness v, calm e grown by (1 - c)."""
    return dict(w, pi=c, flat=f * (1 - c), vivid=v * (1 - c), e=e * (1 - c), flat_choice=careless)


WORLDS = [("C5 world (feed present)", dict(feed=True)),
          ("chronic distress (feed, inflow 0.3)", dict(feed=True, inflow=0.3)),
          ("default life", dict(H.DEFAULT))]
PACKAGES = [("craving cut only", {}),
            ("+ calm e 0.8", dict(e=0.8)),
            ("+ flatten 0.3", dict(f=0.3)),
            ("+ flatten 0.6", dict(f=0.6)),
            ("+ vivid 0.2", dict(v=0.2)),
            ("flattening Buddhism (f.6 e.8)", dict(f=0.6, e=0.8)),
            ("jhana Buddhism (v.2 e.8)", dict(v=0.2, e=0.8))]

if __name__ == "__main__":
    print(__doc__.split("\n")[0])

    print("\nE1. Craving at full strength vs cut to zero, under each package")
    for wn, w in WORLDS:
        print("  " + wn)
        row("craving 1.00 (baseline)", stats(cut(w, 1.0)))
        for name, kw in PACKAGES:
            row(name, stats(cut(w, 0.0, **kw)))

    print("\nE2. Break-even flattening: how much evening-out cancels the gain from cutting craving?")
    print("   (craving 0 with flattening f, against craving 1 with none; first f at or below baseline)")
    for wn, w in WORLDS:
        base = stats(cut(w, 1.0))["V"]
        for ename, e in [("no calm", 0.0), ("calm e 0.8", 0.8)]:
            fs = np.round(np.arange(0.0, 1.01, 0.1), 1)
            Vs = [stats(cut(w, 0.0, f=f, e=e))["V"] for f in fs]
            be = next((f for f, V in zip(fs, Vs) if V <= base), None)
            print("   %-36s %-10s baseline %6.3f | f: %s | break-even %s" % (
                wn, ename, base, " ".join("%.1f:%.2f" % (f, V) for f, V in zip(fs, Vs)),
                "none up to 1.0" if be is None else "f = %.1f" % be))

    print("\nE3. Does flattening help where life is mostly bad? (craving 0, calm 0.8, default life)")
    for f in [0.0, 0.3, 0.6, 0.9]:
        row("flatten %.1f" % f, stats(cut(dict(H.DEFAULT), 0.0, f=f, e=0.8)))

    print("\nE4. Flattening that also makes choice careless (random pick with probability f), calm 0.8")
    for wn, w in WORLDS:
        base = stats(cut(w, 1.0))["V"]
        fs = np.round(np.arange(0.0, 1.01, 0.1), 1)
        Vs = [stats(cut(w, 0.0, f=f, e=0.8, careless=1.0))["V"] for f in fs]
        be = next((f for f, V in zip(fs, Vs) if V <= base), None)
        print("   %-36s baseline %6.3f | f: %s | break-even %s" % (
            wn, base, " ".join("%.1f:%.2f" % (f, V) for f, V in zip(fs, Vs)),
            "none up to 1.0" if be is None else "f = %.1f" % be))
    for f in [0.3, 0.6]:
        row("C5, careless flatten %.1f + calm" % f, stats(cut(WORLDS[0][1], 0.0, f=f, e=0.8, careless=1.0)))
