#!/usr/bin/env python3
"""Mechanical integrity checks for a LaTeX manuscript that carries its own
\\bibitem bibliography (the usual conference-template setup).

Checks:
  * every \\ref resolves to a \\label; unreferenced labels are listed
  * every \\includegraphics file exists (honours \\graphicspath, or --figdir)
  * braces and common environments balance
  * every \\cite key has a \\bibitem; every \\bibitem is cited
  * \\bibitem order matches first-citation order (numeric styles)
  * multi-key citations are in numeric order (--sort-cites rewrites them)

Extras:
  --diff-numbers OLD.tex   list numeric tokens that disappeared from or
                           appeared in the body relative to an older draft
                           (proves a revision changed no statistic)
  --contributions          print the numbered contributions list

Exit status 1 on any error (unresolved ref or cite, missing figure,
unbalanced braces or environment).

Usage:
  tex_integrity.py DRAFT.tex [--figdir DIR] [--sort-cites] [--reorder-bib]
                   [--diff-numbers OLD.tex] [--contributions]
"""

import argparse
import os
import re
import shutil
import sys

ENVS = ["figure", "figure*", "table", "table*", "tabular", "tabularx", "enumerate",
        "itemize", "abstract", "center", "document", "equation", "align", "algorithmic"]


def strip_comments(src):
    return re.sub(r"(?<!\\)%[^\n]*", "", src)


def split_bib(src):
    if r"\begin{thebibliography}" in src:
        body, bib = src.split(r"\begin{thebibliography}", 1)
        return body, r"\begin{thebibliography}" + bib
    return src, ""


def graphics_dirs(src, tex_dir, override):
    if override:
        return [override]
    m = re.search(r"\\graphicspath\{((?:\{[^}]*\})+)\}", src)
    dirs = re.findall(r"\{([^}]*)\}", m.group(1)) if m else [""]
    return [os.path.join(tex_dir, d) for d in dirs]


def cite_keys(text):
    keys = []
    for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", text):
        keys.extend(k.strip() for k in m.group(1).split(","))
    return keys


def check(path, figdir=None):
    src = strip_comments(open(path, encoding="utf-8").read())
    body, bib = split_bib(src)
    errors, notes = [], []

    labels = set(re.findall(r"\\label\{([^}]*)\}", src))
    refs = set(re.findall(r"\\(?:eq|page|auto)?ref\{([^}]*)\}", src))
    for r in sorted(refs - labels):
        errors.append("unresolved \\ref{%s}" % r)
    unref = sorted(labels - refs)
    if unref:
        notes.append("labels never referenced: %s" % ", ".join(unref))

    tex_dir = os.path.dirname(os.path.abspath(path))
    dirs = graphics_dirs(src, tex_dir, figdir)
    for f in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", src):
        candidates = [os.path.join(d, f) for d in dirs] + [os.path.join(tex_dir, f)]
        if not any(os.path.exists(c) or any(os.path.exists(c + ext) for ext in
                   (".pdf", ".png", ".jpg", ".jpeg", ".eps")) for c in candidates):
            errors.append("figure file not found: %s" % f)

    unescaped = re.sub(r"\\[{}]", "", src)
    bal = unescaped.count("{") - unescaped.count("}")
    if bal:
        errors.append("brace balance off by %+d" % bal)
    for env in ENVS:
        b = len(re.findall(r"\\begin\{" + re.escape(env) + r"\}", src))
        e = len(re.findall(r"\\end\{" + re.escape(env) + r"\}", src))
        if b != e:
            errors.append("environment %s: %d begin / %d end" % (env, b, e))

    bibkeys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", bib)
    order, seen = [], set()
    for k in cite_keys(body):
        if k not in seen:
            seen.add(k)
            order.append(k)
    if bib:
        for k in order:
            if k not in bibkeys:
                errors.append("citation key has no \\bibitem: %s" % k)
        uncited = [k for k in bibkeys if k not in seen]
        if uncited:
            notes.append("bibitems never cited: %s" % ", ".join(uncited))
        mism = [(a, b) for a, b in zip(order, bibkeys) if a != b]
        if mism:
            notes.append("bibitem order differs from first-citation order at %d position(s); "
                         "first: cited %s, listed %s (use --reorder-bib)"
                         % (len(mism), mism[0][0], mism[0][1]))
        idx = {k: i for i, k in enumerate(bibkeys)}
        unsorted = 0
        for m in re.finditer(r"\\cite[tp]?\*?(?:\[[^\]]*\])?\{([^}]*)\}", body):
            ks = [k.strip() for k in m.group(1).split(",")]
            if ks != sorted(ks, key=lambda k: idx.get(k, 999)):
                unsorted += 1
        if unsorted:
            notes.append("%d multi-key citation(s) not in numeric order (use --sort-cites)" % unsorted)
    return errors, notes


