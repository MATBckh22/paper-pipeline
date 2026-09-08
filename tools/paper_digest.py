#!/usr/bin/env python3
"""Turn a set of paper PDFs into structural digests you can read side by side.

For each PDF the tool writes <name>.txt (full extracted text) and
<name>.digest.md containing: the title/abstract head, the section headings,
every figure and table caption, and the sentences around "contributions",
"limitations", and "conclusion". Read the digests to learn how a genre
arranges its figures, phrases its claims, and admits its failures.

Requires pypdf (pip install pypdf). Downloads use only the standard library.

Usage:
  paper_digest.py PAPER.pdf [MORE.pdf ...] -o DIGESTS/
  paper_digest.py --arxiv 2208.10552 --arxiv 2309.06440 -o DIGESTS/
  paper_digest.py --phrasing DIGESTS/*.txt        # aggregate phrasing statistics
"""

import argparse
import collections
import glob
import os
import re
import sys
import urllib.request

_HEADING = re.compile(
    r"^(?:(?:I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\.\s+[A-Z][A-Za-z\- ,&:]{2,60}"
    r"|[A-H]\.\s+[A-Z][A-Za-z\- ,&:]{2,70})$")
_CAPTION = re.compile(r"^(Fig\.|Figure|TABLE|Table)\s*[IVX\d]+[\.:]")
_CONTRIB = re.compile(
    r"contributions? (are|is|of this|include)|we make the following|our contributions|"
    r"main contributions|In summary, (we|our)|This paper (makes|contributes)|contributions:",
    re.I)
_LIMIT = re.compile(r"^(?:[IVX]+\.\s+|[A-H]\.\s+)?(LIMITATIONS|Limitations)\b")
_CONCL = re.compile(r"^(?:[IVX]+\.\s+)?(CONCLUSION|Conclusion)")


def extract_text(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf is required: pip install pypdf")
    reader = PdfReader(pdf_path)
    return "\n".join((page.extract_text() or "") for page in reader.pages), len(reader.pages)


def digest(name, text, head=45):
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    out = ["===== %s =====" % name, "--- HEAD (title/abstract) ---"]
    out.extend(lines[:head])
    out.append("--- HEADINGS ---")
    out.extend(ln for ln in lines if _HEADING.match(ln))
    out.append("--- FIGURE/TABLE CAPTIONS ---")
    for i, ln in enumerate(lines):
        if _CAPTION.match(ln):
            out.append(" ".join(lines[i:i + 4])[:700])
    out.append("--- CONTRIBUTIONS / LIMITATIONS / CONCLUSION context ---")
    for i, ln in enumerate(lines):
        if _CONTRIB.search(ln):
            out.append("CONTRIB> " + " ".join(lines[i:i + 8])[:900])
        if _LIMIT.match(ln):
            out.append("LIMIT> " + " ".join(lines[i:i + 6])[:700])
        if _CONCL.match(ln):
            out.append("CONCL> " + " ".join(lines[i:i + 5])[:600])
    return "\n".join(out) + "\n"


def download_arxiv(arxiv_id, outdir):
    url = "https://arxiv.org/pdf/%s" % arxiv_id
    dest = os.path.join(outdir, "%s.pdf" % arxiv_id.replace("/", "_"))
    if not os.path.exists(dest):
        req = urllib.request.Request(url, headers={"User-Agent": "paper-digest/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp, open(dest, "wb") as fh:
            fh.write(resp.read())
    return dest


def phrasing_report(text_paths):
    text = " ".join(open(p, encoding="utf-8", errors="ignore").read() for p in text_paths)
    text = re.sub(r"-\s+", "", text)  # undo hyphenation across lines
    text = re.sub(r"\s+", " ", text)
    n = max(1, len(text_paths))
    forms = collections.OrderedDict([
        ("(Fig. N) parenthetical", r"\(Fig(?:ure|\.)\s*\d+[^)]*\)"),
        ("Fig. N shows/illustrates", r"Fig(?:ure|\.)\s*\d+\s+(?:shows|illustrates|depicts|presents|summarizes|visualizes|compares)"),
        ("as shown in Fig. N", r"(?:as|As) (?:shown|illustrated|depicted|seen) in Fig(?:ure|\.)\s*\d+"),
        ("In Fig. N, ...", r"(?:In|in) Fig(?:ure|\.)\s*\d+\s*,"),
        ("see Fig. N", r"see Fig(?:ure|\.)\s*\d+"),
    ])
    print("Figure-reference phrasing across %d papers:" % n)
    for label, pat in forms.items():
        print("  %5d  %s" % (len(re.findall(pat, text)), label))
    words = ["we present", "we propose", "we show", "we demonstrate", "we find",
             "we observe", "note that", "in order to", "utilize", "leverage",
             "novel", "robust", "however", "moreover", "furthermore", "additionally",
             "in this paper", "in this work", "to the best of our knowledge",
             "we believe", "we hypothesize"]
    low = text.lower()
    print("Word/phrase counts (total across papers):")
    for w in words:
        print("  %5d  %s" % (low.count(w), w))
    print("Em-dashes per paper: %.1f   semicolons per paper: %.1f"
          % (text.count("—") / n, text.count(";") / n))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdfs", nargs="*", help="PDF files to digest")
    ap.add_argument("--arxiv", action="append", default=[],
                    help="arXiv id to download first (repeatable)")
    ap.add_argument("-o", "--outdir", default="digests")
    ap.add_argument("--head", type=int, default=45,
                    help="lines of the head block (title + abstract)")
    ap.add_argument("--phrasing", nargs="*", metavar="TXT",
                    help="aggregate phrasing statistics over extracted .txt files")
    args = ap.parse_args()

    if args.phrasing is not None:
        paths = []
        for pattern in (args.phrasing or [os.path.join(args.outdir, "*.txt")]):
            paths.extend(glob.glob(pattern))
        if not paths:
            sys.exit("no .txt files found for --phrasing")
        phrasing_report(sorted(paths))
        return

    os.makedirs(args.outdir, exist_ok=True)
    pdfs = list(args.pdfs)
    for arxiv_id in args.arxiv:
        pdfs.append(download_arxiv(arxiv_id, args.outdir))
    if not pdfs:
        ap.error("give PDF paths, --arxiv ids, or --phrasing")

    for pdf in pdfs:
        name = os.path.splitext(os.path.basename(pdf))[0]
        try:
            text, pages = extract_text(pdf)
        except Exception as exc:  # noqa: BLE001
            print("%s: extraction failed (%s)" % (pdf, exc))
            continue
        with open(os.path.join(args.outdir, name + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        d = digest(name, text, args.head)
        with open(os.path.join(args.outdir, name + ".digest.md"), "w", encoding="utf-8") as fh:
            fh.write(d)
        print("%-40s %3d pages %6d words -> %s.digest.md"
              % (name, pages, len(text.split()), name))


if __name__ == "__main__":
    main()
