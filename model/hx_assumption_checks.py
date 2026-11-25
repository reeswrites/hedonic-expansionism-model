"""Assumption checks on the combined model (hx_combined.py), which is imported, not edited.

1. Suffering weight sweep: LAM in {1, 1.5, 2, 3, 5} (LOSS, the shortfall weight on pleasure
   below its reference, held at 2), plus a joint LAM = LOSS sweep for the life gap only.
   Re-runs claims 1-7, 9-11 (claim 8, pairs, does not use LAM) and the default-vs-expansionist gap.
2. Pain adapts slower than pleasure (Perez-Truglia 2012). In hx_combined the only way distress
   S fades on its own is FADE (5% per period), which plays the role of suffering's habituation;
   pleasure adapts through reference points and satiety. Here FADE is scaled by f in
   {1.0 (current), 0.5, 0.2, 0}. Re-runs claims 3, 4, 9 and the life gap.
3. Equanimity as a costly skill: e and concept release cr grow only by spending slots on practice
   (diminishing returns toward a cap, as in hx_combined), and now decay 1% per period without
   practice. Practice policies are compared under ordinary and chronic distress (inflow 0.3).
4. Why the savoring phase adds nothing in claim 3.

Hooks: parameters are changed through hx_combined.P (restored afterwards); the practice policy and
skill decay go through a wrapper around hx_combined.plan, which run() looks up at call time.
Runs in parallel over the available cores (about 2-3 minutes on 2 cores).
"""
import contextlib
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hx_combined as H  # noqa: E402

P, M, run, LIKE = H.P, H.M, H.run, H.LIKE
ORIG_PLAN = H.plan
LAMS = [1.0, 1.5, 2.0, 3.0, 5.0]
FADES = [1.0, 0.5, 0.2, 0.0]


@contextlib.contextmanager
def params(**kw):
    """Temporarily override entries of the shared parameter set."""
    old = {k: P[k] for k in kw}
    P.update(kw)
    try:
        yield
    finally:
        P.update(old)


# ------------------------------------------------ quiet versions of the claims (numbers only)
def k1():
    V, drop = {}, {}
    for n in [2, 4, 8, 16]:
        cfg = dict(LIKE, profs=list(range(n)), skill=False)
        V[n], out = M(cfg, full=True)
        drop[n] = np.mean([V_[150:170].mean() - run(dict(cfg, remove_at=150), sd)[0][150:170].mean()
                           for sd, (V_, _) in enumerate(out)])
    return dict(V=V, drop=drop)


def k2():
    r = {}
    for lab, kw in [("ord", {}), ("chr", dict(inflow=0.3))]:
        for e, cr in [(0, 0), (0.8, 0), (0, 1), (0.8, 1)]:
            r[lab, "static", e, cr] = M(dict(LIKE, e=e, cr=cr, x=1.0, **kw))
        for order in [None, "E", "C", "EC", "CE"]:
            r[lab, order] = M(dict(LIKE, practice=order, sched={"practice": 2} if order else {}, **kw), lo=200)
    return r


def k3():
    base = dict(LIKE, S0=6.0, acq=True, sched=H.EXP_SCHED, ban=("relief",))
    rows = {"none": [dict(base)], "fixed": [dict(base, relief="fixed")],
            "gate": [dict(base, relief="gate", thr=t) for t in [0.5, 1, 2, 3]],
            "gradient": [dict(base, relief="gradient", thr=t) for t in [0.5, 1, 2, 3]],
            "two-phase": [dict(base, relief="gate", thr=t, expand_gate=t) for t in [0.5, 1, 2, 3]],
            "three-phase": [dict(base, relief="gate", thr=t, expand_gate=t2)
                            for t in [1, 2, 3] for t2 in [0.25, 0.5] if t2 < t]}
    return {k: max(M(c, hi=150) for c in cfgs) for k, cfgs in rows.items()}


