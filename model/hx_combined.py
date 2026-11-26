"""Combined model: do the headline results survive when the mechanisms interact?

One agent, one shared parameter set P, T periods of SLOTS uses each. Sources by kind:
  sensory (profile, satiety spills within a profile), skill (liking grows while structure
  remains), sensitizing (liking multiplier rises with regular use), material (passive),
  relief (deficit D; also clean relief of distress S), social (a person: closeness, battery,
  shared relief, loss with convex grief), feed (passive, salient, no competence),
  numb (fast relief, capacity cost, opponent-process rebound), acquired (Berlyne two-factor,
  calibrated to Szpunar 2004), practice (meditation: trains equanimity e / concept release cr).
Opt-in, off by default: felt craving (tension, ref_infl; hx_craving.py); flattened or more vivid
  liking and careless choice (flat, vivid, flat_choice; hx_equanimity.py).
Felt yield of a use = g(S) * capacity * dull * attention(arousal, S, e) * base + competence.
  dull = 1 - K0*x*(1-cr) (categorizing load from expertise x) dulls positives AND felt suffering.
  attention = engagement(a) * (1+0.3a) / (1 + CAPT*S*(1-e)*(1+a))   (capture, inverted U)
Value per period = sum gain(y - R_kind) (shortfalls x LOSS; relief/numb exempt) + relief
  + calm carryover + anticipation (planned uses) + fit - LAM * S*(1-e)*dull*(1+0.3a).
Choice per free slot: with prob pi the urge picks (salience * motivation * (cached v + sensitization)),
  otherwise liking picks (true expected felt yield). Schedules (plans) take slots first.
Calibrated: LAM=LOSS=2 (Brown et al. 2024 loss aversion 1.8-2.1); phi by kind
(adaptation_by_domain.md); acquired-taste A1=3.0, s1=1.46, a0=0.157 (hx_acquired_taste fit);
2-5 close ties (Dunbar). Everything else: the most common value across the scripts, or invented.
"""
import numpy as np

P = dict(T=300, SLOTS=3, LAM=2.0, LOSS=2.0, K_REF=0.03, REC=0.25, SPILL=0.5, MOTF=2.0, GS=0.3,
         PHI=dict(material=0.9, sensory=0.5, social=0.2, skill=0.15, sensitizing=0.2, feed=0.5,
                  acquired=0.5, practice=0.15),
         ALPHA=dict(sensory=0.30, social=0.20, skill=0.20, sensitizing=0.15, feed=0.05, practice=0.10),
         FADE=0.05, INFLOW=0.02, SHOCK_P=0.03, SHOCK=(0.5, 2.0),
         RHO_C=0.15, RHO_P=0.10, RHO_N=0.30, MU=0.05, PSI=0.05, REB=0.15, BUILD=0.3,
         CAPT=0.15, K0=0.6, X0=0.5, COMP=0.15, ANT=0.1, ETA=0.5, WDECAY=0.1,
         SAL=dict(material=1.0, sensory=1.0, social=0.7, skill=0.6, sensitizing=0.7, relief=1.0,
                  feed=1.6, numb=1.3, acquired=0.5, practice=0.5),
         SENS=dict(feed=0.2, numb=0.3, relief=0.0), SENS0=0.1,
         AMP=1.3, BUNDLE=0.4, AUT=0.3, GROW=0.08, CDECAY=0.01, RHO_SH=0.15, RHO_AL=0.03,
         CONFLICT=0.03, IMPORT=0.027, Q=0.004, GRIEF=10.0, DRAIN=0.25, RECH=0.25, B_LOW=0.3, OVER=0.6,
         GAMMA=1.0,         ACQ_A=2.0, ACQ_SIG=4.38, ACQ_a=0.052, ACQ_L0=-0.5, ACQ_N=60, C0=0.8, LP=10.0)
ACTIVE = {"skill", "social", "sensitizing", "practice"}
EXEMPT = {"relief", "numb"}
g = lambda S: np.exp(-P["GS"] * S)        # distress numbs liking; p(S) = g(S) blocks learning


def src(kind, l=1.0, prof=None, **kw):
    return dict(dict(kind=kind, l=l, prof=prof, h=1.0, m=0.3, mot=1.0, ema=0.0, ov=0, v=l, w=0.0, sens=1.0,
                     struct=0.0, D=0.0, cl=0.3, share=0.0, F=0.0, ha=1.0, ma=1.0, n=0, quit=False, uses=0), **kw)


