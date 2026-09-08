# What award-winning robotics papers share

Observations from structural digests of the papers below, made with
`tools/paper_digest.py`. The papers are public; only their titles, ids, and
the patterns are listed here.

## Reading list

| Paper | Venue and award | arXiv |
|---|---|---|
| SpeedFolding: Learning Efficient Bimanual Folding of Garments | IROS 2022 best paper | 2208.10552 |
| Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ALOHA) | RSS 2023 | 2304.13705 |
| Universal Manipulation Interface (UMI) | RSS 2024 | 2402.10329 |
| Autonomously Untangling Long Cables | RSS 2022 best systems paper | 2207.07813 |
| LEAP Hand: Low-Cost, Efficient, and Anthropomorphic Hand for Robot Learning | RSS 2023 | 2309.06440 |
| GELLO: A General, Low-Cost, and Intuitive Teleoperation Framework | IROS 2024 | 2309.13037 |
| Flipbot: Learning Continuous Paper Flipping | ICRA 2023 | 2304.02253 |
| PolyTouch: A Robust Multi-Modal Tactile Sensor | ICRA 2025 best paper finalist | 2504.19341 |
| Autonomous Power Line Inspection with Drones via Perception-Aware MPC | IROS 2023 best paper | 2304.00959 |
| TARE: A Hierarchical Framework for Efficiently Exploring Complex 3D Environments | RSS 2021 best paper | roboticsproceedings rss17/p018 |
| FurnitureBench: Reproducible Real-World Benchmark | RSS 2023 | 2305.12821 |
| Teach a Robot to FISH: Versatile Imitation from One Minute of Demonstrations | RSS 2023 | 2303.01497 |
| Iterative Residual Policy for Goal-Conditioned Dynamic Manipulation | RSS 2022 best paper | 2203.00663 |
| NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration | ICRA 2024 best paper | 2310.07896 |
| TinyMPC: Model-Predictive Control on Resource-Constrained Microcontrollers | ICRA 2024 | 2310.16985 |
| MAC-VO: Metrics-aware Covariance for Learning-based Stereo Visual Odometry | ICRA 2025 best paper | 2409.09479 |
| Extrinsic Contact Sensing with Relative-Motion Tracking | ICRA 2021 best paper | 2103.08108 |
| Extended Tactile Perception: Vibration Sensing through Tools | IROS 2021 best paper | 2106.00489 |
| Translating Images into Maps | ICRA 2022 best paper | 2110.00966 |
| Time Optimal Ergodic Search | RSS 2023 | 2305.11643 |
| Advancing Humanoid Locomotion with Denoising World Model Learning | RSS 2024 | 2408.14472 |
| Open X-Embodiment: Robotic Learning Datasets and RT-X Models | ICRA 2024 best paper | 2310.08864 |

## Structure

- Section order converges on Introduction, Related Work, Problem Statement or
  System, Method, Experiments, Limitations, Conclusion. Limitations are either
  a named section or the last subsection of Experiments.
- Contributions are a numbered list at the end of the introduction, each a
  noun. Several papers state what is *not* new before listing what is.
- Abstracts end with a release or project-page sentence in nearly every
  systems paper.
- Page one carries a full-width Figure 1 in most hardware and systems papers,
  placed between the title block and the abstract or at the top of the first
  column. Its caption states the system, the task, the cost, and the headline
  number.

## Figures and captions

- Caption shape: a short title phrase, then panel-by-panel description
  (Left, Right, or (a) (b)), then the takeaway sentence.
- One system figure pairs a photograph with a diagram of the pipeline or
  cycle.
- Failure modes appear as a lettered list with counts in a table, or as a
  photo strip, and are discussed before the conclusion.
- Results tables give success as k/n fractions with the protocol columns
  needed to read them.

## Word choice

Counts over eighteen extracted papers:

| Form | Count |
|---|---|
| "as shown in Fig. N" | 72 |
| "(Fig. N)" parenthetical | 42 |
| "Fig. N shows / illustrates" | 24 |
| "we show" | 46 |
| "we propose" | 31 |
| "we present" | 29 |
| "we observe" | 27 |
| "note that" | 39 |
| "novel" | 61 |
| "robust" | 63 |

Em-dashes average under three per paper; semicolons about eight. Plain
verbs dominate the results and limitations prose: find, observe, attribute,
struggles with, fails to. Failures are reported as fractions in the same
sentence as the success. "Novel" and "robust" are common in this genre even
though writing guides advise against them; treat them as allowed field usage
rather than as evidence of quality.
