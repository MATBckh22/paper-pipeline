#!/usr/bin/env python3
"""CLI: full mechanical validation of a paper-config.

Usage:
  validate_config.py CONFIG [--lexicon PATH] [--discipline NAME] [--frame PATH]

Runs structure checks, outline DAG checks, figure reconciliation, stance
clamping, and (with --frame) the frame linter's lexical pass. Prints
`severity CODE message` lines; exits 1 when any error is present. The LLM
judge stages defined in the skills run on top of this output - this tool is
the reproducible half.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ppl"))

import config as cfgmod  # noqa: E402
import dag  # noqa: E402
import framelint  # noqa: E402
import stance  # noqa: E402

DEFAULT_LEXICON = os.path.join(os.path.dirname(HERE), "data", "stance-lexicon.yaml")


def run(config_path, lexicon_path=DEFAULT_LEXICON, discipline=None, frame_path=None):
    lines, has_error = [], False

    def emit(severity, code, message):
        nonlocal has_error
        if severity == "error":
            has_error = True
        lines.append("%-7s %-22s %s" % (severity, code, message))

    cfg = cfgmod.load_config(config_path)
    for issue in cfgmod.validate_structure(cfg):
        emit(issue.severity, issue.code, issue.message)

    frame = cfg.get("frame") or {}
    outline = cfg.get("outline") or {}
    sections = outline.get("sections") or []
    frame_artifacts = {"gap_statement"} | {
        str(f.get("id")) for f in (frame.get("figures") or [])}

    report = dag.check(sections, frame_artifacts)
    for sid, inp in report.unknown_inputs:
        emit("error", "UNKNOWN_INPUT", "section %s inputs %r which is neither a "
             "frame artifact nor a section" % (sid, inp))
    for (sid, inp) in report.order_violations:
        affected = report.transitively_affected.get((sid, inp), [])
        emit("error", "ORDER_VIOLATION",
             "section %s depends on later section %s (forward reference); "
             "transitively affected: %s; remedies: reorder or restate"
             % (sid, inp, ", ".join(affected)))
    for cycle in report.cycles:
        emit("error", "CYCLE", "dependency cycle: %s" % " -> ".join(cycle))

    figrep = dag.figure_check(frame.get("figures") or [], sections)
    for fid in figrep.orphan_figures:
        emit("error", "FIG_ORPHAN", "figure %s supports no claim in any section "
             "(decoration)" % fid)
    for sid in figrep.prose_only_claims:
        emit("warning", "FIG_PROSE_ONLY", "section %s carries its claim on prose "
             "alone (legitimate, but confirm intentional)" % sid)

    lex = stance.load_lexicon(lexicon_path, discipline)
    default_stance = outline.get("default_stance")
    for s in sections:
        sid = str(s.get("id"))
        declared = s.get("stance") or default_stance
        ceiling, cue = stance.suggest_ceiling(s.get("evidence_note"), lex)
        if s.get("evidence_note") and ceiling is None:
            emit("notice", "CEILING_AMBIGUOUS",
                 "section %s: no ceiling cue matched evidence_note; "
                 "agent adjudication required" % sid)
        effective, clamped = stance.clamp(declared, ceiling)
        if clamped:
            emit("notice", "STANCE_CLAMPED",
                 "section %s: declared %s clamped to %s (evidence cue: %r)"
                 % (sid, declared, effective, cue))

    if frame_path:
        for hit in framelint.scan_file(frame_path):
            emit("notice", "FRAME_LINT_HIT",
                 "line %d: %r matched %s - judge stage must adjudicate"
                 % (hit.line, hit.excerpt, hit.pattern))

    return lines, has_error


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON)
    ap.add_argument("--discipline", default=None)
    ap.add_argument("--frame", default=None)
    args = ap.parse_args()
    lines, has_error = run(args.config, args.lexicon, args.discipline, args.frame)
    print("\n".join(lines) if lines else "clean")
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