def world(cfg):
    profs = cfg.get("profs", [0, 0, 1, 2])
    W = [src("sensory", 1.0 - 0.05 * i, prof=p) for i, p in enumerate(profs)]
    W += [src("material", 0.5), src("relief", 0.0, rate=0.3)]
    W += [src("skill", 0.5, struct=1.5), src("sensitizing", 0.5)] if cfg.get("skill", True) else []
    W += [src("social", 0.9) for _ in range(cfg.get("people", 1))]
    W += [src("feed", 0.5, m=1.0)] if cfg.get("feed") else []
    W += [src("numb", 0.3)] if cfg.get("numb") else []
    W += [src("acquired", P["ACQ_L0"])] if cfg.get("acq") else []
    return W + ([src("practice", 0.2)] if cfg.get("practice") else [])


def base_yield(s, st):
    k = s["kind"]
    if k == "social":
        b = P["GAMMA"] * st["gamma"] * P["AMP"] * s["l"] * s["h"] * (0.7 + 0.3 * s["cl"])
        b += P["BUNDLE"] * s["cl"] - P["AUT"] * (1 - s["cl"])
        return b * (1 - P["OVER"] * st["over"])
    if k == "acquired":
        return s["l"] + P["ACQ_A"] * (1 - np.exp(-s["F"] / P["ACQ_SIG"])) * s["ha"] * s["ma"]
    if k == "practice":
        return s["l"]
    nov = 1.0 if k == "feed" else 0.7 + 0.6 * s["m"]
    return s["l"] * s["sens"] * s["h"] * nov


def attention(st):
    a, e = st["a"], st["e"]
    eng = 1 - 0.8 * (2 * a - 1) ** 2
    return eng * (1 + 0.3 * a) / (1 + P["CAPT"] * st["S"] * (1 - e) * (1 + a))


def felt(s, st, bg):
    """Felt yield (no noise) of using s now; bg = background mode."""
    k = s["kind"]
    if k == "relief":
        return 0.8 * s["D"]
    if k == "numb":
        return s["l"] * g(st["S"]) * st["c"]
    y = g(st["S"]) * st["c"] * st["dull"] * attention(st) * base_yield(s, st)
    y *= 0.5 if bg else 1.0
    if k in ACTIVE and not bg:
        y += P["COMP"] * g(st["S"]) * st["c"]          # competence: producing effects
    if st.get("vivid") and y > 0:                    # opt-in (hx_equanimity.py): liking itself more vivid
        y *= 1 + st["vivid"]
    if st.get("flat"):                               # opt-in (hx_equanimity.py): liking pulled toward the
        y = (1 - st["flat"]) * y + st["flat"] * st["ybar"]   # running average of unflattened liking
    return y


def liking_score(s, st, cfg):
    k = s["kind"]
    if k == "relief":
        return 0.8 * s["D"] + P["LAM"] * P["RHO_C"] * st["S"]
    if k == "numb":
        return felt(s, st, False) + P["LAM"] * P["RHO_N"] * st["S"]
    y = felt(s, st, k == "feed" or cfg.get("bg", 0) > 0.5)
    learn = g(st["S"]) * st["c"]                     # curiosity: expected liking gain (LP horizon)
    if k == "skill" and s["struct"] > 0:
        y += P["LP"] * 0.02 * learn
    if k == "sensitizing":
        y += P["LP"] * 0.04 * learn * (2.5 - s["sens"]) * s["l"] * 0.1
    if k == "social":                                # feel the battery about to run low
        B = st["B"] - P["DRAIN"] / P["SLOTS"] / max(st["gamma"], 0.2)
        y -= P["LAM"] * 0.3 * max(0.0, P["B_LOW"] - B) / P["B_LOW"]
    return y


def want_score(s, st, cfg):
    sal = P["SAL"][s["kind"]] if cfg.get("sal", "biased") == "biased" else 1.0
    extra = 0.8 * s["D"] if s["kind"] == "relief" else 0.0
    extra += 0.3 * st["S"] if s["kind"] == "numb" else 0.0      # negative reinforcement
    return sal * s["mot"] * (s["v"] + s["w"]) + extra


