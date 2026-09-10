---
name: setup
description: One-time installation of the block renderer, mascot styles, and mkdocs.yml wiring that generated labs depend on.
---

# One-Time Setup

Generated labs depend on four things being present in the project. Check each
one before generating the first lab; skip any that are already installed.

## 1. Stylesheets and the block renderer

Copy from this skill's `assets/templates/` into the project:

| Source | Destination |
|--------|-------------|
| `mascot.css` | `docs/css/mascot.css` |
| `scratchblocks.css` | `docs/css/scratchblocks.css` |
| `scratchblocks-init.js` | `docs/js/scratchblocks-init.js` |

All stylesheets live in `docs/css/` and all scripts in `docs/js/`. Put new
files alongside the existing ones rather than creating a second convention.

## 2. mkdocs.yml

Merge these keys into the existing single `markdown_extensions` list rather than
adding a second declaration — a duplicate key silently wins over the first.

```yaml
markdown_extensions:
  - admonition
  - attr_list          # required: puts the mascot image class on the image
  - md_in_html
  - footnotes
  - pymdownx.details   # required: the collapsed solution block
  - pymdownx.superfences
  - toc:
      permalink: true
  - codehilite:
      linenums: true

extra_css:
  - css/extra.css
  - css/mascot.css
  - css/scratchblocks.css

extra_javascript:
  - https://cdn.jsdelivr.net/npm/scratchblocks@3.7.1/build/scratchblocks.min.js
  - js/scratchblocks-init.js
```

`attr_list` and `pymdownx.details` are not optional. Without `attr_list` the
mascot images lose their float class and render full width; without
`pymdownx.details` the `???` solution block renders as literal question marks.

Pin the scratchblocks version. `@latest` will eventually ship a change that
breaks every diagram in the book at once.

## 3. Mascot images

Seven poses must exist at `docs/img/mascot/`:

```
neutral.png  welcome.png  thinking.png  tip.png
warning.png  encouraging.png  celebration.png
```

These are generated separately — see the `learning-mascot` reference in the
`book-installer` skill, which also holds the character sheet and the image
prompts. `check_lab.py` reports a missing pose as an error, because a broken
image on a lab page is more distracting than no image at all.

## 4. The labs index and nav

`docs/labs/index.md` lists every lab as a table with title, level, time, and a
one-line challenge summary. Add a row when a lab is generated.

Add each lab to `mkdocs.yml` under a `Labs` section:

```yaml
  - Labs:
    - List of Labs: labs/index.md
    - Draw a Square With a Loop: labs/draw-a-square/index.md
```

Order labs by dependency, not by date added — a lab that needs variables comes
after the lab that introduces them.

Note that this repo already has a `docs/labs.md` page listing planned labs in
prose. Treat it as the backlog: when a lab from that list is generated, the new
`docs/labs/index.md` row is the live version.

## 5. Python dependency

`check_lab.py` validates generated projects against the bundled Scratch schema
and needs `jsonschema`:

```bash
pip install jsonschema
```

Without it the schema check is skipped with a warning; the `.sb3` files are
still built.
