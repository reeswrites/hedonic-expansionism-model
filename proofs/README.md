# Proofs: hedonic expansionism toy model

Each file has the same sections: Setup, Assumptions, Statement, Proof, Numerical check, Status/limits. The source is the model write-up (see ../docs/). The scripts are in `../model/` and their outputs in `../results/`. All parameters are invented, so read magnitudes as illustrations.

**Status key:** **proved** (derivation in the file); **proved + simulated** (derivation, plus a script confirms it); **simulated** (numerical only); **open** (not established).

| Result | Status | One-line statement | File |
| --- | --- | --- | --- |
| P1 no expansion | proved + simulated | With fixed sources: depleting → 0, renewing → $\ell h^* u > 0$, skill-slope → $c h^* u$ (gains iff $c h^* > \ell_0 h_0$) | [P1_no_expansion.md](P1_no_expansion.md) |
| P1 slow recovery | proved | Novelty settles at $m^* = \varepsilon(1-u)/(\beta u + \varepsilon(1-u)) > 0$; permanent loss only if $\varepsilon = 0$ or $u = 1$ | [P1_no_expansion.md](P1_no_expansion.md) |
| P2 breadth bounded | proved + simulated | $P^*(n) = T\ell h^*(T/n) \uparrow T\ell$; for $T=1$, marginal gain $= \ell\kappa/((n+\kappa)(n-1+\kappa))$ | [P2_breadth_bounded.md](P2_breadth_bounded.md) |
| P3 expansion worth it | proved | Attempt pays iff $p(S)\,\Delta P\,(1-\delta^H)/(1-\delta) > k$; finite optimal breadth | [P3_expansion_worth_it.md](P3_expansion_worth_it.md) |
| P4 threshold | proved (myopic) + simulated | Under A1–A5 the marginal-value ratio $R(S)$ rises from 0 and crosses 1 once at $S^*(L)$; $S^*$ falls in $L$, $\lambda$, relief efficiency | [P4_bottleneck.md](P4_bottleneck.md) |
| P4 DP optimum is a switch | simulated | The dynamic-programming optimum is a near-sharp relieve-then-expand switch | [P4_bottleneck.md](P4_bottleneck.md) |
| P4 soft bottleneck | proved (myopic) + simulated | With concave returns, the relief share $x^*(S)$ is interior and nondecreasing (Topkis); $x^* = \mathrm{logistic}(\ln R/(1-\beta))$ | [P4_bottleneck.md](P4_bottleneck.md) |
| P4 failure cases | proved (myopic) + simulated | Chronic pain raises $S^*$; activation with $\psi \ge \rho$ makes expansion win everywhere; inflow with $\sigma/\rho > S^*(0)$ means relief never ends | [P4_bottleneck.md](P4_bottleneck.md) |
| P4b constant-rebound loop | proved + simulated | Habitual numbing never stops iff $r \ge \theta(1-(1-\rho_n)(1-d))$; long-run flow $g(S^*)c^*L - \lambda S^*$ | [P4b_numbing_loop.md](P4b_numbing_loop.md) |
| P4b opponent-process lock-in | proved + simulated | $r_0 g/\epsilon < \theta C$ guarantees exit; lock-in needs $r_0 g/\epsilon > \theta C$ plus build-up; $m_{\min}$ spacing rule | [P4b_numbing_loop.md](P4b_numbing_loop.md) |
| P4b best relief mix | simulated | Numbing is a bridge (1–2 doses) when clean relief exists; above a capacity cost, never | [P4b_numbing_loop.md](P4b_numbing_loop.md) |
| P4c crossover | proved | Savoring out-relieves clean relief iff $g(S)c\ell h > \rho_c/\rho_p$ (fresh source: $S < 1.57$) | [P4c_pleasure_relief_crossover.md](P4c_pleasure_relief_crossover.md) |
| P4c three-phase policy | simulated; optimality open | Clean relief, then savoring, then expansion beats clean-then-expand by 3–4% | [P4c_pleasure_relief_crossover.md](P4c_pleasure_relief_crossover.md) |
| P5 convex / concave grief | proved + simulated | Convex grief: $\mathbb{E}f(\bar X_n)$ nonincreasing in $n$; concave: nondecreasing; linear: flat | [P5_P6_grief_and_bundles.md](P5_P6_grief_and_bundles.md) |
| P6 bundle threshold | proved + simulated | Bundle wins iff $b > \lambda(qf(1) - \mathbb{E}f(X/k))/(1-q)$; for $s^2$, $\lambda q(k-1)/k$ | [P5_P6_grief_and_bundles.md](P5_P6_grief_and_bundles.md) |
| P6 mixed shapes | proved (first order) + simulated | For rare losses the best breadth minimizes $f(s)/s$ | [P5_P6_grief_and_bundles.md](P5_P6_grief_and_bundles.md) |
| P7a per-period loss | proved | Loss $= \max_i\ell_ih_i - \ell_jh_j \ge 0$; cached values miss habituation and renewal | [P7_wanting.md](P7_wanting.md) |
| P7b lock-in | proved + simulated | $s^* = (1-d)\sigma\pi/d$ (in expectation); lock persists if sensitization alone beats the alternatives; locked loss → best alternative's liking | [P7_wanting.md](P7_wanting.md) |
| P7c urge surfing pays | simulated | $V$ falls as $\pi$ rises in 1,499/1,500 random-world steps | [P7_wanting.md](P7_wanting.md) |
| P7 general monotonicity | open | No proof that $V$ is nonincreasing in $\pi$ | [P7_wanting.md](P7_wanting.md) |
| Refinement lemma | proved | Without capture, nested refinement can't lower a moment's value; with capture it can, even at $e = 1$; pairing is safe without intruders | [refinement_lemma.md](refinement_lemma.md) |
| v1 Results 1–2 | simulated | Resolution backfires without calm; releasing capture lets it keep paying | [refinement_lemma.md](refinement_lemma.md) |
| S1 compersion | proved | Net positive iff $\kappa > (R + \Delta qL + a)/G$; impossible if $G \le R + \Delta qL$ (given $\kappa \le 1$) | [S_social.md](S_social.md) |
| S2 widening circle | proved + simulated | Each added person helps iff $\eta/\kappa < G/(\lambda S)$ | [S_social.md](S_social.md) |
| S3 taste transmission | proved + simulated | Measured ratio $= m[\theta + (1-\theta)D]$; equals $\theta$ only after grief and dependence fade | [S_social.md](S_social.md) |

## Corrections relative to earlier drafts of the write-up

Each is explained in its file.
- P1: "declines only if depleting" should read "goes to zero only if depleting."
- P2/P3: depth applied to one source *does* shrink like $1/n$ under an even split; depth's advantage is that it raises the ceiling $T\max\ell$.
- P4: the threshold and soft-bottleneck theorems are myopic; the page's relief-share table holds DP values, not the closed form.
- P4b: $r_0g/\epsilon \ge \theta c$ is necessary, not sufficient; lock-in also needs build-up.
- P4c: the three-phase policy and the grabbing ablation aren't in the saved script.
- P5/P6: "2–13 sources" holds only for the mixed $\sqrt{s}$ + cubic family.
- P7: $s^*$ is an expected value and a lower bound; the lock condition must use the alternatives' full cached value.
- S1: needs $\kappa \le 1$.
- S3: the early ratio is compressed and shifted down, not centered.
