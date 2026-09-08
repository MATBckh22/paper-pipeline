#!/usr/bin/env python3
"""Test runner for the paper-pipeline validators. Stdlib only.

Run: python3 skills/paper-pipeline/tests/run_tests.py
Set PPL_FORCE_MINIYAML=1 to exercise the fallback parser even when PyYAML
is installed (CI should run both ways).
"""

import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "ppl"))

if os.environ.get("PPL_FORCE_MINIYAML"):
    sys.modules["yaml"] = None  # forces ImportError path in config.load_text

import miniyaml  # noqa: E402
import config  # noqa: E402

FAILURES = []


def check(name, fn):
    try:
        fn()
        print("PASS  %s" % name)
    except AssertionError as e:
        FAILURES.append(name)
        print("FAIL  %s: %s" % (name, e))
    except Exception:
        FAILURES.append(name)
        print("ERROR %s\n%s" % (name, traceback.format_exc()))


# ---------------------------------------------------------------- T1: config

def t1_miniyaml_parses_example():
    path = os.path.join(ROOT, "schemas", "paper-config.example.yaml")
    with open(path, encoding="utf-8") as fh:
        cfg = miniyaml.load(fh.read())
    # Scalars, nested maps, block sequences, flow lists, ints and booleans all
    # round-trip. Values are asserted structurally so the example config can be
    # rewritten without breaking the parser test.
    assert isinstance(cfg["paper"]["venue"], str) and cfg["paper"]["venue"], cfg["paper"]
    assert cfg["outline"]["default_stance"] == "L2"
    secs = cfg["outline"]["sections"]
    assert [s["id"] for s in secs] == ["1", "2", "3", "5"], [s["id"] for s in secs]
    assert secs[2]["figures"] == ["fig1"]
    assert secs[0]["inputs"] == ["gap_statement"]
    just = cfg["frame"]["delimitations"][0]["justification"]
    assert isinstance(just, str) and len(just) > 20, just
    assert cfg["review"]["max_rounds"] == 4
    assert cfg["drafting"]["one_section_at_a_time"] is True


def t1_miniyaml_rejects_out_of_subset():
    for bad, needle in [
        ("key: &anchor val", "anchors"),
        ("key: |\n  text", "multiline"),
        ("key: {a: 1}", "flow mappings"),
    ]:
        try:
            miniyaml.load(bad)
            raise AssertionError("accepted out-of-subset input: %r" % bad)
        except miniyaml.MiniYamlError as e:
            assert needle in str(e), (bad, str(e))


def t1_structural_validation():
    cfg = {
        "paper": {"title": "t", "type": "x", "venue": "v"},  # no length_limit
        "frame": {
            "gap_statement": "g",
            "delimitations": [{"claim": "only two materials"}],  # no justification
            "figures": [{"id": "f1", "supports_claim": "c", "status": "ready"}],
        },
        "outline": {
            "default_stance": "L2",
            "sections": [
                {"id": "1", "heading": "h", "inputs": [], "output": "reader believes x",
                 "stance": "L2", "evidence_note": "own data"},
                {"id": "1", "heading": "h2", "output": ""},  # dup id, empty output
                {"id": "2", "heading": "h3", "output": "y", "stance": "L9"},
            ],
        },
        "review": {"responses_allowed": ["accept", "defend"], "max_rounds": 0},
    }
    codes = [i.code for i in config.validate_structure(cfg)]
    for expected in ("PAPER_FIELD", "DELIM_NO_JUST", "SEC_DUP_ID", "SEC_NO_OUTPUT",
                     "SEC_BAD_STANCE", "RETREAT_REQUIRED", "BAD_MAX_ROUNDS"):
        assert expected in codes, (expected, codes)
    errors = [i for i in config.validate_structure(cfg) if i.severity == "error"]
    assert any(i.code == "DELIM_NO_JUST" for i in errors), "DELIM_NO_JUST must be an error"


