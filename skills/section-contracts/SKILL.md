---
name: section-contracts
description: Use before drafting any paper - to build or revise the paper's frame (gap statement, delimitations, figure inventory) and outline (per-section I/O contracts, stance levels) in a paper-config file. Triggers - "plan my paper", "build the outline", "set up section contracts", "frame the paper", or when a pipeline reaches its planning stage and no validated frame+outline exists. Also run after any outline change to re-validate the dependency DAG.
---

# Section Contracts

Produces `frame.md`, `outline.md`, and the `frame` + `outline` blocks of the
paper-config (schema: `.claude/skills/paper-pipeline/schemas/paper-config.schema.md`).
Runs standalone, or as a plug-in at an external orchestrator's planning gate
(see `paper-pipeline/README.md`, optional integration).

Mechanical validators live in `.claude/skills/paper-pipeline/scripts/`; this
skill is the elicitation and judgment layer on top of them.

## Procedure

### 1. Frame elicitation

**Gap statement** - exactly three moves, each present and cited:
1. What is established (with citations)
2. What is not established (with citations showing the absence is real)
3. Why the absence matters (audience named)

Refuse a gap statement missing any move. Do not accept "no one has done X"
without move 3 - unstudied is not the same as worth studying.

**Delimitations** - `{claim, justification}` pairs. A delimitation without a
justification is **rejected, not warned** (the validator enforces this too).
Push back on justifications that restate the claim.

**Figure inventory** - `{id, supports_claim, status}` per planned figure.
Every figure names the claim it carries; a figure that exists "for
illustration" does not enter the inventory.

### 2. Frame lint - the forward-reference gate

The frame must contain **no method-defending language**: the reader has not
met the method, so any defence of it is circular. Two stages, both mandatory:

1. **Lexical pass**: run
   `python3 .claude/skills/paper-pipeline/scripts/validate_config.py <config> --frame <frame.md>`
   (or `framelint.scan_file` directly). Hits come back with line offsets.
2. **Judge stage**: (a) adjudicate every hit - a pattern match inside a
   quotation or a claim *about the literature's* method choices is a false
   positive; say so and move on. (b) Read the whole frame once asking one
   question per sentence: "does this sentence argue for OUR method or
   design?" A sentence can do that without any listed lexeme (see
   `tests/fixtures/evasive_frame.md`) - flag it even though the linter was
   silent. Confirmed violations move to the methodology section or are
   deleted; never "soften" them in place.

   Scope note (adjudicated 2026-08-30): the prohibition covers the frame's
   NARRATIVE portions - gap statement and literature themes - which the
   reader meets before the method. Delimitation justification lines are
   contractual scope-defence (the schema requires them) and are exempt;
   linter hits inside them are false positives by register.

### 3. Outline elicitation

Per section: `id`, `heading`, `inputs` (section ids or frame artifacts the
section assumes), `output` (one sentence: what the reader believes after it),
`figures`. The `output` is a belief, not a topic - reject "describes the
perception system"; accept "reader believes the grip target is localized to
under 5 mm".

### 4. Stance assignment - evidence first, intent second

For each section, elicit the `evidence_note` BEFORE asking for the intended
stance. Then:

1. Derive the ceiling: `stance.suggest_ceiling(evidence_note, lexicon)` with
   `.claude/skills/paper-pipeline/data/stance-lexicon.yaml` (apply the
   discipline overlay from the config's venue). If no cue matches, adjudicate
   yourself against the four evidence predicates in the lexicon and record
   which predicate you applied.
2. Elicit the author's intended level.
3. Clamp: effective = min(intent, ceiling). **When clamped, tell the author
   which section was clamped, from what to what, and which evidence cue set
   the ceiling.** The author may upgrade the evidence (new experiments, added
   citations) to raise the ceiling; they may never raise the stance past it.

This inversion is the point: intent declared first is how a section gets
written at L4 on L2 evidence - the most predictable reviewer opening there is.

### 5. DAG validation

Run `validate_config.py <config>`. For every `ORDER_VIOLATION`, present the
offending edge AND its transitively affected sections, then offer exactly two
remedies: **reorder** (move the dependency earlier) or **restate** (rewrite
the section so it no longer assumes the later material). For every `CYCLE`,
present the full cycle path and identify which edge is the weakest assumption
to break. `FIG_ORPHAN` errors mean the figure leaves the inventory or a
section adopts its claim; `FIG_PROSE_ONLY` warnings need only author
confirmation - some claims legitimately carry on prose.

### 6. Emit

Write `frame.md` and `outline.md` beside the config; write the `frame` and
`outline` blocks into the config; re-run the validator; report `clean` or
stop. Never hand a config with errors to draft-guard.

## Red flags

- Author supplies stance levels before evidence notes → re-order the
  elicitation; do not silently accept.
- A "justified" delimitation whose justification is "for simplicity" → push
  for the real reason or drop the delimitation.
- Validator errors "to fix later" → there is no later; draft-guard refuses
  configs with errors.
