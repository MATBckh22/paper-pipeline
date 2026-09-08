# paper-pipeline

A small, reproducible toolchain for writing and gating a systems paper: read
the genre, plan the argument, draft one section at a time, and run mechanical
checks after every edit.

Two halves:

- **`skills/`** — six [Claude Code](https://claude.com/claude-code) skills that
  make an AI assistant plan, draft, and review under explicit rules, plus the
  `paper-pipeline` skill that holds the shared data (stance lexicon, phrase
  bank, anti-AI rules) and the validators they call.
- **`tools/`** — standalone Python scripts that run without any assistant:
  fetch a writing guide, digest a stack of award papers, lint prose, and check
  a LaTeX manuscript's citations, references, figures, and numbers.

## Layout

```
skills/
  academic-writing/      story-first structure rules and a revision checklist
  section-contracts/     frame (gap, delimitations, figures) + per-section I/O outline
  exemplar-spec/         build a personal style spec from papers you admire
  draft-guard/           draft one section under guidance precedence, then gate it
  review-response/       adversarial review rounds with accept / defend / retreat
  mock-review/           a single reviewer-style critique
  paper-pipeline/        shared data, rules, schema, validators, tests
tools/
  fetch_text.py          URL -> readable plain text (for reading a guide in full)
  paper_digest.py        PDFs -> structural digests + phrasing statistics
  lint_prose.py          anti-AI and style lint for .tex
  tex_integrity.py       refs, figures, braces, bibliography order, numeric diff
  run_gate.sh            the three checks in one command
examples/
  sample.tex             synthetic manuscript that passes the gate
  sample_bad.tex         synthetic manuscript that fails every check on purpose
docs/
  workflow.md            the pipeline, stage by stage
  writing-checklist.md   the writing rules applied, with sources
  award-paper-patterns.md what award-winning robotics papers share
```

## Install

Python 3.9 or newer. The validators use only the standard library; PyYAML is
used when present and a bundled subset parser otherwise. `paper_digest.py`
needs `pypdf`.

```bash
pip install -r requirements.txt          # pypdf, PyYAML (both optional)
cp -R skills/* /path/to/your/project/.claude/skills/   # for the assistant skills
```

The skill files refer to each other by the installed path
`.claude/skills/paper-pipeline/...`, so keep that layout inside a project.

## Quick start

Gate the synthetic example that should pass:

```bash
tools/run_gate.sh examples/sample.tex L3       # GATE: pass
```

And the one written to fail, which shows what each check catches:

```bash
tools/run_gate.sh examples/sample_bad.tex L1   # GATE: fail
```

Gate your own draft, declared at rhetorical level L3, with an inline
`thebibliography`:

```bash
tools/run_gate.sh paper/main.tex L3
```

Run the validator test suite (both YAML code paths):

```bash
python3 skills/paper-pipeline/tests/run_tests.py
PPL_FORCE_MINIYAML=1 python3 skills/paper-pipeline/tests/run_tests.py
```

## Tools

**`fetch_text.py URL -o guide.txt`** downloads a page with a browser-like
user agent and strips it to text so a guide can be read whole. Hosts that
serve a bot challenge are reported instead of silently returning a stub.

**`paper_digest.py --arxiv 2208.10552 --arxiv 2309.06440 -o digests/`**
downloads the PDFs, extracts text with pypdf, and writes one digest per paper:
title and abstract, section headings, every figure and table caption, and the
sentences around contributions, limitations, and conclusion.
`paper_digest.py --phrasing digests/*.txt` then tallies how the set refers to
figures and which verbs and hedges it uses.

**`lint_prose.py draft.tex --strict`** applies the mechanical rules in
`skills/paper-pipeline/rules/anti-ai-rules.md` and a few of Michael Black's:
em-dash and semicolon limits, exclamation marks, contractions, sentences that
open with a citation, the "not X, Y" contrast tic, flagged vocabulary,
throat-clearing phrases, "we" density, and past-tense narration verbs.

**`tex_integrity.py draft.tex`** resolves every `\ref` and `\cite`, checks
figure files exist, balances braces and environments, and compares bibliography
order with first-citation order. `--sort-cites` rewrites multi-key citations
in numeric order, `--reorder-bib` puts `\bibitem` entries in citation order,
`--diff-numbers old.tex` lists every number that changed between two drafts,
and `--contributions` prints the numbered contributions list.

**`skills/paper-pipeline/scripts/check_draft.py draft.tex --bib draft.tex --stance L3`**
is the citation-resolution and stance gate: every in-text citation must have a
bibliography entry, and no phrase may claim more than the section's declared
level (L1 report, L2 suggest, L3 argue, L4 assert).

**`skills/paper-pipeline/scripts/validate_config.py paper-config.yaml --frame frame.md`**
validates the planning file: outline dependency graph, figure-to-claim
mapping, stance ceilings, and a lexical pass for method-defending language in
the frame.

## Workflow

Read [docs/workflow.md](docs/workflow.md) for the full sequence. In short:

1. Read the genre: fetch the writing guide you follow in full, digest ten to
   twenty award papers from the target venue, and note their patterns.
2. Plan: build the frame and the per-section contracts with
   `section-contracts`; validate the config.
3. Draft one section at a time with `draft-guard`; apply every change as an
   exact, replayable edit.
4. Gate after every edit with `run_gate.sh`; keep a dated log of each pass.
5. Review adversarially with `review-response`, in fresh context, and route
   fixes back through the draft step.
6. Before submission: numeric diff against the last verified draft, anonymity
   sweep, page count on a real compile.

## Provenance

- The stance lexicon and the phrase bank are original; phrase-bank entries
  are written in the register of the Manchester Academic Phrasebank, not
  copied from it.
- `rules/anti-ai-rules.md` merges two public heuristic sets, credited inside
  the file; standard field terminology is exempt by design.
- The writing rules in `docs/writing-checklist.md` are a paraphrase of
  Michael J. Black, "Writing a good scientific paper" (2024), with a link; the
  post itself is not reproduced.
- `docs/award-paper-patterns.md` lists public papers by title and arXiv id
  and summarises structure only.

## License

MIT. See [LICENSE](LICENSE).
