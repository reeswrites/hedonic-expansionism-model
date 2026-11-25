# P1. Without expansion: what happens to a fixed set of sources

## Setup

A source $i$ has liking $\ell_i \ge 0$, freshness $h_i \in [0,1]$ (1 = not habituated), and gets a constant share $u \in [0,1]$ of each period's time. Per-period pleasure from the source is

$$
P_t = \ell_t\, h_t\, u .
$$

(With $n$ sources and the multiplier $g(S)$ from the hub model, total pleasure is $g(S)\sum_i \ell_i h_i u_i$; P1 takes $S = 0$, so $g = 1$, and treats each source separately.)

**Habituation (all types):**

$$
h' = h - \alpha u h + \rho (1-h)(1-u), \qquad \alpha, \rho \in (0,1].
$$

**Liking dynamics by type:**

| Type | Update |
| --- | --- |
| Renewing | $\ell' = \ell$ |
| Depleting | $\ell' = \ell(1-\beta u)$, $\beta \in (0,1]$ |
| Skill-slope | $\ell' = \ell + \gamma u (c - \ell)$, $\gamma \in (0,1]$, cap $c > 0$ |

**Slow-recovery revision (Nov 24).** The depleting type is replaced by a second, slow freshness $m \in [0,1]$ ("novelty"):

$$
m' = m - \beta u\, m + \varepsilon (1-u)(1-m), \qquad 0 \le \varepsilon \ll \rho,
$$

and pleasure becomes $P_t = \ell\, h_t\, m_t\, u$ with $\ell$ constant.

## Assumptions

- (B1) $u$ is constant over time (no expansion, no reallocation).
- (B2) $\alpha, \rho, \beta, \gamma \in (0,1]$ and $\varepsilon \in [0,1]$, so every update coefficient below lies in $[0,1]$.
- (B3) Initial values $h_0, m_0 \in [0,1]$, $\ell_0 \ge 0$; for skill-slope, $\ell_0 \le c$ (for "rises"; the case $\ell_0 > c$ is noted below).

## Statement

For a fixed share $u \in (0,1)$:

1. **Depleting:** $\ell_t = \ell_0 (1-\beta u)^t \to 0$ geometrically, so $P_t \to 0$.
2. **Renewing:** $h_t \to h^*(u) = \dfrac{\rho(1-u)}{\alpha u + \rho(1-u)} \in (0,1)$ geometrically, so $P_t \to \ell\, h^*(u)\, u > 0$. At $u = 1$, $h^* = 0$.
3. **Skill-slope:** $\ell_t \to c$ monotonically, so $P_t \to c\, h^*(u)\, u$. Long-run pleasure exceeds the starting pleasure $\ell_0 h_0 u$ iff $c\, h^*(u) > \ell_0 h_0$; with a fresh start ($h_0 = 1$), iff $c\, h^* > \ell_0$.
4. **Slow recovery:** $m_t \to m^*(u) = \dfrac{\varepsilon(1-u)}{\beta u + \varepsilon(1-u)}$, which is $> 0$ whenever $\varepsilon > 0$ and $u < 1$, and $P_t \to \ell\, h^*(u)\, m^*(u)\, u$. Permanent loss ($m^* = 0$) happens only if $\varepsilon = 0$ or $u = 1$.

A note on the page's headline. "Pleasure only declines if your sources deplete" is loose: a renewing source started fresh also declines, from $\ell u$ to $\ell h^* u$. The precise claim is that **pleasure goes to zero only for depleting sources**. Renewing sources settle at a positive level, and skill-slope sources rise if and only if $c\,h^* > \ell_0 h_0$.

## Proof

**Lemma (affine recurrence).** Let $x' = a x + b$ with $0 \le a < 1$. Then $x_t = x^* + a^t (x_0 - x^*)$ with $x^* = b/(1-a)$, so $x_t \to x^*$ geometrically and monotonically. If $x_0 \in [0,1]$, $b \ge 0$ and $a + b \le 1$, then $x_t \in [0,1]$ for all $t$.

*Proof.* $x' - x^* = a x + b - b/(1-a) = a x - a b/(1-a) = a(x - x^*)$. Iterating gives the formula, and since $a \ge 0$ the sign of $x_t - x^*$ never changes, so convergence is monotone. For the bounds: $x' = a x + b \ge 0$, and $x' \le a + b \le 1$. $\square$

**1. Depleting.** $\ell' = (1-\beta u)\ell$ with $0 \le 1-\beta u < 1$ for $u > 0$, so $\ell_t = \ell_0(1-\beta u)^t \to 0$. Since $h_t \le 1$ (Lemma), $0 \le P_t = \ell_t h_t u \le \ell_t u \to 0$.

**2. Renewing.** Expand the habituation update:

