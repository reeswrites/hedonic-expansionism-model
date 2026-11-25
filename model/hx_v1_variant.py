import numpy as np, hx_model_v1 as m
# Variant: equanimity also stops aversive parts from grabbing attention (intrusion threshold rises with e)
orig_run = m.run
def run_v(r, e, seed, days=40):
    m.TAU = 0.8 * (1 + 2 * e)
    out = orig_run(r, e, seed, days)
    m.TAU = 0.8
    return out
print("Variant: equanimity also reduces intrusion")
print("r    e    mean   near-ceiling  negative  mundane  rich")
for e in [0.0, 0.5, 0.8]:
    for r in [1.0, 2.0, 3.0, 4.0]:
        s = [m.summarize(run_v(r, e, sd)) for sd in range(30)]
        k = {key: np.mean([x[key] for x in s]) for key in s[0]}
        print(f"{r:<4} {e:<4} {k['mean']:6.2f}   {k['near']:6.1%}      {k['neg']:6.1%}  {k['mund']:6.2f}  {k['rich']:6.2f}")
    print()