def sort_cites(path):
    src = open(path, encoding="utf-8").read()
    body, bib = split_bib(src)
    bibkeys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", bib)
    idx = {k: i for i, k in enumerate(bibkeys)}

    def fix(m):
        ks = [k.strip() for k in m.group(2).split(",")]
        return m.group(1) + "{" + ", ".join(sorted(ks, key=lambda k: idx.get(k, 999))) + "}"
    new_body, n = re.subn(r"(\\cite[tp]?\*?(?:\[[^\]]*\])?)\{([^}]*)\}", fix, body)
    changed = sum(1 for a, b in zip(re.findall(r"\\cite[^{]*\{[^}]*\}", body),
                                    re.findall(r"\\cite[^{]*\{[^}]*\}", new_body)) if a != b)
    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(new_body + bib)
    print("sorted %d citation(s); backup at %s.bak" % (changed, path))


def reorder_bib(path):
    src = open(path, encoding="utf-8").read()
    body, bib = split_bib(src)
    if not bib:
        sys.exit("no thebibliography environment found")
    head, rest = bib.split("\\bibitem", 1)
    entries = ["\\bibitem" + e for e in ("\\bibitem" + rest).split("\\bibitem")[1:]]
    tail = ""
    if r"\end{thebibliography}" in entries[-1]:
        entries[-1], tail = entries[-1].split(r"\end{thebibliography}", 1)
        tail = r"\end{thebibliography}" + tail
    by_key = {re.search(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", e).group(1): e for e in entries}
    order, seen = [], set()
    for k in cite_keys(strip_comments(body)):
        if k not in seen and k in by_key:
            seen.add(k)
            order.append(k)
    order += [k for k in by_key if k not in seen]  # uncited entries go last
    new_bib = head + "".join(by_key[k].rstrip("\n") + "\n\n" for k in order) + tail
    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(body + new_bib)
    print("reordered %d bibitems to first-citation order; backup at %s.bak" % (len(order), path))


def numbers(path):
    src = strip_comments(open(path, encoding="utf-8").read())
    body, _ = split_bib(src)
    body = body.split(r"\begin{document}")[-1]
    return set(re.findall(r"\d+(?:[.,]\d+)?", body))


def contributions(path):
    src = strip_comments(open(path, encoding="utf-8").read())
    m = re.search(r"contribut[^\n]*\n?\s*\\begin\{enumerate\}(.*?)\\end\{enumerate\}", src, re.S | re.I)
    if not m:
        print("no contributions list found")
        return
    for i, item in enumerate([x for x in re.split(r"\\item\s*", m.group(1)) if x.strip()], 1):
        print("%d. %s\n" % (i, re.sub(r"\s+", " ", item).strip()))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--figdir", help="directory holding the figure files")
    ap.add_argument("--sort-cites", action="store_true")
    ap.add_argument("--reorder-bib", action="store_true")
    ap.add_argument("--diff-numbers", metavar="OLD.tex")
    ap.add_argument("--contributions", action="store_true")
    args = ap.parse_args()

    if args.sort_cites:
        sort_cites(args.draft)
    if args.reorder_bib:
        reorder_bib(args.draft)
    if args.contributions:
        contributions(args.draft)
        return
    if args.diff_numbers:
        old, new = numbers(args.diff_numbers), numbers(args.draft)
        key = lambda x: float(x.replace(",", ""))  # noqa: E731
        print("numbers dropped since %s: %s" % (args.diff_numbers, sorted(old - new, key=key)))
        print("numbers new in %s: %s" % (args.draft, sorted(new - old, key=key)))

    errors, notes = check(args.draft, args.figdir)
    for n in notes:
        print("note   " + n)
    for e in errors:
        print("error  " + e)
    print("integrity: %d error(s), %d note(s)" % (len(errors), len(notes)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
