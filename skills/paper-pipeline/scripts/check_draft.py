#!/usr/bin/env python3
"""CLI: mechanical per-section draft gate (draft-guard's reproducible half).

Usage:
  check_draft.py DRAFT --bib BIB [--stance L2] [--lexicon PATH] [--discipline NAME]

Checks: every in-text citation resolves against BIB; realized stance phrases
do not exceed the declared level. Prints findings with line numbers; exit 1
on any unresolved citation or stance excess.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ppl"))

import citecheck  # noqa: E402
import stance  # noqa: E402

DEFAULT_LEXICON = os.path.join(os.path.dirname(HERE), "data", "stance-lexicon.yaml")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--bib", required=True)
    ap.add_argument("--stance", default=None, help="declared stance level of the section")
    ap.add_argument("--lexicon", default=DEFAULT_LEXICON)
    ap.add_argument("--discipline", default=None)
    args = ap.parse_args()

    with open(args.draft, encoding="utf-8") as fh:
        draft = fh.read()
    with open(args.bib, encoding="utf-8") as fh:
        bib = fh.read()

    failed = False
    result = citecheck.scan(draft, bib)
    print("citations resolved: %d" % result["resolved_count"])
    for u in result["unresolved"]:
        failed = True
        print("error   CITE_UNRESOLVED      line %d: %s citation %r has no "
              "bibliography entry" % (u.line, u.kind, u.key))

    if args.stance:
        lex = stance.load_lexicon(args.lexicon, args.discipline)
        for hit in stance.scan_draft(draft, args.stance, lex):
            failed = True
            print("error   STANCE_EXCEEDED     line %d: %r is %s language but the "
                  "section is declared %s" % (hit.line, hit.phrase,
                                              hit.phrase_level, args.stance))

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
