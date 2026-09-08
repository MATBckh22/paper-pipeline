#!/usr/bin/env python3
"""Prose lint for a LaTeX (or plain-text) manuscript.

Mechanical checks drawn from two sources: the anti-AI heuristics in
skills/paper-pipeline/rules/anti-ai-rules.md and Michael Black's
"Writing a good scientific paper". Every hit is a candidate for judgment,
not a verdict; the hard limits are the ones the rules file calls mechanical.

Hard limits (fail under --strict):
  em-dashes            <= 3            (rules file; aim for 0-1)
  semicolons           <= 2 / 1000 words (never fewer than 2 allowed)
  exclamation marks    == 0
  contractions         == 0
  sentence opens with \\cite  == 0     (Black: never cite as a noun)
  binary-contrast tic  <= 2            ("not X, Y" / "not X but Y")

Reported only: flagged vocabulary, throat-clearing phrases, "we" density,
allows/enables/provides, past-tense narration verbs, "In Fig. N we" openers,
"novel", "note that", "in order to", intensifier padding.

Usage:
  lint_prose.py DRAFT.tex [--strict] [--json]
"""

import argparse
import json
import re
import sys

FLAGGED_VOCAB = [
    "delve", "tapestry", "landscape", "pivotal", "crucial", "foster", "showcase",
    "testament", "navigate", "leverage", "realm", "embark", "underscore",
    "multifaceted", "nuanced", "comprehensive", "robust", "intricate",
    "cornerstone", "paradigm", "synergy", "holistic", "streamline", "cutting-edge",
    "groundbreaking", "seamless", "transformative",
]
THROAT_CLEARING = [
    "it's important to note", "it is important to note", "it is worth mentioning",
    "it is worth noting", "in the realm of", "in today's rapidly evolving",
    "it goes without saying", "in order to", "when it comes to",
    "as a matter of fact", "with that being said", "it is essential to",
    "plays a vital role", "note that",
]
INTENSIFIERS = [r"\bvery\b", r"\btruly\b", r"\breally\b", r"\bextremely\b",
                r"\bhighly\b", r"\bsignificantly\b"]
PAST_NARRATION = r"\b(presented|proposed|demonstrated|showed|introduced)\b"
CONTRAST_PATTERNS = [
    r"\bnot\s+(?:a|an|the)?\s*[^,.;:()]{2,40},\s*(?:but|rather)\b",
    r",\s*not\s+(?:a|an|the)?\s*[^,.;:()]{2,40}[.;]",
    r"\bnot\s+[^,.;:()]{2,40}\s+but\s+(?:rather\s+)?",
    r"\b(?:is|are|was|were)\s+not\s+[^,.;:()]{2,40}[,;]\s*(?:it|they|this|that)\s+(?:is|are)\b",
]
CONTRACTION = re.compile(
    r"\b\w+n't\b|\b(?:I|you|we|they|it|he|she|that|there|what|who|let)'"
    r"(?:re|ve|ll|d|m|s)\b", re.I)


def preprocess(src):
    """Strip LaTeX scaffolding so counts reflect prose the reader sees."""
    text = re.sub(r"(?<!\\)%[^\n]*", "", src)
    text = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", "", text, flags=re.S)
    text = re.sub(r"\\begin\{(tabular\*?|tabularx|algorithmic|verbatim|lstlisting|equation\*?|align\*?)\}.*?\\end\{\1\}",
                  " ", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]", " MATH ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " MATH ", text)
    text = re.sub(r"\\(?:includegraphics|label|ref|eqref|pageref|url|graphicspath|input|include)\*?(?:\[[^\]]*\])?\{[^}]*\}", " ", text)
    text = re.sub(r"\\(?:emph|textbf|textit|texttt|underline|caption|captionof\{[a-z]+\}|section\*?|subsection\*?|subsubsection\*?|title|footnote|thanks)\*?\{", "{", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]*\}(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)  # remaining commands
    text = text.replace("~", " ").replace("\\,", " ").replace("\\ ", " ")
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text


def find_all(pattern, text, flags=re.I):
    hits = []
    for m in re.finditer(pattern, text, flags):
        line = text.count("\n", 0, m.start()) + 1
        hits.append((line, m.group(0).strip()[:70]))
    return hits


