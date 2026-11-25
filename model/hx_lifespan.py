"""Build vs spend over a finite, uncertain life, judged by several evaluation rules.

Each quarter (age 20-100) an agent splits effort: SPEND (enjoy current liking now) or
BUILD (expand capacity K: skills, acquired tastes, ways to relieve suffering). A policy is
a build share per life stage (young <40, mid 40-65, old 65+) plus a spend pattern
(smooth, or bursty: most spending in each year's last quarter). Pieces:
  spend yield   (L0 + K) * sat(effort), sat(e)=1-exp(-e) (satiation within a quarter)
                base part adapts near fully (phi 0.9, material-like); capacity part
                partly (phi 0.4, acquired tastes/experiences) -- adaptation_by_domain.md
  build         investment I = eta(age)*b*(1-K/KMAX) enters a pipeline and pays out with
                time constant TAU (fast 0.5y / default 2y / slow 6y). Learning slows with age.
                Realized progress is felt as learning-progress liking (phi 0.15, skill-like),
                but building costs effort (COST_B*b, practice is partly dull).
  suffering     unmet needs D0/(1+K), rising after 65 (ageing); weighted by LOSS.
  boredom       max(0, THETA - stimulation)*(1 - meaning); meaning from building and K.
  reference     per kind R' = R + KREF*(phi*y - R); value = gain(y - R), losses x LOSS.
  anticipation  ANT * expected positive yield over the next year * believed survival
                (Loewenstein 1987: small savoring term).
Evaluation rules = aggregation x discounting x 'dull-life block', applied to the SAME lives:
  sum   expected total of momentary value (mortality discounts via survival)
  prio  same over a concave transform g(u)=(1-exp(-1.5u))/1.5 (extra weight on worst moments)
  peL   remembered value of the whole life: E[(peak + end)/2] over the death time
  peY   peak-end of each year, summed over years lived (Kahneman et al. 1993)
  disc  0 or 2%/year pure time preference
  block none | bore (boredom counted, x LOSS) | thr (positive moments below 0.5 count x0.2)
All parameters are invented; read results as directions, not sizes.
"""
import itertools
import numpy as np

DT, AGE0, AGEMAX = 0.25, 20, 100
N = int((AGEMAX - AGE0) / DT)
AGE = AGE0 + DT * np.arange(N)
STAGE = np.digitize(AGE, [40, 65])                    # 0 young, 1 mid, 2 old
LOSS, L0, KMAX, ETA0, ETA_TAU, DECAY = 2.0, 1.0, 3.0, 0.5, 40.0, 0.01
COST_B, D0, THETA, ANT, KREF = 0.3, 0.4, 1.0, 0.1, 0.5
PHI = dict(base=0.9, cap=0.4, lp=0.15)
GRID = np.round(np.arange(0, 1.01, 0.1), 1)
POL = np.array(list(itertools.product(GRID, GRID, GRID)))        # (1331, 3)
BURST_W = {"smooth": np.ones(4), "bursty": np.array([0.4, 0.4, 0.4, 2.8])}
AGGS, DISCS, BLOCKS = ["sum", "prio", "peL", "peY"], [0.0, 0.02], ["none", "bore", "thr"]
RULES = list(itertools.product(AGGS, DISCS, BLOCKS))


def sat(e):
    return 1 - np.exp(-e)


def gain(x):
    return np.where(x > 0, x, LOSS * x)


