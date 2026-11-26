"""Death salience over a lifespan, and practices that answer it.

Fear of death is modelled as one more source of distress: a death-salience signal S(age) that
hurts in proportion to resistance, captures attention, and competes with pleasure for slots.
The question is which response pays over a finite life:

  general   equanimity practice (lowers resistance to all distress)
  targeted  death practice, e.g. maranasati or Epicurean argument (lowers resistance to death
            dread only, learns faster on that target, but exposure raises salience while practising)
  meaning   a standing level of meaning (lowers resistance to all distress, no slots)
  aside     both practices, with dread set aside (suppressed) outside practice
  avoid     suppression: felt dread drops now, a share returns later (rebound) and suppressing
            costs attention

Per quarter (age 20 to 100, Gompertz survival weights, no sampling of the death date):
  S      = profile(age) + bereavement spikes (rate rises with age, half-life 1 year)
           + exposure while doing targeted practice
  R_d    = R0 (1 - kE e)(1 - kX x)(1 - kMd m)       resistance to death dread
  R_o    = R0 (1 - kE e)(1 - tX kX x)(1 - kM m)    resistance to ordinary distress (tX = transfer)
  dread  = S R_d (1 - supp) + rebound release      ordinary suffering = O R_o, O ~ random inflow
  slots  = A - practice - suppression load - capture (dread + ordinary suffering)
  joy    = slots * (1 + sigma * min(S,1) * kX x)
           (finitude held through reflective death practice raises savoring; sigma is swept)
  value  = joy - LAM * (dread + ordinary)
Facing dread also habituates on its own: x grows by hab * felt dread each quarter (exposure
logic); suppressed dread does not count. Skills grow with practice (diminishing returns, learning damped by current distress) and decay
without it. Values are reported per lived year, survival-weighted, averaged over seeds.
"""
import itertools
import numpy as np

# Calibrated against prior-art/death.md:
#  prof "falling": death anxiety peaks in the 20s and declines (Russac 2007; Gesser/Wong 1988)
#  gX = 2.5 x gE: exposure-style CBT moves death anxiety far more than nonspecific practice
#     (Menzies 2018: CBT g~1.7 from few trials, others g~0.2), discounted as an upper bound
#  expo 0.2: exposure raises distress in-session (general exposure-therapy inference)
#  sigma 0.2, and only via death-specific reflection x: savoring gains need vivid or reflective
#     framing (Cozzolino 2004; Frias 2011; O'Brien & Ellsworth 2012), small and short-lived
#  rebound 0.25, supp_load 0.25: delayed rebound is real but small (Arndt 1997; Many Labs 4)
#  kMd 0.2 < kM 0.4: meaning buffers despair more than fear (Breitbart 2015)
P = dict(A=10.0, R0=1.0, kE=0.6, kX=0.8, kM=0.4, kMd=0.2, tX=0.15, LAM=2.0, cap=0.6,
         gE=0.06, gX=0.15, decay=0.01, expo=0.2, sigma=0.2,
         O_rate=0.3, O_size=1.0, O_fade=0.5, supp=0.6, rebound=0.25, rel=0.08, supp_load=0.25, hab=0.005,
         bereave0=0.02, bereave_slope=0.003, spike=1.0, prof="falling", meaning=0.0)
QUARTERS = np.arange(20, 100, 0.25)
SEEDS = 24


def profile(age, kind):
    t = (age - 20) / 70
    if kind == "rising":    # salience grows as death nears
        return 0.2 + 0.8 * t ** 1.5
    if kind == "falling":   # anxiety peaks young, then declines (adult-development pattern)
        return 0.2 + 0.6 * np.exp(-(age - 20) / 20)
    if kind == "bump":      # falls from youth with a midlife bump
        return 0.2 + 0.5 * np.exp(-(age - 20) / 20) + 0.3 * np.exp(-((age - 55) / 8) ** 2)
    return 0.4 + 0 * t      # flat