def lint(src):
    raw_nocomment = re.sub(r"(?<!\\)%[^\n]*", "", src)
    body = raw_nocomment.split(r"\begin{thebibliography}")[0]
    text = preprocess(body)
    words = len(re.findall(r"[A-Za-z]+", text))
    per_k = 1000.0 / max(words, 1)
    report = {"words": words}

    report["em_dashes"] = text.count("---") + text.count("\u2014")
    report["semicolons"] = text.count(";")
    report["semicolons_per_1000"] = round(report["semicolons"] * per_k, 2)
    report["exclamations"] = text.count("!")
    report["contractions"] = [(text.count("\n", 0, m.start()) + 1, m.group(0))
                              for m in CONTRACTION.finditer(text)]
    report["cite_opens_sentence"] = [
        (body.count("\n", 0, m.start()) + 1, m.group(0).strip()[:40])
        for m in re.finditer(r"(?:\A\s*|[.!?]\s+)\\cite", body)]
    contrast = []
    for pat in CONTRAST_PATTERNS:
        contrast.extend(find_all(pat, text))
    report["contrast_tic"] = sorted(set(contrast))

    low = text.lower()
    report["flagged_vocab"] = {w: low.count(w) for w in FLAGGED_VOCAB if low.count(w)}
    report["throat_clearing"] = {p: low.count(p) for p in THROAT_CLEARING if low.count(p)}
    report["intensifiers"] = sum(len(re.findall(p, low)) for p in INTENSIFIERS)
    report["we_per_1000"] = round(len(re.findall(r"\bwe\b", low)) * per_k, 1)
    report["allows_enables_provides"] = len(re.findall(r"\b(?:allows?|enables?|provides?)\b", low))
    report["past_narration"] = find_all(PAST_NARRATION, text)
    report["in_fig_we_openers"] = find_all(r"In Fig(?:ure|\.)?~?\\?ref?\{?[^}]*\}?\s+we\b", body)
    report["novel"] = low.count("novel")
    return report


def render(rep):
    lines = ["words: %d" % rep["words"],
             "em-dashes: %d (limit 3, aim 0-1)" % rep["em_dashes"],
             "semicolons: %d = %.2f per 1000 words (limit 2 per 1000, min 2)"
             % (rep["semicolons"], rep["semicolons_per_1000"]),
             "exclamation marks: %d" % rep["exclamations"],
             "contractions: %d %s" % (len(rep["contractions"]), rep["contractions"][:5]),
             "sentences opening with \\cite: %d %s"
             % (len(rep["cite_opens_sentence"]), rep["cite_opens_sentence"][:3]),
             "binary-contrast constructions: %d (limit 2)" % len(rep["contrast_tic"])]
    for line, snippet in rep["contrast_tic"][:8]:
        lines.append("    line %d: %s" % (line, snippet))
    lines.append("flagged vocabulary: %s" % (rep["flagged_vocab"] or "none"))
    lines.append("throat-clearing phrases: %s" % (rep["throat_clearing"] or "none"))
    lines.append("intensifier padding: %d   'novel': %d" % (rep["intensifiers"], rep["novel"]))
    lines.append("'we' per 1000 words: %.1f   allows/enables/provides: %d"
                 % (rep["we_per_1000"], rep["allows_enables_provides"]))
    lines.append("past-tense narration verbs: %d %s"
                 % (len(rep["past_narration"]), rep["past_narration"][:4]))
    lines.append("'In Fig. N we ...' openers: %d" % len(rep["in_fig_we_openers"]))
    return "\n".join(lines)


def failures(rep):
    f = []
    if rep["em_dashes"] > 3:
        f.append("em-dashes > 3")
    if rep["semicolons"] > max(2, 0.002 * rep["words"]):
        f.append("semicolons > 2 per 1000 words (floor of 2 for short texts)")
    if rep["exclamations"]:
        f.append("exclamation marks present")
    if rep["contractions"]:
        f.append("contractions present")
    if rep["cite_opens_sentence"]:
        f.append("a sentence opens with a citation")
    if len(rep["contrast_tic"]) > 2:
        f.append("binary-contrast constructions > 2")
    return f


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--strict", action="store_true", help="exit 1 when a hard limit fails")
    ap.add_argument("--json", action="store_true", help="print the report as JSON")
    args = ap.parse_args()
    with open(args.draft, encoding="utf-8") as fh:
        rep = lint(fh.read())
    if args.json:
        print(json.dumps(rep, indent=2, default=list))
    else:
        print(render(rep))
    bad = failures(rep)
    if bad:
        print("HARD-LIMIT FAILURES: " + "; ".join(bad))
        if args.strict:
            sys.exit(1)
    else:
        print("hard limits: all pass")


if __name__ == "__main__":
    main()
