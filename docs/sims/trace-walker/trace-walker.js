// Step-by-Step Trace Walker
// CANVAS_HEIGHT: 520
// Use this CANVAS_HEIGHT for all the iframe heights that embed this MicroSim
// Runs a short list of motion instructions one line at a time. With Predict
// turned on, the student must say what the next line will change (position or
// heading) before the turtle is allowed to move.
// Learning objective (Bloom: Analyze): given a short list of motion
// instructions and a starting position and heading, predict the turtle's
// position and heading after each instruction.

// ---------- canvas layout (standard MicroSim variables) ----------
let containerWidth;
let canvasWidth = 800;
let drawHeight = 470;
let controlHeight = 50;
let canvasHeight = drawHeight + controlHeight;
let margin = 10;
let defaultTextSize = 16;

// ---------- colors ----------
const GRID_LINE = '#E0E0E0';
const AXIS_LINE = '#999999';
const TRAIL_TEAL = '#0FBD8C';        // Scratch pen green
const HIGHLIGHT = '#FFAB19';         // the instruction about to run
const TEXT_DARK = '#333333';

// ---------- stage coordinates (the same as the Scratch stage) ----------
const X_MAX = 240;
const Y_MAX = 180;

// ---------- programs ----------
// A move changes the position. A turn changes the heading. Nothing else does.
const MOVE = { text: 'move 100 steps', kind: 'move', amount: 100, changes: 'position' };
const TURN = { text: 'turn right 90 degrees', kind: 'turn', amount: 90, changes: 'heading' };

const programs = [
  {
    name: 'Two sides of a square',
    steps: [MOVE, TURN, MOVE, TURN],
    done: 'Done. The turtle drew two sides and is facing left.'
  },
  {
    name: 'A whole square',
    steps: [MOVE, TURN, MOVE, TURN, MOVE, TURN, MOVE, TURN],
    done: 'Done. The turtle drew a whole square. It is back where it started and facing right.'
  }
];

const HEADING_NAMES = ['right', 'down', 'left', 'up'];   // 0, 90, 180 and 270 degrees clockwise
const STEP_MS = 500;                 // each step animates for half a second

// ---------- state ----------
let program = programs[0];
let stepIndex = 0;                   // the line that will run next
let turtle = { x: 0, y: 0, heading: 0 };
let trail = [{ x: 0, y: 0 }];        // corners of the path drawn so far
let results = [];                    // what each finished line changed
let phase = 'ready';                 // ready | asking | animating | done
let animStart = 0;
let animFrom = null;
let animTo = null;
let feedback = null;                 // { text, good } shown after a prediction
let lastChanged = null;              // 'position' or 'heading', highlighted in the readout

// ---------- controls ----------
let nextButton, resetButton, predictCheckbox, programSelect;
let positionButton, headingButton;   // the two prediction answers
const ANSWER_W = 140;
const ANSWER_H = 28;

// layout rectangles, recomputed every frame from the canvas width
let banner, stagePanel, listPanel, grid;

function setup() {
  updateCanvasSize();
  const canvas = createCanvas(containerWidth, canvasHeight);
  const mainElement = document.querySelector('main');
  canvas.parent(mainElement);
  textSize(defaultTextSize);

  nextButton = createButton('Next step');
  nextButton.parent(mainElement);
  nextButton.mousePressed(nextStep);

  resetButton = createButton('Reset');
  resetButton.parent(mainElement);
  resetButton.mousePressed(resetSim);

  predictCheckbox = createCheckbox('Predict', true);
  predictCheckbox.parent(mainElement);
  predictCheckbox.changed(predictChanged);

  programSelect = createSelect();
  programSelect.parent(mainElement);
  for (let p of programs) programSelect.option(p.name);
  programSelect.changed(programChanged);

  // answer buttons sit in the prompt banner above the stage and only show
  // while the sim is waiting for a prediction
  positionButton = createButton('Position changes');
  positionButton.parent(mainElement);
  positionButton.size(ANSWER_W, ANSWER_H);
  positionButton.mousePressed(function () { answer('position'); });
  positionButton.hide();

  headingButton = createButton('Heading changes');
  headingButton.parent(mainElement);
  headingButton.size(ANSWER_W, ANSWER_H);
  headingButton.mousePressed(function () { answer('heading'); });
  headingButton.hide();

  computeLayout();
  positionControls();

  describe('A coordinate grid with a turtle marker, next to a list of motion instructions. ' +
    'Pressing Next step runs one instruction. With Predict on, the student first chooses whether ' +
    'the instruction changes the position or the heading of the turtle.', LABEL);
}

