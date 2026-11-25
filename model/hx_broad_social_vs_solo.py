"""Head-to-head: a broad social life vs a broad solo life, at equal time.

Each period, a share sigma of time is social, spread by rotation over n_p people (you see the
freshest one); the rest is solo, rotated over n_s solo sources.

People:
  closeness c_j grows with time spent with j and slowly decays: intimacy needs time, so
  spreading over many people keeps each tie shallow. Shared relief, togetherness and
  autonomy all depend on closeness (weak ties cost autonomy, close ones don't).
  Each person carries a pool of tastes you don't have yet; time with them moves some into
  your own solo liking (other minds sample beyond your habits). Pools run out.
  You also take on a share of their suffering (eta) and of their pleasure (kappa).
  Each person can be lost (probability q per period); grief is convex in the share of your
  pleasure they carried; they're replaced by a new acquaintance.
  A social battery drains with social time (faster for low sociability gamma).
Shared activities draw on your own liking stock (you do liked things together), amplified.
Solo sources: liking with freshness; slow solo exploration; solitude relief rho_alone.
"""
import itertools, numpy as np

T, DELTA, LAM = 300, 0.985, 1.5
BASE = dict(gamma=1.0, amp=1.3, bundle=0.4, kappa=0.4, eta=0.15, other_S=0.6,
            rho_shared=0.15, rho_alone=0.03, aut=0.3, conflict=0.03, coord=0.02,
            grow=0.08, decay=0.01, c_cap=1.0, pool=1.5, theta=0.08, e_solo=0.01,
            alpha=0.5, alpha_soc=0.25, rec=0.3, q=0.004, grief=10.0, drain=0.25, recharge=0.25,
            shock=0.04, fade=0.05, Lmax=4.0)
g = lambda S: np.exp(-0.3 * S)

def run(P, sigma, n_p, n_s, seed=0):
    rng = np.random.default_rng(seed)
    c = np.full(n_p, 0.3); hp = np.ones(n_p); pool = np.full(n_p, P["pool"])
    hs = np.ones(n_s); Ls = 1.0; S, B, V = 1.0, 1.0, 0.0
    for t in range(T):
        soc = sigma if (n_p > 0 and B > 0.05) else 0.0
        alone = 1 - soc
        pleasure, relief, imported = 0.0, 0.0, 0.0
        if soc > 0:
            j = np.argmax(hp * (0.5 + c))
            cj = c[j]
            joy = P["gamma"] * P["amp"] * Ls * (0.7 + 0.3 * cj) * hp[j]   # shared activities use your liking too
            pleasure += soc * (joy + P["bundle"] * cj + P["kappa"] * joy - P["aut"] * (1 - cj))
            relief = P["rho_shared"] * min(P["gamma"], 1.0) * cj * soc
            imported = P["eta"] * P["other_S"] * soc
            gain = min(pool[j], P["theta"] * soc * (0.5 + cj))
            pool[j] -= gain; Ls += gain * (1 - Ls / P["Lmax"])
            c[j] = min(P["c_cap"], c[j] + P["grow"] * soc * (1 - c[j]))
            hp[j] -= P["alpha_soc"] * hp[j]   # people renew better than solo sources
            rest = np.ones(n_p, bool); rest[j] = False
            hp[rest] += P["rec"] * (1 - hp[rest])
        c *= (1 - P["decay"])
        if n_s > 0 and alone > 0:
            k = np.argmax(hs)
            pleasure += alone * Ls * hs[k]
            hs[k] -= P["alpha"] * hs[k]
            rest = np.ones(n_s, bool); rest[k] = False
            hs[rest] += P["rec"] * (1 - hs[rest])
            Ls += P["e_solo"] * alone * (1 - Ls / P["Lmax"]) * min(n_s, 4) / 4
        total = pleasure
        V += DELTA**t * (g(S) * total - LAM * S)
        # losses: each person may leave; grief convex in the share of pleasure they carried
        for j in range(n_p):
            if rng.random() < P["q"]:
                share_j = (soc * c[j]) / (soc + alone + 1e-9)
                S += P["grief"] * share_j**2
                c[j] = 0.1; pool[j] = P["pool"]; hp[j] = 1.0
        S = (S * (1 - P["fade"]) + P["shock"] - relief * S - P["rho_alone"] * alone * S
             + P["conflict"] * soc + P["coord"] * soc * np.log1p(n_p) + LAM * 0 + imported * 0.3)
        S = max(S, 0.0)
        B += -P["drain"] * soc / max(P["gamma"], 0.2) + P["recharge"] * alone
        B = min(max(B, 0.0), 1.0)
    return V

