# Meaning: a pleasure, a way of quieting, or a structure for attention?

Date: 2026-11-25. This complements `stimulation_challenge.md`, which already covers Westgate & Wilson's (2018) MAC model of boredom (meaning × attention) and Tam & Inzlicht (2024) on switching and boredom. Those are cited here only by reference. `prior_art.md` covers stress numbing reward and relief. The model's existing equanimity parameter `e` (in `model/hx_model_v2.py`: pain scaled by (1-e), intrusion threshold TAU*(1+2e)) is the natural place for a meaning term to attach.

Method: web search, then fetches of publisher pages, author PDFs, PMC and press releases. PubMed often returned a reCAPTCHA wall.

Tags: **[verified]** = bibliographic details and the claim were checked against a fetched page (abstract, full text or table). **[partly verified]** = the work exists and the gist was checked, but some details (volume/pages, numbers) were not. **[memory]** = not checked this session; treat it as a lead.

Hypotheses:
- **H-pleasure**: meaning is (partly) a felt pleasure, a direct positive term.
- **H-quieting**: meaning mainly lowers negative feeling (distress, resistance, rumination, aversive arousal).
- **H-attention**: meaning gives attention a target, sustains engagement, and slows adaptation and boredom.

---

## 1. H-pleasure: meaning as a felt pleasure

