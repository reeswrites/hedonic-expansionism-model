# P4. Find the bottleneck: threshold theorem, soft (gradient) version, failure cases

## Setup

State $(S, L)$: suffering $S \ge 0$ and liking stock $L \ge 0$. Each period one unit of effort is split: share $r \in [0,1]$ to relief, $1-r$ to expansion. Following `model/hx_p4.py`:

$$
S' = S - \varphi(S)\,r - \psi S (1-r) + \sigma, \qquad L' = (1-\kappa_L) L + \Delta\, p(S)\,(1-r),
$$

where $\varphi(S)$ is suffering removed per unit of relief (the script uses $\varphi(S) = \rho S$), $\psi \ge 0$ is relief produced by expansion itself (behavioral activation; baseline $\psi = 0$), $\sigma \ge 0$ is stressor inflow (baseline $0$), $\Delta > 0$ is expansion efficiency, $p(S)$ is the success rate, and $\kappa_L \in [0,1)$ is liking decay.

Per-period flow and value:
$$
u(S, L) = g(S)\,L - \lambda S, \qquad V = \sum_t \delta^t u(S_t, L_t).
$$

Numbing elasticity: $\eta(S) = -g'(S)/g(S) = -\tfrac{d}{dS}\ln g(S)$.

**Marginal values (myopic, first order).** One unit of relief lowers $S$ by $\varphi(S)$, and one unit of expansion raises $L$ by $\Delta p(S)$. To first order, evaluated at the current state:

