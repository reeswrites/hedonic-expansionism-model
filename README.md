# Hedonic expansionism

**A theory and a set of toy formal models of how to get more out of a life by expanding what you can like.**

Most accounts of well-being, in economics and in philosophy, take a person's tastes as given and ask how to satisfy them. Hedonic expansionism asks a different question: if pleasure is what matters, how should we treat the *capacity* to enjoy, which can grow, shrink, adapt and be trained? The thesis, in one sentence:

> How good a moment can feel probably has a ceiling, but the number of routes to it does not. Liking is fractal: anything liked splits into likable parts and combines into likable wholes, and other people's pleasures can become routes too. Expansion grows those routes, outward, inward and across people, so more of a life is lived near the ceiling. It pays only when calm grows with it, once whatever is currently binding has been released, and when it targets activities, skills and capacities rather than acquisitions or statuses.

This repository contains:

- **[docs/theory.md](docs/theory.md)**: the theory: motivation, thesis, value commitments, sub-claims, content constraints, relation to prior work, objections and open problems, with each claim linked to the model that tests it.
- **[docs/assumptions.md](docs/assumptions.md)**: every assumption, including implicit ones, marked as normative, evidence-backed, argued, or invented, with what changes if it's wrong.
- **[model/](model/)**: 27 small simulation scripts (Python, numpy only).
- **[proofs/](proofs/)**: proofs of the results that can be proved, with their limits.
- **[results/](results/)**: saved output of every script.
- **[prior-art/](prior-art/)**: literature checks (habituation and adaptation, wanting and liking, evolutionary grounding, adaptation by kind of good, stimulation and arousal, meaning), with each citation tagged by how well it was verified.

> **Read results as directions, not sizes.** Most parameters are invented; a few are calibrated from the literature (adaptation rates by kind of good, the acquired-taste curve). A result that is proved and simulated is solid *as a consequence of its assumptions*; whether the assumptions hold is a separate question, addressed (incompletely) by the prior-art notes and listed openly in [docs/assumptions.md](docs/assumptions.md). No empirical data has been collected for this model.

## What the models suggest

In plain terms, with how sure each one is. **Proved** means it follows mathematically from the model's assumptions. **Simulated** means it showed up in simulations with made-up numbers. **Research-backed** means published studies point the same way. Details and caveats are in [docs/theory.md](docs/theory.md).

1. **Variety helps, but mostly as a safety net.** Having more things you enjoy doesn't keep raising how good life feels, because your time is limited. What it buys is resilience when you lose one, and time for each favorite to feel fresh again. *Proved.*
2. **Getting better at noticing only pays if you stay calm.** Learning to notice finer detail (in music, food, people) reveals more to enjoy, but also more to dislike. Without equanimity, the unpleasant parts grab your attention. Experts who grade and categorize everything feel *less*, which matches published research. Calm takes practice: steady practice pays off, while practicing only when things are bad doesn't. *Proved for a single moment; simulated over time; research-backed.*
3. **When you're struggling, put more effort into relief, but never all of it.** The worse things are, the more effort should go to easing them, while keeping a little going toward things that grow your enjoyment. *Proved under stated assumptions.*
4. **Numbing yourself is fine as a bridge, dangerous as a habit.** Escaping a bad moment occasionally can help. Doing it habitually can lock into a loop that leaves you worse off than doing nothing, and the model gives the exact conditions for that loop. Avoiding these loops (and endless feeds) was the single biggest lever in the combined model. *Proved and simulated.*
5. **Your urges are a lagging guess about what you'll enjoy.** Letting urges decide less often, without fighting them, tends to help. *Partly proved; simulated.*
6. **New tastes need spaced exposure and a calm mind.** Trying something you dislike too often, too fast, or while stressed tends to kill the taste before it forms. Complex things (music, crafts, cuisines) take longer to like but stay rewarding much longer. *Simulated, calibrated to a published music study.*
7. **Invest in activities and skills, not purchases or status.** People adapt almost completely to new things and circumstances, but much less to varied, engaging activities. Gains from building skills, regular pleasures like touch or exercise, and genuine rest lasted; gains from purchases faded. *Simulated, calibrated from the adaptation research.*
8. **A few close, chosen people beat a broad solo life for most people.** The benefit comes mostly from shared relief. Solitude is the better life for people who recharge alone or find company draining. Between two people, compromising on something neither loves is the weakest option; taking turns with each other's favorites is how both expand. *Simulated; research-backed in part.*
9. **Calm beats keyed-up.** Moderate arousal works best, and calm pleasures last longer than exciting ones. Arousal mostly works through attention: it amplifies whatever already has your focus, good or bad. *Research-backed; simulated.*
10. **Meaning mostly works by making hard things hurt less.** It doesn't add much pleasure directly. Its main effect is lowering how much we resist and suffer from difficulties. *Research-backed; simulated.*
11. **Build capacity when young, enjoy it when old, and prefer things that pay off soon.** This held under every way of adding up a life that we tried. Quick-paying investments are the best hedge against a shorter life than expected. Counting boredom as suffering is enough to explain why a long, dull life isn't better than a shorter, vivid one. *Simulated.*

### Putting it together: what this says about routine

Several results point the same way: **make the timing regular, keep the content varied.**

- **Routine helps** for pleasures that build with regular use (touch and exercise seem to; regular use beat on-off cycling, and no oscillating schedule beat a fixed one), for practicing calm (steady practice pays; practicing only when things are bad doesn't), for relief cycles like effort then rest, and for acquiring new tastes through spaced exposure.
- **Routine hurts** when the content is always the same (people adapt to fixed circumstances almost completely, to varied activities much less), when everything is scheduled (planned sessions crowded out curiosity, which was already finding good options), and when a habit automates numbing.
- **A good routine, by the model:** a stable frame of regular times; varied content inside it, rotating across different kinds of experience and stopping before things go stale; social time timed by energy rather than quota; some unscheduled time for curiosity; and moderate arousal for most of the day, ending on the best part.

When all the mechanisms were run together in [one combined model](model/hx_combined.py), 6 of 11 headline claims held, 4 weakened, and 1 reversed. Those verdicts mostly survived [checks of three key assumptions](model/hx_assumption_checks.py): how heavily suffering is weighted, pain adapting more slowly than pleasure, and calm being a skill that takes practice to build. See [docs/theory.md §6b](docs/theory.md).

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