function draw() {
  updateCanvasSize();
  computeLayout();

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
  textSize(canvasWidth < 500 ? 20 : 24);
  text('Step-by-Step Trace Walker', canvasWidth / 2, 8);

  updateAnimation();

  drawBanner();
  drawStage();
  drawInstructionList();

  // label for the Program dropdown (left out when there is no room for it)
  if (canvasWidth >= 520) {
    noStroke();
    fill('black');
    textStyle(NORMAL);
    textAlign(LEFT, CENTER);
    textSize(defaultTextSize);
    text('Program:', 268, drawHeight + 25);
  }
}

// ---------- layout ----------
function computeLayout() {
  let top = 104;
  let bottom = drawHeight - 8;
  let leftW = canvasWidth * 0.55;

  banner = { x: margin, y: 38, w: canvasWidth - 2 * margin, h: 60 };
  stagePanel = { x: margin, y: top, w: leftW - margin - 4, h: bottom - top };
  listPanel = { x: leftW + 4, y: top, w: canvasWidth - margin - leftW - 4, h: bottom - top };

  // the readout needs two lines when the stage is too narrow for one
  textStyle(BOLD);
  textSize(15);
  let oneLine = textWidth('Position: (-100, -100)    Heading: right') + 16 <= stagePanel.w;
  textStyle(NORMAL);
  let readoutH = oneLine ? 28 : 42;

  // grid keeps the 4:3 shape of the stage and always shows the whole range
  let availW = stagePanel.w - 12;
  let availH = stagePanel.h - readoutH - 6;
  let s = min(availW / (2 * X_MAX), availH / (2 * Y_MAX));
  let gw = 2 * X_MAX * s;
  let gh = 2 * Y_MAX * s;
  grid = {
    x: stagePanel.x + (stagePanel.w - gw) / 2,
    y: stagePanel.y + readoutH + (availH - gh) / 2,
    w: gw, h: gh, scale: s,
    readoutH: readoutH, oneLine: oneLine
  };
}

function positionControls() {
  let y = drawHeight + 13;
  nextButton.position(10, y);
  resetButton.position(98, y);
  predictCheckbox.position(160, y + 1);
  if (canvasWidth >= 520) {
    programSelect.position(342, y);
  } else {
    programSelect.position(240, y);
    programSelect.style('max-width', max(90, canvasWidth - 250) + 'px');
  }
  // the two answer buttons, centered on the second line of the banner
  let by = banner.y + banner.h - ANSWER_H - 4;
  positionButton.position(canvasWidth / 2 - ANSWER_W - 6, by);
  headingButton.position(canvasWidth / 2 + 6, by);
}

// stage coordinates to screen coordinates (y points up on the stage)
function sx(x) { return grid.x + grid.w / 2 + x * grid.scale; }
function sy(y) { return grid.y + grid.h / 2 - y * grid.scale; }

