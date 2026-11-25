"""Adaptation ladder: several clocks of hedonic adaptation instead of one dial.

Extends hx_yield_reference.py. Each period has SLOTS uses. A source has a KIND:
  material     a purchase/circumstance: yields every period without a slot (passive)
  sensory      an item with a sensory PROFILE id; satiety spills over within a profile
  social       a person/activity; no profile spillover
  skill        liking grows with use while learnable structure remains
  relief       regenerating deficit D; yields 0.8*D; exempt from the reference point
  sensitizing  liking multiplier rises with regular use, falls slowly with deprivation
Clocks, fastest to slowest:
  satiety h    drops on use by alpha_kind * mode; SPILL of that drop hits same-profile items.
               mode: focused x1.5 / background x0.6 (background also yields x0.5 -- assumption);
               forced x1.5 / chosen x1.0; interrupted session: drop x0.6 and yield x1.1.
               Recovery (Rankin et al. 2009): rate rises with use-frequency EMA; using an item
               below h=0.2 (past the plateau) slows its recovery for 6 periods.
  motivation   'wanting' habituates MOTF times faster than h and recovers slower (ration monotony).
  novelty m    depletes with use, recovers slowly by forgetting; yield factor 0.7+0.6*m.
  reference    one per kind: R_k' = R_k + K_REF*(phi_k*yield_k - R_k), compared PER USE
               (per period for material); R_k decays toward 0 when the kind goes unused.
Experienced value = relief + sum over uses of gain(y - R_kind), shortfalls weighted LOSS.
Policies: greedy (oracle: true l*h*novelty), wanting (salience*motivation*liking),
log (an external liking log: logged rating * freshness guessed from time since last use).
All parameters are invented; read results as directions, not sizes.
"""
import numpy as np

T, SLOTS, LOSS, K_REF, REC, SPILL, SEEDS = 400, 2, 2.0, 0.03, 0.25, 0.5, 20
PHI0 = dict(material=0.95, sensory=0.5, social=0.3, skill=0.3, sensitizing=0.2, relief=0.0)
ALPHA = dict(material=0.0, sensory=0.30, social=0.20, skill=0.20, sensitizing=0.15, relief=0.0)
SAL_BIASED = dict(material=1.0, sensory=1.0, social=0.7, skill=0.6, sensitizing=0.7, relief=1.0)
SAL_FLAT = {k: 1.0 for k in PHI0}
FOCUS = dict(focused=(1.5, 1.0), background=(0.6, 0.5))   # (satiety mult, yield mult)
FORCE = dict(chosen=1.0, forced=1.5)
DEFAULT_MODE = ("focused", "chosen", False)               # focus, force, interrupted
KINDS = ["material", "sensory", "social", "skill", "relief", "sensitizing"]


def src(kind, l=1.0, prof=None, m=0.3, **kw):
    s = dict(kind=kind, l=l, prof=prof, h=1.0, m=m, mot=1.0, ema=0.0, ov=0, gap=5, uses=0,
             sens=1.0, struct=0.0, D=0.0, rate=0.0)
    s.update(kw)
    s["log"] = s["l"] * (0.7 + 0.6 * s["m"])
    return s


def base_portfolio():
    return [src("sensory", 1.0, prof=0), src("sensory", 0.9, prof=0), src("sensory", 0.9, prof=1),
            src("social", 0.9), src("material", 0.5), src("relief", rate=0.3)]


def new_source(kind):
    return dict(material=lambda: src("material", 0.8, m=1.0),
                sensory=lambda: src("sensory", 1.0, prof=2, m=1.0),
                social=lambda: src("social", 1.0, m=1.0),
                skill=lambda: src("skill", 0.5, m=1.0, struct=1.5),
                relief=lambda: src("relief", rate=0.3),
                sensitizing=lambda: src("sensitizing", 0.5, m=1.0))[kind]()


def liking(s):
    return s["l"] * s["sens"]


def nov(s):
    return 0.7 + 0.6 * s["m"]


def gain(x):
    return x if x >= 0 else LOSS * x


def score(s, policy, sal):
    if s["kind"] == "relief":
        return 0.8 * s["D"]                      # every policy feels a deficit
    if policy == "greedy":
        return liking(s) * s["h"] * nov(s)
    if policy == "wanting":
        return sal[s["kind"]] * s["mot"] * liking(s)
    return s["log"] * (1 - np.exp(-(s["gap"] + 1) / 3))   # "log": remembered liking * freshness


