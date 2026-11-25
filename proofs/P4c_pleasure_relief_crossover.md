# P4c. Pleasure as relief: the savoring vs clean-relief crossover

## Setup

Following `model/hx_pleasure_relief.py`. State: suffering $S$, liking stock $L$, capacity $c \in (0,1]$, and one go-to pleasure source with liking $\ell_s > 0$ and freshness $h \in [0,1]$. Numbing is $g(S)$, decreasing, with $g(0) = 1$. In each period one action is taken:

| Action | Effect on $S$ this period | Other effects |
| --- | --- | --- |
| Clean relief | $S \leftarrow S - \rho_c S$ | none |
| Savor | $S \leftarrow S - \rho_p\, q\, S$, with $q = g(S)\,c\,\ell_s\,h$ | adds $q$ to pleasure; $h \leftarrow (1-\alpha)h$; builds liking $L \mathrel{+}= D_s\,p(S)\,c$ |
| Grab | same relief and pleasure as savoring | $\ell_s$ depletes, $c$ falls, urge rises; no liking built |
| Expand | none | $L \mathrel{+}= \Delta\,p(S)\,c$ |

All actions are followed by fading $S \leftarrow (1-d)S$ and capacity recovery.

Parameters in the script: $\rho_c = 0.25$, $\rho_p = 0.4$, $g(S) = e^{-kS}$ with $k = 0.3$.

## Assumptions

- (R1) The crossover compares **only the suffering removed in one period**, from the same state, by one unit of effort spent on clean relief vs on savoring.
- (R2) For the headline number: a fresh source ($h = 1$), full capacity ($c = 1$), unit liking ($\ell_s = 1$).

## Statement

**Crossover.** From state $(S, c, \ell_s, h)$ with $S > 0$, savoring removes more suffering than clean relief iff
$$
g(S)\,c\,\ell_s\,h > \frac{\rho_c}{\rho_p}.
$$
With a fresh source, $c = \ell_s = 1$, and exponential numbing, this is
$$
S < S_\times = \frac{\ln(\rho_p/\rho_c)}{k} = \frac{\ln 1.6}{0.3} \approx 1.57.
$$
If $\rho_p \le \rho_c$ (and $g c\ell_s h \le 1$), clean relief always removes at least as much. More generally, for any strictly decreasing $g$ with $g(0) = 1$ and $\rho_c < \rho_p$, the fresh-source crossover is the unique $S_\times = g^{-1}(\rho_c/\rho_p)$, with savoring winning below it and clean relief above.

## Proof

Removed by clean relief: $\rho_c S$. Removed by savoring: $\rho_p\,q\,S = \rho_p\,g(S)\,c\,\ell_s\,h\,S$. For $S > 0$, divide both by $\rho_p S > 0$:
$$
\rho_p\,g(S)\,c\,\ell_s\,h\,S > \rho_c S \iff g(S)\,c\,\ell_s\,h > \rho_c/\rho_p.
$$
With $c = \ell_s = h = 1$ and $g = e^{-kS}$: $e^{-kS} > \rho_c/\rho_p \iff -kS > \ln(\rho_c/\rho_p) \iff S < \ln(\rho_p/\rho_c)/k$. Numerically, $\ln(0.4/0.25) = \ln 1.6 = 0.470$, and $0.470/0.3 = 1.567$.

For general strictly decreasing $g$ with $g(0) = 1 > \rho_c/\rho_p$: the set $\{S : g(S) > \rho_c/\rho_p\}$ is an interval $[0, S_\times)$, where $S_\times = g^{-1}(\rho_c/\rho_p)$ if $g$ reaches that level, and $\infty$ otherwise. If $\rho_p \le \rho_c$, then $\rho_c/\rho_p \ge 1 \ge g c \ell_s h$, so savoring never removes strictly more. $\square$

**Consequences that follow directly:**

- The crossover moves to lower $S$ as the source goes stale ($h \downarrow$), as capacity falls ($c \downarrow$, e.g. after numbing), or as liking depletes ($\ell_s \downarrow$, e.g. after grabbing). For a source with $c\ell_sh = \kappa_s$, $S_\times = \ln(\kappa_s\rho_p/\rho_c)/k$, and savoring never wins once $\kappa_s \le \rho_c/\rho_p = 0.625$. This is the formal content of "ignoring freshness is the biggest loss."
- At high distress, numbing ($g \to 0$) makes pleasure weak relief exactly when relief matters most.

## Numerical check

- Crossover: exact. The three-phase policy that uses it ("clean relief above $S = 1$, savor below when the source is fresh ($h > 0.9$), otherwise expand") gives $V = 263.1$ ($S_0 = 8$) and $324.4$ ($S_0 = 3$) when run through `sim()` in `model/hx_pleasure_relief.py`. That matches the page (263, 324). It is reproduced by `model/hx_pleasure_relief_phased.py` (output in `results/hx_pleasure_relief_phased.txt`). The `savor_liking` policy in the original script savors at high distress too and scores 224.7 / 314.5.
- Other rows match `results/hx_pleasure_relief.txt`: clean then expand 254.1 / 315.2; savor only 28.6 / 282.4; grab −180.0 (100 uses) / 196.2; nothing −191.6 / −55.7.
- The "what makes grabbing bad" ablation (−103, −106, −114, −180) is reproduced exactly by `model/hx_pleasure_relief_phased.py` (−103.1, −105.5, −114.2, −180.0). The original script's sensitivity sweep differs (−113.2 with no urge growth) because it holds the other wanting features at their defaults.

## Status / limits

- **Proved:** the one-period relief crossover.
- **Simulated:** the three-phase policy beating clean-then-expand by about 3–4% (263 vs 254; 324 vs 315).
- **Open:** that the three-phase policy is *optimal*. That needs the full dynamic program over $(S, L, c, h, \ell_s, w)$. The crossover ignores savoring's direct pleasure $q$ and its liking-building, both of which favor savoring, so the best switch point in a full policy need not equal $S_\times$. The simulation's best switch ($S = 1$, on a coarse grid) is below $S_\times \approx 1.57$, which is consistent with savoring at $S \in (1, 1.57)$ using up freshness that is worth more later. That reading is unproved.
