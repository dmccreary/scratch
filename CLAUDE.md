# CLAUDE.md

Project guidance for **Learning Computational Thinking with Scratch** — an
MkDocs Material intelligent textbook for elementary students (grades 3–5).

## Content generation

Before generating content for chapters, labs, lesson plans, quizzes, the FAQ, or
any other student-facing text, read
[`CONTENT-GENERATION-GUIDE.md`](CONTENT-GENERATION-GUIDE.md). It defines the
audience, the voice rules, and how to use the learning mascot.

The teacher's guide, instructor's guide, and other instructor-facing content do
**not** use the mascots described in `CONTENT-GENERATION-GUIDE.md`.

## Learning mascot

The mascot is **Cody the Turtle** — gender-neutral, referred to by name
or as *they/them*. The source of truth for Cody's appearance and voice is
[`docs/img/mascot/character-sheet.md`](docs/img/mascot/character-sheet.md).

The seven pose images are generated from code, not hand-drawn or AI-generated:

```bash
python3 scripts/generate-mascot.py /tmp/cody-svg
```

See the character sheet for the full rasterisation and cropping steps. Do not
edit the PNGs directly — change `scripts/generate-mascot.py` and regenerate, and
update the character sheet in the same commit.

## Building

```bash
mkdocs serve
```

The site is published with `mkdocs gh-deploy --force`.