def k4():
    base = dict(LIKE, S0=6.0, numb=True, shocks=False, skill=False, ban=("relief", "numb"))
    return {name: M(dict(base, **kw), hi=150) for name, kw in
            [("nothing", {}), ("bridge", dict(numb_habit=99, numb_first=2)),
             ("habit>0.5", dict(numb_habit=0.5)), ("habit>2", dict(numb_habit=2.0))]}


def k5():
    def uses(cfg):
        m, out = M(cfg, full=True)
        return m, np.mean([o[1]["uses"].get("skill", 0) + o[1]["uses"].get("sensitizing", 0) for o in out])
    base = dict(feed=True)
    r = {pi: uses(dict(base, pi=pi))[0] for pi in [1.0, 0.5, 0.0]}
    ref, b = uses(dict(base, pi=0.0))[1], uses(dict(base, pi=1.0))[1]
    rec = {n: (uses(dict(base, pi=1.0, **kw))[1] - b) / (ref - b + 1e-9)
           for n, kw in [("flat salience", dict(sal="flat")), ("no sensitization", dict(sens_on=0))]}
    return dict(V=r, rec=rec)


def k6():
    r = {}
    for name, kw in [("massed", dict(sched={"acquired": 1}, burst=3)), ("spaced", dict(sched={"acquired": 3})),
                     ("spaced S0=5", dict(sched={"acquired": 3}, S0=5.0))]:
        out = [run(dict(LIKE, acq=True, skill=False, **kw), s) for s in range(20)]
        r[name] = np.mean([not next(x for x in o[1]["W"] if x["kind"] == "acquired")["quit"] for o in out])
    return r


def k7():
    r = {}
    for tname, kw in {"average": {}, "low soc": dict(gamma=0.6), "solitude": dict(gamma=0.8, rho_al=0.10)}.items():
        solo = M(dict(LIKE, profs=list(range(8)), people=0, **kw))
        soc = {n: max(M(dict(LIKE, profs=list(range(8)), people=n, soc_slots=k, ban=("social",), **kw))
                      for k in [1, 2]) for n in [1, 2, 3, 6]}
        bn = max(soc, key=soc.get)
        r[tname] = (solo, bn, soc[bn])
    return r


def k9():
    base = [run(dict(LIKE, skill=False), s)[0] for s in range(8)]
    r = {}
    for k in ["material", "sensory", "social", "skill", "relief", "sensitizing"]:
        d = np.array([run(dict(LIKE, skill=False, add=k), s)[0] - base[s] for s in range(8)])
        a, b = d[:, 100:200].mean(), d[:, 200:300].mean()
        r[k] = (a, b, b / a if a > 0 else np.nan)
    return r


def k10():
    return {(a, e): M(dict(LIKE, a=a, e=e)) for a in [0.2, 0.5, 0.8] for e in [0.0, 0.8]}


def k11():
    return {f: M(dict(pi=0.8, feed=f)) for f in [True, False]}


def lives():
    d, x = M(H.DEFAULT, 10), M(H.EXPANSIONIST, 10)
    dn = M(dict(H.DEFAULT, numb=False), 10)
    return dict(d=d, x=x, gap=x - d, dn=dn, gap_nonumb=x - dn)


CLAIMS = dict(k1=k1, k2=k2, k3=k3, k4=k4, k5=k5, k6=k6, k7=k7, k9=k9, k10=k10, k11=k11, lives=lives)


