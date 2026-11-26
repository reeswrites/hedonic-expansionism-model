# Hedonic expansionism: the theory

This document states the theory that the code in this repository tests: why it is worth asking, what it claims, which value commitments it rests on, how it relates to existing work, the strongest objections, and what would count against it. Each claim links to the proof, script or saved result that bears on it. Every assumption the model makes, including the implicit ones, is listed in [assumptions.md](assumptions.md).

> **Status.** Exploratory and not peer reviewed. The formal model is a toy. Almost every numeric parameter is invented, so the model can show which claims *follow from* the commitments, which need extra premises, and which are false as stated. It cannot show how large any effect is. Read results as directions, not sizes.

**Contents**

1. [Motivation](#1-motivation)
2. [Thesis](#2-thesis)
3. [Value commitments](#3-value-commitments)
4. [Sub-claims](#4-sub-claims)
5. [Content constraints](#5-content-constraints)
6. [Relationship to hedonism and to prior work](#6-relationship-to-hedonism-and-to-prior-work)
7. [Objections and replies](#7-objections-and-replies)
8. [Open problems and falsifiers](#8-open-problems-and-falsifiers)

---

## 1. Motivation

### Tastes are usually treated as fixed

Most formal accounts of well-being take a person's tastes as given and ask how to satisfy them.

- **Economics.** Stigler and Becker's "De Gustibus Non Est Disputandum" (1977) holds underlying tastes stable across people and time and explains apparent taste change through accumulated "consumption capital." Welfare analysis by revealed preference goes further: what a person chooses *is* the measure of what is good for them, so there is no standpoint from which to ask whether they could come to like something better. Work on endogenous preferences (Bowles 1998) is the main exception, and it is usually framed as a problem for welfare comparison rather than an opportunity.
- **Welfare theory.** Desire-satisfaction theories score a life by how well its desires are met, so changing what one desires is at best neutral. Hedonistic theories score a life by its pleasure and suffering but, in practice, also take the sources of pleasure as fixed and ask how to arrange them.
- **Psychology.** Liking is often measured as a stable trait or a set point that life events perturb and that well-being reverts to.

There are good reasons for this. Fixed tastes make choice data interpretable, protect against paternalism ("you should want something else"), and match the observation that people adapt to most changes in circumstances.

### The question this theory asks instead

Tastes demonstrably change. Most adults like things they disliked as children (coffee, bitter greens, chili, sad music); repeated exposure raises liking for unfamiliar foods and music (Zajonc 2001; Wardle et al. 2003; Szpunar et al. 2004); people acquire tastes from those around them (Birch 1980); and expertise changes how things are experienced, though not always for the better (Rocklage et al. 2021). If tastes can grow, then a theory of well-being has to ask a question that the fixed-taste framing rules out:

> **Is coming to like more things, and to like things better, a good in its own right, and if so, when is it worth pursuing, and which kinds of new liking count?**

Hedonic expansionism is an answer to that question, framed within ethical hedonism. It does not claim that tastes *should* change, or that anyone has a duty to change theirs. It claims that the capacity to like is a lever on how well a life goes, that the lever has predictable limits, and that those limits can be stated precisely enough to test.

---

## 2. Thesis

**Coming to like more things, and to like things better, is a central derived good: the most robust way to get more pleasure over a life. What a person comes to like also matters.**

In one sentence: *how good a moment can feel probably has a ceiling, but the number of routes to it does not. Liking is fractal (anything liked splits into likable parts and combines into likable wholes), and other people's pleasures can become routes too. Expansion grows those routes, outward, inward and across people, so that more of a life is lived near the ceiling. It pays only when calm grows with it and once whatever is currently binding has been released. It targets activities, skills and capacities, not acquisitions or statuses.*

### Three aims and two dimensions

A pleasure-centred life has three aims: **enjoy** what one already likes, **extend** the healthy time in which to enjoy it, and **expand** what one is able to enjoy. This theory is about the third. The aims act on two dimensions:

- **Baseline:** how acceptable ordinary experience feels (ease, security, relief; what the Epicureans called *katastematic* pleasure). Baseline gains are bounded, because relief tops out when suffering reaches zero.
- **Reach:** how high and how widely pleasure can go (peaks, new sources, finer appreciation; *kinetic* pleasure). Reach is bounded in intensity per moment, but not in the number of routes to that intensity.

Enjoying uses the baseline and reach one already has. Extending multiplies both by time. Expanding is how reach grows. The two dimensions are coupled: suffering is often a bottleneck on reach, not only a weight on baseline, because threat and numbing suppress liking as well as adding pain.

### The parts of the thesis, and where each is tested

| Part | Claim | Where tested |
| --- | --- | --- |
| Ceiling per moment | Pleasure in a moment saturates. Under fixed time, breadth alone has bounded, fast-diminishing returns. | [P2](../proofs/P2_breadth_bounded.md) (proved); [hx_model.py](../model/hx_model.py) |
| Open-ended routes | Reach is open-ended only if liking strength is unbounded through depth or discovery; breadth's job is resilience and rest, not open-endedness. | [P2](../proofs/P2_breadth_bounded.md), [P3](../proofs/P3_expansion_worth_it.md) |
| Liking is fractal | Finer resolution can only add to what a moment delivers, *if* aversive parts cannot capture attention. | [Refinement lemma](../proofs/refinement_lemma.md) (proved); [hx_model_v1.py](../model/hx_model_v1.py), [hx_v1_wall.py](../model/hx_v1_wall.py) |
| Outward | New sources: acquired tastes, with spacing and complexity deciding whether a taste forms and how long it lasts. | [hx_acquired_taste.py](../model/hx_acquired_taste.py) |
| Inward | Finer appreciation of familiar sources (resolution), which pays only with equanimity and concept release. | [hx_model_v2.py](../model/hx_model_v2.py), [hx_v2_symmetric.py](../model/hx_v2_symmetric.py) |
| Across people | Others' pleasures registering as one's own (*mudita*), and tastes transmitted through relationships. | [S1–S3](../proofs/S_social.md); [hx_social.py](../model/hx_social.py), [hx_pair.py](../model/hx_pair.py) |
| Pays only with calm | Without equanimity, more resolution reveals more aversive parts and can make life worse. | [Refinement lemma (b)](../proofs/refinement_lemma.md); [results/hx_model_v1.txt](../results/hx_model_v1.txt) |
| Once what binds is released | Effort should be weighted toward relieving suffering in proportion to how much it binds. | [P4](../proofs/P4_bottleneck.md), [P4b](../proofs/P4b_numbing_loop.md), [P4c](../proofs/P4c_pleasure_relief_crossover.md) |
| Activities, not acquisitions | Under adaptation calibrated by kind of good, skill-building and sensitizing sources keep paying; purchases and circumstances fade. | [hx_adaptation_ladder.py](../model/hx_adaptation_ladder.py); [results](../results/hx_adaptation_ladder.txt) |

The thesis has been revised as the model was built. An earlier version said "baseline is bounded and reach is open-ended." Formalizing it showed that breadth alone cannot deliver open-endedness under a fixed time budget ([P2](../proofs/P2_breadth_bounded.md)), which led to the current version: the ceiling is per moment, and open-endedness lives in the number of routes and in depth.

---

## 3. Value commitments

The theory rests on **ethical hedonism**: pleasure is the only thing good in itself and suffering the only thing bad in itself. Everything else, including expansion, matters because of its effects on pleasure and suffering. These commitments are value choices, not findings. The model takes them as inputs; see the NORMATIVE rows of [assumptions.md](assumptions.md#1-values-and-normative-choices).

### Ethical, not psychological, hedonism

Pleasure is what matters, but people do not automatically pursue it. Wanting and liking come apart (Berridge and Robinson 2016), which is why expansion takes effort, practice and design rather than happening on its own. The theory makes no claim that people are pleasure-maximizers.

### Two levels

- **Prudential (how a life goes):** a life goes well as its pleasure exceeds its suffering over its whole length. In the model this is $V = \sum_t \delta^t (P_t - \lambda S_t)$.
- **Moral (how to treat others):** causing suffering is wrong whoever suffers, and everyone's pleasure and suffering count. On hedonism, anything that can feel counts.

### Quantity, not rank

There is no hierarchy of "higher" over "lower" pleasures, unlike Mill. Intensity, duration and renewal are what count. Breadth matters because more sources, and renewing ones, yield more over a life and buffer losses, not because some tastes are more refined.

### Suffering weighting is a normative choice

The model weights suffering above pleasure ($\lambda > 1$; 1.5 or 2 depending on the script). This is a **value choice**, not a calibration. Loss aversion (about 2 in choice data; Brown et al. 2024) is a decision weight, and in experience losses hurt less than people forecast (Kermer et al. 2006; Gal and Rucker 2018). If suffering inputs are already measured in felt intensity, an extra $\lambda$ double-counts negativity bias ([evolution_cognition.md §2](../prior-art/evolution_cognition.md)). The theory's position is that honest measurement of intensity already gives suffering more weight in most real cases, and that $\lambda$ should be swept, not cited. The current scripts do not sweep it; see [assumptions.md](assumptions.md#1-values-and-normative-choices).

### Freedom is a rule-level constraint

Freedom is not a third value beside pleasure and suffering. It is the rule that reliably protects both, justified at the level of practices rather than single acts (a two-level or rule-consequentialist structure). It does three jobs: being controlled or trapped causes suffering in its own right; without real options, liking cannot be told apart from adaptation; and it fixes how goods may be pursued, by offering rather than imposing. In practice freedom means three conditions: a **floor** (basic security, so nobody likes something just to survive), a **menu** (real, visible alternatives) and an **exit** (leaving stays cheap at every point, including the internal exit of not acting on an urge). Freedom as a rule is argued, not modeled ([§8](#8-open-problems-and-falsifiers)).

### Permission, not obligation

Expansion is a good available to a person, never a standard to hold others to. This follows partly from the freedom rule and partly from the model: the condition for an expansion attempt to pay ([P3](../proofs/P3_expansion_worth_it.md)) fails whenever the horizon is short, the attempt is costly, or the person is under threat, so for many people at many times *not* expanding is correct. Guardrails that follow:

1. First person only: never a reason to pressure someone past their own boundaries.
2. Basic needs first: material security and safety come before taste work.
3. Curiosity-driven and reversible; expansion under pressure does not count.
4. "I don't like this" stays final in the moment, even if liking can change in principle.

### Other commitments

- **Expansion is derived, but special.** It matters only because it yields more pleasure, but, like health, it helps in almost any life whatever one's plans (what Rawls called a primary good). [P3](../proofs/P3_expansion_worth_it.md) makes "derived" exact.
- **Suffering is never good in itself, but choosing it can be.** People choose hardship that matters to them (grief, hard projects, sacrifice). Freedom permits the choice, and the balance counts what the hardship yields.
- **Causing is worse than allowing, but allowing still counts.** Failing to prevent suffering is bad, discounted by cost and distance. This position is provisional.

---

## 4. Sub-claims

### 4.1 Liking, not wanting

The good is expanding **liking** (the felt pleasure of having or doing something), not **wanting** (craving, the pull toward it). Wanting may be strong; the failure is when wanting, rather than liking, decides what one does.

Mechanism. Liking and wanting run on different systems: wanting on large, robust dopamine circuits that can sensitize into compulsion; liking on small, fragile "hedonic hotspots" (Berridge and Robinson 2016). The model treats wanting the way reinforcement learning does: a **cached prediction** of how good a source was, plus **incentive sensitization** that grows with use (following the form in Zhang et al. 2009).

What the model shows ([P7](../proofs/P7_wanting.md); [hx_p7.py](../model/hx_p7.py)):

- **Per-period loss (proved).** Even calibrated wanting misleads, because a cached prediction misses habituation (it overrates what was good last time) and misses renewal (it underrates what has recovered since).
- **Lock-in (proved).** With sensitization, the urge's favourite can lock in: it is chosen every period, its freshness goes to zero, and the loss approaches the full liking of the best alternative. This is addiction in the model: wanting rising while liking falls.
- **Urge surfing pays (simulated).** Letting the urge steer less often raised value in 1,499 of 1,500 random-world checks; the exception is real, where liking-greedy choice fails to rest its favourites (see [claim_types.md](claim_types.md)). The urge still arrives at full strength; it just doesn't steer. This matches Bowen and Marlatt (2009), where urge surfing left urges unchanged but reduced smoking. A general proof is open.
- **Cutting craving raises pleasure more than it evens life out (simulated).** In the combined model with an engineered feed present, going from full urge steering to none raised gross pleasure about 70% (about 45% in the default life, where value stays negative without calm) and cut suffering only slightly; about 90% of the gain was extra pleasure, from time moved off the feed onto skills that keep giving. Ups and downs stayed about the same size (pleasure varied a little *more*), while periods below zero fell from 7% to 1%. Two opt-in versions of *felt* craving extend this: if unmet urges are felt as tension, urge surfing alone keeps 70–90% of the gain and weakening the urge itself adds the rest; if sensitized wanting raises the reference point for a kind of good, craving makes pleasure fall over time and cutting it reverses the decline. Both sizes are invented. The growth figures are noisy and not monotone in steering, so the trend claims are weak ([hx_craving.py](../model/hx_craving.py)).
- **Expand or flatten? (simulated, sizes invented).** Contemplative traditions pair less craving with equanimity, which may even out liking, and some teachers claim liking grows more vivid. Coupling each to the drop in craving ([hx_equanimity.py](../model/hx_equanimity.py)): pulling liking toward its average is close to free (fewer disappointments offset lower highs, and choices shift only a little, toward curiosity-driven sources), and no amount of it cancels the gain from cutting craving. The real cost comes if indifference also makes choice careless: then full flattening gives back about two-thirds of the gain in the feed world, though it still beats craving-led choice everywhere tested, and in the default life careless choice actually helped by breaking up numbing habits. Calm (felt distress down) is the biggest addition under chronic distress (+1.1 net value, against +0.4 for 20% more vivid liking); without much distress, vividness adds slightly more. So in the model the package expands rather than flattens, but most of the expansion is from less craving and less distress, and only the untestable vividness claim makes liking itself grow.
- **Wanting's pace is the wrong pace.** Massed, urge-paced exposure keeps a new taste from forming ([hx_acquired_taste.py](../model/hx_acquired_taste.py); Galak et al. 2013 found people self-pace consumption too fast and enjoy it less).
- **Grabbing vs savoring.** The same pleasure used to escape distress (grabbing) rather than experienced when fresh (savoring) loses mainly by ignoring freshness, then turns compulsive as the urge grows ([P4c](../proofs/P4c_pleasure_relief_crossover.md); ablation in [hx_pleasure_relief_phased.py](../model/hx_pleasure_relief_phased.py)).

### 4.2 Baseline and reach

Baseline comes mostly from **conditions and relationships**: security, removal of stressors, and close, chosen company. Reach comes mostly from **skill, exposure, attention, and other people's tastes**. Solo practice (for example, training equanimity) belongs in every good plan, but in the model it is not the largest lever.

What the model shows:

- In the solo-versus-social model, some close, chosen company was optimal for 96% of simulated people, and the advantage came **mainly from shared relief** (lower suffering), with amplification, superadditive bundles and faster taste learning each adding little ([hx_social_vs_solo.py](../model/hx_social_vs_solo.py); [results](../results/hx_social_vs_solo.txt), T2). The size of shared relief is invented and decides the answer (T5: the social gain ranges from 1.8 with no shared relief to about 60 with strong relief). The direction is supported by social baseline theory (Coan and Sbarra 2015; Coan et al. 2006).
- Obligatory or non-close company was worth a fraction as much, and was optimal for far fewer people (62%). For people with low sociability, or whose relief comes from solitude, solitude was optimal ([hx_alone_vs_social.py](../model/hx_alone_vs_social.py)). This matches evidence that autonomy flips the effects of both company and solitude (Nguyen, Ryan and Deci 2018; Weinstein and Ryan 2010).
- Breadth mattered more than social versus solo: narrow lives (solitary, or dependent on one person) did worst; a broad social life beat a broad solo life on average only when ties relieve suffering *and* deepen over time, and its best size was 2–4 close people, not many ([hx_broad_social_vs_solo.py](../model/hx_broad_social_vs_solo.py)). This sits inside the innermost layer of social-network research (Dunbar 2020).

### 4.3 Weight effort by what binds

The more suffering binds, the larger the share of effort that should go to relieving it, but some effort always goes to expansion. This is a gradient, not a gate.

What the model shows:

- **Threshold (proved, myopic).** With relief that has less to do as suffering approaches zero, there is a unique distress level above which relief has the higher marginal value. The direct cost of suffering alone creates the threshold; numbing and blocked learning only lower it ([P4 Theorem 1](../proofs/P4_bottleneck.md)).
- **Gradient (proved, myopic).** With diminishing returns to each kind of effort, the optimal relief share is interior and rises smoothly with distress; splitting effort beat an all-or-nothing switch by up to 28% ([P4 Theorem 3](../proofs/P4_bottleneck.md); [hx_updates.py](../model/hx_updates.py)). This fits evidence that higher needs raise positive feeling even when lower needs are unmet (Tay and Diener 2011).
- **Three exceptions (proved, myopic).** When relief is nearly impossible (chronic pain), expansion becomes the lever. When expansion itself relieves (behavioral activation; Dimidjian et al. 2006), it can lead at every level. When stressors arrive faster than relief clears them, there is no "after the bottleneck": change the conditions, not the person ([P4 Proposition 4](../proofs/P4_bottleneck.md)). The last is the formal version of the quietism guardrail.
- **Which relief matters (proved + simulated).** Relief that preserves the capacity to like (security, rest, support, equanimity) beats numbing relief (avoidance, many drugs). Numbing is at best a bridge: one or two doses at acute distress, then clean relief. Habitual numbing locks into a loop exactly when the rebound is large relative to how fast relief and natural fading clear it, and with suffering that would fade on its own the loop is worse than doing nothing ([P4b](../proofs/P4b_numbing_loop.md)). This largely restates opponent-process theory (Solomon 1980; Koob and Le Moal 2001); the closed-form loop condition and the comparison with doing nothing are the additions.
- **Pleasure as relief (crossover proved).** Pleasure relieves suffering, but numbing stops it registering at high distress. Savoring out-relieves clean relief only below a distress level, so the simulated best policy has three phases: change conditions at high distress, relieve through savoring at moderate distress, expand at low distress ([P4c](../proofs/P4c_pleasure_relief_crossover.md)). That this three-phase policy is optimal is open.
- **Safety first for taste formation.** If distress lowers the chance of trying and of continuing after an unpleasant exposure, acquirable tastes become permanently missed, because a source filed as bad is never resampled ([hx_acquired_taste.py](../model/hx_acquired_taste.py); mechanism from Delaney, Jacobson and Moenig's "Preference Discovery").

### 4.4 Grow sensitivity and calm together

Expansion turns up the volume on everything. Without equanimity, more awareness means more pain, or numbing as a defense. Three skills matter, in order: **equanimity** (no push or pull, so aversive parts do not capture attention), then **concept release** (labels do not replace sensation), alongside **clarity** (noticing more).

What the model shows:

- **Resolution without calm backfires (simulated).** Finer resolution reveals aversive parts that averaging had hidden; without equanimity, a little resolution helps and a lot makes life worse ([results/hx_model_v1.txt](../results/hx_model_v1.txt)).
- **Which part of calm matters (proved).** Softening unpleasantness, however completely, does not protect resolution; releasing attention capture does. An aversive part that takes an attention slot costs the slot even at full equanimity ([refinement lemma (b)](../proofs/refinement_lemma.md); [hx_v1_variant.py](../model/hx_v1_variant.py)).
- **Categorizing is a numbing defense (simulated).** Expertise dulls emotional intensity because experts categorize (Rocklage et al. 2021, more than 700,000 consumers). Modeling categorization as dulling both pleasant and aversive parts reproduces this, and implies that dropping labels without equanimity makes things worse, while equanimity first and then concept release works best ([hx_v2_symmetric.py](../model/hx_v2_symmetric.py)). The "dulls both ways" assumption is weakly supported; see [§7](#7-objections-and-replies).
- **Arousal (simulated).** High arousal sharpens attention capture, so equanimity matters most when keyed up; moderate arousal was best even for people whose ideal is high; calm pleasure's longer carryover raised daily totals ([hx_arousal.py](../model/hx_arousal.py); [stimulation_challenge.md](../prior-art/stimulation_challenge.md); McManus et al. 2024).

### 4.5 Breadth and depth

Expansion goes **outward** to new things and **inward** to finer appreciation of familiar ones. Because liking is fractal, these are the same operation at different scales. It is not refinement toward one correct taste.

What the model shows:

- **Breadth is bounded under fixed time (proved).** With a fixed time budget, new sources mainly buy rest for old ones: the marginal gain falls like $1/n^2$ ([P2](../proofs/P2_breadth_bounded.md)). So breadth's distinctive job is **resilience and recovery time**, especially for novelty-based pleasures that recover only slowly, through forgetting ([P1, slow recovery](../proofs/P1_no_expansion.md)).
- **Depth raises the ceiling.** No amount of breadth exceeds $T \max_i \ell_i$; raising the best liking does. Depth applied to one source among many shrinks like $1/n$, so depth's edge is raising the ceiling, not escaping the time split ([P2, correction](../proofs/P2_breadth_bounded.md)).
- **Fractal liking moves the cap from time to attention.** Features of one activity do not compete for time the way activities do (one meal delivers flavour, texture, company and memory at once), so finer resolution can add routes without taking time from anything else ([hx_model_v1.py](../model/hx_model_v1.py)).
- **Resilience needs convex grief (proved).** Breadth buffers losses *only if* losing a larger share hurts disproportionately. With linear grief breadth gives no protection; with concave grief, as prospect theory suggests, breadth *raises* expected grief and bundling wins ([P5/P6](../proofs/P5_P6_grief_and_bundles.md)). A superadditive bundle beats spreading its strands iff its bonus exceeds a closed-form threshold that rises with the suffering weight, the loss risk and the number of strands.

### 4.6 Capacity and content

Both the **capacity** to like (openness, sensitivity, calm) and the specific **content** liked carry weight. Investing in capacity pays more than spending on the moment because routes to reach are open-ended. Content is where the ethics lives ([§5](#5-content-constraints)).

Expansion should target **activities, skills and capacities, not acquisitions or statuses.** Hedonic adaptation is near-complete for purchases and circumstances but small for intentional, varied, attention-demanding activities (Sheldon and Lyubomirsky 2006; Kahneman and Thaler 2006; Di Tella et al. 2010; [adaptation_by_domain.md](../prior-art/adaptation_by_domain.md)). With adaptation calibrated by kind of good, an added skill-building source *grew* in value over time while an added purchase kept about 14% of its early gain; a social addition modeled as a fixed status adapted away, while the same addition modeled as varied activity kept about half ([hx_adaptation_ladder.py](../model/hx_adaptation_ladder.py); [results](../results/hx_adaptation_ladder.txt), E1 and E7). Relationships last as varied shared activity more than as a status.

Without any expansion, what happens to a fixed set of sources depends on their type: depleting sources go to zero, renewing ones settle at a positive level, and skill-building ones rise if skill growth outpaces habituation ([P1](../proofs/P1_no_expansion.md)). So "expansion is necessary for lasting well-being" is true only for a life running on depleting pleasures; for renewing ones, expansion is an improvement, not a rescue.

### 4.7 Borrow practices, not metaphysics

A practice from any tradition counts if its mechanism (attention, appraisal, state, social context) works without the belief, and it passes the content constraints. Examples: equanimity toward pain and urges (Buddhist "second arrow"); deliberate delight in others' good fortune (*mudita*); a weekly break from production; brief imagined loss to counter adaptation (mental subtraction); scheduling pleasant activities before motivation arrives (behavioral activation). Rebirth, karma, cessation as a goal, and causal claims for ritual are dropped. Evidence that ritual can survive disbelief: open-label placebo helped patients who knew the pills were inert (Kaptchuk et al. 2010). This sub-claim is argued, not modeled.

### 4.8 Meaning works mainly as quieting

Is meaning a pleasure, or a way of quieting suffering? The evidence favors quieting. In a daily-diary study (N≈1,949), purpose cut the rise in negative affect on stressor days by about 36% and left the positive-affect response unchanged (Hill et al. 2018); meaning-centered therapy reduced depression and hopelessness against an active control (Breitbart et al. 2015); and purpose relates strongly to how much pain interferes with life but weakly to its severity. In the theory's terms (suffering = pain × resistance), meaning lowers resistance, not pain. Meaning also appears to slow adaptation, by keeping attention engaged, and contributes only a small direct pleasure (King et al. 2006 show mood feeding meaning *judgments*, not the reverse). Two splits matter: having meaning quiets, while searching for it carries a small cost; and the meaning of a stimulus (harm or relief) can change pain intensity itself, a different mechanism from life purpose.

The model separates the accounts by their signatures: quieting's benefit is zero without suffering and grows with it; attention's is constant; pleasure's is small and constant; and the extra stress exposure of meaningful lives (Baumeister et al. 2013) is a cost. With all four on, the model reproduces the puzzle that meaningful lives contain *more* bad periods yet are better overall. Meaning and equanimity partly substitute, since both lower resistance. This gives "meaningful suffering" a hedonist reading: chosen hardship isn't good in itself; meaning makes it hurt less. See [hx_meaning.py](../model/hx_meaning.py) and [meaning.md](../prior-art/meaning.md).

### 4.9 Building over a finite, uncertain life

Expansion trades pleasure now for capacity later, so it depends on how a life is valued and how long it lasts. The life-span model compares four ways of aggregating a life (total; total with extra weight on the worst moments; peak-end of the whole life; peak-end of each year, summed), with and without pure time discounting, and three ways of blocking the conclusion that a long dull life beats a short intense one. Across all 24 combinations, building capacity when young and spending when old is optimal; the rule changes *when* to switch, not *whether* to build. Uncertainty about one's own hazard type barely matters (regret ≤ 2% against knowing it), except when death comes early: a policy chosen under uncertainty loses about 18% if death comes at 50 (4% under yearly peak-end). Payoff speed matters more: expansion that pays early is the hedge against a short life. Totals and yearly peak-end behave sensibly; whole-life peak-end ignores duration and isn't additive. Counting boredom and unmet needs as suffering is enough to block the long-dull conclusion (a dull life is net negative, so length makes it worse), while a calm, meaningful long life can still win. See [hx_lifespan.py](../model/hx_lifespan.py).

### 4.10 Fear of death is one more stressor, best met by practice

Fear of death fits the theory as distress by resistance: death salience hurts in proportion to how much one resists it, captures attention, and competes with pleasure for time. The model treats it that way and asks which response pays over a whole life. It is calibrated to the literature in [death.md](../prior-art/death.md): dread peaks in the 20s and declines with age (Russac et al. 2007); exposure-style therapy moves death anxiety much more than nonspecific practice (Menzies et al. 2018, from few trials, so discounted); suppression is followed by a small delayed rebound (Arndt et al. 1997; the downstream mortality-salience effects failed to replicate in Many Labs 4); and finitude raises savoring only under vivid or reflective framing (Cozzolino et al. 2004; Frias et al. 2011; O'Brien & Ellsworth 2012).

Four results, robust across suffering weights, skill decay rates and age profiles of dread:

- **Some practice usually beats none (87% of nearby settings), and a mix beats either kind alone at default settings (only 40% of nearby settings; it needs learning fast relative to skill decay, see [claim_types.md](claim_types.md)).** Alternating general equanimity with death-specific practice (death reflection, Epicurean argument, *maraṇasati*) was the best policy in 68 of 72 settings (with or without setting dread aside), against either practice alone at the same time cost. General calm covers ordinary distress too; death-specific practice learns faster on its target and, through reflection, adds some savoring.
- **Start early; practicing only during spikes barely pays.** Starting at 20 was worth roughly five times starting at 50, and an equal slot budget spent only when dread was high returned a third or less as much, because calm is hard to learn while distressed.
- **Whether death-specific practice beats general practice depends on two contested numbers:** how much of one's distress is about death, and whether facing finitude really raises savoring. With no savoring effect it loses to general practice; with a moderate one it wins clearly.
- **Setting dread aside outside practice helps only if it works.** Suppression on its own was the best policy in only 1 of 72 settings. Practicing and otherwise setting dread aside beat practicing alone when setting aside cut felt dread by about 30% or more; below that, the rebound and the loss of natural habituation made it worse. Focused distraction plausibly clears that bar; plain thought suppression probably doesn't.

This gives a hedonist reading of an old aim (Epicurus, the Stoics, Buddhist death contemplation): overcoming fear of death is worth pursuing because the fear is suffering, not because dying is unimportant; and the best route is ordinary skill-building, started early and kept up, with some deliberate contemplation of finitude in the mix. See [hx_death.py](../model/hx_death.py).

### Limits on expansion

- **Sensors.** Genetic differences change the experience itself (bitterness sensitivity; cilantro tasting soapy). People can learn to like such things, but the experience stays different.
- **Gates, not brakes.** Disgust acts less like a brake to be released and more like a gate on what may come close. It tends to open rather than flip into liking, opens for valued people, and can close again under stress.
- **Real harm.** Benign masochism (liking chili burn, horror, sad music; Rozin et al. 2013) needs the "benign." Nausea and visceral pain are never enjoyed. "Liking" real danger means misjudging it as safe.
- **Add, don't erase.** New associations can be learned on top of old ones; attempts to remove core preferences fail and harm.
- **Return on investment.** Yield is high and cost low for activities, contexts, sensory and aesthetic tastes, genres and cuisines; yield is low and cost high for core disgust and deep aversions. Spacing matters: space exposures more widely the more aversive the start, and prefer complex targets, which are slower to acquire but far longer-lasting ([hx_acquired_taste.py](../model/hx_acquired_taste.py)).

---

## 5. Content constraints

Not every new liking is good: learning to enjoy cruelty is expansion too. These tests separate good expansion from bad. They do not assume that value exists independently of liking; content matters through its effects on pleasure and suffering, one's own and others'.

| Constraint | Test | Why it matters | What the model says |
| --- | --- | --- | --- |
| **Non-rivalrous** | Does the liking require someone else's loss? | Rules out cruelty, schadenfreude and status-taste. *Mudita* (delight in others' good) is the model case. | In a twelve-person model, envious agents ($\kappa < 0$) lowered welfare for everyone around them, not just themselves ([hx_social.py](../model/hx_social.py), S4). |
| **Renewal** | Does returning regenerate the pleasure or use it up? | Skilled pleasures deepen; novelty-based ones recover slowly, through forgetting. Moving attention from the surprise to the craft can turn a depleting pleasure into a renewing one. | Load-bearing: it decides which regime of [P1](../proofs/P1_no_expansion.md) a life is in. Complex sources keep about 94% of peak liking after 600 exposures versus 49% for simple ones ([hx_acquired_taste.py](../model/hx_acquired_taste.py)). |
| **Skill slope** | Does repeated engagement build capacity? | Pleasures that build skill keep paying; others plateau. | Skill pleasure ends higher than it started only if skill growth outpaces habituation, so it needs rest ([P1 sharpening](../proofs/P1_no_expansion.md)). Learning-progress sources held up best under a moving reference point ([hx_yield_reference.py](../model/hx_yield_reference.py)). |
| **Liking, not wanting** | Is there strong liking with a natural stopping point? | Separates taste from compulsion. Addiction is wanting rising while liking falls. Every pleasure also trains future desire, so ask what it teaches one to want. | Lock-in proved ([P7](../proofs/P7_wanting.md)); grabbing loses mainly by ignoring freshness ([P4c](../proofs/P4c_pleasure_relief_crossover.md)). |
| **Not adaptive** | Would one still like it if better options were available? | Elster's "sour grapes" test: learning to like what one is stuck with is adaptation, not expansion. | A related test for tastes acquired through a relationship ("does the taste outlast the relationship?") is valid, but only after grief settles; measured early, real expansion looks like adaptation ([S3](../proofs/S_social.md)). |
| **Reflective endorsement** | Would one endorse it with full information? | Mill's "competent judge" test, without his ranking of higher over lower pleasures. | Not modeled. |
| **Resolution counts** | Does it sharpen discrimination within something already liked? | Depth is expansion too, not only breadth. | Resolution pays only when aversive parts cannot capture attention ([refinement lemma](../proofs/refinement_lemma.md)). |

**Telling liking from wanting from the inside.** Collecting new experiences can feel like growth while being craving. Useful questions: does getting it bring joy, or only relief? Is there a natural stopping point? Does returning renew it? Is it still fresh, or is one going back after the liking has dropped? In the model, ignoring freshness was the largest single cost of grabbing. Riding an urge out is a working test: if it passes and nothing is missed, it was wanting or relief; if a calm wish to do the thing remains, it is liking.

**The tests cut both ways.** A dislike that tracks real harm (cruelty, manipulation) is accurate and protective. A dislike that is only resistance to an unfamiliar signal can loosen.

**Indirect harm counts.** A liking harmless in the moment can still cause suffering upstream (for example, through exploitative supply chains). That counts against it, discounted by distance like any harm allowed rather than caused.

---

## 6. Relationship to hedonism and to prior work

### Within hedonism

Hedonic expansionism is not a rival to hedonism. It is a claim about **strategy and capacity** within it: if a life goes well as pleasure exceeds suffering over its length, then the capacity to enjoy matters as much as current enjoyment, and expanding liking is the most robust way to grow that capacity.

It uses a **hybrid account of pleasure**. On the felt-quality view, pleasure is a feeling (the brain's liking response). On the attitudinal view (Feldman 2004), pleasure is taking pleasure *in* something. Expansion fits the hybrid: liking is the feeling, and expansion multiplies the objects it can attach to. The hybrid also handles the heterogeneity problem (chili, jazz and friendship feel nothing alike), which expansionism depends on.

What it **inherits** from hedonism: the experience machine (answered by judging real technologies by the same content tests rather than by thought experiments that assume away tolerance and runaway wanting), the heterogeneity of pleasures, and the measurement and interpersonal-comparison problems.

What it **adds**: capacity for pleasure as a target, not only the amount now; content tests that judge pleasures by their effects; the line between liking and wanting as the line between good and bad expansion; and expanding *whose* pleasure registers as one's own.

### Intellectual lineage

| Tradition | What expansionism takes | Where it departs |
| --- | --- | --- |
| Ancient hedonism (Cyrenaics, Epicurus) | Pleasure as the good; the katastematic/kinetic distinction | Epicurus prunes desire and peaks at relief; expansion keeps growing liking |
| Modern hedonism (Bentham, Mill, Sidgwick, Feldman) | Mill's cultivated pleasures and competent judges; Feldman's attitudinal pleasure | Mill ranks higher over lower; expansionism does not |
| Philosophy of taste (Hume, Dewey) | Hume's recipe for delicacy: practice, comparison, freedom from prejudice; Dewey's aesthetic in ordinary experience | Hume seeks a standard of correct taste; expansion goes outward, not toward correctness |
| Self-cultivation (Aristotle, Nietzsche, Hurka, Nussbaum and Sen) | Pleasure completing activity; capabilities for senses, imagination and play | Perfectionism makes cultivation a duty; here it is permission |
| Contemplative traditions (Buddhism, Stoicism, Taoism, Indian *rasa*) | Clarity plus equanimity; enjoying without grasping; *mudita* | Most aim at liberation, not more pleasure |
| Psychology of pleasure (Berlyne, Scitovsky, Zajonc, Rozin, Berridge, Bryant) | Inverted-U novelty; skilled consumption; mere exposure; acquired tastes; liking versus wanting; savoring | Descriptive; expansionism adds the normative claim |
| Growth psychology (Maslow, Aron, Fredrickson, Csikszentmihalyi) | Growth versus deficiency motivation; self-expansion; broaden-and-build; flow | Focus on the person, not on taste as such |
| Sociology of taste (Bourdieu, Peterson, Saito) | Taste as social; the cultural omnivore; everyday aesthetics | Bourdieu treats taste as distinction; expansion aims to drop the ranking |
| Critics and economics (Elster, Sen, Nussbaum; Stigler and Becker; Bowles) | Sour-grapes test; consumption capital; endogenous preferences | Supplies the guardrails rather than the thesis |

### Closest prior work on the philosophical thesis

One round of search, moderate confidence:

- **Breadth without hierarchy** is already argued in aesthetics: Irvin (2008) on everyday aesthetic experience; Lopes, Nanay and Riggle, *Aesthetic Life and Why It Matters* (2022); Riggle's "volitional openness" to new aesthetic value, the closest thing to an expansion norm. None claims more breadth is itself better *for* a person, and the leading aesthetic pluralists defend aesthetic life on non-hedonic grounds. The hedonic framing is a real point of difference.
- **Liking over wanting as the normative line** is suggested descriptively by Kringelbach and Berridge (2009) but not, as far as found, proposed as a normative principle.
- **Effects-based content constraints** are partly anticipated by adaptive-preference work (Elster, Sen, Nussbaum) and by Irvin; Kagan (2009), "Well-being as enjoying the good," is the realist rival.
- **Expanding whose pleasure counts** is argued separately for compersion (Brunning 2020) and *mudita* (Walter et al. 2024), but not tied to a theory of taste.
- Related: Callard, *Aspiration* (2018), on rationally coming to value what one does not yet value; Bykvist (2010) on the bootstrapping objection to changing one's own preferences.

### Prior work on the formal model

From [prior_art.md](../prior-art/prior_art.md) and [evolution_cognition.md](../prior-art/evolution_cognition.md). Most single components already exist:

| Model part | Status | Closest work |
| --- | --- | --- |
| Freshness decay and recovery; renewing, depleting and skill sources ([P1](../proofs/P1_no_expansion.md), [P2](../proofs/P2_breadth_bounded.md)) | Restatement | Galak, Kruger and Loewenstein 2013; Nelson, Meyvis and Galak 2009; Stigler and Becker 1977 |
| Acquired taste ([hx_acquired_taste.py](../model/hx_acquired_taste.py)) | Restatement, calibrated | Berlyne's two-factor model via Szpunar, Schellenberg and Pliner 2004; Zajonc 2001; Wardle et al. 2003 |
| Numbing loops and rebound ([P4b](../proofs/P4b_numbing_loop.md)) | Largely a restatement | Solomon 1980; Koob and Le Moal 2001; Baker et al. 2004; Hayes et al. 1996 |
| Wanting as cached value plus sensitization; lock-in ([P7](../proofs/P7_wanting.md)) | Mostly done | Zhang et al. 2009; Redish 2004; Bowen and Marlatt 2009 |
| Interdependent utility; empathy versus compassion ([S1–S2](../proofs/S_social.md)) | Standard form | Bergstrom 1999; Klimecki and Singer 2017 |
| Bottleneck ([P4](../proofs/P4_bottleneck.md)) | Partly done; strict version contradicted | Bogdan and Pizzagalli 2006; Lenow et al. 2017; Tay and Diener 2011 |
| Fractal liking ([refinement lemma](../proofs/refinement_lemma.md)) | No formal precedent; evidence pushes back | Rocklage et al. 2021; Stuppy and van den Bergh 2022 |
| **Pleasure-as-relief crossover** ([P4c](../proofs/P4c_pleasure_relief_crossover.md)) | **Not found; likely new** | Each arm supported separately: Fredrickson and Levenson 1998; Bogdan and Pizzagalli 2006 |
| **Breadth buffers only under convex grief; bundle threshold** ([P5/P6](../proofs/P5_P6_grief_and_bundles.md)) | **Conditional result not found; likely new** | Resolves the split between Thaler 1985 (concave, integrate losses) and Linville and Fischer 1991 (renewable resources, separate losses); may explain weak self-complexity findings (Rafaeli-Mor and Steinberg 2002) |
| **The integrated model** | **No combined model of acquired taste and capacity for pleasure found** | — |

### What is likely novel

1. The thesis itself as a normative claim within hedonism: that capacity to like is a central derived good, bounded per moment and open-ended in routes, with liking-not-wanting as the line between good and bad expansion.
2. The pleasure-as-relief crossover and the three-phase relief policy.
3. The result that breadth buffers loss only under convex grief, with an explicit bundle threshold.
4. The integration: one model linking adaptation, acquired taste, attention and equanimity, suffering and relief, wanting, and the social axis.

---

## 6b. Robustness: what survives when the mechanisms interact

Each result above comes from a separate toy model with its own invented parameters. [hx_combined.py](../model/hx_combined.py) puts the mechanisms into one model with a single shared parameter set (literature-calibrated where the prior-art notes allow) and retests the headline claims. Of eleven claims, six hold, four weaken, and one flips.

| Claim | In the combined model |
| --- | --- |
| Breadth has bounded returns; its job is resilience | Holds |
| Equanimity before concept release | Weakens: under ordinary distress either helps; under chronic distress the two are strongly complementary, but order barely matters |
| Relief-first gradient, three phases with savoring | Weakens: any relief beats none, but the gradient ties all-or-none and the savoring phase adds nothing |
| Habitual numbing is worse than nothing when suffering fades | Holds |
| Letting the urge steer less helps | Holds |
| Salience bias is the main cause of underuse | Flips: sensitization and cached wanting that never sees a skill's gains matter more |
| Spacing decides whether a taste is acquired | Holds |
| A few close people beat broad solo for an average person; solitude for low sociability | Holds, with smaller margins; the edge comes from close ties renewing better, not from spreading loss risk |
| Taking turns beats compromise | Holds (in a simplified two-person version) |
| Skill, sensitizing and relief expansion lasts; material fades | Holds |
| Moderate arousal best; high arousal worst without equanimity | Holds, weakly |

**A default life versus one following the recommendations together** differs by a large margin, and about 70% of that gap comes from one mechanism: avoiding numbing loops (and the engineered feed). Three interactions matter for the theory. First, liking-driven choice still numbs, because numbing's immediate relief is genuinely liked; an explicit rule against habitual numbing is needed, and it is the biggest single lever. Second, planning can backfire: scheduling skill and sensitizing sessions crowded out curiosity-driven choice, which already found those sources. Third, time spent on equanimity practice paid off only under chronic distress, where both calm skills were needed together. The combined model is itself a toy, and its gap depends heavily on including a numbing source; see its caveats in the script docstring.

**Assumption checks** ([hx_assumption_checks.py](../model/hx_assumption_checks.py)). The verdicts survive varying the suffering weight from 1 to 5 (except the small social edge, gone at 5) and letting pain adapt more slowly than pleasure, which raises relief's value as a floor by up to 45%. With the calm skills made costly to build and slow to keep, their order matters again, in opposite directions: equanimity first under chronic distress, concept release first under ordinary distress; and practicing only when distressed never pays. The null result for the savoring phase is a test artifact: in the model, savoring relieves distress in every phase, so a separate savoring phase only pauses expansion.

## 7. Objections and replies

### Standard objections

| Objection | Reply | What the model says |
| --- | --- | --- |
| Traditions say to contract desire (Epicurus, the Stoics, ascetics). | They target wanting and grasping, not liking. Their shared move, "enjoy without needing," is kept. | Wanting-driven choice loses value even when calibrated ([P7](../proofs/P7_wanting.md)). |
| Learning to like cruelty is expansion too. | The content constraints rule it out: non-rivalrous, trains good desire. | Envy and rivalrous liking lower group welfare ([hx_social.py](../model/hx_social.py)). |
| People learn to like deprivation (adaptive preferences). | Sour-grapes test plus basic needs first: expansion builds on secure conditions and never replaces changing bad ones. | When stressors outpace relief, the optimum is to change conditions ([P4 Prop. 4.3](../proofs/P4_bottleneck.md)). |
| Depth, not breadth, is real connoisseurship. | Resolution counts as expansion. | Depth raises the ceiling; breadth does not ([P2](../proofs/P2_breadth_bounded.md)). |
| Liking is a fixed evaluator. | The hotspots are fixed; the routes to them (appraisal, attention, association) are not. Expansion builds new routes to the same liking systems. | — |
| Equanimity would flatten taste (horror stops working). | Expert meditators rate pain as just as intense but less unpleasant (Lutz et al.): the signal stays and the added resistance goes. | Equanimity that releases capture lets resolution keep paying ([refinement lemma](../proofs/refinement_lemma.md)). |
| Some things cannot be learned (disgust, sensors). | Granted. Gates open rather than flip; handled by weighing cost against payoff. | Strong aversion was only marginally worth acquiring even over long horizons ([hx_acquired_taste.py](../model/hx_acquired_taste.py)). |
| Expansion becomes consumption. | Liking not wanting; sample rather than buy; renewal and skill slope. | Purchases adapt away ([hx_adaptation_ladder.py](../model/hx_adaptation_ladder.py)). |

### Objections where the model shows the objection partly lands

**Expertise numbs.** Rocklage et al. (2021) found, across more than 700,000 consumers, that expertise *lowers* emotional intensity, and Stuppy and van den Bergh (2022) found that sampling across quality polarizes enjoyment. The naive "finer resolution means more pleasure" is false. The theory's reply splits resolution in two: perceptual resolution while attending, and evaluative categorization. Only the first is expansion, and it needs the categorizing classifier turned off, which is what restored emotion in Rocklage's experiment. The model reproduces "expertise numbs" only by assuming categorizing dulls both pleasant and aversive parts, and the evidence that labels dampen *positive* feeling is thin and partly contrary (Lieberman et al. 2007 is about negative affect; one unreviewed poster found amplification). Explanation, not labeling, may be the better mechanism (Wilson and Gilbert 2008). The model also **failed** to reproduce Stuppy and van den Bergh's polarization under any principled judging rule, and its judging mechanism breaks the refinement lemma ([refinement lemma, notes on v2](../proofs/refinement_lemma.md)). This part of the model is probably wrong in detail.

**A strict bottleneck.** The original claim was lexical: relieve suffering first, then expand. Tay and Diener (2011) found that higher needs raise positive feeling regardless of whether lower needs are met, and behavioral activation is as effective as antidepressants for depression (Dimidjian et al. 2006). The theory conceded: with diminishing returns the bottleneck is a gradient, and expansion can lead when it also relieves ([P4](../proofs/P4_bottleneck.md)). Different kinds of suffering numb and block differently (Bogdan and Pizzagalli found threat, but not negative feedback, blunted reward learning); the model still has one scalar suffering.

**Breadth and loss.** "Breadth makes you resilient" is a common intuition, but the empirical anchor is weak: a meta-analysis found a small average *negative* correlation between self-complexity and well-being (Rafaeli-Mor and Steinberg 2002), and prospect theory implies that pain is concave in loss size, so losses should be bundled (Thaler 1985). The model shows the intuition holds only under convex grief and that under concave grief breadth raises expected grief ([P5/P6](../proofs/P5_P6_grief_and_bundles.md)). Which shape holds is empirical and may differ by domain.

### The strongest objection: reference-dependent adaptation

**Objection.** Evolved pleasure is relative. Utility is scaled to the range of options an organism meets, like a voltmeter (Robson 2001), and the optimal reference point tracks expected outcomes, so happiness is mean-reverting (Rayo and Becker 2007). If so, expansion gets recalibrated away: one's reference point rises to meet whatever is added, and mean experience reverts.

**Reply.** The thesis already concedes a ceiling per moment; it never claims average experience can rise without limit. Under bounded, reference-dependent utility, expansion can still pay through (a) more time above a moving reference, (b) learning-progress pleasure that renews while learnable structure remains (Schmidhuber 2010; Gottlieb et al. 2013), (c) resilience when a source is lost, and (d) set points that can move (Diener, Lucas and Scollon 2006). Because pain adapts less than pleasure (Perez-Truglia 2012), reducing suffering is the more durable gain, which supports weighting effort toward relief when suffering binds.

**Where the model shows it partly lands.** Adding a moving reference point to the model ([hx_yield_reference.py](../model/hx_yield_reference.py); [results](../results/hx_yield_reference.txt), E2):

| Adaptation $\phi$ | No expansion | Acquire new tastes | Learning-progress source |
| --- | --- | --- | --- |
| 0 (none) | 1.10 | 1.37 | 1.58 |
| 0.5 | 0.60 | 0.73 | 0.87 |
| 0.8 | 0.27 | 0.31 | 0.42 |
| 1 (full treadmill) | 0.05 | −0.01 | 0.07 |

Expansion's value shrinks as adaptation becomes complete, and **vanishes under the full treadmill**, where acquiring tastes even costs slightly (the early unpleasant exposures). So the theory **needs adaptation to be partial**. How complete adaptation is, by kind of good, becomes the central empirical question for the whole theory. The literature suggests it is partial for exactly the goods the thesis now targets: intentional activities adapt little over 12 weeks while circumstances adapt fully (Sheldon and Lyubomirsky 2006), and adaptation runs through attention moving away (Kahneman and Thaler 2006). With per-kind adaptation calibrated from that literature, skill-building and sensitizing sources kept paying and purchases faded ([hx_adaptation_ladder.py](../model/hx_adaptation_ladder.py), E7). But the sensitivity run shows the dependence plainly: if skill and social sources adapt as fully as purchases ($\phi \to 1$), their late gain turns negative (E6). Under strong adaptation, **continuing change** (learning progress) keeps experience above the reference better than a larger stock of liked things, which reframes expansion as a process more than an accumulation. Relief stays a floor, but that result is built in by assuming relief is not adapted away.

### The strongest philosophical objection: evolutionary debunking

**Objection.** Beliefs that pleasure is good and pain bad are among the easiest evaluative beliefs to explain away in evolutionary terms (Street 2006; Kahane 2011, 2014). Pleasure was shaped as a fitness signal, not a goal; deliberately expanding liking is "hacking the gauge."

**Reply.** Several replies exist, none decisive. (1) The genetic-fallacy reply: why a capacity exists does not settle what it is worth now. (2) Introspective access: pleasure's goodness is read off the experience by a reliable process, not inferred, so it is not exposed to debunking (Sinhababu 2023). (3) Selection had no need to install a *belief* that pleasure is good, since the feeling already motivates (de Lazari-Radek and Singer 2014); Jaquet (2018) finds this reply weak, because the belief could be a by-product. (4) Retreat to a subjective or attitudinal account, which is immune to debunking but gives up objectivity (Jaquet 2018); the theory's hybrid account of pleasure leaves this route open.

The signal view also cuts the other way: decoupling liking from fitness is exactly what a hedonist who values experience over fitness should want, *provided* expansion does not disable suffering's warning function (Nesse and Berridge 1997). That adds a guardrail: an intervention that numbs warning signals carries an expected-harm cost.

**Where it lands.** The model is a normative model with descriptive dynamics. Its welfare function needs no evolutionary justification, but its suffering weight $\lambda$ cannot be justified by loss aversion either; it has to be defended as an ethical choice. The debunking objection is not modeled and remains open.

### Second-order risks

- **Quietism:** "learn to like it" replacing "change it." Guarded by basic needs first and by [P4 Proposition 4.3](../proofs/P4_bottleneck.md).
- **Coercion:** "you just haven't tried it" as pressure, including in intimate contexts. Guarded by permission, not obligation, and "I don't like this" as final in the moment.
- **Commodification:** markets selling experience-collecting as expansion.
- **Status:** breadth becoming cultural capital (Peterson's omnivore).
- **Relationship pressure:** "expand for me." A close other's invitation can be one of the best routes to new liking; a demand fails the permission rule.

---

## 8. Open problems and falsifiers

### Falsifiers

The theory should be held like a claims register. Any of these would count against it:

| Falsifier | Bears on | How it could be tested |
| --- | --- | --- |
| Cultivated likings turn out less durable or less liked than native ones. | Thesis; acquired taste | Long-run follow-up of exposure studies (persistence after Birch 1980-style interventions was not reported) |
| Expansion reliably drags wanting up with it (more craving, not more liking). | 4.1; liking-not-wanting constraint | Separate wanting and liking measures (as in Ihssen and Wadsley 2021) before and after taste acquisition |
| Broader taste predicts *lower* well-being once wealth and openness are controlled. | Thesis; 4.5 | Panel data with taste-breadth measures |
| Expanded tastes accelerate adaptation instead of renewing, or adaptation to activities is as complete as to circumstances. | 4.6; strongest objection | Experience sampling: if expansion only shifts the reference point, affect rises transiently and then reverts ([hx_yield_reference.py](../model/hx_yield_reference.py), E2) |
| Grief from loss is concave in the share of pleasure lost. | Resilience defense | Then breadth raises expected grief ([P5d](../proofs/P5_P6_grief_and_bundles.md)) |
| Pleasure relieves suffering *best* at high distress. | 4.3 | Contradicts the crossover ([P4c](../proofs/P4c_pleasure_relief_crossover.md)) |
| Shared relief from close ties is small. | 4.2 | Most of the modeled social advantage disappears ([results](../results/hx_social_vs_solo.txt), T5) |
| Liking strength is bounded through both depth and discovery. | Open-endedness | Then reach is bounded too ([P2](../proofs/P2_breadth_bounded.md)) |

### Testable predictions the model makes

- Expansion practices work better once distress is low; relief raises positive feeling most in the *most* distressed only if numbing is concave or threshold-like ([P4 Proposition 2](../proofs/P4_bottleneck.md)).
- Urge surfing reduces acting on urges before it reduces urges; urges fall later only through disuse ([P7](../proofs/P7_wanting.md)).
- Spaced exposure acquires tastes that massed exposure does not, and the best spacing widens as initial aversion rises ([hx_acquired_taste.py](../model/hx_acquired_taste.py)).
- Whether a taste learned through a relationship outlasts it can be read reliably only after grief settles ([S3](../proofs/S_social.md)). No study of this was found.
- Calm pleasant episodes keep their lift longer than excited ones; enjoyment per item falls as switching rate rises ([stimulation_challenge.md](../prior-art/stimulation_challenge.md)).

### Open problems in the model

- **Optimality.** The three-phase relief policy as an optimal policy needs the full dynamic program ([P4c](../proofs/P4c_pleasure_relief_crossover.md)). The bottleneck theorems are proved only for the one-period (myopic) rule ([P4](../proofs/P4_bottleneck.md)). A general proof that letting wanting steer less always helps is open, and may be false, since a noisy urge could help by spacing uses ([P7](../proofs/P7_wanting.md)).
- **Magnitudes.** Every magnitude depends on invented parameters. Shared relief, the moving reference point's completeness, the grief shape and the suffering weight are the parameters that most change conclusions ([assumptions.md](assumptions.md)).
- **Typed suffering.** Different kinds of suffering numb and block differently; the model has one scalar.
- **Model changes suggested by prior art and not yet made:** valence-specific adaptation (pain adapting more slowly than pleasure); an intensity-dependent suffering weight swept from 1 to 5; learning-progress pleasure so that "complex sources renew longer" is derived rather than assumed; a source-specific wanting–liking gap, with lock-in less likely as alternatives improve; attention capture that rises with distress; and "explanation release" in place of symmetric label dampening ([evolution_cognition.md](../prior-art/evolution_cognition.md)).
- **Freedom as a rule.** Whether floor, menu and exit rules win in a multi-agent setting where agents cannot see each other's likings is untested.
- **Equanimity's cost.** The model treats calm as a parameter, not as something acquired at a cost.

### Open value questions

- **Weighing people.** A floor for everyone, designing rivalry away, and weighting suffering heavily are settled. The rule for conflicts that remain is not (fair bargaining in small groups? extra weight for the worse-off at scale?).
- **How steep the discount on allowing suffering is.**
- **Children:** how to widen a child's menu and invite expansion when they cannot yet fully choose.
- **Invitation versus manipulation:** a process rule (chosen, sampled or reversible, curiosity-driven, running on liking, routed through the real world) covers most cases; whether transparency is also required is open.
- **Self-reference:** liking is both what is expanded and what it is judged by, so transformative experiences and engineered liking need a meta-rule.

### Open empirical questions

- How complete adaptation is, by kind of good: the key question for the whole theory.
- Measurement: how to track liking, not consumption, over time, and how to compare liking across people.
- Whether the per-moment ceiling can itself be raised by training, and whether attention bandwidth is trainable.
- Whether domains really differ in "fractal dimension," and how it could be measured (for example, from how expert vocabularies grow).
- Pace: how fast expansion should go, and how it varies by person.
- What fiction and consensual intense experiences train in the people who enjoy them.
- Whether individual expansion thins traditions that depend on depth (cultural homogenization).
- Which features make engineered pleasures (companions, neurotechnology, recommendation feeds) pass or fail the content constraints.
