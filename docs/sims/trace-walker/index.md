---
title: Step-by-Step Trace Walker
description: Run a short list of turtle instructions one line at a time and predict whether each line changes the position or the heading.
image: /sims/trace-walker/trace-walker.png
og:image: /sims/trace-walker/trace-walker.png
twitter:image: /sims/trace-walker/trace-walker.png
social:
   cards: false
quality_score: 100
---

# Step-by-Step Trace Walker

<iframe src="main.html" height="522px" width="100%" scrolling="no"></iframe>

[Run the Step-by-Step Trace Walker MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

**Tracing** means following an algorithm one line at a time and keeping track
of what has changed after each line. To trace the turtle you only need to know
two things about it:

- its **position**: where it is on the stage
- its **heading**: which way its nose is pointing

Moving changes the position. Turning changes the heading. Nothing else does.

This MicroSim never runs the whole program at once. You press **Next step**
and exactly one line runs. That is the whole point: computers run one
instruction at a time, so to understand a computer you have to think one
instruction at a time.

## How to Use

1. Look at the highlighted line in the **Instructions** list. That is the line
   about to run.
2. Press **Next step**. With **Predict** turned on, the sim asks a question
   first. Choose **Position changes** or **Heading changes**.
3. Watch the turtle. The line it draws is its trail.
4. Read the readout above the grid. The part that just changed is highlighted,
   and the finished line in the list is labeled *position* or *heading*.
5. Keep going until the banner says "Done." Then press **Reset** to trace it
   again.
6. Use the **Program** menu to switch from "Two sides of a square" to "A whole
   square."

Turn **Predict** off if you only want to step through and watch.

The grid is the same as the Scratch stage: x goes from -240 to 240 and y goes
from -180 to 180, with (0, 0) in the middle.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/scratch/sims/trace-walker/main.html"
        height="522px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Grade Level
Grades 3-5 (elementary), beginning computational thinking with Scratch

### Duration
10-15 minutes

### Learning Objective
Given a short list of motion instructions and a starting position and heading,
the student can predict the turtle's position and heading after each
instruction. (Bloom's Taxonomy: Analyze)

### Prerequisites
- The worked example "Tracing Four Instructions" in Chapter 1
- Knowing that the middle of the stage is position (0, 0)

### Activities

1. **Trace on Paper First** (5 min): Students copy the trace table from the
   chapter with the Position and Heading columns left blank. They fill in each
   row *before* pressing Next step, then check it against the readout.
2. **Predict Mode** (5 min): With Predict on, students run "Two sides of a
   square." After each answer they say the rule out loud: "moving changes
   position, turning changes heading."
3. **Find the Pattern** (3 min): Students read down the labels in the
   instruction list: position, heading, position, heading. Ask: "What pattern do
   you see? How many times would it repeat for a whole square?"
4. **A Whole Square** (5 min): Students switch programs and predict where the
   turtle will end up and which way it will face before running all eight lines.

### Assessment
- Can the student give the position and heading after any line without running
  it?
- Can the student explain why the turtle faces left after "Two sides of a
  square"?
- Can the student explain why the turtle ends "A whole square" where it started
  and facing the way it started?

## References

1. [Turtle graphics](https://en.wikipedia.org/wiki/Turtle_graphics) - Wikipedia - The position-and-heading model of drawing that this MicroSim traces.
2. [Tracing (software)](https://en.wikipedia.org/wiki/Tracing_(software)) - Wikipedia - Background on following a program's execution step by step.
3. [Scratch](https://scratch.mit.edu/) - MIT Media Lab / Scratch Foundation - The block-based language whose stage coordinates this grid copies.
4. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the JavaScript library used to draw this MicroSim.
