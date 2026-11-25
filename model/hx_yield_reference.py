"""Pleasure yield under a moving reference point.

Tests the "Pleasure yield" profile page together with the strongest objection from the
evolution check (reference-dependent hedonics recalibrate gains away).

Each period you use up to SLOTS pleasure sources, choosing by expected yield.
A source has:
  mean liking l, floor f (probability it shows up at all when used; if it shows up it
  yields l/f so that the mean is the same), freshness h (satiates with use, resets with
  rest), and a type:
    plain    dedicated hedonic channel
    relief   yields the current deficit D, which regenerates every period (hunger, fatigue,
             stiffness); scaled by a framing factor. Relief is measured against the deficit
             state, so it is not adapted away by the reference point (assumption).
    threat   opponent process: each use gives an aversive shock a_n then a pleasant
             after-effect b_n. The shock habituates with uses; the after-effect either
             stays fixed or grows toward b_max (untested for cold; tested as a variant).
    skill    liking grows with use while learnable structure remains (learning progress).
Reference point R (moving): R' = R + k*(phi*raw - R). phi=1 is the full hedonic
treadmill, phi<1 partial adaptation (set points that move, Diener et al. 2006).
Experienced value each period = relief + gain(raw - R), where shortfalls below R are
weighted by LOSS (a normative weight >= 1).
Exploration: every third period one slot goes to a source being acquired or a threat
source (spaced, scheduled exposure). Expansion: every 40 periods, try to add a new plain source (initially disliked,
acquired over spaced exposure) or raise a skill source's structure.
"""
import numpy as np

T, SLOTS, ALPHA, REC, K_REF = 400, 2, 0.45, 0.35, 0.03

def make_sources(kind, rng):
    S = []
    if kind == "high_floor":
        S = [dict(t="plain", l=1.0, f=0.95) for _ in range(4)]
    elif kind == "high_peak":
        S = [dict(t="plain", l=1.0, f=0.40) for _ in range(4)]
    elif kind == "mixed":
        S = [dict(t="plain", l=1.0, f=0.95) for _ in range(3)] + [dict(t="plain", l=1.0, f=0.40)]
    for s in S:
        s["h"] = 1.0
    return S

def gain(x, loss):
    return x if x >= 0 else loss * x

def run(kind="high_floor", phi=0.8, loss=2.0, expand=False, relief=False, threat=None,
        skill=False, seed=0):
    rng = np.random.default_rng(seed)
    src = make_sources(kind, rng)
    if threat:
        src.append(dict(t="threat", l=0.0, f=1.0, h=1.0, a=1.2, b=0.6, n=0, grow=(threat == "grows")))
    if skill:
        src.append(dict(t="skill", l=0.6, f=1.0, h=1.0, struct=3.0))
    D, R, V, below, raws = 0.0, 0.0, 0.0, 0, []
    for t in range(T):
        # expansion: add an initially disliked source acquired by spaced exposure
        if expand and t > 0 and t % 40 == 0:
            src.append(dict(t="plain", l=-0.3, f=0.9, h=1.0, acq=0, target=rng.uniform(0.8, 1.4)))
        # choose: highest expected yield = l*h (threat: after-effect minus shock)
        def expected(s):
            if s["t"] == "threat":
                return (s["b"] - s["a"] * 0.85 ** s["n"]) * s["h"] + 0.3  # people try it for the rebound
            if "acq" in s:
                return s["l"] * s["h"] + 0.4  # curiosity bonus keeps exposures coming
            return s["l"] * s["h"]
        order = sorted(range(len(src)), key=lambda i: -expected(src[i]))
        explore = [i for i, s in enumerate(src) if s["t"] == "threat" or ("acq" in s and s["acq"] < 15)]
        if explore and t % 3 == 0:     # scheduled, spaced exploration slot
            pick = explore[(t // 3) % len(explore)]
            used = {pick} | set([i for i in order if i != pick][:SLOTS - 1])
        else:
            used = set(order[:SLOTS])
        raw = 0.0
        for i in used:
            s = src[i]
            if s["t"] == "threat":
                shock = s["a"] * 0.85 ** s["n"]
                raw += (s["b"] - shock) * s["h"]
                s["n"] += 1
                if s["grow"]:
                    s["b"] += 0.03 * (1.6 - s["b"])
            else:
                shows = rng.random() < s["f"]
                raw += (s["l"] / s["f"]) * s["h"] if shows else 0.0
                if "acq" in s:      # acquired taste: liking rises toward target with exposures
                    s["acq"] += 1
                    s["l"] += 0.12 * (s["target"] - s["l"])
                if s["t"] == "skill" and s["struct"] > 0:
                    step = min(0.02, s["struct"]); s["l"] += step; s["struct"] -= step
            s["h"] -= ALPHA * s["h"]
        for i, s in enumerate(src):
            if i not in used:
                s["h"] += REC * (1 - s["h"])
        # relief: deficit regenerates; one relief per period if available
        rel = 0.0
        if relief:
            D += 0.5
            rel = 0.8 * D * 1.0
            D = 0.0
        exp_val = rel + gain(raw - R, loss)
        V += exp_val
        below += (raw - R) < 0
        raws.append(raw)
        R += K_REF * (phi * raw - R)
    return V / T, below / T

def avg(seeds=20, **kw):
    r = np.array([run(seed=s, **kw) for s in range(seeds)])
    return r.mean(axis=0)

if __name__ == "__main__":
    print("E1. Portfolio: high-floor vs high-peak (same mean yield). Mean experienced value / % periods below reference")
    for phi in [0.0, 0.8, 1.0]:
        for loss in [1.0, 2.0]:
            cells = []
            for kind in ["high_floor", "mixed", "high_peak"]:
                v, b = avg(kind=kind, phi=phi, loss=loss)
                cells.append(f"{kind:>10} {v:5.2f}/{b:4.0%}")
            print(f"  adaptation phi={phi:<4} loss weight {loss}: " + "   ".join(cells))

    print("\nE2. Does expansion survive a moving reference point? (high-floor base)")
    print("    mean experienced value: no expansion / with expansion / with skill source / both")
    for phi in [0.0, 0.5, 0.8, 1.0]:
        a = avg(phi=phi)[0]; b = avg(phi=phi, expand=True)[0]
        c = avg(phi=phi, skill=True)[0]; d = avg(phi=phi, expand=True, skill=True)[0]
        print(f"  phi={phi:<4} {a:6.2f}  {b:6.2f}  {c:6.2f}  {d:6.2f}")

    print("\nE3. Relief as a floor under full adaptation (phi=1)")
    for kind in ["high_floor", "high_peak"]:
        a = avg(kind=kind, phi=1.0)[0]; b = avg(kind=kind, phi=1.0, relief=True)[0]
        print(f"  {kind:>10}: without relief {a:6.2f}   with relief {b:6.2f}")

    print("\nE4. Threat exploitation (opponent process): after-effect fixed vs growing")
    for phi in [0.0, 0.8]:
        a = avg(phi=phi)[0]; b = avg(phi=phi, threat="fixed")[0]; c = avg(phi=phi, threat="grows")[0]
        print(f"  phi={phi:<4} no threat source {a:6.2f}   after-effect fixed {b:6.2f}   after-effect grows {c:6.2f}")
