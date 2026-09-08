"""Mechanical citation resolution.

Every in-text citation must resolve to a real bibliography entry. Runs every
draft round (brief 3.6): fabricated and drifted references are the
highest-frequency, highest-cost failure in LLM-assisted academic writing.

Supported in-text forms: LaTeX \\cite/\\citep/\\citet{key,...}, pandoc
[@key], and author-year "(Surname, 2023)" / "(Surname et al., 2023a)".
Supported bibliographies: BibTeX (@type{key,...) and markdown reference
lists ("Surname, X., ... (2023a).").
"""

import re
import collections

Unresolved = collections.namedtuple("Unresolved", "line kind key")

_LATEX_CITE = re.compile(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]+)\}")
_PANDOC_CITE = re.compile(r"\[@([A-Za-z0-9_:.\-]+)(?:[;,\s]+@([A-Za-z0-9_:.\-]+))*\]")
_PANDOC_KEY = re.compile(r"@([A-Za-z0-9_:.\-]+)")
_AUTHOR_YEAR = re.compile(
    r"\(\s*([A-Z][A-Za-z'\u2019\-]+)"          # lead surname
    r"(?:\s+(?:et al\.?|and\s+[A-Z][A-Za-z'\u2019\-]+|&\s*[A-Z][A-Za-z'\u2019\-]+))?"
    r"\s*,\s*(\d{4}[a-z]?)\s*\)")
_BIBTEX_KEY = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,")
_BIBITEM_KEY = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}")
_MD_ENTRY = re.compile(
    r"^\s*(?:\d+\.\s*)?([A-Z][A-Za-z'\u2019\-]+),\s+[A-Z].*?\((\d{4}[a-z]?)\)",
    re.MULTILINE)


def parse_bibliography(bib_text):
    keys = set(_BIBTEX_KEY.findall(bib_text)) | set(_BIBITEM_KEY.findall(bib_text))
    pairs = {(m.group(1).lower(), m.group(2)) for m in _MD_ENTRY.finditer(bib_text)}
    return keys, pairs


def scan(draft_text, bib_text):
    keys, pairs = parse_bibliography(bib_text)
    unresolved, resolved = [], 0
    for lineno, line in enumerate(draft_text.splitlines(), 1):
        for m in _LATEX_CITE.finditer(line):
            for key in (k.strip() for k in m.group(1).split(",")):
                if key in keys:
                    resolved += 1
                else:
                    unresolved.append(Unresolved(lineno, "latex", key))
        for m in _PANDOC_CITE.finditer(line):
            for key in _PANDOC_KEY.findall(m.group(0)):
                if key in keys:
                    resolved += 1
                else:
                    unresolved.append(Unresolved(lineno, "pandoc", key))
        for m in _AUTHOR_YEAR.finditer(line):
            surname, year = m.group(1).lower(), m.group(2)
            if (surname, year) in pairs:
                resolved += 1
            elif year[-1].isalpha() and (surname, year[:-1]) in pairs or \
                    (surname, year + "a") in pairs:
                # year-letter drift: cited 2023 vs listed 2023a (or reverse) -
                # resolvable but flagged, the a/b suffix must be consistent
                unresolved.append(Unresolved(lineno, "year-suffix-drift",
                                             "%s %s" % (m.group(1), year)))
            else:
                unresolved.append(Unresolved(lineno, "author-year",
                                             "%s %s" % (m.group(1), year)))
    return {"unresolved": unresolved, "resolved_count": resolved}