def use(S, s, mode, motf, rng):
    """One session with source s. Returns raw yield y and updates the clocks."""
    s["uses"] += 1
    s["gap"] = 0
    if s["kind"] == "relief":
        y, s["D"] = 0.8 * s["D"], 0.0
        return y
    focus, force, inter = mode
    sat_m, y_m = FOCUS[focus]
    sat_m *= FORCE[force]
    y = liking(s) * s["h"] * nov(s) * y_m * (1.1 if inter else 1.0) * rng.uniform(0.75, 1.25)
    s["log"] = 0.7 * s["log"] + 0.3 * liking(s) * nov(s)          # the liking log's rating
    drop = min(0.95, ALPHA[s["kind"]] * sat_m * (0.6 if inter else 1.0))
    if s["h"] < 0.2:
        s["ov"] = 6                                                 # used past the plateau
    s["h"] -= drop * s["h"]
    s["mot"] -= min(0.95, motf * drop) * s["mot"]
    if s["prof"] is not None:
        for o in S:
            if o is not s and o["prof"] == s["prof"]:
                o["h"] -= SPILL * drop * o["h"]
                o["mot"] -= SPILL * min(0.95, motf * drop) * o["mot"]
    s["m"] -= 0.03 * s["m"]
    if s["kind"] == "skill" and s["struct"] > 0:
        step = min(0.02, s["struct"]); s["l"] += step; s["struct"] -= step
    if s["kind"] == "sensitizing":
        s["sens"] += 0.04 * (2.5 - s["sens"])
    return y


def run(seed=0, portfolio=None, add=None, add_at=100, phi=None, policy="greedy", sched=None,
        modes=None, sal=None, motf=2.0, ban=None):
    """sched(t, S) -> list of sources forced into slots this period (the rest by policy);
    ban(s) -> True excludes s from the policy's fill (scheduled-only sources).
    modes: {id(source): mode}. Returns per-period value array and the source list."""
    rng = np.random.default_rng(seed)
    S = portfolio() if portfolio else base_portfolio()
    phi = {**PHI0, **(phi or {})}
    sal = sal or SAL_BIASED
    modes = modes or {}
    R = {k: 0.0 for k in KINDS}
    V = np.zeros(T)
    for t in range(T):
        if add and t == add_at:
            S.append(new_source(add))
        active = [s for s in S if s["kind"] != "material"]
        chosen = list(sched(t, S)) if sched else []
        rest = sorted([s for s in active if all(s is not c for c in chosen)
                       and not (ban and ban(s))],
                      key=lambda s: -score(s, policy, sal))
        chosen = (chosen + rest)[:SLOTS]
        ys = {k: [] for k in KINDS}
        for s in chosen:
            ys[s["kind"]].append(use(S, s, modes.get(id(s), DEFAULT_MODE), motf, rng))
        mat = sum(liking(s) * nov(s) * rng.uniform(0.9, 1.1) for s in S if s["kind"] == "material")
        for s in S:
            if s["kind"] == "material":
                s["m"] -= 0.03 * s["m"]
        ys["material"] = [mat] if mat > 0 else []
        v = sum(ys["relief"])
        for k in KINDS:
            if k == "relief":
                continue
            v += sum(gain(y - R[k]) for y in ys[k])
            if ys[k]:
                R[k] += K_REF * (phi[k] * np.mean(ys[k]) - R[k])
            else:
                R[k] -= 0.5 * K_REF * R[k]          # deprivation lowers the reference
        V[t] = v
        for s in S:                                 # slow and recovery clocks
            used = any(s is c for c in chosen)
            s["ema"] = 0.9 * s["ema"] + 0.1 * used
            r = REC * (0.5 + 1.5 * s["ema"]) * (0.4 if s["ov"] > 0 else 1.0)
            s["h"] += r * (1 - s["h"])
            s["mot"] += 0.6 * r * (1 - s["mot"])
            s["ov"] = max(0, s["ov"] - 1)
            s["m"] += 0.004 * (1 - s["m"])
            if not used:
                s["gap"] += 1
                if s["kind"] == "sensitizing":
                    s["sens"] -= 0.01 * (s["sens"] - 1.0)
            if s["kind"] == "relief":
                s["D"] = min(3.0, s["D"] + s["rate"])
    return V, S


