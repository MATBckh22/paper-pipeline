"""Stance lexicon: ceiling derivation, clamping, and draft scanning.

The clamp direction is fixed by the brief (3.3): the author declares intent,
the evidence sets the maximum, and disagreement clamps DOWN with a report.
Ceiling derivation here is the mechanical stage; an ambiguous evidence_note
(no cue matched) is returned as (None, None) for the agent to adjudicate.
"""

import os
import re
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config as _config

LEVELS = ("L1", "L2", "L3", "L4")

Hit = collections.namedtuple("Hit", "line phrase phrase_level")


def load_lexicon(path, discipline=None):
    with open(path, "r", encoding="utf-8") as fh:
        lex = _config.load_text(fh.read())
    if discipline:
        overlay = (lex.get("disciplines") or {}).get(discipline) or {}
        for level, block in (overlay.get("levels") or {}).items():
            base = lex["levels"].setdefault(level, {})
            for key, val in block.items():
                base[key] = val
        for level, cues in (overlay.get("ceiling_cues") or {}).items():
            lex["ceiling_cues"][level] = list(lex["ceiling_cues"].get(level, [])) + list(cues)
    return lex


def _rank(level):
    return LEVELS.index(level)


def _negated(note_lc, pos, markers):
    window = note_lc[max(0, pos - 24):pos]
    return any(re.search(r"\b%s\s*$" % re.escape(m.rstrip("-")), window) or
               ("%s " % m) in window for m in markers)


def suggest_ceiling(evidence_note, lexicon):
    """Return (level, cue) or (None, None) when no cue matches.

    Weakness cues (L1/L2) dominate: the lowest matched weakness wins.
    Otherwise the highest non-negated strength cue (L4 then L3) wins.
    """
    if not evidence_note:
        return None, None
    note = evidence_note.lower()
    cues = lexicon.get("ceiling_cues") or {}
    markers = lexicon.get("negation_markers") or []
    for level in ("L1", "L2"):
        for cue in cues.get(level, []):
            if cue.lower() in note:
                return level, cue
    for level in ("L4", "L3"):
        for cue in cues.get(level, []):
            pos = note.find(cue.lower())
            if pos >= 0 and not _negated(note, pos, markers):
                return level, cue
    return None, None


def clamp(declared, ceiling):
    """Return (effective_level, clamped?). Ceiling None -> declared stands."""
    if declared is None:
        return ceiling, False
    if ceiling is None or _rank(declared) <= _rank(ceiling):
        return declared, False
    return ceiling, True


def scan_draft(text, declared_level, lexicon):
    """Flag realized stance phrases ABOVE the section's declared level."""
    if declared_level not in LEVELS:
        raise ValueError("declared_level must be one of %s" % (LEVELS,))
    limit = _rank(declared_level)
    patterns = []
    for level in LEVELS[limit + 1:]:
        block = (lexicon.get("levels") or {}).get(level) or {}
        for phrase in list(block.get("verbs") or []) + list(block.get("modals") or []):
            patterns.append((re.compile(r"\b%s\b" % re.escape(phrase), re.IGNORECASE),
                             phrase, level))
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx, phrase, level in patterns:
            if rx.search(line):
                hits.append(Hit(lineno, phrase, level))
    return hits
