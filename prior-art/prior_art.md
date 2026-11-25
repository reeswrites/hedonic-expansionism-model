# Prior-art check: toy formal model of "hedonic expansionism"

Date: 2026-11-24. Method: web search, then fetches of abstracts, publisher pages and PDFs. PubMed and PMC pages mostly returned a reCAPTCHA wall, so for those papers I used OpenAlex, publisher pages, lab PDFs, or secondary reviews. Papers I could **not** read directly are marked **[not read]**. Anything marked **[memory]** comes from background knowledge and was not checked this session. Treat it as a lead, not a citation.

Verdict key: **Yes** = the work already contains the model's result; **Partly** = it has the mechanism or a close version; **No** = it lacks the result or cuts against it.

---

## 1. Freshness/adaptation, breadth with bounded returns, renewing / depleting / skill-building sources

| Work | Has result? | What it gives the model |
|---|---|---|
| Galak, Kruger & Loewenstein (2013), "Slow Down! Insensitivity to Rate of Consumption Leads to Avoidable Satiation," *JCR* 39(5):993-1009. https://ideas.repec.org/a/oup/jconrs/doi10.1086-666597.html | **Yes** for freshness decaying with use and recovering with rest | Longer gaps between episodes slow satiation, but people don't anticipate this. People who chose their own consumption rate enjoyed it *less* than people given a slower rate. This is direct empirical support for the model's "grabbing ignores freshness" (item 5). |
| Nelson, Meyvis & Galak (2009), "Enhancing the Television-Viewing Experience through Commercial Interruptions," *JCR* 36(2):160-172. https://ideas.repec.org/a/oup/jconrs/doi10.1086-597030.html | **Yes** (short timescale) | Interruptions disrupt adaptation and raise enjoyment, even though people say they prefer no interruption. The effect disappears for stimuli that don't produce adaptation. This supports making freshness source-specific. |
| Galak, Redden & Kruger (2009), "Variety Amnesia: Recalling Past Variety Can Accelerate Recovery from Satiation," *JCR* 36(4):575-584. https://ideas.repec.org/a/oup/jconrs/v36y2009i4p575-584.html (title confirmed; abstract via Galak's talk summary, https://marketing.wharton.upenn.edu/wp-content/uploads/2016/10/GalakTitleAbstract.pdf) | **Partly**; complicates the model | Recovery from satiation depends partly on *perceived* time and *perceived* variety. A pure physical decay/recovery clock is therefore an approximation. |
| Redden (2008), "Reducing satiation: the role of categorization level," *JCR* **[not read; known only from a secondary abstract]** (Kaefring 2013 summary). | **Partly** (bears on item 2) | Sub-categorizing consumption (for example "Chinese" or "Italian" meals instead of "food") reduces satiation. This is the closest empirical analogue to "finer resolution creates more fresh sources." |
| Sheldon & Lyubomirsky (2012), "The Challenge of Staying Happier: Testing the Hedonic Adaptation Prevention Model," *PSPB* 38(5):670-680; Bao & Lyubomirsky (2013) applied it to relationships | **Partly** | Adaptation runs through two paths: fewer positive events over time, and rising aspirations. **Variety** and **appreciation** moderate it. Tested in a 3-wave study of N=481. The model has a variety lever and an appreciation (resolution/savoring) lever but **no aspiration-creep term**. Consider adding one. |
| Stigler & Becker (1977), "De Gustibus Non Est Disputandum," *AER* 67(2):76-90. https://www.uvm.edu/~jfarley/EEseminar/readings/StiglerBeckerAER.pdf | **Yes** for "skill-building" sources | Music appreciation is M = f(t, S), and consumption capital S accumulates from past M. With *beneficial addiction* the shadow price falls, so consumption rises with exposure. With *harmful addiction* (∂S/∂M_past < 0) the shadow price rises. Their renewing / skill-building / depleting split maps onto ∂S/∂M_past = 0, > 0, < 0. This framing is about 50 years old. |
| Becker & Murphy (1988), "A Theory of Rational Addiction," *JPE* 96(4):675-700. https://ideas.repec.org/a/ucp/jpolec/v96y1988i4p675-700.html | **Partly** (bears on items 4 and 6) | Adjacent complementarity gives unstable steady states, cold-turkey quitting and binges. It also predicts that anxiety can trigger addiction. Agents are fully rational, so it lacks the model's wanting/liking split. |
| Szpunar, Schellenberg & Pliner (2004), "Liking and memory for musical stimuli as a function of exposure," *JEP:LMC* 30(2):370-381 (summarizes Berlyne's two-factor model). https://sites.utm.utoronto.ca/sites/sites.utm.utoronto.ca.glenn_website/files/download/Szpunar.pdf | **Partly** | Berlyne's two-factor model has learned safety, which raises liking, and boredom, which grows with exposure. Together they give an inverted U over exposures. For complex orchestral excerpts under focused listening, liking peaked around 2-8 exposures and was back to baseline by 32. Simpler stimuli peaked earlier and lower. Incidental listening rose monotonically. **Usable parameters:** the peak is in single-digit exposures, and complexity raises both the peak and the later decline. |
| McAlister (1982), "A dynamic attribute satiation model of variety-seeking behavior," *JCR* (MIT working paper: https://dspace.mit.edu/handle/1721.1/47201) **[not read; abstract page returned empty]** | Likely **Yes** for attribute-level satiation with inventory decay **[memory]** | Satiation is accumulated per *attribute*, not per product, and it decays over time. This is very close to the model's freshness variable and is worth reading in full. |

**Contradictions or complications.** Recovery is partly perceptual (Galak et al.), and adaptation also runs through aspiration creep (Sheldon & Lyubomirsky). Bounded returns to breadth under fixed time follow from any concave satiation model. I found no source treating them as a new result.

---

## 2. "Fractal" liking: resolution splits experience into more likable features, also reveals aversive parts; equanimity keeps resolution paying

| Work | Has result? | Notes |
|---|---|---|
| Rocklage, Rucker, Nordgren, Inman & Janiszewski (2021), "Emotionally Numb: Expertise Dulls Consumer Experience," *JCR* 48(3):355-373. https://ideas.repec.org/a/oup/jconrs/v48y2021i3p355-373..html | **No: contradicts the naive version** | Uses more than 700k consumers and 6M observations across movies, photography, wine and beer. Expertise *lowers* emotional intensity, both cross-sectionally and longitudinally. Mechanism: experts build classifying cognitive structures. Inducing those structures numbed novices, and steering experts away from them restored emotion. This is the single most important paper for item 2. "Resolution" in the form of categorizing/evaluating knowledge reduces affect, so the model must separate *perceptual resolution while attending* from *evaluative categorization*. The model's equanimity/attention-release term could be recast as "not running the classifier," which the experiment supports. |
| Stuppy & van den Bergh (2022), "How sampling high- and low-quality products affects enjoyment," *Psychology & Marketing* 39(4):726-740. https://research.tilburguniversity.edu/en/publications/how-sampling-high-and-low-quality-products-affects-enjoyment/ | **Yes** for "resolution reveals aversive parts" | Four experiments, N=1,080. Sampling across quality levels steepens the link between quality and enjoyment, so high-quality items gain enjoyment and low-quality items lose it. This is a clean empirical version of the two-sided effect of resolution. |
| Orr & Ohlsson (2005), "Relationship between complexity and liking as a function of expertise," *Music Perception* 22(4):583-611. https://www.Gwern.net/doc/psychology/novelty/2005-orr.pdf | **Partly** | Expertise "dissolves" the inverted U between complexity and liking. Experts judge on other dimensions (timbre, expressiveness). The peak doesn't shift; complexity simply stops predicting liking. |
| Frøst & Noble (2002), "Preliminary study of the effect of knowledge and sensory expertise on liking for red wines," *AJEV* 53(4):275-284 (UC Davis summary) | **No** | Knowledge had little effect on liking. Sensory expertise was non-monotonic: the medium group liked wines less. Individual differences were much larger than expertise effects. |
| Hong (2025), "How we learn to like: the role of perceptual learning in development of liking, quality perception, and appreciation," *Food Sci. Biotechnol.* 34(15):3453-3472. https://link.springer.com/article/10.1007/s10068-025-01857-4 | **Partly** (review) | Argues that perceptual learning supplies richer attributes for appreciation, but admits **direct evidence for a perceptual-learning-to-liking link is limited**. Frequent consumers were sometimes *less* sensitive to negative attributes, which cuts against "resolution reveals aversive parts." |
| Arch et al. (2016), "Enjoying food without caloric cost," *BRAT* 79:23-34. https://www.colorado.edu/clinicalpsychology/sites/default/files/attached-files/arch_brown_et_al_mindfulness_and_eating_paper_brat_2016.pdf | **Partly** (attention increases enjoyment) | Mindful vs. distracted tasting raised chocolate enjoyment (d=.51). The raisin result was marginal (d=.27), and there was about 20% lower calorie intake. **Parameter:** brief attention manipulations give a small-to-medium effect on enjoyment. |
| Quoidbach, Dunn, Petrides & Mikolajczak (2010), "Money Giveth, Money Taketh Away," *Psych Science*. https://orbi.uliege.be/bitstream/2268/12758/1/QDPM_PS_2010.pdf | **Partly** | Wealth and money primes reduce savoring (β=-.17). Money-primed participants spent 32 s vs. 45 s eating chocolate and showed less enjoyment. Savoring predicts happiness (β=.34). This supports savoring capacity as a trainable or erodible state variable. |
| Bryant & Veroff (2007), *Savoring: A New Model of Positive Experience* (book) **[not read beyond catalog]** | **Partly** **[memory]** | Savoring is the capacity to attend to, appreciate and amplify positive experience. It is conceptual, not formal. |
| Reich & Zautra (2002), Dynamic Model of Affect (see item 3) | **Partly** | Under stress, affective discrimination collapses: PA and NA become one bipolar dimension. This is evidence that "resolution" is state-dependent and degraded by suffering, which connects items 2 and 3. |

**Verdict for item 2.** Treating resolution as a recursive multiplier of likable features ("fractal") is **not formalized anywhere I found**. Searches: "perceptual learning increases pleasure," "expertise enjoyment," "hedonic expansionism," "expanding capacity for pleasure." The empirical record, however, is **mixed to negative** for the simple claim. Expertise numbs affect (Rocklage) and polarizes enjoyment by quality (Stuppy). Liking benefits of discrimination are mostly asserted, not shown (Hong). The model's equanimity term is the part with some experimental backing, through Rocklage's restoration manipulation.

---

## 3. Bottleneck: relieve suffering first; suffering numbs liking and blocks exploration; exceptions

| Work | Has result? | Notes |
|---|---|---|
| Bogdan & Pizzagalli (2006), "Acute stress reduces reward responsiveness: implications for depression," *Biol Psychiatry* 60:1147-1154. https://depressioninstitute.uci.edu/wp-content/uploads/sites/37/bogdan_bp06.pdf | **Yes** (stress numbs reward learning) | Under threat of shock, reward response bias roughly halved: 0.08 vs. 0.16 overall, 0.08 vs. 0.17 for shock. 74% of participants showed lower bias. Discriminability was unchanged. Self-reported anhedonia predicted the drop. Negative performance feedback had **no** significant effect, so not every stressor numbs. **Parameter:** about 50% reduction in reward sensitivity under acute aversive threat. |
| Lenow, Constantino, Daw & Phelps (2017), "Chronic and Acute Stress Promote Overexploitation in Serial Decision Making," *J Neurosci* 37(23):5681-5689 (via OpenAlex) | **Yes** (stress reduces exploration) | Both cortisol response and chronic self-reported stress led to staying too long with current options. Their proposed mechanism is a lowered estimate of environment quality, which is a cleaner mechanism than "fear blocks learning." |
| Reich & Zautra (2002), *Motivation & Emotion* 26(3):209-222. https://www.asu.edu/xed/resilience/images/Reich-Motivation%20and%20Emotion%202002.pdf | **Partly** | Dynamic Model of Affect: at low stress PA and NA are independent; at high stress they become inversely correlated as processing capacity narrows. Zautra et al. (2005, fibromyalgia) found PA fell more steeply in stressful weeks for one patient group. |
| Fredrickson & Levenson (1998), "Positive emotions speed recovery from the cardiovascular sequelae of negative emotions," *Cognition & Emotion* 12(2):191-220 | **Partly** (exception: pleasure as clean relief) | Contentment and amusement films sped cardiovascular recovery after fear compared with neutral or sad films (omega²=.27). Smilers recovered in 36 s vs. 56 s for non-smilers. This is pleasure working *during* distress, so it pushes against a strict bottleneck. |
| Tay & Diener (2011), "Needs and subjective well-being around the world," *JPSP* (Illinois news summary: https://news.illinois.edu/researchers-look-for-ingredients-of-happiness-around-the-world/) | **No: contradicts a strict lexical bottleneck** | Across many countries, higher needs contributed to positive feelings **regardless of whether lower needs were met**. Basic needs predicted life evaluation; social and autonomy needs predicted positive and negative feelings. A threshold bottleneck should therefore be soft, not lexicographic. |
| Behavioral activation: Lewinsohn (1970s); Dimidjian et al. (2006); summarized in Kanter et al. (2012), *Br J Psychiatry* 200:361-363. https://www.cambridge.org/core/product/28347FA380E03B3066B4C8AFAC867B34/core-reader | **Partly** (the stated exception) | BA matched paroxetine and beat cognitive therapy for moderate-to-severe depression in Dimidjian (2006). This is strong evidence that scheduling pleasure and mastery treats suffering. The model's exception is therefore a major empirical regularity, not an edge case. |
| Feeney & Thrush (2010) via Feeney & Collins (2019), *Curr Opin Psychol* 25:182-186 | **Partly** (secure base) | Secure-base support led to more exploration persistence and performance on a novel task; intrusiveness reduced exploration. |

**Missing piece.** Baumeister et al. (2001), "Bad is stronger than good," and Cacioppo's negativity bias are the standard sources on positive/negative affect asymmetry **[memory; not fetched]**. Note also that Bogdan & Pizzagalli found the effect for threat but not for negative feedback, so the "suffering" input needs a type.

---

## 4. Numbing vs. clean relief; habitual numbing loops worse than nothing; stopping rule

| Work | Has result? | Notes |
|---|---|---|
| Solomon & Corbit (1974); Solomon (1980), "The opponent-process theory of acquired motivation: the costs of pleasure and the benefits of pain," *Am Psychol* 35(8):691-712. https://www.appstate.edu/~steelekm/classes/psy5300/Documents/Solomon1980_Opponent.pdf | **Yes** for rebound and the bridge/trap timing rule | The a-process is fixed. The b-process is slow, opposite in sign, "strengthened by use and weakened by disuse." Net affect is a minus b, with rebound after offset. **Critical decay duration:** if uses are spaced beyond it, b doesn't accumulate. In ducklings, 5-minute gaps were enough. There is also a "savings" effect (fast re-strengthening). This **is** a stopping/spacing rule separating bridge from trap. The "benefits of pain" side (aversive a-process with pleasant b-rebound, as in sauna or parachuting) is a clean-relief mechanism. The toy model largely restates this and should borrow its dynamics. |
| Koob & Le Moal (2001), "Drug addiction, dysregulation of reward, and allostasis," *Neuropsychopharmacology* 24(2):97-129 | **Yes** for the spiral | The hedonic set point shifts upward through opponent-process counteradaptation. Reinforcement shifts from positive to negative, and each self-regulation failure adds distress, so the cycle spirals. "Habitual numbing loops are worse than nothing" is the core of this account. |
| Baker, Piper, McCarthy, Majeskie & Fiore (2004), "Addiction motivation reformulated: an affective processing model of negative reinforcement," *Psych Review* 111(1):33-51 | **Yes** | Escaping negative affect is the dominant motive. Interoceptive cues of rising withdrawal are learned preconsciously, so use resembles signaled avoidance, which resists extinction. Moderate negative affect leaves cognitive control intact; high negative affect shifts to habitual responding. This last point also supports item 5's crossover. Withdrawal raises drug-cue incentive and lowers non-drug reward. |
| Hayes, Wilson, Gifford, Follette & Strosahl (1996), "Experiential avoidance and behavioral disorders," *JCCP* 64(6):1152-1168. https://contextualscience.org/files/184%20Experiential%20avoidance%20JCCP%201996.pdf | **Yes** (verbal theory) | Avoidance "appears to work, even when it does not." It brings rebound (thought suppression), mood-linked loops, and suppression that raises distress. Brief healthy coping is explicitly carved out, which is the bridge/trap distinction stated verbally. |
| Keramati & Gutkin (2014), homeostatic reinforcement learning, *eLife* https://elifesciences.org/articles/04811 **[not read; page blocked]** | Likely **Partly** **[memory]** | Defines reward as reduction of drive (distance from setpoint). A natural formal substrate for "clean relief." |

**Verdict for item 4.** Mostly a **restatement**. Opponent-process theory plus allostasis already gives rebound, escalation, and a spacing rule. Whatever is new would be the *explicit comparison against doing nothing* and a decision-theoretic stopping rule. I did not find that as a closed-form result. Searches: opponent-process, allostasis, Baker 2004, Hayes 1996.

---

## 5. Relief crossover (weak at high distress, best at moderate); savoring vs. grabbing

- **Galak, Kruger & Loewenstein (2013)** (item 1): self-paced "grabbing" gives less pleasure than an imposed slower pace. **Yes** for savoring vs. grabbing, at the level of consumption rate.
- **Baker et al. (2004)**: high negative affect pushes processing to fast, habitual responses, while moderate negative affect preserves control. **Partly** supports the crossover, though as a control mechanism rather than relief magnitude.
- **Bogdan & Pizzagalli (2006)** and **Reich & Zautra (2002)**: at high stress, reward sensitivity and affective discrimination fall. This is the "weak at high distress" arm.
- **Fredrickson & Levenson (1998)**: positive emotion speeds recovery after moderate, lab-induced fear and sadness. This is the "works at moderate distress" arm.
- **Ong, Bergeman, Bisconti & Wallace (2006)**, *JPSP* 91(4):730: daily positive emotion moderates stress reactivity and aids recovery. Resilience decouples PA from NA "particularly on days characterized by heightened stress." **Partly**: this suggests the crossover point depends on trait resilience.
- **Leknes et al. (2011)**, "Relief as a Reward," *PLoS ONE* **[not read; fetch failed]**: relief pleasantness scales with expected pain **[memory]**. If correct, it supports a rising arm at low-to-moderate distress.
- **Bylsma, Morris & Rottenberg (2008)**, meta-analysis of emotional reactivity in MDD **[not read]**: reduced positive reactivity in depression ("emotion context insensitivity") **[memory]**.

**Verdict.** I couldn't find an explicit inverted U of *pleasure-as-relief effectiveness against distress level*. Searches: undoing effect, relief reward, stress/positive affect, Ong 2006. Each arm has empirical support, so this crossover is a plausible **novel synthesis** that is testable.

---

## 6. Wanting = cached value plus sensitization; lock-in; urge surfing

| Work | Has result? | Notes |
|---|---|---|
| Zhang, Berridge, Tindell, Smith & Aldridge (2009), "A Neural Computational Model of Incentive Salience," *PLoS Comput Biol* 5(7):e1000437 | **Yes** for "wanting = cached value modulated by state" | Incentive salience is Ṽ(r, κ): multiplicative r·κ or additive r + log κ. κ>1 is sensitization or appetite; κ=1 reduces to TD learning. Shown in ventral pallidum firing on the first trial in a new state, with no relearning. **Borrow this functional form directly.** |
| Redish (2004), "Addiction as a computational process gone awry," *Science* 306:1944-1947. https://experts.umn.edu/en/publications/addiction-as-a-computational-process-gone-awry/ | **Yes** for lock-in | A non-compensable dopamine increase means the TD error never settles, so value grows without bound and the drug-yielding action is over-selected. |
| Bowen & Marlatt (2009), "Surfing the urge," *Psychol Addict Behav* 23(4):666-671 | **Yes** for "act on the urge less without reducing it" | N=123. Urge measures did **not** differ, but the mindfulness group smoked significantly fewer cigarettes over 7 days. This matches the model's urge-surfing parameter. |
| Garrison, ... Brewer (2018/2020), "Craving to Quit" RCT, *Nicotine Tob Res* 22(3):324-331 (via OpenAlex) | **No/mixed** | App-based mindfulness did **not** improve 6-month abstinence: 9.8% vs. 12.1%, p=.51. The craving-smoking association weakened with more treatment completion (dose-response). Elwafi et al. (2013) reported decoupling of craving and smoking **[not read; PubMed blocked]**. |
| Larsen, Hollands, Garland, Evers & Wiers, "Be More Mindful..." (review) https://discovery.ucl.ac.uk/10179528/1/Hollands_MANUSCRIPT%20NEUROBIOREV-D-23-00709.pdf | **Partly** | A verbal model in which awareness and acceptance weaken the craving→behavior link. Cites Garland's "restructuring reward" (value shifts back to natural rewards) and value-updating accounts of cue devaluation. |
| Daw, Niv & Dayan (2005), model-based vs. model-free **[memory; not fetched]** | **Partly** | The cached-value vs. model-based split is standard. |

**Possible conflict.** The model says urge surfing *raises* value. Brewer-style accounts instead say mindful attention *updates cached value downward* by revealing the true hedonic outcome ("disenchantment") **[memory; partly supported by the Larsen review]**. These are different mechanisms; the model should state which one it means. The per-period loss from wanting–liking mismatch looks like a straightforward extension of Zhang et al.

---

## 7. Resilience from breadth needs convex grief; bundle-vs-spread threshold

| Work | Has result? | Notes |
|---|---|---|
| Linville (1987), "Self-complexity as a cognitive buffer against stress-related illness and depression," *JPSP* 52(4):663-676 | **Partly** (verbal and empirical) | Stress × self-complexity interaction: more distinct self-aspects led to less depression and illness after stress. Spillover between self-aspects is the implicit mechanism, not convexity. |
| Koch & Shepperd (2004), "Is self-complexity linked to better coping?" *J Personality* 72(4):727-760. https://people.clas.ufl.edu/shepperd/files/JP2004-Complexity.pdf; reports Rafaeli-Mor & Steinberg (2002), *PSPR* 6:31-58 | **No: weak or contradictory replication** | The meta-analysis found a **small average negative** correlation between self-complexity and well-being, with large heterogeneity. A vote count of prospective studies showed no clear benefit. Measurement (the H statistic, a card sort with a 2:1 positive:negative word ratio) is contested. **The empirical anchor for "breadth gives resilience" is weak.** |
| Linville & Fischer (1991), "Preferences for separating or combining events," *JPSP* 60(1):5-23. https://scholars.duke.edu/publication/771234 | **Partly supports convex grief over time** | "Renewable resources" model: coping resources are limited but replenish, so people prefer to *separate* two negative events in time. This contradicts the hedonic-editing prediction. In effect it is a convex per-period loss cost, which is the closest existing formalization I found of the model's convex grief. |
| Thaler (1985), hedonic editing / prospect theory (summarized at https://en.wikipedia.org/wiki/Mental_accounting) | **No: contradicts** | The prospect-theory value function is convex in losses (diminishing sensitivity), so pain is *concave* in loss size and **integrating losses** is optimal. That is the opposite of convex grief. The model must justify convexity (e.g., via resource depletion, as in Linville & Fischer) instead of assuming it. |
| Aron self-expansion model (https://en.wikipedia.org/wiki/Self-expansion_model) | **Partly** | Inclusion of other in self. Losing a high-expansion relationship brings "self-contraction." This is a breadth-of-self idea without a convexity condition. |

**Verdict.** I couldn't find the explicit threshold b > λq(k−1)/k or any statement that breadth buffers *only if* grief is convex. Searches: self-complexity, diversification and well-being, hedonic editing, renewable resources. As far as I can tell, the **conditionality result is novel**. It is exactly the issue that separates Linville & Fischer from Thaler, so it should be framed as resolving that.

---

## 8. Social axis: κ·others' pleasure − η·others' suffering; compersion; compassion vs. empathy; taste transmission

| Work | Has result? | Notes |
|---|---|---|
| Bergstrom (1999), "Systems of Benevolent Utility Functions," *JPET* 1(1):71-100. https://ideas.repec.org/a/bla/jpbect/v1y1999i1p71-100.html | **Yes** for the utility form | Interdependent utilities that depend on others' utilities, analyzed with dominant-diagonal matrix theory (conditions for a unique solution). If κ applies to others' *utility* rather than raw pleasure, the model needs Bergstrom's convergence condition to avoid infinite regress. Also relevant: Becker's altruism work and Ray & Vohra's "Games of Love and Hate" (https://economics.brown.edu/sites/default/files/papers/RayVohraLoveHate.pdf) **[not read]**. |
| Klimecki & Singer (2017), "The Compassionate Brain," in *Oxford Handbook of Compassion Science*. https://www.unige.ch/fapse/e3lab/files/8215/4072/9893/Klimecki_2017_BC.pdf; Klimecki et al. (2013, 2014) | **Yes** for "widening pays only if empathic distress is low" | Empathy training **raised** negative affect, and subsequent compassion training brought it back to baseline and **raised** positive affect. Compassion alone raised PA without lowering NA. Effects appear within about 1 week of training. **Parameter:** η can be trained down and κ up in days to weeks. Empathic distress predicted aggression; compassion predicted forgiveness. |
| Flicker & Sancier-Barbosa, "Your Happiness Is My Happiness" (compersion predictors), *Arch Sex Behav* (2023/2024), N=255. https://www.psypost.org/study-identifies-key-factors-boosting-compersion-in-non-monogamous-relationships; Thouin-Savard et al. "Compersion: When jealousy-inducing situations don't (just) induce jealousy" **[not read]** | **Partly** | The strongest predictors of compersion were positive regard for and closeness to the metamour and knowledge of the partner's other relationship. Jealousy and attachment anxiety predicted lower compersion toward new connections. Openness and self-esteem were weak predictors. This supports a threshold with an appraisal term. No effect sizes were available in the source I read. |
| Birch (1980), "Effects of peer models' food choices and eating behaviors on preschoolers' food preferences," *Child Dev* 51(2):489-496 | **Yes** for social taste transmission | After 4 days, 12 of 17 children increased preference for their non-preferred vegetable, with a median rise of 2.5 points on a 9-point scale. Younger children shifted more. **Persistence was not reported** in the source I read. |
| Couples' taste convergence (*Appetite*, 2017; Polish/German group; via TIME summary https://time.com/4943252/food-tastes-relationship) | **Partly** | 100 couples: smell and taste preferences converged with relationship length, independent of relationship happiness. Cross-sectional only. |
| Slotter, Gardner & Finkel (2010), "Who am I without you?" *PSPB* 36(2):147-160 | **Partly** | After a breakup, self-concept content changes and clarity drops; reduced clarity uniquely predicts distress. It does **not** measure whether acquired tastes persist. |

**Verdict.** The utility form is standard (Becker, Bergstrom). Empathy vs. compassion is well established. Whether partner-transmitted tastes **outlast the relationship**: I couldn't find a direct study. Searches: breakup and taste persistence, couples' taste convergence, Slotter 2010. This is an open empirical question the model could pose.

---

## Overall verdict

**Restatements** (borrow rather than rebuild):
- Freshness decay and recovery (Galak et al. 2013; Nelson et al. 2009; McAlister 1982).
- Skill-building vs. depleting sources (Stigler & Becker 1977, beneficial vs. harmful addiction).
- Numbing loops and rebound (Solomon 1980 opponent process, including the critical decay duration as a spacing rule; Koob & Le Moal 2001; Baker et al. 2004).
- Wanting as state-modulated cached value (Zhang et al. 2009) and lock-in (Redish 2004).
- Interdependent utility (Bergstrom 1999).
- Empathy vs. compassion (Klimecki & Singer).

**Partly novel, with empirical tension:**
- The fractal/resolution mechanism. No formal precedent found, but Rocklage et al. (2021) show expertise *numbs* emotion, and Stuppy & van den Bergh (2022) show it polarizes enjoyment. The model should separate perceptual resolution from evaluative categorization, and use Rocklage's restoration manipulation as the analogue of the equanimity term.
- A strict bottleneck is contradicted by Tay & Diener (2011) and by behavioral activation's efficacy. Make it a soft, typed threshold.

**Most plausibly novel:**
- (a) The relief crossover (inverted U of relief vs. distress).
- (b) Breadth-gives-resilience *conditional on convex grief*, with an explicit bundle/spread threshold. This resolves the Thaler (concave, integrate losses) vs. Linville & Fischer (renewable resources, separate losses) split, and may explain the self-complexity null results.
- (c) The combined system linking all eight parts. I found no integrated formal model of "expanding capacity to like." Searches: "hedonic expansionism," "expanding the capacity for pleasure," "formal model acquired taste," preference discovery.

**Borrow from:**
- Zhang et al. (2009): κ-modulated incentive salience.
- Solomon (1980): a−b dynamics with a critical decay duration.
- Stigler-Becker consumption capital.
- Berlyne two-factor (learned safety vs. boredom) for skill-building sources, with peaks at 2-8 exposures for complex stimuli (Szpunar et al. 2004).
- Sheldon & Lyubomirsky's HAP model, for an aspiration-creep term.
- Linville & Fischer (1991) renewable resources, to justify convex grief.
- Bergstrom (1999), for a well-posed κ system.
- Delaney, Jacobson & Moenig, "Preference Discovery" (2017 working paper; https://web.williams.edu/Economics/wp/DelaneyJacobsonMoenigPreferenceDiscovery.pdf): goods believed bad are never sampled, so their value is never learned. This is a ready formalization of why exploration under stress (low sampling) causes lasting welfare loss.

**Methodological caution:** Fredrickson & Losada's (2005) "critical positivity ratio" (2.9013) used Lorenz equations without justification. *American Psychologist* formally retracted its modeling after Brown, Sokal & Friedman (2013) (https://en.wikipedia.org/wiki/Critical_positivity_ratio). Toy-model thresholds (compersion threshold, bundle/spread, bottleneck) should be presented as qualitative conditions, not precise numbers, unless they are fitted to data.

## Not read / gaps

- Not read in full: McAlister (1982) abstract; Redden (2008); Pizzagalli (2014) review; Elwafi et al. (2013); Leknes et al. (2011); Keramati & Gutkin (2014); Bylsma et al. (2008); Rafaeli-Mor & Steinberg (2002) directly (only via Koch & Shepperd); Aron, Paris & Aron (1995); Daw et al. (2005); Baumeister et al. (2001). Most failed on PubMed/PMC reCAPTCHA or site errors.
- Not searched in depth: positive emotion differentiation/granularity (could support resolution); Bryant's Savoring Beliefs Inventory norms; long-term follow-up of Birch's peer-modeling effects.
