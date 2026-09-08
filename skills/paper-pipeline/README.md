# paper-pipeline (skill)

Shared data, rules, schema, and validators used by the sibling skills
`section-contracts`, `exemplar-spec`, `draft-guard`, and `review-response`.
Nothing here orchestrates stages; each part runs standalone or when a skill
calls it.

## Parts

| Part | Path |
|---|---|
| paper-config schema and example | `schemas/paper-config.schema.md`, `schemas/paper-config.example.yaml` |
| stance lexicon (L1 report, L2 suggest, L3 argue, L4 assert) | `data/stance-lexicon.yaml` |
| phrase bank (moves x stance levels) | `data/phrase-bank.yaml` |
| style-spec and exemplar-library templates | `data/style-spec.md`, `data/exemplar-library.md` |
| anti-AI writing heuristics | `rules/anti-ai-rules.md` |
| method-defence patterns for the frame linter | `rules/method-defense-patterns.txt` |

## Validators

Python 3.9 or newer, standard library only; PyYAML is used when present and
the bundled `miniyaml` subset parser otherwise. Keep configs inside the YAML
subset described in the schema so both parsers agree.

- `scripts/validate_config.py CONFIG [--frame FRAME.md] [--discipline D]`
  Structure checks, outline dependency graph (forward references with their
  transitive blast radius, full cycle paths), figure-to-claim reconciliation,
  stance clamp notices, and the frame linter's lexical pass.
- `scripts/check_draft.py DRAFT --bib BIB [--stance L2] [--discipline D]`
  Citation resolution (LaTeX, pandoc, and author-year forms, with year-suffix
  drift detection) and a realized-hedging scan against the declared stance.
  Run after every edit.
- `scripts/ppl/stylespec_validate.py` (used by `exemplar-spec`)
  Every rule in a style-spec's Traceable section must cite a passage id that
  exists in the exemplar library and holds a quoted passage.

## Lifecycle

```
exemplar-spec (once per author) --> style-spec.md + exemplar-library.md
section-contracts (per paper)   --> frame.md, outline.md, config frame/outline
draft-guard (per section)       --> drafted section + precedence-log.md
review-response (per round)     --> review-ledger.md, routed fixes
```

## Guidance precedence

When two sources of guidance conflict, the higher tier wins and the conflict
is logged: (1) the venue's author guide, (2) traceable style-spec rules,
(3) phrase-bank templates for the required move, (4) anti-AI heuristics.

## Tests

```
python3 skills/paper-pipeline/tests/run_tests.py
PPL_FORCE_MINIYAML=1 python3 skills/paper-pipeline/tests/run_tests.py
```

The fixtures include two adversarial frames: one with blatant method-defending
phrasing the lexical pass must catch, and one that argues for the method with
no listed lexeme, which the lexical pass must miss so that the judgment stage
in `section-contracts` is shown to be necessary.

## Optional orchestrator integration

If an external multi-stage orchestrator hands work between agents, it should
carry only a pointer to the config (path, schema version, content digest) and
re-read the file at each gate rather than copying it. See the schema for the
pointer shape.
