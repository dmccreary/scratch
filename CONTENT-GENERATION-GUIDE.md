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

## Scratch Blocks: Always Render, Never Screenshot

Scratchblocks is a human-readable text notation for a Scratch program. This
book renders it live: `docs/js/scratchblocks-init.js` (loaded from
`mkdocs.yml`) turns the notation into real Scratch 3 block art in the browser,
styled by `docs/css/scratchblocks.css`.

### When to use it

**Use scratchblocks for every block stack, every block, and every code snippet
you show a student.** A rendered diagram is one block of text a future editor
can fix in seconds; a screenshot of the same blocks is a binary file that goes
stale the moment the program changes, cannot be searched, cannot be translated,
and cannot be read by a screen reader.

Only use a PNG when the thing on screen is **not blocks**: the Scratch editor
interface (menus, the extension picker, the block palette), the drawing a
program produces on the stage, or a photograph. If you are about to generate or
capture an image of blocks, stop and write scratchblocks instead.

### How to use it — block stacks

Wrap the notation in an HTML `<pre>` tag whose class is `blocks`, with a blank
line before and after it:

```html
<pre class="blocks">
when green flag clicked
erase all
set pen size to (5)
pen down
move (100) steps
wait (1) seconds
turn right (90) degrees
</pre>
```

That renders as:

<pre class="blocks">
when green flag clicked
erase all
set pen size to (5)
pen down
move (100) steps
wait (1) seconds
turn right (90) degrees
</pre>

Three rules that are easy to get wrong:

1. **Escape angle brackets** as `&lt;` and `&gt;` inside the `<pre>`, or the
   browser's HTML parser eats a boolean like `<(x) > (50)>`.
2. **Indent the whole `<pre>` block by four spaces** when it sits inside an
   admonition (`!!! note`) or a collapsible (`??? note`). Lose the indent and
   the block falls out of the box.
3. **Markdown is not processed inside the `<pre>`** — no links, no bold, no
   mascot images. Put those in the paragraph above it.

### How to use it — inline blocks

To name a single block in the middle of a sentence, use inline code with the
`.b` class (`attr_list` is enabled, so the class reaches the renderer):

```markdown
Drag the `move (10) steps`{.b} block under the green flag.
```

Which reads as: Drag the `move (10) steps`{.b} block under the green flag.

Use this whenever you would otherwise write a block name in plain backticks or
paste a one-block screenshot.

### Notation syntax

The full text syntax — operand brackets, C-blocks and `end`, custom blocks,
comments — is documented in
[`skills/scratch-lab-generator/references/scratchblocks-syntax.md`](skills/scratch-lab-generator/references/scratchblocks-syntax.md).

Two different limits apply, and it matters which one you are under:

- **Rendering on a page** accepts any valid scratchblocks notation.
- **Compiling to a downloadable `.sb3`** (labs only) accepts only the blocks in
  the generated table in that reference. An unlisted block is a hard error, not
  a silent guess.

### Checking your work

Build the site and confirm each diagram drew as blocks rather than plain text:

```bash
mkdocs serve
```

For a full lab, `skills/scratch-lab-generator` generates the page, the diagram,
and the `.sb3` files from one source file, and
`python3 skills/scratch-lab-generator/scripts/check_lab.py docs/labs/<slug>`
verifies that they still agree.

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
