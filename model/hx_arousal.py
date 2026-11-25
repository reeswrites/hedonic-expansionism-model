"""Arousal as three parameters on top of the v1 fractal-liking model (wall-clock recovery).

From prior-art/stimulation_challenge.md: arousal acts on pleasure mainly through attention.
  capture     higher arousal lowers the threshold at which aversive parts grab attention
              (equanimity still raises it): tau_eff = TAU*(1+2e)*(1 - 0.5*a)
  narrowing   higher arousal sharpens priority: the top attended part gets weight (1+a),
              the others (1 - 0.5a); applies to whatever wins, pleasant or aversive
  transfer    leftover arousal polarizes: both pleasant and unpleasant parts scaled by (1+0.3a)
  engagement  inverted U: attention to liked parts is lost to mind-wandering at low arousal and
              to distraction at high arousal: eng = 1 - 0.8*(2a-1)^2 (Aston-Jones & Cohen;
              Unsworth & Robison); aversive capture is not reduced by low engagement
  fit         small bonus 0.2*(1 - |a - ideal|) for matching the person's current ideal arousal
  carryover   part of each hour's positive feeling carries into the next hour; calm pleasure
              decays slower (keep 0.6) than excited pleasure (keep 0.2); the excited share is a.
Question: does equanimity matter more at high arousal? And how does calm vs excited
pleasure change daily totals?
"""
import numpy as np
import hx_model_v1 as m

def run(a, e, r=3.0, ideal=0.5, seed=0, days=30, keep=None, eng_on=True):
    rng = np.random.default_rng(seed)
    world = m.make_world(rng)
    feats = {n: m.coarse(world[n], D, r) for n, D, _, _ in m.ACTIVITIES}
    fresh = {k: np.ones(len(v)) for k, v in feats.items()}
    tau = m.TAU * (1 + 2 * e) * (1 - 0.5 * a)
    keep = ((1 - a) * 0.6 + a * 0.2) if keep is None else keep
    eng = (1 - 0.8 * (2 * a - 1) ** 2) if eng_on else 1.0
    carry, total, neg_hours, n = 0.0, 0.0, 0, 0
    for _ in range(days):
        for name, D, _, hours in m.ACTIVITIES:
            for _ in range(hours):
                ell, h = feats[name], fresh[name]
                intr = np.where(ell < -tau)[0]; intr = intr[np.argsort(ell[intr])][:m.A]
                liked = np.where(ell > 0)[0]
                pick = liked[np.argsort(-(ell[liked] * h[liked]))][:m.A - len(intr)]
                vals_pos = list(ell[pick] * h[pick]); vals_neg = list(-ell[intr])
                # narrowing: whatever wins attention (largest magnitude) gets more weight
                items = [(v, +1) for v in vals_pos] + [(v, -1) for v in vals_neg]
                items.sort(key=lambda x: -x[0])
                pos = neg = 0.0
                for k, (v, sgn) in enumerate(items):
                    w = (1 + a) if k == 0 else (1 - 0.5 * a)
                    if sgn > 0: pos += w * v
                    else: neg += w * v
                pos *= (1 + 0.3 * a) * eng; neg *= 1 + 0.3 * a
                v = m.CAP * np.tanh(pos / m.CAP) - (1 - e) * m.CAP * np.tanh(neg / m.CAP)
                v += 0.2 * (1 - abs(a - ideal))
                v_felt = v + carry
                carry = keep * max(v, 0.0)
                total += v_felt; neg_hours += v_felt < 0; n += 1
                for k2 in fresh:
                    used = np.zeros(len(fresh[k2]), bool)
                    if k2 == name: used[pick] = True
                    fresh[k2][used] -= m.ALPHA * fresh[k2][used]
                    fresh[k2][~used] += m.RHO * (1 - fresh[k2][~used])
    return total / n, neg_hours / n

def avg(**kw):
    r = np.array([run(seed=s, **kw) for s in range(20)])
    return r.mean(axis=0)

if __name__ == "__main__":
    print("T1. Mean felt valence (and % negative hours) by arousal and equanimity, resolution 3")
    print(f"{'arousal':>8} | " + " | ".join(f"e={e:<4}" for e in [0.0, 0.5, 0.8]) + " | equanimity gain (0 -> 0.8)")
    for a in [0.2, 0.5, 0.8]:
        cells, vals = [], []
        for e in [0.0, 0.5, 0.8]:
            v, nh = avg(a=a, e=e); vals.append(v); cells.append(f"{v:5.2f} ({nh:3.0%})")
        print(f"{a:>8} | " + " | ".join(cells) + f" | {vals[2]-vals[0]:+.2f}")

    print("\nT2. Calm vs excited carryover, isolated (arousal 0.5, e=0.5): no carryover / excited (0.2) / calm (0.6)")
    for keep in [0.0, 0.2, 0.6]:
        v, _ = avg(a=0.5, e=0.5, keep=keep)
        print(f"  carryover kept {keep}: mean felt valence {v:5.2f}")

    print("\nT4. Without the engagement curve (the biased first version), for comparison: best arousal, ideal 0.5")
    best = max(((avg(a=a, e=0.5, eng_on=False)[0], a) for a in [0.1, 0.3, 0.5, 0.7, 0.9]))
    print(f"  best arousal {best[1]} (valence {best[0]:.2f})")

    print("\nT3. Ideal arousal varies by person/state: best arousal level for ideal 0.2 / 0.5 / 0.8 (e=0.5)")
    for ideal in [0.2, 0.5, 0.8]:
        best = max(((avg(a=a, e=0.5, ideal=ideal)[0], a) for a in [0.1, 0.3, 0.5, 0.7, 0.9]))
        print(f"  ideal {ideal}: best arousal {best[1]} (valence {best[0]:.2f})")