$$
h' = h - \alpha u h + \rho(1-u) - \rho(1-u) h = \underbrace{\bigl(1 - \alpha u - \rho(1-u)\bigr)}_{a}\, h + \underbrace{\rho(1-u)}_{b}.
$$

Since $\alpha u + \rho(1-u)$ is a convex combination of $\alpha$ and $\rho$, it lies in $(0, \max(\alpha,\rho)] \subseteq (0,1]$ for $u \in [0,1]$. So $0 \le a < 1$, $b \ge 0$, and $a + b = 1 - \alpha u \le 1$. By the Lemma,

$$
h_t \to h^* = \frac{b}{1-a} = \frac{\rho(1-u)}{\alpha u + \rho(1-u)}.
$$

For $u \in (0,1)$ numerator and denominator are positive and the denominator is larger by $\alpha u > 0$, so $h^* \in (0,1)$. At $u = 1$, $b = 0$ and $h^* = 0$. Then $P_t = \ell h_t u \to \ell h^* u$.

**3. Skill-slope.** Subtract the update from $c$:

$$
c - \ell' = c - \ell - \gamma u (c - \ell) = (1-\gamma u)(c - \ell),
$$

so $c - \ell_t = (1-\gamma u)^t (c - \ell_0) \to 0$, monotonically, since $0 \le 1 - \gamma u < 1$. If $\ell_0 \le c$ then $\ell_t \uparrow c$; if $\ell_0 > c$ then $\ell_t \downarrow c$. Both $\ell_t$ and $h_t$ converge, so their product does: $P_t \to c\, h^* u$. Comparing with $P_0 = \ell_0 h_0 u$ gives the condition in the Statement.

**4. Slow recovery.** The $m$-update has the same form as the $h$-update with $(\alpha, \rho)$ replaced by $(\beta, \varepsilon)$:

$$
m' = \bigl(1 - \beta u - \varepsilon(1-u)\bigr) m + \varepsilon (1-u).
$$

For $u > 0$ or $\varepsilon > 0$, the coefficient $a_m = 1 - \beta u - \varepsilon(1-u)$ lies in $[0,1)$ by the same convex-combination argument, and $a_m + b_m = 1 - \beta u \le 1$. By the Lemma, $m_t \to m^* = \varepsilon(1-u)/(\beta u + \varepsilon(1-u))$. This is positive iff $\varepsilon > 0$ and $u < 1$. The $h$ and $m$ recurrences don't depend on each other, so $P_t = \ell h_t m_t u \to \ell h^* m^* u$. $\square$

**Corollaries used on the page.**

- $m^*$ is strictly decreasing in $u$: write $m^* = 1/(1 + \beta u / (\varepsilon(1-u)))$, and $u/(1-u)$ is increasing. Heavy use keeps a novelty-based pleasure near its floor. Spreading time over more sources ($u = T/n$) raises $m^*$, which is the "breadth buys slow recovery" point.
- The convergence rate of $m$ is $a_m = 1 - \beta u - \varepsilon(1-u)$, close to 1 when $\beta u$ and $\varepsilon$ are small, so recovery is slow, as intended.
- $\varepsilon = 0$ gives $m' = (1-\beta u)m$, exactly the old depleting type. The revision contains the old model as a special case.

## Numerical check

- `model/hx_model.py` → `results/hx_model.txt`, "P1 fixed liking set" ($n = 5$, $u = 0.2$, $\alpha = 0.6$, $\rho = 0.3$, $\beta = 0.02$, $\gamma = 0.01$, $c = 3$). Closed forms: $h^*(0.2) = 0.24/0.36 = 0.667$. Depleting at $t = 200$: $0.996^{199} \cdot 0.667 = 0.450 \cdot 0.667 = 0.300$ (output 0.300). Renewing: 0.667 (output 0.667). Skill at $t = 200$: $\ell = 3 - 2\cdot 0.998^{199} = 1.657$, times 0.667 gives 1.105 (output 1.105). The skill-slope limit is $c h^* = 2.0 > \ell_0 = 1$, so the sharpening condition holds here.
- Slow-recovery fixed point: no repo script. An ad hoc iteration ($\beta = 0.02$, $\varepsilon = 0.002$, $u = 0.2$, 20,000 steps) gives $m = 0.28571$, matching $m^* = 0.0016/0.0056 = 0.28571$.

## Status / limits

- **Proved** for constant $u$. With a time-varying $u_t$ the recurrences become non-autonomous; convergence still holds if $u_t$ converges, but that isn't shown here.
- The skill-slope condition $c\,h^* > \ell_0 h_0$ is the page's "sharpening", stated with $h_0$ made explicit.
- The slow-recovery revision has no simulation in the repo. Whether $\varepsilon > 0$ for a given pleasure (and whether tolerance fully reverses) is empirical.
- P1 says nothing about which $u$ is optimal; P2 covers the even split, and P7 covers choice.