def simulate(pol=POL, tau=2.0, burst="smooth", size=1.0):
    """Vectorized over policies. Returns core momentary value (no anticipation/boredom),
    positive stimulation, boredom, capacity K, all shaped (P, N)."""
    P = len(pol)
    b_t = pol[:, STAGE]
    K, pipe = np.zeros(P), np.zeros(P)
    R = dict(base=np.full(P, PHI["base"] * L0 * sat(0.7)), cap=np.zeros(P), lp=np.zeros(P))
    out = {k: np.zeros((P, N)) for k in ["core", "pos", "bore", "K"]}
    for t in range(N):
        b, age = b_t[:, t], AGE[t]
        e = (1 - b) * BURST_W[burst][t % 4]
        I = size * ETA0 * np.exp(-(age - AGE0) / ETA_TAU) * b * np.clip(1 - (K + pipe) / KMAX, 0, 1) * DT
        pipe += I
        r = pipe * (1 - np.exp(-DT / tau))
        pipe -= r
        K += r - DECAY * K * DT
        y = dict(base=L0 * sat(e), cap=K * sat(e), lp=r / DT)
        v = sum(gain(y[k] - R[k]) for k in y)
        for k in y:
            R[k] += KREF * DT * (PHI[k] * y[k] - R[k])
        D = D0 * (1 + max(0.0, age - 65) / 15) / (1 + K)
        pos = y["base"] + y["cap"] + y["lp"]
        meaning = np.clip(b + 0.5 * K / KMAX, 0, 1)
        out["core"][:, t] = v - COST_B * b - LOSS * D
        out["pos"][:, t] = pos
        out["bore"][:, t] = np.maximum(0, THETA - pos) * (1 - meaning)
        out["K"][:, t] = K
    return out


# ---- mortality: survival S has length N+1 (S[t] = alive at start of quarter t; S[N] = 0)
def surv_from_hazard(h_year):
    hq = 1 - (1 - np.clip(h_year, 0, 1)) ** DT
    return np.concatenate([[1.0], np.cumprod(1 - hq)[:-1], [0.0]])


def gompertz(m=1.0):
    return surv_from_hazard(m * 3e-5 * np.exp(0.095 * AGE))


def known(age_death):
    return np.concatenate([(AGE < age_death).astype(float), [0.0]])


SCEN = {
    "const 2%/y": surv_from_hazard(np.full(N, 0.02)),
    "gompertz": gompertz(),
    "uncertain": np.mean([gompertz(m) for m in (1 / 3, 1, 3)], axis=0),
}


def momentary(sim, S, block):
    """Momentary value series under a dull-life block, with anticipation from beliefs S."""
    pos = sim["pos"]
    cs = np.concatenate([np.zeros((len(pos), 1)), np.cumsum(pos, 1)], 1)
    idx = np.arange(N)
    hi = np.minimum(idx + 5, N)
    ahead = (cs[:, hi] - cs[:, idx + 1]) / np.maximum(hi - idx - 1, 1)
    believe = S[np.minimum(idx + 4, N)] / np.maximum(S[idx], 1e-12)
    u = sim["core"] + ANT * ahead * believe
    if block == "bore":
        u = u - LOSS * sim["bore"]
    elif block == "thr":
        u = np.where((u >= 0) & (u < 0.5), 0.2 * u, u)
    return u


def evaluate(u, S, agg, disc):
    """Expected value of momentary series u (P, n) under survival S (n+1,)."""
    n = u.shape[1]
    w = (1 - disc) ** (DT * np.arange(n))
    alive, die = S[:-1], S[:-1] - S[1:]
    if agg == "sum":
        return (u * alive * w).sum(1) * DT
    if agg == "prio":
        return ((1 - np.exp(-1.5 * u)) / 1.5 * alive * w).sum(1) * DT
    if agg == "peL":
        return ((np.maximum.accumulate(u, 1) + u) / 2 * die * w).sum(1)
    yrs = u[:, : n - n % 4].reshape(len(u), -1, 4)          # peY
    pe = (yrs.max(2) + yrs[:, :, -1]) / 2
    return (pe * S[3: n - n % 4: 4] * w[::4][: pe.shape[1]]).sum(1)   # alive in Q4


def best(sims, S, rule):
    """Best (policy row, burst, value) over all policies and spend patterns."""
    agg, disc, block = rule
    out = []
    for burst, sim in sims.items():
        v = evaluate(momentary(sim, S, block), S, agg, disc)
        i = int(np.argmax(v))
        out.append((v[i], i, burst))
    v, i, burst = max(out)
    return i, burst, v


def tag(rule):
    return f"{rule[0]:<4} d={rule[1]:.0%} {rule[2]:<4}"


def fmt(i):
    return "/".join(f"{x:.1f}" for x in POL[i])


