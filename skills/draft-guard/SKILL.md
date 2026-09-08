---
name: draft-guard
description: Use whenever drafting or revising a section of a paper that has a paper-config - it wraps the drafting step with guidance-precedence resolution and a per-section quality gate (stance vs hedging, figure references, citation resolution). Triggers - "draft section X", "write the results section", "revise section 3 of the paper", or when an orchestrator dispatches a drafting step and a paper-config exists. Not for papers without a config - run section-contracts first.
---

# Draft Guard

Wraps drafting. Two jobs (brief §3.6): deterministic precedence resolution
across the four guidance tiers, and a per-section gate before any section is
declared done. Refuses to run without a validated paper-config
(`validate_config.py` clean) — outline errors compound at draft time. Honors
`drafting.one_section_at_a_time`: when true, decline requests to draft
multiple sections in one pass.

## Guidance precedence — deterministic, four tiers, highest wins

1. **Venue author guide + field convention** (from `paper.venue_style_guide`
   and the venue's actual template rules)
2. **`style-spec.md`, `traceable` partition only** (exemplar-backed rules;
   `asserted` rules sit between tiers 3 and 4 — author preference beats
   generic heuristics but never beats an exemplar-backed or phrase-bank move)
3. **Phrase-bank move templates**
   (`.claude/skills/paper-pipeline/data/phrase-bank.yaml`, indexed
   move × stance level — use the section's *effective* stance from the config)
4. **Anti-AI heuristics**
   (`.claude/skills/paper-pipeline/rules/anti-ai-rules.md` — the merged,
   deduplicated set; do NOT also run WQC and AAW separately)

Tier 4 is at the bottom on purpose: reviewers read for the move, not for
novelty of phrasing. When a heuristic proscribes a construction the phrase
bank supplies for the required move, the phrase bank wins.

**Log every resolution.** Append to `precedence-log.md` beside the config:

```
[PRECEDENCE] section=5.2 | conflict: anti-ai "formulaic transition" (T4)
  vs phrase_bank compare_prior/L3 (T3) | winner: T3 | applied: "Against the
  range reported by..."
```

The log is how the author audits decisions and how the tiers get tuned
against real conflicts instead of guesses. No silent resolutions.

**Outside the stack:** the descriptive Style Profile from
`shared/style_calibration_protocol.md` (Schema 10) shapes *voice* (sentence
rhythm, vocabulary preference) and is applied under its own protocol's
priority rules. It never overrides tiers 1–3 and never legitimizes a tier-4
violation; when profile and tiers collide, the tiers win and the collision is
logged like any other.

## Per-section gate — all three pass before the section advances

1. **Stance discipline.** Run
   `python3 .claude/skills/paper-pipeline/scripts/check_draft.py <draft> --bib <bib> --stance <effective_level>`.
   Every `STANCE_EXCEEDED` hit is rewritten down to the declared level using
   the phrase bank's entries for that move at that level — or the author
   upgrades the evidence and section-contracts re-derives the ceiling. Never
   fix by deleting the claim's hedge context while keeping the claim.

2. **Figure references survive without the figure.** For every in-text figure
   reference, read the surrounding prose with the figure hidden: the sentence
   must still state its point ("the traces cluster tightly
   (Fig. 4)"), never delegate it ("see Fig. 4"). `[judgment]` — no script.

3. **Citations resolve — every round, not once at the end.** The same
   `check_draft.py` run covers this. Any `CITE_UNRESOLVED` is fixed before
   the section advances: locate the real entry, or delete the claim that
   needed it. Never leave a citation "to fix at submission"; fabricated and
   drifted references are the highest-cost failure in LLM-assisted academic
   writing. `year-suffix-drift` findings mean the a/b disambiguation is
   inconsistent between text and bibliography — fix both sides.

## Red flags

- "Run the gate once at the end" → the gate is per section, per round.
- A stance fix that swaps "we show" for "we would argue" but keeps an L4
  claim sentence intact → the *claim* must weaken, not just the verb.
- Untracked precedence decisions ("I just picked the nicer phrasing") → log
  or it didn't happen.
- Asked to draft the whole paper in one pass with
  `one_section_at_a_time: true` → decline, cite the config.
