# Genre study — [VENUE], [YEAR RANGE]

> Template. Copy to your paper folder as `genre-study.md`, then fill it in and
> delete these quote blocks. A worked example is in
> `examples/genre-study-robotics.md`.
>
> This is the output of stage 1 of the workflow: read the genre before writing
> in it. The point is not to admire good papers but to extract the conventions
> your reviewers already expect, so that your own choices are deliberate rather
> than accidental.

**Field:** [e.g. robotics, computer vision, HCI, systems]
**Papers studied:** [N]
**Selection rule:** [e.g. best-paper winners and nominees at VENUE, 2021-2025]
**Compiled:** [date] by [name]

## How this study was built

```bash
# 1. Download and digest the papers
tools/paper_digest.py --arxiv ID --arxiv ID ... -o digests/

# 2. Aggregate word choice and figure-reference phrasing
tools/paper_digest.py --phrasing 'digests/*.txt'
```

Then read every `.digest.md` and fill in the sections below. Digests give you
headings, captions, and the contribution and limitation sentences; the phrasing
run gives you the counts. Anything the tools cannot see, such as where Figure 1
sits on the page, you read off the PDFs yourself.

> Ten to twenty papers is enough to see a convention. Fewer than about eight and
> you are reading noise. Pick award winners and nominees: those are the papers
> reviewers, area chairs, and an award committee all judged to be good, so their
> conventions are the safest to adopt.

## Reading list

| Paper | Venue and award | Identifier |
|---|---|---|
| [title] | [venue, year, award] | [arXiv id or DOI] |
| | | |

> Keep the identifier so anyone can reproduce the digest. Note when a paper is
> an outlier you included deliberately.

## Structure

> Answer from the `--- HEADINGS ---` block of each digest.

- **Section order.** [The order most papers follow, and how many deviate.]
- **Where Related Work sits.** [Section 2, or after the method?]
- **Is there a Problem Statement or Preliminaries section?** [How many use one.]
- **Limitations.** [A named section, the last subsection of Experiments, a
  paragraph in the conclusion, or absent?]
- **Section count and page budget.** [Typical count; what gets the most space.]

## Contributions

> Answer from the `CONTRIB>` lines of each digest.

- **Where the list sits.** [End of the introduction, or nowhere?]
- **Form.** [Numbered list, bulleted list, or a prose sentence?]
- **How many.** [Typical number.]
- **Phrasing.** [Nouns naming what was built or measured, or verbs naming
  activities? Quote two examples verbatim.]
- **Do any state what is *not* new?** [Papers that disclaim before claiming.]

## Abstract

- **Move order.** [e.g. context, gap, what we do, headline numbers.]
- **Does it carry numbers?** [How many papers put a measured result in the
  abstract, and how precisely.]
- **Last sentence.** [Release statement, project page, a claim, or a limitation?]
- **Length.** [Typical word count.]

## Figures and captions

- **Figure 1.** [What it shows: a system photo, a teaser, a pipeline diagram,
  a revealing example. Where it sits on page 1. Does it span both columns?]
- **Does the caption of Figure 1 carry the headline result?** [How many do.]
- **Caption shape.** [The pattern most captions follow. Quote one verbatim.]
- **Caption length.** [Typical; do captions stand alone without the body text?]
- **How failures are shown.** [A photo strip, a lettered list, a table of counts,
  or not at all.]
- **Figure count.** [Typical number, and how many span both columns.]

## Results reporting

- **How success is reported.** [Percentages, k/n fractions, both?]
- **Uncertainty.** [Confidence intervals, standard deviations, or bare point
  estimates? How many papers report n?]
- **Comparison tables.** [Do they include protocol columns that make the
  comparison honest? Is a caveat stated about differing protocols?]
- **Failure analysis.** [Are failure modes named and counted? Quote one
  sentence that admits a failure.]

## Word choice

> Fill the counts from `tools/paper_digest.py --phrasing`. Record totals across
> the set, and note the per-paper average where it matters.

| Form | Count |
|---|---|
| "as shown in Fig. N" | |
| "(Fig. N)" parenthetical | |
| "Fig. N shows / illustrates" | |
| "we show" | |
| "we propose" | |
| "we present" | |
| "note that" | |
| [add the terms your field argues about] | |

- **Em-dashes per paper:** [ ]
- **Semicolons per paper:** [ ]
- **Tense.** [Present or past, for related work and for the conclusion?]
- **Person.** [First-person plural, or passive?]
- **Field terms a general writing guide would flag but this genre accepts.**
  [e.g. "novel", "robust". List them, with counts, so your lint does not fight
  the convention.]

## What I will copy

> Three to six specific, testable moves. Each becomes a candidate rule in your
> style spec (`skills/paper-pipeline/data/style-spec.md`), so phrase it as an
> instruction, not an observation. Cite the paper it came from.

1. [Move, and the paper it came from.]
2.
3.

## What I will not copy

> Mandatory. It forces critical reading and marks the boundary of the
> convention: the genre does some things because they are right and others out
> of habit.

1. [Practice, and why it does not serve your paper.]
2.

## Open questions

> Conventions you could not resolve from the sample, or where the papers
> disagree. Note how you plan to decide.

-
