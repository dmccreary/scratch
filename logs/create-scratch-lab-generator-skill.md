# Session Log: create scratch-lab-generator skill

**Date:** 2026-09-08
**Textbook:** Learning Computational Thinking with Scratch
**Deliverable:** `skills/scratch-lab-generator/` (17 files) plus the first
generated lab, `docs/labs/draw-a-square/`

## Goal

Build a skill that turns a one-line verbal description of a challenge and its
solution into a complete Scratch lab: a mascot-narrated lesson page, before and
after block diagrams, and the Scratch programs that implement them.

## Steps Executed

- **Step 1 (Survey existing conventions).** Read `mkdocs.yml`, `docs/labs.md`,
  `docs/intro/03-first-square.md`, and the chapter stubs. Found the mascot
  convention already defined by the `book-installer` skill's
  `references/learning-mascot.md` — seven poses (`neutral`, `welcome`,
  `thinking`, `tip`, `warning`, `encouraging`, `celebration`), images floated
  into the admonition *body* via `attr_list`, never the title bar. The new skill
  matches that convention exactly rather than inventing a second one.

- **Step 2 (Ground the Scratch file format in real data).** Rather than writing
  `project.json` from memory, fetched the actual project behind the curriculum's
  existing link — [Cody the Turtle Draws a Square](https://scratch.mit.edu/projects/400053670/)
  — via the Scratch project-token API, and used its block graph as the reference
  for opcodes, input shadow types, and `next`/`parent` linkage. Downloaded its
  two SVG assets (the CoderDojo turtle costume and the blank backdrop) and
  bundled them into the skill so every generated `.sb3` ships the real Cody
  sprite and is fully self-contained.

- **Step 3 (Write the compiler).** `scripts/make_sb3.py` compiles scratchblocks
  text into a valid Scratch 3 project: 69 blocks across 8 palettes plus 13
  aliases, C-block nesting, nested reporters, boolean expressions, dropdown menu
  shadow blocks, broadcasts, auto-created variables, and custom blocks with
  `%s`/`%b` parameters. An unrecognized line is a hard error naming the closest
  known block, never a silent guess.

- **Step 4 (Write the verification gate).** `scripts/check_lab.py` compiles every
  `.txt` in a lab directory, validates each project against the official Scratch
  3 JSON schema (bundled offline in `assets/`), and checks the page: required
  sections, mascot images that exist on disk, download links that resolve, and
  block diagrams that still match their `.txt` source. `--fix` re-syncs a drifted
  diagram while preserving the indentation that keeps it inside a `???` block.

- **Step 5 (Write the templates).** `assets/templates/` gained the lab page
  template, `mascot.css` (seven pose admonitions in the CoderDojo palette),
  `scratchblocks.css`, and `scratchblocks-init.js` — the last re-rendering on
  MkDocs Material's instant navigation, which swaps page content without a
  reload.

- **Step 6 (Write the references).** `references/setup.md` (one-time project
  wiring), `references/lab-structure.md` (page anatomy, pose vocabulary, Cody's
  voice rules), and `references/scratchblocks-syntax.md` — the last **generated**
  from the compiler's own tables by `scripts/gen_syntax_ref.py`, so the docs can
  never claim a block that does not compile.

- **Step 7 (Test).** `scripts/test_make_sb3.py`, 52 assertions across 12 groups.

- **Step 8 (Generate the first lab).** Ran the skill against backlog item #1 in
  `docs/labs.md` ("Sprite Movement Commands") to produce
  `docs/labs/draw-a-square/`.

## Verification

Correctness was checked at four independent levels, because a `.sb3` that fails
to open in Scratch is worse for a student than no download at all:

| Level | Method | Result |
|-------|--------|--------|
| Structural | Block graph compared against the real project 400053670 | Opcodes, shadow types and linkage match |
| Schema | Official `sb3_schema.json` from `scratch-parser` | All projects valid |
| Load | `scratch-parser` in Node — the same library scratch.mit.edu uses to validate uploads | All projects load |
| Render | Built the site, served it, drove a real browser | Both diagrams render as SVG; all seven mascot admonitions style and float correctly; the nested solution diagram survives the collapsed block |

The `.sb3` files were additionally re-downloaded over HTTP from the built site
and re-parsed, to confirm nothing is corrupted in transit.

## Bugs Found and Fixed During the Session

1. **Custom-block parameters leaked into `variables`.** Body blocks are emitted
   before the `define` hat, so the parameter scope was still empty when they
   compiled and `(size)` became a variable reporter instead of an argument
   reporter. Fixed by pre-scanning the script's `define` header
   (`Builder.scope_for`) before emitting the stack.
2. **The `define` hat was not linked to its body.** `emit_define` discarded the
   `next` id, leaving the definition detached from the blocks under it.
3. **`>` as a comparison operator was miscounted as a bracket close.** This broke
   every `repeat until <(x position) > (200)>`. Fixed by adopting Scratch's own
   spacing convention: `<` followed by a space is the less-than operator, `>`
   preceded by a space is greater-than; otherwise they delimit a boolean.
4. **`--fix` stripped indentation** when re-syncing a diagram nested inside a
   `???` block, which would have broken the solution reveal. The fix now
   captures and re-applies the leading indent.
5. **A trailing `?` tokenized as a separate word**, so `touching [edge v]?` did
   not match its block signature. Signatures now normalize `% ?` to `%?`.

## Repository Changes Made Along the Way

- **`mkdocs.yml` declared `markdown_extensions` twice.** The second declaration
  silently won, which meant `admonition`, `footnotes` and `toc` were not active
  for the whole book. Collapsed into one list and added `attr_list`,
  `md_in_html`, `pymdownx.details` and `pymdownx.superfences`.
- **`docs/labs.md` and `docs/labs/index.md` both render to `/labs/`** — a direct
  URL collision. Moved the backlog page into `docs/labs/index.md` with `git mv`
  so history follows, added a "Labs Ready to Run" table above the existing prose,
  and re-headed the remainder "Planned Labs". Nav gained a **Labs** section and
  the now-duplicate "Summary of Labs" entry under Intro was removed.

## The First Lab: Draw a Square

Generated from backlog item #1. Decisions taken and stated per the skill's own
workflow:

- **Owning chapter:** 4. Motion & Coordinates. Concepts: *When Green Flag
  Clicked*, *Sequencing*, *Script*, *Move Steps Block*, *Turn Right Block*,
  *Degrees Of Turn*.
- **Starter is incomplete, not broken.** For a student's first lab, building the
  pattern teaches more than debugging one. The starter draws one side and one
  corner; the student adds the remaining three groups — exactly step 6 of the
  backlog entry.
- **Pen blocks are given, not taught.** The backlog frames this lab as pure
  movement, but without a visible line the "Check Your Work" section has nothing
  observable. The pen blocks are pre-placed so the square can be seen, leaving
  lab 2 ("Drawing with the Pen") its own job. The program is otherwise identical
  to the existing project 400053670, `wait` blocks included — which sets up the
  loops lab, since twelve blocks collapse to three.

Starter: 7 blocks. Solution: 16 blocks. Both validate and load.

## Mascot Images

The seven poses did not exist in the repository when the skill was written, and
image generation is outside what this session could do. The lab was authored
against the seven canonical filenames, and the layout was verified using
temporary stand-ins which were then deleted, so no placeholder artwork was ever
committed. `check_lab.py` correctly reported all seven as errors.

**Dan regenerated the mascot images afterwards using a high-quality image
generator**, along with `character-sheet.md` and `image-prompts.md`, and
standardized stylesheets on `docs/css/` (the skill's `references/setup.md` was
updated to match). With the real poses in place the lab now passes the gate with
**0 errors, 0 warnings**.

## Results Summary

- Skill files: 17 (`SKILL.md`, `TODO.md`, 3 references, 4 scripts, 8 assets)
- Python: 1,452 lines across `make_sb3.py`, `check_lab.py`, `gen_syntax_ref.py`
  and `test_make_sb3.py`
- Blocks supported: 69, plus 13 aliases, across Events, Motion, Pen, Control,
  Looks, Variables, Operators and Sensing
- Tests: 52 assertions in 12 groups, all passing
- Labs generated: 1 (`docs/labs/draw-a-square/`), gate clean

## Design Note

The `.txt` block source is the single source of truth. The diagram rendered on
the page and the downloadable `.sb3` are both derived from it, and `check_lab.py`
fails the build if they diverge. This is the property that makes the skill worth
having: a lab cannot ship a picture that disagrees with the program a student
downloads.

## Follow-ups

See [`skills/scratch-lab-generator/TODO.md`](../skills/scratch-lab-generator/TODO.md).
The headline item is **rendering the turtle drawing beside the block code** —
the compiler already produces an ordered block tree, so a small pen/motion
interpreter could emit the resulting figure as SVG from the same `.txt`, making
the starter's broken output visible as the hook and turning "Check Your Work"
into a picture instead of a description.
