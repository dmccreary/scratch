// Decomposing a House Drawing - vis-network tree diagram
// CANVAS_HEIGHT: 600
// The total height is set by "main { height: 600px }" in style.css.
// One drawing job ("Draw a house") is broken down across four levels until
// every piece is a single Scratch block. Clicking a box answers the question
// "Is this small enough to program?" and highlights the path back to the top.
// Learning objective (Bloom: Analyze): given a drawing task, identify which
// parts are still too big to program and which are small enough to be one
// instruction.

// ---------- the book's color palette (Scratch block colors) ----------
const LEVEL_COLORS = [
    '#9966FF',   // level 0: the whole job (purple)
    '#4C97FF',   // level 1: still too big (blue)
    '#FFAB19',   // level 2: still too big (orange)
    '#0FBD8C'    // level 3: small enough to be one Scratch block (green)
];
const EDGE_COLOR = '#888888';
const EDGE_DIM = '#D0D0D0';
const EDGE_PATH = '#333333';
const CHECK = '✓ ';   // check-mark glyph placed in front of every green label

// ---------- tree data ----------
// label: text shown in the box (\n starts a new line so the boxes stay narrow)
// name:  the same text on one line, used in the infobox and tooltip
// A corner of the square walls is a 90 degree turn (360 / 4). A corner of the
// three-sided roof is a 120 degree turn (360 / 3).
const treeData = [
    { id: 'house', parent: null, level: 0, name: 'Draw a house',
      label: 'Draw a house',
      small: false, reason: 'This is the whole job. It is made of two shapes.' },

    { id: 'walls', parent: 'house', level: 1, name: 'Draw the walls (a square)',
      label: 'Draw the walls\n(a square)',
      small: false, reason: 'A square is four sides and four corners.' },
    { id: 'roof', parent: 'house', level: 1, name: 'Draw the roof (a triangle)',
      label: 'Draw the roof\n(a triangle)',
      small: false, reason: 'A triangle is three sides and three corners.' },

    { id: 'w-side', parent: 'walls', level: 2, name: 'Draw one side',
      label: 'Draw one side',
      small: false, reason: 'You still have to put the pen down first.' },
    { id: 'w-corner', parent: 'walls', level: 2, name: 'Turn one corner',
      label: 'Turn one corner',
      small: false, reason: 'You have to say how far to turn.' },
    { id: 'r-side', parent: 'roof', level: 2, name: 'Draw one side',
      label: 'Draw one side',
      small: false, reason: 'You still have to put the pen down first.' },
    { id: 'r-corner', parent: 'roof', level: 2, name: 'Turn one corner',
      label: 'Turn one corner',
      small: false, reason: 'You have to say how far to turn.' },

    { id: 'w-pen', parent: 'w-side', level: 3, name: 'Put the pen down',
      label: CHECK + 'Put the\npen down',
      small: true, reason: 'This is one block in Scratch.' },
    { id: 'w-move', parent: 'w-side', level: 3, name: 'Move forward 100 steps',
      label: CHECK + 'Move forward\n100 steps',
      small: true, reason: 'This is one block in Scratch.' },
    { id: 'w-turn', parent: 'w-corner', level: 3, name: 'Turn right 90 degrees',
      label: CHECK + 'Turn right\n90 degrees',
      small: true, reason: 'This is one block in Scratch.' },
    { id: 'r-pen', parent: 'r-side', level: 3, name: 'Put the pen down',
      label: CHECK + 'Put the\npen down',
      small: true, reason: 'This is one block in Scratch.' },
    { id: 'r-move', parent: 'r-side', level: 3, name: 'Move forward 100 steps',
      label: CHECK + 'Move forward\n100 steps',
      small: true, reason: 'This is one block in Scratch.' },
    { id: 'r-turn', parent: 'r-corner', level: 3, name: 'Turn right 120 degrees',
      label: CHECK + 'Turn right\n120 degrees',
      small: true, reason: 'This is one block in Scratch. A triangle corner is a bigger turn than a square corner.' }
];

const byId = {};
treeData.forEach(function (n) { byId[n.id] = n; });

let nodes, edges, network;
let selectedId = null;

function answerText(n) {
    return n.small ? 'Yes' : 'Not yet';
}

// ---------- build the network ----------
function initializeNetwork() {
    nodes = new vis.DataSet(treeData.map(function (n) {
        return {
            id: n.id,
            label: n.label,
            level: n.level,
            // hover tooltip gives the same answer as a click
            title: 'Small enough to program? ' + answerText(n),
            color: nodeColor(n, false),
            borderWidth: 2,
            opacity: 1
        };
    }));

    edges = new vis.DataSet(treeData.filter(function (n) { return n.parent; }).map(function (n) {
        return { id: n.parent + '>' + n.id, from: n.parent, to: n.id, width: 2, color: { color: EDGE_COLOR } };
    }));

    const options = {
        layout: {
            hierarchical: {
                enabled: true,
                direction: 'UD',
                sortMethod: 'directed',
                levelSeparation: 110,
                // The spec asked for 160, but six green boxes at 160 apart are
                // wider than the page, which shrinks the text. 126 keeps the
                // labels readable in a normal-width textbook column.
                nodeSpacing: 126,
                treeSpacing: 126,
                blockShifting: true,
                edgeMinimization: true,
                parentCentralization: true
            }
        },
        physics: { enabled: false },
        // The student cannot drag or zoom, so the layout cannot be broken by accident
        interaction: {
            dragNodes: false,
            dragView: false,
            zoomView: false,
            hover: true,
            tooltipDelay: 150,
            selectConnectedEdges: false,
            navigationButtons: false,
            keyboard: false
        },
        nodes: {
            shape: 'box',
            margin: { top: 9, right: 11, bottom: 9, left: 11 },
            shapeProperties: { borderRadius: 9 },
            font: { size: 16, face: 'Arial', color: 'white', bold: { color: 'white' } },
            shadow: { enabled: true, color: 'rgba(0,0,0,0.18)', size: 5, x: 2, y: 2 },
            chosen: false
        },
        edges: {
            arrows: { to: { enabled: true, scaleFactor: 0.8 } },
            smooth: { enabled: true, type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.45 },
            chosen: false,
            hoverWidth: 0,
            selectionWidth: 0
        }
    };

    const container = document.getElementById('network');
    network = new vis.Network(container, { nodes: nodes, edges: edges }, options);

    network.once('afterDrawing', fitNetwork);

    network.on('click', function (params) {
        if (params.nodes.length > 0) {
            selectNode(params.nodes[0]);
        } else {
            clearSelection();
        }
    });

    // pointer cursor shows the boxes respond to a click
    network.on('hoverNode', function () { container.style.cursor = 'pointer'; });
    network.on('blurNode', function () { container.style.cursor = 'default'; });
}

