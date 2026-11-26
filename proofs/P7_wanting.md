# P7. Liking, not wanting: per-period loss, lock-in, and urge surfing

## Setup

Following `model/hx_p7.py`. There are $n$ sources with liking $\ell_i > 0$ and freshness $h_i \in [0,1]$. Each period exactly one source $j$ is used, giving pleasure $\ell_j h_j$. Then:

- used: $h_j \leftarrow (1-\alpha)h_j$; rested: $h_i \leftarrow h_i + \rho(1-h_i)$; in the depleting variant, $\ell_j \leftarrow (1-\beta)\ell_j$;
- **cached prediction:** $v_j \leftarrow v_j + \eta_v(\text{pleasure}_j - v_j)$ for the used source only, with $\eta_v \in (0,1]$; $v_i$ for $i \ne j$ is unchanged;
- **sensitization:** $s_j \leftarrow s_j + \sigma$, then every $s_i \leftarrow (1-d)s_i$, with $\sigma \ge 0$, $d \in (0,1)$.

**Wanting** is $w_i = v_i + s_i$. Each period, with probability $\pi$ the urge decides ($j = \arg\max_i w_i$); otherwise liking decides ($j = \arg\max_i \ell_ih_i$). Value is $V = \sum_t \delta^t \ell_{j_t}h_{j_t}$.

## Assumptions

- (W1) Initial $v_i \ge 0$ and $s_i \ge 0$; pleasures are nonnegative, so $v_i \ge 0$ always (a convex combination of nonnegative numbers).
- (W2) For P7b, the "urge's favourite" is a fixed source $j$ that wins $\arg\max w$ whenever the urge decides.

## Statement

**P7a (per-period loss).** When source $j$ is used, the loss against the best choice by current liking is
$$
\Lambda_t = \max_i \ell_ih_i - \ell_jh_j \ge 0,
$$
with equality iff $j$ attains the maximum. If liking decides, $\Lambda_t = 0$. When the urge decides, $\Lambda_t > 0$ iff $\arg\max_i(v_i + s_i)$ doesn't attain $\max_i\ell_ih_i$. Even with $s \equiv 0$ this happens, through two staleness errors in $v$: (i) $v_j$ was set when $j$ was fresher, so it overstates a source that has habituated (missing habituation); (ii) $v_i$ for a rested source is frozen at its last, more habituated, reading, so it understates a source that has recovered (missing renewal).

**P7b (lock-in).**
1. *Sensitization steady state.* If the favourite is used every period ($\pi = 1$ under lock), $s_j \to s^* = (1-d)\sigma/d$. If it is used in each period independently with probability $f$, then $\mathbb{E}s_j \to (1-d)\sigma f/d$. In particular, if it is used exactly when the urge decides, $f = \pi$ and
$$
\mathbb{E}s_j \to s^* = \frac{(1-d)\,\sigma\,\pi}{d}.
$$
2. *Persistence (sufficient condition, $\pi = 1$).* If at some time $t_1$ the favourite wins on sensitization alone with room to spare,
$$
\min\bigl(s_j(t_1),\, s^*\bigr) > \max_{i\ne j}\bigl(v_i + s_i(t_1)\bigr),
$$
then $j$ is chosen in every later period.
3. *Necessary condition for permanent lock ($\pi = 1$).* If $j$ is chosen in every period from some time on, then $s^* \ge \max_{i\ne j} v_i^{\text{frozen}}$, where $v_i^{\text{frozen}}$ are the alternatives' last cached values. (Because $v_j \to 0$ under lock, as shown below, the relevant gap is the alternatives' *full* cached value, not the initial gap $v_i - v_j$.)
4. *Loss under lock ($\pi = 1$).* $h_j \to 0$ and $h_i \to 1$ for $i \ne j$, so $\Lambda_t \to \max_{i\ne j}\ell_i$: the full liking of the best alternative.

**P7c (urge surfing pays).** Simulated, not proved; see below.

## Proofs

**P7a.** $\Lambda_t \ge 0$ because $\ell_jh_j \le \max_i \ell_ih_i$, with equality iff $j$ is a maximizer. If liking decides, $j$ is by definition a maximizer. For the two errors: just after use, $j$'s freshness is multiplied by $1-\alpha < 1$, but $v_j$ moves only a fraction $\eta_v$ toward the (pre-update) pleasure. A rested source's $h_i$ rises toward 1, but $v_i$ doesn't change until $i$ is used again. $\square$

**P7b.1.** Under $\pi = 1$ lock, each period $s_j' = (1-d)(s_j + \sigma)$, an affine map with coefficient $1-d \in (0,1)$ and fixed point $s^* = (1-d)s^* + (1-d)\sigma \Rightarrow s^* = (1-d)\sigma/d$. By P1's Lemma, $s_j \to s^*$ monotonically. If use happens with probability $f$ independently of $s_j$, then $\mathbb{E}s_j' = (1-d)(\mathbb{E}s_j + \sigma f)$, with fixed point $(1-d)\sigma f/d$, by the same argument applied to the expectation. $\square$

