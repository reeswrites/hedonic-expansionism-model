"""Hedonic expansionism, social axis (v0 conventions from hx_model.py).

Experienced value of agent i:
  U_i = own_i - lam*S_i + kappa_i * sum_j P_j - lam*eta_i * sum_j S_j - appraisal_i
kappa: mudita weight on others' pleasure. eta: weight on others' felt suffering
(empathic distress). appraisal: jealousy strands that are appraisals only
(comparison, borrowed scarcity); they change no input. All parameters invented.
"""
import numpy as np

LAM = 2.0
alpha, rho = 0.6, 0.3

def steady_fresh(u):
    return rho * (1 - u) / (alpha * u + rho * (1 - u))

# ---------------------------------------------------------------- 1. compersion
def compersion_net(kappa, G, r, k=3, b=0.3, protect=False, dq=0.02, W=6.0,
                   s_b=0.5, appraisal=0.0):
    """Net change for you when partner takes outside pleasure G.
    Shared bundle: k strands, superadditive bonus b only if shared time >= threshold
    (the one Friday night). r = share of shared time diverted. protect=True: the
    threshold slot is kept, so only the linear part is lost.
    Risk: q rises by dq; loss of bundle costs bundle value + convex grief lam*W*s_b^2."""
    lose_bonus = (not protect) and r > 0
    R = r * k + (k * b if lose_bonus else r * k * b)
    L = k * (1 + b) + LAM * W * s_b ** 2
    return kappa * G - R - dq * L - appraisal, R, dq * L

def kappa_star(G, **kw):
    _, R, risk = compersion_net(0.0, G, **kw)
    return (R + risk + kw.get("appraisal", 0.0)) / G

def part1():
    print("1. Compersion threshold kappa* = (R + dq*L + appraisal)/G   (G=2, r=0.2)")
    print("   case                          R      dq*L   kappa*")
    cases = [("unprotected slot, dq=.02", dict(protect=False, dq=0.02)),
             ("protected slot,   dq=.02", dict(protect=True, dq=0.02)),
             ("protected slot,   dq=.005", dict(protect=True, dq=0.005)),
             ("protected, dq=.005, appr=.5", dict(protect=True, dq=0.005, appraisal=0.5)),
             ("unprotected, dq=.05", dict(protect=False, dq=0.05))]
    for name, kw in cases:
        _, R, risk = compersion_net(0, 2.0, r=0.2, **kw)
        print(f"   {name:29s} {R:5.2f}  {risk:5.3f}  {kappa_star(2.0, r=0.2, **kw):5.2f}")
    # bundle threshold shift: b > lam*q*(k-1)/k
    for q in [0.05, 0.07, 0.10]:
        print(f"   bundle-beats-spread needs b > {LAM*q*2/3:.3f} at q={q:.2f} (k=3)")

# ---------------------------------------------------------------- 2. breadth over subjects
def part2(rng):
    print("\n2a. Vicarious pleasure from m people, fixed attention A=1, vicarious habituates")
    for m in [1, 2, 3, 5, 10, 30, 100]:
        u = 1.0 / m
        print(f"   m={m:3d}  V={steady_fresh(u)*1.0:.3f}   E[grief share^2], q=.05: "
              f"{0.05*0.95/m + 0.05**2:.4f}")
    print("2b. Widening the circle: net per added person = a*(kappa*G - lam*eta*S)")
    # ladder rungs: (name, mean G, mean S) others' pleasure / suffering as witnessed
    ladder = [("self-adjacent", 1.0, 0.2), ("benefactor", 1.0, 0.25), ("friend", 1.0, 0.3),
              ("neutral", 0.8, 0.35), ("difficult", 0.7, 0.4), ("all", 0.6, 0.5)]
    for eta_ratio in [1.0, 0.3, 0.0]:
        kappa = 0.6; eta = eta_ratio * kappa; tot = 0; row = []
        for name, G, S in ladder:
            m = 5
            tot_m = m * (kappa * G - LAM * eta * S)
            tot += tot_m; row.append(f"{tot:+.2f}")
        print(f"   eta/kappa={eta_ratio:.1f} cumulative (5/rung, attention unbounded): " + " ".join(row))

