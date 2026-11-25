# P3. When expansion is worth it

## Setup

- Discount factor $\delta \in (0,1]$, remaining horizon $H \in \{1, 2, \dots\}$ periods.
- An expansion attempt costs $k > 0$ in enjoyment now (in this period's value units).
- It succeeds with probability $p(S) \in [0,1]$, nonincreasing in suffering $S$ ("safety comes first").
- If it succeeds, per-period pleasure rises by $\Delta P \ge 0$ in each of the remaining $H$ periods, starting this period ($t = 0, \dots, H-1$).
- The annuity factor is
  $$A(\delta, H) = \sum_{t=0}^{H-1}\delta^t = \begin{cases}\dfrac{1-\delta^H}{1-\delta} & \delta < 1\\[4pt] H & \delta = 1.\end{cases}$$

## Assumptions

- (C1) The person is risk-neutral over $V = \sum_t \delta^t(P_t - \lambda S_t)$ (expected value is what counts).
- (C2) A failed attempt changes nothing except the cost $k$; a successful one changes only $P$, by a constant $\Delta P$.
- (C3) $S$ and $p(S)$ are fixed during the decision (the attempt doesn't change suffering).
- (C4) Not attempting is always available at zero cost.

## Statement

The attempt raises expected value iff

$$
p(S)\,\Delta P\,\frac{1-\delta^H}{1-\delta} > k \qquad \bigl(\text{for } \delta = 1:\ p(S)\,\Delta P\, H > k\bigr).
$$

**Comparative statics.** The left side is nondecreasing in $H$ and in $\delta$, nonincreasing in $S$, and increasing in $\Delta P$. So expansion fails when the horizon is short, the person is under threat ($p$ low), the gain is small, or the attempt is costly ($k$ high).

**Corollary (finite optimal breadth).** Suppose each attempt adds one source to a set of $n$ equal renewing sources, so $\Delta P = \Delta P(n) = P^*(n+1) - P^*(n)$ from P2, and $k$, $p$, $A$ stay fixed from one attempt to the next. Then there is a finite $\bar n$ such that adding a source pays iff $n < \bar n$, and stopping at $\bar n$ maximizes expected value among one-at-a-time breadth plans. With the P2 parameters ($T = \ell = 1$, $\kappa = \alpha/\rho = 2$):

$$
\text{adding the } (n+1)\text{th source pays} \iff (n+1)(n+2) < \frac{2\,p(S)\,A(\delta,H)}{k}.
$$

## Proof

**Main inequality.** Under (C1)–(C4) the expected change in $V$ from attempting is
$$
\mathbb{E}[\Delta V] = -k + p(S)\sum_{t=0}^{H-1}\delta^t\,\Delta P + (1-p(S))\cdot 0 = p(S)\,\Delta P\,A(\delta,H) - k.
$$
For $\delta < 1$ the geometric sum is $(1-\delta^H)/(1-\delta)$, since $(1-\delta)\sum_{t=0}^{H-1}\delta^t = 1 - \delta^H$. Attempting beats not attempting iff $\mathbb{E}[\Delta V] > 0$, which is the stated inequality.

**Comparative statics.** $A$ is a sum of $H$ nonnegative terms $\delta^t$, so it is nondecreasing in $H$, and each term is nondecreasing in $\delta$. $p$ is nonincreasing in $S$ by assumption. The left side is the product of nonnegative factors, so it inherits each monotonicity.

**Corollary.** From P2, $\Delta P(n) = \ell\kappa/((n+\kappa)(n-1+\kappa))$, which is strictly decreasing and tends to 0. So $D(n) = p\,\Delta P(n)\,A - k$ is strictly decreasing in $n$ and tends to $-k < 0$. Let $\bar n = \min\{n \ge 1 : D(n) \le 0\}$ (finite, since $D(n) \to -k$). Then $D(n) > 0$ for $n < \bar n$ and $D(n) \le 0$ for $n \ge \bar n$. The expected value of growing from $n_0$ to $N$ sources is $\sum_{n=n_0}^{N-1} D(n)$, a sum of terms that are positive and then nonpositive, so it is maximized at $N = \bar n$ (for $n_0 < \bar n$). With $\kappa = 2$, $\ell = 1$: $\Delta P(n) = 2/((n+1)(n+2))$, and $D(n) > 0 \iff (n+1)(n+2) < 2pA/k$. $\square$

## Numerical check

No dedicated script; the inequality is exact. The corollary uses $\Delta P(n)$ from P2, checked in `results/hx_model.txt` (marginal column). Example: $p = 0.5$, $\delta = 0.97$, $H = 100$ gives $A = (1 - 0.97^{100})/0.03 = (1 - 0.0476)/0.03 = 31.7$. With $k = 0.5$, $2pA/k = 63.5$, so adding pays while $(n+1)(n+2) < 63.5$, which is up to $\bar n = 7$ sources ($7 \cdot 8 = 56 < 63.5$, $8 \cdot 9 = 72 > 63.5$).

## Status / limits

- **Proved** under (C1)–(C4).
- Gains starting next period rather than now multiply the left side by $\delta$.
- Holding $A$ fixed across successive attempts ignores that each attempt uses up horizon. Since $A$ only shrinks over time, this shortcut can only overstate $\bar n$.
- On depth vs breadth: the page says depth "has no such ceiling." That holds only if liking is unbounded (P2) and only for depth applied broadly. Raising one source's liking under an even split gives a gain that shrinks like $1/n$ (see the correction in P2).
- "Permission, not obligation" is the observation that the inequality fails for many realistic $(p, H, k, \Delta P)$; that is an empirical claim about those values, not a theorem.
