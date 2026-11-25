# Refinement lemma (v1 fractal liking, with notes on v2)

## Setup

Following `model/hx_model_v1.py` (moment valuation) and `model/hx_v1_variant.py` / `hx_v1_wall.py` (attention capture that varies with equanimity).

- An activity has a finite set of **finest parts** with likings $x_1, \dots, x_N \in \mathbb{R}$.
- A **resolution** is a partition of the parts into **features**. A feature's liking is the average of its parts: $\ell_F = \frac{1}{|F|}\sum_{k\in F}x_k$ (a mixed thing blurs toward "meh").
- Partition $\mathcal{P}'$ **refines** $\mathcal{P}$ if every feature of $\mathcal{P}'$ lies inside one feature of $\mathcal{P}$.
- **Moment valuation** with $A$ attention slots, intrusion threshold $\tau > 0$, equanimity $e \in [0,1]$, ceiling $C > 0$, and freshness $h \equiv 1$ (equal freshness):
  1. *Capture:* features with $\ell < -\tau$ are intruders; up to $A$ of the worst take slots, $I$ = that set.
  2. *Liked:* the remaining $A - |I|$ slots go to the features with the highest positive liking, $K$ = that set.
  3. *Value:* $v = C\tanh(\mathrm{pos}/C) - (1-e)\,C\tanh(\mathrm{neg}/C)$, with $\mathrm{pos} = \sum_{F\in K}\ell_F$ and $\mathrm{neg} = -\sum_{F\in I}\ell_F$.
- **Without attention capture** means $\tau = \infty$: no intruders, so $I = \varnothing$ and $v = C\tanh(\mathrm{pos}/C)$.

## Assumptions

- (F1) The finer resolution is a refinement of the coarser one (nested partitions).
- (F2) Equal freshness across features (a single moment, or freshness carried over equally).
- (F3) Valuation exactly as above. In particular $C\tanh(\cdot/C)$ is strictly increasing, so with no intruders, value is a strictly increasing function of $\mathrm{pos}$.

## Statement

**(a) Refinement under averaging, without capture.** If $\tau = \infty$ and $\mathcal{P}'$ refines $\mathcal{P}$, then $v(\mathcal{P}') \ge v(\mathcal{P})$.