def mean_over(f, seeds=SEEDS):
    return np.mean([f(s) for s in range(seeds)], axis=0)


def e1_gains(phi=None, kinds=KINDS):
    """Gain in mean value over periods 100-200 and 300-400 from adding one source at t=100."""
    out = {}
    base = [run(seed, phi=phi)[0] for seed in range(SEEDS)]
    for k in kinds:
        d = np.array([run(seed, add=k, phi=phi)[0] - base[seed] for seed in range(SEEDS)])
        out[k] = (d[:, 100:200].mean(), d[:, 300:400].mean())
    return out


def e1():
    print("E1. Which expansions survive adaptation? Add one source of a kind at t=100.")
    print("    gain in mean experienced value per period vs no addition (20 paired seeds)")
    print(f"    {'kind':<12}{'t 100-200':>10}{'t 300-400':>10}{'kept':>7}")
    for k, (a, b) in e1_gains().items():
        print(f"    {k:<12}{a:10.3f}{b:10.3f}{b / a if a else 0:7.0%}")


def x_portfolio(kind="sensory"):
    def p():
        S = base_portfolio()
        S.append(src("sensory", 1.0, prof=5, x=True) if kind == "sensory"
                 else src("sensitizing", 0.6, x=True))
        return S
    return p


def e2():
    print("\nE2. Exposure mode: music-like sensory item X scheduled into a slot every period")
    print("    mean value t100-400 / X mean yield per use (last 50) / X freshness h (last 50)")
    for focus in ["focused", "background"]:
        for force in ["chosen", "forced"]:
            for inter in [False, True]:
                def f(seed):
                    hs, ys = [], []
                    def sched(t, S):
                        x = S[-1]
                        if t >= T - 50:
                            hs.append(x["h"]); ys.append(liking(x) * x["h"] * nov(x) * FOCUS[focus][1]
                                                         * (1.1 if inter else 1.0))
                        return [x]
                    S = x_portfolio()()
                    V, _ = run(seed, portfolio=lambda: S, sched=sched,
                               modes={id(S[-1]): (focus, force, inter)})
                    return V[100:].mean(), np.mean(ys), np.mean(hs)
                v, y, h = mean_over(f)
                tag = f"{focus}/{force}/{'interrupted' if inter else 'continuous'}"
                print(f"    {tag:<36}{v:7.3f}{y:8.3f}{h:7.2f}")


def e3():
    print("\nE3. Four sensory items (liking 1.0), nothing else; mean value t100-400 / mean h")
    for name, profs in [("one shared profile", [0, 0, 0, 0]), ("four profiles", [0, 1, 2, 3])]:
        for pol in ["greedy", "log"]:
            def f(seed):
                V, S = run(seed, portfolio=lambda: [src("sensory", 1.0, prof=p) for p in profs],
                           policy=pol)
                return V[100:].mean(), np.mean([s["h"] for s in S])
            v, h = mean_over(f)
            print(f"    {name:<20} policy={pol:<7}{v:7.3f}{h:7.2f}")


