# P5 & P6. Grief shape decides whether breadth helps; the bundle threshold

## Setup

- $n$ sources of equal pleasure. Each is lost independently with probability $q \in (0,1)$ per period. Let $X_i \sim \mathrm{Bernoulli}(q)$ indicate the loss of source $i$, $X = \sum_i X_i \sim \mathrm{Binomial}(n,q)$, and $s = \bar X_n = X/n$ the share of pleasure lost.
- **Grief** is $f(s)$, with $f : [0,1] \to [0,\infty)$, $f(0) = 0$, $f(1) = 1$ (normalization). Expected grief is $\mathbb{E} f(\bar X_n)$.
- **P6 comparison** (from `model/hx_model.py` and `bstar` in `model/hx_updates.py`), one period, $k$ strands, suffering weight $\lambda > 0$:
  - *Bundle:* the $k$ strands are lost together with probability $q$. If kept, pleasure is $k(1+b)$ (superadditive bonus $b$ per strand). If lost, grief is $\lambda k f(1)$.
  - *Spread:* $k$ separate sources, lost independently. Pleasure is $k - X$, and grief is $\lambda k f(X/k)$.

## Assumptions

- (G1) Independent, identically distributed losses; equal pleasure per source.
- (G2) Risk-neutral comparison of expected pleasure minus $\lambda\times$ grief.
- Convexity or concavity of $f$ as stated in each result.

## Statement

**P5a (linear grief).** $\mathbb{E}[\bar X_n] = q$ for all $n$: breadth gives no protection.

**P5b (squared grief).** $\mathbb{E}[\bar X_n^2] = q(1-q)/n + q^2$, strictly decreasing in $n$ toward the floor $q^2$.

**P5c (convex grief).** If $f$ is convex, $\mathbb{E} f(\bar X_n)$ is nonincreasing in $n$.

**P5d (mirror: concave grief).** If $f$ is concave, $\mathbb{E} f(\bar X_n)$ is nondecreasing in $n$: breadth raises expected grief.

**P6a (general bundle threshold).** The bundle has higher expected value than the spread iff
$$
b > b^* = \frac{\lambda\,\bigl(q\,f(1) - \mathbb{E} f(X/k)\bigr)}{1-q}, \qquad X \sim \mathrm{Binomial}(k,q).
$$

**P6b (squared grief).** For $f(s) = s^2$, $b^* = \lambda q (k-1)/k$.

**P6c (sign).** For convex $f$, $b^* \ge 0$; for concave $f$, $b^* \le 0$, so any nonnegative bonus makes the bundle weakly better; for linear $f$, $b^* = 0$.

**P6d (rare losses: what matters is grief per unit lost).** As $q \to 0$, $\mathbb{E} f(X/n) = n\,q\,f(1/n) + O(q^2)$. To first order in $q$, the breadth that minimizes expected grief minimizes $f(s)/s$ over $s \in \{1, \tfrac12, \tfrac13, \dots\}$. If $f(s)/s$ is decreasing, one source is best; if it is increasing, more breadth is better. If it falls and then rises, there is a finite best breadth near $n \approx 1/\arg\min_s f(s)/s$.

## Proofs

**P5a.** $\mathbb{E}[X/n] = nq/n = q$.

**P5b.** $\mathbb{E}[s^2] = \mathrm{Var}(s) + (\mathbb{E}s)^2 = \mathrm{Var}(X)/n^2 + q^2 = nq(1-q)/n^2 + q^2 = q(1-q)/n + q^2$.

**P5c (leave-one-out Jensen).** Let $n \ge 2$. For each $i$, let $\bar X^{(-i)} = \frac{1}{n-1}\sum_{j\ne i}X_j$ be the mean without source $i$. Then
$$
\frac1n\sum_{i=1}^n \bar X^{(-i)} = \frac{1}{n(n-1)}\sum_{i=1}^n\sum_{j\ne i}X_j = \frac{1}{n(n-1)}(n-1)\sum_j X_j = \bar X_n,
$$
because each $X_j$ appears in exactly $n-1$ of the inner sums. So $\bar X_n$ is the average of the $n$ leave-one-out means. By convexity of $f$ (finite Jensen),
$$
f(\bar X_n) = f\!\left(\frac1n\sum_i \bar X^{(-i)}\right) \le \frac1n\sum_i f(\bar X^{(-i)}).
$$
Taking expectations: each $\bar X^{(-i)}$ is the mean of $n-1$ i.i.d. Bernoulli($q$) variables, so it has the same distribution as $\bar X_{n-1}$, and $\mathbb{E}f(\bar X^{(-i)}) = \mathbb{E}f(\bar X_{n-1})$. Hence $\mathbb{E}f(\bar X_n) \le \mathbb{E}f(\bar X_{n-1})$. $\square$

**P5d.** Same argument with the Jensen inequality reversed for concave $f$. $\square$

