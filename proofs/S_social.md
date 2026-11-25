# S. Social axis: compersion threshold, widening the circle, taste transmission

## Setup

Experienced value for person $i$ (`model/hx_social.py`):
$$
U_i = P_i - \lambda S_i + \kappa_i\sum_{j\ne i}P_j - \lambda\,\eta_i\sum_{j\ne i}S_j - a_i,
$$
where $\kappa_i$ is mudita (others' pleasure counting as one's own; $\kappa < 0$ is envy), $\eta_i$ is empathic distress, $a_i \ge 0$ is appraisal-only jealousy (comparison, borrowed scarcity), and $\lambda > 0$ is the suffering weight.

## Assumptions

- (Q1) Effects are additive as in $U_i$ and evaluated in expectation (risk-neutral).
- (Q2) For S1's "no amount of compersion" claim: $\kappa \le 1$ (others' pleasure can't count for more than one's own).
- (Q3) For S2: $\kappa > 0$, and each added person contributes their pleasure $G$ and suffering $S$ independently of the others (no attention limit), as in the script's ladder.

---

## S1. Compersion threshold

**Setup.** A partner gains pleasure $G > 0$ from someone else. You lose real rival inputs $R \ge 0$ (time, attention, possibly a bundle bonus), the risk of losing the relationship rises by $\Delta q \ge 0$ with loss cost $L \ge 0$, and appraisal costs $a \ge 0$.

**Statement.** Your net change is
$$
N = \kappa G - R - \Delta q\,L - a,
$$
so $N > 0$ iff $\kappa > \kappa^* = (R + \Delta q\,L + a)/G$. Under (Q2), if $G \le R + \Delta q\,L$ then $N \le 0$ for every admissible $\kappa$, so no amount of compersion makes it net positive. Training $\kappa$ or removing $a$ lowers only the $a$ part of the requirement; $R$ and $\Delta q$ are untouched by feelings work.

**Proof.** From $U$ with the partner's $\Delta P = G$, your own losses $R$, expected loss $\Delta q\,L$ and appraisal $a$: $\Delta U = \kappa G - R - \Delta qL - a$. Divide $N > 0$ by $G > 0$ to get $\kappa^*$. If $G \le R + \Delta qL$, then with $\kappa \le 1$ and $a \ge 0$: $\kappa G \le G \le R + \Delta qL \le R + \Delta qL + a$, so $N \le 0$. $\kappa^*$ depends on $a$ additively, with coefficient $1/G$, and on $R$ and $\Delta q$ separately. $\square$

**Worked example (script parameters).** $G = 2$, $k = 3$ strands, bonus $b = 0.3$, diverted share $r = 0.2$, $\lambda = 2$, grief weight $W = 6$, bundle share $s_b = 0.5$.
- Unprotected slot: the whole bonus is lost, so $R = rk + kb = 0.6 + 0.9 = 1.5$.
- Protected slot: only the linear part is lost, so $R = rk(1+b) = 0.6 + 0.18 = 0.78$.
- Loss cost: $L = k(1+b) + \lambda W s_b^2 = 3.9 + 3 = 6.9$.

| Case | $R$ | $\Delta q L$ | $a$ | $\kappa^*$ |
| --- | --- | --- | --- | --- |
| Unprotected, $\Delta q = 0.02$ | 1.50 | 0.138 | 0 | $1.638/2 = 0.82$ |
| Protected, $\Delta q = 0.02$ | 0.78 | 0.138 | 0 | $0.918/2 = 0.46$ |
| Protected, $\Delta q = 0.005$ | 0.78 | 0.0345 | 0 | $0.8145/2 = 0.41$ |
| Same, appraisal $a = 0.5$ | 0.78 | 0.0345 | 0.5 | $1.3145/2 = 0.66$ |

These match the page and `results/hx_social.txt`. The added risk also raises the P6 bundle threshold $b^* = \lambda q(k-1)/k$, which is linear in $q$: 0.067, 0.093, 0.133 at $q = 0.05, 0.07, 0.10$ (same output).

---

## S2. Widening the circle: sign condition

**Statement.** Under (Q3), each added person changes $U$ by $\kappa G - \lambda\eta S$. For $S > 0$, this is positive iff
$$
\frac{\eta}{\kappa} < \frac{G}{\lambda S}.
$$
Cumulative value along a ladder of rungs with $(G_r, S_r)$ and $m_r$ people per rung is $\sum_r m_r(\kappa G_r - \lambda\eta S_r)$. It rises at rung $r$ iff that rung meets the condition.

**Proof.** The added person contributes $\kappa G$ (mudita term) and $-\lambda\eta S$ (empathic distress term) to $U$. Dividing $\kappa G > \lambda\eta S$ by $\kappa\lambda S > 0$ gives the condition. Cumulative sums add the per-rung terms, so the running total increases exactly at rungs where the term is positive. $\square$

