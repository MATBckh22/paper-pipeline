# Review ledger — [PAPER SHORT NAME]

> Template. Copy to your paper folder as `review-ledger.md`. Append-only, one
> block per round. The ledger is the termination predicate's evidence: without
> it there is no loop, only opinions.
>
> Rounds are read-only. Edits go through the drafting step between rounds,
> never during one.

## Round [N] — [date]

**Panel:** [how the review was produced: fresh-context subagents with N
temperaments, an external reader, a mock-review run. Note what context the
panel was given, and say plainly if fresh context was not enforced.]

**Attacks returned:** [n], ranked by severity x likelihood. Ties break toward
earlier sections.

> Severity: `revision` costs a rewrite inside the section (1); `section` costs
> the section's contract, meaning its stated output no longer holds (2);
> `paper` costs the frame, meaning the gap statement or a delimitation fails (3).
> Likelihood: low (1), med (2), high (3).

### Rank [n] — [attack id] ([target], [severity] x [likelihood] = [score])

**Attack:** [the reviewer's point, stated at its strongest. If you cannot state
it at full strength, you are not ready to answer it.]

**Response: [ACCEPT | DEFEND | RETREAT].**
[For ACCEPT: what changes, and where.]
[For DEFEND: the evidence that answers it. A defence that adds evidence to the
draft counts as an accept in form.]
[For RETREAT: the narrower claim you now make. Retreat is a legitimate outcome,
not a failure; the reviewer is the one who will notice if you rationalize.]

**Action item:** [who does what, and by when. Mark author homework explicitly.]

---

## Round [N] termination assessment

> Stop iff no new attack of severity at least `section` AND likelihood at least
> `med` was accepted or retreated this round. Attacks that were *defended* do
> not block termination; new high-severity attacks that forced a change do.

[n] attacks accepted or retreated at severity >= section with likelihood >= med
-> **[the loop continues | the loop terminates]**.

Rounds used: [n] of [max].

> Hitting the round cap is not a clean exit. It means the contested object is
> the frame rather than the prose: go back to the frame and outline, and
> re-examine the gap statement and delimitations before drafting again.