def plan(t, W, st, cfg):
    """Scheduled uses for period t (relief policy, habits, social plan, expansion plans)."""
    S, out = st["S"], []
    rel = next(s for s in W if s["kind"] == "relief")
    mode, thr = cfg.get("relief", "policy"), cfg.get("thr", 2.0)
    k_rel = {"gate": P["SLOTS"] * (S > thr), "fixed": 1,
             "gradient": int(P["SLOTS"] * S**2 / (S**2 + thr**2) + 0.5)}.get(mode, 0)
    out += [rel] * int(k_rel)
    if cfg.get("numb_habit") is not None:
        nb = next(s for s in W if s["kind"] == "numb")
        if S > cfg["numb_habit"] or nb["w"] > 1.0 or t < cfg.get("numb_first", 0):
            out.append(nb)
    if cfg.get("soc_slots", 0) and (not cfg.get("rhythm", True) or st["B"] >= 0.4):
        ppl = sorted([s for s in W if s["kind"] == "social"], key=lambda s: -s["h"] * (0.5 + s["cl"]))
        out += ppl[:cfg["soc_slots"]]
    if S <= cfg.get("expand_gate", np.inf):
        for kind, every in cfg.get("sched", {}).items():
            for s in W:
                if s["kind"] != kind or t % every or (kind == "practice" and t >= 200):
                    continue
                if kind == "acquired":
                    if s["quit"] or s["n"] >= P["ACQ_N"]:
                        continue
                    out += [s] * cfg.get("burst", 1)
                else:
                    out.append(s)
    return out


