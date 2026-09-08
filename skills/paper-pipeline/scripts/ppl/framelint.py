"""Frame linter, mechanical stage.

Scans frame.md for method-defending language (the forward-reference gate,
brief 3.3). This is stage one of two: a cheap lexical pass over a maintained
pattern list localizes candidates with line offsets; the LLM judge stage
(section-contracts SKILL.md) suppresses false positives among the hits AND
reads the whole frame once for evasive phrasings the list cannot catch.
Lexical-only is noisy; judge-only is not reproducible - both stages run.
"""

import os
import re
import collections

Hit = collections.namedtuple("Hit", "line pattern excerpt")

DEFAULT_PATTERNS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "rules", "method-defense-patterns.txt")


def load_patterns(path=DEFAULT_PATTERNS):
    patterns = []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(re.compile(line, re.IGNORECASE))
    return patterns


def scan(text, patterns=None):
    if patterns is None:
        patterns = load_patterns()
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rx in patterns:
            m = rx.search(line)
            if m:
                start = max(0, m.start() - 30)
                hits.append(Hit(lineno, rx.pattern, line[start:m.end() + 30].strip()))
    return hits


def scan_file(path, patterns=None):
    with open(path, "r", encoding="utf-8") as fh:
        return scan(fh.read(), patterns)
