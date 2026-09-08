# Anti-AI writing heuristics — merged, deduplicated (tier 4)

Single rule set merging `academic-paper/references/writing_quality_check.md`
(**WQC**) and `conorbronsdon/avoid-ai-writing` `SKILL.md` (**AAW**), which
overlap materially (brief §2.5). Each rule is tagged with its source and
whether it is `[mechanical]` (pattern/count detectable) or `[judgment]`
(requires reading for meaning).

**Precedence position: BOTTOM (tier 4).** These are quality heuristics, not
laws. Academic prose legitimately uses formulaic constructions; reviewers
read for the move, not for novelty of phrasing. When any higher tier — venue
guide (1), traceable style-spec rule (2), phrase-bank template for the
required move (3) — calls for a construction this file proscribes, the higher
tier wins and the conflict is logged (see draft-guard). These rules improve
prose; they never exist to evade detectors (WQC's design boundary, kept).

**Optional mechanical assist:** when the `avoid-ai-writing` repo is present,
`node detector/validate.js` runs its 51-type engine over a draft; treat its
output exactly like linter hits — candidates for judgment, not verdicts.

## 1. Vocabulary `[mechanical]` (WQC ∪ AAW tier1-3 — heavy overlap, merged)

Flag-and-ask terms (not banned; ask "is this the most precise word?"):
delve, tapestry, landscape, pivotal, crucial, foster, showcase, testament,
navigate, leverage, realm, embark, underscore, multifaceted, nuanced,
comprehensive, robust, intricate, cornerstone, paradigm, synergy, holistic,
streamline, cutting-edge, groundbreaking, seamless, transformative.

**Discipline exception (WQC, kept):** standard field terminology is exempt —
"robust estimator" (statistics), "landscape" (literal, ecology), "paradigm
shift" (philosophy of science), "robust" in robotics control contexts.

## 2. Punctuation `[mechanical]`

- Em dash: ≤ 3 per paper, prefer 0–1; quotes keep their originals (both).
- Semicolons: ≤ 2 per 1000 words (WQC).
- No 2+ consecutive paragraphs opening colon-into-list (WQC); colon-into-triple
  is `[judgment]` — three-item lists are often simply true in technical prose
  (AAW carve-out, kept).

## 3. Openers, filler, meta-commentary

- Throat-clearing deletions (both): "It's important to note", "It is worth
  mentioning", "In the realm of", "In today's rapidly evolving", "It goes
  without saying", "In order to"→"To", "When it comes to", "As a matter of
  fact", "With that being said". `[mechanical]`
- Meta-commentary ("This section will discuss…") — do the thing instead.
  **Exception (WQC, kept): intro roadmap sentences are standard practice.**
  `[judgment]`
- Template/transition phrases, filler, hollow intensifiers (AAW): "Moreover,"
  chains, "It is essential to", "plays a vital role", "very/truly/really"
  padding. `[mechanical]`
- Rhetorical-question and speculative-scenario openers (AAW). `[judgment]`

## 4. Structure

- Rule-of-three compulsion: use as many points as the evidence warrants; 2 is
  fine, 5 is fine (WQC). `[judgment]`
- Uniform paragraph length / low burstiness: 5+ consecutive sentences in a
  narrow word-count band → vary (both). Methods sections legitimately run
  uniform (WQC per-section targets, kept). `[mechanical]` for detection,
  `[judgment]` for the fix.
- Synonym cycling: one name per concept per section; technical repetition is
  clarity (both — also enforced at tier 2 by most style specs, where it wins
  automatically). `[judgment]`
- Binary-contrast tic ("not X — it's Y"): ≤ 2 per paper (both). `[mechanical]`
- Mirror structure: identical internal rhythm in every section (WQC).
  `[judgment]`
- Negation chains, bullet lists of bare noun phrases, inline-header list
  inflation (AAW). `[mechanical]` where AAW's detector maps them, else
  `[judgment]`.

## 5. Inflation and hedging

- Significance/novelty inflation: "groundbreaking", "paradigm-shifting",
  self-labeled importance (AAW; WQC vocabulary overlap). Show, don't label.
  `[mechanical]` for the marker words, `[judgment]` for unlabeled inflation.
- Hedge-stacking ("may potentially suggest") and confidence stacking
  ("clearly and unambiguously demonstrates") (AAW). **Interaction rule:
  hedging LEVEL is governed by the section's declared stance (tier above this
  file, via stance-lexicon); this rule only removes redundant doubling within
  the level.** `[mechanical]`
- Vague attribution ("experts agree", "studies show" uncited) (AAW) — in
  academic prose this is a citation failure first: cite or cut. `[mechanical]`
- Generic conclusions / future-narrative closers ("As technology continues to
  evolve…") (AAW). `[mechanical]`

## 6. Artifacts `[mechanical]` (AAW)

Unfilled placeholders ("[insert…]", "TODO"), chatbot citation-markup leaks,
cutoff disclaimers ("as of my knowledge…"), AI-tool URL parameters,
sycophantic tone. Always errors — no judgment stage needed.

## Dropped in the merge (register mismatch)

AAW rules for conversational/social registers — engagement-bait closers,
hashtag stuffing, recap-flattery openers, wall-of-text reply rules — do not
apply to academic manuscripts and are excluded rather than tagged.
