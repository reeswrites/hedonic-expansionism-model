# What kind of claim is each finding?

Most parameters in this model are invented, so a claim is only as portable as its dependence on them. This page sorts each README claim by type and, where possible, states the condition it rests on as a unit-free ratio, a comparison between terms that doesn't depend on any particular number.

| Type | Meaning |
|---|---|
| **A: all values** | Holds for every parameter value in the model (a direction, a limit, an invariance). |
| **B: ratio condition** | Holds exactly when one unit-free ratio is above or below a threshold. |
| **C: region** | Holds across most of a sampled parameter region; the failure share is given. |
| **D: one setting** | Shown only at the default parameters. |

Sweeps drew every parameter log-uniformly within 3× either side of its default. The scripts were exploratory and are not in the repo; treat the percentages as rough.

## Summary

| # | Claim | Type | Condition, in words | Old label vs. what holds |
|---|---|---|---|---|
| 1 | Variety is a safety net | A (ceiling), B (resilience) | Breadth gets you half its ceiling at n = 1 + κ favourites, κ = wear-out rate / recovery rate. Breadth protects iff grief per unit lost grows with the size of the loss, and losses are independent. | "Proved" is right. The old wording "more favourites don't keep raising" was wrong: each one adds a little (about κ/n²), toward a ceiling. |
| 2 | Noticing more pays only if calm | B | Finer noticing pays when dislikes are mild relative to the threshold at which they grab attention: τ/σ_neg ≳ 2–3. Then it pays even with no calm at all (81% of draws above 2, 100% above 3). Calm that only softens pain doesn't protect. | Narrower than "stay calm": what matters is calm that keeps dislikes from grabbing attention. |
| 3 | Relief first, keep one small thing | B | Switch when the marginal gain from relief exceeds that from growth (R = M_R/M_E = 1). "Keep one small thing" needs diminishing returns within each kind of effort (β < 1); with linear returns the rule is all-or-nothing. Kept slice beat switching in 97% of draws, 100% for β < 0.7. | "Proved" covers the one-step rule only; the full optimal plan is simulated. |
| 4 | Numbing: bridge, not habit | B (loop), C (rest) | The habit locks in iff rebound / (trigger level × clearing rate) ≥ 1 (800/800 draws). A bridge helps only if numbing relieves faster than clean relief (ρ_n/ρ_c > 1; never helped below 1, 96% above 3). The habit is reliably worse than doing nothing only if suffering would fade faster than you discount the future (d > 1 − δ). | "Worse than doing nothing" held in only 45% of locked-in draws: stronger than the model supports. |
| 5 | Urges are a lagging guess | A/B (P7a, b), C (P7c) | Urge surfing pays except when pure liking-greedy choice under-spaces its favourites: the 1 failure in 1,500 (and 3 of 400 in a fresh sweep) all had r ≈ 0.97–0.99, where r = fresh liking of the source greedy never uses / lowest worn value it accepts. 0 failures with r < 0.85. | The old note that the exception was "within seed noise" was wrong: it is a real effect, about 50 standard errors. |
| 6 | New tastes need spacing and calm | A (directions), B (whether it can flip) | More rest and less stress always help. A dislike can flip only if its depth is smaller than the taste's eventual pull: abs(ℓ0)/A_K below the rested factor (≤ 1); deeper aversions never flip, whatever the spacing. "Every few days" is one setting (best gap 2 at ℓ0 = +0.5, 8 at −0.5). | "Simulated" undersells it: the directions are provable in a few lines. |
| 7 | Activities over purchases | B | What survives adaptation is (1 − φ) × yield. Activity beats purchase iff (1 − φ_act)·ȳ_act > (1 − φ_mat)·ȳ_mat; reverses as φ_skill nears 1 (about 0.86). | "Simulated" undersells it: near-analytic. |
| 8 | A few close people beat solo | C (55%) | Holds when company multiplies enjoyment well above solo, γ·amp·(1 + κ) ≳ 1.5–2 (12% win below 0.87, 97% above 4.6), or shared relief far exceeds solitary relief. "Two to four people" is D. | "For most people" is too strong: only about half of nearby parameter space agrees. |
| 9 | Calm beats keyed-up | C, near A | Best arousal ≤ 0.5 in 99.75% of draws; modal optimum 0.3. Engagement is symmetric about 0.5, and every other term penalises arousal, so the model can't favour high arousal. Fails mainly if calm carryover is not longer than excited carryover (an input, not a result). | "Moderate" is really moderate-to-low. |
| 10 | Meaning mostly makes hard things hurt less | B | Quieting beats meaning's other channels iff λ·P·p·(1 − e)·[K_R − K_X(1 − K_R)] > B_M + ΔA (300/300 draws). At defaults it fails; it holds when stressors come at rate > 0.37 (default 0.2). Meaning's value scales exactly with (1 − e), so meaning and equanimity substitute for all values (A). | "Mostly" comes from the research; the model's own defaults contradict it. |
| 11 | Build young, enjoy old, quick payoffs | Near A (first two parts), C (spend all when old) | Building share falls with age in 99–100% of draws under all three rules; fast payoff beats slow in 99–100%. Spending everything when old holds 61–81%; building returns late when the boredom threshold is high, because building also supplies meaning. | "Simulated" undersells the first two; "every way of adding up a life" varied rules, not parameters. |
| 12 | Fear of death: practice, early | C | Practice beats none 87%; start at 20 beats 50, 93%; steady beats only-when-dreading, 87%. A mix beats either practice alone in only 40%: it needs fast learning relative to skill decay, √(gE·gX)/decay ≳ 10 (default ≈ 9.5, right on the edge). | "Mix" is not a robust headline. |

## Cross-cutting findings

- **Several labels undersell.** Claims 6, 7 and 11 are nearly or fully provable, not just simulated.
- **Several overstate.** Claim 4 ("worse than doing nothing"), 8 ("most people"), 10 ("mostly"), 12 ("mix") hold only in part of the parameter space.
- **Choice invariance (A, with a caveat).** Choice by liking depends only on the order of the candidates' full scores, so any strictly increasing transform applied to every candidate's whole score leaves choices unchanged. In the combined model this does not hold for flattening: relief is exempt, and the curiosity and social-battery terms are added after it, so flattening shifts choices (toward sensitizing sources, away from relief).
- **The "6 of 11" combined-model check** covers its own 11 claims, not README claims 1–12; meaning, lifespan and death were never retested there.
