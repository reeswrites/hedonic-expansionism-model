# P2. Breadth alone has diminishing, bounded returns

## Setup

- $n$ renewing sources, each with the same constant liking $\ell > 0$.
- Total time per period $T \in (0,1]$, split evenly: each source gets $u = T/n$. This requires $u \le 1$, i.e. $n \ge T$.
- Freshness follows the habituation update from P1, $h' = h - \alpha u h + \rho(1-h)(1-u)$, with steady state
  $$h^*(u) = \frac{\rho(1-u)}{\alpha u + \rho(1-u)}.$$
- Steady-state pleasure with $n$ sources:
  $$P^*(n) = \sum_{i=1}^n \ell\, h^*(u)\, u = n \cdot \ell\, h^*(T/n)\, \frac{T}{n} = T\ell\, h^*(T/n).$$
- Write $\kappa = \alpha/\rho$ (habituation relative to recovery).

## Assumptions

- (B1)–(B2) from P1: constant shares, $\alpha, \rho \in (0,1]$, so each source converges to $h^*(u)$ (P1, part 2).
- Equal liking and an even split. Unequal liking is discussed under limits.

## Statement

1. $P^*(n)$ is strictly increasing in $n$ and bounded above by $T\ell$, with $P^*(n) \to T\ell$ as $n \to \infty$.
2. For $T = 1$, in closed form:
   $$P^*(n) = \ell\,\frac{n-1}{n-1+\kappa}, \qquad P^*(n+1) - P^*(n) = \frac{\ell\,\kappa}{(n+\kappa)(n-1+\kappa)},$$
   so the marginal gain is strictly decreasing and of order $\ell\kappa/n^2$.
3. With the page's parameters ($\alpha = 0.6$, $\rho = 0.3$, so $\kappa = 2$; $\ell = T = 1$): $P^*(n) = 1 - \frac{2}{n+1}$ and the marginal gain is $\frac{2}{(n+1)(n+2)}$: $+0.333$ from 1 to 2 sources, $+0.0152$ from 10 to 11, $+0.000194$ from 100 to 101.

## Proof

**1.** Rewrite the steady state as
$$h^*(u) = \frac{1}{1 + \dfrac{\alpha u}{\rho(1-u)}} \qquad (0 < u < 1).$$
The function $u \mapsto u/(1-u)$ is strictly increasing on $(0,1)$, so $h^*$ is strictly decreasing in $u$. Since $u = T/n$ is strictly decreasing in $n$, $h^*(T/n)$ is strictly increasing in $n$, and so is $P^*(n) = T\ell\, h^*(T/n)$. (At $n = T = 1$, $u = 1$ and $h^* = 0$, consistent with the formula below.) Because $h^* < 1$, $P^*(n) < T\ell$. As $n \to \infty$, $u \to 0$, $\alpha u/(\rho(1-u)) \to 0$, and $h^* \to 1$, so $P^*(n) \to T\ell$.

**2.** With $T = 1$, $u = 1/n$ and $1 - u = (n-1)/n$:
$$h^*(1/n) = \frac{\rho (n-1)/n}{\alpha/n + \rho(n-1)/n} = \frac{\rho(n-1)}{\alpha + \rho(n-1)} = \frac{n-1}{n-1+\kappa}.$$
So $P^*(n) = \ell (n-1)/(n-1+\kappa)$. Then
$$P^*(n+1) - P^*(n) = \ell\left[\frac{n}{n+\kappa} - \frac{n-1}{n-1+\kappa}\right] = \ell\,\frac{n(n-1+\kappa) - (n-1)(n+\kappa)}{(n+\kappa)(n-1+\kappa)} = \frac{\ell\,\kappa}{(n+\kappa)(n-1+\kappa)}.$$
(The numerator: $n^2 - n + n\kappa - (n^2 + n\kappa - n - \kappa) = \kappa$.) Both factors of the denominator increase with $n$, so the marginal gain strictly decreases, and it is at most $\ell\kappa/(n-1)^2$ for $n \ge 2$.

**3.** Substitute $\kappa = 2$, $\ell = 1$: $P^*(n) = (n-1)/(n+1) = 1 - 2/(n+1)$, and the marginal gain is $2/((n+1)(n+2))$. Values: $n=1$: $2/6 = 0.3333$; $n=10$: $2/132 = 0.01515$; $n=100$: $2/10302 = 0.000194$. $\square$

## What carries the open-endedness

The page's conclusion is that **reach is open-ended iff liking strength is unbounded, through depth or through discovery**. In this model that follows because the bound $T\ell$ is linear in $\ell$: breadth moves $P^*$ toward the bound but can never pass it, while raising liking raises the bound itself.

**Correction to the page.** The page says that the value of depth (raising $\ell_i$ for one source) "doesn't shrink as $n$ grows." Under the even split that is not right. Raising one source's liking by $\Delta\ell$ adds
$$\Delta\ell \cdot h^*(T/n) \cdot \frac{T}{n},$$
which falls like $1/n$ (the rise in $h^*$ is bounded by 1). Two correct versions:

- **Depth everywhere:** raising every source's liking by $\Delta\ell$ adds $T\Delta\ell\, h^*(T/n)$, which increases with $n$ toward $T\Delta\ell$. It doesn't shrink.
- **Depth raises the ceiling:** with unequal likings and the even split, $P^* = \frac{T}{n} h^*(T/n)\sum_i \ell_i \le T \max_i \ell_i$. No amount of breadth exceeds $T\max_i\ell_i$, but raising $\max_i \ell_i$ does. Reallocating time toward the deepest source would help further, but that is limited by habituation and isn't solved here.

## Numerical check

`model/hx_model.py` → `results/hx_model.txt`, "P2 breadth". Output: $P^* = 0.000, 0.333, 0.500, 0.667, 0.818, 0.905, 0.961, 0.980$ for $n = 1,2,3,5,10,20,50,100$, and marginal gains $0.3333, 0.1667, 0.1000, 0.0476, 0.0152, 0.0043, 0.0008, 0.0002$. All match $1 - 2/(n+1)$ and $2/((n+1)(n+2))$ (e.g. $n = 5$: $1 - 2/6 = 0.667$, marginal $2/42 = 0.0476$). The same curve reappears for vicarious pleasure in `results/hx_social.txt` (2a).

## Status / limits

- **Proved** (equal liking, even split, renewing sources, steady state).
- Not shown: that the even split is optimal for unequal likings, or the optimal allocation under habituation. The bound $T\max_i\ell_i$ holds for the even split only. For an arbitrary split it is $\sum_i \ell_i h^*(u_i) u_i \le \max_i\ell_i \sum_i u_i = T\max_i \ell_i$, so the ceiling statement survives any allocation.
- Transients are ignored: a newly added source starts fresh, so short-run gains from breadth are larger than the steady-state gains here.
- Whether liking is unbounded (open-endedness) is an empirical premise, not a result. v1 (fractal liking) moves the cap from time to attention and a ceiling $C$.