| Work | What it says | Bearing |
|---|---|---|
| King, L. A., Hicks, J. A., Krull, J. L. & Del Gaiso, A. K. (2006). "Positive affect and the experience of meaning in life." *JPSP* 90(1):179-196. doi 10.1037/0022-3514.90.1.179 [verified, full text at https://existentialpsych.sites.tamu.edu/wp-content/uploads/sites/152/2016/08/KingetalJPSP2006.pdf] | Six studies. Study 1 (N=568): general PA with meaning in life (MIL) r=.53. NA was related to *lower* MIL at a similar size (reported |r|≈.45; sign inferred from the regression text). In a joint regression, PA β=.39 and NA β=.34 (NA predicting lower meaning) both unique. Daily diary (Study 2): daily PA and NA both uniquely predicted daily meaning, but only average PA predicted global meaning (β=.50). PA did **not** predict meaning prospectively over 2 years. Priming positive-mood words raised meaning ratings (14.25 vs 11.34, p=.03 one-tailed). Induced positive mood raised meaning only when no attributional cue was given (Mood × Cue F(2,188)=3.31, p=.03 one-tailed): mood is used *as information* for the meaning judgment. | The main causal arrow shown is **PA → meaning judgment**, not meaning → PA. Meaning ratings partly *read off* current pleasure. That is evidence that the two co-occur, not that meaning is an extra source of pleasure. |
| Heintzelman, S. J. & King, L. A. (2014). "Life is pretty meaningful." *American Psychologist* 69(6):561-574 [partly verified: full text at https://www.its.caltech.edu/~squartz/HKLifeisPrettyMeaningful.pdf; vol/pages from memory] | Most samples rate meaning above the scale midpoint. Meaning correlates with PA (r=.39, citing Hicks & King 2009). Mild mood boosts (happy music, comics) raise meaning ratings. Meaning tracks environmental *coherence*: seeing photos in a seasonal pattern vs random order raised meaning ratings (Heintzelman et al. 2013; no effect sizes given). "When the world makes sense, life feels more meaningful." | Meaning has a *felt* component ("the feeling that life is meaningful"), tied to detecting coherence. This is close to a "feeling of rightness" or fluency signal. Fluency is mildly positive [memory: Winkielman fluency-affect work], so a small direct positive term is defensible. |
| Kreiss, C. & Schnell, T. (2022). "Have a good day! An experience-sampling study of daily meaningful and pleasant activities." *Frontiers in Psychology* doi 10.3389/fpsyg.2022.977687 [verified, full text] | ESM, 62 students, about 1,860 moments. State meaningfulness and pleasantness r=.44. Pleasantness variance was 86% within-person; meaningfulness was 62% within-person. Studying and working were "meaningful-unpleasant." | Meaning and pleasure dissociate at the moment level. Meaning is more trait-like and stable than pleasure. |
| Choi, J., Catapano, R. & Choi, I. (2017). "Taking stock of happiness and meaning in everyday life: an experience sampling approach." *Social Psychological and Personality Science* 8(6):641-651 [memory; only seen cited] | Same dissociation in Korean ESM data, from memory. | Lead only. |

**Verdict: weakly supported.** Meaning and PA correlate about .4-.5. The experimental evidence runs mostly from mood to meaning *judgments*. A felt "coherence/rightness" signal exists, but no study isolates it as a pleasure independent of PA. **Treat it as a small direct term.**

---

## 2. H-quieting: meaning lowers negative feeling

### 2.1 Stress buffering and distress

| Work | What it says | Bearing |
|---|---|---|
| Hill, P. L., Sin, N. L., Turiano, N. A., Burrow, A. L. & Almeida, D. M. (2018). "Sense of purpose moderates the associations between daily stressors and daily well-being." *Annals of Behavioral Medicine* 52(8):724-729. doi 10.1093/abm/kax039 [verified, full text PMC6052784] | NSDE/MIDUS diary, N=1,949, about 14,400 days. Purpose × stressor on NA: B=−0.005, p<.001. The stressor-day NA increase was 0.186 at low purpose vs 0.119 at high purpose, **about 36% smaller**. Physical symptoms: 0.456 vs 0.241, **about 47% smaller**. Purpose raised PA overall (B=0.030, p<.001), but **purpose × stressor on PA = 0.000 (p=.95)**. | **The cleanest datum for the model.** Purpose shrinks the *negative response to the same stressor* (the resistance term). It adds only a level shift to PA and does not buffer PA. This is correlational. |
| Baumeister, R. F., Vohs, K. D., Aaker, J. L. & Garbinsky, E. N. (2013). "Some key differences between a happy life and a meaningful life." *Journal of Positive Psychology* 8(6):505-516. doi 10.1080/17439760.2013.830764 [verified: full text at the Carlson School PDF; vol/pages from memory] | N=397 (3 waves). Happiness and meaning r=.63-.70. Partial correlations (each controlling the other), happiness vs meaning: stress −.47 vs **+.18**; worry −.24 vs **+.11**; anxious self-concept −.41 vs **+.16**; negative events −.38 vs **+.18**; positive events .18 vs .42; past+future thinking −.31 vs +.11; "I am a giver" −.17 vs +.32. Percent of time feeling bad: −.59 with happiness, **.04 with meaning**. "Meaningful involvements increase one's stress, worries, arguments, and anxiety." The authors call the results tentative. | Not evidence that meaning is non-hedonic. It is evidence that meaningful *commitments raise exposure* to stressors. Meanwhile, the share of time feeling bad is unrelated to meaning. This fits **more pain exposure × less resistance ≈ net zero distress**. It is a quieting-with-exposure-cost pattern, not a pleasure. Partial correlations remove the large shared variance, which inflates the apparent opposition. |
| Purpose in life and depression/anxiety meta-analysis. *Journal of Clinical Psychology* 79(12):2736-2767 (2023). doi 10.1002/jclp.23576 [verified: abstract; authors not recorded] | 99 studies, N=66,468. Purpose with depression r=−.49 [−.52, −.45]. Purpose with anxiety r=−.36. Stronger in clinical samples. The proposed mechanism is reduced avoidance motivation. | Large negative-affect association; cross-sectional. |
| Anoschin, A., Zürn, M. K. & Remmers, C. (2024). "Longitudinal associations of experiential and reflective dimensions of meaning in life with psychopathological symptoms." *Clinical Psychology in Europe* 6(3):e11381 [verified, full text] | Preregistered, two waves about 6 months apart, N=388/538. *Experienced* meaning → later depression β=−.09 to −.13. Depression → later experienced meaning β=−.15 (bidirectional). *Reflecting/searching* for meaning → later depression **+.085** (exploratory). | Small, bidirectional protective effect. **Searching for meaning (rumination-like) goes the other way**, which separates meaning-present (quieting) from meaning-search (a rumination cost). |
| Breitbart, W. et al. (2015). "Meaning-centered group psychotherapy..." *Journal of Clinical Oncology* 33(7):749-754 [verified, full text PMC4334778] | RCT, N=253 advanced cancer patients, active control (supportive group). MCGP vs SGP within-group d: depression −0.67 vs −0.34; hopelessness −0.53 vs −0.01; desire for hastened death −0.31 vs −0.10; physical symptom distress −0.35 vs −0.06 (−0.57 at follow-up); spiritual well-being +0.54 vs +0.17. Anxiety ns. In intention-to-treat, only QoL, depression and hopelessness stayed significant. | **Experimental support**: a meaning intervention mostly reduces *distress*, including distress about physical symptoms (a resistance-type outcome). |
| Huta, V. & Ryan, R. M. (2010). "Pursuing pleasure or virtue..." *Journal of Happiness Studies* 11:735-762 [verified, full text] | Study 4: 10-day intervention, N=114, no control group. Eudaimonic pursuit reduced NA at the end (t=−7.57) and at 3 months (−5.84). PA did *not* rise immediately (−0.31) but did at 3 months (2.58*). Hedonic pursuit raised PA immediately (2.97**), which faded by 3 months (0.85). | Meaning acts first on NA. PA comes later and cumulatively. That fits quieting plus slow adaptation, not an immediate pleasure. |
| Park, C. L. (2010). "Making sense of the meaning literature: an integrative review of meaning making and its effects on adjustment to stressful life events." *Psychological Bulletin* 136(2):257-301. doi 10.1037/a0018301 [verified: abstract] | Distinguishes global vs situational meaning, and meaning-making *efforts* vs meaning *made*. Theory outruns evidence. The *quality* of meaning made matters at least as much as the quantity. | Meaning-made (resolution) is the active ingredient. Effortful searching is not reliably helpful, consistent with Anoschin et al. |
| Steger; Krause | Not checked this session. | Leads only. |
| Frankl, V. E. *Man's Search for Meaning* (1946/1959) [memory] | Historical claim that suffering with meaning becomes bearable. | Historical only, not evidence. |

### 2.2 Meaning maintenance: meaning violations as aversive arousal

| Work | What it says | Bearing |
|---|---|---|
| Heine, S. J., Proulx, T. & Vohs, K. D. (2006). "The meaning maintenance model: on the coherence of social motivations." *Personality and Social Psychology Review* 10(2):88-110 [verified: author PDF] | Meaning = "what links people, places, objects, and ideas to one another in expected and predictable ways." Threats to one framework lead to affirming other, even unrelated, frameworks. | Meaning as expected relations, a prediction/coherence construct. |
| Proulx, T. & Inzlicht, M. (2012). "The five 'A's of meaning maintenance." *Psychological Inquiry* 23(4):317-335 [verified, full text] | Meaning violations "evoke a common, biologically based syndrome of aversive arousal." Compensation efforts are "palliative behaviors" aimed at reducing aversive arousal "rather than resolving meaning violations, per se." A misattribution placebo extinguishes compensation. Accommodation "uniquely prevent[s] the anxious reexperiencing" of the violation. | **Strong theoretical support for H-quieting.** Meaning's motivational force is *relief from the aversive arousal of incoherence*. |
| Proulx, T. & Heine, S. J. (2010). "The frog in Kierkegaard's beer." *Social and Personality Psychology Compass* 4(10):889-905 [verified, full text] | Violations share "a common syndrome of immediate arousal" that "seldom manifests as a conscious emotional experience." | The arousal is often sub-conscious, so self-reported NA will undercount it. |
| Randles, D., Heine, S. J. & Santos, N. (2013). "The common pain of surrealism and death: acetaminophen reduces compensatory affirmation following meaning threats." *Psychological Science* 24(6):966-973 [partly verified: APS press release and journal listing; vol/pages from memory] | Mortality salience raised bail-setting (about $300 → >$400) on placebo, but much less on acetaminophen. A surreal Lynch film had the same pattern. | An analgesic blunts meaning-threat compensation, so **meaning loss is processed like pain**. Restoring meaning works as analgesia. |

### 2.3 Key test: does meaning lower resistance to the *same* pain?

| Work | What it says | Bearing |
|---|---|---|
| Almeida, V. M., Carvalho, C. & Pereira, M. G. (2020). "The contribution of purpose in life to psychological morbidity and quality of life in chronic pain patients." *Psychology, Health & Medicine* 25(2):160-170 [verified, full text] | N=103 chronic pain. Purpose with pain **severity r=−.20**, with pain **interference r=−.58**. Purpose predicted lower anxiety/depression (β=−.33) controlling for severity, interference and catastrophizing. Purpose did *not* predict physical QoL. | **Pattern fits pain × resistance**: purpose barely tracks intensity but strongly tracks interference and distress. Cross-sectional. |
| Boring, B. L., Maffly-Kipp, J., Mathur, V. A. & Hicks, J. A. (2022). "Meaning in life and pain: the differential effects of coherence, purpose, and mattering..." *Journal of Pain Research* 15:299-314 [verified, full text] | MIDUS (n≈1,500-2,500), students n=519, weekly N=138. Purpose had inconsistent, mostly null links with pain *severity/frequency*. One association was positive (baseline purpose b=+.27). Purpose did not predict chronic pain onset (OR=.995). Coherence was the stronger predictor. | **Meaning does not reduce pain intensity**, consistent with a resistance-only effect. Coherence may matter more than purpose. |
| Dezutter, J., Luyckx, K. & Wachholtz, A. (2015). "Meaning in life in chronic pain patients over time..." *Journal of Behavioral Medicine* 38:384-396 [partly verified: abstract] | N=273, 3 waves over 2 years. Presence of meaning predicted well-being (depression, life satisfaction). The abstract reports nothing for pain intensity. | Consistent with the above. |
| Wiech, K. et al. (2008). "An fMRI study measuring analgesia enhanced by religion as a belief system." *Pain* 139(2):467-476, doi 10.1016/j.pain.2008.07.030 [partly verified: abstract; N=24 (12 Catholic, 12 atheist/agnostic) from a secondary blog; pages from memory] | A religious image (Virgin Mary) produced analgesia in Catholics only, via right vlPFC (emotion regulation). Participants reported *detachment* from pain. | An experimental meaning frame changes pain via a regulatory, reappraisal route. The abstract does not separate the intensity vs unpleasantness split. |
| Leknes, S. et al. (2013). "The importance of context: when relative relief renders pain pleasant." *Pain* 154(3):402-410 [verified, full text PMC3590449] | n=16. The same moderate heat was rated pleasant as relief (hedonic +2.3 vs −0.8) and *also* less intense (VAS 3.4 vs 5.3). | Contextual meaning can flip *sign*, and it changes intensity too. Already relevant to `prior_art.md` relief. |
| Arntz, A. & Claassens, L. (2004). "The meaning of pain influences its experienced intensity." *Pain* 109:20-25 [verified via abstract reproduction at https://dolor.blogspot.com/2004/05/meanings-and-pain-intensity.html] | N=31. A cold bar described as "hot" hurt more, mediated by perceived tissue damage. | **Threat-meaning** (harm appraisal) raises *intensity*. This is different from life-meaning and purpose. |

**Verdict on H-quieting: supported, the strongest of the three.** Converging evidence: daily-diary buffering of NA but not PA (Hill, about 36% smaller NA reactivity); an RCT reducing distress (Breitbart); pain studies where purpose tracks interference/distress far more than intensity (Almeida, Boring); and the MMM account of meaning violations as aversive, analgesic-sensitive arousal (Proulx & Inzlicht; Randles). **Caveat:** no experiment found manipulates *purpose/meaning* and measures pain unpleasantness vs intensity separately. That clean test is missing. Appraisal of *what the pain signifies* (harm, relief) changes intensity too, so "meaning" must be split into **life meaning/purpose** (acts on resistance) vs **stimulus meaning** (acts on the pain signal itself).

---

## 3. H-attention: meaning sustains engagement and slows adaptation

| Work | What it says | Bearing |
|---|---|---|
| Kahneman, D. & Thaler, R. H. (2006). "Anomalies: utility maximization and experienced utility." *Journal of Economic Perspectives* 20(1):221-234 [verified, full text] | "Withdrawal of attention is the main mechanism of adaptation to life changes..." As a state "loses its novelty it ceases to be the exclusive focus of attention." | Adaptation = attention leaving. Anything that holds attention on a source slows its adaptation. The paper does not mention meaning. |
| O'Brien, E. & Kassirer, S. (2019). "People are slow to adapt to the warm glow of giving." *Psychological Science* 30(2):193-204, doi 10.1177/0956797618814145 [partly verified: APS release; vol/pages from memory] | Preregistered. Exp 1 (n=96): $5/day for 5 days spent on self vs others. Self-spending happiness declined steadily. Giving happiness on day 5 was about as strong as day 1. Exp 2 (n=502): happiness from 10 rounds of winnings declined "far more slowly" when donated. No effect sizes in the release. | **The best direct evidence** that a meaning-laden (prosocial) version of the same pleasure habituates more slowly. The mechanism (meaning vs attention vs social) is not isolated. |
| Huta & Ryan (2010), above | Eudaimonic benefits are delayed and cumulative. Hedonic PA gains fade within 3 months. | Consistent with slower adaptation. Small, uncontrolled study. |
| Westgate & Wilson (2018) MAC model | See `stimulation_challenge.md`. Boredom = low meaning *or* attention mismatch. | Already covered. |
| van Tilburg, W. A. P. & Igou, E. R. (2012). "On boredom: lack of challenge and meaning as distinct boredom experiences." *Motivation and Emotion* 36(2):181-194 [verified: abstract] | Four studies. Boredom uniquely involves feeling unchallenged *and* judging the situation meaningless. | Meaninglessness is part of boredom. |
| Fahlman, S. A., Mercer, K. B., Gaskovski, P., Eastwood, A. E. & Eastwood, J. D. (2009). "Does a lack of life meaning cause boredom?..." *Journal of Social and Clinical Psychology* 28(3):307-340 [partly verified: citation and a cited r=−.34 between boredom proneness and meaning in life, from a secondary paper; the longitudinal and experimental results were not read] | Title claims psychometric, longitudinal and experimental support for low meaning → boredom. | Lead for the causal direction. |
| Kreiss & Schnell (2022), above | Meaning is more stable within a person than pleasantness (62% vs 86% within-person variance). | Indirect: meaning fluctuates less, which fits slower decay. |

**Verdict: plausible, modestly supported.** The mechanism chain is well supported in parts: attention-withdrawal drives adaptation (K&T), meaninglessness drives boredom (van Tilburg & Igou; MAC), and prosocial pleasure barely adapts over 5 days or 10 rounds (O'Brien & Kassirer). But no study shows that meaning *per se*, holding pleasure constant, slows habituation, and no study reports adaptation rate parameters.

---

## 4. The hedonic vs eudaimonic debate

- Ryan, R. M. & Deci, E. L. (2001). "On happiness and human potentials: a review of research on hedonic and eudaimonic well-being." *Annual Review of Psychology* 52:141-166 [partly verified: search listing; PubMed blocked] frames two traditions.
- Ryff, C. D. (1989). "Happiness is everything, or is it?" *JPSP* 57(6):1069-1081 [memory]. Purpose in life is one of six PWB dimensions; Hill et al. use its subscale.
- Kashdan, T. B., Biswas-Diener, R. & King, L. A. (2008). "Reconsidering happiness: the costs of distinguishing between hedonics and eudaimonia." *Journal of Positive Psychology* 3:219-233 [verified: abstract] argues eudaimonia lacks a clear definition and measurement, and that the two overlap and may share mechanisms.

For an ethical hedonist, the Kashdan et al. position is the friendly one: meaning need not be a separate good if its well-being effects run through affect. The evidence above suggests they run mostly through *less negative affect* and *slower decay*, with only a small direct positive term.

---

## 5. Overall answer: is meaning a pleasure or a way of quieting?

**Mainly quieting, then attention, and only slightly a pleasure.** The best-designed evidence (diary moderation, RCT, longitudinal) shows meaning or purpose acting on the *negative* side. It lowers NA reactivity to the same stressor, depression, hopelessness and pain interference, and it leaves pain intensity and PA reactivity roughly unchanged. Meaning's absence or violation is itself aversive arousal that analgesics blunt. The positive-side link (PA r≈.4-.5) runs largely from mood *into* meaning judgments. Meaningful commitments carry a real exposure cost: more stress and worry (Baumeister partial r≈.1-.2), which roughly offsets the quieting, so time spent feeling bad is unrelated to meaning (r=.04). Prosocial and eudaimonic pleasures decay more slowly, which gives meaning a second, attention/adaptation route.

Two splits matter. **Present meaning** quiets, while **searching** for meaning adds slightly to later symptoms (rumination-like). **Life meaning/purpose** acts on resistance, while **stimulus meaning** (harm or relief appraisal) acts on the pain signal itself.

---

## 6. Proposed model representation

Let meaning `m ∈ [0,1]` be a property of an activity or commitment, standardized so that about ±1 SD of trait purpose spans about 0.3-0.5 of the range.

1. **Resistance multiplier (main term).** Suffering = pain × resistance. Use `resistance_eff = r0 · (1 − k_r · m)`, or fold it into equanimity: `e_eff = 1 − (1 − e)(1 − k_r · m)`. Calibration: Hill 2018 gives about 36% smaller NA reactivity from low to high purpose (about 2 SD); Breitbart gives physical-symptom-distress d≈−0.3 to −0.5 vs control. **k_r ≈ 0.3-0.5**. Pain intensity is unaffected by m (Boring; Almeida severity r≈−.2).
2. **Exposure cost.** Meaningful commitments raise stressor exposure: `pain_rate ← pain_rate · (1 + k_x · m)`, **k_x ≈ 0.1-0.3** (Baumeister partial r .11-.18). The net effect on distress is near zero for typical m. This term lets the model reproduce Baumeister's pattern.
3. **Slower adaptation (attention term).** The freshness decay rate is `λ_eff = λ0 · (1 − k_a · m)`, optionally with a higher intrusion threshold so meaningful targets hold attention slots. **k_a ≈ 0.3-0.8**, poorly constrained: O'Brien & Kassirer show near-zero decay over 5 days for giving vs a steady decline for self-spending. Flag this as a free parameter.
4. **Small direct positive term.** `+ β_m · m` per hour of meaningful activity, with **β_m ≈ 0-0.1** of the max hedonic unit. This is the felt "coherence/rightness" component. Keep it small, because most PA-meaning covariance runs PA → meaning.
5. **Meaning violation (MMM).** Incoherence adds aversive arousal `a_v`, removed when meaning is restored. This is relief, which `prior_art.md` relief typing can absorb as *clean relief* if made by accommodation and *palliative* if made by affirmation.
6. **Search for meaning ≠ meaning.** Optionally, a `search` state adds a small rumination cost (Anoschin β≈+.09).

## 7. Three predictions that distinguish the hypotheses

1. **Pain × meaning interaction (quieting vs pleasure).** Give a heat-pain task with and without a purpose frame (pain earns a donation to a chosen charity), plus a no-pain condition with the same frame. *H-quieting*: the frame lowers unpleasantness, not intensity, and the benefit grows with pain level (zero at no pain). *H-pleasure*: a constant positive shift that also appears in the no-pain condition. This intensity/unpleasantness split for life-purpose is the clean test missing from the literature.
2. **Decay slope vs offset (attention vs pleasure).** Repeat a matched-pleasantness activity 10 or more times with vs without meaning (O'Brien & Kassirer design), adding mind-wandering probes. *H-attention*: a shallower decline slope, with fewer mind-wandering reports mediating it. *H-pleasure*: a parallel offset with the same slope. *H-quieting*: no difference without a stressor.
3. **Which affect moves (ESM, next-prompt lags).** *H-quieting*: momentary meaning predicts lower *next-prompt* NA and rumination, especially after a stressor, with little PA gain once current PA is controlled. *H-pleasure*: meaning predicts next-prompt PA beyond current PA, regardless of stressors. A pharmacological corollary (MMM): acetaminophen should shrink the felt cost of meaning *threats* but not the felt benefit of meaning *present*, if meaning is quieting.

---

## Not read in full / gaps

- Steger and Krause stress-buffering papers were not fetched.
- The Fahlman et al. (2009) longitudinal and experimental results were not read.
- The Choi et al. (2017) ESM paper was not read.
- Full statistics for Wiech et al. (2008) and Randles et al. (2013) were not seen, only abstracts and press releases.
- No study found that manipulates life-purpose and separately measures pain intensity vs unpleasantness.
- No study found that estimates adaptation-rate parameters for meaningful vs non-meaningful activities.
