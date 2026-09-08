#!/usr/bin/env python3
"""Fetch a web page and reduce it to readable plain text.

Use it to pull writing guides or blog posts into a local file you can read in
full, instead of relying on a summariser. Sends a browser-like User-Agent;
some hosts (Medium, for example) still refuse automated clients, in which
case try a mirror of the same post.

Usage:
  fetch_text.py URL [-o OUT.txt] [--min-words N]
"""

import argparse
import html
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

_BLOCKED_MARKERS = ("Attention Required! | Cloudflare", "Just a moment...",
                    "Enable JavaScript and cookies to continue")


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


def html_to_text(raw):
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    raw = re.sub(r"<(script|style|noscript|svg|nav|footer)[^>]*>.*?</\1>", "", raw,
                 flags=re.S | re.I)
    raw = re.sub(r"<h([1-6])[^>]*>", lambda m: "\n\n" + "#" * int(m.group(1)) + " ",
                 raw, flags=re.I)
    raw = re.sub(r"</h[1-6]>", "\n", raw, flags=re.I)
    raw = re.sub(r"<li[^>]*>", "\n- ", raw, flags=re.I)
    raw = re.sub(r"<(p|div|br|blockquote|figcaption|tr)[^>]*>", "\n", raw,
                 flags=re.I)
    text = re.sub(r"<[^>]+>", "", raw)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    # drop empty list bullets left by icon-only <li> elements
    text = re.sub(r"^- *$", "", text, flags=re.M)
    # drop lines holding no letters or digits (stray markup fragments), then
    # normalise the blank lines those removals leave behind
    text = "\n".join(ln.rstrip() for ln in text.split("\n")
                     if re.search(r"[A-Za-z0-9]", ln) or not ln.strip())
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("-o", "--output", help="write text here (default: stdout)")
    ap.add_argument("--min-words", type=int, default=200,
                    help="warn when fewer words than this were recovered")
    args = ap.parse_args()

    try:
        raw = fetch(args.url)
    except Exception as exc:  # noqa: BLE001
        sys.exit("fetch failed: %s" % exc)
    if any(marker in raw for marker in _BLOCKED_MARKERS):
        sys.exit("the host returned a bot-challenge page, not the article; "
                 "try a mirror of the same post")
    text = html_to_text(raw)
    words = len(re.findall(r"[A-Za-z]+", text))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("%d words -> %s" % (words, args.output))
    else:
        sys.stdout.write(text)
    if words < args.min_words:
        print("warning: only %d words recovered; the page may be paywalled "
              "or rendered by JavaScript" % words, file=sys.stderr)


if __name__ == "__main__":
    main()