**(b) With capture, refinement can lower value, even at full equanimity.** There exist parts, $A$, $\tau$ such that $v(\mathcal{P}') < v(\mathcal{P})$ for every $e \in [0,1]$, including $e = 1$.

**(c) Pairing corollary (within a moment).** Adding a parallel layer of features (another activity's features available in the same moment) can't lower $v$ if no added feature is an intruder ($\ell \ge -\tau$ for all added features). If an added feature intrudes, value can fall.

## Proof

**(a).** Let $K$ be the attended liked set at the coarse resolution, $|K| \le A$, with every $\ell_F > 0$ for $F \in K$. For each $F \in K$, let $F^\dagger$ be a finer feature inside $F$ with the largest liking. The coarse liking is the size-weighted average of the finer features it contains. (Averaging over parts in nested blocks: $\ell_F = \sum_{G\subseteq F}\frac{|G|}{|F|}\ell_G$.) A maximum is at least a weighted average, so
$$\ell_{F^\dagger} \ge \ell_F > 0.$$
The $F^\dagger$ are distinct, since different coarse features have disjoint parts, and each is liked. So $\{F^\dagger : F\in K\}$ is a feasible attended set at the fine resolution (at most $A$ liked features, no intruders since $\tau = \infty$), with
$$\sum_{F\in K}\ell_{F^\dagger} \ge \sum_{F\in K}\ell_F = \mathrm{pos}(\mathcal{P}).$$
The fine resolution attends the top $\min(A, \#\text{liked})$ features, which maximizes $\mathrm{pos}$ over feasible sets, so $\mathrm{pos}(\mathcal{P}') \ge \mathrm{pos}(\mathcal{P})$. Since $v$ is increasing in $\mathrm{pos}$ (F3), $v(\mathcal{P}') \ge v(\mathcal{P})$. $\square$

**(b).** Take $A = 1$, $\tau = 0.8$, one coarse feature with two parts $\{+2, -1.2\}$.
- *Coarse:* $\ell = 0.4 > 0$ and $0.4 > -\tau$, so it isn't an intruder and fills the one slot: $v = C\tanh(0.4/C) > 0$ ($\approx 0.398$ for $C = 3$).
- *Fine:* $-1.2 < -0.8$, so the $-1.2$ part intrudes and takes the only slot, leaving 0 slots for the $+2$ part. So $\mathrm{pos} = 0$, and $v = -(1-e)\,C\tanh(1.2/C) \le 0$.

For every $e \in [0,1]$, $v(\text{fine}) \le 0 < v(\text{coarse})$. At $e = 1$ the pain is fully neutralized, but the slot is still lost. $\square$

So softening unpleasantness, however completely, does not protect resolution. Only raising $\tau$ (releasing capture) does: if $\tau \ge 1.2$, the example reverts to case (a) and fine value is $C\tanh(2/C) > C\tanh(0.4/C)$. In the variant scripts $\tau = 0.8(1+2e)$, so capture is released only partly ($\tau = 2.08$ at $e = 0.8$). The lemma then protects refinement only for parts with $x_k \ge -\tau(e)$.

**(c).** Adding features enlarges the set of candidates without changing existing likings. If no added feature intrudes, the intruder set $I$ is unchanged and the liked candidates form a superset, so the top-$(A-|I|)$ sum of positive likings can't fall, and $v$ can't fall. If an added feature has $\ell < -\tau$, it may join $I$, take a slot and add to $\mathrm{neg}$; the (b) example with the $-1.2$ feature as the "added layer" shows $v$ can then fall. $\square$

## Notes on v2 (four skills)

v2 (`model/hx_model_v2.py`, `hx_v2_symmetric.py`) changes the valuation in three ways. These are checks of how far the lemma carries; the page doesn't claim them.
- **Concept-release dulling** multiplies attended likings by $(1 - k(1-c)) > 0$. This is a positive rescaling of $\mathrm{pos}$ (and, in the symmetric version, of $\mathrm{neg}$), so it preserves order, and (a) still holds.
- **Labeled parts capture less** ($\tau/\text{dull}$ in the symmetric version) only raises $\tau$, which helps.
- **Judging against the domain's best** ($\ell' = \ell - w(\max\ell - \ell)$, $w = J(1-e)JS$) **breaks (a) even without capture**, because refinement raises the reference $\max\ell$. Counterexample ($w = 0.1$, i.e. $e = 0$, $J = 1$, $JS = 0.1$; $\tau = \infty$; $A = 12$): coarse features are 11 with parts $\{1,1\}$ and one with parts $\{6,-4\}$, all averaging 1. Coarse: reference 1, all judged 1, $\mathrm{pos} = 12$. Fine: reference 6, the "1" parts are judged $1 - 0.1\cdot5 = 0.5$, the 6 stays 6, and $\mathrm{pos} = 6 + 11\cdot0.5 = 11.5 < 12$. This is consistent with the page's failed Stuppy & van den Bergh prediction ("the judging mechanism is probably wrong in detail").

## Numerical check

- Counterexample (b), computed with v1's valuation rule ($C = 3$): coarse 0.398; fine $0.000$ at $e = 1$ and $-1.140$ at $e = 0$.
- v2 judging counterexample, same rule with judging applied: coarse 2.99799, fine 2.99719 (both near the ceiling, fine strictly lower).
- Simulation-level evidence (not a check of the lemma itself, which is single-moment): `results/hx_model_v1.txt` (softens pain only, $e = 0.8$): mean valence peaks at $r = 3$ (0.56) and falls at $r = 4$ (0.23). `results/hx_v1_variant.txt` (capture released with $e$, $e = 0.8$): 0.04 → 0.40 → 0.81 → 1.00, and near-ceiling time 24.6% at $r = 4$. `results/hx_v1_wall.txt` (wall-clock recovery): with capture release, near-ceiling time 59.8% / 61.2% at $r = 3, 4$. These match the page's Result 2 and the robustness check.

## Status / limits

- **Proved:** (a), (b), (c) for a single moment at equal freshness under nested refinement.
- **Gap between lemma and simulation:** the scripts build resolutions with `np.array_split` over the finest parts at different counts, so a finer resolution is *not* in general a refinement of a coarser one (chunk boundaries don't align). The lemma applies exactly only to nested partitions, and the simulations use approximately nested ones.
- Across moments, freshness differs and attended parts habituate. The pairing cost found in simulation (wearing out the paired source) is a cross-period effect outside the lemma.
- The v2 judging counterexample needs many attended slots. This construction needs $(A-1)w > 1$: with one part raised by $\Delta$, the change in $\mathrm{pos}$ is $\Delta(1 - (A-1)w)$. At the default $A = 3$, $w \le 0.1$, it doesn't bite. It shows the lemma doesn't extend to v2 in general; whether (a) survives judging for small $(A-1)w$ is not settled here.
