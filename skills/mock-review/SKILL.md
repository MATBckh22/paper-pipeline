---
name: mock-review
description: Use when the user wants a draft paper, thesis chapter, or abstract critiqued as a peer reviewer would - "review my paper", "act as reviewer 2", "will this get accepted", "find weaknesses", "mock review", "pre-submission check". Produces a structured ICRA/IROS/RSS-style review with ranked weaknesses, scores, and a prioritized fix list. Critique only - does not rewrite the text.
---

# Mock Review

Simulate the review a manuscript would actually receive at a top robotics
venue (ICRA/IROS/RSS/RA-L). The goal is to surface every objection *before* a
real reviewer does. Be harsh but fair: every criticism must be specific,
located, and actionable. No generic filler ("could be clearer") — say what,
where, and why it fails.

## Procedure

1. **Read the entire target first** (all files/chapters given). Never review
   from a summary or from memory of an earlier version.
2. Identify the paper's claimed contributions verbatim. The review judges the
   paper against *its own claims* — not against a different paper you wish
   they'd written. Flag separately any claim the evidence doesn't support.
3. Apply the reviewer priors below.
4. Output the structured review (format at bottom). Rank weaknesses by how
   likely they are to cause rejection, not by order encountered.

## Robotics-reviewer priors (what real reviewers attack)

**Novelty and framing**
- "What is new here?" must be answerable from the intro alone. Integration of
  known components is acceptable *only* if framed as a systems/empirical
  contribution with a finding no prior work provides.
- Title/abstract promises vs. delivery: any promised-but-absent element
  (a method named but not evaluated, a capability claimed but not shown) is a
  near-automatic reject. Hunt for these first.
- Missing citations: name the 3-5 works a knowledgeable reviewer would expect
  cited; check whether the closest competitor is compared against fairly.

**Experimental rigor**
- Sample size and statistics: n per condition, correct test for the data
  shape (normality checked?), CIs on rates, median for skewed data. Wide CIs
  are not a flaw if stated; unstated ones are.
- Baselines/ablations: is any comparison possible that the authors avoided?
  If the system has removable components, why is there no ablation? (If the
  paper argues the system *is* the ablation of a richer system, check the
  argument is explicit.)
- Confounds: single operator, single session, fixed placement, ordering
  effects, self-classification bias. Which are controlled, which acknowledged,
  which silently ignored?
- Generality: does the evaluation envelope support the breadth of the claims?
  Quote any sentence whose claim exceeds the tested conditions.
- Reproducibility: could a competent lab rebuild this from the paper + repo?
  What's missing (parameters, protocol, code/data availability)?

**Systems-paper specifics**
- Is there a metric beyond success rate (throughput, repeatability, cost,
  time-to-deploy)? Papers with only a success rate get "limited evaluation".
- Failure analysis: taxonomized and counted, or anecdotal?
- Human-in-the-loop: does an operator's involvement inflate the headline
  numbers? Is their role (control vs. crutch) stated honestly?
- Cost/accessibility claims: backed by actual figures (BOM, comparison), or
  vibes?

**Presentation**
- Can the story be reconstructed from figures + captions alone?
- Numbers consistent across abstract/body/tables/conclusion (check 3 at
  random, report mismatches).
- Page budget, anonymity, venue formatting compliance if venue is known.

## Output format

```
## Summary (3-5 sentences proving the paper was read; neutral tone)

## Strengths (3+, specific, with locations)

## Weaknesses (ranked by rejection risk)
W1. [MAJOR/MINOR] <claim of defect> — <location> — <why it matters> — <what would fix it>
...

## Questions to the authors (things a rebuttal must answer)

## Missing/questionable citations

## Minor issues & typos (location: issue, compact list)

## Scores (1-5, venue style)
Novelty: n/5 — one-line justification
Technical soundness: n/5 — ...
Experimental rigor: n/5 — ...
Clarity: n/5 — ...
Overall: <reject / weak reject / borderline / weak accept / accept> — the
one issue that most determines this rating

## Priority fix list (ordered; effort estimate per item)
```

## Rules

- Critique only — do not rewrite the manuscript in this mode. If asked to fix
  the findings afterward, that's a separate pass (use the academic-writing
  skill's rules for it).
- Verdicts must be honest, including "this would likely be rejected because
  X". An inflated mock review is worthless; say the hard thing.
- If reviewing for a specific venue, state its acceptance norms and judge
  against them (e.g., ICRA ~40-45% acceptance, values working systems and
  honest evaluation; RSS values depth and rigor over breadth).
- If multiple rounds are requested, act as three reviewers with different
  temperaments (skeptic on novelty, methodologist on stats, systems person on
  practicality) and write a meta-review reconciling them.
