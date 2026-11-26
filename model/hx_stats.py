"""Effect sizes with uncertainty, for any script in model/.

Two sources of uncertainty, reported separately:
  seed noise         paired(): run two policies on the same seeds (common random numbers) and
                     report the mean per-seed difference with its standard error. Pairing cancels
                     most noise shared by both policies, so it is tighter than comparing two means.
  parameter spread   sweep(): redraw the invented parameters, recompute the effect in each world,
                     and report its median, middle-50% range and the share of worlds where its
                     sign holds. With mostly invented constants, this is the real error bar.

Effects in this model have no units, so report them relative to something: a share of a
baseline, or a share of a yardstick effect computed in the same world (sweep's `scale`).
No p-values: with enough seeds any difference becomes "significant", and dividing by the
spread across seeds measures how noisy the simulation is, not how large the effect is.
"""
import contextlib

import numpy as np


def paired(f_a, f_b, seeds=20):
    """f_x(seed) -> scalar. Returns mean of f_b - f_a, its standard error, and per-seed diffs."""
    d = np.array([f_b(s) - f_a(s) for s in range(seeds)])
    return dict(diff=d.mean(), se=d.std(ddof=1) / np.sqrt(len(d)), n=len(d), diffs=d)


def fmt_paired(r, base=None):
    s = "%+.3f ± %.3f (SE, %d paired seeds)" % (r["diff"], r["se"], r["n"])
    if base:
        s += ", %+.0f%% of baseline" % (100 * r["diff"] / abs(base))
    return s


@contextlib.contextmanager
def perturbed(P, rng, keys, spread=3.0, cap=0.95):
    """Temporarily redraw P[k] log-uniformly within `spread`x of its value; fractions capped."""
    old = {k: P[k] for k in keys}
    try:
        for k in keys:
            v = old[k] * np.exp(rng.uniform(-np.log(spread), np.log(spread)))
            P[k] = min(v, cap) if old[k] < 1 else v
        yield
    finally:
        P.update(old)


def sweep(P, effect, keys, draws=60, scale=None, seed=0, spread=3.0):
    """effect() -> scalar computed under the current P; scale() -> yardstick in the same world.
    Returns median, quartiles and sign share of effect (or of effect/scale if given)."""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(draws):
        with perturbed(P, rng, keys, spread):
            e = effect()
            vals.append(e / scale() if scale else e)
    v = np.array(vals)
    return dict(median=np.median(v), q1=np.percentile(v, 25), q3=np.percentile(v, 75),
                pos=(v > 0).mean(), n=len(v), vals=v)


def fmt_sweep(r, pct=False):
    m = 100 if pct else 1
    u = "%" if pct else ""
    return "median %+.2f%s, middle half %+.2f%s to %+.2f%s, positive in %.0f%% of %d worlds" % (
        m * r["median"], u, m * r["q1"], u, m * r["q3"], u, 100 * r["pos"], r["n"])