def run(cfg, seed=0):
    rng, env, lossr = (np.random.default_rng(seed + i * 10**6) for i in range(3))  # choice, shocks, losses
    W, T, SL = world(cfg), P["T"], P["SLOTS"]
    st = dict(S=cfg.get("S0", 1.0), c=1.0, e=cfg.get("e", 0.0), cr=cfg.get("cr", 0.0),
              x=cfg.get("x", P["X0"]), a=cfg.get("a", 0.5), B=1.0, over=0.0,
              gamma=cfg.get("gamma", 1.0), flat=cfg.get("flat", 0.0), vivid=cfg.get("vivid", 0.0),
              ybar=cfg.get("ybar0", 0.5))
    R = {k: 0.0 for k in P["PHI"]}
    carry, pend, build, pi = 0.0, 0.0, 0.0, cfg.get("pi", 0.0)
    rho_al, motf = cfg.get("rho_al", P["RHO_AL"]), cfg.get("motf", P["MOTF"])
    V, log = np.zeros(T), dict(uses={}, feed_y=[], other_y=[], pl=np.zeros(T), su=np.zeros(T), tens=np.zeros(T))
    tau, rc = cfg.get("tension", 0.0), cfg.get("ref_infl", 0.0)   # opt-in craving costs (hx_craving.py)
    for t in range(T):
        if cfg.get("remove_at") == t:                    # lose the most-used sensory source
            W.remove(max((s for s in W if s["kind"] == "sensory"), key=lambda s: s["uses"]))
        if cfg.get("add") and t == 100:                  # one new source (claim 9)
            k = cfg["add"]; l = dict(material=0.8, skill=0.5, sensitizing=0.5, relief=0.0).get(k, 1.0)
            W.append(src(k, l, m=1.0, prof=7 if k == "sensory" else None, struct=1.5 * (k == "skill"), rate=0.3))
        st["S"] += pend + cfg.get("inflow", P["INFLOW"]); pend = 0.0
        shock, size = env.random() < P["SHOCK_P"], env.uniform(*P["SHOCK"])
        st["S"] += size * (shock and cfg.get("shocks", True))
        st["dull"] = 1 - P["K0"] * st["x"] * (1 - st["cr"])
        st["over"] = max(0.0, P["B_LOW"] - st["B"]) / P["B_LOW"]
        planned = plan(t, W, st, cfg)[:SL]
        chosen = list(planned)
        ban = set(cfg.get("ban", ())) | {"material", "practice"}
        while len(chosen) < SL:
            pool = [s for s in W if s["kind"] not in ban and all(s is not c for c in chosen)
                    and not (s["kind"] == "acquired" and (s["quit"] or s["n"] < P["ACQ_N"]))]
            if not pool:
                break
            f = want_score if rng.random() < pi else liking_score
            if st["flat"] and cfg.get("flat_choice") and rng.random() < st["flat"] * cfg["flat_choice"]:
                chosen.append(pool[rng.integers(len(pool))])   # opt-in: indifference picks at random
                continue
            chosen.append(max(pool, key=lambda s: f(s, st, cfg)))
        unmet = 0.0
        if tau:
            rest = [s for s in W if s["kind"] not in ban and all(s is not c for c in chosen)]
            unmet = max([max(0.0, want_score(s, st, cfg) - max(liking_score(s, st, cfg), 0.0)) for s in rest] or [0.0])
        v, pos, nsoc = 0.0, 0.0, 0
        for i, s in enumerate(chosen):
            k = s["kind"]; s["uses"] += 1
            log["uses"][k] = log["uses"].get(k, 0) + 1
            bg = k == "feed" or (k in ("sensory", "acquired") and rng.random() < cfg.get("bg", 0))
            nz = 1 if k in EXEMPT else rng.uniform(0.8, 1.2)
            y = felt(s, st, bg) * nz
            (log["feed_y"] if k == "feed" else log["other_y"]).append(y)
            if st["flat"] and k not in EXEMPT:           # average of what would be felt unflattened
                st["ybar"] += 0.05 * (felt(s, dict(st, flat=0.0), bg) * nz - st["ybar"])
            if i < len(planned):
                v += P["ANT"] * max(s["v"], 0)           # anticipation of planned pleasures
            if k == "relief":
                v += y; s["D"] = 0.0; st["S"] -= P["RHO_C"] * st["S"]
            elif k == "numb":
                v += y; st["S"] -= P["RHO_N"] * st["S"]; st["c"] *= 1 - P["MU"]
                pend += P["REB"] * (1 + build); build += P["BUILD"]
            else:
                v += y - R[k] if y >= R[k] else P["LOSS"] * (y - R[k])
                R[k] += P["K_REF"] * (P["PHI"][k] * y + rc * s["w"] - R[k])
                pos += max(y, 0)
                if y > 0 and not bg:                     # savoring relieves (undoing effect)
                    st["S"] -= min(0.5, P["RHO_P"] * y) * st["S"]
            s["v"] += P["ETA"] * (y - s["v"]); s["w"] += P["SENS"].get(k, P["SENS0"]) * cfg.get("sens_on", 1)
            learn = g(st["S"]) * st["c"]
            drop = min(0.95, P["ALPHA"].get(k, 0.0) * (0.6 if bg else 1.0))
            s["ov"] = 6 if s["h"] < 0.2 else s["ov"]
            s["h"] -= drop * s["h"]; s["mot"] -= min(0.95, motf * drop) * s["mot"]
            if s["prof"] is not None:
                for o in W:
                    if o is not s and o["prof"] == s["prof"]:
                        o["h"] -= P["SPILL"] * drop * o["h"]
            s["m"] -= 0.03 * s["m"] * (k != "feed")
            if k == "skill" and s["struct"] > 0:
                d = min(0.02 * learn, s["struct"]); s["l"] += d; s["struct"] -= d
                st["x"] += 0.004 * (1 - st["x"])
            if k == "sensitizing":
                s["sens"] += 0.04 * learn * (2.5 - s["sens"])
            if k == "acquired":
                s["F"] += learn; s["n"] += 1
                s["ha"] *= 1 - P["ACQ_a"]; s["ma"] *= 1 - P["ACQ_a"] / 5
                if s["n"] <= P["ACQ_N"] and y <= 0 and rng.random() > P["C0"] * (1 - min(st["S"] / 5, 1)):
                    s["quit"] = True                     # filed as a 'bad', never resampled
            if k == "practice":                          # order: E, C, EC (e to 0.5 first), CE
                o = cfg["practice"]
                q = "e" if o == "E" or (o == "EC" and st["e"] < 0.5) or (o == "CE" and st["cr"] >= 0.5) else "cr"
                st[q] += 0.02 * learn * ((0.9 if q == "e" else 1.0) - st[q])
            if k == "social":
                nsoc += 1
                st["S"] -= P["RHO_SH"] * min(st["gamma"], 1) * s["cl"] * st["S"] * (1 - st["over"])
                st["S"] += P["CONFLICT"] + P["IMPORT"] + 0.3 * st["over"]
                s["cl"] += P["GROW"] * (1 - s["cl"])
        mat = sum(s["l"] * (0.7 + 0.6 * s["m"]) * rng.uniform(0.9, 1.1) for s in W if s["kind"] == "material")
        if mat:
            y = mat * g(st["S"]) * st["dull"]
            v += y - R["material"] if y >= R["material"] else P["LOSS"] * (y - R["material"])
            R["material"] += P["K_REF"] * (P["PHI"]["material"] * y - R["material"]); pos += y
        for k in R:
            if all(c["kind"] != k for c in chosen) and k != "material":
                R[k] -= 0.5 * P["K_REF"] * R[k]          # deprivation lowers the reference
        keep = 0.6 * (1 - st["a"]) + 0.2 * st["a"]
        Sfelt = st["S"] * (1 - st["e"]) * st["dull"] * (1 + 0.3 * st["a"])
        V[t] = v + carry + 0.2 * (1 - abs(st["a"] - 0.5)) - P["LAM"] * (Sfelt + tau * unmet)
        log["pl"][t] = v + carry; log["su"][t] = Sfelt + tau * unmet; log["tens"][t] = tau * unmet
        carry = keep * 0.5 * pos
        # relationship loss: convex grief in the share of (recent) time the person carried
        for s in W:
            if s["kind"] == "social":
                s["share"] = 0.9 * s["share"] + 0.1 * sum(1 for c in chosen if c is s) / max(len(chosen), 1)
                if lossr.random() < P["Q"]:
                    st["S"] += P["GRIEF"] * s["share"] ** 2
                    s.update(cl=0.1, h=1.0, share=0.0)
                s["cl"] *= 1 - P["CDECAY"]
        nal = len(chosen) - nsoc
        st["S"] -= rho_al * nal / SL * st["S"]
        st["B"] = min(1, max(0, st["B"] - P["DRAIN"] * nsoc / SL / max(st["gamma"], 0.2) + P["RECH"] * nal / SL))
        st["S"] = max(0.0, st["S"] * (1 - P["FADE"]))
        st["c"] += P["PSI"] * (1 - st["c"]); build *= 0.9
        for s in W:                                      # recovery clocks
            used = sum(1 for c in chosen if c is s)
            s["ema"] = 0.9 * s["ema"] + 0.1 * (used > 0)
            r = P["REC"] * (0.5 + 1.5 * s["ema"]) * (0.4 if s["ov"] > 0 else 1.0)
            s["h"] += r * (1 - s["h"]); s["mot"] += 0.6 * r * (1 - s["mot"])
            s["ov"] = max(0, s["ov"] - 1); s["m"] += 0.004 * (1 - s["m"])
            s["w"] *= 1 - P["WDECAY"]
            if s["kind"] == "acquired":
                idle = SL - used
                s["ha"] = 1 - (1 - s["ha"]) * np.exp(-0.3 * idle); s["ma"] = 1 - (1 - s["ma"]) * np.exp(-0.005 * idle)
            if s["kind"] == "relief":
                s["D"] = min(3.0, s["D"] + s["rate"])
            if s["kind"] == "sensitizing" and not used:
                s["sens"] -= 0.01 * (s["sens"] - 1.0)
    log["W"], log["st"] = W, st
    return V, log


