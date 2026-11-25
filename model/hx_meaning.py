"""Meaning: pleasure, quieting, or attention? (prior-art/meaning.md)

A day-level model. Each period brings a stressor with probability p_stress (pain of size P),
and the person does a repeated activity whose freshness h decays with use and recovers.
Meaning m in [0,1] can act in three ways (each switchable):
  quieting   suffering = pain x resistance; meaning lowers resistance:
             resistance = (1-e)(1 - K_R*m), pain intensity unchanged (Hill et al. 2018:
             purpose cut the negative-affect response to stressors by ~36%)
  exposure   meaningful lives take on more stressors: p_stress*(1 + K_X*m) (Baumeister et al. 2013)
  attention  meaning slows adaptation of the activity: decay ALPHA*(1 - K_A*m)
             (Kahneman & Thaler 2006; O'Brien & Kassirer 2019)
  pleasure   small direct term B_M*m (King et al. 2006: weak)
Felt value per period = activity pleasure + B_M*m - LAM * suffering.
"""
import numpy as np

T, LAM, ALPHA, REC = 400, 2.0, 0.35, 0.25
K_R, K_X, K_A, B_M = 0.4, 0.2, 0.5, 0.05

def run(m, p_stress=0.2, pain=1.5, e=0.3, quiet=True, expose=True, attend=True, pleas=True, seed=0):
    rng = np.random.default_rng(seed)
    h, V, neg = 1.0, 0.0, 0
    ps = p_stress * (1 + K_X * m) if expose else p_stress
    resist = (1 - e) * (1 - K_R * m) if quiet else (1 - e)
    decay = ALPHA * (1 - K_A * m) if attend else ALPHA
    for t in range(T):
        act = 1.0 * h
        h -= decay * h; h += REC * (1 - h)
        suffer = pain * resist if rng.random() < ps else 0.0
        v = act + (B_M * m if pleas else 0.0) - LAM * suffer
        V += v; neg += v < 0
    return V / T, neg / T

def avg(**kw):
    r = np.array([run(seed=s, **kw) for s in range(40)])
    return r.mean(axis=0)

def gain(**kw):
    return avg(m=1.0, **kw)[0] - avg(m=0.0, **kw)[0]

if __name__ == "__main__":
    print("T1. Value of meaning (m=1 minus m=0), all mechanisms on, by stress level")
    for ps in [0.0, 0.1, 0.2, 0.4]:
        print(f"  stressor rate {ps:<4} gain {gain(p_stress=ps):+.3f}")

    print("\nT2. Signatures: gain from meaning by stress level, one mechanism at a time")
    mech = {"quieting only": dict(quiet=True, expose=False, attend=False, pleas=False),
            "attention only": dict(quiet=False, expose=False, attend=True, pleas=False),
            "pleasure only": dict(quiet=False, expose=False, attend=False, pleas=True),
            "exposure only": dict(quiet=False, expose=True, attend=False, pleas=False)}
    print("  " + " " * 16 + "".join(f"stress {ps:<6}" for ps in [0.0, 0.2, 0.4]))
    for name, kw in mech.items():
        print(f"  {name:16s}" + "".join(f"{gain(p_stress=ps, **kw):+12.3f}" for ps in [0.0, 0.2, 0.4]))

    print("\nT3. Baumeister pattern: meaning brings more stressors but less suffering per stressor")
    for m in [0.0, 1.0]:
        v, neg = avg(m=m, p_stress=0.2)
        print(f"  meaning {m}: value {v:.3f}, share of periods negative {neg:.1%}")

    print("\nT4. Meaning vs equanimity: both lower resistance; do they substitute?")
    for e in [0.0, 0.5, 0.8]:
        print(f"  equanimity {e}: gain from meaning {gain(p_stress=0.3, e=e):+.3f}")