**Check (script ladder, $\kappa = 0.6$, $\lambda = 2$, 5 people per rung).** Rungs $(G, S)$: self-adjacent (1, 0.2), benefactor (1, 0.25), friend (1, 0.3), neutral (0.8, 0.35), difficult (0.7, 0.4), all (0.6, 0.5). The thresholds $G/(\lambda S)$ are 2.5, 2.0, 1.67, 1.14, 0.875, 0.6.
- $\eta/\kappa = 1$: the condition fails at "difficult" ($1 > 0.875$) and "all" ($1 > 0.6$). Increments $+1.8, +1.5, +1.2, +0.3, -0.3, -1.2$ give the cumulative 1.8, 3.3, 4.5, 4.8, 4.5, 3.3.
- $\eta/\kappa = 0.3$: the condition holds at every rung (0.3 < 0.6), so the total rises at every rung to 11.7.

Both match `results/hx_social.txt` (2b) and the page.

**Breadth of people (2a).** With fixed attention $A = 1$ split over $m$ people, vicarious pleasure follows P2's curve exactly ($0, 0.333, 0.5, 0.667, 0.818, \dots$), so it has the same bounded, diminishing returns. Expected squared grief share is $q(1-q)/m + q^2$ (P5b): 0.050 at $m = 1$ and 0.012 at $m = 5$. Both are in `results/hx_social.txt`.

---

## S3. Taste transmission: what the measured ratio means

**Setup.** At breakup time $T$, B's learned liking for a taste is $x$, of which a share $\theta$ is internalized (kept) and $1-\theta$ is dependent (unwinds afterwards). After the breakup, the dependent part is multiplied by $D(t) \in [0,1]$ (in the script, $D = 0.7^{t-T+1}$), and the whole taste is suppressed by a grief factor $m(t) \in (0,1]$ (0.3 for 15 periods, then 1). Measured liking is $\bigl[\theta x + (1-\theta)D(t)x\bigr]m(t)$.

**Statement.** The measured ratio (after/before) is
$$
\hat\theta(t) = m(t)\bigl[\theta + (1-\theta)D(t)\bigr] = m(t)D(t) + m(t)\bigl(1-D(t)\bigr)\theta.
$$
It equals $\theta$ for every $\theta$ iff $m(t) = 1$ and $D(t) = 0$. Otherwise it is an affine function of $\theta$ with slope $m(1-D) < 1$, mapping $[0,1]$ onto $[mD,\, m]$. Early tests therefore **compress** the true range: a fully dependent taste ($\theta = 0$) reads $mD > 0$ (false positive, inflated by dependent liking that hasn't faded), and a fully internalized taste ($\theta = 1$) reads $m < 1$ (false negative, deflated by grief).

**Proof.** Divide the measured liking by $x$ and expand. Setting $\hat\theta(t) = \theta$ for all $\theta \in [0,1]$ requires intercept $mD = 0$ and slope $m(1-D) = 1$; with $m > 0$ the first gives $D = 0$, and then the second gives $m = 1$. Conversely, $m = 1$ and $D = 0$ give $\hat\theta = \theta$. The endpoints of the image are $\theta = 0 \mapsto mD$ and $\theta = 1 \mapsto m$. $\square$

**Correction to the page's wording:** "compressed toward the middle" is loose. The early reading is compressed (slope $m(1-D)$), but it is centered on $m(1+D)/2$, not on 0.5. With strong grief suppression ($m = 0.3$) the whole range is pulled *down*: two periods after, it is $[0.10, 0.30]$.

**Check.** Two periods after the breakup the script has applied the dependent decay three times ($t = T, T+1, T+2$), so $D = 0.7^3 = 0.343$ and $m = 0.3$. Predicted $\hat\theta$ for $\theta = 0, 0.3, 0.7, 1$: $0.103, 0.162, 0.240, 0.300$. `results/hx_social.txt` (part 3) gives $0.099, 0.156, 0.232, 0.289$ relative to a pre-breakup level of 0.964, i.e. ratios $0.103, 0.162, 0.241, 0.300$. Late ($t = T+40$, $m = 1$, $D = 0.7^{41} \approx 0$): ratio $= \theta$ (0.00, 0.30, 0.70, 1.00). All match.

---

## Status / limits

- **Proved:** S1 threshold and its corollary (given $\kappa \le 1$, which the page leaves implicit); S2 sign condition; S3 ratio formula. **Simulated:** S4 (many people) and S5 (pairs), not treated here.
- S2 ignores limited attention in the ladder (the script's "attention unbounded"). With attention split as in 2a, each person's vicarious term shrinks, but the sign condition per person is unchanged if the suffering term is scaled by the same attention share. The script doesn't model that scaling.
- The grief floor with correlated losses (S2's "toward a floor set by correlated losses") is not modeled; see the limits in P5/P6.
- S3 assumes internalized and dependent liking are learned in fixed proportion $\theta$, as in the script. In the script, C's dependence on B is tracked separately and isn't analyzed here.
