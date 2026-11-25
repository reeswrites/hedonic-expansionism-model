# Hedonic expansionism

**A theory and a set of toy formal models of how to get more out of a life by expanding what you can like.**

Most accounts of well-being, in economics and in philosophy, take a person's tastes as given and ask how to satisfy them. Hedonic expansionism asks a different question: if pleasure is what matters, how should we treat the *capacity* to enjoy, which can grow, shrink, adapt and be trained? The thesis, in one sentence:

> How good a moment can feel probably has a ceiling, but the number of routes to it does not. Liking is fractal: anything liked splits into likable parts and combines into likable wholes, and other people's pleasures can become routes too. Expansion grows those routes, outward, inward and across people, so more of a life is lived near the ceiling. It pays only when calm grows with it, once whatever is currently binding has been released, and when it targets activities, skills and capacities rather than acquisitions or statuses.

This repository contains:

- **[docs/theory.md](docs/theory.md)**: the theory: motivation, thesis, value commitments, sub-claims, content constraints, relation to prior work, objections and open problems, with each claim linked to the model that tests it.
- **[docs/assumptions.md](docs/assumptions.md)**: every assumption, including implicit ones, marked as normative, evidence-backed, argued, or invented, with what changes if it's wrong.
- **[model/](model/)**: 26 small simulation scripts (Python, numpy only).
- **[proofs/](proofs/)**: proofs of the results that can be proved, with their limits.
- **[results/](results/)**: saved output of every script.
- **[prior-art/](prior-art/)**: literature checks (habituation and adaptation, wanting and liking, evolutionary grounding, adaptation by kind of good, stimulation and arousal, meaning), with each citation tagged by how well it was verified.

> **Read results as directions, not sizes.** Most parameters are invented; a few are calibrated from the literature (adaptation rates by kind of good, the acquired-taste curve). A result that is proved and simulated is solid *as a consequence of its assumptions*; whether the assumptions hold is a separate question, addressed (incompletely) by the prior-art notes and listed openly in [docs/assumptions.md](docs/assumptions.md). No empirical data has been collected for this model.

## Findings at a glance

| Area | Finding | Status |
| --- | --- | --- |
| Reach | Breadth alone has bounded returns under fixed time; open-endedness comes from routes and depth. Breadth's job is resilience and recovery time. | P2 proved; holds in combined model |
| Fractal liking and calm | Finer resolution never lowers what a moment can deliver *if* aversive parts can't capture attention; with capture it can. Categorizing is itself a numbing defense, matching evidence that expertise dulls emotion. | Lemma proved; simulated |
| Suffering and relief | The optimal relief share rises smoothly with distress. Habitual numbing locks into a loop under an exact condition and is worse than nothing when suffering would fade. | Proved; numbing result holds in combined model |
| Wanting | Wanting as cached value plus sensitization; lock-in proved; letting the urge steer less helps. | Partly proved; holds |
| Acquired taste | Spacing decides whether a taste forms; complex targets acquire slowly and last; stress makes acquirable tastes permanently missed. | Simulated, partly calibrated |
| Adaptation | Adaptation is near-complete for purchases and circumstances, small for intentional, varied activities. Skill-building, sensitizing and relief expansion lasts; material fades. | Literature-calibrated simulation |
| Breadth and loss | Breadth buffers only if grief is convex in the share lost; if concave, bundling wins. Closed-form bundle threshold. | Proved |
| Social | A few close, chosen people beat a broad solo life for an average person; solitude is better for low sociability. Compromise is the weakest way to be together; taking turns is how pairs expand. | Simulated |
| Arousal | Arousal acts on pleasure mainly through attention; moderate arousal is best; calm pleasure lasts longer. | Literature-backed; simulated |
| Meaning | Meaning works mainly as quieting (lowering resistance to suffering), partly by slowing adaptation, only slightly as pleasure. | Literature-backed; simulated |
| A finite life | Build capacity young, spend old, under all 24 aggregation and discounting rules tested; payoff speed is the hedge against a short life; counting boredom as suffering blocks "a long dull life beats a short intense one". | Simulated |
| Robustness | In one combined model with shared parameters, 6 of 11 headline claims hold, 4 weaken, 1 flips; avoiding numbing loops is the largest single lever. | Simulated |

**Likely novel** (see the prior-art notes): the pleasure-as-relief crossover, breadth-as-resilience conditional on convex grief with the bundle threshold, and the integrated model. Most single components already exist in the literature and are cited.

## Running

```bash
pip install -r requirements.txt
./run_all.sh        # regenerates results/*.txt (several minutes)
```

Each script also runs on its own from `model/`; each has a docstring describing its model and choices.

## Status

Exploratory and not peer reviewed. Open problems include the optimality of the three-phase relief policy, a general dynamic proof that liking-driven choice helps, freedom as a rule in a multi-agent setting, and every magnitude. Issues and critiques are welcome.

## License

Code: MIT ([LICENSE](LICENSE)). Docs, proofs and notes: CC BY 4.0 ([LICENSE-docs.md](LICENSE-docs.md)).

## Citation

reeswrites (2026). *Hedonic expansionism: a theory and toy formal models.* https://github.com/reeswrites/hedonic-expansionism-model