SIG = [0.0, 0.25, 0.5, 0.75]
NP = [1, 3, 6, 12]
NS = [1, 4, 8]

def evaluate(P, seeds=8):
    v = lambda s, a, b: np.mean([run(P, s, a, b, sd) for sd in range(seeds)])
    out = {}
    out["narrow solo"] = v(0.0, 0, 1)
    out["broad solo"] = max((v(0.0, 0, b), b) for b in NS)
    out["narrow social (1 person)"] = max((v(s, 1, b), s) for s in SIG[1:] for b in [8])
    out["broad social"] = max((v(s, a, 8), s, a) for s in SIG[1:] for a in NP[1:])
    out["best overall"] = max((v(s, a, b), s, a, b) for s in SIG for a in NP for b in NS)
    return out

def P_(**kw):
    P = dict(BASE); P.update(kw); return P

TYPES = {
    "average": {},
    "low sociability": dict(gamma=0.6),
    "solitude is my relief": dict(rho_alone=0.10, gamma=0.8),
    "only weak ties possible": dict(c_cap=0.3),
    "high empathic distress": dict(eta=0.6),
    "high relationship risk": dict(q=0.02, grief=16.0),
}

if __name__ == "__main__":
    for name, kw in TYPES.items():
        r = evaluate(P_(**kw))
        bs, (bsv, bsn) = r["narrow solo"], r["broad solo"]
        ns = r["narrow social (1 person)"]
        bsoc = r["broad social"]; best = r["best overall"]
        print(f"=== {name}")
        print(f"  narrow solo               {bs:7.1f}")
        print(f"  broad solo                {bsv:7.1f}  ({bsn} solo sources)")
        print(f"  narrow social (1 person)  {ns[0]:7.1f}  (social share {ns[1]})")
        print(f"  broad social              {bsoc[0]:7.1f}  (social share {bsoc[1]}, {bsoc[2]} people)")
        print(f"  best overall              {best[0]:7.1f}  (social {best[1]}, {best[2]} people, {best[3]} solo sources)")

    print("\n=== which premises decide it (average type): broad solo vs best broad social vs best overall")
    for asoc in [0.5, 0.25]:
        for rel in [0.05, 0.15, 0.3]:
            for grow in [0.04, 0.08, 0.16]:
                r = evaluate(P_(alpha_soc=asoc, rho_shared=rel, grow=grow), seeds=4)
                b = r["broad social"]; best = r["best overall"]
                print(f"  people renew {'better' if asoc < 0.5 else 'same  '} | shared relief {rel:<4} | closeness growth {grow:<4} | "
                      f"broad solo {r['broad solo'][0]:6.1f}  broad social {b[0]:6.1f} ({b[1]}, {b[2]}p)  "
                      f"best {best[0]:6.1f} (social {best[1]}, {best[2]}p)")

    print("\n=== average: value by number of people (social share 0.5, 8 solo sources)")
    for a in [1, 2, 3, 4, 6, 8, 12]:
        val = np.mean([run(P_(), 0.5, a, 8, sd) for sd in range(8)])
        print(f"  {a:2d} people: {val:7.1f}")