def survival(ages):
    # Gompertz hazard per year, normalised to ~ 80-year median from age 20
    h = 0.0001 * np.exp(0.085 * (ages - 20)) * 2.2
    S = np.exp(-np.cumsum(h * 0.25))
    return S


SURV = survival(QUARTERS)


def practice_plan(policy, age, q, S_now):
    """Return (general slots, targeted slots, suppress?) for this quarter."""
    kind, start = policy.get("kind", "none"), policy.get("start", 20)
    if kind == "none" or age < start:
        return 0, 0, policy.get("avoid", False)
    heavy = age < start + 15
    on = (heavy and True) or (q % 3 == 0)
    if policy.get("when_high") and S_now < 1.0:
        on = False
    g = 1.0 if on else 0.0
    if kind == "general":
        return g, 0, False
    if kind == "targeted":
        return 0, g, False
    av = policy.get("avoid", False)
    if kind == "both":   # alternate quarters, same total slots
        return (g, 0, av) if q % 2 == 0 else (0, g, av)
    if kind == "avoid":
        return 0, 0, True
    raise ValueError(kind)


def run(policy, seed, p=P, horizon=None):
    rng = np.random.default_rng(seed)
    e = x = 0.0
    O = spikes = store = 0.0
    m = p["meaning"]
    vals, joys, dreads = [], [], []
    for q, age in enumerate(QUARTERS):
        if horizon is not None and age >= 20 + horizon:
            break
        # environment
        if rng.random() < p["O_rate"]:
            O += p["O_size"] * rng.exponential(1.0)
        rate = (p["bereave0"] + p["bereave_slope"] * max(0, age - 20) / 10) * 1.0
        if rng.random() < rate:
            spikes += p["spike"]
        base = profile(age, p["prof"])
        S_now = base + spikes
        gs, ts, avoid = practice_plan(policy, age, q, S_now)
        S = S_now + p["expo"] * ts
        R_d = p["R0"] * (1 - p["kE"] * e) * (1 - p["kX"] * x) * (1 - p["kMd"] * m)
        R_o = p["R0"] * (1 - p["kE"] * e) * (1 - p["tX"] * p["kX"] * x) * (1 - p["kM"] * m)
        felt = S * R_d
        release = p["rel"] * store
        store -= release
        if avoid:
            hidden = felt * p["supp"]
            store += hidden * p["rebound"]
            felt -= hidden
        faced = felt  # dread actually felt is what habituates (suppressed dread does not)
        dread = felt + release
        ordinary = O * R_o
        load = p["supp_load"] if avoid else 0.0
        capture = dread + ordinary
        slots = max(0.0, p["A"] - gs - ts - load - capture)
        joy = slots * (1 + p["sigma"] * min(S, 1.0) * p["kX"] * x)
        v = joy - p["LAM"] * (dread + ordinary)
        vals.append(v); joys.append(joy); dreads.append(dread)
        # learning, damped by distress (calm is hard to learn in a spike)
        damp = 1.0 / (1.0 + capture)
        if gs:
            e += p["gE"] * damp * (p["cap"] - e) / p["cap"] * gs * p["cap"]
        else:
            e *= 1 - p["decay"]
        if ts:
            x += p["gX"] * damp * (p["cap"] - x) / p["cap"] * ts * p["cap"]
        else:
            x *= 1 - p["decay"]
        x += p["hab"] * faced * (p["cap"] - x)   # natural habituation to faced dread
        O *= 1 - p["O_fade"]
        spikes *= 0.5 ** 0.25
    n = len(vals)
    w = SURV[:n]
    vals, joys, dreads = map(np.array, (vals, joys, dreads))
    per_year = lambda a: float((a * w).sum() / w.sum())
    return per_year(vals), per_year(joys), per_year(dreads), e, x


def M(policy, p=P, horizon=None):
    r = np.array([run(policy, s, p, horizon)[:3] for s in range(SEEDS)])
    return r.mean(0)


def with_p(**kw):
    q = dict(P); q.update(kw); return q