# ---------------------------------------------------------------- 3. taste transmission
def transmit(theta, w=1.0, eta=0.08, T_rel=40, T=120, grief_cue=True, grief_len=15):
    """Chain A -> B -> C. A likes the feature (1.0). B learns from A at rate eta*w.
    Fraction theta of what B learns is internalized (own liking, kept);
    1-theta is dependent (B likes it as part of valuing A; held only while edge exists).
    C learns from B the same way. A-B ends at T_rel. Grief cue: after breakup the
    feature reminds B of A and is suppressed for grief_len periods (factor 0.3)."""
    li = {"B": 0.0, "C": 0.0}; ld = {"B": 0.0, "C": 0.0}
    hist = []
    for t in range(T):
        AB = t < T_rel
        LB = li["B"] + ld["B"]
        if AB:
            gap = max(0.0, 1.0 - LB)
            li["B"] += eta * w * theta * gap
            ld["B"] += eta * w * (1 - theta) * gap
        else:
            ld["B"] *= 0.7  # dependent liking unwinds once the valued person is gone
        LB = li["B"] + ld["B"]
        gapC = max(0.0, LB - li["C"] - ld["C"])
        li["C"] += eta * w * theta * gapC
        ld["C"] += eta * w * (1 - theta) * gapC
        ld["C"] = min(ld["C"], max(0.0, LB - li["C"]))  # C's dependent part tracks B
        supp = 0.3 if (grief_cue and T_rel <= t < T_rel + grief_len) else 1.0
        hist.append((li["B"] + ld["B"]) * supp)
    hist = np.array(hist)
    return hist[T_rel - 1], hist[T_rel + 2], hist[T_rel + 40], li["C"] + ld["C"]

def part3():
    print("\n3. Taste transmission A->B->C, A-B ends at t=40")
    print("   theta  B@39   B@42(test early)  B@80(test late)  ratio_late  C@end")
    for th in [0.0, 0.3, 0.7, 1.0]:
        pre, early, late, C = transmit(th)
        print(f"   {th:4.1f}  {pre:.3f}  {early:.3f}             {late:.3f}            "
              f"{late/pre:.2f}        {C:.3f}")

# ---------------------------------------------------------------- 4. multi-agent
def gini(x):
    x = np.sort(x - min(0, x.min())); n = len(x)
    return (2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum())

