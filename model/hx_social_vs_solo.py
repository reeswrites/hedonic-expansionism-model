"""Solo vs social pleasure, built from the theory's premises about relational pleasure.

Each period a share sigma of time is social (with close, chosen people unless noted),
a share z is solo practice (equanimity etc.), the rest is solo pleasure.

Mechanisms for social advantage (each can be switched off):
  amp     co-presence multiplies the valence of shared experience (m > 1)
  bundle  superadditive joint pleasure b with no solo substitute
  renew   social sources habituate less (other minds keep supplying novelty)
  learn   liking through valuing: new tastes acquired faster with others
  transmit tastes learned with others partly internalize into your solo stock (theta)
  relief  shared burdens lower suffering (baseline)
Costs: coordination (availability < 1), autonomy cost for unchosen / non-close time,
conflict suffering, loss risk with convex grief (spread over n_friends), sociability gate gamma.
Solo practice: either a multiplicative converter cv on all pleasure (self as converter),
or an additive reducer of suffering (self as a small extra lever).
"""
import itertools, numpy as np

T, DELTA, LAM = 200, 0.98, 1.5
BASE = dict(amp=1.3, bundle=0.3, a_soc=0.25, a_solo=0.5, rec=0.3,
            e_solo=0.02, e_soc=0.05, theta=0.5, relief=0.15, avail=0.8,
            aut=0.0, conflict=0.03, q=0.01, grief=6.0, n_friends=3, gamma=1.0, drain=0.4,
            Lmax=4.0, shock=0.4, fade=0.05, zeta=0.05, practice="converter")
g = lambda S: np.exp(-0.3 * S)
p = lambda S: np.exp(-0.3 * S)

def run(sigma, z, P):
    Ls, Lc, hs, hc, S, cv, V = 1.0, 1.0, 1.0, 1.0, 1.0, 0.6, 0.0
    solo = max(0.0, 1 - sigma - z)
    for t in range(T):
        s_eff = sigma * P["avail"]
        ps = solo * Ls * hs
        pc = s_eff * (P["gamma"] * P["amp"] * Lc * hc + P["bundle"])
        pleasure = g(S) * cv * (ps + pc) - s_eff * P["aut"]
        share = pc / (ps + pc + 1e-9)
        grief = P["q"] * P["grief"] * share**2 / P["n_friends"]
        V += DELTA**t * (pleasure - LAM * (S + grief))
        # habituation: social habituates less
        hs += -P["a_solo"] * solo * hs + P["rec"] * (1 - solo) * (1 - hs)
        hc += -P["a_soc"] * s_eff * hc + P["rec"] * (1 - s_eff) * (1 - hc)
        # expansion: learning with others is faster; part transfers to solo stock
        room_s, room_c = 1 - Ls / P["Lmax"], 1 - Lc / P["Lmax"]
        Lc += P["e_soc"] * s_eff * p(S) * room_c
        Ls += (P["e_solo"] * solo + P["theta"] * P["e_soc"] * s_eff) * p(S) * room_s
        # suffering: shocks, fading, shared relief, conflict, solo practice
        S = (S * (1 - P["fade"]) + P["shock"] * 0.1 - P["relief"] * min(P["gamma"], 1.0) * s_eff * S
             + P["conflict"] * s_eff + P["drain"] * max(0.0, 1 - P["gamma"]) * 2 * s_eff**2)
        if P["practice"] == "converter":
            cv += P["zeta"] * z * (1.0 - cv)
        else:
            S -= P["zeta"] * 3 * z * S
        S = max(S, 0.0)
    return V

GRID = np.round(np.arange(0, 1.01, 0.1), 2)

def best(P, z_grid=(0.0,)):
    return max((run(s, z, P), s, z) for s, z in itertools.product(GRID, z_grid) if s + z <= 1)

def with_(**kw):
    P = dict(BASE); P.update(kw); return P

if __name__ == "__main__":
    print("T1. Best social share by sociability gate and kind of company (no practice)")
    print(f"{'gamma':>6} | {'close, chosen':>22} | {'not close / obligatory':>24} | solo-only V")
    for gam in [0.3, 0.6, 1.0, 1.3]:
        a = best(with_(gamma=gam)); b = best(with_(gamma=gam, amp=1.0, aut=0.3, bundle=0.0, relief=0.05))
        solo = run(0, 0, with_(gamma=gam))
        print(f"{gam:>6} | sigma*={a[1]:.1f} V={a[0]:7.1f} | sigma*={b[1]:.1f} V={b[0]:7.1f}     | {solo:7.1f}")

    print("\nT2. Which mechanism drives the social advantage? (gamma=1, close & chosen)")
    full = best(BASE); solo = run(0, 0, BASE)
    print(f"  all mechanisms on   sigma*={full[1]:.1f}  gain over solo={full[0]-solo:6.1f}")
    off = {"amp": dict(amp=1.0), "bundle": dict(bundle=0.0), "renew": dict(a_soc=0.5),
           "learn": dict(e_soc=0.02), "transmit": dict(theta=0.0), "relief": dict(relief=0.0)}
    for k, kw in off.items():
        r = best(with_(**kw)); s0 = run(0, 0, with_(**kw))
        print(f"  without {k:9s}   sigma*={r[1]:.1f}  gain over solo={r[0]-s0:6.1f}")
    only = {"level only (amp+bundle)": dict(a_soc=0.5, e_soc=0.02, theta=0.0, relief=0.0),
            "capacity only (renew+learn+transmit)": dict(amp=1.0, bundle=0.0, relief=0.0),
            "baseline only (relief)": dict(amp=1.0, bundle=0.0, a_soc=0.5, e_soc=0.02, theta=0.0),
            "additive only, no synergy (bundle=0, amp=1)": dict(amp=1.0, bundle=0.0)}
    for k, kw in only.items():
        r = best(with_(**kw)); s0 = run(0, 0, with_(**kw))
        print(f"  {k:44s} sigma*={r[1]:.1f}  gain={r[0]-s0:6.1f}")

    print("\nT3. 'Solitary is good but not optimal' across people (gate gamma varies)")
    rng = np.random.default_rng(0)
    gams = np.exp(rng.normal(np.log(0.8), 0.6, 200))
    for label, kw in [("all mechanisms", {}), ("no capacity mechanisms", dict(a_soc=0.5, e_soc=0.02, theta=0.0)),
                      ("not-close company only", dict(amp=1.0, aut=0.3, bundle=0.0, relief=0.05))]:
        sig = np.array([best(with_(gamma=gm, **kw))[1] for gm in gams])
        print(f"  {label:24s} some social optimal for {np.mean(sig > 0):5.1%};  median sigma*={np.median(sig):.1f};  "
              f"range {sig.min():.1f}-{sig.max():.1f}")

    print("\nT4. Self as converter vs small additive lever (practice share z also chosen)")
    for mode in ["converter", "additive"]:
        r = best(with_(practice=mode), z_grid=GRID)
        print(f"  {mode:9s}: best social={r[1]:.1f} practice={r[2]:.1f} V={r[0]:7.1f}")

    print("\nT5. Sensitivity: how big is shared relief vs the level/capacity effects? (gamma=1)")
    for rel in [0.0, 0.05, 0.15]:
        for amp, bun in [(1.0, 0.0), (1.3, 0.3), (1.6, 0.6)]:
            r = best(with_(relief=rel, amp=amp, bundle=bun)); s0 = run(0, 0, with_(relief=rel, amp=amp, bundle=bun))
            print(f"  relief={rel:<5} amp={amp:<4} bundle={bun:<4} sigma*={r[1]:.1f} gain={r[0]-s0:6.1f}")