def t1_example_config_is_clean():
    cfg = config.load_config(os.path.join(ROOT, "schemas", "paper-config.example.yaml"))
    errors = [i for i in config.validate_structure(cfg) if i.severity == "error"]
    assert errors == [], errors


check("T1 miniyaml parses example config", t1_miniyaml_parses_example)
check("T1 miniyaml rejects out-of-subset", t1_miniyaml_rejects_out_of_subset)
check("T1 structural validation codes", t1_structural_validation)
check("T1 example config validates clean", t1_example_config_is_clean)


# ---------------------------------------------------------------- T2: stance

import stance  # noqa: E402

LEXPATH = os.path.join(ROOT, "data", "stance-lexicon.yaml")


def t2_overlay_merge():
    base = stance.load_lexicon(LEXPATH)
    eng = stance.load_lexicon(LEXPATH, discipline="engineering")
    assert "validates" not in base["levels"]["L4"]["verbs"]
    assert "validates" in eng["levels"]["L4"]["verbs"]
    assert eng["levels"]["L2"]["verbs"] == base["levels"]["L2"]["verbs"]


def t2_ceiling_from_evidence():
    lex = stance.load_lexicon(LEXPATH)
    lvl, cue = stance.suggest_ceiling("single apparatus, no independent replication", lex)
    assert lvl == "L2", (lvl, cue)
    # negated strength cue must not fire as L4
    lvl2, cue2 = stance.suggest_ceiling("we had no ablation and no controls", lex)
    assert lvl2 != "L4", (lvl2, cue2)
    lvl3, _ = stance.suggest_ceiling("controlled comparison with alternatives excluded", lex)
    assert lvl3 == "L4", lvl3
    lvl4, cue4 = stance.suggest_ceiling("completely novel measurement context", lex)
    assert (lvl4, cue4) == (None, None), (lvl4, cue4)


def t2_clamp():
    assert stance.clamp("L4", "L2") == ("L2", True)
    assert stance.clamp("L2", "L4") == ("L2", False)
    assert stance.clamp("L3", None) == ("L3", False)
    assert stance.clamp(None, "L2") == ("L2", False)


def t2_scan_draft():
    lex = stance.load_lexicon(LEXPATH)
    text = "The results suggest a batch effect.\nWe show that the filter resolves it.\n"
    hits = stance.scan_draft(text, "L2", lex)
    assert len(hits) == 1 and hits[0].phrase == "we show" and hits[0].line == 2, hits
    assert stance.scan_draft(text, "L4", lex) == []


check("T2 discipline overlay merge", t2_overlay_merge)
check("T2 ceiling derivation from evidence_note", t2_ceiling_from_evidence)
check("T2 clamp direction", t2_clamp)
check("T2 draft hedging scan", t2_scan_draft)


# ------------------------------------------------------------ T3: phrase bank

def t3_phrase_bank():
    with open(os.path.join(ROOT, "data", "phrase-bank.yaml"), encoding="utf-8") as fh:
        bank = config.load_text(fh.read())
    moves = bank["moves"]
    required = {"signal_gap", "state_aim", "describe_method", "report_results",
                "compare_prior", "acknowledge_limitation", "draw_implication"}
    assert required <= set(moves), required - set(moves)
    for move, by_level in moves.items():
        assert by_level, "move %s has no levels" % move
        for level, phrasings in by_level.items():
            assert level in stance.LEVELS, (move, level)
            assert isinstance(phrasings, list) and phrasings, (move, level)


check("T3 phrase bank shape and level refs", t3_phrase_bank)


# ------------------------------------------------- T4: DAG + figures + linter

import dag  # noqa: E402
import framelint  # noqa: E402

FIX = os.path.join(HERE, "fixtures")


def _sections(path):
    cfg = config.load_config(path)
    return cfg["outline"]["sections"]


