"""Hedonic expansionism, model v2: four skills plus expertise-driven categorizing.

Builds on v1 (fractal liking) with wall-clock recovery (hx_v1_wall.py).
Skills (Shinzen Young's three, plus concentration):
  clarity r        resolution; at r you resolve N(r) = BASE * r^D features
  equanimity e     softens pain by (1-e), raises the intrusion threshold to TAU*(1+2e),
                   and scales down judging by (1-e)
  concept release c labels don't replace sensation: positive contributions are
                   multiplied by (1 - k*(1-c)), where k is the categorizing load
  concentration A  attention slots per hour

Expertise in a domain at level x in [0,1] raises r = 1 + x*(R-1) and categorizing
load k = K0 * x together (Rocklage et al. 2021: experts classify, which numbs).

Judging: each feature is graded against a reference in its domain.
  "best"  (default): ell' = ell - J*(1-e)*JS*(ref - ell), ref = best feature (only lowers)
  "mean"  (contrast variant): ell' = ell + J*(1-e)*JS*(ell - ref), ref = mean of sampled pool
  "range" (ad hoc, Q4 only): "mean" with slope scaled by sampled range / full range
All parameters are invented.
"""
import numpy as np
import hx_model_v1 as v1

BASE, R, CAP = v1.BASE, v1.R, v1.CAP
ALPHA, RHO, TAU = v1.ALPHA, v1.RHO, v1.TAU
ACTIVITIES, MUNDANE = v1.ACTIVITIES, v1.MUNDANE
K0 = 0.6          # categorizing load at full expertise
JS = 0.1          # judging slope (0.3 makes judging swamp everything; see JS_SENS)
R_DEFAULT = 2.0   # resolution in non-expert domains
EXPERT = "music"  # the expert's domain
SEEDS, DAYS = range(30), 40


def judge(ell, J, e, mode="best", pool=None):
    """Shift liking by grading against a reference drawn from `pool` (default: all features)."""
    pool = ell if pool is None else pool
    w = J * (1 - e) * JS
    if w == 0:
        return ell.copy()
    if mode == "best":
        return ell - w * (pool.max() - ell)
    if mode == "mean":
        return ell + w * (ell - pool.mean())
    # "range" (ad hoc): contrast slope grows with how much of the quality range was sampled
    return ell + w * (ell - pool.mean()) * np.ptp(pool) / np.ptp(ell)


def run(res, k, e=0.0, c=0.0, A=3, J=1.0, seed=0, days=DAYS):
    """res, k: dicts activity -> resolution / categorizing load. Returns log of (name, v, pos, neg)."""
    rng = np.random.default_rng(seed)
    world = v1.make_world(rng)
    tau = TAU * (1 + 2 * e)
    feats = {n: judge(v1.coarse(world[n], D, res[n]), J, e) for n, D, _, _ in ACTIVITIES}
    fresh = {n: np.ones(len(f)) for n, f in feats.items()}
    log = []
    for _ in range(days):
        for name, _, _, hours in ACTIVITIES:
            ell = feats[name]
            dull = 1 - k[name] * (1 - c)
            for _ in range(hours):
                h = fresh[name]
                intr = np.where(ell < -tau)[0]
                intr = intr[np.argsort(ell[intr])][:A]
                liked = np.where(ell > 0)[0]
                pick = liked[np.argsort(-(ell[liked] * h[liked]))][:A - len(intr)]
                pos = dull * (ell[pick] * h[pick]).sum()
                neg = -ell[intr].sum()
                p_part = CAP * np.tanh(pos / CAP)
                n_part = (1 - e) * CAP * np.tanh(neg / CAP)
                log.append((name, p_part - n_part, p_part, n_part))
                for n2 in fresh:  # wall-clock recovery
                    used = np.zeros(len(fresh[n2]), bool)
                    if n2 == name:
                        used[pick] = True
                    fresh[n2][used] -= ALPHA * fresh[n2][used]
                    fresh[n2][~used] += RHO * (1 - fresh[n2][~used])
    return log


def expert_setup(x, k_on=True, everywhere=False):
    """Resolution/load dicts for expertise level x in the expert domain (or all domains)."""
    res, k = {}, {}
    for n, *_ in ACTIVITIES:
        hit = everywhere or n == EXPERT
        res[n] = 1 + x * (R - 1) if hit else R_DEFAULT
        k[n] = (K0 * x if k_on else 0.0) if hit else 0.0
    return res, k


def summarize(log, domains=None):
    rows = [(v, p, q) for n, v, p, q in log if domains is None or n in domains]
    v = np.array([r[0] for r in rows])
    return dict(val=v.mean(), near=(v > 0.6 * CAP).mean(), neg=(v < 0).mean(),
                inten=np.abs(v).mean(), pos=np.mean([r[1] for r in rows]),
                pain=np.mean([r[2] for r in rows]))


def avg(fn, domains=None):
    s = [summarize(fn(sd), domains) for sd in SEEDS]
    return {key: np.mean([x[key] for x in s]) for key in s[0]}


RICH = [n for n, *_ in ACTIVITIES if n not in MUNDANE]


