// The Four Powers of Computational Thinking - interactive infographic
// CANVAS_HEIGHT: 500
// Use this CANVAS_HEIGHT for all the iframe heights that embed this MicroSim
// A student clicks one of four cards (Decomposition, Pattern Recognition,
// Abstraction, Algorithm Design) and an infobox explains that power with a
// definition, a school-life example and a Scratch example.
// Learning objective (Bloom: Understand): given the name of one of the four
// powers, explain what it means and give one everyday example of it.

// ---------- canvas layout (standard MicroSim variables) ----------
let containerWidth;
let canvasWidth = 800;
let drawHeight = 450;
let controlHeight = 50;
let canvasHeight = drawHeight + controlHeight;
let margin = 12;
let defaultTextSize = 16;

// ---------- the book's color palette (Scratch block colors) ----------
const MOTION_BLUE = '#4C97FF';     // decomposition
const CONTROL_ORANGE = '#FFAB19';  // pattern recognition
const PURPLE = '#9966FF';          // abstraction
const PEN_GREEN = '#0FBD8C';       // algorithm design
const PANEL_GRAY = '#F5F5F5';      // infobox background
const TEXT_DARK = '#333333';       // infobox text

// ---------- content ----------
const powers = [
  {
    name: 'Decomposition',
    subtitle: 'Break it into pieces',
    color: MOTION_BLUE,
    definition: 'Breaking a big problem into smaller problems you can solve one at a time.',
    school: 'A book report is really: read the book, pick your favorite part, write about it, check your spelling.',
    scratch: 'Drawing a house is really: draw a square, then draw a triangle on top.'
  },
  {
    name: 'Pattern Recognition',
    subtitle: 'Spot what repeats',
    color: CONTROL_ORANGE,
    definition: 'Noticing when the same thing happens more than once.',
    school: 'Every multiplication problem in the row uses the same steps with different numbers.',
    scratch: 'All four sides of a square use the same move-and-turn pair.'
  },
  {
    name: 'Abstraction',
    subtitle: 'Give it a name',
    color: PURPLE,
    definition: 'Giving a group of steps one short name so you can stop thinking about the details.',
    school: 'You say "brush your teeth" instead of listing eight separate steps.',
    scratch: 'You make a block called "draw square" and just use its name after that.'
  },
  {
    name: 'Algorithm Design',
    subtitle: 'Put it in order',
    color: PEN_GREEN,
    definition: 'Putting your steps in an order that actually works.',
    school: 'You have to put on socks before shoes, not after.',
    scratch: 'Pen down has to come before you move, or nothing gets drawn.'
  }
];

// ---------- state ----------
let selected = -1;                      // index of the selected card, -1 = none yet
let visited = [false, false, false, false];
let lift = [0, 0, 0, 0];                // animated hover lift for each card, in pixels
let cardRects = [];                     // recomputed whenever the width changes
let infoRect = { x: 0, y: 0, w: 0, h: 0 };
let narrow = false;                     // true when the canvas is under 600 px wide
let resetButton;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(containerWidth, canvasHeight);
  canvas.parent(document.querySelector('main'));
  textSize(defaultTextSize);

  resetButton = createButton('Start Over');
  resetButton.parent(document.querySelector('main'));
  resetButton.position(10, drawHeight + 12);
  resetButton.mousePressed(startOver);

  computeLayout();
  describe('Four colored cards named Decomposition, Pattern Recognition, Abstraction and ' +
    'Algorithm Design. Clicking a card shows its definition, a school example and a Scratch ' +
    'example in a panel, and a counter shows how many of the four powers have been explored.', LABEL);
}

function draw() {
  updateCanvasSize();

  // drawing region
  fill('aliceblue');
  stroke('silver');
  strokeWeight(1);
  rect(0, 0, canvasWidth, drawHeight);
  // control region
  fill('white');
  rect(0, drawHeight, canvasWidth, controlHeight);

  // title
  noStroke();
  fill('black');
  textStyle(NORMAL);
  textAlign(CENTER, TOP);
  let titleSize = narrow ? 18 : 24;
  textSize(titleSize);
  while (textWidth('The Four Powers of Computational Thinking') > canvasWidth - 20 && titleSize > 12) {
    titleSize -= 1;
    textSize(titleSize);
  }
  text('The Four Powers of Computational Thinking', canvasWidth / 2, narrow ? 10 : 9);

  // cards: draw the selected card last so its scaled-up edge sits on top
  let hovered = cardUnderMouse();
  for (let i = 0; i < powers.length; i++) {
    let target = (i === hovered) ? 4 : 0;
    lift[i] = lerp(lift[i], target, 0.3);
    if (i !== selected) drawCard(i);
  }
  if (selected >= 0) drawCard(selected);

  drawInfobox();

  // pointer cursor tells the student the cards respond to a click
  cursor(hovered >= 0 ? HAND : ARROW);

  // control region hint
  noStroke();
  fill(TEXT_DARK);
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(narrow ? 13 : defaultTextSize);
  text(narrow ? 'Click each card.' : 'Click each card to see what that power means.',
    110, drawHeight + controlHeight / 2);
}