def t4_forward_reference_is_transitive():
    report = dag.check(_sections(os.path.join(FIX, "forwardref_config.yaml")),
                       frame_artifacts={"gap_statement"})
    assert report.order_violations == [("1", "5")], report.order_violations
    affected = report.transitively_affected[("1", "5")]
    assert "2" in affected, "pairwise-only check: section 2 not marked affected (%s)" % affected
    assert "1" in affected, affected
    assert report.cycles == [], report.cycles


def t4_full_cycle_reported():
    report = dag.check(_sections(os.path.join(FIX, "cycle_config.yaml")),
                       frame_artifacts={"gap_statement"})
    assert len(report.cycles) == 1, report.cycles
    cycle = report.cycles[0]
    assert cycle[0] == cycle[-1] and set(cycle) == {"3", "4", "5"}, cycle
    assert len(cycle) == 4, "full path expected, got %s" % (cycle,)


def t4_unknown_input():
    secs = [{"id": "1", "heading": "h", "inputs": ["ghost"], "output": "x"}]
    report = dag.check(secs, frame_artifacts={"gap_statement"})
    assert report.unknown_inputs == [("1", "ghost")], report.unknown_inputs


def t4_figure_reconciliation():
    figures = [
        {"id": "figA", "supports_claim": "c1", "status": "ready"},
        {"id": "figB", "supports_claim": None, "status": "ready"},   # degree 0
        {"id": "figC", "supports_claim": "c3", "status": "ready"},   # unreferenced
    ]
    sections = [
        {"id": "1", "heading": "h", "output": "x", "figures": ["figA"]},
        {"id": "2", "heading": "h", "output": "y"},                  # prose-only
    ]
    rep = dag.figure_check(figures, sections)
    assert set(rep.orphan_figures) == {"figB", "figC"}, rep.orphan_figures
    assert rep.prose_only_claims == ["2"], rep.prose_only_claims


def t4_frame_linter():
    blatant = framelint.scan_file(os.path.join(FIX, "blatant_frame.md"))
    assert len(blatant) >= 2, blatant
    lines = {h.line for h in blatant}
    assert any(l >= 11 for l in lines), "hits must carry real line offsets: %s" % lines
    evasive = framelint.scan_file(os.path.join(FIX, "evasive_frame.md"))
    assert evasive == [], ("lexical pass should MISS the evasive fixture "
                           "(that is why the judge stage exists): %s" % evasive)


def t4_cli_end_to_end():
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import validate_config
    lines, has_error = validate_config.run(os.path.join(FIX, "forwardref_config.yaml"))
    assert has_error
    joined = "\n".join(lines)
    assert "ORDER_VIOLATION" in joined and "transitively affected: 1, 2" in joined, joined
    lines2, err2 = validate_config.run(
        os.path.join(ROOT, "schemas", "paper-config.example.yaml"))
    assert not err2, "\n".join(lines2)
    assert any("STANCE_CLAMPED" not in l for l in lines2)


check("T4 forward reference reported transitively", t4_forward_reference_is_transitive)
check("T4 full cycle path reported", t4_full_cycle_reported)
check("T4 unknown input reported", t4_unknown_input)
check("T4 figure bipartite reconciliation", t4_figure_reconciliation)
check("T4 frame linter blatant/evasive split", t4_frame_linter)
check("T4 validate_config CLI end-to-end", t4_cli_end_to_end)


# ------------------------------------------------------------- T6: citecheck

import citecheck  # noqa: E402

BIBTEX = """
@inproceedings{doe2023alpha, title={Alpha}, year={2023}}
@article{roe2022beta, title={Beta}, year={2022}}
"""

MDBIB = """
5. Doe, C., Lee, C., Cai, J. (2023a). Alpha: Learning Continuous Part
   Sorting. Conf. A.
19. Doe, T. Z., Kumar, V. (2023b). Learning Fine-Grained Bimanual
   Manipulation. Conf. B.
46. Lee, C., Nazir, A. (2019). Dynamic Sorting Manipulation. Conf. C.
"""