def q1():
    print("Q1  expertise in music (e=0, c=0): expert-domain valence / %neg")
    print("cells: valence / %neg / pos-part (how strongly liked features register)")
    print("x     r     k     clarity-only            +categorizing           +cat+judging")
    for x in [0, 0.25, 0.5, 0.75, 1.0]:
        cells = []
        for k_on, J in [(False, 0), (True, 0), (True, 1)]:
            res, k = expert_setup(x, k_on)
            m = avg(lambda sd: run(res, k, J=J, seed=sd), [EXPERT])
            cells.append(f"{m['val']:5.2f}/{m['neg']:5.1%}/{m['pos']:4.2f}")
        print(f"{x:<5} {1 + 3 * x:<5} {K0 * x:<5.2f} " + "   ".join(cells))


def q2():
    res, k = expert_setup(0.0)
    base = avg(lambda sd: run(res, k, seed=sd), [EXPERT])
    print(f"\nQ2  full expertise, judging on. Novice reference (x=0,e=0,c=0): "
          f"val {base['val']:.2f}, near {base['near']:.1%}, neg {base['neg']:.1%}")
    print("c     e     val    near   neg")
    res, k = expert_setup(1.0)
    for c in [0, 0.5, 1]:
        for e in [0, 0.5, 0.8]:
            m = avg(lambda sd: run(res, k, e=e, c=c, seed=sd), [EXPERT])
            print(f"{c:<5} {e:<5} {m['val']:5.2f}  {m['near']:5.1%}  {m['neg']:5.1%}")


def q3():
    for x in [0.75, 1.0]:
        print(f"\nQ3  dissociation at expertise x={x} (expert domain)")
        print("profile              val   inten  %neg   pos-part  pain-part")
        res, k = expert_setup(x)
        for label, e, c in [("neither  e0 c0", 0, 0), ("calm-dull e.8 c0", 0.8, 0),
                            ("vivid    e0 c1", 0, 1), ("both     e.8 c1", 0.8, 1)]:
            m = avg(lambda sd: run(res, k, e=e, c=c, seed=sd), [EXPERT])
            print(f"{label:<20} {m['val']:5.2f}  {m['inten']:5.2f}  {m['neg']:5.1%}  "
                  f"{m['pos']:6.2f}    {m['pain']:6.2f}")


def js_sens():
    """How much the judging slope matters at full expertise, e=0.8, c in {0,1}."""
    global JS
    print("\nJudging-slope sensitivity (x=1, e=0.8): JS  c=0 val  c=1 val")
    res, k = expert_setup(1.0)
    for js in [0.0, 0.1, 0.2, 0.3]:
        JS, row = js, []
        for c in [0, 1]:
            row.append(avg(lambda sd: run(res, k, e=0.8, c=c, seed=sd), [EXPERT])["val"])
        print(f"  {js:<4} {row[0]:6.2f}  {row[1]:6.2f}")
    JS = 0.1


def q4():
    """Stuppy-style: grade full-resolution music features against a sampled quality band."""
    print("\nQ4  sampling width vs effective liking of top/bottom deciles (music, r=R, e=0)")
    print("mode  width   top-decile  bottom-decile  spread")
    D = dict((n, d) for n, d, *_ in ACTIVITIES)[EXPERT]
    for mode in ["best", "mean", "range"]:
        for width in [0.0, 0.2, 0.5, 1.0]:
            tops, bots = [], []
            for sd in SEEDS:
                ell = v1.coarse(v1.make_world(np.random.default_rng(sd))[EXPERT], D, R)
                q = np.sort(ell)
                lo, hi = np.quantile(ell, [0.5 - width / 2, 0.5 + width / 2])
                pool = ell[(ell >= lo) & (ell <= hi)] if width > 0 else np.array([np.median(ell)])
                eff = judge(ell, 1.0, 0.0, mode, pool) if width > 0 else ell
                n10 = max(1, len(ell) // 10)
                order = np.argsort(ell)
                tops.append(eff[order[-n10:]].mean()); bots.append(eff[order[:n10]].mean())
            t, b = np.mean(tops), np.mean(bots)
            tag = "none " if width == 0 else f"{width:<5}"
            print(f"{mode:<5} {tag}   {t:6.2f}      {b:6.2f}        {t - b:5.2f}")


def q5():
    print("\nQ5  training paths (skills rise with t in all domains; judging on)")
    print("t     path              mean   rich   mund   %neg")
    paths = {"clarity only": lambda t: (0, 0), "clarity+release": lambda t: (0, t),
             "clarity+equanim": lambda t: (0.8 * t, 0), "clarity+both": lambda t: (0.8 * t, t)}
    for t in [0, 0.33, 0.67, 1.0]:
        res, k = expert_setup(t, everywhere=True)
        for label, f in paths.items():
            e, c = f(t)
            a = avg(lambda sd: run(res, k, e=e, c=c, seed=sd))
            ri = avg(lambda sd: run(res, k, e=e, c=c, seed=sd), RICH)
            mu = avg(lambda sd: run(res, k, e=e, c=c, seed=sd), list(MUNDANE))
            print(f"{t:<5} {label:<17} {a['val']:5.2f}  {ri['val']:5.2f}  {mu['val']:5.2f}  {a['neg']:5.1%}")
        print()


if __name__ == "__main__":
    q1(); q2(); q3(); q4(); q5(); js_sens()