// ---------- prompt banner (above the stage) ----------
function drawBanner() {
  let b = banner;
  stroke('silver');
  strokeWeight(1);
  fill(phase === 'asking' ? 'lemonchiffon' : 'white');
  rect(b.x, b.y, b.w, b.h, 10);

  noStroke();
  textAlign(CENTER, CENTER);
  if (phase === 'asking') {
    fill(TEXT_DARK);
    textStyle(BOLD);
    fitText('Where will the turtle be after this line?', b.w - 20, 17);
    text('Where will the turtle be after this line?', b.x + b.w / 2, b.y + 15);
    textStyle(NORMAL);
    return;
  }

  // everything else is one message, wrapped and centered in the banner
  let msg;
  let color = TEXT_DARK;
  let doneText = (phase === 'done') ? program.done : '';
  if (feedback) {
    msg = feedback.text + (doneText ? ' ' + doneText : '');
    color = feedback.good ? 'darkgreen' : 'saddlebrown';
  } else if (doneText) {
    msg = doneText;
  } else if (stepIndex === 0 && phase === 'ready') {
    msg = 'Press Next step to run the highlighted line.';
  } else if (lastChanged) {
    msg = 'Line ' + stepIndex + ' changed the ' + lastChanged + '.';
  } else {
    msg = '';
  }
  fill(color);
  textStyle(feedback ? BOLD : NORMAL);
  let size = 17;
  textSize(size);
  let lines = wrapLines(msg, b.w - 24);
  while (lines.length * (size + 5) > b.h - 6 && size > 10) {
    size -= 1;
    textSize(size);
    lines = wrapLines(msg, b.w - 24);
  }
  let lineH = size + 5;
  let y = b.y + b.h / 2 - (lines.length - 1) * lineH / 2;
  for (let ln of lines) {
    text(ln, b.x + b.w / 2, y);
    y += lineH;
  }
  textStyle(NORMAL);
}

// ---------- stage: readout, grid, trail, turtle ----------
function drawStage() {
  let p = stagePanel;
  stroke('silver');
  strokeWeight(1);
  fill('white');
  rect(p.x, p.y, p.w, p.h, 10);

  drawReadout();

  // gridlines every 20 units
  stroke(GRID_LINE);
  strokeWeight(1);
  for (let x = -X_MAX; x <= X_MAX; x += 20) line(sx(x), sy(-Y_MAX), sx(x), sy(Y_MAX));
  for (let y = -Y_MAX; y <= Y_MAX; y += 20) line(sx(-X_MAX), sy(y), sx(X_MAX), sy(y));

  // axes
  stroke(AXIS_LINE);
  strokeWeight(1.5);
  line(sx(-X_MAX), sy(0), sx(X_MAX), sy(0));
  line(sx(0), sy(-Y_MAX), sx(0), sy(Y_MAX));

  // tick marks and labels every 100 units. The labels sit along the bottom
  // and left edges of the grid so the turtle's path never covers them.
  if (grid.scale > 0.3) {
    stroke(AXIS_LINE);
    strokeWeight(1.5);
    for (let x = -200; x <= 200; x += 100) line(sx(x), sy(0) - 3, sx(x), sy(0) + 3);
    for (let y = -100; y <= 100; y += 100) line(sx(0) - 3, sy(y), sx(0) + 3, sy(y));
    noStroke();
    fill('dimgray');
    textStyle(NORMAL);
    textSize(12);
    textAlign(CENTER, BOTTOM);
    for (let x = -200; x <= 200; x += 100) {
      if (x !== 0) text(x, sx(x), sy(-Y_MAX) - 2);
    }
    textAlign(LEFT, CENTER);
    for (let y = -100; y <= 100; y += 100) {
      if (y !== 0) text(y, sx(-X_MAX) + 4, sy(y));
    }
  }

  // where the turtle is right now (part way through a step while animating)
  let now = currentTurtle();

  // trail of the path travelled so far
  stroke(TRAIL_TEAL);
  strokeWeight(3);
  strokeCap(ROUND);
  noFill();
  for (let i = 1; i < trail.length; i++) {
    line(sx(trail[i - 1].x), sy(trail[i - 1].y), sx(trail[i].x), sy(trail[i].y));
  }
  let last = trail[trail.length - 1];
  line(sx(last.x), sy(last.y), sx(now.x), sy(now.y));

  // turtle marker: a green triangle whose point shows the heading
  push();
  translate(sx(now.x), sy(now.y));
  rotate(radians(now.heading));
  stroke('white');
  strokeWeight(1.5);
  fill('green');
  let t = max(8, 13 * min(1, grid.scale * 1.25));
  triangle(t, 0, -t * 0.7, -t * 0.7, -t * 0.7, t * 0.7);
  pop();
}