def M(cfg, seeds=8, lo=0, hi=None, full=False):
    out = [run(cfg, s) for s in range(seeds)]
    m = np.mean([V[lo:hi].mean() for V, _ in out])
    return (m, out) if full else m


# --------------------------------------------------------------- the eleven claims
LIKE = dict(pi=0.0)


def c1():
    print("1. Breadth vs ceiling: n sensory sources (distinct profiles), liking-driven")
    print("   n   mean V   p95 V   loss over t150-170 from losing the favourite at t150 (paired)")
    for n in [2, 4, 8, 16]:
        cfg = dict(LIKE, profs=list(range(n)), skill=False)
        m, out = M(cfg, full=True)
        p95 = np.mean([np.percentile(V, 95) for V, _ in out])
        drop = np.mean([V[150:170].mean() - run(dict(cfg, remove_at=150), sd)[0][150:170].mean()
                        for sd, (V, _) in enumerate(out)])
        print(f"   {n:<3} {m:7.3f} {p95:7.3f}   {drop:+.3f}")


def c2():
    print("\n2. Equanimity vs concept release, liking-driven; ordinary vs chronic distress (inflow 0.3)")
    for lab, kw in [("ordinary", {}), ("chronic", dict(inflow=0.3))]:
        print(f"   [{lab}] static, full expertise x=1: " + "  ".join(
            f"e{e}/cr{cr} {M(dict(LIKE, e=e, cr=cr, x=1.0, **kw)):.3f}" for e, cr in [(0, 0), (0.8, 0), (0, 1), (0.8, 1)]))
        row = []
        for order in [None, "E", "C", "EC", "CE"]:
            cfg = dict(LIKE, practice=order, sched={"practice": 2} if order else {}, **kw)
            m, out = M(cfg, lo=200, full=True)
            e = np.mean([o[1]["st"]["e"] for o in out]); cr = np.mean([o[1]["st"]["cr"] for o in out])
            row.append(f"{order}: {m:.3f} (e{e:.2f} cr{cr:.2f})")
        print(f"   [{lab}] practice every 2nd period t<200, V t200-300: " + "  ".join(row))


EXP_SCHED = {"skill": 2, "sensitizing": 3, "acquired": 3}


