// Abstraction Layers Explorer
// CANVAS_HEIGHT: 480
// Use this CANVAS_HEIGHT for all the iframe heights that embed this MicroSim
// A student peels back the layers of an abstraction: one named block
// ("draw flower") opens up into three blocks, which open up into eight
// machine steps. Sliding back hides the detail again.
// Learning objective (Bloom: Understand): explain that naming a group of steps
// hides detail without removing it, and state how many underlying steps a
// single named block stands for.

// ---------- canvas layout (standard MicroSim variables) ----------
let containerWidth;
let canvasWidth = 750;
let drawHeight = 400;
let controlHeight = 80;              // two rows of controls
let canvasHeight = drawHeight + controlHeight;
let margin = 12;
let leftPad = 15;                    // controls are aligned left with 15 px padding
let sliderLeftMargin = 140;          // room for the labels to the left of each control
let defaultTextSize = 16;

// ---------- the book's color palette (Scratch block colors) ----------
// Each layer has a fill color and the darker outline color Scratch uses with it.
const PURPLE = '#9966FF';
const PURPLE_DARK = '#774DCB';
const BLUE = '#4C97FF';
const BLUE_DARK = '#3373CC';
const GREEN = '#0FBD8C';
const GREEN_DARK = '#0B8E69';
const TEXT_DARK = '#333333';

// ---------- content: three bands, top to bottom ----------
const bands = [
  {
    title: 'What you say',
    blocks: ['draw flower'],
    fill: PURPLE, outline: PURPLE_DARK,
    count: '1 thing to remember',
    blockTextSize: 20
  },
  {
    title: 'What that means',
    blocks: ['draw square', 'turn right 45', 'repeat 8 times'],
    fill: BLUE, outline: BLUE_DARK,
    count: '3 things to remember',
    blockTextSize: 17
  },
  {
    title: 'What the computer does',
    blocks: ['pen down', 'move 100', 'turn 90', 'move 100', 'turn 90', 'move 100', 'turn 90', 'move 100'],
    fill: GREEN, outline: GREEN_DARK,
    count: '8 things to remember',
    blockTextSize: 15
  }
];

const captions = [
  'One name. That is all you have to remember.',
  'The name was really three things.',
  'And those were really eight things. The name hid all of them for you.'
];

const REVEAL_MS = 400;               // a newly shown band slides into place in 400 ms

// ---------- state ----------
let detailSlider, countCheckbox, resetButton;
let reveal = [1, 0, 0];              // 0 = hidden, 1 = fully shown, animated per band
let narrow = false;                  // true when the canvas is under 500 px wide

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(containerWidth, canvasHeight);
  const mainElement = document.querySelector('main');
  canvas.parent(mainElement);
  textSize(defaultTextSize);

  // Row 1: Detail level slider, 1 to 3 in steps of 1
  detailSlider = createSlider(1, 3, 1, 1);
  detailSlider.parent(mainElement);
  detailSlider.position(sliderLeftMargin, drawHeight + 8);
  detailSlider.size(sliderWidth());

  // Row 2: Show step count checkbox (its label is drawn to its left) and Reset
  countCheckbox = createCheckbox('', false);
  countCheckbox.parent(mainElement);
  countCheckbox.position(sliderLeftMargin, drawHeight + 44);

  resetButton = createButton('Reset');
  resetButton.parent(mainElement);
  resetButton.position(sliderLeftMargin + 50, drawHeight + 43);
  resetButton.mousePressed(resetSim);

  describe('Three stacked bands of Scratch-style blocks. The top band has one purple block named ' +
    'draw flower. A detail level slider reveals a second band of three blue blocks and a third ' +
    'band of eight green blocks, showing the steps the one name was hiding.', LABEL);
}

function draw() {
  updateCanvasSize();
  narrow = canvasWidth < 500;

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
  textSize(narrow ? 20 : 24);
  text('Abstraction Layers Explorer', canvasWidth / 2, 9);

  let level = detailSlider.value();
  let showCounts = countCheckbox.checked();

  // move each band's reveal value toward its target (shown or hidden)
  for (let i = 1; i < 3; i++) {
    let target = (level > i) ? 1 : 0;
    let step = deltaTime / REVEAL_MS;
    if (reveal[i] < target) reveal[i] = min(target, reveal[i] + step);
    if (reveal[i] > target) reveal[i] = max(target, reveal[i] - step);
  }

  // Draw the bottom band first so a band sliding down comes out from
  // underneath the band above it, like a drawer opening.
  let geo = bandGeometry();
  // A dashed outline marks each band that is still hidden. The detail has
  // not gone away; it is only out of sight.
  for (let i = 1; i < 3; i++) {
    if (reveal[i] < 1) drawHiddenPlaceholder(geo[i], 1 - ease(reveal[i]));
  }
  for (let i = 2; i >= 0; i--) {
    if (reveal[i] > 0) drawBand(i, geo[i], ease(reveal[i]), showCounts);
  }
  // arrows between the bands that are showing
  for (let i = 1; i < 3; i++) {
    if (reveal[i] > 0) drawDownArrow(geo[i - 1].y + geo[i - 1].h, geo[i].y, ease(reveal[i]));
  }

  // caption under the bands
  let last = geo[2];
  let captionTop = last.y + last.h + 4;
  noStroke();
  fill(TEXT_DARK);
  textStyle(NORMAL);
  textAlign(CENTER, CENTER);
  textSize(16);
  text(captions[level - 1], margin, captionTop, canvasWidth - 2 * margin, drawHeight - captionTop - 6);

  // control labels, to the left of each control
  noStroke();
  fill('black');
  textStyle(NORMAL);
  textAlign(LEFT, CENTER);
  textSize(defaultTextSize);
  text('Detail level: ' + level, leftPad, drawHeight + 19);
  text('Show step count', leftPad, drawHeight + 55);
}

