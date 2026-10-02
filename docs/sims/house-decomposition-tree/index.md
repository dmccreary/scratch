---
title: Decomposing a House Drawing
description: A clickable tree that breaks the job "draw a house" into smaller and smaller pieces until every piece is a single Scratch block.
image: /sims/house-decomposition-tree/house-decomposition-tree.png
og:image: /sims/house-decomposition-tree/house-decomposition-tree.png
twitter:image: /sims/house-decomposition-tree/house-decomposition-tree.png
social:
   cards: false
quality_score: 100
---

# Decomposing a House Drawing

<iframe src="main.html" height="602px" width="100%" scrolling="no"></iframe>

[Run the Decomposing a House Drawing MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

**Decomposition** means breaking a big job into smaller jobs, and breaking
those into even smaller ones, until every piece is small enough to hand to a
computer. This MicroSim shows that for one job: *draw a house*.

The tree has four **levels**. The top level is the whole job. Each level below
it is more detailed and less fuzzy than the one above:

- **Purple** is the whole job.
- **Blue** and **orange** boxes are still too big to program.
- **Green** boxes, marked with a check, are small enough to be one Scratch block.

The change from orange to green is the message of the whole diagram: green
means "small enough to program."

## How to Use

1. Rest the mouse on any box. A small tip answers the question "Small enough
   to program?" with **Yes** or **Not yet**.
2. Click a box. The panel at the bottom gives the answer and the reason.
3. Look at the thick dark line. It shows the path from the box you clicked
   back up to "Draw a house," so you can see which big job the small step
   belongs to. The other boxes fade.
4. Click the empty background to clear the highlight.

Try to predict the answer before you click. Then check.

The boxes cannot be dragged and the picture cannot be zoomed, so the layout
always stays the same.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/scratch/sims/house-decomposition-tree/main.html"
        height="602px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Grade Level
Grades 3-5 (elementary), beginning computational thinking with Scratch

### Duration
10-15 minutes

### Learning Objective
Given a drawing task, the student can identify which parts of the task are
still too big to program and which parts are small enough to become a single
instruction. (Bloom's Taxonomy: Analyze)

### Prerequisites
- The idea that a program is a list of steps done in order
- The worked example "Drawing a House" in Chapter 1

### Activities

1. **Predict** (3 min): Before clicking anything, students point to each box
   and say "Yes" or "Not yet." They click to check.
2. **Trace a Path** (5 min): Students click "Move forward 100 steps" under the
   walls and read the path line out loud, from the top job down to the block.
   They repeat for one green box under the roof.
3. **Spot the Difference** (3 min): Students compare the two "Turn right"
   boxes. Why is one 90 degrees and the other 120 degrees? (A square has four
   corners and a triangle has three, and the turns always add up to one full
   circle of 360 degrees.)
4. **Your Turn** (5 min): On paper, students draw their own tree for a new job,
   such as "draw a kite" or "draw a robot face," and color the boxes that are
   small enough to be one block.

### Assessment
- Can the student say why "Draw one side" is not yet small enough?
- Can the student name all the single-block steps needed for the walls?
- Given a new drawing job, can the student keep cutting until every piece is
  one instruction?

## References

1. [Decomposition (computer science)](https://en.wikipedia.org/wiki/Decomposition_(computer_science)) - Wikipedia - Breaking a complex problem into parts that are easier to understand and program.
2. [Turtle graphics](https://en.wikipedia.org/wiki/Turtle_graphics) - Wikipedia - The move-and-turn drawing style used for the house, including why the turns of a closed shape add up to 360 degrees.
3. [Scratch](https://scratch.mit.edu/) - MIT Media Lab / Scratch Foundation - The block-based programming language used throughout this book.
4. [vis-network Documentation](https://visjs.github.io/vis-network/docs/network/) - vis.js - Documentation for the JavaScript library used to draw this tree.
