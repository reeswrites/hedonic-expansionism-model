import numpy as np, hx_model_v1 as m
# Wall-clock recovery: every activity's features recover each hour unless attended.
def run_wall(r, e, seed, days=40, variant=True):
    rng = np.random.default_rng(seed)
    world = m.make_world(rng)
    tau = m.TAU * (1 + 2 * e) if variant else m.TAU
    feats = {n: m.coarse(world[n], D, r) for n, D, _, _ in m.ACTIVITIES}
    fresh = {k: np.ones(len(v)) for k, v in feats.items()}
    log = []
    for _ in range(days):
        for name, D, _, hours in m.ACTIVITIES:
            for _ in range(hours):
                ell, h = feats[name], fresh[name]
                intr = np.where(ell < -tau)[0]; intr = intr[np.argsort(ell[intr])][:m.A]
                liked = np.where(ell > 0)[0]
                pick = liked[np.argsort(-(ell[liked]*h[liked]))][:m.A-len(intr)]
                pos = (ell[pick]*h[pick]).sum(); neg = -ell[intr].sum()
                v = m.CAP*np.tanh(pos/m.CAP) - (1-e)*m.CAP*np.tanh(neg/m.CAP)
                for k in fresh:
                    used = np.zeros(len(fresh[k]), bool)
                    if k == name: used[pick] = True
                    fresh[k][used] -= m.ALPHA*fresh[k][used]
                    fresh[k][~used] += m.RHO*(1-fresh[k][~used])
                log.append((name, v))
    return log
for variant in [False, True]:
    print("equanimity also reduces intrusion" if variant else "equanimity softens pain only")
    for e in [0.0, 0.8]:
        for r in [1.0, 2.0, 3.0, 4.0]:
            s = [m.summarize(run_wall(r, e, sd, variant=variant)) for sd in range(30)]
            k = {key: np.mean([x[key] for x in s]) for key in s[0]}
            print(f"  e={e} r={r}  mean={k['mean']:.2f} near={k['near']:.1%} neg={k['neg']:.1%} mund={k['mund']:.2f} rich={k['rich']:.2f}")