$$
M_R(S,L) = \varphi(S)\left(-\frac{\partial u}{\partial S}\right) = \varphi(S)\bigl(\lambda + L\,|g'(S)|\bigr) = \varphi(S)\bigl(\lambda + L\, g(S)\,\eta(S)\bigr),
$$
$$
M_E(S,L) = \Delta\, p(S)\,\frac{\partial u}{\partial L} = \Delta\, p(S)\, g(S).
$$

Their ratio is
$$
R(S) = \frac{M_R}{M_E} = \frac{\varphi(S)}{\Delta\,p(S)}\left[\frac{\lambda}{g(S)} + L\,\eta(S)\right].
$$

The **myopic rule** relieves iff $R > 1$. This is the "greedy" policy in the script.

## Assumptions

- (A1) $g$ is differentiable, $g > 0$, nonincreasing, $g(0) = 1$, and log-concave ($\ln g$ concave), so $\eta \ge 0$ and $\eta$ is nondecreasing. This covers exponential numbing ($\eta \equiv k$) and logistic numbing ($\eta(S) = k\,\mathrm{logistic}(k(S - s_0))$, increasing). It covers linear numbing $g = 1 - kS$ only on $[0, 1/k)$, where $g > 0$; there $\eta = k/(1-kS)$ is increasing. The script clips at 0, but with $k = 0.09$ and $S \le 10 < 1/k$ the clip never binds.
- (A2) $p > 0$ and nonincreasing.
- (A3) $\varphi(0) = 0$ and $\varphi$ is strictly increasing.
- (A4) $\lambda > 0$.
- (A5) Relief wins somewhere: there is $\bar S$ in the state space with $R(\bar S) > 1$.
- (A6, for the crossing to be a single point) $\varphi$, $p$, $g$, $g'$ are continuous.

## Statement

**Theorem 1 (threshold).** Fix $L \ge 0$, with $\psi = \sigma = 0$. Under (A1)–(A4), $R$ is strictly increasing on $[0,\infty)$ with $R(0) = 0$. Under (A5)–(A6) there is a unique $S^*(L) \in (0, \bar S)$ with $R(S^*) = 1$; the myopic rule expands for $S < S^*$ and relieves for $S > S^*$. $S^*$ is nonincreasing in $L$ and $\lambda$, nonincreasing in relief efficiency (replacing $\varphi$ by $a\varphi$ with $a > 1$), and nondecreasing in $\Delta$.

**Remark (order needs only A3–A4).** With $g \equiv 1$ and $p$ constant, $R = \lambda\varphi(S)/(\Delta p)$ is still strictly increasing from 0. The direct cost of suffering alone creates the threshold; numbing and blocked learning only lower it.

**Proposition 2 (affect gain).** The first-order gain in positive feeling from one unit of relief is $G(S) = \varphi(S)\, L\, |g'(S)|$. With $\varphi = \rho S$ and exponential numbing $g = e^{-kS}$, $G(S) = \rho k L\, S e^{-kS}$ is hump-shaped with its maximum at $S = 1/k$. If $g$ is concave, $G$ is strictly increasing.

**Theorem 3 (soft bottleneck).** Suppose relief effort $x$ delivers $\varphi(S) h(x)$ and expansion effort $1-x$ delivers $\Delta p(S) h(1-x)$, with $h$ increasing and strictly concave. Then the myopic share
$$
x^*(S) = \arg\max_{x\in[0,1]}\; M_R\,h(x) + M_E\,h(1-x)
$$
is unique and nondecreasing in $S$ (Topkis). It equals $1/2$ exactly where $R = 1$, i.e. at the old threshold $S^*$. For $h(x) = x^\beta$ with $0 < \beta < 1$:
$$
x^* = \frac{R^{1/(1-\beta)}}{1 + R^{1/(1-\beta)}} = \mathrm{logistic}\!\left(\frac{\ln R}{1-\beta}\right),
$$
which is interior for $0 < R < \infty$.

**Proposition 4 (failure cases).**
1. *Chronic pain* (relief nearly impossible). With $\varphi = \rho S$, $R$ is proportional to $\rho$, so $S^*$ increases as $\rho \to 0$. If $\rho$ is small enough, (A5) fails on a bounded state space and the myopic rule expands at every distress level.
2. *Behavioral activation* ($\psi > 0$). The myopic rule relieves iff $(\rho - \psi) S \bigl(\lambda + L g\eta\bigr) > \Delta p g$. If $\psi \ge \rho$, expansion wins at every $S$. If $\psi < \rho$, Theorem 1 holds with $\varphi$ replaced by $(\rho-\psi)S$, so the threshold is higher.
3. *Stressor inflow* ($\sigma > 0$, $\varphi = \rho S$). Under full relief $S_t \to \sigma/\rho > 0$. If $\sigma/\rho > S^*(0)$, then from any start the myopic rule eventually relieves in every period: there is no "after the bottleneck."

## Proofs

**Theorem 1.** Write $R = f \cdot B$ with $f(S) = \varphi(S)/(\Delta p(S))$ and $B(S) = \lambda/g(S) + L\eta(S)$.

*$f$ is strictly increasing with $f(0) = 0$.* $f(0) = 0$ by (A3). For $0 \le S_1 < S_2$: $\varphi(S_1) \ge 0$ and, by (A2), $0 < p(S_2) \le p(S_1)$, so
$$
f(S_1) = \frac{\varphi(S_1)}{\Delta p(S_1)} \le \frac{\varphi(S_1)}{\Delta p(S_2)} < \frac{\varphi(S_2)}{\Delta p(S_2)} = f(S_2),
$$
where the strict step uses $\varphi(S_1) < \varphi(S_2)$ from (A3).

*$B$ is positive and nondecreasing.* $g > 0$ is nonincreasing, so $\lambda/g$ is positive (A4) and nondecreasing. By (A1), $\eta = -(\ln g)'$ is nondecreasing and $\ge 0$, and $L \ge 0$. So $B > 0$ and $B$ is nondecreasing.

*Product.* For $S_1 < S_2$: $R(S_1) = f(S_1)B(S_1) \le f(S_1)B(S_2) < f(S_2)B(S_2) = R(S_2)$. The first step uses $f(S_1) \ge 0$ and $B(S_1) \le B(S_2)$; the second uses $f(S_1) < f(S_2)$ and $B(S_2) > 0$. So $R$ is strictly increasing with $R(0) = 0$.

*Crossing.* Under (A6), $R$ is continuous. $R(0) = 0 < 1 < R(\bar S)$, so by the intermediate value theorem some $S^* \in (0, \bar S)$ has $R(S^*) = 1$, and strict monotonicity makes it unique, with $R < 1$ below and $R > 1$ above. (Without (A6), $\{S : R(S) \le 1\}$ is still an interval $[0, S^*]$ or $[0, S^*)$, so the rule still switches exactly once.)

*Comparative statics.* $\partial R/\partial L = f\eta \ge 0$ and $\partial R/\partial \lambda = f/g \ge 0$. Scaling $\varphi$ by $a > 1$ scales $R$ by $a$, and raising $\Delta$ scales $R$ by $1/\Delta$. In general, if $R(\cdot\,;\theta') \ge R(\cdot\,;\theta)$ pointwise, then $R(S^*(\theta);\theta') \ge 1$, and since $R(\cdot\,;\theta')$ is strictly increasing and equals 1 at $S^*(\theta')$, we get $S^*(\theta') \le S^*(\theta)$. $\square$

*Dynamics of the myopic rule.* With $\psi = \sigma = 0$, relief strictly lowers $S$ (if $\varphi(S) \le S$) and expansion leaves $S$ unchanged while raising $L$ when $\Delta p > \kappa_L L$. A rising $L$ lowers $S^*(L)$, which can put the current $S$ back above the threshold. So the myopic path is: relieve down to $S^*$, expand, top up relief. The greedy rollout for exponential numbing shows exactly this ($r_t$ = 1,1,1,0,1,0,0 at $t$ = 0,2,5,10,20,40,80 from $S_0 = 8$).

**Proposition 2.** Lowering $S$ by $\varphi(S)$ raises $gL$ by $\varphi(S)L|g'(S)|$ to first order. For $g = e^{-kS}$ and $\varphi = \rho S$: $G(S) = \rho k L\,S e^{-kS}$ and $G'(S) = \rho k L\,e^{-kS}(1 - kS)$, which is positive for $S < 1/k$ and negative for $S > 1/k$. If $g$ is concave, $|g'| = -g'$ is nondecreasing, so $G = \varphi L|g'|$ is a product of a strictly increasing nonnegative function and a nonnegative nondecreasing one; it is strictly increasing wherever $g' \ne 0$, by the same product argument as in Theorem 1. $\square$

So the page's caution is correct: "relief raises positive feeling most in the most distressed" needs concave (or threshold-like) numbing. Under exponential numbing the gain peaks at moderate distress ($S = 4$ for $k = 0.25$).

**Theorem 3.** Dividing the objective by $M_E > 0$ doesn't change the maximizer, so maximize
$$
F(x, S) = R(S)\,h(x) + h(1-x).
$$
*Uniqueness:* $F(\cdot, S)$ is strictly concave in $x$ (a positive multiple of a strictly concave function plus a strictly concave function), so the maximizer on $[0,1]$ is unique.
*Monotonicity (Topkis):* $\partial^2 F/\partial x\,\partial S = R'(S)\,h'(x) \ge 0$, since $R$ is nondecreasing (Theorem 1) and $h$ is increasing. So $F$ has increasing differences in $(x, S)$, and by Topkis' theorem the maximizer $x^*(S)$ is nondecreasing in $S$. (For differentiable $h$, the cross-partial condition is equivalent to increasing differences.)
*Midpoint:* at $R = 1$, $F(x) = h(x) + h(1-x)$ is symmetric under $x \mapsto 1-x$, so by uniqueness $x^* = 1/2$.
*Power case:* for $h(x) = x^\beta$, $h'(0^+) = \infty$, so the optimum is interior and satisfies the first-order condition
$$
R\,\beta x^{\beta-1} = \beta (1-x)^{\beta-1} \iff \left(\frac{x}{1-x}\right)^{1-\beta} = R \iff \frac{x}{1-x} = R^{1/(1-\beta)}.
$$
Solving, $x^* = z/(1+z)$ with $z = R^{1/(1-\beta)}$. Writing $z = e^{\ln R/(1-\beta)}$ gives the logistic form. $\square$

**Proposition 4.**
1. $R \propto \rho$, so the pointwise comparison argument gives that $S^*$ is nonincreasing in $\rho$. On a bounded space $[0, S_{\max}]$, choose $\rho < 1/\bigl(R(S_{\max})|_{\rho = 1}\bigr)$; then $R < 1$ everywhere and (A5) fails.
2. One unit of expansion now also lowers $S$ by $\psi S$, so $M_E^{BA} = \Delta p g + \psi S(\lambda + Lg\eta)$, while $M_R$ is unchanged. Then $M_R > M_E^{BA} \iff (\rho-\psi)S(\lambda + Lg\eta) > \Delta p g$. If $\psi \ge \rho$, the left side is $\le 0 <$ the right side for every $S$. If $\psi < \rho$, this is Theorem 1's condition with $\varphi$ replaced by $(\rho-\psi)S$, which satisfies (A3); the threshold rises because $(\rho - \psi)S < \rho S$.
3. With $r = 1$, $S' = (1-\rho)S + \sigma$, an affine map with fixed point $\sigma/\rho$ (P1's Lemma), so relief can never push $S$ below $\sigma/\rho$ in the limit, and from above it never goes below. With $r = 0$, $S' = S + \sigma$, so $S$ rises. $S^*(L) \le S^*(0)$ for all $L \ge 0$ (comparative statics). Suppose $\sigma/\rho > S^*(0)$. Any period with $S \le S^*(L)$ is an expansion period and raises $S$ by $\sigma$, so after finitely many periods $S > S^*(0) \ge S^*(L)$. From then on the rule relieves, and under relief $S$ stays $\ge \min(S, \sigma/\rho) > S^*(0)$, so it relieves forever. $\square$

## Numerical check

- `model/hx_p4.py` → `results/hx_p4_out.txt`. Exponential case ($\lambda = 1.5$, $\Delta = 0.5$, $\rho = 0.3$, $p = 0.9e^{-0.25S}$, $g = e^{-0.25S}$): greedy $S^*(L=1) = 0.64$ and $S^*(L=10) = 0.34$. Solving $R = 1$ in closed form gives $0.637$ and $0.334$, and $S^*(0) = 0.703$. The thresholds fall with $L$ in all three shapes (linear 0.81 → 0.57, sigmoid 0.95 → 0.83), as Theorem 1 says.
- Failure cases from the same output: chronic pain $\rho = 0.01$ gives $S^* = 3.94$ ($L=1$), and solving $R=1$ gives 3.940. Behavioral activation $\psi = 0.25$ gives $S^* = 2.00$, which equals the Theorem-1 threshold with $\rho - \psi = 0.05$ (closed form 2.002). Stressor inflow $\sigma = 0.5$: greedy relieves in every sampled period, and $S_{\text{end}} = 1.67 = \sigma/\rho > S^*(0) = 0.70$.
- Page table values (Optimal / Relief-first / Expansion-first / 50-50) match the output, e.g. linear $S_0 = 8$: 151.1 / 142.3 / −286.9 / 58.6.
- Soft bottleneck: `model/hx_updates.py` → `results/hx_updates_out.txt` (part 2). The closed-form greedy share at $S = S^* = 0.64$ is 0.50 for every $\beta < 1$, as Theorem 3 says. The DP-optimal share is monotone in $S$ for $\beta = 1, 0.7, 0.5$, with 1 grid violation at $\beta = 0.9$. Splitting beats the bang-bang switch: at $\beta = 0.5$, greedy 167.2 vs 130.8 (+28%) and DP 166.7 (+27%) from $S_0 = 8$.

## Status / limits

- **Theorems 1 and 3 are proved for the myopic (one-period, first-order) rule.** The page's "so the best policy is relief down to $S^*$" goes further: that the *dynamic-programming* optimum is a single switch is **simulated, not proved**. The DP optimum differs from the greedy one in value (e.g. 138.8 vs 130.8, exponential, $S_0 = 8$) and in timing.
- **Correction to the page's soft-bottleneck table.** The relief shares quoted on the page ($\beta = 0.7$: 0.40 / 0.70 / 0.95 / 1 at $S$ = 0.5 / 1 / 3 / 8) are the DP shares at $t = 0$, not values of the closed-form $x^*$, which gives 0.27 / 0.89 / 1.00 / 1.00. The DP 50/50 point also sits above $S^*$ (0.75 for $\beta = 0.7$, 0.88 for $\beta = 0.5$, vs 0.64). The closed form and the Topkis monotonicity are myopic results; DP monotonicity is numerical only.
- The greedy beating the DP at $\beta = 0.5$ (167.2 vs 166.7) is discretization error (21 actions, 81 × 81 grid).
- Linear numbing satisfies (A1) only while $g > 0$.
- Suffering of different kinds (the prior-art "soft and typed" note) is not modeled: one $S$, one $g$, one $p$.
