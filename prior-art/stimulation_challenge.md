# Arousal, stimulation and challenge: should the model get an arousal layer?

Date: 2026-11-25. This complements `prior_art.md` (Berlyne two-factor, stress numbing reward, Reich & Zautra, Fredrickson undoing) and `evolution_cognition.md` (learning progress, Kidd Goldilocks, benign masochism). Those are cited here only by reference.

Source for the hypotheses: a set of informal claims about optimal stimulation and hedonic homeostasis (largely unsourced), treated here as claims to check.

Method: web search, then fetches of publisher pages, repositories (RePEc/IDEAS, university repositories, lab PDFs) and secondary pages. PubMed/PMC mostly returned a reCAPTCHA wall.

Tags: **[verified]** = bibliographic details and the claim were checked against a fetched page (abstract, publisher page or full text). **[partly verified]** = existence/title checked, but some details (volume/pages, or a specific claim) were not. **[memory]** = background knowledge not checked this session; treat it as a lead.

---

## 0. Lead question: how does arousal affect attention and pleasure?

### 0.1 Arousal and attention

| Work | What it says | Model relevance |
|---|---|---|
| Easterbrook, J. A. (1959). "The effect of emotion on cue utilization and the organization of behavior." *Psychological Review* 66(3) [partly verified: catalog summary; pages 183-201 from memory] | As arousal rises, the range of cues used narrows. Peripheral cues are dropped first. This helps when the task depends on central cues and hurts when it needs peripheral ones. It is a review of about 60 studies with no new data. | Arousal narrows attention breadth. |
| Mather, M. & Sutherland, M. R. (2011). "Arousal-biased competition in perception and memory." *Perspectives on Psychological Science* 6(2):114-133 [verified: journal issue page and abstract] | Arousal *strengthens the existing priority bias*: high-priority items (salient bottom-up or goal-relevant top-down) gain and low-priority items lose, in both perception and long-term memory. This explains when arousal helps and when it hurts emotional memory. | This is the cleanest mechanism. Arousal acts like a **lower softmax temperature** on attention competition. It amplifies whatever already wins, whether pleasant or aversive. |
| Aston-Jones, G. & Cohen, J. D. (2005). "An integrative theory of locus coeruleus-norepinephrine function: adaptive gain and optimal performance." *Annual Review of Neuroscience* 28:403-450 [verified, full text] | LC has phasic and tonic modes. Phasic bursts at moderate tonic levels support task engagement (exploit). High tonic activity is distractible and supports exploration. When task utility falls, LC shifts to tonic mode, which "facilitates the disengagement of performance from this task." OFC evaluates reward and ACC evaluates cost. Ties to the Yerkes-Dodson inverted U. | Arousal is a **gain** parameter, and the explore/exploit switch is driven by falling *utility*, not by arousal itself. This links directly to the model's freshness decay: as freshness drops, utility drops, and tonic mode means switching. |
| Unsworth, N. & Robison, M. K. (2016). "Pupillary correlates of lapses of sustained attention." *Cognitive, Affective, & Behavioral Neuroscience* 16:601-615 [verified, full text] | Mind-wandering and inattention went with *smaller* pretrial pupils (low arousal). External distraction went with *larger* pupils (high arousal). The authors caution "there is likely not a simple one-to-one correspondence." | Both arousal extremes lose attention, in different ways: low arousal leaks attention inward (mind-wandering), high arousal leaks it to external capture. |

**Summary.** Arousal's best-supported effect is on the *allocation and gain of attention*: it narrows attention and sharpens priority (Easterbrook, ABC), and an inverted U governs engaged performance (LC-NE). Lapses happen at both ends.

### 0.2 Arousal and pleasure/liking

