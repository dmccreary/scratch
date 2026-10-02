// Algorithm Design Flowchart - clickable Mermaid flowchart
// CANVAS_HEIGHT: 700
// The total height is set by "main { height: 700px }" in style.css.
// The five moves of algorithm design, top to bottom. Clicking a box fills the
// infobox below the chart with what that move means and what it looked like
// for the square-drawing example in the chapter.
// Learning objective (Bloom: Apply): given a new drawing problem, name the
// five moves of algorithm design in order and say what to do at each move.

// ---------- the book's color palette (Scratch block colors) ----------
const PURPLE = '#9966FF';
const BLUE = '#4C97FF';
const ORANGE = '#FFAB19';
const GREEN = '#0FBD8C';

// ---------- content ----------
// label: text in the box on a normal-width page
// short: text in the box when the container is narrower than 480 pixels
const moves = {
    A: {
        label: '1. Understand the goal', short: '1. Understand', color: PURPLE,
        means: 'Say exactly what done looks like.',
        square: 'Four sides of 100 steps, four square corners, ending where it started.'
    },
    B: {
        label: '2. Decompose into pieces', short: '2. Decompose', color: BLUE,
        means: 'Cut it into pieces small enough to be one instruction.',
        square: 'A side is pen-down-and-move. A corner is turn-right-90.'
    },
    C: {
        label: '3. Find the patterns', short: '3. Patterns', color: ORANGE,
        means: 'Look for pieces that repeat.',
        square: 'Side and corner repeat four times.'
    },
    D: {
        label: '4. Put the steps in order', short: '4. Order', color: GREEN,
        means: 'Decide what has to happen before what.',
        square: 'Pen down must come before the first move, or the first side is missing.'
    },
    E: {
        label: '5. Does it finish?', short: '5. Finish?', color: '#333333',
        means: 'Make sure the steps run out. If they do not, go back to move 2 and break the problem down again.',
        square: 'Eight instructions, then it stops.'
    },
    F: {
        label: 'Your algorithm is ready', short: 'Ready!', color: PURPLE,
        means: 'You can now build it in Scratch.',
        square: 'Three lines of plain words became eight blocks.'
    }
};

const NARROW_WIDTH = 480;      // below this the box labels shorten
let selectedId = null;         // the box the student clicked last
let narrowLabels = null;       // which label set the chart was last drawn with
let renderCount = 0;

// ---------- Mermaid chart definition ----------
function chartDefinition(narrow) {
    const t = function (id) { return narrow ? moves[id].short : moves[id].label; };
    return [
        'flowchart TD',
        '    A["' + t('A') + '"]:::purple --> B["' + t('B') + '"]:::blue',
        '    B --> C["' + t('C') + '"]:::orange',
        '    C --> D["' + t('D') + '"]:::green',
        '    D --> E{"' + t('E') + '"}:::decision',
        '    E -- "yes" --> F["' + t('F') + '"]:::purple',
        // The loop back is the important part of this chart: when an algorithm
        // does not finish, you break the problem down again.
        '    E -- "no" --> B',
        '    classDef purple fill:' + PURPLE + ',stroke:#774DCB,stroke-width:2px,color:#FFFFFF,font-size:16px,font-weight:bold',
        '    classDef blue fill:' + BLUE + ',stroke:#3373CC,stroke-width:2px,color:#FFFFFF,font-size:16px,font-weight:bold',
        '    classDef orange fill:' + ORANGE + ',stroke:#CF8B17,stroke-width:2px,color:#FFFFFF,font-size:16px,font-weight:bold',
        '    classDef green fill:' + GREEN + ',stroke:#0B8E69,stroke-width:2px,color:#FFFFFF,font-size:16px,font-weight:bold',
        '    classDef decision fill:#FFFFFF,stroke:#333333,stroke-width:2px,color:#333333,font-size:16px,font-weight:bold',
        '    linkStyle default stroke:#666666,stroke-width:2px',
        // every box is clickable; this is what keeps the chart from being a static image
        '    click A call showMove("A")',
        '    click B call showMove("B")',
        '    click C call showMove("C")',
        '    click D call showMove("D")',
        '    click E call showMove("E")',
        '    click F call showMove("F")'
    ].join('\n');
}

// ---------- drawing ----------
async function renderChart() {
    const container = document.getElementById('chart');
    const narrow = container.clientWidth < NARROW_WIDTH;
    narrowLabels = narrow;
    renderCount += 1;
    const result = await mermaid.render('flowSvg' + renderCount, chartDefinition(narrow));
    container.innerHTML = result.svg;
    if (result.bindFunctions) result.bindFunctions(container);   // wires up the click directives
    markSelected();
}

// Put a thick dark border on the box that was clicked last
function markSelected() {
    document.querySelectorAll('#chart .node').forEach(function (node) {
        const match = node.id.match(/flowchart-(.+)-\d+$/);
        node.classList.toggle('selected', !!match && match[1] === selectedId);
    });
}

// Called by the Mermaid click directives. Fills the infobox for one move.
function showMove(id) {
    const move = moves[id];
    if (!move) return;
    selectedId = id;
    markSelected();

    const box = document.getElementById('infobox');
    box.style.borderColor = move.color;
    box.textContent = '';

    const title = document.createElement('div');
    title.className = 'info-title';
    title.style.backgroundColor = tint(move.color);
    title.textContent = move.label;
    box.appendChild(title);

    const body = document.createElement('div');
    body.className = 'info-body';
    const means = document.createElement('p');
    means.textContent = move.means;
    body.appendChild(means);
    const square = document.createElement('p');
    const strong = document.createElement('strong');
    strong.textContent = 'For the square: ';
    square.appendChild(strong);
    square.appendChild(document.createTextNode(move.square));
    body.appendChild(square);
    box.appendChild(body);
}
window.showMove = showMove;    // Mermaid looks the callback up on window

// a pale version of a hex color for the infobox title bar
function tint(hex) {
    const n = parseInt(hex.slice(1), 16);
    return 'rgba(' + (n >> 16) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',0.16)';
}

// ---------- start up ----------
document.addEventListener('DOMContentLoaded', function () {
    mermaid.initialize({
        startOnLoad: false,
        securityLevel: 'loose',            // lets the click directives call showMove()
        theme: 'default',
        themeVariables: { fontFamily: 'Arial, Helvetica, sans-serif', fontSize: '16px' },
        flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis',
            rankSpacing: 26,
            nodeSpacing: 34,
            padding: 12
        }
    });
    renderChart();

    // re-render when the container width changes
    let resizeTimer = null;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(renderChart, 150);
    });
});
