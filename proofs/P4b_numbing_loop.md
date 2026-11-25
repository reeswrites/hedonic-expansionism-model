# P4b. Numbing relief: the loop condition, its long-run cost, and the opponent-process version

## Setup

Following `model/hx_relief_types2.py` and `model/hx_updates.py` (part 3). State: suffering $S \ge 0$, liking stock $L > 0$, liking capacity $c \in (0,1]$. Pleasure is $g(S)\,c\,L$ with $g$ decreasing, $g(0) = 1$; value is $V = \sum_t \delta^t (g(S_t)c_tL_t - \lambda S_t)$.

A **numbing dose** in period $t$:
- cuts suffering by a fraction $\rho_n \in (0,1)$: $S \leftarrow (1-\rho_n)S$;
- cuts capacity: $c \leftarrow (1-\mu)c$, with $\mu \in [0,1)$;
- adds a rebound $r_t \ge 0$ to suffering at the start of period $t+1$;
- builds no liking.

Every period, suffering fades, $S \leftarrow (1-d)S$ with $d \in [0,1)$, and capacity recovers, $c \leftarrow c + \psi(1-c)$ with $\psi \in (0,1]$.

**Habitual numbing:** dose whenever $S_t > \theta$ (a trigger level $\theta > 0$).

Notation: $a = (1-\rho_n)(1-d) \in (0,1)$ and $C = 1 - a = 1 - (1-\rho_n)(1-d)$. (The page writes the opponent-process condition as $\theta c$; this $c$ is $C$, not capacity.)

**Constant rebound:** $r_t \equiv r$.

**Opponent-process rebound (Solomon):** $r_t = r_0 A_t$, where the counter-reaction $A$ evolves as
$$A_{t} = (1-\epsilon)A_{t-1} + g_A \cdot \mathbf{1}[\text{dose at } t], \qquad A_0 \ge 0,$$
with $r_0 > 0$, growth $g_A > 0$ and decay $\epsilon \in (0,1]$. (The page calls the growth $g$; renamed $g_A$ to avoid a clash with numbing $g(S)$.) The rebound added at $t+1$ is $r_0 A_t$, using $A$ after the period-$t$ update, as in `sim3`.

## Assumptions

- (N1) While the loop runs, the only changes to $S$ are the dose, fading and the rebound (no clean relief, no shocks). Shocks are allowed in the numerical checks; they can start a loop but are not needed for one to persist.
- (N2) In the opponent-process part, $A_0 \le g_A/\epsilon$ (true for $A_0 = 0$).

## Statement

**Theorem 1 (constant-rebound loop).** Let $S^* = r/C$. If habitual numbing starts with $S_0 > \theta$, then it never stops iff $S^* \ge \theta$, i.e.
$$
r \ge \theta\,C = \theta\bigl(1-(1-\rho_n)(1-d)\bigr).
$$
If $S^* < \theta$, it stops after finitely many doses.

**Proposition 2 (long-run cost inside the loop).** While the loop runs, $S_t \to S^* = r/C$, $c_t \to c^* = \dfrac{\psi}{1-(1-\mu)(1-\psi)}$ (which is $< 1$ iff $\mu > 0$), and $L$ is constant. So per-period value tends to
$$
g(S^*)\,c^*\,L - \lambda S^* \;<\; L \quad (\text{when } r > 0 \text{ or } \mu > 0).
$$
The right side is the limit with no numbing and no expansion when $d > 0$ ($S \to 0$, $c \to 1$). If not numbing also allows expansion, as in the script's "nothing" baseline, the comparison is even less favourable to the loop.

**Theorem 3 (opponent-process lock-in).** Under (N2):
1. *Necessity.* If $r_0 g_A/\epsilon < \theta C$, every run of habitual numbing ends in finite time.
2. *Sufficiency once built up.* If at some dose period $t_1$ in a run we have $S_{t_1} > \theta$ and $r_0 A_{t_1} \ge \theta C$, the run never ends.
3. *Reachability.* During an unbroken run, $A_t \uparrow g_A/\epsilon$. So condition 2 is eventually met in a long enough run iff $r_0 g_A/\epsilon > \theta C$.

The page's "loop condition becomes $r_0 g/\epsilon \ge \theta c$" is the asymptotic version. It is necessary (part 1) and, with strict inequality, sufficient once the counter-reaction has built up (parts 2–3). Whether it does build up depends on how long early runs last, e.g. whether recurring stressors re-trigger before $A$ decays.