**P6a.** Bundle: $\mathbb{E}[\text{value}] = (1-q)k(1+b) - \lambda k q f(1)$. Spread: $\mathbb{E}[k - X] - \lambda k\,\mathbb{E}f(X/k) = k(1-q) - \lambda k\,\mathbb{E}f(X/k)$. The bundle is better iff
$$
(1-q)k(1+b) - \lambda kqf(1) > k(1-q) - \lambda k\,\mathbb{E}f(X/k) \iff (1-q)\,b > \lambda\bigl(qf(1) - \mathbb{E}f(X/k)\bigr),
$$
after dividing by $k > 0$ and cancelling $k(1-q)$. Dividing by $1-q > 0$ gives $b^*$. $\square$

**P6b.** With $f(1) = 1$ and P5b at $n = k$: $q - \bigl[q(1-q)/k + q^2\bigr] = q(1-q) - q(1-q)/k = q(1-q)(k-1)/k$. Dividing by $1-q$ gives $b^* = \lambda q(k-1)/k$. $\square$

**P6c.** At $n = 1$, $\mathbb{E}f(\bar X_1) = qf(1) + (1-q)f(0) = qf(1)$. For convex $f$, P5c gives $\mathbb{E}f(X/k) \le qf(1)$, so $b^* \ge 0$. For concave $f$, P5d gives the reverse, so $b^* \le 0$. For linear $f$, both hold. $\square$

**P6d.** Split by the number of losses:
$$
\mathbb{E}f(X/n) = \underbrace{nq(1-q)^{n-1}f(1/n)}_{X=1} + \sum_{j\ge2}\binom{n}{j}q^j(1-q)^{n-j}f(j/n).
$$
The second term is at most $\max f\cdot P(X \ge 2) \le \max f \binom n2 q^2 = O(q^2)$ for fixed $n$, and $(1-q)^{n-1} = 1 - O(q)$. So $\mathbb{E}f(X/n) = q\cdot\dfrac{f(1/n)}{1/n} + O(q^2)$. Minimizing the leading term over $n$ is minimizing $f(s)/s$ over $s = 1/n$. $\square$

Note: convex $f$ with $f(0) = 0$ implies $f(s)/s$ is nondecreasing (the slope of a chord from the origin). So P6d's condition is weaker than convexity, but only first order in $q$.

## Numerical check

- `model/hx_model.py` → `results/hx_model.txt` (Monte Carlo, $q = 0.05$). P5: linear 0.0495 / 0.0501 / 0.0500; squared 0.0497 / 0.0184 / 0.0073 for $n = 1, 3, 10$. The exact P5b values are 0.0500 / 0.0183 / 0.00725. P6 ($k = 3$, $\lambda = 2$): bundle 2.546 / 2.691 / 3.114 vs spread 2.74 at $b = 0, 0.05, 0.20$. Exact: bundle $= 0.95\cdot3(1+b) - 0.3$ gives 2.550 / 2.693 / 3.120, and spread $= 2.85 - 6(0.01833) = 2.740$. $b^* = 2\cdot0.05\cdot\tfrac23 = 0.0667$.
- `model/hx_updates.py` → `results/hx_updates_out.txt` (part 1, exact sums): $b^*$ for $f = s^\gamma$, $\gamma = 0.5, 1, 1.5, 2, 3$: $-0.0718, 0, 0.0420, 0.0667, 0.0900$. Hand check for $\gamma = 3$: $\mathbb{E}(X/3)^3 = 0.135375/27 + 0.007125\cdot8/27 + 0.000125 = 0.00725$, and $2(0.05 - 0.00725)/0.95 = 0.0900$. The Monte Carlo difference at $b^* + 0.01$ is about $+0.033 \approx 0.95\cdot3\cdot0.01$, as expected. Expected grief falls with $n$ for $\gamma > 1$, is flat for $\gamma = 1$, and rises for $\gamma = 0.5$ (0.050 → 0.192), matching P5c and P5d.
- Mixed shapes, $f = w\sqrt s + (1-w)s^3$: the best $n$ (searched over $n \le 40$) is 13, 7, 5, 3, 2 for $w = 0.02, 0.05, 0.1, 0.2, 0.5$. The first-order estimate $1/\arg\min f(s)/s$ is 8.3, 5.7, 4.2, 3.0, 1.7, right in direction but rough. ($w = 0$ is pure convex and hits the search edge at 40.)

## Status / limits

- **Proved:** P5a–d and P6a–c. P6d is proved to first order in $q$.
- **Correction to the page's mixed-shapes sentence:** "a finite best breadth (2–13 sources across the shapes tried)" holds for the $\sqrt{s}$ + cubic family. The logistic S-curves in the same output give best $n = 1$ ($c = 4$) or the search edge $n = 40$ ($c = 8, 16$), not an interior optimum. Also, "f(s)/s rises or falls" is only a first-order rule for rare losses.
- Independence is essential. With correlated losses (one shock taking several sources), the floor $q^2$ in P5b rises. The variance decomposition shows this: $\mathrm{Var}(\bar X_n) = \frac{q(1-q)}{n}\bigl(1 + (n-1)\rho_X\bigr)$ for pairwise correlation $\rho_X$, which tends to $q(1-q)\rho_X$, not 0. (This is standard; it is stated here, not used above.)
- Equal pleasure per source is assumed. With unequal pleasures, $s$ is a weighted mean and the leave-one-out argument needs adjusting.
- Which grief shape a person has (prospect theory's concave vs Linville & Fischer's convex) is empirical.
