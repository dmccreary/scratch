---
name: scratch-lab-generator
description: Generates a complete Scratch lab from a one-line verbal description of a challenge and its solution. Produces the lab page with mascot-narrated challenge, before/after block diagrams, and real downloadable .sb3 programs in docs/labs/<slug>/. Use when adding a hands-on Scratch lab or turning an entry in docs/labs.md into a full lesson.
model: sonnet
license: MIT
---

# Scratch Lab Generator

Turn a sentence into a finished lab.

> "A lab where students fix a square-drawing program that's missing its turn
> block — the solution uses repeat 4 with move and turn 90."

becomes `docs/labs/draw-a-square/` containing a complete lesson page, two block
diagrams, and two `.sb3` files a student can open in Scratch.

## What gets generated

```
docs/labs/<lab-slug>/
├── index.md        the complete lab: challenge, task, hints, solution
├── starter.txt     scratchblocks source for the "before" program
├── starter.sb3     compiled Scratch project (loadable, schema-validated)
├── solution.txt    scratchblocks source for the "after" program
└── solution.sb3    compiled Scratch project
```

The `.txt` files are the single source of truth. The diagram on the page and
the downloadable project are both derived from them, so they cannot drift.

## Before generating anything

Run the checks in [`references/setup.md`](references/setup.md). The renderer,
the mascot CSS, the `mkdocs.yml` extensions, and the seven mascot poses must be
in place or every generated lab will render wrong in the same way. This is a
one-time cost per project — skip it once it is done.

## Workflow

### 1. Pin down the challenge and the solution

The user's description gives you a challenge and a solution. Before writing
anything, settle these and state them back in one line each:

- **The concept.** One idea per lab. Look it up in
  `docs/learning-graph/concept-list.md` and name the owning chapter from
  `mkdocs.yml`. A lab that teaches two concepts is two labs.
- **The starter state.** Incomplete, broken, or absent — see
  [`references/lab-structure.md`](references/lab-structure.md). The starter must
  be *one idea away* from the solution.
- **The slug.** Short, hyphenated, verb-first: `draw-a-square`,
  `fix-the-hexagon`, `color-every-other-side`.

If the description does not say whether the starter is broken or merely
incomplete, choose: a broken starter teaches debugging, an incomplete one
teaches construction. Say which you picked and why, then keep going — do not
stop to ask.

### 2. Write the block programs first

Write `solution.txt`, then derive `starter.txt` from it by removing or breaking
exactly one thing. Use the syntax and block vocabulary in
[`references/scratchblocks-syntax.md`](references/scratchblocks-syntax.md) —
that table is generated from the compiler, so a block listed there compiles and
a block missing from it does not.

Keep programs small. A lab that fits on one screen is a lab a student finishes.

Compile and check as you go:

```bash
python3 skills/scratch-lab-generator/scripts/make_sb3.py docs/labs/<slug>/solution.txt
```

An unknown block is a hard error with a suggestion, not a silent guess. If a
lab genuinely needs a block that is not in the table, add it to the `BLOCKS`
dict in `scripts/make_sb3.py` — opcode, slot descriptors, and shape — then:

```bash
python3 skills/scratch-lab-generator/scripts/test_make_sb3.py
python3 skills/scratch-lab-generator/scripts/gen_syntax_ref.py
```

The test suite must stay green; the reference table is generated from the
compiler and must never be hand-edited.

### 3. Write index.md

Start from `assets/templates/lab-index-template.md` and fill every placeholder.
[`references/lab-structure.md`](references/lab-structure.md) gives the section
order, the mascot pose for each slot, and Cody's voice rules.

Three things that are easy to get wrong:

- **Mascot paths are `../../img/mascot/<pose>.png`** — relative to the rendered
  URL `labs/<slug>/`, not to the source file.
- **Escape `<` and `>` as `&lt;` and `&gt;`** inside `<pre class="blocks">`, or
  the browser's HTML parser will eat a boolean like `<(x) > (50)>`.
- **Keep the four-space indent** on a diagram nested inside a `???` block. Lose
  it and the solution reveal breaks apart.

The solution goes inside a collapsed `???` block. Never put it inline.

### 4. Verify

```bash
python3 skills/scratch-lab-generator/scripts/check_lab.py docs/labs/<slug>
```

This compiles every `.txt` into a `.sb3`, validates each one against the
official Scratch 3 schema bundled in `assets/`, and checks the page: required
sections, mascot images that exist on disk, download links that resolve, and
diagrams that still match their source. Add `--fix` to re-sync a diagram from
its `.txt` after editing the blocks.

**The lab is not done until this exits clean.** A `.sb3` that fails to open in
Scratch is worse for a student than no download at all.

Then build the site and look at the page:

```bash
mkdocs build --strict
```

### 5. Wire it in

- Add a row to `docs/labs/index.md`.
- Add the page to the `Labs` section of `mkdocs.yml` nav, in dependency order.
- If the lab came from the backlog in `docs/labs.md`, leave that file alone —
  it is the plan, not the index.

## Scope rules

- **One lab per invocation.** If asked for a series, generate them one at a
  time and verify each before starting the next.
- **Do not invent mascot poses.** Seven exist; use those.
- **Do not hand-edit a `.sb3`.** Change the `.txt` and recompile.
- **Do not link to scratch.mit.edu project IDs you have not been given.** A
  guessed project ID is a broken lab.

## Reference files

| File | What it holds |
|------|---------------|
| [`references/setup.md`](references/setup.md) | One-time project wiring: CSS, JS, `mkdocs.yml`, mascot poses |
| [`references/lab-structure.md`](references/lab-structure.md) | Page anatomy, mascot pose vocabulary, Cody's voice |
| [`references/scratchblocks-syntax.md`](references/scratchblocks-syntax.md) | Block source syntax and the full supported-block table |
| `scripts/make_sb3.py` | Compiles scratchblocks text into a real `.sb3` |
| `scripts/check_lab.py` | Builds and verifies a whole lab directory |
| `scripts/test_make_sb3.py` | Compiler regression tests — run after touching `make_sb3.py` |
| `scripts/gen_syntax_ref.py` | Regenerates the supported-block reference from the compiler |
| `assets/templates/` | Lab page template, mascot CSS, block renderer CSS/JS |
| `assets/costumes/` | The CoderDojo turtle sprite and blank backdrop embedded in every `.sb3` |
| `assets/sb3_schema.json` | Official Scratch 3 project schema, bundled for offline validation |