def verdicts(r):
    """Turn claim numbers into yes/no verdicts, matching the wording of theory.md 6b."""
    v = {}
    if "k1" in r:
        V, dr = r["k1"]["V"], r["k1"]["drop"]
        v["1 breadth bounded, buffers loss"] = (V[16] - V[8] < 0.25 * (V[8] - V[2]) and dr[16] < dr[2] / 2,
                                               f"+{V[8] - V[2]:.2f}/+{V[16] - V[8]:.2f} loss {dr[2]:.2f}->{dr[16]:.2f}")
    if "k2" in r:
        q = r["k2"]
        inter = q["chr", "static", 0.8, 1] - q["chr", "static", 0.8, 0] - q["chr", "static", 0, 1] + q["chr", "static", 0, 0]
        v["2a calm skills complementary (chronic)"] = (inter > 0.1, f"interaction {inter:+.2f}")
        for lab in ["ord", "chr"]:
            d = q[lab, "EC"] - q[lab, "CE"]
            v[f"2b equanimity-first beats release-first ({lab})"] = (d > 0.05, f"EC-CE {d:+.2f}")
    if "k3" in r:
        q = r["k3"]
        v["3a any relief beats none"] = (max(q["gate"], q["gradient"]) - q["none"] > 0.1,
                                         f"+{max(q['gate'], q['gradient']) - q['none']:.2f}")
        v["3b gradient beats gate"] = (q["gradient"] - q["gate"] > 0.02, f"{q['gradient'] - q['gate']:+.3f}")
        v["3c savoring phase adds value"] = (q["three-phase"] - q["two-phase"] > 0.02,
                                             f"{q['three-phase'] - q['two-phase']:+.3f}")
    if "k4" in r:
        q = r["k4"]
        v["4 habitual numbing worse than nothing"] = (q["habit>0.5"] < q["nothing"],
                                                      f"{q['habit>0.5']:.2f} vs {q['nothing']:.2f}")
    if "k5" in r:
        q = r["k5"]
        v["5a urge steering less helps"] = (q["V"][0.0] > q["V"][0.5] > q["V"][1.0], f"pi0-pi1 {q['V'][0.0] - q['V'][1.0]:+.2f}")
        v["5b salience is main cause of underuse"] = (q["rec"]["flat salience"] > q["rec"]["no sensitization"],
                                                      f"{q['rec']['flat salience']:.0%} vs {q['rec']['no sensitization']:.0%}")
    if "k6" in r:
        q = r["k6"]
        v["6 spacing decides acquisition"] = (q["spaced"] > q["massed"] + 0.1, f"{q['spaced']:.0%} vs {q['massed']:.0%}")
    if "k7" in r:
        q = r["k7"]
        v["7a few close people beat solo (average)"] = (q["average"][2] > q["average"][0] and q["average"][1] <= 6,
                                                        f"best n={q['average'][1]} +{q['average'][2] - q['average'][0]:.2f}")
        v["7b solo wins for low sociability"] = (q["low soc"][0] >= q["low soc"][2],
                                                 f"{q['low soc'][0] - q['low soc'][2]:+.2f}")
    if "k9" in r:
        q = r["k9"]
        ok = all(q[k][2] >= 0.9 for k in ["skill", "sensitizing", "relief"]) and q["material"][2] < 0.7
        v["9 skill/sens/relief last, material fades"] = (ok, " ".join(f"{k[:4]} {q[k][2]:.0%}" for k in
                                                         ["material", "skill", "sensitizing", "relief"]))
    if "k10" in r:
        q = r["k10"]
        ok = q[0.5, 0.0] > max(q[0.2, 0.0], q[0.8, 0.0]) and q[0.8, 0.0] < q[0.2, 0.0]
        v["10 moderate arousal best, high worst w/o eq."] = (ok, f"a.2 {q[0.2, 0.0]:.2f} a.5 {q[0.5, 0.0]:.2f} a.8 {q[0.8, 0.0]:.2f}")
    if "k11" in r:
        v["11 engineered feed lowers V"] = (r["k11"][True] < r["k11"][False],
                                            f"{r['k11'][True]:.2f} vs {r['k11'][False]:.2f}")
    if "lives" in r:
        q = r["lives"]
        v["gap expansionist - default"] = (q["gap"] > 0.5, f"{q['gap']:+.2f} (no-numb world {q['gap_nonumb']:+.2f})")
    return v


