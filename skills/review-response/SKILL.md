---
name: review-response
description: Use to run and manage adversarial review rounds on a drafted paper with a paper-config - "run the review loop", "attack my draft", "process the reviewer findings", "should I defend or concede this point". Wraps a review panel (academic-paper-reviewer when installed, mock-review otherwise) with fresh-context enforcement, attack ranking, typed responses including retreat, and a termination predicate. Not a drafting skill - fixes route back through draft-guard.
---

# Review Response

Wraps the review panel — `academic-paper-reviewer` (5-seat panel with Devil's
Advocate and `re-review` mode) when installed, `mock-review` otherwise. The
panel generates attacks; this skill adds what the panel lacks (brief §3.7):
structural context isolation, a ranking, a typed response set **including
retreat**, and a stopping rule. It never replaces the panel's own protocol.

## 1. Fresh-context enforcement — structural, not instructional

When `review.fresh_context` is true: the review MUST run in a context that
contains the **draft and the outline and nothing else**. If it can see the
drafting rationale it inherits the drafting blind spots and confirms them
back.

Enforce by construction — dispatch the panel as a subagent whose prompt
contains only: the draft path, `outline.md`, the venue line from the config,
and the panel's own instructions. Excluded by construction: the paper-config
frame block, `precedence-log.md`, style-spec, this session's drafting
history, and every prior round's responses (the panel's own `re-review` mode
governs what round-1 material it consumes). Telling a same-context reviewer
to "ignore the context" does not satisfy this — if a subagent is impossible,
tell the author fresh context is not enforced this round and record that in
the ledger.

## 2. Attack ranking

Every attack from the panel is recorded as:

```
- id: R2-3
  target_section: "5"        # section id from the outline, or "frame"
  severity: section          # revision (1) | section (2) | paper (3)
  likelihood: high           # low (1) | med (2) | high (3)
  text: <the attack, verbatim>
```

Severity scoping: `revision` costs a rewrite within the section; `section`
costs the section's contract (its `output` no longer holds); `paper` costs
the frame (gap statement or a delimitation fails). Rank by
severity × likelihood, descending; process in rank order. Ties break toward
the attack targeting the earlier section (upstream damage propagates).

## 3. Typed responses — retreat is first-class

For EVERY attack, present all three options from `review.responses_allowed`
before recommending one:

- **accept** — the attack is right; fix as directed (route via draft-guard).
- **defend** — the attack fails; write the rebuttal and cite the evidence in
  the draft that defeats it. A defence that needs evidence not in the draft
  is not a defence — it is an `accept` (add the evidence) in disguise.
- **retreat** — weaken the claim or narrow the scope: lower the section's
  stance level, add a delimitation, or shrink the claimed envelope. Retreat
  edits the config (stance/delimitations) AND the prose, via
  section-contracts then draft-guard.

**L4 rule:** when the attacked section's effective stance is L4,
default-suggest retreat to L3 BEFORE composing any defence. Only defend an
L4 claim when the draft already contains the direct, controlled,
alternatives-excluded evidence the L4 predicate requires — and say so by
pointing at it. A process that only generates defences trains the author to
rationalize, and the reviewer is the one who will notice.

Record every attack + chosen response + rationale in `review-ledger.md`
beside the config, append-only, one block per round.

## 4. Termination predicate

After each full round, stop the loop iff: **no new high-severity attack
(severity ≥ section AND likelihood ≥ med) was accepted or retreated from this
round.** New attacks that were *defended* do not block termination; new
high-severity attacks that forced a change do — the paper is still moving.

Hard backstop: `review.max_rounds`. Hitting it is NOT a clean exit — it means
something structural is wrong. Surface it as: "Round N of N consumed and
high-severity attacks still land. The contested object is the frame, not the
prose — return to section-contracts and re-examine the gap statement and
delimitations before any further drafting." Never silently stop at the cap.

## Red flags

- A round with zero retreats and zero accepts across 5+ attacks → the
  responses are rationalizations; re-read §3 and re-adjudicate the top three
  attacks with retreat considered first.
- "The reviewer misunderstood" as a defence → a misunderstanding reviewer is
  data about the prose; the response is accept (fix the prose), not defend.
- Editing the draft during a review round → rounds are read-only; edits go
  through draft-guard between rounds.
- Skipping the ledger "to save time" → the ledger is the termination
  predicate's evidence; no ledger, no loop.
