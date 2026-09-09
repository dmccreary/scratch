# Content Generation Guide

Rules for generating student-facing content for **Learning Computational
Thinking with Scratch**. Read this before writing chapters, labs, lesson plans,
quizzes, or the FAQ.

Instructor-facing content (the teacher's guide, answer keys, pacing notes) does
**not** use the mascot and does not need to follow the voice rules below.

## Audience

Elementary students, roughly **grades 3–5**, who do not yet type quickly.
Everything is dragged and clicked, never typed. Keep sentences short, define
every new word the first time it appears, and never assume prior programming
experience.

## Learning Mascot: Cody the CoderDojo Turtle

### Mascot File Index

The canonical files for this mascot. When editing any of these, update the
others in the same turn so they stay in sync.

| File | Purpose |
|------|---------|
| [`docs/img/mascot/character-sheet.md`](docs/img/mascot/character-sheet.md) | Canonical identity document (name, species, colors, voice, age rules). Source of truth. |
| [`docs/img/mascot/image-prompts.md`](docs/img/mascot/image-prompts.md) | Self-contained AI prompts for regenerating each pose. |
| [`docs/img/mascot/neutral.png`](docs/img/mascot/neutral.png) | Default / general-purpose pose. |
| [`docs/img/mascot/welcome.png`](docs/img/mascot/welcome.png) | Chapter- and lab-opening pose. |
| [`docs/img/mascot/thinking.png`](docs/img/mascot/thinking.png) | Key-concept / predict pose. |
| [`docs/img/mascot/tip.png`](docs/img/mascot/tip.png) | Hint / helpful-guidance pose. |
| [`docs/img/mascot/warning.png`](docs/img/mascot/warning.png) | Common-mistake / pitfall pose. |
| [`docs/img/mascot/encouraging.png`](docs/img/mascot/encouraging.png) | Difficult-content / "stuck?" pose. |
| [`docs/img/mascot/celebration.png`](docs/img/mascot/celebration.png) | End-of-chapter / achievement pose. |
| [`docs/css/mascot.css`](docs/css/mascot.css) | Custom admonition styles for the seven pose contexts. |
| [`docs/learning-graph/mascot-test.md`](docs/learning-graph/mascot-test.md) | Rendering test page that exercises every admonition style. |
| [`scripts/generate-mascot.py`](scripts/generate-mascot.py) | Source of the artwork — regenerates all seven poses as SVG. |

### Character Overview

- **Name**: Cody
- **Species**: Turtle
- **Personality**: patient, curious, encouraging, playful
- **Catchphrase**: "One step at a time!"
- **Visual**: chunky leaf-green turtle with a CoderDojo-purple shell, teal-rimmed
  shell plates, a cream belly, big sparkly eyes and blush cheeks, holding a teal
  marker pen

Cody is **gender-neutral**. Refer to Cody by name or as *they/them* — never
*he* or *she*.

Cody is also a character *inside* the course: the first lab introduces "Cody our
CoderDojo turtle" as the sprite the student commands. The mascot and the sprite
are the same turtle, so it is fine for Cody to talk about their own drawing.

### Voice Characteristics

- Short sentences, grade 3–5 vocabulary, one idea per sentence
- **Never** calls a task "easy", "simple", or "obvious" — a student who finds it
  hard should never be made to feel they are the problem
- Prefers *try* over *know*: "let's try it and see", not "you should know this"
- Talks about the program, never about the student's ability
- Treats being stuck as normal and expected
- Signature phrases: "One step at a time!", "What do you think will happen?",
  "Let's try it and see!"

### Mascot Admonition Format

Always place the mascot image in the admonition body, never in the title bar:

    !!! mascot-welcome "Title Here"
        ![Cody waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
        Admonition text goes here after the image.

The path is relative to the **rendered page URL**. Pages at
`docs/chapters/<slug>/index.md` and `docs/labs/<slug>/index.md` both render one
directory deep inside one directory, so both use `../../img/mascot/`.

### Placement Rules

| Context | Admonition Type | Frequency |
|---------|----------------|-----------|
| General note / forward link | `mascot-neutral` | As needed |
| Chapter or lab opening | `mascot-welcome` | Exactly one |
| Key concept / predict question | `mascot-thinking` | 2–3 per chapter |
| Helpful hint | `mascot-tip` | As needed |
| Common mistake | `mascot-warning` | As needed |
| Difficult step / "Stuck?" | `mascot-encourage` | Where students may struggle |
| Chapter or lab complete | `mascot-celebration` | Exactly one, at the end |

### Do's and Don'ts

**Do:**

- Use Cody to introduce a new topic warmly
- Include the catchphrase in welcome admonitions
- Keep each admonition to 1–3 sentences
- Match the pose to the content type
- Make the body text specific to *this* chapter, not generic filler

**Don't:**

- Use Cody more than five or six times in a chapter
- Put two mascot admonitions back to back
- Use the mascot for decoration with nothing to say
- Change Cody's personality, voice, or appearance
- Use Cody in instructor-facing pages

### Checking Your Work

After adding mascot admonitions, build the site and confirm the images resolve:

```bash
mkdocs serve
```

Then compare against the [Mascot Style Guide](docs/learning-graph/mascot-test.md).
