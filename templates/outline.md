# Outline — [PAPER SHORT NAME] (section I/O contracts)

> Template. Copy to your paper folder as `outline.md`, fill it in, and mirror
> it into the `outline:` block of your paper-config. Delete these quote blocks.
>
> Document order equals section order. `inputs` name what a section assumes,
> either a frame artifact or an earlier section id. `output` is the belief the
> reader holds after reading it, never a topic: reject "describes the
> perception system", accept "reader believes the target is localized to under
> 5 mm".

| § | Heading | Assumes | Reader believes after it | Stance | Figures |
|---|---------|---------|--------------------------|--------|---------|
| 1 | Introduction | gap_statement | [belief] | L3 | fig-[name] |
| 2 | Related Work | gap_statement | [belief] | L3 | — |
| 3 | [Method / System] | 1 | [belief] | L1 | fig-[name] |
| 4 | [Protocol] | 3 | [belief] | L1 | — |
| 5 | Results | 4 | [belief] | L3 | fig-[name] |
| 6 | Limitations | 5 | [belief] | L1 | — |
| 7 | Conclusion | 5, 6 | [belief] | L3 | — |

## Stance levels

> From `skills/paper-pipeline/data/stance-lexicon.yaml`. The stance recorded
> above is the *effective* level after clamping.

| Level | Name | Evidence it requires |
|---|---|---|
| L1 | report | the measurement exists |
| L2 | suggest | own data, one interpretation among several |
| L3 | argue | own data plus converging support, alternatives addressed |
| L4 | assert | direct, controlled, alternatives excluded |

## Evidence notes and clamping

> Write the evidence note BEFORE choosing the stance. The note sets a ceiling;
> your intent cannot exceed it. Record any clamp and the cue that caused it, so
> the decision is auditable. You may raise a ceiling by adding evidence; never
> by raising the stance.

| § | Evidence note | Ceiling | Declared | Effective | Cue |
|---|---|---|---|---|---|
| 1 | [what the evidence is] | | | | |
| 5 | [what the evidence is] | | | | |

## Validator run notes

> Paste the outcome of
> `python3 skills/paper-pipeline/scripts/validate_config.py config.yaml`
> and adjudicate every warning and notice. Confirmed warnings are fine; record
> why they are intentional.

**Errors:** [count]
**Confirmed warnings:** [e.g. sections carrying claims on prose alone]
**Stance adjudications:** [any CEILING_AMBIGUOUS notices and how you resolved
them, naming the evidence predicate you applied]
