# Precedence and gate log — [PAPER SHORT NAME]

> Template. Copy to your paper folder as `precedence-log.md`. Append-only:
> newest entries at the bottom, never edit an old one. A paper folder is often
> untracked by git until submission, so this file is its only history.
>
> Two entry types. `[PRECEDENCE]` records a guidance conflict and how it was
> resolved. `[GATE]` records a run of the mechanical checks. No silent
> resolutions: if two rules disagreed and you picked one, it goes here.

## Guidance precedence

Highest tier wins, and the conflict is logged:

1. the venue's author guide
2. traceable style-spec rules
3. phrase-bank templates for the required move
4. anti-AI heuristics

---

[PRECEDENCE] [date] | section=[id] | conflict: [rule A, tier N] vs
  [rule B, tier M] | winner: [tier] | applied: "[the text as written]"
  Rationale: [one line, only if the choice is not obvious from the tiers]

[GATE] [date] | [what triggered this run: a section draft, a revision pass, a
  pre-submission check]
  - Citations: [n]/[n] resolved; [unresolved keys, or none]
  - Stance: [n] hits. [For each: the phrase, the section, its declared level,
    and whether you fixed the claim or judged it a false positive by register.]
  - Prose lint: em-dashes [n], semicolons [n] ([n] per 1000 words),
    contrast constructions [n], flagged vocabulary [list or none]
  - Integrity: [n] errors, [n] notes. [Missing figures, unresolved refs,
    bibliography order.]
  - Numeric diff vs [previous draft]: [numbers dropped / added, or "no
    statistic changed"]
  - Page count: [n] of [limit]

---

> Worked example of a useful entry, from a real revision. Delete it.

[GATE] 2026-01-15 | anti-AI pass over the full draft
  Measured before: 45 em-dashes (limit 3), ~30 semicolons (limit ~9),
  14 binary-contrast constructions (limit 2), 0 flagged vocabulary.
  Applied: em-dashes 45 -> 1; contrasts 14 -> 2, keeping the two that carry a
  real distinction; 7 clause-chaining semicolons converted to periods.
  Adjudication: the remaining semicolons are parenthetical statistics,
  enumeration separators, and one parallel-contrast caption, which are the
  reserved uses the rule permits. Raw count above the nominal limit accepted
  on that basis.
  All numbers, claims, and citations unchanged. Post-pass: stance 0 hits,
  citations 35/35, still 7 pages.
