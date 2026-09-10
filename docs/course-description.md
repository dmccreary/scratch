---
title: Course Description for Course Learning Computational Thinking with Scratch
description: A detailed course description for Learning Computational Thinking with Scratch including overview, topics covered and learning objectives in the format of the 2001 Bloom Taxonomy
quality_score: 100
---

# Course Description

**Title:** Learning Computational Thinking with Scratch

**Target Audience:** Elementary school students (approximately grades 3-5) who do not yet have strong keyboarding skills. Scratch's drag-and-drop block interface lets these students focus on computational thinking without needing to type code, building the conceptual foundation they will need once their typing skills are ready for text-based languages like Python.

**Prerequisites:** None. Basic mouse use (dragging and clicking) is expected; keyboard typing skill is not required. No prior programming experience is assumed.

## Course Overview

Scratch is a mature, visual block-based programming language, but this course is not a tour of every block, sprite, or sound effect it offers. Instead, this course uses Scratch as a vehicle for teaching **computational thinking**: the set of problem-solving practices — decomposition, pattern recognition, abstraction, and algorithm design — that underlie all of computer science, independent of any one language or tool.

This course is designed specifically for students who do not yet type quickly or confidently. Scratch's drag-and-drop blocks remove the typing barrier so students can focus entirely on the thinking skills of programming — sequencing, looping, and decision-making — using only mouse actions like dragging, clicking, and snapping blocks together. As students' keyboarding skills develop alongside this course, they build the conceptual readiness they will need to move on to typing real code in Python.

A central theme of the course is abstraction. Students are introduced to Scratch's "Make a Block" feature early and repeatedly, learning to package repeated logic into their own named, reusable procedures by dragging and naming blocks rather than copying blocks by hand or typing function definitions. This habit of building and calling one's own abstractions is the single most important transferable skill for later work in text-based languages.

The course also places sustained emphasis on turtle-graphics-style drawing: using Scratch's motion and pen blocks to move a sprite, turn by angles, and draw shapes and patterns. This mirrors, block-for-block, the syntax and mental model of Python's `turtle` module, so that a student who finishes this course can move to `forward()`, `left()`, `right()`, and `penup()`/`pendown()` in Python with almost no conceptual gap — only a change in notation. Loops, variables, conditionals, and custom procedures are all taught in this drawing context so that the "shape" of a program in Scratch visually and logically matches the "shape" of the equivalent Python program the student will write next.

By the end of this course, students will think of programming not as memorizing a language's features, but as a general process of breaking a problem down, spotting repeating patterns, designing an algorithm, and expressing that algorithm precisely — a process that carries directly from Scratch's blocks into Python's typed commands.

## Main Topics Covered

- Computational thinking fundamentals: decomposition, pattern recognition, abstraction, algorithm design
- Sequencing and program flow (scripts as ordered steps)
- Coordinates, headings, and motion (x/y position, degrees of turn)
- Turtle-graphics-style drawing with the pen and motion blocks (lines, angles, polygons, patterns)
- Loops: fixed-count repetition and repeat-until (condition-based) repetition
- Variables: creating, naming, and updating values to control drawings and logic
- Conditionals: if / if-else and building simple decision logic
- Custom blocks ("Make a Block") as user-defined abstraction and procedural decomposition
- Parameters and inputs to custom blocks (generalizing a procedure)
- Events and simple interactivity (keyboard/mouse input driving a program)
- Debugging strategies: reading a script, isolating errors, testing incrementally
- Mapping Scratch concepts to Python and the `turtle` module (bridge/transition unit)

## Topics Not Covered

- Exhaustive coverage of every Scratch block, category, or sprite/costume/sound feature
- Scratch's cloud variables, cloning at an advanced level, or backpack sharing across projects
- Game-design-specific topics (physics engines, complex collision systems, scoring/level systems) except as incidental examples
- Multiplayer, online sharing, or the Scratch community site features
- Text-based Python syntax itself (variables, loops, and functions in actual Python code) — this course prepares students for that material but stops at the conceptual bridge
- List/data-structure blocks beyond a brief conceptual introduction

## Learning Outcomes

After completing this course, students will be able to:

### Remember

*Retrieving, recognizing, and recalling relevant knowledge from long-term memory.*

- Recall the names and icons of Scratch's motion, pen, control, and operator block categories used in this course
- Recognize the syntax for turning by degrees and moving forward/backward a number of steps
- State the definitions of decomposition, pattern recognition, abstraction, and algorithm
- Identify the parts of a custom block definition (name, parameters, and body)
- Recall the difference between a fixed-count loop and a condition-based loop

### Understand

*Constructing meaning from instructional messages, including oral, written, and graphic communication.*

- Explain why breaking a large drawing or task into smaller steps (decomposition) makes it easier to program
- Describe how repeated blocks in a script indicate an opportunity to use a loop or a custom block
- Explain how a sprite's heading and position determine what a pen-drawing script will produce
- Compare a script that repeats blocks manually to an equivalent script that uses a loop
- Explain, in general terms, how a Scratch custom block corresponds to a function/procedure in a text-based language like Python

### Apply

*Carrying out or using a procedure in a given situation.*

- Use motion and pen blocks to draw specified shapes (triangle, square, star, spiral) with a Scratch sprite
- Use a repeat loop to draw a regular polygon without repeating blocks manually
- Create and call a custom block to draw a reusable shape (e.g., a "draw square" block)
- Add parameters to a custom block so the same block can draw shapes of different sizes or turn angles
- Use variables to track and update values such as side length, number of sides, or angle
- Use conditionals to make a script respond differently to different inputs or states

### Analyze

*Breaking material into constituent parts and determining how the parts relate to one another and to an overall structure or purpose.*

- Break down a complex drawing (e.g., a flower made of overlapping polygons) into a sequence of simpler, reusable drawing steps
- Trace through a script step-by-step to predict the sprite's resulting path and final position
- Identify which parts of a script are repeated patterns that could be extracted into a loop or a custom block
- Diagnose why a script produces an incorrect drawing by isolating which block or value is responsible
- Compare two different scripts that produce the same drawing and analyze their relative efficiency and clarity

### Evaluate

*Making judgments based on criteria and standards through checking and critiquing.*

- Critique a classmate's script for opportunities to reduce repetition through loops or custom blocks
- Judge whether a given custom block is well-designed (clear name, sensible parameters, single responsibility)
- Assess whether a drawing algorithm is stated precisely enough that another student could follow it without seeing the code
- Evaluate trade-offs between a quick, repetitive solution and a more abstracted, reusable one
- Justify which control structure (loop vs. conditional vs. custom block) best fits a given problem

### Create

*Putting elements together to form a coherent or functional whole; reorganizing elements into a new pattern or structure.*

- Design and build an original turtle-graphics-style drawing project (e.g., a generative art piece or pattern maker) using loops, variables, and custom blocks
- Create a personal library of custom drawing blocks (e.g., shapes, spirals, flowers) that can be combined into larger compositions
- Design an algorithm on paper (pseudocode or flowchart) before implementing it in Scratch, then implement and test it
- **Capstone project:** Plan, decompose, and build a multi-part Scratch drawing project that combines at least three custom blocks, a loop, a variable, and a conditional, and present the underlying algorithm in a way that maps clearly to how it would be expressed in Python's `turtle` module