def c3():
    print("\n3. Relief from S0=6 (mean V over t0-150; best threshold per policy)")
    base = dict(LIKE, S0=6.0, acq=True, sched=EXP_SCHED, ban=("relief",))
    rows = {"no relief": [dict(base)],
            "fixed 1 slot": [dict(base, relief="fixed")],
            "gate (all-or-none)": [dict(base, relief="gate", thr=t) for t in [0.5, 1, 2, 3]],
            "gradient (share rises w/ S)": [dict(base, relief="gradient", thr=t) for t in [0.5, 1, 2, 3]],
            "two-phase: relieve, then expand": [dict(base, relief="gate", thr=t, expand_gate=t) for t in [0.5, 1, 2, 3]],
            "three-phase: relieve, savor, expand": [dict(base, relief="gate", thr=t, expand_gate=t2)
                                                    for t in [1, 2, 3] for t2 in [0.25, 0.5] if t2 < t]}
    for name, cfgs in rows.items():
        best = max((M(c, hi=150), c.get("thr"), c.get("expand_gate")) for c in cfgs)
        print(f"   {name:<38} V={best[0]:7.3f}  thr={best[1]} expand<={best[2]}")


def c4():
    print("\n4. Habitual numbing when suffering fades (S0=6, no shocks, no clean relief); mean V t0-150")
    base = dict(LIKE, S0=6.0, numb=True, shocks=False, skill=False, ban=("relief", "numb"))
    for name, kw in [("nothing (ordinary pleasures only)", {}),
                     ("bridge: numb first 2 periods only", dict(numb_habit=99, numb_first=2)),
                     ("habit: numb if S>0.5 or urge>1", dict(numb_habit=0.5)),
                     ("habit: numb if S>2 or urge>1", dict(numb_habit=2.0))]:
        m, out = M(dict(base, **kw), hi=150, full=True)
        n = np.mean([o[1]["uses"].get("numb", 0) for o in out])
        print(f"   {name:<36} V={m:7.3f}  numb uses={n:5.1f}  final S={np.mean([o[1]['st']['S'] for o in out]):.2f}")


def c5():
    print("\n5. Urge surfing: probability pi that the urge steers (salience biased, feed present)")
    base = dict(feed=True)
    def uses(cfg):
        m, out = M(cfg, full=True)
        u = np.mean([o[1]["uses"].get("skill", 0) + o[1]["uses"].get("sensitizing", 0) for o in out])
        return m, u
    for pi in [1.0, 0.75, 0.5, 0.25, 0.0]:
        m, u = uses(dict(base, pi=pi))
        print(f"   pi={pi:<5} V={m:7.3f}  skill+sensitizing uses={u:5.1f}")
    print("   Underuse decomposition at pi=1 (uses of skill+sensitizing; V):")
    ref = uses(dict(base, pi=0.0))[1]; b = uses(dict(base, pi=1.0))
    for name, kw in [("flat salience", dict(sal="flat")), ("wanting habituates 1x", dict(motf=1.0)),
                     ("no sensitization", dict(sens_on=0)), ("flat salience + no sensitization", dict(sal="flat", sens_on=0)),
                     ("no feed in the world", dict(feed=False))]:
        m, u = uses(dict(base, pi=1.0, **kw))
        print(f"   {name:<34} uses={u:5.1f} (recovers {(u - b[1]) / (ref - b[1] + 1e-9):5.0%} of gap; "
              f"liking-driven {ref:.0f}, urge {b[1]:.0f}) V={m:.3f}")


def c6():
    print("\n6. Acquired taste (K=2, l0=-0.5, 60 planned exposures, then free choice); 20 seeds")
    for name, kw in [("massed: 3 per period", dict(sched={"acquired": 1}, burst=3)),
                     ("spaced: 1 every 3 periods", dict(sched={"acquired": 3})),
                     ("spaced, distressed (S0=5)", dict(sched={"acquired": 3}, S0=5.0)),
                     ("widely spaced: every 8", dict(sched={"acquired": 8}))]:
        out = [run(dict(LIKE, acq=True, skill=False, **kw), s) for s in range(20)]
        a = [next(x for x in o[1]["W"] if x["kind"] == "acquired") for o in out]
        acq = np.mean([not x["quit"] for x in a])
        fresh = np.mean([x["l"] + P["ACQ_A"] * (1 - np.exp(-x["F"] / P["ACQ_SIG"])) * x["ma"] for x in a])
        neg = np.mean([x["n"] for x in a if x["quit"]] or [np.nan])
        print(f"   {name:<28} P(kept trying)={acq:4.0%}  quit at exposure {neg:5.1f}  rested liking at end "
              f"{fresh:+.2f}  V={np.mean([o[0].mean() for o in out]):.3f}")