// ---------- layout ----------
function computeLayout() {
  narrow = canvasWidth < 600;
  cardRects = [];
  let top = narrow ? 38 : 46;
  if (narrow) {
    // 1 x 4 stack of short cards with the infobox below them
    let gap = 5;
    let h = 44;
    for (let i = 0; i < 4; i++) {
      cardRects.push({ x: margin, y: top + i * (h + gap), w: canvasWidth - 2 * margin, h: h });
    }
    let y = top + 4 * (h + gap) + 2;
    infoRect = { x: margin, y: y, w: canvasWidth - 2 * margin, h: drawHeight - y - 8 };
  } else {
    // 2 x 2 grid on the left (about 55%), infobox on the right (about 45%)
    let gap = 14;
    let leftW = canvasWidth * 0.55;
    let w = (leftW - margin - gap) / 2;
    let h = (drawHeight - top - margin - gap) / 2;
    for (let i = 0; i < 4; i++) {
      let col = i % 2;
      let row = floor(i / 2);
      cardRects.push({ x: margin + col * (w + gap), y: top + row * (h + gap), w: w, h: h });
    }
    let x = leftW + gap;
    infoRect = { x: x, y: top, w: canvasWidth - margin - x, h: drawHeight - top - margin };
  }
}

function cardUnderMouse() {
  for (let i = 0; i < cardRects.length; i++) {
    let r = cardRects[i];
    if (mouseX >= r.x && mouseX <= r.x + r.w && mouseY >= r.y && mouseY <= r.y + r.h) return i;
  }
  return -1;
}

// ---------- cards ----------
function drawCard(i) {
  let p = powers[i];
  let r = cardRects[i];
  let isSelected = (i === selected);
  let s = isSelected ? (narrow ? 1.02 : 1.05) : 1;

  push();
  translate(r.x + r.w / 2, r.y + r.h / 2 - lift[i]);
  scale(s);
  translate(-r.w / 2, -r.h / 2);

  // soft shadow so the lifted card looks raised
  noStroke();
  fill(0, 0, 0, 40);
  rect(3, 4 + lift[i], r.w, r.h, 14);

  fill(p.color);
  rect(0, 0, r.w, r.h, 14);

  if (isSelected) {
    // white inner border marks the selected card
    noFill();
    stroke('white');
    if (narrow) {
      strokeWeight(3);
      rect(3, 3, r.w - 6, r.h - 6, 11);
    } else {
      strokeWeight(4);
      rect(5, 5, r.w - 10, r.h - 10, 10);
    }
  }

  if (narrow) {
    drawIcon(i, 38, r.h / 2, 48, 28);
    cardText(p.name, 74, r.h / 2 - 9, 15, BOLD, LEFT, r.w - 86);
    cardText(p.subtitle, 74, r.h / 2 + 10, 13, NORMAL, LEFT, r.w - 86);
  } else {
    cardText(p.name, r.w / 2, 26, 18, BOLD, CENTER, r.w - 24);
    drawIcon(i, r.w / 2, r.h / 2 + 4, r.w - 40, r.h - 96);
    cardText(p.subtitle, r.w / 2, r.h - 24, 16, NORMAL, CENTER, r.w - 24);
  }
  pop();
}

// White card text with a faint shadow, shrunk if needed so it never leaves the card
function cardText(str, x, y, size, style, align, maxW) {
  noStroke();
  textStyle(style);
  textAlign(align, CENTER);
  textSize(size);
  while (textWidth(str) > maxW && size > 10) {
    size -= 1;
    textSize(size);
  }
  fill(0, 0, 0, 70);
  text(str, x + 1, y + 1);
  fill('white');
  text(str, x, y);
  textStyle(NORMAL);
}

