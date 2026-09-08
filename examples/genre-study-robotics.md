# Genre study — ICRA, IROS, and RSS, 2021-2025

> Worked example of `templates/genre-study.md`, filled in for robotics systems
> papers. Use it to see the level of detail a study needs; build your own for
> your own venue rather than borrowing these conclusions.

**Field:** robotics, weighted toward manipulation and systems papers
**Papers studied:** 22
**Selection rule:** best-paper winners and nominees at ICRA, IROS, and RSS,
2021-2025, plus four widely cited low-cost hardware papers included because
they occupy the same design point as the paper being written
**Compiled:** 2026-09 from public PDFs

## How this study was built

```bash
tools/paper_digest.py --arxiv 2208.10552 --arxiv 2304.13705 --arxiv 2207.07813 \
  --arxiv 2309.06440 --arxiv 2309.13037 --arxiv 2304.02253 -o digests/
tools/paper_digest.py --phrasing 'digests/*.txt'
```

Eighteen of the twenty-two extracted cleanly; the rest were read by hand
because their PDFs embed the text as images. Figure placement was read off the
PDFs, since the digests cannot see the page layout.

## Reading list

| Paper | Venue and award | Identifier |
|---|---|---|
| SpeedFolding: Learning Efficient Bimanual Folding of Garments | IROS 2022 best paper | 2208.10552 |
| Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ALOHA) | RSS 2023 | 2304.13705 |
| Universal Manipulation Interface (UMI) | RSS 2024 | 2402.10329 |
| Autonomously Untangling Long Cables | RSS 2022 best systems paper | 2207.07813 |
| LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand | RSS 2023 | 2309.06440 |
| GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework | IROS 2024 | 2309.13037 |
| Flipbot: Learning Continuous Paper Flipping | ICRA 2023 | 2304.02253 |
| PolyTouch: A Robust Multi-Modal Tactile Sensor | ICRA 2025 best paper finalist | 2504.19341 |
| Autonomous Power Line Inspection with Drones via Perception-Aware MPC | IROS 2023 best paper | 2304.00959 |
| TARE: Hierarchical Framework for Exploring Complex 3D Environments | RSS 2021 best paper | RSS 2021 p018 |
| FurnitureBench: Reproducible Real-World Benchmark | RSS 2023 | 2305.12821 |
| Teach a Robot to FISH: Versatile Imitation from One Minute of Demonstrations | RSS 2023 | 2303.01497 |
| Iterative Residual Policy for Goal-Conditioned Dynamic Manipulation | RSS 2022 best paper | 2203.00663 |
| NoMaD: Goal Masked Diffusion Policies | ICRA 2024 best paper | 2310.07896 |
| TinyMPC: Model-Predictive Control on Resource-Constrained Microcontrollers | ICRA 2024 | 2310.16985 |
| MAC-VO: Metrics-aware Covariance for Stereo Visual Odometry | ICRA 2025 best paper | 2409.09479 |
| Extrinsic Contact Sensing with Relative-Motion Tracking | ICRA 2021 best paper | 2103.08108 |
| Extended Tactile Perception: Vibration Sensing through Tools | IROS 2021 best paper | 2106.00489 |
| Translating Images into Maps | ICRA 2022 best paper | 2110.00966 |
| Time Optimal Ergodic Search | RSS 2023 | 2305.11643 |
| Advancing Humanoid Locomotion with Denoising World Model Learning | RSS 2024 | 2408.14472 |
| Open X-Embodiment: Robotic Learning Datasets and RT-X Models | ICRA 2024 best paper | 2310.08864 |

## Structure

- **Section order.** Introduction, Related Work, Problem Statement or System,
  Method, Experiments, Limitations, Conclusion. Nearly all follow it. Papers
  that move Related Work later are the ones whose contribution is a hardware
  design rather than an algorithm.
- **Where Related Work sits.** Section II in eighteen of twenty-two.
- **Problem Statement or Preliminaries.** About half use a short separate
  section to fix notation and state assumptions before the method.
- **Limitations.** Either a named section or the last subsection of
  Experiments, titled "System Limitations" or "Limitations and Conclusion".
  Only a few bury it in the conclusion, and those read as weaker.
- **Section count and page budget.** Six to eight sections. Experiments take
  the most space, typically a third of the paper.

## Contributions

- **Where the list sits.** End of the introduction, after the approach is
  named.
- **Form.** Numbered list in most, a bulleted list in several, and a single
  prose sentence beginning "The key contribution of this paper is" in a few.
- **How many.** Two to four. Three is most common; four is the practical
  ceiling before the list reads as padding.
- **Phrasing.** Nouns naming an artifact or a measurement, not activities.
  Verbatim: "A novel quadratic-programming algorithm that is optimized for
  MPC, is matrix-inversion free"; "An end-to-end robotic system for efficient
  smoothing and folding".
- **Papers that state what is not new.** GELLO opens its list with "the ideas
  behind GELLO are not new, rather our contributions can be summarized in the
  three points below". This disarms the obvious reviewer objection before it
  is raised, and it reads as confidence rather than weakness.

