# style-spec — TEMPLATE (replace with your own; built by the exemplar-spec skill)

Normative craft rules derived from third-party exemplars listed in
`exemplar-library.md`. Consumed by draft-guard: `Traceable` rules are
precedence tier 2; `Asserted` rules sit between tiers 3 and 4. Every
Traceable rule must cite a passage id `(source: P<n>)` that exists in the
library and holds a quoted passage; `scripts/ppl/stylespec_validate.py`
enforces this.

## Traceable

- Close the abstract with a direct prior-art comparison on the axis the paper
  wins, stated in a defined unit (source: P1)
- Carry the headline result in one sentence that couples cost, time, and
  reliability as numbers, not adjectives (source: P2)
- State the cost or accessibility constraint as a requirement before naming
  the system (source: P3)

## Asserted

- Success rates carry n and an exact binomial confidence interval at first
  mention.
- Losing numbers are pre-framed before they appear; the reader never
  discovers them.
- One name per concept for the whole paper.
- Limitations get a named section with causes attributed: design trade or
  unfinished work.
