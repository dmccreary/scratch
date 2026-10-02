---
title: Algorithm Design Flowchart
description: A clickable flowchart of the five moves of algorithm design, with each move explained using the square-drawing example.
image: /sims/algorithm-design-flow/algorithm-design-flow.png
og:image: /sims/algorithm-design-flow/algorithm-design-flow.png
twitter:image: /sims/algorithm-design-flow/algorithm-design-flow.png
social:
   cards: false
quality_score: 100
---

# Algorithm Design Flowchart

<iframe src="main.html" height="702px" width="100%" scrolling="no"></iframe>

[Run the Algorithm Design Flowchart MicroSim Fullscreen](./main.html){ .md-button .md-button--primary }

## About This MicroSim

**Algorithm design** is the work of inventing an algorithm, not just following
one. Good algorithm design follows five moves:

1. **Understand the goal.** Say exactly what "done" looks like.
2. **Decompose.** Cut the goal into pieces small enough to be single steps.
3. **Find patterns.** Look for pieces that repeat.
4. **Order the steps.** Decide what has to happen before what.
5. **Check for finishing.** Make sure the steps run out.

This flowchart shows the five moves from top to bottom. Click any box and the
panel under the chart tells you what that move means and what it looked like
when the chapter designed the square-drawing algorithm.

Look at the arrow marked **no**. It goes from the diamond back up to move 2.
That loop is the important part of the chart. When an algorithm does not
finish, you do not start over from nothing. You go back and break the problem
down again.

## How to Use

1. Move the mouse over a box. Its border gets thicker and the pointer changes,
   which tells you the box can be clicked.
2. Click the box. Read the panel below the chart.
3. Click the boxes in order, from 1 to 5, and follow the arrows with your
   finger.
4. Click the diamond. What happens if the answer is "no"?

On a narrow screen the labels in the boxes get shorter so the chart still fits.

## Iframe Embed Code

You can add this MicroSim to any web page by adding this to your HTML:

```html
<iframe src="https://dmccreary.github.io/scratch/sims/algorithm-design-flow/main.html"
        height="702px"
        width="100%"
        scrolling="no"></iframe>
```

## Lesson Plan

### Grade Level
Grades 3-5 (elementary), beginning computational thinking with Scratch

### Duration
10-15 minutes

### Learning Objective
Given a new drawing problem, the student can name the five moves of algorithm
design in order and say what they would do at each move.
(Bloom's Taxonomy: Apply)

### Prerequisites
- The four powers of computational thinking from earlier in Chapter 1
- The worked example "Designing the Square Algorithm"

### Activities

1. **Walk the Chart** (4 min): Students click each box in order and read the
   "For the square" line out loud.
2. **Cover and Recall** (3 min): Students cover the screen and name the five
   moves in order. They uncover the chart to check.
3. **New Problem** (6 min): Give a new drawing problem, such as "draw a
   triangle with sides 100 steps long." For each move, students write one
   sentence saying what they would do. They use the flowchart as a checklist.
4. **Follow the Loop** (2 min): Ask: "Suppose your steps never run out. Which
   arrow do you follow? Where does it take you, and why not back to move 1?"

### Assessment
- Can the student name the five moves in order without looking?
- Can the student say what they would do at each move for a new shape?
- Can the student explain what the "no" arrow means?

## References

1. [Algorithm](https://en.wikipedia.org/wiki/Algorithm) - Wikipedia - What an algorithm is: a finite list of steps, in order, that solves a problem.
2. [Flowchart](https://en.wikipedia.org/wiki/Flowchart) - Wikipedia - How boxes, diamonds and arrows are used to draw a process.
3. [Scratch](https://scratch.mit.edu/) - MIT Media Lab / Scratch Foundation - The block-based programming language used throughout this book.
4. [Mermaid Flowchart Syntax](https://mermaid.js.org/syntax/flowchart.html) - Mermaid - Documentation for the JavaScript library used to draw this chart.
