# Teachers Guide

This guide is for the mentors and teachers running a Scratch session, not for the
students. The student-facing material is in the [Intro](../intro/01-getting-started.md)
labs. This page covers how to run the session around those labs: what to set up
beforehand, how long each lab takes, where students reliably get stuck, and how to
tell when a student is ready to move on to Python.

## Who These Labs Are For

Scratch is our starting point for students who do not yet have keyboarding skills.
A student who cannot comfortably use the shift key, or copy and paste text, will
spend the whole hour fighting the keyboard instead of thinking about the program.
Dragging blocks removes that obstacle entirely.

The trade-off is that Scratch hides syntax. That is exactly what we want at this
stage, because the concepts we are teaching -- events, sequence, variables, loops,
and functions -- are the same concepts they will meet again in Python turtle
graphics. We are building the mental model first and the typing second.

## Before Your First Session

1. Create your own account at [scratch.mit.edu](https://scratch.mit.edu/) and work
   through all seven intro labs yourself. Do not skip this. The labs take a mentor
   about 30 minutes and you will discover the small UI details students ask about.
2. Know where the "Add Extension" button is (bottom-left corner of the editor). The
   Pen extension is not loaded by default and nearly every lab needs it. See
   [Adding the Pen Extension](../intro/02-list-of-blocks-used-in-intro.md).
3. Learn the block colors. Motion is blue, Events is yellow-brown, Control is
   orange-gold, Variables is orange, Pen is blue-green, Operators is green. When a
   student is hunting for a block, the fastest hint you can give is the color of the
   palette tab, not the name of the block.
4. Find the laminated [Scratch cards](https://scratch.mit.edu/help/cards/) in the
   plastic bins and put them on the table.
5. Skim the first four principles of computational thinking in our
   [Beginning Concepts](https://coderdojotc.github.io/CoderDojoTC/beginning-concepts/)
   page. You will refer back to them all session.

## Accounts and Saving Work

Students need their own account if they want to come back next week and continue.
Have a parent or guardian help them create it -- we have a
[handout](https://github.com/dmccreary/scratch/blob/master/handouts/scratch-make-an-account.docx)
for recording the username and password.

If a student has no account yet, use **File > Save to your computer**. That
downloads a `.sb3` file they can bring back and reopen with **File > Load from your
computer**. It is worth knowing what is inside that file -- see
[Inside the .sb3 File](sb3-file-format.md).

## Writing About Code

When you need to write a script down -- in a lesson plan, an issue, an email to
another mentor, or a chat reply -- use **scratchblocks**, not a screenshot:

```scratch
when green flag clicked
pen down
repeat (4)
  move (100) steps
  turn cw (90) degrees
end
```

It is the community-standard text notation for Scratch code, it is searchable and
correctable in a way images are not, and it is what the Scratch Wiki and forums use.
Screenshots are still right for showing the *interface*; scratchblocks is for showing
the *code*. See [Scratchblocks Notation](scratchblocks.md).

## The Lesson Arc

The seven intro labs are one continuous program. Each lab rewrites the same square
drawing to be shorter and more general. That progression *is* the lesson, so resist
the urge to let a student jump ahead to the loop version -- the loop only feels like
a win if they first felt the pain of copying four blocks by hand.

| # | Lab | Concept introduced | Typical time |
|---|-----|--------------------|--------------|
| 1 | [Getting Started](../intro/01-getting-started.md) | The editor, the green flag, events | 10 min |
| 2 | [Adding the Pen Extension](../intro/02-list-of-blocks-used-in-intro.md) | Extensions, pen down, pen color and size | 10 min |
| 3 | [Drawing a Square](../intro/03-first-square.md) | Sequence, angles, 360 / 4 = 90 | 15 min |
| 4 | [Variables](../intro/04-variables-square.md) | Naming a value, changing it in one place | 15 min |
| 5 | [Loops](../intro/05-loops.md) | Repetition, loop count | 15 min |
| 6 | [Functions](../intro/06-functions.md) | Naming a block of code, calling it | 15 min |
| 7 | [Functions With Parameters](../intro/07-functions-with-parameters.md) | Passing a value in, reuse at different sizes | 20 min |

A first-time student usually reaches lab 4 or 5 in a single session. That is a good
session. Getting to lab 7 in one sitting is uncommon and not a goal.

## Teaching Moves That Work

**Predict before you run.** Before a student presses the green flag, ask "what do you
think will happen?" Then run it. A wrong prediction followed by a surprise is worth
more than a correct program they did not think about.

**Ask, do not fix.** When a drawing comes out wrong, do not reach for the mouse. Ask
"which block drew that part?" Let them point at the block. Students who are shown the
fix learn that mentors fix things; students who find the fix learn that they can.

**Change one number.** The fastest debugging tool in Scratch is changing a single
number and pressing the flag again. Teach that loop explicitly -- change, run, look --
because it transfers directly to Python later.

**Use the math out loud.** 360 / 4 = 90 for a square, 360 / 6 = 60 for a hexagon,
360 / 8 = 45 for an octagon. Say the division every time. By lab 5 most students
will predict the angle before you ask.

**Let them decorate.** Costume changes, backdrops, and sound blocks are not a
distraction from the lesson -- they are why the student comes back next week. Budget
five minutes at the end for it.

## Where Students Get Stuck

| Symptom | Cause | What to ask |
|---------|-------|-------------|
| Nothing draws | Pen extension never added, or `pen down` missing | "Is the pen touching the paper?" |
| Nothing happens at all | Blocks not attached under `when green flag clicked` | "Which block starts your program?" |
| The old drawing is still there | No `erase all` at the top | "How do we clear the paper first?" |
| Shape does not close | Angle is not 360 divided by the number of sides | "How many turns? What do they add up to?" |
| Shape spirals or drifts | `turn left` used where `turn right` was intended, or mixed | "Point with your finger which way it turns." |
| Sprite runs off the stage | Distance too large for the 480x360 stage | "What happens if the number is smaller?" |
| Changing the variable does nothing | The literal number is still in the block, not the variable | "Is that the orange variable block, or a typed number?" |
| Custom block does nothing | Blocks were built next to the definition, not attached under it | "Is it snapped under the hat?" |
| Program runs too fast to see | No `wait` block in the loop | "Can we slow it down to watch it?" |

The `wait` block is worth introducing early even though it is not a lab. Being able
to watch the sprite draw one side at a time is what turns "the computer did
something" into "the computer did what I told it to, in order."

## Checking Understanding

Blocks in the right order do not prove understanding. These four questions do, and
they take about a minute each:

1. **Sequence:** "If I swap these two blocks, what changes?"
2. **Variables:** "I want the square twice as big. How many things do you have to
   change?" (The answer should be *one*.)
3. **Loops:** "How many times does this block run? How do you know?"
4. **Functions:** "Draw me three squares of different sizes without copying any
   blocks." (This is lab 7 -- if they can do it, they have parameters.)

## When to Move On to Python

A student is ready for the Python turtle graphics curriculum when they can do all of
the following without help:

- Predict what a script will draw before running it
- Use a variable instead of a repeated literal number
- Explain why a hexagon turns 60 degrees
- Write a custom block that takes a parameter
- Type reasonably, including the shift key and copy/paste

The last item is usually the one that decides it. The concepts transfer immediately;
the keyboarding is the gate. The Python labs deliberately repeat this same square,
variable, loop, function progression, so a student switching over gets to be the
expert on the concepts while learning the typing.

## For Curious Students

Every so often a student asks where their project actually lives, or what the
downloaded file is. That question deserves a real answer, and the answer is a good
one: the `.sb3` file is just a ZIP archive, and their program inside it is plain
text. You can show them in about a minute with `unzip` and a text editor. See
[Inside the .sb3 File](sb3-file-format.md).
