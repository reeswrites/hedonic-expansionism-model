"""Pleasure as relief: liking-driven savoring vs wanting-driven grabbing.

State: suffering S, liking stock L, capacity c, plus one go-to pleasure source with
liking ls and freshness h, and an urge level w (wanting).
Per period, one action:
  clean  : S -= RHO_C*S
  savor  : experience the source fully. quality q = g(S)*c*ls*h. Adds q to pleasure,
           relieves S -= RHO_P*q*S (undoing effect), builds liking L += DS*p(S)*c.
           Source habituates (h falls), recovers when rested. ls is renewing.
  grab   : the same source used to escape, driven by urge w. Same pleasure and relief
           per use, but ls depletes, attention narrows (c falls slightly), no liking
           is built, and each use raises w (incentive sensitization).
  expand : L += DLT*p(S)*c
Pleasure P = g(S)*c*L (+ q when the source is used). V = sum delta^t (P - lam*S).
"""
import numpy as np

T, DELTA, LAM, DLT, DS = 100, 0.97, 1.5, 0.5, 0.2
RHO_C, RHO_P, FADE, PSI = 0.25, 0.4, 0.03, 0.05
ALPHA, REC = 0.5, 0.3           # source habituation / recovery
BETA, MU_G, W_UP, W_DECAY, W_TRIG = 0.05, 0.02, 0.3, 0.1, 1.0
g = lambda S: np.exp(-0.3 * S); p = lambda S: np.exp(-0.3 * S)

def sim(S0, policy, thr):
    S, L, c, ls, h, w, V = S0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0
    counts = {"clean": 0, "savor": 0, "grab": 0, "expand": 0, "none": 0}
    for t in range(T):
        a = policy(S, h, w, thr)
        counts[a] += 1
        q = g(S) * c * ls * h if a in ("savor", "grab") else 0.0
        V += DELTA**t * (g(S) * c * L + q - LAM * S)
        if a == "clean":
            S -= RHO_C * S
        elif a in ("savor", "grab"):
            S -= RHO_P * q * S
            h -= ALPHA * h
            if a == "savor":
                L += DS * p(S) * c
            else:
                ls *= (1 - BETA); c *= (1 - MU_G); w += W_UP
        elif a == "expand":
            L += DLT * p(S) * c
        if a not in ("savor", "grab"):
            h += REC * (1 - h)
        w *= (1 - W_DECAY)
        S -= FADE * S
        c += PSI * (1 - c)
    return V, counts

# Policies
clean_first = lambda S, h, w, thr: "clean" if S > thr else "expand"
def savor_liking(S, h, w, thr):
    # liking-driven: savor when the source is fresh, otherwise clean relief or expand
    if S > thr:
        return "savor" if h > 0.6 else "clean"
    return "savor" if h > 0.9 else "expand"
def savor_only_relief(S, h, w, thr):
    # pleasure is the only relief available; still liking-driven
    if S > thr:
        return "savor" if h > 0.6 else "expand"
    return "savor" if h > 0.9 else "expand"
def grab_wanting(S, h, w, thr):
    # wanting-driven: use the source whenever distressed OR whenever the urge is high
    return "grab" if (S > thr or w > W_TRIG) else "expand"
nothing = lambda S, h, w, thr: "none"

POLICIES = [("clean relief, then expand", clean_first),
            ("savor (liking-driven) + clean", savor_liking),
            ("savor only (no clean relief)", savor_only_relief),
            ("grab (wanting-driven)", grab_wanting),
            ("do nothing", nothing)]
THRS = [0.1, 0.25, 0.5, 1, 2, 4]

for S0 in [8.0, 3.0]:
    print(f"=== starting distress S0={S0}")
    for name, pol in POLICIES:
        V, thr, cnt = max(((*sim(S0, pol, th)[:1], th, sim(S0, pol, th)[1]) for th in THRS),
                          key=lambda x: x[0])
        used = ", ".join(f"{k} {v}" for k, v in cnt.items() if v)
        print(f"  {name:32s} V={V:7.1f}  thr={thr:<4}  [{used}]")
    print()

# Sensitivity: how strong must sensitization be for grabbing to lose to clean relief / nothing?
print("Grab vs alternatives as wanting sensitization varies (S0=8)")
base_clean = max(sim(8, clean_first, th)[0] for th in THRS)
base_none = sim(8, nothing, 1)[0]
for wu in [0.0, 0.15, 0.3, 0.6]:
    for beta in [0.0, 0.05, 0.15]:
        W_UP, BETA = wu, beta
        Vg, cnt = max((sim(8, grab_wanting, th) for th in THRS), key=lambda x: x[0])
        print(f"  urge growth={wu:<4} liking depletion={beta:<4} grab V={Vg:7.1f} uses={cnt['grab']:3d}  "
              f"(clean-first {base_clean:.1f}, nothing {base_none:.1f})")
