# paper-config schema (v1.0)

One YAML file per paper. Every pipeline skill reads it; `section-contracts`
writes `frame` and `outline`; `exemplar-spec` writes `inputs.style_spec`.
Structural validation: `scripts/validate_config.py <config>` (exit 1 on errors).

## Optional orchestrator integration

The config is a user-project artifact that lives beside the manuscript. If an
external multi-stage orchestrator hands work between agents, it should carry
only a pointer to the config and re-read the file at each gate rather than
copying it:

```
paper_config_ref:
  config_path: <workspace-relative path>
  config_version: "paper-config/1.0"
  content_sha256: <hex digest over the exact config bytes>
```

Consumers verify the digest before trusting the pointer; a mismatch means the
binding is broken and the config path must be re-established.

## YAML subset (enforced by the fallback parser)

Block mappings, block sequences, flow lists of scalars, quoted/plain scalars,
`#` comments. **No** anchors/aliases, multiline (`|`/`>`) scalars, flow
mappings, or tabs. PyYAML parses a superset; keep configs inside the subset so
they load identically everywhere.

## Fields

### `paper` (required)
| field | req | meaning |
|---|---|---|
| `title` | yes | working title |
| `type` | yes | e.g. `conference-systems`, `journal`, `thesis-chapter` |
| `venue` | yes | target venue + year |
| `venue_style_guide` | no | one line: template, page limit, anonymity |
| `length_limit` | yes | hard limit as the venue states it |

### `inputs`
Paths, workspace-relative: `bibliography`, `style_spec`, `phrase_bank`,
`figure_source`.

### `frame` (written by section-contracts)
- `gap_statement` — three-move form: established (cited) → not established
  (cited) → why it matters. Prose, but all three moves must be present.
- `delimitations[]` — `{claim, justification}`. **A delimitation without a
  justification is a validation error, not a warning.**
- `figures[]` — `{id, supports_claim, status}`. `supports_claim` names the
  claim the figure carries; `status` ∈ `planned|ready|blocked`.

### `outline` (written by section-contracts)
- `default_stance` — L1–L4, applied when a section omits `stance`.
- `sections[]`:

| field | req | meaning |
|---|---|---|
| `id` | yes | string, unique; document order = list order |
| `heading` | yes | working heading |
| `inputs` | no | list of section ids and/or frame artifact names this section assumes |
| `output` | yes | what the reader believes after the section — one sentence |
| `stance` | no | declared rhetorical level L1–L4 (see `data/stance-lexicon.yaml`) |
| `evidence_note` | with stance | free text describing the evidence; source of the stance **ceiling** |
| `figures` | no | figure ids referenced by this section |

### `drafting`
- `precedence` — ordered tier names, highest first. Default:
  `[venue_guide, style_spec_traceable, phrase_bank, anti_ai_heuristics]`.
- `one_section_at_a_time` — boolean; draft-guard refuses multi-section drafts
  when true.

### `review`
- `fresh_context` — boolean; review-response enforces structurally when true.
- `rank_by` — `severity_x_likelihood` (only defined value in v1.0).
- `responses_allowed` — subset of `accept|defend|retreat`; **must include
  `retreat`** (validation error otherwise).
- `stop_when` — prose statement of the termination predicate (documentation;
  the predicate itself is fixed in review-response).
- `max_rounds` — integer ≥ 1 hard backstop.

## Validation codes

`validate_config.py` emits `severity CODE message` lines. Errors:
`PAPER_MISSING PAPER_FIELD DELIM_NO_CLAIM DELIM_NO_JUST FIG_NO_ID FIG_FIELD
SEC_NOT_MAP SEC_NO_ID SEC_DUP_ID SEC_NO_HEADING SEC_NO_OUTPUT SEC_INPUTS_TYPE
SEC_BAD_STANCE BAD_DEFAULT_STANCE BAD_RESPONSE_TYPE RETREAT_REQUIRED
BAD_MAX_ROUNDS` plus DAG codes `ORDER_VIOLATION CYCLE UNKNOWN_INPUT
FIG_ORPHAN` and stance code `STANCE_CLAMPED` (reported as a notice with the
clamp reason). Warnings: `GAP_MISSING EVIDENCE_NOTE_MISSING FIG_PROSE_ONLY`.