def e4():
    print("\nE4. Schedules for one favourite X (other slot(s) greedy; X never picked off-schedule)")
    print("    mean value t100-400 and X uses")
    scheds = {
        "fixed: every period": lambda t: True,
        "fixed: every other period": lambda t: t % 2 == 0,
        "oscillate 3 on / 3 off": lambda t: (t // 3) % 2 == 0,
        "oscillate 8 on / 8 off": lambda t: (t // 8) % 2 == 0,
        "oscillate 20 on / 20 off": lambda t: (t // 20) % 2 == 0,
        "adaptive (greedy picks X)": None,
    }
    print(f"    {'schedule':<30}{'X=sensory':>10}{'uses':>6}{'X=sensitizing':>15}{'uses':>6}")
    for name, on in scheds.items():
        row = []
        for kind in ["sensory", "sensitizing"]:
            def f(seed):
                sched = (lambda t, S: [S[-1]] if on(t) else []) if on else None
                ban = (lambda s: s.get("x", False)) if on else None
                V, S = run(seed, portfolio=x_portfolio(kind), sched=sched, ban=ban)
                return V[100:].mean(), S[-1]["uses"]
            v, u = mean_over(f)
            row += [v, u]
        print(f"    {name:<30}{row[0]:10.3f}{row[1]:6.0f}{row[2]:15.3f}{row[3]:6.0f}")


def e5():
    print("\nE5. Wanting-driven vs liking-driven choice; base + skill (starts 0.5) + sensitizing")
    print("    value t100-400, then uses of skill/sensitizing (of 800 slots).")
    print("    greedy = true current liking*freshness (myopic); log = liking log + gap-based freshness")
    def p():
        S = base_portfolio()
        S += [src("skill", 0.5, struct=1.5), src("sensitizing", 0.6)]
        return S
    print(f"    {'condition':<34}{'greedy':>16}{'wanting':>16}{'log':>16}")
    for name, sal, motf in [("salience biased, wanting 2x fast", SAL_BIASED, 2.0),
                            ("salience flat,   wanting 2x fast", SAL_FLAT, 2.0),
                            ("salience flat,   wanting 1x (ctl)", SAL_FLAT, 1.0),
                            ("salience biased, wanting 1x", SAL_BIASED, 1.0)]:
        cells = []
        for pol in ["greedy", "wanting", "log"]:
            def f(seed):
                V, S = run(seed, portfolio=p, policy=pol, sal=sal, motf=motf)
                return V[100:].mean(), S[-2]["uses"], S[-1]["uses"]
            v, a, b = mean_over(f)
            cells.append(f"{v:6.3f} {a:3.0f}/{b:3.0f}")
        print(f"    {name:<34}" + "".join(f"{c:>16}" for c in cells))


def e6():
    print("\nE6. Sensitivity: E1 late gain (t 300-400) as phi varies")
    kinds = ["material", "sensory", "social", "skill"]
    print(f"    {'phi_material':<16}" + "".join(f"{k:>10}" for k in kinds))
    for pm in [0.3, 0.6, 0.8, 0.95, 1.0]:
        g = e1_gains(phi=dict(material=pm), kinds=kinds)
        print(f"    {pm:<16}" + "".join(f"{g[k][1]:10.3f}" for k in kinds))
    print(f"    {'phi_social=skill':<16}" + "".join(f"{k:>10}" for k in kinds))
    for ps in [0.3, 0.5, 0.7, 1.0]:
        g = e1_gains(phi=dict(social=ps, skill=ps), kinds=kinds)
        print(f"    {ps:<16}" + "".join(f"{g[k][1]:10.3f}" for k in kinds))
    print(f"    {'phi_sensory':<16}" + "".join(f"{k:>10}" for k in kinds))
    for ps in [0.3, 0.8, 1.0]:
        g = e1_gains(phi=dict(sensory=ps), kinds=kinds)
        print(f"    {ps:<16}" + "".join(f"{g[k][1]:10.3f}" for k in kinds))


# ---- Calibrated run (Nov 25), using prior-art/adaptation_by_domain.md ----
# material/circumstance ~0.9 (full, months); sensory 0.5 (unknown, kept); social as a
# circumstance (marriage-like, full in ~2 years) 0.9 vs social as a varied activity 0.2;
# skill / intentional activity 0.15; sensitizing 0.2 (weak evidence); relief exempt.
CALIBRATED = {
    "social as circumstance": dict(material=0.9, sensory=0.5, social=0.9, skill=0.15, sensitizing=0.2),
    "social as varied activity": dict(material=0.9, sensory=0.5, social=0.2, skill=0.15, sensitizing=0.2),
}

def calibrated():
    print("\nE7. Calibrated adaptation: E1 gain from adding one source (early t100-200 / late t300-400)")
    for label, ph in CALIBRATED.items():
        g = e1_gains(phi=ph)
        cells = "  ".join(f"{k} {a:+.3f}/{b:+.3f}" for k, (a, b) in g.items()) if isinstance(g, dict) else str(g)
        print(f"  {label}: {cells}")


if __name__ == "__main__":
    print(__doc__.split("\n")[0])
    print(f"T={T}, slots={SLOTS}, seeds={SEEDS}, LOSS={LOSS}, K_REF={K_REF}, phi={PHI0}\n")
    e1(); e2(); e3(); e4(); e5(); e6()
    calibrated()