# ------------------------------------------------ check 3: equanimity as a costly skill
DECAY = 0.01
POLICIES = {"none": lambda t, S: False,
            "constant: 1 slot every 3rd period": lambda t, S: t % 3 == 0,
            "heavy early (t<60) then every 6th": lambda t, S: t < 60 or t % 6 == 0,
            "heavy early only, no maintenance": lambda t, S: t < 60,
            "only when distressed (S>1.5)": lambda t, S: S > 1.5}


def practice_plan(policy, decay=DECAY):
    """Wrap plan(): decay e and cr after a period without practice; add a practice slot by policy."""
    def plan(t, W, st, cfg):
        pr = next(s for s in W if s["kind"] == "practice")
        if t > 0 and pr["uses"] == pr.get("seen", 0):
            st["e"] -= decay * st["e"]
            st["cr"] -= decay * st["cr"]
        pr["seen"] = pr["uses"]
        out = ORIG_PLAN(t, W, st, cfg)
        return ([pr] if POLICIES[policy](t, st["S"]) else []) + out
    return plan


def k_practice(policy, order, inflow, decay=DECAY, seeds=10):
    H.plan = practice_plan(policy, decay)
    try:
        out = [run(dict(LIKE, practice=order, inflow=inflow), s) for s in range(seeds)]
    finally:
        H.plan = ORIG_PLAN
    Vs = np.array([o[0] for o in out])
    return dict(V=Vs.mean(0), e=np.mean([o[1]["st"]["e"] for o in out]), cr=np.mean([o[1]["st"]["cr"] for o in out]),
                slots=np.mean([o[1]["uses"].get("practice", 0) for o in out]) / (P["T"] * P["SLOTS"]))


# ------------------------------------------------ check 4: savoring phase
def k_savor(rho_p):
    base = dict(LIKE, S0=6.0, acq=True, sched=H.EXP_SCHED, ban=("relief",), relief="gate", thr=1)
    with params(RHO_P=rho_p):
        two, three = M(dict(base, expand_gate=1), hi=150), M(dict(base, expand_gate=0.5), hi=150)
    return two, three


def k_savor_window():
    """How many periods (t<150) does the agent spend in the savoring window 0.5 < S <= 1?"""
    seen = []
    def plan(t, W, st, cfg):
        if t < 150:
            seen.append(st["S"])
        return ORIG_PLAN(t, W, st, cfg)
    H.plan = plan
    try:
        out = [run(dict(LIKE, S0=6.0, acq=True, sched=H.EXP_SCHED, ban=("relief",), relief="gate", thr=1,
                        expand_gate=0.5), s) for s in range(8)]
    finally:
        H.plan = ORIG_PLAN
    S = np.array(seen)
    acq = np.mean([o[1]["uses"].get("acquired", 0) for o in out])
    return dict(window=np.mean((S > 0.5) & (S <= 1)), above=np.mean(S > 1), below=np.mean(S <= 0.5), acq=acq)


# ------------------------------------------------ parallel driver
def task(job):
    tag, overrides, fn, args = job
    with params(**overrides):
        res = CLAIMS[fn]() if fn in CLAIMS else globals()[fn](*args)
    return tag, fn, args, res


def jobs():
    J = []
    for lam in LAMS:
        for fn in CLAIMS:
            J.append((("lam", lam), dict(LAM=lam), fn, ()))
        J.append((("lamloss", lam), dict(LAM=lam, LOSS=lam), "lives", ()))
    for f in FADES:
        if f != 1.0:
            for fn in ["k3", "k4", "k9", "lives"]:
                J.append((("fade", f), dict(FADE=f * P["FADE"]), fn, ()))
    for inflow in [P["INFLOW"], 0.3]:
        for pol in POLICIES:
            J.append((("prac", inflow), {}, "k_practice", (pol, "EC", inflow)))
        for pol in ["constant: 1 slot every 3rd period", "heavy early (t<60) then every 6th"]:
            for order in ["E", "C", "CE"]:
                J.append((("order", inflow), {}, "k_practice", (pol, order, inflow)))
        for decay in [0.003, 0.03]:                  # sensitivity to the decay rate
            for pol in ["none", "constant: 1 slot every 3rd period", "heavy early (t<60) then every 6th"]:
                for order in ["EC", "CE"]:
                    J.append((("decay", inflow), {}, "k_practice", (pol, order, inflow, decay)))
    for rp in [0.0, 0.1, 0.3]:
        J.append((("savor",), {}, "k_savor", (rp,)))
    J.append((("savor",), {}, "k_savor_window", ()))
    return J