def simulate(kappas, seed=0, T=300, veto=True, protect=False, security=False,
             eta_ratio=1.0, theta=0.6, k=3, b=0.3, p_opp=0.15):
    rng = np.random.default_rng(seed)
    n = len(kappas); kappas = np.asarray(kappas, float)
    eta = eta_ratio * kappas                   # kappa<0 -> others' grief felt as pleasure
    appr_coef = np.clip(0.3 - 0.5 * kappas, 0, None)   # comparison/borrowed scarcity
    partner = np.array([i ^ 1 for i in range(n)])      # couples (0,1),(2,3)...
    friends = [[(i + 2) % n, (i - 2) % n] for i in range(n)]
    single_until = np.full(n, -1)
    grief_left = np.zeros(n); grief_amt = np.zeros(n)
    li = np.zeros(n); ld = np.zeros(n); li[0] = 1.0
    own_tot = np.zeros(n); exp_tot = np.zeros(n); taken = vetoed = 0
    q0, dq = 0.004, (0.003 if security else 0.015)
    for t in range(T):
        coupled = partner >= 0
        P = np.ones(n) + 0.3 * (li + ld)          # solo sources + new feature
        S = np.zeros(n); appraisal = np.zeros(n); hazard = np.full(n, q0)
        shared = np.where(coupled, 1.0, 0.0)
        for i in range(n):
            j = partner[i]
            if j < 0 or rng.random() > p_opp:
                continue
            G = rng.uniform(0.5, 3.0)
            r = 0.2
            # actual bundle loss per partner, same scale as the bundle term below
            Rj = 0.5 * (k * r * (1 + b) + (0 if protect else k * (1 - r) * b))
            L = 0.5 * k * (1 + b) + LAM * 6.0 * 0.5 ** 2 * 0.25
            if G - Rj - (0.1 if protect else 0) < 0:
                continue                      # i declines: not worth it to i
            netj = kappas[j] * G - Rj - dq * L - appr_coef[j] * G
            if veto and netj < 0:
                vetoed += 1; continue
            taken += 1
            P[i] += G
            shared[i] -= r; shared[j] -= r
            if protect:
                P[i] -= 0.1  # logistics cost: i uses solo time instead
            appraisal[j] += appr_coef[j] * G
            hazard[i] += dq; hazard[j] += dq
        for i in range(n):
            if partner[i] >= 0:
                s = max(shared[i], 0)
                bonus = b if (s >= 0.95 or protect) else 0.0
                P[i] += k * s * (1 + bonus) / 1.0 * 0.5
        # grief
        S += np.where(grief_left > 0, grief_amt, 0); grief_left -= 1
        # taste transmission along partner+friend edges
        for i in range(n):
            nbrs = [(partner[i], 1.0)] if partner[i] >= 0 else []
            nbrs += [(f, 0.5) for f in friends[i]]
            for j, w in nbrs:
                gap = max(0.0, (li[j] + ld[j]) - (li[i] + ld[i]))
                li[i] += 0.03 * w * theta * gap; ld[i] += 0.03 * w * (1 - theta) * gap
        # experienced value
        for i in range(n):
            others = list(friends[i]) + ([partner[i]] if partner[i] >= 0 else [])
            vic = sum(P[j] for j in others) / len(others)
            vs = sum(S[j] for j in others) / len(others)
            own = P[i] - LAM * S[i]
            own_tot[i] += own
            exp_tot[i] += own + kappas[i] * vic - LAM * eta[i] * vs - appraisal[i]
        # breakups (couple hazard = max of the two) and re-pairing
        for i in range(n):
            j = partner[i]
            if j > i and rng.random() < max(hazard[i], hazard[j]):
                for a in (i, j):
                    share = (P[a] - 1.0 - 0.3 * (li[a] + ld[a])) / P[a]
                    grief_amt[a] = share ** 2 * P[a]; grief_left[a] = 10
                    single_until[a] = t + 10; partner[a] = -1
                    ld[a] *= 0.3            # dependent liking unwinds
        singles = [i for i in range(n) if partner[i] < 0 and t >= single_until[i]]
        rng.shuffle(singles)
        for a, c in zip(singles[::2], singles[1::2]):
            partner[a], partner[c] = c, a
    return own_tot / T, exp_tot / T, taken, vetoed, (li + ld).mean()

def part4():
    n = 12
    print("\n4. Multi-agent (n=12, 6 couples + ring of friends, 300 periods, 20 seeds)")
    print("   scenario                     own   experienced  gini_exp  taken  vetoed  taste")
    pops = {"all k=0": [0.0] * n, "all k=0.3": [0.3] * n, "all k=0.6": [0.6] * n,
            "mixed 0/.3/.6": [0.0, 0.3, 0.6] * 4, "all k=-0.3 (envy)": [-0.3] * n,
            "mixed with 4 envious": [-0.3, 0.3, 0.6] * 4}
    configs = [("veto", dict(veto=True)), ("no veto", dict(veto=False)),
               ("veto+protect+security", dict(veto=True, protect=True, security=True)),
               ("no veto+protect+security", dict(veto=False, protect=True, security=True))]
    for cname, ckw in configs:
        print(f"  [{cname}]")
        for pname, ks in pops.items():
            res = [simulate(ks, seed=s, **ckw) for s in range(20)]
            own = np.mean([r[0].mean() for r in res]); ex = np.mean([r[1].mean() for r in res])
            g = np.mean([gini(r[1]) for r in res])
            tk = np.mean([r[2] for r in res]); vt = np.mean([r[3] for r in res])
            tst = np.mean([r[4] for r in res])
            print(f"   {pname:27s} {own:5.2f}  {ex:6.2f}       {g:.3f}    {tk:5.0f}  {vt:5.0f}  {tst:.2f}")
    print("  [eta/kappa = 0.3, no veto+protect+security]")
    for pname in ["all k=0.6", "all k=-0.3 (envy)"]:
        res = [simulate(pops[pname], seed=s, veto=False, protect=True, security=True,
                        eta_ratio=0.3) for s in range(20)]
        print(f"   {pname:27s} {np.mean([r[0].mean() for r in res]):5.2f}  "
              f"{np.mean([r[1].mean() for r in res]):6.2f}")

if __name__ == "__main__":
    rng = np.random.default_rng(0)
    part1(); part2(rng); part3(); part4()
