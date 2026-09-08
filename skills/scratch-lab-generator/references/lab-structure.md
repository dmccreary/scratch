---
name: lab-structure
description: The anatomy of a generated Scratch lab page, the mascot pose vocabulary, and Cody's voice rules.
---

# Lab Structure and Mascot Voice

## Why a lab is shaped this way

A CoderDojo lab is not a tutorial. A tutorial tells a student what to type; a
lab hands them a problem and lets them discover the answer. The structure below
follows **predict → attempt → check → reveal**, and the order matters: a
solution shown before the student has struggled with the problem is a solution
they will not remember.

That is why the finished program lives inside a collapsed `???` block. The
student has to choose to open it.

## Page anatomy

A lab directory looks like this:

```
docs/labs/<lab-slug>/
├── index.md        the complete lab, generated from the template
├── starter.txt     block source for the "before" program  (optional)
├── starter.sb3     compiled, loadable Scratch project     (generated)
├── solution.txt    block source for the "after" program   (required)
└── solution.sb3    compiled, loadable Scratch project     (generated)
```

`index.md` follows `assets/templates/lab-index-template.md` in this order:

| Section | Purpose | Mascot |
|---------|---------|--------|
| Title + `lab-meta` strip | Level, time, owning chapter | — |
| **Cody's Challenge** | The problem, in Cody's voice. This is the hook. | `mascot-welcome` |
| What You Will Learn | 2-4 bullets, one per learning-graph concept | — |
| Before You Start | Prerequisite labs or chapters | — |
| The Starter Program | The broken or incomplete program, plus its diagram and download | — |
| **Predict Before You Run** | A question answered *before* clicking the flag | `mascot-thinking` |
| Your Task | Numbered steps — what to do, never how to click | — |
| **Cody's Tip** | The one hint that unlocks the concept | `mascot-tip` |
| **Watch Out** | The specific mistake this lab provokes | `mascot-warning` |
| Check Your Work | Observable success criteria, not "it works" | — |
| **Stuck?** (collapsed) | A stronger hint, still not the answer | `mascot-encourage` |
| The Solution (collapsed) | Finished diagram, download, and *why* it works | — |
| **You Did It!** | What the student can now do that they could not before | `mascot-celebration` |
| Go Further | 2-3 extension challenges, no answers given | — |
| Where This Goes Next | Link forward to the next lab | `mascot-neutral` |
| Blocks Used | Table: block, palette, what it does | — |
| Concepts Covered | Links to the chapter and learning graph | — |

Sections marked required in `scripts/check_lab.py` must be present. Sections
that do not apply to a particular lab may be dropped — a lab with no starter
program has no starter section — but never drop the challenge or the
celebration.

## The two programs

Most labs ship **two** block programs:

- **`starter.txt`** — the "before" state. This is what makes it a lab rather
  than a reading. It is either
  - *incomplete*: a loop with an empty body, a missing turn block; or
  - *broken*: a plausible bug — a `turn` of 90 where the shape needs 60, a
    `pen down` placed after the movement instead of before.
- **`solution.txt`** — the "after" state, the working program.

The starter should be **one idea away** from the solution. If a student has to
discover three separate things, split it into two labs.

A lab may legitimately have only `solution.txt` — a from-scratch build where
the challenge is the blank canvas. In that case the starter section is omitted.

## Mascot pose vocabulary

The seven generated poses live in `docs/img/mascot/`. Each maps to one CSS
admonition class:

| Pose file | Class | Use it for |
|-----------|-------|------------|
| `welcome.png` | `mascot-welcome` | The opening challenge. Exactly one per lab. |
| `thinking.png` | `mascot-thinking` | A prediction question, or a key insight. |
| `tip.png` | `mascot-tip` | A hint that helps without giving the answer. |
| `warning.png` | `mascot-warning` | The mistake this lab is designed to surface. |
| `encouraging.png` | `mascot-encourage` | The "stuck?" hint, and hard steps. |
| `celebration.png` | `mascot-celebration` | Lab complete. Exactly one per lab. |
| `neutral.png` | `mascot-neutral` | Side notes, forward links, anything else. |

Image paths are relative to the **rendered URL**, not the source file. A lab at
`docs/labs/<slug>/index.md` renders at `labs/<slug>/`, so mascot images are
always `../../img/mascot/<pose>.png`.

Always place the image in the admonition **body**, never the title bar:

```markdown
!!! mascot-tip "Cody's Tip"
    ![Cody giving a tip](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    A square has four corners, and the turns have to add up to a full circle.
```

Use four to six mascot admonitions per lab. More than that and the character
stops signalling anything.

## Cody's voice

Cody is the CoderDojo turtle who draws with a pen, already established in
`docs/intro/`. Cody is a fellow learner, not a teacher.

- **First person, present tense.** "I started a program..." not "The student
  will be given a program."
- **Cody owns the mistakes.** "I forgot something" beats "you must add".
  A bug that belongs to the mascot is safe to laugh at; a bug that belongs to
  the student is not.
- **Ask, don't tell.** End the challenge with a real question.
- **Short sentences.** The audience is roughly ages 8-14 and many are reading
  their first program.
- **No jargon before it is earned.** Say "the blocks inside the loop" until the
  lab has taught the words "loop body".
- **Never reveal the answer in a tip.** A tip narrows the search; it does not
  end it.

Cody says "steps" and "turn", not "translate" and "rotate". Cody never says
"simply", "just", or "obviously".
