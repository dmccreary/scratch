# scratch-lab-generator TODO

## 1. Render the turtle drawing beside the block code

**Idea.** Every turtle-graphics lab shows the blocks but not what they draw. A
student reading `starter.txt` has to run the program to find out that Cody stops
after one side. Put the resulting drawing next to the diagram and the difference
between starter and solution becomes visible at a glance:

```
┌─────────────────┐   ┌──────────────┐
│  block diagram  │   │  what it     │
│  (scratchblocks)│   │  draws       │
└─────────────────┘   └──────────────┘
```

**Why it is worth doing.** It is the single highest-value addition left. It
strengthens three parts of the lab at once:

- *Cody's Challenge* — show the broken output as the hook, so the problem is
  visible before a word of explanation.
- *Predict Before You Run* — the student predicts, then checks against the
  picture without leaving the page.
- *Check Your Work* — "your square should look like this" beats a prose
  description of a square.

It also makes the **Go Further** experiments self-checking: change 90 to 120 and
the page can show what a triangle looks like.

**Approach.** The compiler already builds a complete, ordered block tree, so a
small interpreter can walk it and emit SVG directly — no browser, no Scratch VM.
A new `scripts/render_drawing.py` would:

1. Reuse `make_sb3.parse_scripts()` to get the tree (single source of truth
   preserved — the drawing comes from the same `.txt` as the diagram and the
   `.sb3`).
2. Walk the script from the green-flag hat, tracking `(x, y, heading, pen_down,
   pen_size, pen_color)` on Scratch's stage geometry — 480×360, origin at
   centre, heading 90 = right, `turn right` increases heading clockwise.
3. Emit an SVG `<path>` per pen-down stroke, sized to the stage, and write
   `starter-drawing.svg` / `solution-drawing.svg` into the lab directory.
4. `check_lab.py` regenerates and diffs it like it already does for `.sb3`, so
   the picture cannot drift from the blocks.

The lab template would gain a `.lab-compare` flex row (the CSS is already in
`assets/templates/scratchblocks.css`) holding the diagram and the drawing.

**Open questions.**

- **Loops with variables.** `repeat (sides)` where `sides` is set at runtime
  needs constant folding or a tiny evaluator. Start by supporting literal
  operands and simple arithmetic on already-assigned variables; refuse anything
  else with a clear error rather than drawing something wrong. A lab whose
  picture disagrees with its code is worse than no picture.
- **Non-terminating programs.** `forever` and `repeat until` need a step budget
  and a documented cap.
- **Partial drawings.** A starter that draws one side should render exactly that
  — the incomplete figure is the point, so no auto-closing of paths.
- **Pen colour changes** mid-drawing mean one `<path>` per colour run.
- **Where it does not apply.** Labs with no pen blocks (events, looks, sensing)
  should skip the drawing rather than emit an empty stage.

**Scope guard.** This is an interpreter for the pen/motion subset only. If it
starts growing sensing, cloning, or sprite interaction, stop — that is a job for
the real VM, not for a lab illustration.

## 2. Smaller follow-ups

- **Inline block spans in the "Blocks Used" table.** The renderer already
  handles `code.b` inline; `` `move (10) steps`{.b} `` would show real block
  shapes in the table. Deferred on the first lab to keep the table narrow — try
  it and check the column widths on mobile.
- **Stage-position control per lab.** `make_sb3.py` places the sprite at
  `(0, 0)` at size 20. A lab drawing a large figure may want a different start
  so the drawing stays on stage. Currently only reachable via CLI flags, not
  from `check_lab.py`.
- **A `scratchblocks` fenced-code alias.** Authors currently write raw
  `<pre class="blocks">`. A ```` ```scratch ```` fence would be friendlier, but
  needs a superfences custom format so codehilite does not mangle it.
