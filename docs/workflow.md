# The pipeline, stage by stage

Everything runs locally on the author's machine from the repository root.
Nothing is sent to a service except the downloads in stage 1. Dates and
outcomes of every pass go into a plain-text log beside the manuscript
(`precedence-log.md` in the skills' vocabulary), because a paper folder is
often untracked by git until submission and the log is its only history.

## 1. Read the genre

- Fetch the writing guide you follow, in full, with
  `tools/fetch_text.py URL -o guide.txt`. A summary of a guide is not the
  guide.
- Collect ten to twenty papers that won or were nominated for awards at the
  target venue over the last five years. Download and digest them:
  `tools/paper_digest.py --arxiv ID ... -o digests/`. Read the digests for
  section order, where Figure 1 sits, how captions are shaped, how
  contributions are phrased, and how limitations are admitted. Run
  `--phrasing` for the verbs and figure-reference forms the genre uses.
- Record the findings in a copy of `templates/genre-study.md`. Its last two
  sections are the ones that matter: what you will copy, which becomes
  candidate rules in your style spec, and what you will not, which marks the
  boundary between convention that serves the reader and convention that is
  merely habit. `examples/genre-study-robotics.md` is a filled-in study.
- Look at your own figures before writing captions.

## 2. Plan

- Run the `section-contracts` skill. It elicits a gap statement in three
  moves (established, not established, why it matters), delimitations with
  justifications, a figure inventory with the claim each figure carries, and
  a per-section contract: inputs, the belief the reader holds afterwards, and
  the rhetorical stance the evidence licenses.
  Start from `templates/frame.md` and `templates/outline.md`.
- Validate: `skills/paper-pipeline/scripts/validate_config.py config.yaml --frame frame.md`.
- If you have papers you admire, run `exemplar-spec` once to turn quoted
  passages into traceable style rules.

## 3. Draft

- One section at a time with `draft-guard`, under the precedence order in the
  config: venue guide, traceable style rules, phrase bank, anti-AI heuristics.
- Make every later change as an exact-string replacement that asserts the
  target occurs once. This keeps edits auditable and lets a previous version
  be rebuilt by replay.
- Keep one name per concept; keep every number identical wherever it appears.

## 4. Gate

`tools/run_gate.sh draft.tex L3` runs three checks:

1. `check_draft.py`: citation resolution and the stance scan against the
   declared level. Run the whole draft at the paper's highest declared level
   and section extracts at their own levels.
2. `lint_prose.py --strict`: the mechanical anti-AI and style limits.
3. `tex_integrity.py`: references, figure files, brace and environment
   balance, bibliography order, unsorted multi-citations.

Then `tex_integrity.py new.tex --diff-numbers old.tex` to prove that a prose
pass changed no statistic. Record the outcome in a copy of
`templates/precedence-log.md`, which also holds every guidance conflict you
resolved while drafting.

## 5. Review

- `review-response` runs an adversarial panel in fresh context, ranks attacks
  by severity times likelihood, and requires a typed response to each: accept,
  defend with evidence, or retreat the claim. Fixes route back through stage 3
  and the gate. Record each round in a copy of `templates/review-ledger.md`;
  the ledger is what the termination test reads.
- `mock-review` gives a single reviewer-style read when a full round is too
  much.

## 6. Submit

- Compile on the real template; the tools do not compile.
- Anonymity sweep for double-blind venues: names, affiliations, grant ids,
  identifying URLs, "our previous work", PDF metadata.
- Page count against the hard limit, including references.
- Disclose AI assistance where the venue requires it.
