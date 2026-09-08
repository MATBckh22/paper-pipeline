# Writing checklist

A working paraphrase of the rules this pipeline enforces or asks an author to
apply by hand. The primary source is Michael J. Black, "Writing a good
scientific paper" (Perceiving Systems blog, 8 November 2024, mirrored at
https://perceiving-systems.blog/en/post/writing-a-good-scientific-paper).
Read the original in full; this list is a reminder, not a substitute.
Items marked [gate] are checked mechanically by `tools/run_gate.sh`.

## Story

- One paper, one idea. If two ideas compete, the reader remembers neither.
- Goal, problem, solution, repeated. State what the reader should want,
  take it away, then give it back with the insight.
- Write the talk first, or explain the work aloud to a friend; the order you
  explain it in is the order of the paper.
- Name the nugget: the insight that makes the unsolvable solvable. It is not
  the technical contribution; it is what led to it.
- State the hypothesis, even if the sentence never appears in the paper.

## Title, abstract, teaser

- The title is the abstract in one line. Short, suggestive, not cute.
- Abstract in the rhythm: what is widely done, what recent work does, what it
  fails to do, what you do, what that still leaves open, what you do about it,
  what you measured. End with the release statement.
- Figure 1 is the abstract as a picture: a revealing example, a summary of
  results, or a system overview only if it is cartoon-simple. Page one.

## Introduction and related work

- Why the problem matters and why it is unsolved, in the first paragraph.
- Contributions in one place, numbered, each a noun the paper proves.
- Related work by theme, in the present tense, teaching the history. Go back
  in time; state what prior work got right before what it left open.
- Never cite as a noun ("[12] showed"); write the authors' names. [gate]
- Keep multi-citations in numeric order. [gate]

## Method and experiments

- Introduce each design element with the problem it solves and what it costs.
- Parameters in a table, with their derivation.
- The equations must match the code; the parameters in the paper must be the
  ones the experiment ran.
- Change one thing at a time; if you removed several things together, say the
  deficit cannot be attributed among them.
- Report point estimate, dispersion, n, and the test used; k/n fractions for
  success rates.
- Pre-frame a losing number before it appears; never let the reader discover
  it.
- Failures are a feature: name them, count them, attribute them.

## Figures and captions

- Figures at the top of the page ([t]), never mid-column.
- Every caption states what is shown, what to look at, what the colours mean,
  and what to conclude. A reader of figures and captions alone should follow
  the story.
- Text in figures legible at print size.
- "Figure 3 shows", not "In Figure 3 we show". [gate reports the opener]

## Sentences

- Present tense throughout, including related work and the conclusion.
- Direct verbs. Avoid "can be", "allows to", vague "provides" and "enables".
- "More" and "better" need "than what".
- No contractions, no exclamation marks. [gate]
- Em-dashes at most three, ideally none. Semicolons at most two per thousand
  words. [gate]
- The "not X, Y" contrast at most twice in a paper. [gate]
- Hyphenate compound adjectives: low-cost, open-loop, per-trial.
- Delete throat-clearing: "it is worth noting", "in order to", "note that".
- Do not sell. No "novel", "honest", "cheapest possible"; show it instead.
- Hedge exactly as far as the evidence allows: report, suggest, argue,
  assert are four different levels. [gate checks the declared level]

## Limitations and conclusion

- A named Limitations section. Attribute each limit to a design trade or to
  unfinished work, with a path forward.
- The conclusion is a second abstract in the present tense with a little more
  analysis; future work brief.
- Mention the supplementary video or material in the text if it exists.

## Before submission

- Fill the page limit; cut a fifth if over, starting with paragraph-final
  orphan lines and restated context.
- Every number identical in abstract, body, tables, and conclusion. [gate:
  numeric diff]
- Proofread the bibliography; search the PDF for "?".
- Anonymity sweep and PDF metadata for double-blind venues.
