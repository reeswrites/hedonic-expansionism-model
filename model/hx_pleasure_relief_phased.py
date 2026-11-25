"""Reproduces two P4c results that were first run inline:
1. The three-phase policy (clean relief at high distress, savoring at moderate, expand at low).
2. The ablation of what makes wanting-driven grabbing costly.
Uses the model in hx_pleasure_relief.py. Run from model/.
"""
import itertools
import hx_pleasure_relief as m

def phased(s1):
    def pol(S, h, w, thr):
        if S > s1:
            return "clean"
        if S > thr:
            return "savor" if h > 0.6 else "clean"
        return "savor" if h > 0.9 else "expand"
    return pol

if __name__ == "__main__":
    for S0 in [8.0, 3.0]:
        best = max(((m.sim(S0, phased(s1), th)[0], s1, th, m.sim(S0, phased(s1), th)[1])
                    for s1, th in itertools.product([0.5, 1, 1.5, 2, 3, 4, 99], m.THRS) if s1 >= th),
                   key=lambda x: x[0])
        clean = max(m.sim(S0, m.clean_first, th)[0] for th in m.THRS)
        print(f"S0={S0}: three-phase best V={best[0]:.1f} (clean above S={best[1]}, savor down to {best[2]}) "
              f"{best[3]} | clean-first {clean:.1f}")

    print("\nGrab with each wanting feature switched on in turn (S0=8, best threshold)")
    orig = (m.W_UP, m.BETA, m.MU_G)
    for label, wu, beta, mug in [("ignores freshness only", 0, 0, 0), ("+ liking depletes", 0, 0.05, 0),
                                  ("+ attention narrows", 0, 0.05, 0.02), ("+ urge grows (full)", 0.3, 0.05, 0.02)]:
        m.W_UP, m.BETA, m.MU_G = wu, beta, mug
        V, cnt = max((m.sim(8, m.grab_wanting, th) for th in m.THRS), key=lambda x: x[0])
        print(f"  {label:26s} V={V:7.1f} uses={cnt['grab']}")
    m.W_UP, m.BETA, m.MU_G = orig