**Proposition 4 (spacing rule).** Suppose doses are taken exactly every $m \ge 1$ periods. Then the post-dose counter-reaction converges (monotonically from $A_0 = 0$) to
$$A^*(m) = \frac{g_A}{1-(1-\epsilon)^m},$$
and the steady per-dose rebound stays below the self-sustaining level, $r_0A^*(m) < \theta C$, iff
$$
m > \frac{\ln\bigl(1 - r_0 g_A/(\theta C)\bigr)}{\ln(1-\epsilon)}.
$$
A finite safe spacing exists iff $r_0 g_A < \theta C$, i.e. iff a single dose from rest can't re-trigger on its own. The minimum safe spacing is the smallest integer $m \ge 1$ strictly above the bound. The page's $\lceil\cdot\rceil$ form gives this except when the bound is an exact integer, where it gives the boundary value $r_0A^* = \theta C$.

## Proofs

**Theorem 1.** While the loop runs, each period applies the dose, then fading, and the next period starts with the rebound added:
$$S_{t+1} = (1-d)(1-\rho_n)S_t + r = aS_t + r.$$
This map is increasing in $S_t$ (since $a > 0$) with fixed point $S^* = r/(1-a) = r/C$.

($\Leftarrow$) If $S^* \ge \theta$ and $S_t > \theta$, then $S_{t+1} = aS_t + r > a\theta + r \ge a\theta + C\theta = \theta$, using $r = CS^* \ge C\theta$. By induction $S_t > \theta$ for every $t$, so the dose is always triggered.

($\Rightarrow$, contrapositive) If $S^* < \theta$: as long as the loop runs, P1's Lemma gives $S_t = S^* + a^t(S_0 - S^*) \to S^* < \theta$, so some finite $t$ has $S_t \le \theta$ and the loop stops. $\square$

*Check:* $\theta = 0.5$, $\rho_n = 0.5$, $d = 0.03$ give $C = 1 - 0.5 \cdot 0.97 = 0.515$ and $\theta C = 0.2575$. Rebounds 0.3 and 1.0 both exceed it.

