# Documentation

The prose that goes with the code, proofs and results in this repository.

| Document | What it covers |
| --- | --- |
| [theory.md](theory.md) | The theory of hedonic expansionism: motivation, thesis, value commitments, sub-claims, content constraints, relationship to hedonism and prior work, objections and replies, open problems and falsifiers. Each claim links to the proof or script that tests it. |
| [assumptions.md](assumptions.md) | Every assumption the model and theory rest on, explicit and implicit, grouped by area, with where it is used, its status (normative, evidence, argued or invented) and what changes if it is wrong. |

Elsewhere in the repository:

| Folder | Contents |
| --- | --- |
| [`../proofs/`](../proofs/README.md) | Proofs, each with setup, assumptions, statement, proof, numerical check and limits, plus an index with status labels |
| [`../model/`](../model/) | Simulation scripts, one per section of the theory |
| [`../results/`](../results/) | Saved output of every script (regenerate with `run_all.sh`) |
| [`../prior-art/`](../prior-art/) | Literature checks with verification tags: [prior_art.md](../prior-art/prior_art.md) (the model's components), [evolution_cognition.md](../prior-art/evolution_cognition.md) (evolutionary and cognitive grounding, the strongest objections), [adaptation_by_domain.md](../prior-art/adaptation_by_domain.md) (how completely people adapt, by kind of good), [stimulation_challenge.md](../prior-art/stimulation_challenge.md) (arousal, stimulation and challenge) |

## Suggested reading order

1. [theory.md §2, Thesis](theory.md#2-thesis), for the claim and where each part is tested.
2. [assumptions.md, The assumptions that matter most](assumptions.md#the-assumptions-that-matter-most), for what the conclusions hinge on.
3. [theory.md §7, Objections and replies](theory.md#7-objections-and-replies), especially the strongest objection and where the model shows it partly lands.
4. The [proofs index](../proofs/README.md), then individual proofs.

**Read results as directions, not sizes.** Almost every numeric parameter is invented; see the status column in [assumptions.md](assumptions.md).
