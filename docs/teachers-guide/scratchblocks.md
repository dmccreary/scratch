# Scratchblocks: Our Notation for Discussing Code

**Scratchblocks is the preferred notation whenever we write about Scratch code
instead of showing it.** Use it in lesson plans, in issues and pull requests, in
email to other mentors, in chat, and in any part of this site where a script needs
to be discussed rather than screenshotted.

Here is a complete script written in scratchblocks. This is the actual program in
[CoderDojo-Turtle-Square.sb3](../examples/CoderDojo-Turtle-Square.sb3):

```scratch
when green flag clicked
erase all
set pen size to (5)
set pen color to [#005dff]
pen down
repeat (4)
  move (100) steps
  turn cw (90) degrees
  wait (1) seconds
end
```

## Why We Prefer It Over Screenshots

A screenshot of blocks is an image. That has real costs that add up across a site
like this one:

- **It cannot be searched.** A student searching this site for "pen down" will never
  find it inside a PNG.
- **It cannot be corrected.** Changing one number in a screenshot means reopening
  Scratch, rebuilding the script, recapturing, cropping, and recommitting a binary
  file. Changing a number in scratchblocks is typing one character.
- **It cannot be diffed.** Git shows "image changed" and nothing more. Scratchblocks
  shows exactly which block moved.
- **It cannot be copied.** A mentor answering a question in chat can paste
  scratchblocks text into their reply. They cannot paste half a screenshot.
- **It is not accessible.** A screen reader reads nothing from a picture of blocks.

Screenshots are still the right choice when the *user interface* is the subject --
where the "Add Extension" button is, what the palette looks like, what the drawing
output should be. Our intro labs use screenshots correctly for that. Use
scratchblocks when the *code* is the subject.

## The Syntax

Scratchblocks reads almost exactly like the blocks look. The only thing to learn is
which bracket means which kind of input slot:

| You write | You get | Example |
|-----------|---------|---------|
| `(10)` | a round number or reporter slot | `move (10) steps` |
| `[Hello]` | a text slot | `say [Hello!]` |
| `[apple v]` | a dropdown, note the `v` | `set [score v] to (0)` |
| `<...>` | a hexagonal boolean slot | `if <(score) > (5)> then` |
| `[#005dff]` | a color swatch | `set pen color to [#005dff]` |
| `end` | closes a C-block | closes `repeat`, `if`, `forever` |
| `// text` | a block comment | `move (10) steps // one side` |

Reporters nest by putting one inside another's parentheses:

```scratch
move ((distance) * (2)) steps
turn cw ((360) / (sides)) degrees
```

Custom blocks use `define`, and the parameters are written as slots right in the
name:

```scratch
define square (size)
repeat (4)
  move (size) steps
  turn cw (90) degrees
end
```

That definition is then called like any other block:

```scratch
when green flag clicked
erase all
pen down
square (50)
square (100)
square (150)
```

A blank line separates one script from another.

## Where the Notation Comes From

Scratchblocks is the community standard, not something local to us. It is used:

- On the [Scratch Wiki](https://en.scratch-wiki.info/), inside
  `<scratchblocks>...</scratchblocks>` tags
- On the Scratch discussion forums, inside `[scratchblocks]...[/scratchblocks]` tags
- In many Scratch books and course materials

The renderer is an open source JavaScript library,
[scratchblocks](https://github.com/scratchblocks/scratchblocks), originally written
by Tim Radvan. It turns the text above into the real, colored Scratch block graphics
in a browser. There is a live editor at
[scratchblocks.github.io](https://scratchblocks.github.io/) where you can paste text
and see the rendered blocks immediately -- that is the fastest way to check your
syntax, and a good thing to show a curious student.

On this site we write scratchblocks inside a fenced code block tagged `scratch`.
Until the renderer is wired into the theme, those fences display as plain monospaced
text, which is still readable, searchable, and copyable. When the renderer is added,
every one of those fences becomes real Scratch blocks with no edits to the pages.

## What It Does Not Cover

Scratchblocks describes **scripts**, not **projects**. It has no way to represent
sprites, costumes, sounds, backdrops, the stage, or the starting values of variables.

So the two notations do different jobs, and you want both:

- **Scratchblocks** when you are discussing code -- a lesson plan, an answer to a
  question, a bug in a script.
- **A `.sb3` file** when a student needs to actually run the project. That file is a
  ZIP archive holding a JSON description of everything, which is covered in
  [Inside the .sb3 File](sb3-file-format.md).