## Abstract

- **Move order.** Context, why it is hard, what we do and what it is called,
  quantified results.
- **Numbers.** Almost every abstract carries at least one measured result, and
  the strongest carry a direct comparison: "While prior work achieved 3-6
  Folds Per Hour, SpeedFolding achieves 30-40 FPH."
- **Last sentence.** A release statement or project URL in nearly every
  systems paper.
- **Length.** 150 to 250 words.

## Figures and captions

- **Figure 1.** A full-width teaser on page 1 in most hardware and systems
  papers, placed between the title block and the abstract or at the top of the
  first column. It shows the system in use, often as a photo strip of one full
  task cycle, sometimes paired with a scale comparison or a pipeline diagram.
- **Headline result in the caption.** Common in hardware papers. LEAP Hand's
  Figure 1 caption gives assembly time and cost; ALOHA's gives total system
  cost; GELLO's gives the bill of materials.
- **Caption shape.** A short title phrase, then panel-by-panel description
  keyed by "Left:", "Right:", or "(a)", then the takeaway. Verbatim from
  SpeedFolding: "SpeedFolding learns to fold garments from arbitrary
  configurations: Given a crumpled t-shirt, the robot unfolds using fling
  actions (1, 2), smooths it with a drag action (3)..."
- **Caption length.** Long by the standards of other fields, forty to a
  hundred words, and self-contained. Reading only figures and captions gives
  the story.
- **How failures are shown.** A lettered list of failure modes with counts per
  experimental tier (Untangling Long Cables), a photo of a failure case
  alongside successes (Flipbot panel E), or a table row per failure type
  (GELLO).
- **Figure count.** Seven to eleven, with one or two spanning both columns.

## Results reporting

- **How success is reported.** Percentages in the abstract, k/n fractions in
  the tables and body. "SGTM successfully detects that 8/12 cases are
  untangled" is the register.
- **Uncertainty.** Weaker than it should be. Many report a bare percentage
  with no n and no interval. A paper that reports n, an exact interval, and
  the test used stands out favourably, so this is a place to exceed the genre
  rather than match it.
- **Comparison tables.** The better ones carry protocol columns, media, trial
  counts, and sensing, and state in the caption that protocols differ so the
  numbers position rather than rank.
- **Failure analysis.** The strongest papers name and count failures.
  Verbatim from ALOHA: "the policy picks up the candy 10/10, pulls on both
  ends 8/10, while unwraps the candy 0/10". Reporting a zero is a mark of
  trustworthiness, not weakness.

## Word choice

Counts across the eighteen cleanly extracted papers.

| Form | Count |
|---|---|
| "as shown in Fig. N" | 72 |
| "(Fig. N)" parenthetical | 42 |
| "Fig. N shows / illustrates" | 24 |
| "In Fig. N, ..." | 25 |
| "see Fig. N" | 13 |
| "we show" | 46 |
| "we propose" | 31 |
| "we present" | 29 |
| "we observe" | 27 |
| "note that" | 39 |
| "novel" | 61 |
| "robust" | 63 |

- **Em-dashes per paper:** 2.8
- **Semicolons per paper:** 8.3
- **Tense.** Present for what the paper shows and for related work; past for
  what happened in the experiments.
- **Person.** First-person plural throughout. Passive only where the agent is
  irrelevant.
- **Field terms a general guide would flag but this genre accepts.** "Novel"
  and "robust", 61 and 63 uses. Both appear in award-winning titles. Treat
  them as allowed field usage; do not let a lint rule fight the convention.

## What I will copy

1. Page-1 full-width teaser whose caption carries the cost and the headline
   number, from LEAP Hand, GELLO, and ALOHA.
2. Numbered contributions as nouns naming artifacts and measurements, from
   SpeedFolding and TinyMPC.
3. A named Limitations section that separates design trades from unfinished
   work, from SpeedFolding and ALOHA.
4. Failures named and counted, including zeros, from ALOHA and Untangling
   Long Cables.
5. Abstract closing on a direct comparison in a unit the paper defines, from
   SpeedFolding.
6. Disclaiming what is not new before listing what is, from GELLO.

## What I will not copy

1. Bare success percentages with no n and no interval. Common in the sample
   and a genuine weakness; reporting n and an exact binomial interval costs
   one clause and buys credibility.
2. Comparison tables that rank across incompatible protocols without saying
   so. The caption must state whether it ranks or merely positions.
3. Stacking a secondary contribution into the abstract, which dilutes the
   single idea the paper should be remembered for.

## Open questions

- Whether the page-1 teaser is a venue convention or a hardware-paper
  convention. The sample conflates the two, since most teaser papers are also
  hardware papers. Resolve by checking algorithm-only best papers at the same
  venues.
- How many papers report repeatability or variance rather than a single
  success rate. None in this sample do, which is either a real gap or a
  selection artifact of reading manipulation papers.