**P7b.2.** Assume $j$ is chosen in every period from $t_1$ to $t$ (induction hypothesis). Then:
- For $i \ne j$: $v_i$ is frozen and $s_i(t) = (1-d)^{t-t_1}s_i(t_1) \le s_i(t_1)$, so $\max_{i\ne j}(v_i + s_i(t)) \le M := \max_{i\ne j}(v_i + s_i(t_1))$.
- $s_j(t)$ moves monotonically from $s_j(t_1)$ toward $s^*$ (P7b.1), so $s_j(t) \ge \min(s_j(t_1), s^*) > M$.
- $v_j(t) \ge 0$ by (W1).

So $w_j(t) = v_j(t) + s_j(t) > M \ge w_i(t)$ for all $i \ne j$, and $j$ is chosen at $t$. By induction, $j$ is chosen forever. $\square$

**P7b.3.** Under permanent lock from $t_0$: $h_j(t) = (1-\alpha)^{t-t_0}h_j(t_0) \to 0$, so pleasure $\ell_jh_j \to 0$. Then $v_j$, an exponentially weighted average of recent pleasures with weight $\eta_v > 0$, also tends to 0. (Formally, $v_j' = (1-\eta_v)v_j + \eta_v x_t$ with $x_t \to 0$ gives $v_j \to 0$.) $s_i \to 0$ for $i \ne j$, and the $v_i$ are frozen. If $s^* < \max_{i\ne j}v_i$, then for large $t$, $w_j(t) = v_j + s_j \to s^* < \max_{i\ne j} v_i \le \max_{i\ne j} w_i(t)$, so $j$ is not the argmax, a contradiction. $\square$

**P7b.4.** Under lock, $h_j \to 0$ as above, and each rested source satisfies $1 - h_i' = (1-\rho)(1-h_i)$, so $h_i \to 1$. So $\max_i\ell_ih_i \to \max_{i\ne j}\ell_i$ (for large $t$ the max is over $i \ne j$), and $\ell_jh_j \to 0$. $\square$

## Numerical check

`model/hx_p7.py` → `results/hx_p7.txt` ($\ell = 1.0, 0.9, 0.8, 0.7, 0.6$; $\alpha = 0.5$, $\rho = 0.3$, $\eta_v = 0.5$, $d = 0.1$, 200 periods, 50 seeds):

| $\sigma$ | $\pi=1$ | $0.5$ | $0.1$ | $0$ (liking steers) |
| --- | --- | --- | --- | --- |
| 0 | 33.69 | 54.47 | 59.08 | 60.36 |
| 0.1 | 8.29 (lock 0.94) | 50.28 | 58.58 | 60.36 |
| 0.3 | 1.98 (lock 1.00) | 46.50 | 58.42 | 60.36 |

These match the page's P7c table. Late per-period gap at $\pi = 1$, $\sigma = 0.3$: 0.90, which is $\max_{i\ne j}\ell_i = 0.9$ when the locked source is the top-liked one, as P7b.4 predicts. With $\sigma = 0.3$, $d = 0.1$: $s^* = 0.9\cdot0.3/0.1 = 2.7$ (at $\pi = 1$), far above any $v_i \le 1$, so P7b.2 guarantees permanent lock once $s_j$ climbs past the alternatives. The lock share rises from 0.26 ($\pi = 0$) to 1.00 ($\pi = 1$), roughly tracking $\pi$ above 0.5. Random worlds: $V$ rose with more urge-steering in 1 of 1,500 steps (largest +0.569; not seed noise, but a real exception: greedy liking alternates its top two sources and never rests them, and occasional urge picks space them out. Failures occur only when the unused source's fresh liking is within a few percent of the lowest worn value greedy accepts; see [claim_types.md](../docs/claim_types.md)).

## Status / limits

- **Proved:** P7a, P7b.1–4.
- **Simulated:** P7c ($V$ decreasing in $\pi$), with 1,499/1,500 monotone steps.
- **Open:** a general proof that $V$ is nonincreasing in $\pi$. It is not even clear it is true in general: under habituation, always following current liking (greedy) is not guaranteed to be optimal, so a noisy urge could in principle help by spacing uses.
- **Corrections to the page.** (1) $s^* = (1-d)\sigma\pi/d$ is a steady state of the *expected* sensitization, and it is exact only if the favourite is used exactly when the urge decides. If liking also sometimes picks it, the use frequency $f > \pi$ and $\mathbb{E}s^*$ is larger, so the page's value is a lower bound. (2) "Stays the favourite as long as $s^*$ exceeds its gap in predicted value to the next option" understates the requirement under $\pi = 1$: the favourite's own cached value erodes to 0 under lock, so permanent lock needs $s^* \ge \max_{i\ne j}v_i$ (P7b.3). A sufficient condition is P7b.2. For $\pi < 1$, $s_j$ is random and lock is a statement about frequencies, which is not proved here.
- Mechanism choice (prior art): the model has urge surfing lower how often the urge *steers* ($\pi$), not the learned value (Brewer's account). Urges fall later only through disuse, since $\mathbb{E}s^* \propto f$.