function drawReadout() {
  let p = stagePanel;
  let pos = 'Position: (' + turtle.x + ', ' + turtle.y + ')';
  let head = 'Heading: ' + HEADING_NAMES[turtle.heading / 90];
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  noStroke();

  let parts;
  if (grid.oneLine) {
    textSize(15);
    let gap = textWidth('    ');
    let total = textWidth(pos) + gap + textWidth(head);
    let x = p.x + (p.w - total) / 2;
    let y = p.y + grid.readoutH / 2 + 3;
    parts = [{ s: pos, x: x, y: y, key: 'position' },
             { s: head, x: x + textWidth(pos) + gap, y: y, key: 'heading' }];
  } else {
    fitText('Position: (-100, -100)', p.w - 16, 14);
    parts = [{ s: pos, x: p.x + (p.w - textWidth(pos)) / 2, y: p.y + 13, key: 'position' },
             { s: head, x: p.x + (p.w - textWidth(head)) / 2, y: p.y + 31, key: 'heading' }];
  }
  for (let part of parts) {
    // a soft highlight marks the value the last line changed
    if (part.key === lastChanged) {
      fill('gold');
      rect(part.x - 5, part.y - 10, textWidth(part.s) + 10, 20, 6);
    }
    fill(TEXT_DARK);
    text(part.s, part.x, part.y);
  }
  textStyle(NORMAL);
}

// ---------- instruction list ----------
function drawInstructionList() {
  let p = listPanel;
  stroke('silver');
  strokeWeight(1);
  fill('white');
  rect(p.x, p.y, p.w, p.h, 10);

  noStroke();
  fill(TEXT_DARK);
  textStyle(BOLD);
  textAlign(LEFT, CENTER);
  fitText('Instructions', p.w - 20, 16);
  text('Instructions', p.x + 10, p.y + 16);
  textStyle(NORMAL);

  let steps = program.steps;
  let listTop = p.y + 32;
  let gap = 5;
  let rowH = min(40, (p.y + p.h - 8 - listTop - gap * (steps.length - 1)) / steps.length);
  let rowX = p.x + 8;
  let rowW = p.w - 16;

  // One text size for every row, small enough for the longest row and its
  // "what changed" label. If that would make the text too small to read, the
  // label moves to a second line inside the row instead.
  let longest = '8. turn right 90 degrees';
  let size = min(16, rowH * 0.5);
  textSize(size);
  while (size > 12 && textWidth(longest) + textWidth('position') + 26 > rowW) {
    size -= 0.5;
    textSize(size);
  }
  let twoLines = textWidth(longest) + textWidth('position') + 26 > rowW;
  if (twoLines) {
    size = min(14, rowH * 0.36);
    textSize(size);
    while (size > 9 && textWidth(longest) + 14 > rowW) {
      size -= 0.5;
      textSize(size);
    }
  }
  let textDy = twoLines ? -rowH * 0.2 : 1;
  let labelDy = twoLines ? rowH * 0.22 : 1;

  for (let i = 0; i < steps.length; i++) {
    let y = listTop + i * (rowH + gap);
    let isDone = i < stepIndex;
    let isCurrent = (i === stepIndex) && phase !== 'done';

    push();
    if (isDone) drawingContext.globalAlpha = 0.5;      // finished lines fade to 50%
    stroke(isCurrent ? 'darkorange' : 'silver');
    strokeWeight(isCurrent ? 2 : 1);
    fill(isCurrent ? HIGHLIGHT : 'white');
    rect(rowX, y, rowW, rowH, 8);

    noStroke();
    fill(isCurrent ? 'black' : TEXT_DARK);
    textStyle(isCurrent ? BOLD : NORMAL);
    textAlign(LEFT, CENTER);
    textSize(size);
    text((i + 1) + '. ' + steps[i].text, rowX + 7, y + rowH / 2 + textDy);
    pop();

    // what the finished line changed, drawn at full strength so it can be read
    if (isDone) {
      noStroke();
      fill(TEXT_DARK);
      textStyle(ITALIC);
      textAlign(RIGHT, CENTER);
      textSize(size);
      text(results[i], rowX + rowW - 8, y + rowH / 2 + labelDy);
      textStyle(NORMAL);
    }
  }
}

// ---------- stepping ----------
function nextStep() {
  if (phase !== 'ready') return;
  feedback = null;
  if (predictCheckbox.checked()) {
    phase = 'asking';
    updateControlStates();
  } else {
    startStep();
  }
}

