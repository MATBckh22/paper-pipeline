"""paper-config loader and structural validator.

Loads with PyYAML when available, otherwise with the bundled miniyaml
subset parser. Structural validation covers what a schema checker can decide
without judgment; semantic checks (DAG, stance, figures) live in dag.py and
stance.py.
"""

import os
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

Issue = collections.namedtuple("Issue", "severity code message")

STANCE_LEVELS = ("L1", "L2", "L3", "L4")
RESPONSE_TYPES = {"accept", "defend", "retreat"}


def load_text(text):
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except ImportError:
        import miniyaml
        return miniyaml.load(text)


def load_config(path):
    with open(path, "r", encoding="utf-8") as fh:
        return load_text(fh.read())


def _err(code, msg):
    return Issue("error", code, msg)


def _warn(code, msg):
    return Issue("warning", code, msg)


def validate_structure(cfg):
    issues = []
    if not isinstance(cfg, dict):
        return [_err("NOT_A_MAP", "config root must be a mapping")]

    paper = cfg.get("paper")
    if not isinstance(paper, dict):
        issues.append(_err("PAPER_MISSING", "top-level 'paper' block is required"))
    else:
        for field in ("title", "type", "venue", "length_limit"):
            if not paper.get(field):
                issues.append(_err("PAPER_FIELD", "paper.%s is required" % field))

    frame = cfg.get("frame") or {}
    if frame:
        if not frame.get("gap_statement"):
            issues.append(_warn("GAP_MISSING", "frame.gap_statement not yet set"))
        for i, d in enumerate(frame.get("delimitations") or []):
            if not isinstance(d, dict) or not d.get("claim"):
                issues.append(_err("DELIM_NO_CLAIM", "delimitations[%d] has no claim" % i))
            elif not d.get("justification"):
                # brief 3.3: rejected, not warned
                issues.append(_err(
                    "DELIM_NO_JUST",
                    "delimitations[%d] (%r) has no justification" % (i, d.get("claim")),
                ))
        for i, f in enumerate(frame.get("figures") or []):
            if not isinstance(f, dict) or not f.get("id"):
                issues.append(_err("FIG_NO_ID", "figures[%d] has no id" % i))
            else:
                for field in ("supports_claim", "status"):
                    if field not in f or f.get(field) in (None, ""):
                        issues.append(_err(
                            "FIG_FIELD", "figure %r missing %s" % (f.get("id"), field)))

    outline = cfg.get("outline") or {}
    sections = outline.get("sections") or []
    seen = set()
    for i, s in enumerate(sections):
        if not isinstance(s, dict):
            issues.append(_err("SEC_NOT_MAP", "sections[%d] is not a mapping" % i))
            continue
        sid = s.get("id")
        if not sid:
            issues.append(_err("SEC_NO_ID", "sections[%d] has no id" % i))
            continue
        sid = str(sid)
        if sid in seen:
            issues.append(_err("SEC_DUP_ID", "duplicate section id %r" % sid))
        seen.add(sid)
        if not s.get("heading"):
            issues.append(_err("SEC_NO_HEADING", "section %r has no heading" % sid))
        if not s.get("output"):
            issues.append(_err(
                "SEC_NO_OUTPUT",
                "section %r declares no output (what the reader believes after it)" % sid))
        inputs = s.get("inputs")
        if inputs is not None and not isinstance(inputs, list):
            issues.append(_err("SEC_INPUTS_TYPE", "section %r inputs must be a list" % sid))
        stance = s.get("stance")
        if stance is not None and stance not in STANCE_LEVELS:
            issues.append(_err(
                "SEC_BAD_STANCE",
                "section %r stance %r not in %s" % (sid, stance, "/".join(STANCE_LEVELS))))
        if stance is not None and not s.get("evidence_note"):
            issues.append(_warn(
                "EVIDENCE_NOTE_MISSING",
                "section %r declares stance %s with no evidence_note; "
                "the ceiling cannot be derived" % (sid, stance)))
    default_stance = outline.get("default_stance")
    if default_stance is not None and default_stance not in STANCE_LEVELS:
        issues.append(_err("BAD_DEFAULT_STANCE", "outline.default_stance %r invalid" % default_stance))

    review = cfg.get("review") or {}
    if review:
        allowed = review.get("responses_allowed")
        if allowed is not None:
            extra = set(map(str, allowed)) - RESPONSE_TYPES
            if extra:
                issues.append(_err("BAD_RESPONSE_TYPE", "unknown response types: %s" % sorted(extra)))
            if "retreat" not in set(map(str, allowed)):
                # brief 3.7: retreat must be first-class
                issues.append(_err("RETREAT_REQUIRED", "responses_allowed must include 'retreat'"))
        mr = review.get("max_rounds")
        if mr is not None and (not isinstance(mr, int) or mr < 1):
            issues.append(_err("BAD_MAX_ROUNDS", "review.max_rounds must be an integer >= 1"))

    return issues
