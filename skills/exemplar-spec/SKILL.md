---
name: exemplar-spec
description: Use to build or extend an author's normative style specification from exemplar papers they admire - "set up my style spec", "learn from these papers", "what makes this paper read well", or before a paper's first drafting pass when inputs.style_spec does not exist yet. Runs once per author (not per paper); re-run only to add exemplars or revise rules.
---

# Exemplar Spec

Builds `style-spec.md` + `exemplar-library.md` from 4–6 papers the author
selects. **Complements style calibration
(`shared/style_calibration_protocol.md`), never replaces it**: calibration is
descriptive — "how does this author write" from their own samples; this is
normative — "what does good look like in this field" from third-party
exemplars. Statistical mimicry of your own voice cannot teach you a move you
have never made (brief §2.1). Runs once per author; the library is personal.

## Elicitation — per exemplar paper

1. **Citation and venue.** Full reference; why the author picked it (one line).
2. **Three quoted passages**, each with location (section/page). Quote
   verbatim — the passage IS the evidence a traceable rule will cite.
3. **Per passage, the *move***: the rhetorical function the passage performs —
   what it does to the reader — never a summary of its content.
   - Accept: "concedes the rival system's superiority on the headline metric
     before shifting the comparison axis to cost"
   - Reject: "talks about how their system compares to a competitor system" (content
     summary — push back and re-elicit)
4. **One thing the paper does the author would NOT copy.** Mandatory — it
   forces critical reading and marks the spec's boundary.

## Output formats

`exemplar-library.md` — one block per passage:

```
## [P1] Avigal et al., "SpeedFolding", IROS 2022
> While prior work achieved 3-6 FPH, SpeedFolding achieves 30-40 FPH...
Move: makes throughput the headline by comparing directly on the axis the
  paper wins, in the first paragraph.
Would-not-copy: hardware-dependent speed claims stated without CI.
```

`style-spec.md` — rules partitioned, partition preserved verbatim in the file:

```
## Traceable
- Lead the results section with the metric the paper wins on, compared
  directly against prior art's numbers (source: P1)
- Concede the rival's headline metric before shifting the comparison axis
  (source: P4, P7)

## Asserted
- Never open a paragraph with "However".
- Numbers in text use the same precision as in their table.
```

**Keep the partition.** Downstream (draft-guard) weights them differently —
`traceable` is tier 2, `asserted` sits below phrase-bank — and the author
needs to see which of their rules are invented.

## Validation — run before accepting the spec

`stylespec_validate.check(spec_text, library_text)`
(`.claude/skills/paper-pipeline/scripts/ppl/stylespec_validate.py`).
**Reject any `Traceable` rule whose citation does not resolve to a quoted
passage in the library** — no source ref, a P-id not in the library, or a
library block with no verbatim quote. The fix is either to add the missing
passage (with the author supplying the quote) or to move the rule to
`Asserted`, honestly. Never fabricate a passage to save a rule.

## Red flags

- Rules extracted from papers the author never named → not an exemplar; drop.
- A "move" that is a topic description → re-elicit until it names the
  rhetorical function.
- Skipping the would-not-copy item ("I like everything about it") → push
  once; if the author insists, record "none identified" explicitly.
- More than ~15 traceable rules from 4 papers → the spec is drifting into a
  style guide transcription; keep only rules with quoted evidence.
