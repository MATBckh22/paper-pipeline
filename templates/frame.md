# Frame — [PAPER SHORT NAME]

> Template. Copy to your paper folder as `frame.md` and fill it in, then mirror
> the same content into the `frame:` block of your paper-config. The
> `section-contracts` skill produces both. Delete these quote blocks when done.
>
> Validate with:
> `python3 skills/paper-pipeline/scripts/validate_config.py config.yaml --frame frame.md`

## Gap statement

> Exactly three moves, each present and each cited. The validator warns when
> the statement is missing; the skill refuses one that omits a move.

**Established.** [What prior work has shown, with citations and numbers.]

**Not established.** [What is missing, with citations that show the absence is
real. "No one has done X" is not enough on its own.]

**Why it matters.** [Who is affected and what the absence costs them. Name the
audience. Unstudied is not the same as worth studying.]

> No method-defending language anywhere above. The reader has not met your
> method yet, so any argument for it here is circular. The frame linter checks
> a pattern list, and the skill reads the whole frame for defences the list
> cannot catch.

## Delimitations

> `{claim, justification}` pairs. A delimitation without a justification is a
> validation error, not a warning. The justification must not restate the
> claim. These lines are contractual scope defence and are exempt from the
> no-method-defence rule above.

- **[Scope limit, stated plainly.]**
  Why: [what this buys the study, or why the excluded case does not change the
  conclusion. If the limit makes the task harder rather than easier, say so.]

- **[Scope limit.]**
  Why: [ ]

## Figure inventory

> Every figure names the claim it carries. A figure that exists "for
> illustration" does not enter the inventory. Status is planned, ready, or
> blocked.

| id | supports claim | status |
|---|---|---|
| fig-[name] | [the claim this figure carries, as a sentence] | planned |
| | | |

## Notes

> Optional. Record adjudications you had to make, so a later revision does not
> relitigate them.

-
