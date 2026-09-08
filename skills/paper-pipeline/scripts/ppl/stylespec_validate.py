"""style-spec validator.

Enforces the traceable/asserted partition contract (brief 3.2): every rule in
the `Traceable` section must cite `(source: P<n>)` where P<n> is a passage in
the exemplar library that actually contains a quoted passage. Asserted rules
need no source - the partition exists so downstream consumers can weight
them differently and the author can see which rules are invented.

Library block format:
    ## [P3] Zhao et al., ICRA 2023
    > quoted passage text...
    Move: pre-empting the protocol-mismatch objection before the comparison table
    Would-not-copy: ...
Spec rule format (Traceable section):
    - Rule text ... (source: P3)
"""

import re
import collections

Violation = collections.namedtuple("Violation", "line rule problem")

_LIB_HEADER = re.compile(r"^##\s*\[(P\d+)\]\s*(.+)$")
_QUOTE = re.compile(r"^\s*>\s*\S")
_SOURCE_REF = re.compile(r"\(source:\s*((?:P\d+)(?:\s*,\s*P\d+)*)\)")
_P_ID = re.compile(r"P\d+")
_RULE = re.compile(r"^\s*[-*]\s+(.*)$")


def parse_library(library_text):
    """Return {passage_id: has_quote} for every library block."""
    passages = {}
    current = None
    for line in library_text.splitlines():
        m = _LIB_HEADER.match(line)
        if m:
            current = m.group(1)
            passages[current] = False
        elif current and _QUOTE.match(line):
            passages[current] = True
    return passages


def _rules(spec_text):
    """Yield (start_line, rule_text, section) with continuation lines joined.

    A rule starts at a '- '/'* ' bullet and extends over following indented,
    non-bullet, non-heading, non-blank lines (markdown soft wrap).
    """
    section = None
    current = None  # (start_line, [parts])
    for lineno, line in enumerate(spec_text.splitlines() + [""], 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            if current:
                yield current[0], " ".join(current[1]), section
                current = None
            heading = stripped.lower().lstrip("# ").strip()
            if "traceable" in heading:
                section = "traceable"
            elif "asserted" in heading:
                section = "asserted"
            elif stripped.startswith("##"):
                section = None
            continue
        m = _RULE.match(line)
        if m:
            if current:
                yield current[0], " ".join(current[1]), section
            current = (lineno, [m.group(1).strip()])
        elif current and stripped:
            current[1].append(stripped)
        else:
            if current:
                yield current[0], " ".join(current[1]), section
                current = None


def check(spec_text, library_text):
    passages = parse_library(library_text)
    violations = []
    for lineno, rule, section in _rules(spec_text):
        if section != "traceable":
            continue
        ref = _SOURCE_REF.search(rule)
        if not ref:
            violations.append(Violation(
                lineno, rule, "traceable rule has no (source: P<n>) citation"))
            continue
        for pid in _P_ID.findall(ref.group(1)):
            if pid not in passages:
                violations.append(Violation(
                    lineno, rule, "cites %s which is not in the library" % pid))
            elif not passages[pid]:
                violations.append(Violation(
                    lineno, rule,
                    "cites %s but that block holds no quoted passage" % pid))
    return violations