def payback(d):
    """First period after which the cumulative gain over no practice stays positive."""
    c = np.cumsum(d)
    neg = np.where(c <= 0)[0]
    return 0 if len(neg) == 0 else (None if neg[-1] == len(c) - 1 else neg[-1] + 1)


def report(R, X):
    """R: claim results by (sweep, value); X: other results by (tag, function, args)."""
    yn = lambda b: "yes" if b else "NO "
    print(__doc__.split("\n")[0], "\n")

    print("CHECK 1. Suffering weight LAM (LOSS fixed at 2). Verdict per claim; detail at each LAM.")
    V = {lam: verdicts({fn: R["lam", lam][fn] for fn in CLAIMS}) for lam in LAMS}
    print(f"   {'claim':<46}" + "".join(f"LAM={lam:<4}" for lam in LAMS) + "  changes at")
    for c in V[2.0]:
        flips = [lam for lam in LAMS if V[lam][c][0] != V[2.0][c][0]]
        print(f"   {c:<46}" + "".join(f"{yn(V[lam][c][0]):<9}" for lam in LAMS) +
              f"  {'robust' if not flips else 'differs from LAM=2 at ' + ','.join(map(str, flips))}")
    print("   detail:")
    for c in V[2.0]:
        print(f"   {c[:40]:<40} " + " | ".join(V[lam][c][1] for lam in LAMS))
    print("   gap with LAM=LOSS swept jointly: " + "  ".join(
        f"{lam}: {R['lamloss', lam]['lives']['gap']:+.2f}" for lam in LAMS))
    print("   raw lives (default / expansionist), LAM only: " + "  ".join(
        f"{lam}: {R['lam', lam]['lives']['d']:.2f}/{R['lam', lam]['lives']['x']:.2f}" for lam in LAMS))

    print("\nCHECK 2. Distress habituation (FADE) at f x current; pleasure adaptation unchanged.")
    F = {1.0: {fn: R["lam", 2.0][fn] for fn in ["k3", "k4", "k9", "lives"]}}
    F.update({f: R["fade", f] for f in FADES if f != 1.0})
    print(f"   {'':<34}" + "".join(f"f={f:<7}" for f in FADES))
    rows = [("claim 3: no relief", lambda r: r["k3"]["none"]),
            ("claim 3: best relief (gate/grad)", lambda r: max(r["k3"]["gate"], r["k3"]["gradient"])),
            ("  relief floor (best - none)", lambda r: max(r["k3"]["gate"], r["k3"]["gradient"]) - r["k3"]["none"]),
            ("  gradient - gate", lambda r: r["k3"]["gradient"] - r["k3"]["gate"]),
            ("  three-phase - two-phase", lambda r: r["k3"]["three-phase"] - r["k3"]["two-phase"]),
            ("claim 4: nothing", lambda r: r["k4"]["nothing"]),
            ("claim 4: bridge (numb 2 periods)", lambda r: r["k4"]["bridge"]),
            ("claim 4: habit (numb if S>0.5)", lambda r: r["k4"]["habit>0.5"]),
            ("claim 4: habit (numb if S>2)", lambda r: r["k4"]["habit>2"])]
    rows += [(f"claim 9 kept: {k}", (lambda k: lambda r: r["k9"][k][2])(k))
             for k in ["material", "sensory", "social", "skill", "relief", "sensitizing"]]
    rows += [(f"claim 9 late gain: relief", lambda r: r["k9"]["relief"][1]),
             ("lives: default", lambda r: r["lives"]["d"]), ("lives: expansionist", lambda r: r["lives"]["x"]),
             ("lives: gap", lambda r: r["lives"]["gap"]), ("lives: gap, no numbing in world", lambda r: r["lives"]["gap_nonumb"])]
    for name, fn in rows:
        print(f"   {name:<34}" + "".join(f"{fn(F[f]):<9.3f}" for f in FADES))
    for f in FADES:
        print(f"   f={f}: " + "  ".join(f"{c.split()[0]}:{yn(b).strip()}" for c, (b, _) in
                                       verdicts(F[f]).items()))

    print(f"\nCHECK 3. Equanimity/release as costly skills (order EC, decay {DECAY}/period unpracticed); 10 seeds")
    for inflow, lab in [(P["INFLOW"], "ordinary"), (0.3, "chronic (inflow 0.3)")]:
        res = {a[0]: x for (tag, fn, a), x in X.items() if tag == ("prac", inflow)}
        base = res["none"]["V"]
        print(f"   [{lab}] policy{'':<34} slots  V all   V t200+  e_end cr_end  payback")
        for pol, x in res.items():
            pb = payback(x["V"] - base) if pol != "none" else "-"
            print(f"   {pol:<40} {x['slots']:5.0%} {x['V'].mean():7.3f} {x['V'][200:].mean():7.3f}"
                  f"   {x['e']:.2f}  {x['cr']:.2f}    {pb if pb is not None else 'never'}")
        ords = {(a[0], a[1]): x for (tag, fn, a), x in X.items() if tag in (("order", inflow), ("prac", inflow))}
        for pol in ["constant: 1 slot every 3rd period", "heavy early (t<60) then every 6th"]:
            print(f"   [{lab}] order under '{pol}': " + "  ".join(
                f"{o} {ords[pol, o]['V'].mean():.3f}" for o in ["E", "C", "EC", "CE"]))
        dec = {a[::3] + a[1:2]: x for (tag, fn, a), x in X.items() if tag == ("decay", inflow)}
        for d in [0.003, 0.03]:
            print(f"   [{lab}] decay {d}: " + "  ".join(
                f"{p.split(':')[0].split(' (')[0]}/{o} {dec[p, d, o]['V'].mean():.3f}"
                for p in ["none", "constant: 1 slot every 3rd period", "heavy early (t<60) then every 6th"]
                for o in ["EC", "CE"] if not (p == "none" and o == "CE")))

    print("\nCHECK 4. Savoring phase (claim 3 setup, gate thr=1; two-phase expands at S<=1, three-phase at S<=0.5)")
    sv = {a[0]: x for (tag, fn, a), x in X.items() if fn == "k_savor"}
    for rp, (two, three) in sv.items():
        print(f"   RHO_P={rp}: two-phase {two:.3f}  three-phase {three:.3f}  diff {three - two:+.3f}")
    w = next(x for (tag, fn, a), x in X.items() if fn == "k_savor_window")
    print(f"   share of periods t<150 with S>1 (relief) {w['above']:.0%}, 0.5<S<=1 (savor window) {w['window']:.0%}, "
          f"S<=0.5 {w['below']:.0%}; acquired uses {w['acq']:.1f}")


if __name__ == "__main__":
    t0 = time.time()
    J = sorted(jobs(), key=lambda j: j[2] not in ("k7", "k2", "k3"))   # big jobs first
    with Pool(os.cpu_count()) as pool:
        out = pool.map(task, J, chunksize=1)
    R, X = {}, {}
    for tag, fn, args, res in out:
        if fn in CLAIMS:
            R.setdefault(tag, {})[fn] = res
        else:
            X[tag, fn, args] = res
    report(R, X)
    print(f"\n(runtime {time.time() - t0:.0f}s on {os.cpu_count()} cores)")