// Line-art icons drawn in code. Each icon is designed in a 140 x 90 box
// centered on (cx, cy) and scaled to fit the space the card gives it.
function drawIcon(i, cx, cy, w, h) {
  let u = min(w / 140, h / 90);
  push();
  translate(cx, cy);
  stroke('white');
  strokeWeight(max(1.5, 3 * u));
  strokeJoin(ROUND);
  noFill();

  if (i === 0) {
    // Decomposition: one large square that splits into four small squares
    rect(-66 * u, -28 * u, 56 * u, 56 * u, 3 * u);
    arrow(-2 * u, 0, 20 * u, 0, 6 * u);
    let q = 23 * u;
    let g = 9 * u;
    let x0 = 30 * u;
    let y0 = -(2 * q + g) / 2;
    for (let a = 0; a < 2; a++) {
      for (let b = 0; b < 2; b++) {
        rect(x0 + a * (q + g), y0 + b * (q + g), q, q, 2 * u);
      }
    }
  } else if (i === 1) {
    // Pattern recognition: a row of three identical triangles
    let tw = 34 * u;
    let g = 12 * u;
    for (let k = -1; k <= 1; k++) {
      let x = k * (tw + g);
      triangle(x - tw / 2, 22 * u, x + tw / 2, 22 * u, x, -22 * u);
    }
  } else if (i === 2) {
    // Abstraction: a named box in front, with the details greyed out behind it
    stroke(255, 255, 255, 110);
    for (let k = 0; k < 4; k++) {
      let y = (-34 + k * 14) * u;
      rect(-34 * u, y, (k % 2 === 0 ? 96 : 76) * u, 9 * u, 2 * u);
    }
    stroke('white');
    fill(PURPLE);
    rect(-62 * u, -4 * u, 104 * u, 34 * u, 6 * u);
    let labelSize = 15 * u;
    if (labelSize >= 8) {
      noStroke();
      fill('white');
      textStyle(BOLD);
      textAlign(CENTER, CENTER);
      textSize(labelSize);
      text('draw square', -10 * u, 13 * u);
      textStyle(NORMAL);
    } else {
      line(-48 * u, 13 * u, 28 * u, 13 * u);
    }
  } else {
    // Algorithm design: three numbered steps joined by downward arrows
    let ys = [-32 * u, 0, 32 * u];
    let d = 22 * u;
    for (let k = 0; k < 3; k++) {
      stroke('white');
      noFill();
      circle(-34 * u, ys[k], d);
      line(-14 * u, ys[k], (k === 1 ? 44 : 30) * u, ys[k]);
      if (k < 2) arrow(-34 * u, ys[k] + d / 2 + 1 * u, -34 * u, ys[k + 1] - d / 2 - 2 * u, 4 * u);
      if (13 * u >= 7) {
        noStroke();
        fill('white');
        textStyle(BOLD);
        textAlign(CENTER, CENTER);
        textSize(13 * u);
        text(k + 1, -34 * u, ys[k] + 0.5 * u);
        textStyle(NORMAL);
      }
    }
  }
  pop();
}

// A line with an arrowhead at (x2, y2), drawn with the current stroke
function arrow(x1, y1, x2, y2, headSize) {
  line(x1, y1, x2, y2);
  let a = atan2(y2 - y1, x2 - x1);
  line(x2, y2, x2 - headSize * cos(a - PI / 5), y2 - headSize * sin(a - PI / 5));
  line(x2, y2, x2 - headSize * cos(a + PI / 5), y2 - headSize * sin(a + PI / 5));
}