def t6_latex_and_pandoc_keys():
    draft = ("Alpha \\cite{doe2023alpha} and tactile work "
             "[@roe2022beta] but also \\citep{ghost2020fake}.\n")
    res = citecheck.scan(draft, BIBTEX)
    assert res["resolved_count"] == 2, res
    assert len(res["unresolved"]) == 1, res["unresolved"]
    u = res["unresolved"][0]
    assert u.key == "ghost2020fake" and u.line == 1 and u.kind == "latex", u


def t6_author_year():
    draft = ("As shown by (Doe et al., 2023a) and (Lee, 2019).\n"
             "A fabricated one: (Nobody, 2020).\n"
             "Suffix drift: (Doe, 2023).\n")
    res = citecheck.scan(draft, MDBIB)
    assert res["resolved_count"] == 2, res
    kinds = {(u.kind, u.line) for u in res["unresolved"]}
    assert ("author-year", 2) in kinds, res["unresolved"]
    assert ("year-suffix-drift", 3) in kinds, res["unresolved"]


def t6_bibitem_bibliography():
    bib = "\\begin{thebibliography}{99}\n\\bibitem{doe2023alpha}\nC. Doe...\n\\end{thebibliography}"
    res = citecheck.scan("Alpha \\cite{doe2023alpha} and \\cite{ghost}.", bib)
    assert res["resolved_count"] == 1 and len(res["unresolved"]) == 1, res


check("T6 latex/pandoc key resolution", t6_latex_and_pandoc_keys)
check("T6 author-year resolution and drift", t6_author_year)
check("T6 thebibliography bibitem keys", t6_bibitem_bibliography)


# ------------------------------------------------------ T7: style-spec check

import stylespec_validate  # noqa: E402

LIBRARY = """
## [P1] Avigal et al., SpeedFolding, IROS 2022
> While prior work achieved 3-6 FPH, SpeedFolding achieves 30-40 FPH.
Move: makes throughput the headline on the axis the paper wins.
Would-not-copy: speed claims without CI.

## [P2] Gealy et al., Blue, ICRA 2019
Move: (author forgot to paste the quote here)
Would-not-copy: none identified.
"""

SPEC = """
## Traceable
- Lead results with the metric the paper wins on (source: P1)
- Number every functional requirement before the design (source: P2)
- Concede the rival metric before shifting axes (source: P9)
- State the cost target as a design requirement

## Asserted
- Never open a paragraph with However.
"""


def t7_stylespec_validation():
    v = stylespec_validate.check(SPEC, LIBRARY)
    problems = {(x.problem.split()[1] if x.problem.startswith("cites") else "nosrc")
                for x in v}
    assert len(v) == 3, v
    assert any("P9" in x.problem and "not in the library" in x.problem for x in v), v
    assert any("P2" in x.problem and "no quoted passage" in x.problem for x in v), v
    assert any("no (source:" in x.problem for x in v), v
    # asserted rules pass without source
    assert not any("However" in x.rule for x in v), v


def t7_wrapped_rules_join():
    spec = ("## Traceable\n"
            "- Lead results with the metric the paper wins on,\n"
            "  compared directly against prior art (source: P1)\n"
            "- A wrapped rule whose citation line\n"
            "  is missing entirely\n")
    v = stylespec_validate.check(spec, LIBRARY)
    assert len(v) == 1, v
    assert "no (source:" in v[0].problem and v[0].line == 4, v


def t7_real_spec_validates():
    with open(os.path.join(ROOT, "data", "style-spec.md"), encoding="utf-8") as fh:
        spec = fh.read()
    with open(os.path.join(ROOT, "data", "exemplar-library.md"), encoding="utf-8") as fh:
        lib = fh.read()
    v = stylespec_validate.check(spec, lib)
    assert v == [], v


check("T7 style-spec traceable partition validation", t7_stylespec_validation)
check("T7 wrapped rules joined before source check", t7_wrapped_rules_join)
check("T7 real style-spec validates clean", t7_real_spec_validates)


if __name__ == "__main__":
    print("\n%d failure(s)" % len(FAILURES))
    sys.exit(1 if FAILURES else 0)
