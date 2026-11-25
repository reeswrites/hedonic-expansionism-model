"""When is alone better than social? Extends hx_social_vs_solo.py with the conditions it lacked.

New pieces:
  absorption   some solo pleasures need full attention (reading, practice, meditation).
               Done with others present they lose a share OMEGA of their value, and they
               grow with skill only when done alone.
  battery      a social battery B in [0,1]: social time drains it (faster for low
               sociability gamma), time alone recharges it. Below B_LOW, social time
               costs suffering instead of relieving it (overstimulation).
  solitude     time alone can itself relieve suffering (rho_alone), alongside or instead
  relief       of shared relief (rho_shared). People differ in which relief works for them.
  loss         the main relationship ends with probability q per period. Grief is convex in
               the share of pleasure it carried, and the social liking stock falls back.
  parallel     a share of social time can be spent together but each absorbed in their own
               thing: absorption at (1-OMEGA), partial togetherness and relief, half the drain,
               and no skill growth (that needs real solitude).
  friends      social time spread over n friends: losing one carries 1/n of the share.
Policies:
  fixed        the same social share every period, plus a parallel fraction (searched)
  rhythm       battery-aware: social at a chosen dose when B >= threshold, else alone (searched)
  solo         never social
"""
import numpy as np

T, DELTA, LAM = 300, 0.985, 1.5
BASE = dict(gamma=1.0, amp=1.3, bundle=0.3, a_soc=0.25, a_solo=0.5, rec=0.3,
            e_soc=0.05, e_solo=0.02, theta=0.5,
            rho_shared=0.15, rho_alone=0.03, conflict=0.03,
            absorb=0.4, omega=0.6, skill=0.01, Lmax=4.0,
            drain=0.25, recharge=0.25, b_low=0.3, over=0.6,
            q=0.004, grief=8.0, shock=0.04, fade=0.05, n=1)
g = lambda S: np.exp(-0.3 * S)
p = lambda S: np.exp(-0.3 * S)

def run(P, policy, param, seed=0, par=0.0, dose=0.8):
    rng = np.random.default_rng(seed)
    Lsolo, Lab, Lc = 1.0, 1.0, 1.0
    hs, ha, hc = 1.0, 1.0, 1.0
    S, B, V = 1.0, 1.0, 0.0
    for t in range(T):
        if policy == "solo":
            sigma = 0.0
        elif policy == "fixed":
            sigma = param
        else:  # rhythm: social when the battery is high enough
            sigma = dose if B >= param else 0.0
        alone = 1 - sigma
        joint, par_t = sigma * (1 - par), sigma * par           # together-on-one-thing vs parallel
        ab, cas = alone * P["absorb"], alone * (1 - P["absorb"])
        # absorption done in parallel with others loses OMEGA of its value
        p_ab = ab * Lab * ha + par_t * Lab * ha * (1 - P["omega"])
        p_cas = cas * Lsolo * hs
        p_soc = joint * (P["gamma"] * P["amp"] * Lc * hc + P["bundle"]) + par_t * 0.6 * P["bundle"]
        over = max(0.0, P["b_low"] - B) / P["b_low"]          # 0..1 overstimulation
        pleasure = g(S) * (p_ab + p_cas + p_soc * (1 - P["over"] * over))
        share = p_soc / (p_ab + p_cas + p_soc + 1e-9)
        V += DELTA**t * (pleasure - LAM * S)
        # relationship loss: convex grief in the share it carried
        if sigma > 0 and rng.random() < P["q"]:
            S += P["grief"] * (share / P["n"])**2
            Lc = 1.0 + (Lc - 1.0) * (1 - 0.7 / P["n"])
        # freshness
        hs += -P["a_solo"] * cas * hs + P["rec"] * (1 - cas) * (1 - hs)
        ab_all = ab + par_t
        ha += -P["a_solo"] * ab_all * ha + P["rec"] * (1 - ab_all) * (1 - ha)
        hc += -P["a_soc"] * joint * hc + P["rec"] * (1 - joint) * (1 - hc)
        # learning: social taste learning; absorption skill grows only alone
        Lc += P["e_soc"] * joint * p(S) * (1 - Lc / P["Lmax"])
        Lsolo += (P["e_solo"] * cas + P["theta"] * P["e_soc"] * joint) * p(S) * (1 - Lsolo / P["Lmax"])
        Lab += P["skill"] * ab * (1 - Lab / P["Lmax"]) * 4
        # suffering: shocks, fading, shared relief (needs battery), solitude relief, conflict, overstimulation
        shared = P["rho_shared"] * min(P["gamma"], 1.0) * (joint + 0.5 * par_t) * (1 - over)
        S = S * (1 - P["fade"]) + P["shock"] - shared * S - P["rho_alone"] * alone * S \
            + P["conflict"] * joint + 0.3 * over * sigma
        S = max(S, 0.0)
        # battery: drains with social time (faster for low gamma), recharges alone
        B += -P["drain"] * (joint + 0.5 * par_t) / max(P["gamma"], 0.2) + P["recharge"] * alone
        B = min(max(B, 0.0), 1.0)
    return V