// ---------- infobox ----------
function drawInfobox() {
  let r = infoRect;
  stroke('silver');
  strokeWeight(1);
  fill(PANEL_GRAY);
  rect(r.x, r.y, r.w, r.h, 10);

  let pad = narrow ? 10 : 14;
  let counterH = narrow ? 24 : 34;
  let exploredCount = visited.filter(v => v).length;

  if (selected < 0) {
    // first load: italic grey prompt
    noStroke();
    fill('dimgray');
    textStyle(ITALIC);
    textAlign(CENTER, CENTER);
    textSize(narrow ? 15 : 17);
    drawWrapped(wrapLines('Click a card to learn about that power.', r.w - 2 * pad),
      r.x + r.w / 2, r.y + (r.h - counterH) / 2, narrow ? 20 : 24, true);
    textStyle(NORMAL);
  } else {
    let p = powers[selected];
    // heading band in the card's own color, so the link to the card is obvious
    let headH = narrow ? 26 : 34;
    noStroke();
    fill(p.color);
    rect(r.x + 1, r.y + 1, r.w - 2, headH, 9, 9, 0, 0);
    cardText(p.name, r.x + pad, r.y + 1 + headH / 2, narrow ? 16 : 18, BOLD, LEFT, r.w - 2 * pad);

    // body: pick the largest text size that fits the panel
    let bodyTop = r.y + headH + (narrow ? 7 : 12);
    let bodyH = r.y + r.h - counterH - bodyTop;
    let sections = [
      { label: '', body: p.definition },
      { label: 'At school: ', body: p.school },
      { label: 'In Scratch: ', body: p.scratch }
    ];
    // wide layout: each label sits on its own line; narrow layout: the label
    // shares the first line with its text, which saves two lines of height
    let inline = narrow;
    let size = narrow ? 15 : 16;
    let layout = layoutSections(sections, r.w - 2 * pad, size, inline);
    while (layout.height > bodyH && size > 10) {
      size -= 1;
      layout = layoutSections(sections, r.w - 2 * pad, size, inline);
    }
    let y = bodyTop;
    textAlign(LEFT, TOP);
    textSize(size);
    noStroke();
    for (let sec of layout.sections) {
      let indent = sec.label ? 14 : 0;
      if (sec.label) {
        fill(p.color);
        circle(r.x + pad + 4, y + size * 0.55, 8);
        fill(TEXT_DARK);
        textStyle(BOLD);
        text(sec.label, r.x + pad + indent, y);
        textStyle(NORMAL);
        if (!inline) y += layout.lineH;
      }
      fill(TEXT_DARK);
      for (let k = 0; k < sec.lines.length; k++) {
        let firstLineShift = (inline && k === 0) ? sec.labelW : 0;
        text(sec.lines[k], r.x + pad + indent + firstLineShift, y);
        y += layout.lineH;
      }
      y += layout.gap;
    }
  }

  // counter at the bottom of the infobox
  noStroke();
  textAlign(LEFT, CENTER);
  textSize(narrow ? 14 : 16);
  let cy = r.y + r.h - counterH / 2 - (narrow ? 0 : 3);
  if (exploredCount === 4) {
    fill(PEN_GREEN);
    textStyle(BOLD);
    let msg = 'You have explored all four powers!';
    while (textWidth(msg) > r.w - 2 * pad && textSize() > 10) textSize(textSize() - 1);
    text(msg, r.x + pad, cy);
  } else {
    fill(TEXT_DARK);
    textStyle(NORMAL);
    text('Explored: ' + exploredCount + ' of 4', r.x + pad, cy);
    // four small dots, one per power, filled in when that card has been opened
    let dx = r.x + pad + textWidth('Explored: 0 of 4') + 14;
    for (let i = 0; i < 4; i++) {
      stroke(powers[i].color);
      strokeWeight(2);
      if (visited[i]) fill(powers[i].color); else noFill();
      circle(dx + i * 18, cy, 11);
    }
    noStroke();
  }
  textStyle(NORMAL);
}

// Word-wrap each section at the given text size and report the total height
function layoutSections(sections, maxW, size, inline) {
  textSize(size);
  let lineH = round(size * 1.32);
  let gap = round(size * 0.55);
  let out = [];
  let h = 0;
  for (let sec of sections) {
    let labelW = 0;
    if (sec.label && inline) {
      textStyle(BOLD);
      labelW = textWidth(sec.label);
    }
    textStyle(NORMAL);
    let lines = wrapLines(sec.body, maxW - (sec.label ? 14 : 0), labelW);
    out.push({ label: sec.label, labelW: labelW, lines: lines });
    h += (lines.length + (sec.label && !inline ? 1 : 0)) * lineH + gap;
  }
  return { sections: out, lineH: lineH, gap: gap, height: h - gap };
}

// Split a string into lines no wider than maxW at the current text size.
// firstIndent is space already used on the first line (for an inline label).
function wrapLines(str, maxW, firstIndent) {
  let words = str.split(' ');
  let lines = [];
  let current = '';
  let room = maxW - (firstIndent || 0);
  for (let w of words) {
    let trial = current ? current + ' ' + w : w;
    if (textWidth(trial) > room && current) {
      lines.push(current);
      current = w;
      room = maxW;
    } else {
      current = trial;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function drawWrapped(lines, x, yCenter, lineH) {
  let y = yCenter - (lines.length - 1) * lineH / 2;
  for (let ln of lines) {
    text(ln, x, y);
    y += lineH;
  }
}

// ---------- interaction ----------
function mousePressed() {
  let i = cardUnderMouse();
  if (i >= 0) {
    // clicking the selected card again keeps it selected, so the infobox is never empty
    selected = i;
    visited[i] = true;
  }
}

function startOver() {
  selected = -1;
  visited = [false, false, false, false];
}

// ---------- responsive behavior ----------
function windowResized() {
  updateCanvasSize();
  resizeCanvas(containerWidth, canvasHeight);
  computeLayout();
}

function updateCanvasSize() {
  const container = document.querySelector('main').getBoundingClientRect();
  containerWidth = Math.floor(container.width);
  if (containerWidth !== canvasWidth) {
    canvasWidth = containerWidth;
    if (cardRects.length) computeLayout();
  } else {
    canvasWidth = containerWidth;
  }
}