def c7():
    print("\n7. Broad social vs broad solo (8 solo sources; social plan k slots/period when battery>=0.4)")
    types = {"average": {}, "low sociability": dict(gamma=0.6),
             "solitude is my relief": dict(gamma=0.8, rho_al=0.10)}
    for tname, kw in types.items():
        solo = M(dict(LIKE, profs=list(range(8)), people=0, **kw))
        res = {n: max(M(dict(LIKE, profs=list(range(8)), people=n, soc_slots=k, ban=("social",), **kw))
                      for k in [1, 2]) for n in [1, 2, 3, 4, 6, 12]}
        bn = max(res, key=res.get)
        print(f"   {tname:<22} solo {solo:6.3f} | social by #people " +
              " ".join(f"{n}:{v:.3f}" for n, v in res.items()) + f" | best {bn}")


def c8(seeds=40, N=12, Tp=200):
    """Pair: simplified, standalone. Same satiety/recovery/reference/loss/competence params."""
    print("\n8. Pairs (simplified: 12 joint activities, taste overlap 0, mudita 0.5, learning 0.05)")
    res = {}
    for strat in ["solo", "compromise", "turns", "overlap"]:
        tot = []
        for sd in range(seeds):
            rng = np.random.default_rng(sd)
            L = np.clip(1 + 0.4 * rng.normal(size=(2, N)), 0, 2); H = np.ones((2, N))
            Rf, val = np.zeros(2), 0.0
            for t in range(Tp):
                fav = np.argmax(L * H, axis=1)
                if strat == "solo":
                    pick, joint = fav, False
                else:
                    i = {"turns": fav[t % 2], "compromise": np.argmax(np.min(L * H, axis=0)),
                         "overlap": np.argmax((L * H).sum(0))}[strat]
                    pick, joint = np.array([i, i]), True
                y = L[[0, 1], pick] * H[[0, 1], pick]
                if joint:
                    y = P["AMP"] * y + 0.5 * y[::-1] + P["BUNDLE"] + P["COMP"]
                for p_ in (0, 1):
                    d = y[p_] - Rf[p_]
                    val += d if d >= 0 else P["LOSS"] * d
                    Rf[p_] += P["K_REF"] * (P["PHI"]["social"] * y[p_] - Rf[p_])
                    used = np.zeros(N, bool); used[pick[p_]] = True
                    H[p_, used] -= P["ALPHA"]["sensory"] * H[p_, used]
                    H[p_, ~used] += P["REC"] * (1 - H[p_, ~used])
                if joint:
                    i = pick[0]; d = L[1, i] - L[0, i]
                    L[0 if d > 0 else 1, i] += 0.05 * abs(d)
            tot.append(val / Tp / 2)
        res[strat] = np.mean(tot)
    print("   " + "  ".join(f"{k} {v:.3f}" for k, v in res.items()))


def c9():
    print("\n9. Which expansions last: add one source at t=100 to a world without skill/sensitizing")
    base = [run(dict(LIKE, skill=False), s)[0] for s in range(8)]
    for k in ["material", "sensory", "social", "skill", "relief", "sensitizing"]:
        d = np.array([run(dict(LIKE, skill=False, add=k), s)[0] - base[s] for s in range(8)])
        a, b = d[:, 100:200].mean(), d[:, 200:300].mean()
        print(f"   {k:<12} early {a:+.3f}  late {b:+.3f}  kept {b / a if a > 0 else float('nan'):5.0%}")


def c10():
    print("\n10. Arousal x equanimity (liking-driven, standard world)")
    for a in [0.2, 0.5, 0.8]:
        r = [M(dict(LIKE, a=a, e=e)) for e in [0.0, 0.8]]
        print(f"   a={a}: e=0 {r[0]:.3f}  e=0.8 {r[1]:.3f}  equanimity gain {r[1] - r[0]:+.3f}")


def c11():
    print("\n11. Feeds (urge steers 80%): share of slots, felt yield per use, cached wanting vs liking")
    for pi in [0.8, 0.0]:
        m, out = M(dict(pi=pi, feed=True), full=True)
        m0 = M(dict(pi=pi, feed=False))
        n = sum(sum(o[1]["uses"].values()) for o in out)
        f = sum(o[1]["uses"].get("feed", 0) for o in out)
        fy = np.mean([y for o in out for y in o[1]["feed_y"]] or [0])
        oy = np.mean([y for o in out for y in o[1]["other_y"]])
        fd = [x for o in out for x in o[1]["W"] if x["kind"] == "feed"]
        wl = np.mean([P["SAL"]["feed"] * x["mot"] * (x["v"] + x["w"]) for x in fd])
        print(f"   pi={pi}: feed share {f / n:4.0%}, feed yield {fy:.3f} vs other uses {oy:.3f}, "
              f"feed wanting {wl:.2f}, competence from feed 0; V with feed {m:.3f} vs without {m0:.3f}")