| Work | What it says | Model relevance |
|---|---|---|
| Russell, J. A. (1980). "A circumplex model of affect." *JPSP* 39(6):1161-1178 [verified, full text] | Affect lies on a circle defined by pleasure-displeasure and arousal-sleep. The two axes are conceptually distinct but correlated (~.36 in self-report). | Arousal is **not itself a hedonic axis**. "Optimal arousal" can't be a hedonic variable by definition. It can only matter through effects on valence. |
| Reversal theory: Apter, M. J. (1982). *The Experience of Motivation* [memory]; overview at https://en.wikipedia.org/wiki/Reversal_theory [verified for content] | Telic (goal) state: arousal runs from relaxation (pleasant) to anxiety (unpleasant). Paratelic (play) state: arousal runs from boredom (unpleasant) to excitement (pleasant). The same arousal reverses hedonic tone with state, for example under a "protective frame." Mostly illustrative evidence. | **Complicates a single inverted U.** The arousal→pleasure map is state-indexed (two monotone curves of opposite sign), not one curve. |
| Excitation transfer: Zillmann (1971, 1983) [memory]; https://en.wikipedia.org/wiki/Excitation-transfer_theory [verified for content]; Cantor, Zillmann & Bryant (1975), "Enhancement of experienced sexual arousal... through misattribution of unrelated residual excitation," *JPSP* 32(1):69-75 [partly verified: title] | Residual arousal from one stimulus intensifies the emotional response to the next, if it comes before the residue decays and the arousal is misattributed. The theory has been criticized for underweighting appraisal. | There is a *direct* amplification term, but it is short-lived (minutes) and works on **intensity, not sign**. |
| Dutton, D. G. & Aron, A. P. (1974). *JPSP* 30(4):510-517 [partly verified via https://en.wikipedia.org/wiki/Misattribution_of_arousal]; White, G. L., Fishbein, S. & Rutstein, J. (1981). *JPSP* 41(1):56-62 [partly verified, same page] | Men who had just crossed a fear-inducing bridge called the female interviewer more often. White et al.: aroused men rated an attractive target *higher* and an unattractive target *lower*, regardless of the arousal source's valence. | Arousal **polarizes** evaluation. This is the hedonic mirror of ABC: it amplifies the existing sign. |
| Chim, L., Hogan, C. L., Fung, H. H. & Tsai, J. L. (2017). "Valuing calm enhances enjoyment of calming (vs. exciting) amusement park rides and exercise." *Emotion* (advance online), doi 10.1037/emo0000348 [verified, full text] | People enjoy activities that match their *ideal affect*. Valuing calm predicted enjoyment of a Ferris wheel (β≈.40) but not a roller coaster (β≈.10, ns). Experimentally induced valuing of calm made low-intensity exercise more enjoyable than high-intensity (partial η²≈.06). *Actual* calm did not predict enjoyment. | A **fit term**: pleasure depends on the match between an activity's arousal and the person's current ideal arousal. This is the real version of "the optimum is relative to the person." The effect size is modest. |
| Tsai, J. L. (2007). "Ideal affect: cultural causes and behavioral consequences." *Perspectives on Psychological Science* 2(3):242-259 [partly verified: title/abstract; vol/pages from memory] | Affect valuation theory: people differ in valuing high-arousal positive states (HAP, excitement) vs low-arousal positive states (LAP, calm). This is shaped by culture and temperament. | Ideal arousal is a trait-and-state parameter. |
| Stress blunting reward: Bogdan & Pizzagalli (2006); Reich & Zautra (2002) | Already in `prior_art.md`: acute threat roughly halves reward responsiveness, and high stress collapses affective discrimination. | High *threat* arousal lowers liking. This is already in the model as distress-gated numbing. |

### 0.3 Arousal and durability of positive affect

| Work | What it says |
|---|---|
| McManus, M. D., Nakamura, J. & Siegel, J. T. (2024). "Hiding in plain sight: The distinct importance of low-arousal positive affect." *Motivation and Emotion* 48:336-422 [verified, full text partly read] | Systematic review of 226 papers. LAPA and HAPA differed in 89% of comparisons. LAPA uniquely predicts life satisfaction, and it has a more consistent link to cardiovascular health and sleep. **Durability:** after social contact, "only LAPA is still elevated two hours later" (citing Liu et al. 2021 [partly verified via the review]). LAPA may be less disrupted by trauma. Proposed LAPA subtypes: calm, satisfaction, relief. |

**Implication.** LAP decays more slowly than HAP. The model's relief term already resembles one LAPA subtype.

### 0.4 Verdict on the lead question

1. **Mainly through attention.** The strongest, best-replicated effect is that arousal sets attentional gain and breadth. It amplifies whatever already wins the priority competition (Easterbrook; ABC; LC-NE), with lapses at both extremes (Unsworth & Robison).
2. **Direct amplification of liking is real but small, brief and sign-preserving.** Excitation transfer and misattribution intensify, and White et al. show arousal *polarizes*: liked things are liked more and disliked things less. It is not a positive hedonic boost.
3. **As a separate dimension, arousal has no hedonic value of its own** (Russell). What matters is the *fit* between arousal and the current ideal or mode (reversal theory; Chim et al.). There is also one durability asymmetry: LAP outlasts HAP.

**Would a layer change the model's conclusions?** Mostly it would **relabel** existing terms. The "battery" covers fatigue and recovery, "attention capture" covers gain, and distress numbing plus equanimity cover high-threat arousal. Three pieces are *not* redundant and are worth adding as parameters rather than a full layer:
- (a) **Arousal as a capture temperature.** Higher arousal raises the share of attention taken by the top-priority item, whatever its sign. This interacts with the fractal-liking lemma: arousal raises the risk of aversive capture, so the equanimity-first ordering should matter *more* at high arousal.
- (b) **Ideal-arousal fit.** A multiplicative enjoyment term, max about 10% of variance.
- (c) **Slower decay for low-arousal positive affect.**

---

## 1. Optimal stimulation and arousal theories

| Work | Verdict | Notes |
|---|---|---|
| Hebb, D. O. (1955). "Drives and the C.N.S." *Psychological Review* 62:243-254 [memory] | Supports the inverted U (for cue function) | This is the origin of optimal arousal. |
| Berlyne [in `prior_art.md`] | Supports | Arousal potential from collative variables. |
| Teigen, K. H. (1994). "Yerkes-Dodson: A law for all seasons." *Theory & Psychology* 4(4):525-547 [verified, abstract] | **Complicates** | The original 1908 law concerned stimulus strength × discrimination difficulty in habit formation. Later restatements in terms of arousal, anxiety, stress or motivation are "often wrongly credited," and the law's flexibility reflects vague constructs. Treat the inverted U as a family of hypotheses, not a law. |
| Zuckerman (1979), *Sensation Seeking: Beyond the Optimal Level of Arousal*; (1994) *Behavioral Expressions and Biosocial Bases of Sensation Seeking* [partly verified: titles via https://en.wikipedia.org/wiki/Marvin_Zuckerman] | Supports trait variation | Sensation seeking is seeking "varied, novel, complex and intense" experience. His later work moved toward biochemical approach/avoidance models [memory]. |
| Raju, P. S. (1980). "Optimum stimulation level: its relationship to personality, demographics, and exploratory behavior." *J. Consumer Research* 7(3):272-282 [partly verified: citation; findings not read] | Supports trait variation | OSL is a measurable trait that predicts exploratory consumer behavior [memory for findings]. |
| Apter, reversal theory (see 0.2) | **Complicates** | Two state-indexed curves, not one inverted U. |

**Model:** Keep an inverted U for *attention/performance* (LC-NE). For *pleasure*, use fit to a state-dependent ideal (reversal mode or ideal affect).

## 2. State dependence

- **SPS.** Greven, C. U., Lionetti, F., Booth, C., Aron, E. N. et al. (2019). "Sensory processing sensitivity in the context of environmental sensitivity: a critical review and development of research agenda." *Neuroscience & Biobehavioral Reviews* 98:287-305 [verified, abstract]. SPS fits differential susceptibility: worse outcomes in negative environments and *greater benefit* from positive ones. The authors say "scientific knowledge is lagging behind" and call for more reliable, objective measurement. Aron & Aron (1997), *JPSP* 73(2):345-368 [memory]. **Evidence quality: moderate to weak.** It relies on self-report, and the HSP scale's factor structure is disputed [memory].
- **Introversion.** Eysenck (1967) [memory]. Geen (1984, *JPSP* 46(6):1303-1312) found introverts chose lower noise levels, and at their own chosen levels arousal was equal across groups [memory; search did not surface it]. This supports a *person-specific optimum*.
- **Sleep loss.** Gujar et al. (2011), "Sleep deprivation amplifies reactivity of brain reward networks, biasing the appraisal of positive emotional experiences," *J. Neurosci.* [partly verified: title]. Venkatraman et al. (2007), "Sleep deprivation elevates expectation of gains and attenuates response to losses following risky decisions," *Sleep* [partly verified: title]. **Complicates** "fatigue lowers the preferred stimulation level": sleep loss can *raise* reward reactivity and gain-seeking.
- **Fatigue/stress:** high threat lowers reward sensitivity (`prior_art.md`).

**Verdict:** "The optimum is relative to person and state" is supported. "Fatigue lowers the optimum" is plausible but not directly shown. Sleep loss partly cuts the other way, toward reward-seeking with poorer valuation.

## 3. Flow and challenge-skill balance

- Fong, C. J., Zaleski, D. J. & Leach, J. K. (2015). "The challenge-skill balance and antecedents of flow: a meta-analytic investigation." *Journal of Positive Psychology* 10(5):425-446 [partly verified: abstract via https://www.instituteofcoaching.org (dated 2014 online); vol/pages from memory]. 28 studies. Balance-flow association is **moderate**, and weaker with intrinsic motivation. It is weaker in individualistic cultures, in work/education settings, with experience sampling, and for state rather than trait flow. Clear goals and sense of control are comparably robust antecedents.
- Barthelmäs, M. & Keller, J. (2021). "Antecedents, boundary conditions and consequences of flow." In Peifer & Engeser (eds.), *Advances in Flow Research*, 71-107 [verified, abstract], condensing Keller & Landhäußer (2012) "The flow model revisited." Flow depends on *perceived* skill-demand fit **plus the value attributed to the activity**. They reject the "above-average challenge and skill" (quadrant/octant) framing. No systematic tests of the revised model exist yet.
- Peifer, C., Schulz, A., Schächinger, H., Baumann, N. & Antoni, C. H. (2014). "The relation of flow-experience and physiological arousal under stress — can u shape it?" *J. Experimental Social Psychology* 53:62-69 [verified, full text]. Absorption has an **inverted U** with sympathetic arousal and cortisol (highest at *moderately* elevated cortisol) and a **linear positive** relation with parasympathetic HRV. N=22 men, correlational.
- Moneta (2004), "The flow experience across cultures," *J. Happiness Studies*; Moneta & Csikszentmihalyi (1996) [partly verified: reference list only]. Csikszentmihalyi (1975), *Beyond Boredom and Anxiety* [memory]: boredom channel = skill > challenge; anxiety channel = challenge > skill.

**Verdict:** Flow sits at **moderate**, not high, sympathetic arousal, with high vagal tone. The claim "flow = high arousal" is wrong as stated. That flow is "costly" is **unsupported**: no source found shows a recovery debt after flow. Peifer's parasympathetic finding hints that it may be cheaper than stressed effort. **Model:** P(flow) = f(fit between perceived challenge and skill) × activity value. Put in a modest battery drain, and flag it as an assumption.

## 4. Rest and recovery

- Sonnentag, S. & Fritz, C. (2007). "The Recovery Experience Questionnaire." *J. Occupational Health Psychology* 12(3):204-221 [verified, abstract]. There are four separable experiences: detachment, relaxation, mastery and control (N=930).
- Bennett, A. A., Bakker, A. B. & Field, J. G. (2018). "Recovery from work-related effort: a meta-analysis." *J. Organizational Behavior* 39(3):262-275 [verified, abstract]. 54 samples, N=26,592. **Detachment** is most strongly tied to lower fatigue. **Control** (and mastery [memory]) is most strongly tied to higher vigor.
- Albulescu, P. et al. (2022). "'Give me a break!' A systematic review and meta-analysis on the efficacy of micro-breaks." *PLOS ONE* 17(8):e0272460 [verified, full text]. Micro-breaks: vigor d=.36, fatigue d=.35, performance d=.16 (ns). Performance gains held only for low-demand tasks (cognitive tasks d≈−.09). Longer breaks gave larger gains (b=.07).

**Verdict:** Rest = recovery is supported, and recovery has *two* channels: low-arousal detachment (removes fatigue) and *active* mastery/control (adds vigor). Rest is therefore not only low arousal. **No study found directly compares alternating high/low arousal with sustained arousal for pleasure.** That remains a model prediction.

## 5. Switching costs and boredom

- Rubinstein, J. S., Meyer, D. E. & Evans, J. E. (2001). "Executive control of cognitive processes in task switching." *JEP:HPP* 27(4):763-797 [verified, full text partly]. The switch cost was about 975 ms in Exp. 1. It grew with rule complexity (+823 ms for complex rules) and shrank with cues. Two stages: goal shifting and rule activation. Meyer's "up to 40% of productive time" is a popular remark, not a result of this paper (https://www.apa.org/research/action/multitask) [verified].
- Monsell, S. (2003). "Task switching." *Trends in Cognitive Sciences* 7(3):134-140 [partly verified: title/PubMed listing; vol/pages from memory]. Kiesel, A. et al. (2010). "Control and interference in task switching — a review." *Psychological Bulletin* 136(5):849-874 [partly verified: full text; vol/pages from memory]. *Residual* switch costs remain even after long preparation, for example 58 ms at 800 ms preparation.
- Leroy, S. (2009). "Why is it so hard to do my work? The challenge of attention residue when switching between work tasks." *OBHDP* 109(2):168-181 [verified, abstract]. Unfinished prior tasks leave residue that hurts the next task. Finishing alone is not enough. Time pressure on the prior task *helps* disengagement.
- Eastwood, J. D., Frischen, A., Fenske, M. J. & Smilek, D. (2012). "The unengaged mind: defining boredom in terms of attention." *Perspectives on Psychological Science* 7(5):482-495 [partly verified: abstract; vol/pages from memory]. Boredom is "the aversive experience of wanting, but being unable, to engage in satisfying activity."
- Westgate, E. C. & Wilson, T. D. (2018). "Boring thoughts and bored minds: the MAC model of boredom and cognitive engagement." *Psychological Review* 125(5):689-713 [partly verified: dissertation abstract at https://libraetd.lib.virginia.edu/public_view/4m90dv97n; vol/pages from memory]. Boredom comes from a **meaning** deficit (activity not tied to valued goals) and/or an **attention** deficit (demand-resource mismatch). **Both over- and under-stimulation produce attentional boredom.** Different boredom types motivate different remedies.
- Tam, K. Y. Y. & Inzlicht, M. (2024). "Fast-forward to boredom: how switching behavior on digital media makes people more bored." *JEP: General* [verified via https://www.apa.org/news/press/releases/2024/08/online-videos-boredom]. Seven experiments, N>1,200. People *predicted* that switching would relieve boredom, but it **increased** boredom. Watching one 10-minute video was less boring and more meaningful than switching among seven 5-minute videos (the APA release's figures). Fast-forwarding within one 50-minute video had the same effect. Proposed mechanism: switching makes content feel meaningless.

**Verdict:** Task-set switch costs are real but sub-second to about 1 s per switch, scaling with complexity. Residue from *unfinished* tasks is the larger practical cost. The claim that within-task sensory micro-novelty is low-tax is **unsupported, and partly contradicted**: Tam & Inzlicht show that even within-video skipping raises boredom through lost meaning. Boredom as a switch signal is supported (MAC; LC-NE disengagement), but *acting* on it by rapid switching backfires.

## 6. Feeds and short-form video

- Ihssen, N. & Wadsley, M. (2021). "A reward and incentive-sensitization perspective on compulsive use of social networking sites — wanting but not liking predicts checking frequency and problematic use behavior." *Addictive Behaviors* 116:106808 [verified, abstract]. Wanting and liking were separable. **Wanting**, not liking, predicted checking frequency and problematic use.
- Cho, H. et al. (2021). "Reflect, not regret: understanding regretful smartphone use with app feature-level analysis." *Proc. ACM HCI* 5(CSCW2):456 [verified, full text]. 26.5% of ESM sessions were regretted, with Instagram the highest at 41.9%. Passive and recommendation features dominated regretted sessions over 10 minutes ("rabbit holes"). Rewarding use was not regretted. Lukoff et al. (CHI 2021): autoplay and recommendations reduce sense of agency [partly verified via Cho].
- Guo, L., ... Hiniker, A. (2025). "What social media use do people regret? An analysis of 34K smartphone screenshots with multimodal LLM." *CHI '25* [verified, full text]. Algorithmically recommended content and comments were the most regretted, messaging the least. Over 60% of communication sessions drifted into browsing.
- Verduyn, P. et al. (2015). "Passive Facebook usage undermines affective well-being." *JEP: General* 144(2):480-488 [verified, abstract]. Lab and ESM studies, mediated by envy. Later reviews contest the generality of the passive/active split [memory].
- Lyngs, U. et al. (2019). "Self-control in cyberspace." *CHI 2019* [verified]. Dual-systems framing of 367 tools. Does not address wanting vs liking.

**Verdict:** "Feeds drive wanting more than liking" is **supported** (Ihssen & Wadsley), as are regret for recommended and passive feeds, and switching-induced boredom. "Zero switching cost" is **wrong**: the task-set cost is low, but the meaning/boredom cost is real. No direct experiment found that infinite scroll *per se* lowers enjoyment. The evidence is indirect (Tam & Inzlicht; Cho et al.).

## 7. Anticipation and memory

- Loewenstein, G. (1987). "Anticipation and the valuation of delayed consumption." *Economic Journal* 97(387):666-684 [verified, abstract]. Savoring and dread explain postponing pleasures and hurrying pains.
- Van Boven, L. & Ashworth, L. (2007). "Looking forward, looking back: anticipation is more evocative than retrospection." *JEP: General* 136(2):289-300 [partly verified: citation; claim from title].
- Kahneman, D., Fredrickson, B. L., Schreiber, C. A. & Redelmeier, D. A. (1993). "When more pain is preferred to less: adding a better end." *Psychological Science* 4(6):401-405 [verified, full text]. 22 of 32 (69%) chose to repeat the longer trial, which had a milder end. Replication: 24 of 37.
- Redelmeier, D. A. & Kahneman, D. (1996). *Pain* 66(1):3-8 [partly verified via https://en.wikipedia.org/wiki/Peak%E2%80%93end_rule].
- Alaybek, B. et al. (2022). "All's well that ends (and peaks) well? A meta-analysis of the peak-end rule and duration neglect." *OBHDP* 170:104149 [verified, abstract]. Peak-end r=.581 [.487, .661] over 174 effects. The peak-end score is comparable to the overall average. Duration effect "essentially nil."

**Scheduling implication:** Put the best segment last in a block (end effect). Announce pleasures in advance (anticipatory utility). Remembered value ≈ mean(peak, end), which is weakly sensitive to duration, so long low-grade feed sessions are under-remembered relative to time spent.

## 8. Competence and mastery

- White, R. W. (1959). "Motivation reconsidered: the concept of competence." *Psychological Review* 66(5):297-333 [partly verified: PubMed title; vol/pages from memory]. Effectance: pleasure in *producing effects on the environment*, distinct from drive reduction.
- SDT competence: Ryan & Deci (2000), *American Psychologist* 55(1):68-78 [memory].
- What is distinct from learning progress (`evolution_cognition.md`): effectance is about **agency/contingency** (my action → visible effect), not information gain. It connects to the agency finding (Lukoff/Cho): feeds that remove agency remove effectance pleasure even when content is novel. Mastery and control experiences also predict vigor in recovery (Bennett et al.).

## 9. Compensatory stimulation

- Poerio, G. L., Blakey, E., Hostler, T. J. & Veltri, T. (2018). "More than a feeling: autonomous sensory meridian response (ASMR) is characterized by reliable changes in affect and physiology." *PLOS ONE* 13(6):e0196645 [verified, full text]. Study 1: N=1,002, 813 experiencers. Pleasant affect rose *only in experiencers*. Study 2: N=110. Experiencers' heart rate fell 3.41 bpm (d=.39) while skin conductance *rose*. Experiencers report using it for relaxation and sleep.
- Zentall, S. (1975). "Optimal stimulation as theoretical basis of hyperactivity." *American J. Orthopsychiatry* 45(4):549-563 [verified, abstract]. Hyperactivity is a homeostatic bid to *raise* low stimulation, the opposite of the "reduce stimulation" clinical norm. Zentall & Zentall (1983), *Psychological Bulletin* 94:446-471 [memory].

**Verdict:** "Compensatory stimulation" is **partly supported**. ASMR is a low-heart-rate, mildly activating, pleasant state *for a subgroup*, used for relaxation. Its use specifically as a *retreat from overstimulation* is untested (self-report motives only). Zentall supports the under-stimulation branch of compensation. Note that ASMR combines lower HR with higher SCL: it is not simply "low arousal," which fits Peifer's co-activation pattern.

---

## Informal claims: scorecard

| Claim | Status |
|---|---|
| Too little and too much stimulation both hurt | **Supported** for attention/boredom (MAC Study 2; LC-NE). Weaker for pleasure, which is state-indexed (reversal theory). |
| Optimum relative to person and state | **Supported** (Zuckerman; Geen [memory]; Chim et al. causal). Fatigue direction unproven; sleep loss partly opposite. |
| Compensatory stimulation (ASMR as retreat) | **Partly**: relaxation use and HR drop verified; "retreat from overstimulation" untested. |
| Three zones: flow (high, costly) / cruising / rest | Flow is at **moderate** arousal, so "high" is wrong. "Costly" is unsupported. "Cruising" has no literature construct. Rest is supported but has an active channel (mastery/control). |
| Smooth ramp vs shock start | **Unsupported** (nothing found). |
| Context-switch tax vs low-tax within-task micro-novelty | Tax **supported** but small per switch; residue is the bigger cost. Low-tax micro-novelty is **contradicted** in media (Tam & Inzlicht). |
| Feeds = zero-switching-cost novelty, drive wanting > liking | Wanting > liking **supported**. "Zero cost" **wrong** (meaning/boredom cost). |

## Proposed model layer (as parameters, not a full layer)

State variables: tonic arousal *a* ∈ [0,1]; ideal arousal *a\** (trait plus state; mode telic/paratelic); battery *B* (existing); unfinished-task residue *R*; switch count *s* per window.

1. **Attention gain/temperature.** Attention share over candidate sources = softmax(priority / τ), with τ = τ0/(1 + κ·a). High *a* sharpens capture of the top item, whatever its valence (ABC). Engaged-attention efficiency g(a) is an inverted U peaking at moderate *a*. Mind-wandering probability rises as *a* → 0, and external capture rises as *a* → 1.
2. **Momentary pleasure** = Σ valence × attention share × freshness × resolution (existing), × fit term [1 − φ·(a − a\*)²]. φ is small (Chim: about 6-10% variance). Add a short excitation-transfer term: intensity ×(1 + ε·a_residual), sign-preserving, decay over minutes.
3. **Threat arousal** uses the existing distress gate (reward sensitivity × ~0.5 under acute threat).
4. **Flow:** P(flow) ∝ fit(challenge, skill) × value (Barthelmäs & Keller), maximal at moderate *a*. Mild battery drain (assumed).
5. **Switching:** each task-set switch costs ~0.2-1 s (complexity-scaled) plus residue *R* when the prior task is unfinished. *R* reduces attention to the new task. Content switching inside a medium adds a meaning penalty that raises boredom (Tam & Inzlicht), which *lowers* pleasure even though novelty rises.
6. **Recovery:** detachment lowers fatigue (dB+); mastery/control raise vigor. Micro-breaks d ≈ .35 for both.
7. **Decay:** LAP decays more slowly than HAP. Liu et al.: LAP still elevated at 2 h, HAP not.
8. **Memory/anticipation:** remembered value ≈ mean(peak, end), duration weight ≈ 0. Anticipatory utility is added before scheduled pleasures.

## Testable predictions

1. **Polarization:** in experience sampling, arousal predicts |valence| (intensity) better than valence itself. High-arousal moments amplify whichever source dominates attention, good or bad.
2. **LAP durability:** matched for initial intensity, calm/contented episodes show slower decay of positive affect over 1-2 h than excited ones.
3. **Switch-rate penalty:** within a feed session, enjoyment per item falls with switching rate. Urge (wanting) predicts return frequency better than end-of-session liking.
4. **Ideal-arousal fit:** liking ratings are higher when an activity's arousal matches the day's stated ideal (calm vs excited) than activity arousal alone predicts. This can be checked in experience-sampling data.
5. **Alternation (model prediction, no direct test found):** blocks of moderate-arousal engagement separated by detachment breaks yield more total weekly liking than sustained high arousal. The gain comes mostly through battery recovery and through ends placed at good moments (peak-end).