**Proposition 2.** $S_t \to S^*$ by Theorem 1's recurrence. Capacity per looped period is $c' = (1-\mu)c + \psi\bigl(1-(1-\mu)c\bigr) = (1-\psi)(1-\mu)c + \psi$, which is affine with coefficient $(1-\psi)(1-\mu) \in [0,1)$, so (P1's Lemma) $c_t \to c^* = \psi/\bigl(1-(1-\psi)(1-\mu)\bigr)$. Then
$$c^* < 1 \iff \psi < 1 - (1-\psi)(1-\mu) \iff (1-\psi)(1-\mu) < 1-\psi \iff \mu > 0 \quad (\psi < 1).$$
$L$ is unchanged because a dose builds no liking. The flow converges to $g(S^*)c^*L - \lambda S^*$. Since $g \le 1$ and $c^* \le 1$, this is at most $L - \lambda S^*$, and it is strictly below $L$ when $S^* > 0$ (i.e. $r > 0$) or when $c^* < 1$ with $g(S^*) > 0$. With no numbing and $d > 0$, $S_t = (1-d)^tS_0 \to 0$ and $c \to 1$, so the flow tends to $L$. $\square$

As the page says, whether the loop is worse than doing nothing *in total* depends on how fast suffering would fade on its own: numbing helps early, and the loop's cost recurs forever after.

**Theorem 3.**
*Bound on $A$.* With $A_0 \le g_A/\epsilon$: if $A_{t-1} \le g_A/\epsilon$ then $A_t \le (1-\epsilon)g_A/\epsilon + g_A = g_A/\epsilon$. In fact, if $A_0 < g_A/\epsilon$ then $A_t < g_A/\epsilon$ strictly, and if $A_0 = 0$ then $A_t < g_A/\epsilon$ for all $t$. So $r_t \le \bar r := r_0 g_A/\epsilon$.

1. If $\bar r < \theta C$: during a run, $S_{t+1} = aS_t + r_t \le aS_t + \bar r$. By induction $S_t \le \tilde S_t$, where $\tilde S_{t+1} = a\tilde S_t + \bar r$ and $\tilde S_0 = S_0$ (the map $x \mapsto ax + \bar r$ is increasing). Since $\tilde S_t \to \bar r/C < \theta$, some finite $t$ has $S_t \le \theta$, and the run ends.
2. During a run, $A$ moves monotonically toward $g_A/\epsilon$ (P1's Lemma: $A_t - g_A/\epsilon = (1-\epsilon)(A_{t-1} - g_A/\epsilon)$). Under (N2), $A$ is nondecreasing during the run, so $r_t \ge r_0A_{t_1} \ge \theta C$ for all $t \ge t_1$ in the run. Then, as in Theorem 1, $S_t > \theta$ implies $S_{t+1} = aS_t + r_t > a\theta + \theta C = \theta$. By induction the run never ends.
3. In an unbroken run, $A_t \to g_A/\epsilon$, so $r_0A_t \to \bar r$. If $\bar r > \theta C$, then $r_0A_t \ge \theta C$ after finitely many doses, and part 2 applies provided the run lasts that long. If $\bar r \le \theta C$, then $r_0A_t < \theta C$ for all $t$ (strict bound above), so the condition in part 2 is never met. $\square$

*Boundary $\bar r = \theta C$:* not covered. $r_t \uparrow \theta C$ from below, and whether $S_t$ stays above $\theta$ depends on initial conditions.

**Proposition 4.** Between consecutive doses there are $m - 1$ dose-free periods. If $A$ is the post-dose value at one dose, the next post-dose value is $(1-\epsilon)^{m-1}$ (decay) $\times(1-\epsilon)$ (decay in the dose period) $\times A + g_A$, i.e.
$$A \mapsto (1-\epsilon)^m A + g_A.$$
This is affine with coefficient $(1-\epsilon)^m \in [0,1)$, so (P1's Lemma) the post-dose $A$ converges monotonically to $A^*(m) = g_A/(1-(1-\epsilon)^m)$, from below if $A_0 = 0$. The condition $r_0 A^*(m) < \theta C$ is equivalent to
$$1 - (1-\epsilon)^m > \frac{r_0 g_A}{\theta C} \iff (1-\epsilon)^m < 1 - \frac{r_0g_A}{\theta C}.$$
If $r_0 g_A \ge \theta C$ the right side is $\le 0$ and no $m$ works. (Indeed $A^*(m) \ge g_A$ for every $m$, so even the first dose's rebound reaches $r_0 g_A \ge \theta C$.) Otherwise, taking logs (both sides positive) and dividing by $\ln(1-\epsilon) < 0$, which flips the inequality, gives $m > \ln(1 - r_0g_A/\theta C)/\ln(1-\epsilon)$. For $\epsilon = 1$, $A^*(m) = g_A$ and every $m \ge 1$ is safe. $\square$

Why $r_0A^* < \theta C$ is the right notion of "safe": by Theorem 3(1) with $\bar r$ replaced by $r_0A^*(m)$, even a run of consecutive doses started from this counter-reaction level couldn't sustain itself.

## Numerical check

- Constant rebound, `model/hx_relief_types2.py`: calling its `sim(8, 0.5, 99, mu, reb, d, clean_ok=False)` (habitual, trigger 0.5) gives $-40.6$, $-106.5$ ($d = 0.03$) and $-37.5$, $-99.8$ ($d = 0.1$), all with 100 doses out of 100. That reproduces the page's habitual column ($-41$, $-107$, $-38$, $-100$) and agrees with Theorem 1 ($r = 0.3, 1.0 > 0.2575$, and $\theta C = 0.5(1 - 0.5\cdot 0.9) = 0.275$ at $d = 0.1$). `best(...)` reproduces the stopping-rule column (200.9, 66.4, 272.1, 213.7). The "nothing" column (−107.8, 183.7) means no relief but expansion allowed. The habitual table is not printed by the saved script; these values come from calling its functions.
- Best-mix table: `results/hx_relief_types2.txt` ($d = 0.03$): 343.5 / 254.1; 260.0 (1 dose above $S = 6$); 255.8; 254.1. These match the page.
- Opponent process, `model/hx_updates.py` → `results/hx_updates_out.txt` (part 3), $\theta = 2$, $\theta C = 1.030$, shocks $+3$ every 10 periods. Rows with $r_0g_A/\epsilon \le 1.03$ (0.50, 0.50) never lock (31 uses out of 150). Rows above it (1.20, 3.00, 3.33, 1.80) do, and the run becomes permanent at $t = 0, 60, 90, 0$. The delays at 3.00 and 3.33 show the build-up in Theorem 3(3).
- $m_{\min}$: for $(r_0, g_A, \epsilon) = (0.5, 0.3, 0.05)$, the bound is $\ln(1 - 0.15/1.03)/\ln 0.95 = 3.07$, so $m_{\min} = 4$. The spacing sweep confirms it: $r_0A^*(3) = 1.05 > 1.03$ and $r_0A^*(4) = 0.81 < 1.03$. For $(0.6, 0.6, 0.2)$ the bound is 1.93, so $m = 2$; for $(1.2, 1, 1)$, $r_0g_A = 1.2 > 1.03$, so $m_{\min} = \infty$. All match the output.

## Status / limits

- **Proved:** Theorems 1 and 3 and Propositions 2 and 4. **Simulated:** the best-mix and habitual-vs-stopping tables.
- **Gap in the page's opponent-process claim:** $r_0g/\epsilon \ge \theta c$ is necessary (with $<$ giving guaranteed exit) but not by itself sufficient for lock-in. Lock-in also requires a run long enough for the counter-reaction to build to $\theta C/r_0$. The boundary case $=$ is undetermined.
- "Safe spacing" is defined by the steady per-dose rebound. The simulations show that spacing alone, without clean relief in the gaps, need not maximize value: in the output, spaced use at $m_{\min}$ is sometimes worse than the stopping rule.
- The total-value comparison with doing nothing (which depends on $d$) is simulated, not proved.
