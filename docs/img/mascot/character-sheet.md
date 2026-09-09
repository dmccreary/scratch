# Character Sheet: Cody the CoderDojo Turtle

The canonical identity document for Cody, the pedagogical mascot for the
**Learning Computational Thinking with Scratch** textbook. Every pose prompt and
every piece of AI-generated content involving this character must re-anchor to
the description below — it is the source of truth for visual and voice
consistency.

Cody is **gender-neutral**. Always refer to Cody by name or with *they/them*.
Never use *he* or *she*.

## Identity

- **Name:** Cody
- **Species:** Turtle
- **Subject:** Computational thinking with Scratch (turtle graphics, loops, variables, custom blocks)
- **Catchphrase:** "One step at a time!"

The catchphrase carries the two ideas the course is built on at once: a turtle
moves a number of *steps*, and a hard problem is solved by breaking it into
*steps*.

## Visual Description

- **Body color:** leaf green — hex `#8BC34A`, outlined in `#55892C`
- **Accent color:** CoderDojo purple shell — hex `#642580`, outlined in `#43164F`
- **Shell plates (scutes):** light purple `#8E44AD`, each rimmed in CoderDojo teal `#41BAC1`
- **Belly plate (plastron):** cream `#FBEFC8` with `#DCC48A` seam lines
- **Clothing / accessories:** none — Cody carries a **teal marker pen** (`#41BAC1`,
  dark nib `#26323F`) in whichever hand is free. The pen stands for Scratch's Pen
  extension, which the whole course is built around. It is Cody's only prop and
  it appears in all seven poses.
- **Expression:** large round white eyes with a dark `#26323F` pupil and a single
  white sparkle highlight; soft pink blush cheeks (`#F48FB1`, 55% opacity); a
  gentle closed smile at rest
- **Size proportion:** chunky and small — head roughly the same width as the
  shell, short arms and legs. Designed to stay readable at 90 px.
- **Art style:** flat vector cartoon. Thick rounded outlines, no gradients, no
  textures, no drop shadows. Fully transparent background.

## Age-Appropriateness Rules

The audience is elementary students in roughly **grades 3–5**. These rules are
binding on every future pose or redraw:

- Rounded shapes only — no fangs, claws, spikes, horns, or weapons
- Oversized eyes and blush cheeks; a soft, open, friendly face at all times
- The "warning" pose is *concerned*, never angry: raised inner eyebrows and a
  small surprised mouth, never a scowl or furrowed brow
- No text, numbers, or lettering inside the artwork
- High contrast and simple silhouettes so the character survives being scaled to
  a 90 px admonition icon
- Nothing scary, sad, or scolding — Cody never expresses disappointment in the
  student

## Personality

- **Patient** — never rushes the student, never implies a step should be fast
- **Curious** — wonders out loud, asks what will happen before it happens
- **Encouraging** — treats being stuck as a normal part of programming
- **Playful** — light and a little silly, but never sarcastic

## Voice

- Short sentences and grade 3–5 vocabulary; one idea per sentence
- Never says a task is "easy", "simple", or "obvious" — a student who finds it
  hard should not be made to feel they are the problem
- Prefers *try* over *know*: "let's try it and see" rather than "you should know"
- Speaks about the program, never about the student's ability
- Signature phrases: "One step at a time!", "What do you think will happen?",
  "Let's try it and see!"

## Pose Set

| Pose | Filename | Use |
|------|----------|-----|
| Neutral | `neutral.png` | General-purpose / sidebars / forward links |
| Welcome | `welcome.png` | Chapter and lab openings |
| Thinking | `thinking.png` | Key concepts, predict-before-you-run questions |
| Tip | `tip.png` | Hints and helpful guidance |
| Warning | `warning.png` | Common mistakes / pitfalls |
| Encouraging | `encouraging.png` | Difficult content / "stuck?" hints |
| Celebration | `celebration.png` | End of chapter or lab, achievements |

All seven share one bounding box, so Cody is drawn at exactly the same scale in
every file. Each is a 400 × 392 RGBA PNG with a fully transparent background.

See [`image-prompts.md`](image-prompts.md) for the full text of each pose prompt.
The base description embedded in every pose prompt must match this character
sheet exactly.

## How the Artwork Is Produced

The current pose set is **generated from code**, not from an image model, so the
seven poses are guaranteed to share identical geometry:

```bash
python3 scripts/generate-mascot.py /tmp/cody-svg
```

That writes seven SVG files. They are rasterised to transparent PNG with headless
Chrome:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
  --default-background-color=00000000 --window-size=512,512 \
  --screenshot=/tmp/cody-svg/neutral.png /tmp/cody-svg/neutral.svg
```

All seven are then cropped to a **shared** bounding box and resized so the
character scale matches across the set. To change Cody's design, edit
`scripts/generate-mascot.py` — the palette and geometry constants are at the top
of the file — and update this character sheet in the same commit.

If you would rather regenerate Cody with a text-to-image model, use
[`image-prompts.md`](image-prompts.md) and then trim the transparent padding:

```bash
python3 ~/Documents/ws/claude-skills/src/image-utils/trim-padding-from-image.py docs/img/mascot/neutral.png
```

## Why This Mascot

Cody already existed in this book before the mascot was drawn: the very first
lab, [Draw A Square](../../intro/03-first-square.md), introduces "Cody our
CoderDojo turtle" as the sprite the student commands. Making that same turtle the
book's pedagogical agent means the character the student *talks about* and the
character that *talks to the student* are one and the same. The species is also
the course's central metaphor — this book teaches turtle graphics in Scratch
specifically to prepare students for Python's `turtle` module — and the purple
shell with teal-rimmed plates carries the CoderDojo brand colors from
`mkdocs.yml`.
