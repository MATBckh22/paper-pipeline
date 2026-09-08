#!/usr/bin/env bash
# Run the full mechanical gate on one manuscript.
#
#   tools/run_gate.sh DRAFT.tex [STANCE] [BIB]
#
# STANCE is the declared rhetorical level for the whole draft (L1-L4, default
# L3; see skills/paper-pipeline/data/stance-lexicon.yaml). BIB defaults to the
# draft itself, which is right when the bibliography is an inline
# \begin{thebibliography} block; pass a .bib file otherwise.
#
# Exit status is non-zero if any of the three checks fails.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
DRAFT="${1:?usage: run_gate.sh DRAFT.tex [STANCE] [BIB]}"
STANCE="${2:-L3}"
BIB="${3:-$DRAFT}"

echo "== 1/3 citations + stance (declared $STANCE) =="
python3 "$ROOT/skills/paper-pipeline/scripts/check_draft.py" "$DRAFT" --bib "$BIB" \
  --stance "$STANCE" --lexicon "$ROOT/skills/paper-pipeline/data/stance-lexicon.yaml"
s1=$?
echo
echo "== 2/3 prose lint =="
python3 "$HERE/lint_prose.py" "$DRAFT" --strict
s2=$?
echo
echo "== 3/3 structural integrity =="
python3 "$HERE/tex_integrity.py" "$DRAFT"
s3=$?
echo
if [ $((s1 | s2 | s3)) -eq 0 ]; then
  echo "GATE: pass"
else
  echo "GATE: fail (citations/stance=$s1, lint=$s2, integrity=$s3)"
fi
exit $((s1 | s2 | s3))
