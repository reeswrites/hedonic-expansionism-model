"""Hedonic expansionism, model v1: fractal liking.

Each activity has features down to a finest resolution R. At resolution r you can
tell apart N(r) = base * r^D features; coarser features are averages of the finer
ones they contain (mixed parts blur toward 'meh'). Each moment you attend to A
features: liked ones chosen by liking x freshness, plus any strongly aversive ones
that intrude on their own (negativity bias). Pleasure saturates at a ceiling;
equanimity e scales down how much the aversive features hurt.
"""
import numpy as np

BASE, R, A, CAP = 3, 4.0, 3, 3.0
ALPHA, RHO = 0.5, 0.15        # habituation per attended hour, recovery per rest hour
TAU = 0.8                     # aversiveness at which a feature intrudes on attention

# name, fractal dimension D, share of liked parts, hours per day
ACTIVITIES = [
    ("chores",   0.5, 0.50, 3),
    ("commute",  0.6, 0.45, 1),
    ("meals",    1.5, 0.75, 2),
    ("music",    1.8, 0.80, 1),
    ("friends",  1.6, 0.75, 2),
]
MUNDANE = {"chores", "commute"}

def make_world(rng):
    world = {}
    for name, D, pi, _ in ACTIVITIES:
        n = int(round(BASE * R ** D))
        pos = rng.random(n) < pi
        ell = np.where(pos, rng.exponential(1.0, n), -rng.exponential(0.8, n))
        world[name] = ell
    return world

def coarse(ell, D, r):
    n = max(1, int(round(BASE * r ** D)))
    n = min(n, len(ell))
    return np.array([c.mean() for c in np.array_split(ell, n)])

def run(r, e, seed, days=40):
    rng = np.random.default_rng(seed)
    world = make_world(rng)
    feats = {name: coarse(world[name], D, r) for name, D, _, _ in ACTIVITIES}
    fresh = {k: np.ones(len(v)) for k, v in feats.items()}
    log = []
    for _ in range(days):
        for name, D, _, hours in ACTIVITIES:
            ell, h = feats[name], fresh[name]
            for _ in range(hours):
                intrude = np.where(ell < -TAU)[0]
                intrude = intrude[np.argsort(ell[intrude])][:A]
                slots = A - len(intrude)
                liked = np.where(ell > 0)[0]
                pick = liked[np.argsort(-(ell[liked] * h[liked]))][:slots]
                pos = (ell[pick] * h[pick]).sum()
                neg = -ell[intrude].sum()
                v = CAP * np.tanh(pos / CAP) - (1 - e) * CAP * np.tanh(neg / CAP)
                used = np.zeros(len(ell), bool); used[pick] = True
                h[used] -= ALPHA * h[used]
                h[~used] += RHO * (1 - h[~used])
                log.append((name, v))
    return log

def summarize(log):
    names = np.array([n for n, _ in log]); v = np.array([x for _, x in log])
    mund = np.isin(names, list(MUNDANE))
    return dict(mean=v.mean(), near=(v > 0.6 * CAP).mean(), neg=(v < 0).mean(),
                mund=v[mund].mean(), rich=v[~mund].mean())

if __name__ == "__main__":
    seeds = range(30)
    print("r    e    mean   near-ceiling  negative  mundane  rich")
    for e in [0.0, 0.5, 0.8]:
        for r in [1.0, 1.5, 2.0, 3.0, 4.0]:
            s = [summarize(run(r, e, sd)) for sd in seeds]
            m = {k: np.mean([x[k] for x in s]) for k in s[0]}
            print(f"{r:<4} {e:<4} {m['mean']:6.2f}   {m['near']:6.1%}      {m['neg']:6.1%}  "
                  f"{m['mund']:6.2f}  {m['rich']:6.2f}")
        print()