function nodeColor(n, isSelected) {
    const c = LEVEL_COLORS[n.level];
    const border = isSelected ? '#333333' : 'white';
    return {
        background: c,
        border: border,
        hover: { background: c, border: '#333333' },
        highlight: { background: c, border: '#333333' }
    };
}

// Show the whole tree, as large as the container allows but never zoomed past 1:1.
// (network.fit() leaves a wide empty margin, so the scale is worked out here
// from the boxes' own bounding boxes instead.)
function fitNetwork() {
    if (!network) return;
    const container = document.getElementById('network');
    let left = Infinity, right = -Infinity, top = Infinity, bottom = -Infinity;
    treeData.forEach(function (n) {
        const b = network.getBoundingBox(n.id);
        left = Math.min(left, b.left);
        right = Math.max(right, b.right);
        top = Math.min(top, b.top);
        bottom = Math.max(bottom, b.bottom);
    });
    const pad = 12;   // room for the box shadows and the thick selection border
    const scale = Math.min(1,
        container.clientWidth / (right - left + 2 * pad),
        container.clientHeight / (bottom - top + 2 * pad));
    network.moveTo({
        position: { x: (left + right) / 2, y: (top + bottom) / 2 },
        scale: scale,
        animation: false
    });
}

// ---------- selection and path highlight ----------
// Returns the ids from the given node up to the root ("Draw a house")
function pathToRoot(id) {
    const path = [];
    let n = byId[id];
    while (n) {
        path.push(n.id);
        n = n.parent ? byId[n.parent] : null;
    }
    return path;
}

function selectNode(id) {
    selectedId = id;
    const path = pathToRoot(id);

    nodes.update(treeData.map(function (n) {
        const onPath = path.indexOf(n.id) >= 0;
        return {
            id: n.id,
            opacity: onPath ? 1 : 0.3,                    // dim everything off the path
            font: { color: onPath ? 'white' : 'rgba(255,255,255,0.75)' },
            borderWidth: n.id === id ? 4 : 2,
            color: nodeColor(n, n.id === id)
        };
    }));

    edges.update(treeData.filter(function (n) { return n.parent; }).map(function (n) {
        const onPath = path.indexOf(n.id) >= 0 && path.indexOf(n.parent) >= 0;
        return {
            id: n.parent + '>' + n.id,
            width: onPath ? 4 : 2,                        // thicken the path to the top
            color: { color: onPath ? EDGE_PATH : EDGE_DIM }
        };
    }));

    showInfo(byId[id], path);
}

function clearSelection() {
    selectedId = null;
    nodes.update(treeData.map(function (n) {
        return { id: n.id, opacity: 1, font: { color: 'white' }, borderWidth: 2, color: nodeColor(n, false) };
    }));
    edges.update(treeData.filter(function (n) { return n.parent; }).map(function (n) {
        return { id: n.parent + '>' + n.id, width: 2, color: { color: EDGE_COLOR } };
    }));
    document.getElementById('infobox').innerHTML =
        '<div class="info-prompt">Click any box to find out if it is small enough to program.</div>';
}

function showInfo(n, path) {
    const box = document.getElementById('infobox');
    box.textContent = '';

    const heading = document.createElement('div');
    heading.className = 'info-heading';
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.style.backgroundColor = LEVEL_COLORS[n.level];
    heading.appendChild(chip);
    heading.appendChild(document.createTextNode(n.name));
    box.appendChild(heading);

    const line = document.createElement('div');
    line.appendChild(document.createTextNode('Is this small enough to program? '));
    const answer = document.createElement('span');
    answer.className = 'answer ' + (n.small ? 'yes' : 'notyet');
    answer.textContent = answerText(n);
    line.appendChild(answer);
    line.appendChild(document.createTextNode(' ' + n.reason));
    box.appendChild(line);

    // the path from the top job down to this box
    if (path.length > 1) {
        const p = document.createElement('div');
        p.className = 'info-path';
        const names = path.slice().reverse().map(function (id) { return byId[id].name; });
        p.textContent = 'Part of: ' + names.join(' → ');
        box.appendChild(p);
    }
}

// ---------- start up ----------
document.addEventListener('DOMContentLoaded', function () {
    initializeNetwork();
    // re-fit the tree whenever the iframe changes width
    window.addEventListener('resize', function () {
        network.redraw();
        fitNetwork();
    });
});
