# Mascot Style Guide

This page shows every mascot admonition style for reference. Use it to check
that Cody's seven poses render correctly and stay readable against their
admonition background colors.

Cody's full design rules live in the
[character sheet](../img/mascot/character-sheet.md); the prompts for redrawing
the poses live in [image prompts](../img/mascot/image-prompts.md).

!!! mascot-neutral "A Note from Cody"
    ![Cody neutral pose](../../img/mascot/neutral.png){ class="mascot-admonition-img" }
    This is the neutral style. Use it for side notes, forward links, and
    anything that does not need a particular emotional tone.

!!! mascot-welcome "Welcome!"
    ![Cody waving welcome](../../img/mascot/welcome.png){ class="mascot-admonition-img" }
    This is the welcome style, used once at the opening of a chapter or lab.
    One step at a time!

!!! mascot-thinking "Key Insight"
    ![Cody thinking](../../img/mascot/thinking.png){ class="mascot-admonition-img" }
    This is the thinking style, used for key concepts and for
    predict-before-you-run questions. What do you think will happen?

!!! mascot-tip "Cody's Tip"
    ![Cody giving a tip](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    This is the tip style, used for a hint that helps without giving away the
    answer.

!!! mascot-warning "Watch Out!"
    ![Cody warning](../../img/mascot/warning.png){ class="mascot-admonition-img" }
    This is the warning style, used for the mistake a lab is designed to
    surface. Cody looks concerned here, never angry.

!!! mascot-encourage "Keep Going!"
    ![Cody encouraging](../../img/mascot/encouraging.png){ class="mascot-admonition-img" }
    This is the encouraging style, used for difficult steps and for the
    collapsed "Stuck?" hint. Being stuck is a normal part of programming.

!!! mascot-celebration "You Did It!"
    ![Cody celebrating](../../img/mascot/celebration.png){ class="mascot-admonition-img" }
    This is the celebration style, used once at the end of a chapter or lab.
    Its background is deliberately dark so the bright confetti stays visible.

## Pose Reference

Every pose at its raw size, on the page background:

<div style="display:flex;flex-wrap:wrap;gap:1rem;align-items:flex-end">
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/neutral.png" alt="Cody neutral" style="width:120px">
    <figcaption><code>neutral.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/welcome.png" alt="Cody welcome" style="width:120px">
    <figcaption><code>welcome.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/thinking.png" alt="Cody thinking" style="width:120px">
    <figcaption><code>thinking.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/tip.png" alt="Cody tip" style="width:120px">
    <figcaption><code>tip.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/warning.png" alt="Cody warning" style="width:120px">
    <figcaption><code>warning.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px">
    <img src="../../img/mascot/encouraging.png" alt="Cody encouraging" style="width:120px">
    <figcaption><code>encouraging.png</code></figcaption>
  </figure>
  <figure style="margin:0;text-align:center;width:150px;background:#311b4f;padding:6px;border-radius:6px">
    <img src="../../img/mascot/celebration.png" alt="Cody celebrating" style="width:120px">
    <figcaption style="color:#f3e5f5"><code>celebration.png</code></figcaption>
  </figure>
</div>

## Usage

Place the image in the admonition **body**, never in the title bar:

```markdown
!!! mascot-tip "Cody's Tip"
    ![Cody giving a tip](../../img/mascot/tip.png){ class="mascot-admonition-img" }
    Body text goes here, after the image.
```

The image path is relative to the **rendered page URL**, not the Markdown file.
A chapter at `docs/chapters/05-loops-repetition/index.md` renders at
`chapters/05-loops-repetition/`, so it also uses `../../img/mascot/`.

Use Cody no more than five or six times in a chapter, and never place two
mascot admonitions back to back.
