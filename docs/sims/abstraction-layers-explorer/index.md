---
title: Abstraction Layers Explorer
description: Slide the detail level to open up one named block and see the hidden steps underneath, then hide them again.
image: /sims/abstraction-layers-explorer/abstraction-layers-explorer.png
og:image: /sims/abstraction-layers-explorer/abstraction-layers-explorer.png
twitter:image: /sims/abstraction-layers-explorer/abstraction-layers-explorer.png
social:
   cards: false
quality_score: 100
---

# Abstraction Layers Explorer

<iframe src="main.html" height="482px" width="100%" scrolling="no"></iframe>

[Run the Abstraction Layers Explorer MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }
<br/>
[Edit in the p5.js Editor](https://editor.p5js.org/)

## About This MicroSim

**Abstraction** means giving a group of steps one short name, and then using
the name instead of the steps. The important part is that the steps do not go
away. The name only *hides* them.

This MicroSim lets you open up one name and look underneath:

- **What you say** is one purple block: `draw flower`.
- **What that means** is three blue blocks.
- **What the computer does** is eight green blocks.

Each layer has more to remember than the one above it. That is why a good name
is so useful: you only have to hold one thing in your head.

## How to Use

1. Start at **Detail level 1**. You see one name. That is all you have to
   remember.
2. Slide **Detail level** to 2. A new band slides open to show what the name
   was really made of.
3. Slide to 3 to see the steps the computer follows.
4. Turn on **Show step count** to see how many things you would have to
   remember at each layer: 1, then 3, then 8.
5. Slide back to 1. The detail hides again, but it is still there.
6. Press **Reset** to go back to the start.

On a narrow screen the eight green blocks wrap onto two rows.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/scratch/sims/abstraction-layers-explorer/main.html"
        height="482px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Grade Level
Grades 3-5 (elementary), beginning computational thinking with Scratch

### Duration
10-15 minutes

### Learning Objective
The student can explain that naming a group of steps hides detail without
removing it, and can state how many underlying steps a single named block
stands for. (Bloom's Taxonomy: Understand)

### Prerequisites
- Decomposition: a big job is made of smaller jobs
- The "Draw Square" worked example in Chapter 1

### Activities

1. **Predict** (3 min): With the slider at 1, ask: "How many steps do you think
   are hiding inside `draw flower`?" Write the guesses on the board.
2. **Open It Up** (5 min): Students slide to 2 and then 3 with **Show step
   count** turned on. They read each caption out loud.
3. **Hide It Again** (2 min): Students slide back to 1. Ask: "Did the eight
   steps disappear? Where did they go?" (They are still there. The name hides
   them.)
4. **Name Your Own** (5 min): Students pick an everyday job, such as "set the
   table," and write the name on one line and the hidden steps underneath it.

### Teacher Note
The eight green blocks are the steps that draw one square. A real flower
program repeats those steps eight times, so the full list is even longer than
the bottom band shows. That makes a good extension question: "If one square is
eight steps, how many steps is the whole flower?"

### Assessment
- Can the student say in their own words what a name hides?
- Can the student say how many steps one named block stands for at each layer?
- Can the student explain why Student B's short description in the chapter is
  not missing anything?

## References

1. [Abstraction (computer science)](https://en.wikipedia.org/wiki/Abstraction_(computer_science)) - Wikipedia - How naming and hiding detail lets programmers think about bigger things.
2. [Computational thinking](https://en.wikipedia.org/wiki/Computational_thinking) - Wikipedia - Overview of computational thinking, including abstraction.
3. [Scratch](https://scratch.mit.edu/) - MIT Media Lab / Scratch Foundation - The block-based language whose "Make a Block" feature lets students build their own named blocks.
4. [p5.js Reference](https://p5js.org/reference/) - p5.js - Documentation for the JavaScript library used to draw this MicroSim.
