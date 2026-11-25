"""Hedonic expansionism v1, 'middle' experiment: what lifts mundane activities?

Builds on hx_model_v1 + the equanimity-intrusion variant (TAU*(1+2e)), applied throughout.
Levers (applied only to chores and commute, except attention training):
  reframe  : raise share of liked parts by +d by flipping aversive finest features to mildly liked
  pair     : a second feature layer (music or friends) is co-available during mundane hours, sharing
             the A attention slots AND the freshness vector of that source's own dedicated hour
  structure: raise D of chores/commute (more distinguishable parts at every resolution)
  attention: A from 3 to 4 (all activities)
World draws use a per-activity RNG so changing one activity's size does not reshuffle the others.
"""
import numpy as np
import hx_model_v1 as m

BASE, R, CAP, ALPHA, RHO = m.BASE, m.R, m.CAP, m.ALPHA, m.RHO
ACTS = m.ACTIVITIES
MUNDANE = m.MUNDANE
SEEDS, DAYS = range(30), 40
WALLCLOCK = False   # if True, every unattended feature of every activity recovers each hour (v1: only the active one)


def make_world(seed, Dmap, reframe):
    world = {}
    for i, (name, D0, pi, _) in enumerate(ACTS):
        D = Dmap.get(name, D0)
        rng = np.random.default_rng([seed, i])
        n = int(round(BASE * R ** D))
        pos = rng.random(n) < pi
        ell = np.where(pos, rng.exponential(1.0, n), -rng.exponential(0.8, n))
        if reframe and name in MUNDANE:
            frng = np.random.default_rng([seed, i, 99])
            p_flip = min(1.0, reframe / (1 - pi))
            flip = (~pos) & (frng.random(n) < p_flip)
            ell[flip] = frng.exponential(0.4, flip.sum())   # mildly liked
        world[name] = ell
    return world


def hour(ell, h, A, tau, e):
    """One hour over a feature vector (possibly concatenated layers). Returns v and picked mask."""
    intrude = np.where(ell < -tau)[0]
    intrude = intrude[np.argsort(ell[intrude])][:A]
    slots = A - len(intrude)
    liked = np.where(ell > 0)[0]
    pick = liked[np.argsort(-(ell[liked] * h[liked]))][:slots]
    pos = (ell[pick] * h[pick]).sum()
    neg = -ell[intrude].sum()
    v = CAP * np.tanh(pos / CAP) - (1 - e) * CAP * np.tanh(neg / CAP)
    used = np.zeros(len(ell), bool); used[pick] = True
    return v, used


def run(r, e, seed, A=3, Dmap=None, reframe=0.0, pair=None, days=DAYS):
    Dmap = Dmap or {}
    tau = 0.8 * (1 + 2 * e)
    world = make_world(seed, Dmap, reframe)
    Ds = {name: Dmap.get(name, D) for name, D, _, _ in ACTS}
    feats = {k: m.coarse(world[k], Ds[k], r) for k in world}
    fresh = {k: np.ones(len(v)) for k, v in feats.items()}
    log = []
    for _ in range(days):
        for name, _, _, hours in ACTS:
            for _ in range(hours):
                if pair and name in MUNDANE:
                    a, b = feats[name], feats[pair]
                    ell = np.concatenate([a, b]); h = np.concatenate([fresh[name], fresh[pair]])
                    v, used = hour(ell, h, A, tau, e)
                    h[used] -= ALPHA * h[used]; h[~used] += RHO * (1 - h[~used])
                    fresh[name][:] = h[:len(a)]; fresh[pair][:] = h[len(a):]
                    active = (name, pair)
                else:
                    h = fresh[name]
                    v, used = hour(feats[name], h, A, tau, e)
                    h[used] -= ALPHA * h[used]; h[~used] += RHO * (1 - h[~used])
                    active = (name,)
                if WALLCLOCK:
                    for k in fresh:
                        if k not in active:
                            fresh[k] += RHO * (1 - fresh[k])
                log.append((name, v))
    return log


def summarize(log, pair=None):
    names = np.array([n for n, _ in log]); v = np.array([x for _, x in log])
    mund = np.isin(names, list(MUNDANE))
    out = dict(mund=v[mund].mean(), mean=v.mean(), near=(v > 0.6 * CAP).mean(), neg=(v < 0).mean(),
               music=v[names == "music"].mean(), friends=v[names == "friends"].mean())
    return out


def cond(r, e, **kw):
    s = [summarize(run(r, e, sd, **kw)) for sd in SEEDS]
    return {k: np.mean([x[k] for x in s]) for k in s[0]}


LEVERS = [
    ("baseline", {}),
    ("reframe +0.1", dict(reframe=0.1)),
    ("reframe +0.2", dict(reframe=0.2)),
    ("pair music", dict(pair="music")),
    ("pair friend", dict(pair="friends")),
    ("structure D=1.0", dict(Dmap={"chores": 1.0, "commute": 1.0})),
    ("structure D=1.5", dict(Dmap={"chores": 1.5, "commute": 1.5})),
    ("attention A=4", dict(A=4)),
]

if __name__ == "__main__":
    import sys
    if "wall" in sys.argv:
        WALLCLOCK = True; print("WALLCLOCK recovery")
    extra = []
    if "combo" in sys.argv:
        extra = [
            ("D=1.5 + pair music", dict(Dmap={"chores": 1.5, "commute": 1.5}, pair="music")),
            ("D=1.5 + pair friend",dict(Dmap={"chores": 1.5, "commute": 1.5}, pair="friends")),
            ("D=1.5 + reframe +0.2", dict(Dmap={"chores": 1.5, "commute": 1.5}, reframe=0.2)),
            ("D=1.5 + A=4", dict(Dmap={"chores": 1.5, "commute": 1.5}, A=4)),
            ("pair friend + reframe +0.2", dict(pair="friends", reframe=0.2)),
        ]
    for e in [0.5, 0.8]:
        for r in [2.0, 3.0]:
            base = cond(r, e)
            print(f"\n== e={e} r={r} ==")
            print(f"{'lever':28s} mund   day   near   neg   d_music d_friend")
            for lab, kw in LEVERS + extra:
                c = base if lab == "baseline" else cond(r, e, **kw)
                print(f"{lab:28s} {c['mund']:5.2f} {c['mean']:5.2f} {c['near']:5.1%} {c['neg']:5.1%}"
                      f"  {c['music']-base['music']:+5.2f}  {c['friends']-base['friends']:+5.2f}")