# ------------------------------------------------- default vs expansionist life
DEFAULT = dict(pi=0.5, bg=0.5, a=0.75, feed=True, numb=True, people=1, acq=True,
               sched={"acquired": 1}, burst=3)
EXPANSIONIST = dict(pi=0.1, bg=0.0, a=0.5, feed=True, numb=True, ban=("feed", "numb", "social"),
                    people=3, soc_slots=1, rhythm=True, acq=True, relief="gradient", thr=2.0,
                    practice="EC", sched={"skill": 3, "sensitizing": 4, "acquired": 3, "practice": 3})
ABLATE = {"choice (urge steers)": dict(pi=0.8),
          "attention mode (background)": dict(bg=0.5),
          "arousal (high)": dict(a=0.75),
          "practice (no equanimity/release)": dict(practice=None, sched={"skill": 3, "sensitizing": 4, "acquired": 3}),
          "relief policy (no gradient)": dict(relief="policy"),
          "numbing + feed allowed": dict(ban=("social",)),
          "social (1 person, unplanned)": dict(people=1, soc_slots=0, ban=("feed", "numb")),
          "acquired taste massed": dict(sched={"skill": 3, "sensitizing": 4, "acquired": 1, "practice": 3}, burst=3),
          "no skill/sensitizing plan": dict(sched={"acquired": 3, "practice": 3})}


def lives():
    print("\nLIVES (10 seeds, mean V per period over all 300 periods; and t200-300)")
    d, de = M(DEFAULT, 10), M(DEFAULT, 10, lo=200)
    x, xe = M(EXPANSIONIST, 10), M(EXPANSIONIST, 10, lo=200)
    print(f"   default      {d:.3f}  late {de:.3f}\n   expansionist {x:.3f}  late {xe:.3f}  gap {x - d:+.3f} (late {xe - de:+.3f})")
    dn = M(dict(DEFAULT, numb=False), 10)
    print(f"   default with no numbing source in its world {dn:.3f}  gap {x - dn:+.3f}")
    print("   Ablation: revert one component of the expansionist life to default (loss of V; share of gap)")
    for name, kw in ABLATE.items():
        a = M(dict(EXPANSIONIST, **kw), 10)
        print(f"   {name:<34} {a:.3f}  loss {x - a:+.3f}  ({(x - a) / (x - d):5.0%})")
    print("   Add one component to the default life (gain)")
    for name, kw in [("urge surfing pi=0.1", dict(pi=0.1)), ("focused mode", dict(bg=0.0)),
                     ("moderate arousal", dict(a=0.5)), ("ban numbing+feed", dict(ban=("feed", "numb"))),
                     ("3 people, planned", dict(people=3, soc_slots=1, ban=("social",)))]:
        print(f"   + {name:<32} gain {M(dict(DEFAULT, **kw), 10) - d:+.3f}")


def mechanisms():
    """Switch one mechanism off in BOTH lives; how much of the gap is left?"""
    print("   Mechanism ablation (switched off in both lives): default / expansionist / gap")
    zero_phi = {k: 0.0 for k in P["PHI"]}
    for name, kw in [("none (full model)", {}), ("reference points (phi=0)", dict(PHI=zero_phi)),
                     ("loss weight (LOSS=LAM=1)", dict(LOSS=1.0, LAM=1.0)), ("distress numbing (g=1)", dict(GS=0.0)),
                     ("attention capture", dict(CAPT=0.0)), ("categorizing dulling", dict(K0=0.0)),
                     ("numbing rebound", dict(REB=0.0, BUILD=0.0, MU=0.0)), ("competence", dict(COMP=0.0)),
                     ("anticipation", dict(ANT=0.0)), ("convex grief", dict(GRIEF=0.0)),
                     ("sensitization", dict(SENS=dict(feed=0.0, numb=0.0, relief=0.0), SENS0=0.0))]:
        old = {k: P[k] for k in kw}; P.update(kw)
        d, x = M(DEFAULT, 10), M(EXPANSIONIST, 10)
        P.update(old)
        print(f"   {name:<30} {d:7.3f} {x:7.3f}  gap {x - d:+.3f}")


if __name__ == "__main__":
    print(__doc__.split("\n")[0])
    print({k: v for k, v in P.items() if not isinstance(v, dict)}, "\n")
    for f in [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, lives, mechanisms]:
        f()