def best(P, seeds=8):
    avg = lambda pol, x: np.mean([run(P, pol, x, s) for s in range(seeds)])
    solo = avg("solo", 0)
    avgf = lambda s, pr: np.mean([run(P, "fixed", s, sd, par=pr) for sd in range(seeds)])
    avgr = lambda th, d: np.mean([run(P, "rhythm", th, sd, dose=d) for sd in range(seeds)])
    fixed = max((avgf(s, pr), s, pr) for s in np.round(np.arange(0, 1.01, 0.1), 2) for pr in [0.0, 0.5, 1.0])
    rhythm = max((avgr(th, d), th, d) for th in [0.2, 0.4, 0.6, 0.8, 1.0] for d in [0.3, 0.6, 0.9])
    return solo, fixed, rhythm

def P_(**kw):
    P = dict(BASE); P.update(kw); return P

def line(label, P):
    solo, (vf, sf, pr), (vr, th, d) = best(P)
    print(f"  {label:36s} solo {solo:7.1f} | fixed {vf:7.1f} (share {sf:.1f}, parallel {pr:.1f}) | "
          f"rhythm {vr:7.1f} (dose {d} when battery>={th})")

if __name__ == "__main__":
    print("T1. Sociability and absorption: best fixed social share")
    print(f"{'gamma':>6} | " + " ".join(f"absorb={a:<4}" for a in [0.0, 0.4, 0.8]))
    for gam in [0.4, 0.7, 1.0, 1.3]:
        cells = []
        for a in [0.0, 0.4, 0.8]:
            _, (vf, sf, pr), _ = best(P_(gamma=gam, absorb=a))
            cells.append(f"{sf:.1f} (par {pr:.1f})")
        print(f"{gam:>6} | " + "   ".join(cells))

    print("\nT2. Rhythm vs fixed mix (battery-aware alternation)")
    for gam in [0.4, 0.7, 1.0, 1.3]:
        line(f"gamma={gam}", P_(gamma=gam))

    print("\nT3. Which relief works for you: shared vs solitude")
    for label, kw in [("shared relief only", dict(rho_shared=0.15, rho_alone=0.0)),
                      ("solitude relief only", dict(rho_shared=0.0, rho_alone=0.10)),
                      ("both", dict(rho_shared=0.15, rho_alone=0.10))]:
        for gam in [0.7, 1.0]:
            line(f"{label}, gamma={gam}", P_(gamma=gam, **kw))

    print("\nT4. Relationship risk: how much to keep in solo sources")
    for q in [0.0, 0.004, 0.02, 0.05]:
        for grief in [4.0, 16.0]:
            line(f"loss prob {q}, grief scale {grief}", P_(q=q, grief=grief))

    print("\nT4b. Same risk, spread over 3 friends")
    for q in [0.02, 0.05]:
        line(f"loss prob {q}, grief 16, 3 friends", P_(q=q, grief=16.0, n=3))

    print("\nT5. Absorption skill: value of protected solitude over a long horizon")
    for skill in [0.0, 0.01, 0.03]:
        for omega in [0.2, 0.6, 0.9]:
            line(f"skill growth {skill}, interference {omega}", P_(skill=skill, omega=omega))