// Where each band sits. The third band is taller on a narrow canvas because
// its eight blocks wrap onto two rows.
function bandGeometry() {
  let top = narrow ? 38 : 44;
  let gap = narrow ? 16 : 22;
  let heights = narrow ? [64, 64, 100] : [78, 78, 78];
  let out = [];
  let y = top;
  for (let i = 0; i < 3; i++) {
    out.push({ x: margin, y: y, w: canvasWidth - 2 * margin, h: heights[i] });
    y += heights[i] + gap;
  }
  return out;
}

// smooth start and stop for the slide
function ease(t) {
  return t * t * (3 - 2 * t);
}

function drawBand(i, g, e, showCounts) {
  let band = bands[i];
  push();
  // slide down from behind the band above, fading in on the way
  translate(0, -(1 - e) * g.h * 0.75);
  drawingContext.globalAlpha = e;

  // white panel
  stroke('silver');
  strokeWeight(1);
  fill('white');
  rect(g.x, g.y, g.w, g.h, 10);

  // band title on the left of the header line
  let headerY = g.y + (narrow ? 13 : 16);
  noStroke();
  fill(TEXT_DARK);
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  textSize(narrow ? 13 : 15);
  text(band.title, g.x + 12, headerY);

  // step count on the right of the header line
  if (showCounts) {
    fill(band.outline);
    textAlign(RIGHT, CENTER);
    text(band.count, g.x + g.w - 12, headerY);
  }
  textStyle(NORMAL);

  // blocks
  let headerH = narrow ? 24 : 28;
  drawBlocks(band, g.x + 10, g.y + headerH, g.w - 20, g.h - headerH - 8);
  pop();
}

// Dashed outline that stands in for a band the slider has not opened yet
function drawHiddenPlaceholder(g, alpha) {
  push();
  drawingContext.globalAlpha = alpha;
  drawingContext.setLineDash([6, 6]);
  stroke('darkgray');
  strokeWeight(1.5);
  noFill();
  rect(g.x, g.y, g.w, g.h, 10);
  drawingContext.setLineDash([]);
  noStroke();
  fill('dimgray');
  textStyle(ITALIC);
  textAlign(CENTER, CENTER);
  textSize(narrow ? 14 : 16);
  text('Hidden detail', g.x + g.w / 2, g.y + g.h / 2);
  pop();
}

// Lay the band's blocks out in one centered row. If they do not fit, shrink
// the text; on a narrow canvas wrap them onto two rows instead.
function drawBlocks(band, x, y, w, h) {
  let labels = band.blocks;
  let size = narrow ? 12 : band.blockTextSize;
  let gap = 6;
  let padX = narrow ? 7 : 10;
  let rows = [labels];
  textStyle(BOLD);

  let rowWidth = function (row) {
    let total = 0;
    for (let s of row) total += textWidth(s) + 2 * padX;
    return total + gap * (row.length - 1);
  };

  textSize(size);
  if (narrow && rowWidth(labels) > w && labels.length > 3) {
    let half = ceil(labels.length / 2);
    rows = [labels.slice(0, half), labels.slice(half)];
  }
  let widest = function () {
    let m = 0;
    for (let row of rows) m = max(m, rowWidth(row));
    return m;
  };
  while (widest() > w && size > 9) {
    size -= 0.5;
    textSize(size);
  }

  let blockH = min(narrow ? 28 : 36, (h - gap * (rows.length - 1)) / rows.length);
  let totalH = rows.length * blockH + (rows.length - 1) * gap;
  let by = y + (h - totalH) / 2;
  for (let row of rows) {
    let bx = x + (w - rowWidth(row)) / 2;
    for (let s of row) {
      let bw = textWidth(s) + 2 * padX;
      stroke(band.outline);
      strokeWeight(1.5);
      fill(band.fill);
      rect(bx, by, bw, blockH, 7);
      noStroke();
      fill('white');
      textAlign(CENTER, CENTER);
      text(s, bx + bw / 2, by + blockH / 2 + 1);
      bx += bw + gap;
    }
    by += blockH + gap;
  }
  textStyle(NORMAL);
}

// Arrow that grows downward from one band to the next as the lower band opens
function drawDownArrow(yTop, yBottom, e) {
  let cx = canvasWidth / 2;
  let y1 = yTop + 3;
  let y2 = y1 + (yBottom - 3 - y1) * e;
  if (y2 - y1 < 4) return;
  stroke('dimgray');
  strokeWeight(3);
  line(cx, y1, cx, y2 - 2);
  noStroke();
  fill('dimgray');
  triangle(cx - 7, y2 - 8, cx + 7, y2 - 8, cx, y2);
}

function resetSim() {
  detailSlider.value(1);
  countCheckbox.checked(false);
}

function sliderWidth() {
  return max(80, canvasWidth - sliderLeftMargin - margin - 8);
}

// ---------- responsive behavior ----------
function windowResized() {
  updateCanvasSize();
  resizeCanvas(containerWidth, canvasHeight);
  detailSlider.size(sliderWidth());
}

function updateCanvasSize() {
  const container = document.querySelector('main').getBoundingClientRect();
  containerWidth = Math.floor(container.width);
  canvasWidth = containerWidth;
}
