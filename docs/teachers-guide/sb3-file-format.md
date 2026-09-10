# Inside the .sb3 File

**A `.sb3` file is not a special binary format. It is an ordinary ZIP archive, and
the program inside it is a plain text JSON file called `project.json`.**

That single fact is worth knowing as a mentor, and it is worth showing to any
student who asks where their project actually lives. Nothing is hidden. When a
student presses **File > Save to your computer**, Scratch writes a ZIP containing
their code as readable text plus one file per costume and sound.

## Proof, Using Our Own Example

The example project on this site is
[CoderDojo-Turtle-Square.sb3](../examples/CoderDojo-Turtle-Square.sb3). Ask your
operating system what it is:

```bash
file CoderDojo-Turtle-Square.sb3
```

```
CoderDojo-Turtle-Square.sb3: Zip archive data, at least v1.0 to extract, compression method=deflate
```

Now list what is inside it:

```bash
unzip -l CoderDojo-Turtle-Square.sb3
```

```
  Length      Date    Time    Name
---------  ---------- -----   ----
     3423  05-25-2020 18:45   project.json
      560  05-25-2020 18:45   83a9787d4cb6f3b7632b4ddfebf74367.wav
    37420  05-25-2020 18:45   83c36d806dc92327b9e7049a565c6bff.wav
      202  05-25-2020 18:45   cd21514d0531fdffb22204e0ec5ed84a.svg
      467  05-25-2020 18:45   9af27a7ad39ec41b7cbfda3622d08a1a.svg
    35003  05-25-2020 18:45   00c7cc0dda5a3e305182918fce955957.svg
---------                     -------
    77075                     6 files
```

Six files. Note the proportions: the entire program is 3,423 bytes of text, and the
other 73,652 bytes are the cat sprite's two costumes, the backdrop, and two sounds.
**The code is about 4% of the file. The artwork and audio are the other 96%.** That
is a genuinely useful thing to point out to a student who is surprised their
"program" is 64 KB.

Every part has a job:

| File | What it is |
|------|------------|
| `project.json` | The whole program: sprites, scripts, variables, and how they connect |
| `*.svg` | Costumes and backdrops, as vector images |
| `*.wav` | Sounds |

The asset filenames are not random. Each is the MD5 hash of that file's contents, so
two sprites using the identical costume store it only once, and `project.json`
refers to each asset by that same hash.

## Reading a Block

Open `project.json` and every block appears in a dictionary, keyed by an arbitrary
ID string. Here is one real block from that file:

```json
"k4L`,mB@k%A/bBXcn;Xh": {
  "opcode": "motion_movesteps",
  "next": "30N.apc/K!*E9T/BrF_:",
  "parent": "VwbebnQsTEM=ffUZ6ZIc",
  "inputs": { "STEPS": [1, [4, "100"]] },
  "fields": {},
  "shadow": false,
  "topLevel": false
}
```

Read it left to right and it is just `move (100) steps`:

- `opcode` is which block it is. The prefix is the palette it came from --
  `motion_`, `control_`, `pen_`, `event_`, `data_`.
- `next` and `parent` are the block IDs above and below it. A script is a linked
  list, not a nested tree -- this is the single most surprising thing about the
  format.
- `inputs` holds the values typed into the slots.
- `topLevel` is `true` only for the block that starts a script, which also carries
  `x` and `y` -- where the script sits on the canvas.

The `[1, [4, "100"]]` encoding takes a minute to get used to. The outer `1` means
the slot holds a typed-in value rather than another block plugged into it. The inner
number says what kind of value it is. These four appear in our example project:

| Code | Meaning | Seen in |
|------|---------|---------|
| `4` | number | `move (100) steps` |
| `5` | positive number | `wait (1) seconds` |
| `6` | whole number | `repeat (4)` |
| `9` | color | `set pen color to [#005dff]` |

C-blocks such as `repeat` hold their body in a `SUBSTACK` input that points at the
first block inside the loop:

```json
"VwbebnQsTEM=ffUZ6ZIc": {
  "opcode": "control_repeat",
  "inputs": {
    "TIMES": [1, [6, "4"]],
    "SUBSTACK": [2, "k4L`,mB@k%A/bBXcn;Xh"]
  }
}
```

Follow `SUBSTACK` to that block, then follow `next` three times, and you have
recovered the whole loop body. The nine blocks in that file reassemble into exactly
the script we write in [scratchblocks](scratchblocks.md) as:

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

Those two representations describe the same nine blocks. The JSON is what Scratch
reads; the scratchblocks is what humans read.

## Try It Yourself

The whole thing takes about a minute:

1. Download a project with **File > Save to your computer**.
2. Make a copy, and rename the copy from `.sb3` to `.zip`.
3. Double-click it. On macOS and Windows it unpacks like any other ZIP.
4. Open `project.json` in a text editor.

From a terminal, without renaming anything:

```bash
unzip -p CoderDojo-Turtle-Square.sb3 project.json | python3 -m json.tool | less
```

Scratch does not care about the extension when *you* open it, but the editor's
file picker does, so keep the original `.sb3` around and experiment on the copy.

## Why This Matters to a Mentor

**Backups are trivial.** A `.sb3` is one self-contained file. Copy it to a USB stick
and the project is safe -- costumes, sounds, and all.

**You can recover a "lost" project.** If a student's project will not load, the code
is still sitting there in readable text. Even in the worst case you can open
`project.json`, read the opcodes, and rebuild the script by hand.

**Projects work in version control.** You can commit `.sb3` files to Git, which is
how the example on this site is stored. Note that Git treats it as a binary blob, so
diffs are not readable -- if you want a reviewable history of a script, write it in
[scratchblocks](scratchblocks.md) next to the file.

**It answers "is Scratch real programming?"** It comes up, usually from a parent.
The honest answer is that the blocks are a user interface over a data structure, and
that data structure is a real program representation. You can open it and show them.

**It sets up a genuinely good idea.** Code is data. A student's program is a text
file that another program reads. That concept underpins compilers, interpreters, and
the Python they will learn next, and here it is visible with `unzip` and a text
editor.

## Editing the JSON Directly

You can unpack a `.sb3`, edit `project.json`, re-zip it, and load it back into
Scratch. Re-zip the *contents* of the folder, not the folder itself -- Scratch
expects `project.json` at the top level of the archive:

```bash
cd unpacked && zip -r ../rebuilt.sb3 .
```

This is a fine demonstration and a bad habit. Scratch's editor is the reliable way
to change a project, hand-edited JSON is easy to corrupt, and Scratch gives no useful
error message when a file will not load. Always work on a copy.

## A Note on Older Files

You may still find old projects in the bins or on old accounts:

| Extension | Scratch version | Format |
|-----------|-----------------|--------|
| `.sb3` | Scratch 3.0, current | ZIP containing `project.json` |
| `.sb2` | Scratch 2.0 | ZIP containing `project.json`, different JSON layout |
| `.sb` | Scratch 1.4 | Binary Squeak image format, **not** text |

Only the oldest, `.sb`, is a genuinely opaque binary format. Scratch 3 can still
import `.sb2` and `.sb` files and will convert them on load.
