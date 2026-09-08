---
name: academic-writing
description: Use when writing or revising any academic text - thesis chapters, conference/journal papers (ICRA, IROS, RSS, RA-L), abstracts, introductions, related work, results sections, figure captions, rebuttals, or LaTeX manuscripts. Also when the user asks to "polish", "tighten", "academicize", or "make this publishable". Enforces story-first structure, claim-evidence discipline, and honest-limitations style for robotics/engineering papers.
---

# Academic Writing

Distilled from Michael Black's "Writing a Good Scientific Paper", Simon Peyton
Jones' "How to Write a Great Research Paper", the Whitesides Group's
outline-first method, and the structure of award-winning robotics systems
papers (SpeedFolding, ALOHA, UMI, FEAST). Apply these rules when drafting; use
the checklists when revising.

## The one non-negotiable

**A paper is one idea, told as a story — not a lab notebook.** The story order
is logical, never chronological. If you cannot state the paper's single
contribution in one sentence, stop writing and find it first. Everything that
does not serve that sentence competes with it.

## Structure rules

### Abstract (write it first, rewrite it last)
Four moves, in order, no fluff:
1. Context + problem (why anyone cares)
2. Why it's hard / why existing work falls short
3. What we do (the idea, named)
4. Quantified results (real numbers, the headline first)

No citations, no "in this paper we present" openers, no undefined acronyms.
If a number appears in the abstract it must appear identically in the body.

### Introduction
- Funnel: broad context → specific problem → why hard → gap → our approach →
  contributions. One paragraph per step, no early reveal of jargon.
- End with an **explicit numbered contributions list**. Each contribution is a
  claim the paper proves, phrased as a noun ("a 60-trial characterization
  of..."), not an activity ("we performed trials...").
- State the research question as a question early — readers evaluate
  everything after it against that question.
- Never promise anything the paper doesn't deliver. Cross-check the
  contributions list against the results section every revision.

### Related work
- Organize by **theme, not by paper**. Each paragraph: what that line of work
  achieves → what it leaves open → one sentence positioning our work.
- Be generous. Praising prior work costs nothing and reads as confidence;
  reviewers are often the authors being cited.
- End each theme with the delta, not a putdown: "we quantify what X did not
  measure", never "unlike X, we actually...".

### System/method sections (systems papers)
- Every paragraph follows *problem faced → design decision → why/validation*
  (the UMI pattern). A component described without the problem it solves gets
  cut.
- State operating parameters in a table, not prose. Derivations of parameters
  ("1.5× observed max") matter more than the values.
- Declare scope and assumptions **before** the method so reviewers judge the
  system against its declared envelope, not their imagination.

### Results
- Define every metric and the success criterion *before* the first result.
- Report: point estimate + dispersion + n + the right test. Success rates get
  exact binomial CIs; skewed timings get median alongside mean; say which
  test and why (Welch for unequal variance, etc.).
- Failure analysis is a feature: taxonomize failures, count them, attribute
  causes. A paper that understands its failures reads as trustworthy.
- Never let a losing number appear before its framing. Pre-frame ("this is a
  reliability result, not a speed result"), then give the number plainly.
- Comparison tables: include the conditions/protocol columns that make the
  comparison honest; caption must say whether it's a normalized ranking or
  positioning evidence.

### Limitations
A named section, not a paragraph hidden in the conclusion. State each limit
plainly, attribute its cause (design trade vs. unfinished work), and say
which are fixable. A reviewer who finds a weakness you didn't state writes a
different review than one who reads you stating it.

### Figures and captions
- Figure 1 sells the idea; a reader who sees only the figures and captions
  must be able to reconstruct the story (that reader is most reviewers).
- Every caption is self-contained: what is shown, how to read it, what to
  conclude. Never "Results of experiment 2."
- Axis labels with units, fonts legible at print size, colorblind-safe.

## Sentence-level rules

- One point per paragraph; the topic sentence states it; reading only topic
  sentences must give a coherent summary (the Whitesides skeleton test).
- Active voice for what you did ("we measure"), passive only when the agent
  is irrelevant. Present tense for what the paper shows and for facts; past
  tense for what happened in experiments.
- One name per concept, forever. If it's the "grip target" in Sec. III it is
  never the "grasp point" in Sec. V. Build a terminology table for the paper.
- Every number: value + unit + uncertainty (where it exists). Write "44%
  slower (p=0.0003)", not "much slower".
- Kill: "very", "novel" (show it instead), "note that", "it is worth
  mentioning", "in order to"→"to", "utilize"→"use", "a large amount
  of"→quantify it.
- Hedging calibration: claim exactly what the evidence supports. "suggests"
  for indication, "shows/demonstrates" for direct evidence, "proves" almost
  never. Never hedge twice ("may potentially suggest").
- No anthropomorphized results ("the data wants..."); "the results indicate"
  is fine.
- Acronyms: define at first use in abstract AND body separately; if used
  fewer than 3 times, don't create it.

## Process

1. **Outline first**: section headers → figure/table list → topic-sentence
   skeleton. Get the skeleton approved (by user/advisor) before prose.
2. Draft fast, revise slow. First-draft prose is scaffolding.
3. **The 20% cut**: after a full draft, cut a fifth. Cut candidates: throat-
   clearing openers, restated context, method detail that belongs in an
   appendix/repo, adjectives.
4. Consistency pass before any submission: every number appears identically
   in abstract, body, tables, and conclusion; every citation resolves; every
   figure/table/section reference is live; contribution list ↔ results ↔
   conclusion all match.
5. For anonymized venues: sweep for names, affiliations, grant IDs,
   identifying URLs, "our previous work [X]" phrasing, and PDF metadata.

## Venue mechanics (conference papers)

- Plan the page budget *before* writing: assign pages per section, count
  figures at final size. Cutting late destroys structure; planning early
  doesn't.
- Respect hard limits literally (page count includes references at ICRA).
- Video is a first-class artifact for systems papers: show one full cycle in
  real time, each failure mode once, then a montage. Keep the paper text
  quantitative and let the video carry qualitative evidence.
- Check the venue's AI-disclosure policy; ICRA 2027 requires disclosure of
  AI-generated content in the acknowledgments.

## Thesis ↔ paper conversion

- A paper is not a compressed thesis; it is the thesis's single strongest
  claim with only the evidence that proves it. Cut whole thesis chapters, not
  paragraphs from every chapter.
- Anything promised-but-not-done in the thesis (future-work stages,
  scaffolded sections) must not appear in the paper as a claim or a title
  word.
- Thesis chapters may re-expand paper sections, but keep numbers and
  terminology synchronized in both directions.

## Revision checklist (run on request or before any hand-off)

- [ ] One-sentence contribution statable? Appears in abstract, intro, conclusion?
- [ ] Abstract: 4 moves present, numbers match body?
- [ ] Contributions list ↔ results sections one-to-one?
- [ ] Topic-sentence skeleton reads coherently alone?
- [ ] Every metric defined before use; every rate has n and CI?
- [ ] Failure modes taxonomized and counted?
- [ ] Limitations named, caused, and triaged?
- [ ] Captions self-contained; Figure 1 tells the story?
- [ ] Terminology: one name per concept throughout?
- [ ] Weak-number pre-framing in place; nothing hidden?
- [ ] 20% cut attempted; page budget met with margin?
- [ ] Anonymity/metadata sweep done (if double-anonymous)?