POLICIES = {
    "none": dict(kind="none"),
    "avoid (suppress)": dict(kind="avoid"),
    "general equanimity": dict(kind="general"),
    "targeted death practice": dict(kind="targeted"),
    "both, alternating": dict(kind="both"),
    "both + set dread aside otherwise": dict(kind="both", avoid=True),
    "targeted, only when salience high": dict(kind="targeted", when_high=True),
    "general, only when salience high": dict(kind="general", when_high=True),
}

if __name__ == "__main__":
    base = M(POLICIES["none"])[0]
    print(__doc__.split("\n")[0])
    print("Calibrated defaults: dread falls with age, gX=2.5 gE, expo 0.2, sigma 0.2 via reflection only.")
    print("Value per lived year (survival-weighted). LAM=2, meaning 0, practice 1 slot of 10,")
    print("every quarter for 15 years from start, then every 3rd quarter.\n")

    print("D1. Policy x how dread changes with age (value; gain over none in brackets)")
    profs = ["rising", "falling", "bump", "flat"]
    print("   %-36s" % "policy" + "".join("%18s" % k for k in profs))
    best = {}
    for name, pol in POLICIES.items():
        row = []
        for pr in profs:
            v = M(pol, with_p(prof=pr))[0]
            b = M(POLICIES["none"], with_p(prof=pr))[0]
            row.append("%8.3f (%+.3f)" % (v, v - b))
            best.setdefault(pr, []).append((v, name))
        print("   %-36s" % name + "".join("%18s" % c for c in row))
    for pr in profs:
        print("   best under %-8s: %s" % (pr, max(best[pr])[1]))

    print("\nD2. When to start (targeted and general), rising vs falling dread")
    for pr in ["rising", "falling"]:
        for kind in ["general", "targeted"]:
            b = M(POLICIES["none"], with_p(prof=pr))[0]
            cells = []
            for st in [20, 35, 50, 65, 80]:
                v = M(dict(kind=kind, start=st), with_p(prof=pr))[0]
                cells.append("start %d %+.3f" % (st, v - b))
            print("   %-8s %-9s " % (pr, kind) + "  ".join(cells))

    print("\nD3. Targeted vs general: depends on how much of your distress is about death")
    print("   (ordinary stressor rate O_rate, and targeted learning speed gX relative to gE=0.06; calibrated 0.15)")
    print("   %-10s" % "O_rate" + "".join("%26s" % ("gX=%.2f T-G" % g) for g in [0.06, 0.09, 0.15, 0.24]))
    for o in [0.0, 0.15, 0.3, 0.6]:
        row = []
        for g in [0.06, 0.09, 0.15, 0.24]:
            pp = with_p(O_rate=o, gX=g)
            t = M(POLICIES["targeted death practice"], pp)[0]
            gn = M(POLICIES["general equanimity"], pp)[0]
            bo = M(POLICIES["both, alternating"], pp)[0]
            win = max([(t, "T"), (gn, "G"), (bo, "B")])[1]
            row.append("%+.3f best %s" % (t - gn, win))
        print("   %-10.2f" % o + "".join("%26s" % c for c in row))

    print("\nD4. Avoidance: good now, bad later? (gain over none, by horizon in years)")
    for pr in ["rising", "falling"]:
        cells = []
        for hz in [2, 5, 10, 20, 40, 80]:
            pp = with_p(prof=pr)
            d = M(POLICIES["avoid (suppress)"], pp, hz)[0] - M(POLICIES["none"], pp, hz)[0]
            cells.append("%2dy %+.3f" % (hz, d))
        print("   %-8s " % pr + "  ".join(cells))
    print("   natural habituation hab (falling, lifetime gain of avoid over none):  " + "  ".join(
        "hab %.3f %+.3f" % (h, M(POLICIES["avoid (suppress)"], with_p(hab=h))[0]
                              - M(POLICIES["none"], with_p(hab=h))[0]) for h in [0.0, 0.005, 0.01, 0.02]))
    print("   sensitivity (falling, lifetime): rebound share x attention load")
    for rb in [0.0, 0.25, 0.5, 1.0]:
        cells = []
        for ld in [0.0, 0.25, 0.5]:
            pp = with_p(rebound=rb, supp_load=ld)
            d = M(POLICIES["avoid (suppress)"], pp)[0] - M(POLICIES["none"], pp)[0]
            cells.append("load %.2f %+.3f" % (ld, d))
        print("     rebound %.2f  " % rb + "  ".join(cells))

    print("   suppression strength supp (falling, lifetime; avoid minus none | 'both+aside' minus 'both'):")
    for sp in [0.1, 0.2, 0.4, 0.6]:
        pp = with_p(supp=sp)
        print("     supp %.1f  avoid %+.3f   aside %+.3f" % (
            sp, M(POLICIES["avoid (suppress)"], pp)[0] - M(POLICIES["none"], pp)[0],
            M(POLICIES["both + set dread aside otherwise"], pp)[0] - M(POLICIES["both, alternating"], pp)[0]))

    print("\nD5. Exposure cost and finitude savoring (targeted minus general; falling dread)")
    print("   %-12s" % "expo" + "".join("%16s" % ("sigma=%.2f" % s) for s in [0.0, 0.1, 0.2, 0.4]))
    for ex in [0.0, 0.1, 0.2, 0.4]:
        row = []
        for s in [0.0, 0.1, 0.2, 0.4]:
            pp = with_p(expo=ex, sigma=s)
            row.append("%+.3f" % (M(POLICIES["targeted death practice"], pp)[0]
                                   - M(POLICIES["general equanimity"], pp)[0]))
        print("   %-12.1f" % ex + "".join("%16s" % c for c in row))
    print("   does salience itself pay once accepted? value of none vs targeted when sigma high:")
    for s in [0.0, 0.4, 1.0]:
        pp = with_p(sigma=s)
        print("     sigma %.1f: none %.3f  targeted %.3f  joy none %.3f  joy targeted %.3f" % (
            s, M(POLICIES["none"], pp)[0], M(POLICIES["targeted death practice"], pp)[0],
            M(POLICIES["none"], pp)[1], M(POLICIES["targeted death practice"], pp)[1]))

    print("\nD6. Meaning as a substitute (gain over none, by meaning level; falling)")
    for m in [0.0, 0.5, 1.0]:
        pp = with_p(meaning=m)
        b = M(POLICIES["none"], pp)[0]
        g = M(POLICIES["general equanimity"], pp)[0] - b
        t = M(POLICIES["targeted death practice"], pp)[0] - b
        print("   meaning %.1f: none %.3f  general %+.3f  targeted %+.3f" % (m, b, g, t))

    print("\nD7. Robustness: winner across LAM, decay, profile and suppression strength")
    keys = ["none", "avoid (suppress)", "general equanimity", "targeted death practice", "both, alternating",
            "both + set dread aside otherwise"]
    tally = {}
    rows = []
    for lam, dec, pr, sp in itertools.product([1, 2, 3, 5], [0.003, 0.01, 0.03], ["falling", "bump", "rising"],
                                              [0.2, 0.6]):
        pp = with_p(LAM=lam, decay=dec, prof=pr, supp=sp)
        vs = {k: M(POLICIES[k], pp)[0] for k in keys}
        w = max(vs, key=vs.get)
        tally[w] = tally.get(w, 0) + 1
        avoid_bad = vs["avoid (suppress)"] < vs["none"]
        rows.append((lam, dec, pr, w, avoid_bad, sp))
    for k in keys:
        print("   %-26s wins %2d / %d" % (k, tally.get(k, 0), len(rows)))
    print("   avoidance worse than doing nothing in %d / %d" % (sum(r[4] for r in rows), len(rows)))
    for sp in [0.2, 0.6]:
        sub = [r for r in rows if r[5] == sp]
        print("   supp %.1f winners: %s" % (sp, {k: sum(r[3] == k for r in sub) for k in keys if any(r[3] == k for r in sub)}))
    print("   winners at fast decay 0.03: %s" % sorted({r[3] for r in rows if r[1] == 0.03}))
    print("   winners at LAM=1: %s" % sorted({r[3] for r in rows if r[0] == 1}))