// the student picked "Position changes" or "Heading changes"
function answer(choice) {
  if (phase !== 'asking') return;
  let good = (choice === program.steps[stepIndex].changes);
  feedback = good
    ? { good: true, text: 'Yes!' }
    : { good: false, text: 'Not this time — moving changes position, turning changes heading.' };
  startStep();
}

function startStep() {
  let step = program.steps[stepIndex];
  animFrom = { x: turtle.x, y: turtle.y, heading: turtle.heading };
  animTo = { x: turtle.x, y: turtle.y, heading: turtle.heading };
  if (step.kind === 'move') {
    // heading is measured clockwise from "right"; y goes up on the stage
    animTo.x = turtle.x + Math.round(step.amount * Math.cos(radians(turtle.heading)));
    animTo.y = turtle.y - Math.round(step.amount * Math.sin(radians(turtle.heading)));
  } else {
    animTo.heading = turtle.heading + step.amount;    // may pass 360 while animating
  }
  lastChanged = null;
  animStart = millis();
  phase = 'animating';
  updateControlStates();
}

function updateAnimation() {
  if (phase !== 'animating') return;
  if (millis() - animStart < STEP_MS) return;
  // the step is finished: record the new state
  let step = program.steps[stepIndex];
  turtle = { x: animTo.x, y: animTo.y, heading: animTo.heading % 360 };
  if (step.kind === 'move') trail.push({ x: turtle.x, y: turtle.y });
  results[stepIndex] = step.changes;
  lastChanged = step.changes;
  stepIndex += 1;
  phase = (stepIndex >= program.steps.length) ? 'done' : 'ready';
  updateControlStates();
}

// the turtle as it should be drawn this frame
function currentTurtle() {
  if (phase !== 'animating') return turtle;
  let t = constrain((millis() - animStart) / STEP_MS, 0, 1);
  t = t * t * (3 - 2 * t);
  return {
    x: lerp(animFrom.x, animTo.x, t),
    y: lerp(animFrom.y, animTo.y, t),
    heading: lerp(animFrom.heading, animTo.heading, t)
  };
}

function resetSim() {
  stepIndex = 0;
  turtle = { x: 0, y: 0, heading: 0 };
  trail = [{ x: 0, y: 0 }];
  results = [];
  phase = 'ready';
  feedback = null;
  lastChanged = null;
  updateControlStates();
}

function programChanged() {
  let name = programSelect.value();
  for (let p of programs) {
    if (p.name === name) program = p;
  }
  resetSim();
}

// turning Predict off in the middle of a question just runs the line
function predictChanged() {
  if (phase === 'asking' && !predictCheckbox.checked()) {
    feedback = null;
    startStep();
  }
}

function updateControlStates() {
  // Next step is only live when the sim is waiting for it. After the last
  // line it stays disabled until Reset is pressed.
  if (phase === 'ready') {
    nextButton.removeAttribute('disabled');
  } else {
    nextButton.attribute('disabled', '');
  }
  if (phase === 'asking') {
    positionButton.show();
    headingButton.show();
  } else {
    positionButton.hide();
    headingButton.hide();
  }
}

// ---------- text helpers ----------
// Set the largest text size, up to maxSize, at which str fits in maxW
function fitText(str, maxW, maxSize) {
  let size = maxSize;
  textSize(size);
  while (textWidth(str) > maxW && size > 9) {
    size -= 0.5;
    textSize(size);
  }
  return size;
}

// Split a string into lines no wider than maxW at the current text size
function wrapLines(str, maxW) {
  let words = str.split(' ');
  let lines = [];
  let current = '';
  for (let w of words) {
    let trial = current ? current + ' ' + w : w;
    if (textWidth(trial) > maxW && current) {
      lines.push(current);
      current = w;
    } else {
      current = trial;
    }
  }
  if (current) lines.push(current);
  return lines;
}

// ---------- responsive behavior ----------
function windowResized() {
  updateCanvasSize();
  resizeCanvas(containerWidth, canvasHeight);
  // the grid scale is recomputed so the whole coordinate range stays visible
  computeLayout();
  positionControls();
}

function updateCanvasSize() {
  const container = document.querySelector('main').getBoundingClientRect();
  containerWidth = Math.floor(container.width);
  canvasWidth = containerWidth;
}
