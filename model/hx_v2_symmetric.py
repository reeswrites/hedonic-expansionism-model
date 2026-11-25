"""Variant of v2: categorizing dulls BOTH directions (Rocklage: lower emotional intensity overall;
affect labeling also dampens negative feeling). Labeled aversive parts also capture attention less."""
import numpy as np, hx_model_v2 as m
v1 = m.v1

def run_sym(res, k, e=0.0, c=0.0, A=3, J=1.0, seed=0, days=m.DAYS):
    rng = np.random.default_rng(seed)
    world = v1.make_world(rng)
    feats = {n: m.judge(v1.coarse(world[n], D, res[n]), J, e) for n, D, _, _ in m.ACTIVITIES}
    fresh = {n: np.ones(len(f)) for n, f in feats.items()}
    log = []
    for _ in range(days):
        for name, _, _, hours in m.ACTIVITIES:
            ell = feats[name]; dull = 1 - k[name] * (1 - c)
            tau = m.TAU * (1 + 2 * e) / max(dull, 1e-6)
            for _ in range(hours):
                h = fresh[name]
                intr = np.where(ell < -tau)[0]; intr = intr[np.argsort(ell[intr])][:A]
                liked = np.where(ell > 0)[0]
                pick = liked[np.argsort(-(ell[liked] * h[liked]))][:A - len(intr)]
                pos = dull * (ell[pick] * h[pick]).sum()
                neg = dull * -ell[intr].sum()
                p_part = m.CAP * np.tanh(pos / m.CAP); n_part = (1 - e) * m.CAP * np.tanh(neg / m.CAP)
                log.append((name, p_part - n_part, p_part, n_part))
                for n2 in fresh:
                    used = np.zeros(len(fresh[n2]), bool)
                    if n2 == name: used[pick] = True
                    fresh[n2][used] -= m.ALPHA * fresh[n2][used]
                    fresh[n2][~used] += m.RHO * (1 - fresh[n2][~used])
    return log

def stats(x, e, c, judging=True, seeds=30):
    res, k = m.expert_setup(x)
    J = 1.0 if judging else 0.0
    rows = []
    for s in range(seeds):
        L = [r for r in run_sym(res, k, e, c, J=J, seed=s) if r[0] == "music"]
        v = np.array([r[1] for r in L]); pp = np.array([r[2] for r in L]); nn = np.array([r[3] for r in L])
        rows.append((v.mean(), np.abs(v).mean(), (v < 0).mean(), pp.mean(), nn.mean()))
    return np.mean(rows, axis=0)

print("Q1 symmetric dulling, e=0 c=0, music: valence / intensity / %neg")
for J in [False, True]:
    print(" judging", "on" if J else "off")
    for x in [0, 0.25, 0.5, 0.75, 1.0]:
        v, i, n, p, q = stats(x, 0, 0, J)
        print(f"  x={x:<5} val={v:5.2f} intensity={i:4.2f} neg={n:5.1%}")
print("\nQ2 symmetric, full expertise, judging on: valence / intensity / %neg")
for c in [0, 0.5, 1]:
    for e in [0, 0.5, 0.8]:
        v, i, n, p, q = stats(1.0, e, c)
        print(f"  c={c:<4} e={e:<4} val={v:5.2f} intensity={i:4.2f} neg={n:5.1%}")