def q1(sims):
    print("Q1. Optimal build share young/mid/old (and spend pattern) by rule and mortality scenario")
    print("    (tau=2y payoff). s=smooth, B=bursty spending. K65 = capacity at 65 under that policy")
    print(f"    {'rule':<20}" + "".join(f"{s:>24}" for s in SCEN))
    res = {}
    for rule in RULES:
        cells = []
        for name, S in SCEN.items():
            i, burst, _ = best(sims, S, rule)
            res[rule, name] = (i, burst)
            k65 = sims[burst]["K"][i, np.searchsorted(AGE, 65)]
            cells.append(f"{fmt(i)} {burst[0] if burst == 'smooth' else 'B'} K65={k65:.1f}")
        print(f"    {tag(rule):<20}" + "".join(f"{c:>24}" for c in cells))
    return res


def q2():
    print("\nQ2. Constructed lives (known length, no mortality). Short-intense: 30 years, quarters")
    print("    [0.9, 2.2, 1.2, -0.2] each year. Long-dull: 0.3/quarter, meaning 0.2.")
    print("    Long-calm: 0.6/quarter, meaning 0.6. Boredom = (1-stim)*(1-meaning).")
    print("    Cell: smallest length multiple (of 30y) at which the long life wins (search to 10x)")
    yr = np.array([0.9, 2.2, 1.2, -0.2])

    def life(kind, years):
        n = int(round(years / DT))
        if kind == "intense":
            u, bore = np.tile(yr, n // 4 + 1)[:n], np.zeros(n)
        else:
            lvl, mean = (0.3, 0.2) if kind == "dull" else (0.6, 0.6)
            u, bore = np.full(n, lvl), np.full(n, (1 - lvl) * (1 - mean))
        return u, bore

    def value(kind, years, agg, disc, block):
        u, bore = life(kind, years)
        if block == "bore":
            u = u - LOSS * bore
        elif block == "thr":
            u = np.where((u >= 0) & (u < 0.5), 0.2 * u, u)
        S = np.concatenate([np.ones(len(u)), [0.0]])
        return evaluate(u[None], S, agg, disc)[0]

    mults = np.round(np.arange(1, 10.01, 0.1), 1)
    print(f"    {'rule':<20}{'long-dull':>11}{'long-calm':>11}")
    out = {}
    for rule in RULES:
        si = value("intense", 30, *rule)
        cells = []
        for kind in ["dull", "calm"]:
            win = [m for m in mults if value(kind, 30 * m, *rule) > si]
            cells.append(f"{win[0]:.1f}x" if win else "never")
        out[rule] = cells
        print(f"    {tag(rule):<20}{cells[0]:>11}{cells[1]:>11}")

    print("\n    Additivity check: append one mild year (0.4/quarter) to the 30-year intense life,")
    print("    ending low (as above) or reordered to end each year on its peak. Change in value:")
    print(f"      {'agg':<6}{'ends low':>10}{'ends on peak':>14}")
    for agg in AGGS:
        cells = []
        for order in [yr, np.sort(yr)]:
            u0 = np.tile(order, 30)
            u1 = np.concatenate([u0, np.full(4, 0.4)])
            S0, S1 = np.r_[np.ones(len(u0)), 0], np.r_[np.ones(len(u1)), 0]
            cells.append(evaluate(u1[None], S1, agg, 0)[0] - evaluate(u0[None], S0, agg, 0)[0])
        print(f"      {agg:<6}{cells[0]:+10.3f}{cells[1]:+14.3f}")
    return out


def q3(sims):
    print("\nQ3a. Known lifespan vs uncertain hazard. Rule: sum, d=0, block=bore (and peY).")
    print("    Optimal build share young/mid/old; regret = value lost on the true type by using")
    print("    the policy chosen under type-uncertainty instead of the type's own optimum.")
    cases = {"known death 50": known(50), "known death 80": known(80), "known death 95": known(95),
             "gompertz x3 hazard": gompertz(3), "gompertz x1": gompertz(1),
             "gompertz x1/3": gompertz(1 / 3), "uncertain (mix)": SCEN["uncertain"]}
    for rule in [("sum", 0.0, "bore"), ("peY", 0.0, "bore")]:
        iu, bu, _ = best(sims, SCEN["uncertain"], rule)
        print(f"    rule {tag(rule)}   uncertain-optimal policy {fmt(iu)} {bu}")
        for name, S in cases.items():
            i, burst, v = best(sims, S, rule)
            vu = evaluate(momentary(sims[bu], S, rule[2]), S, rule[0], rule[1])[iu]
            print(f"      {name:<20}{fmt(i):>13} {burst:<7} regret of uncertain policy "
                  f"{(v - vu) / max(abs(v), 1e-9):6.1%}")

    print("\nQ3b. Fast vs slow payoff of building (same eventual capacity). Best value by rule")
    print("    (sum, d=0, bore); premium of fast over slow; size multiple the slow kind needs to tie.")
    rule = ("sum", 0.0, "bore")
    speeds = {}
    for tau in [0.5, 6.0]:
        for size in [1.0, 1.25, 1.5, 2.0]:
            if tau == 0.5 and size > 1:
                continue
            speeds[tau, size] = {b: simulate(tau=tau, burst=b, size=size) for b in BURST_W}
    print(f"    {'scenario':<20}{'fast':>8}{'slow':>8}{'premium':>9}{'young b fast/slow':>20}{'tie at':>8}")
    for name, S in {**SCEN, "known death 50": known(50), "known death 95": known(95)}.items():
        vf = best(speeds[0.5, 1.0], S, rule)
        vs = best(speeds[6.0, 1.0], S, rule)
        tie = next((f"{s}x" for s in [1.25, 1.5, 2.0] if best(speeds[6.0, s], S, rule)[2] >= vf[2]), ">2x")
        print(f"    {name:<20}{vf[2]:8.2f}{vs[2]:8.2f}{(vf[2] - vs[2]) / abs(vs[2]):9.1%}"
              f"{POL[vf[0]][0]:>13.1f}/{POL[vs[0]][0]:.1f}{tie:>8}")


def q4(res, q2res):
    print("\nQ4. Robustness across the 24 rules (Q1 optima, all three mortality scenarios)")
    rows = {}
    for (rule, scen), (i, burst) in res.items():
        r = rows.setdefault(rule, [])
        r.append((POL[i], burst))
    def count(pred):
        hits = [rule for rule, r in rows.items() if all(pred(p, b) for p, b in r)]
        return len(hits), hits
    checks = {
        "builds when young (b_young >= 0.3)": lambda p, b: p[0] >= 0.3,
        "builds less when old than young": lambda p, b: p[2] < p[0],
        "spends all when old (b_old = 0)": lambda p, b: p[2] == 0,
        "bursty spending chosen": lambda p, b: b == "bursty",
    }
    for name, pred in checks.items():
        n, hits = count(pred)
        aggs = sorted({h[0] for h in hits})
        print(f"    {name:<38}{n:3d}/24   (aggregations where it holds in all scenarios: {aggs})")
    d = [POL[res[(r[0], 0.02, r[2]), s][0]] - POL[res[r, s][0]] for r in RULES if r[1] == 0 for s in SCEN]
    d = np.array(d)
    print(f"    discounting 0 -> 2%: change in build share young/mid/old, mean {d.mean(0).round(2)}, "
          f"range young [{d[:, 0].min():+.1f}, {d[:, 0].max():+.1f}]; sign flips build->none: "
          f"{int(((d[:, 0] < 0) & (np.array([POL[res[(r[0], 0.02, r[2]), s][0]][0] for r in RULES if r[1] == 0 for s in SCEN]) == 0)).sum())}")
    agg_flip = {}
    for agg in AGGS:
        agg_flip[agg] = np.mean([POL[res[r, s][0]][0] for r in RULES if r[0] == agg for s in SCEN])
    print("    mean young build share by aggregation:",
          "  ".join(f"{a} {v:.2f}" for a, v in agg_flip.items()))
    dull_never = [tag(r) for r in RULES if q2res[r][0] == "never"]
    print(f"    Q2 long-dull never wins under {len(dull_never)}/24 rules")


if __name__ == "__main__":
    print(__doc__.split("\n")[0])
    print(f"LOSS={LOSS} KMAX={KMAX} ETA0={ETA0} COST_B={COST_B} D0={D0} THETA={THETA} ANT={ANT} "
          f"PHI={PHI} policies={len(POL)}x2 spend patterns\n")
    sims = {b: simulate(burst=b) for b in BURST_W}
    res = q1(sims)
    q2res = q2()
    q3(sims)
    q4(res, q2res)
