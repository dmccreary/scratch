#!/usr/bin/env python3
"""
make_sb3.py - compile scratchblocks text into a real, loadable Scratch 3 (.sb3) file.

The same .txt file that renders as a block diagram on the lab page is the source
of truth for the downloadable program, so the picture and the project can never
drift apart.

Usage:
    python3 make_sb3.py starter.txt -o starter.sb3
    python3 make_sb3.py solution.txt -o solution.sb3 --project-name "Draw a Square"
    python3 make_sb3.py solution.txt --json          # print project.json, build nothing

Supported syntax is documented in references/scratchblocks-syntax.md. Any line the
compiler does not recognize is a hard error that names the line and suggests the
closest known block, so a bad lab fails at build time rather than in front of a
student.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import zipfile
from difflib import get_close_matches

HERE = os.path.dirname(os.path.abspath(__file__))
COSTUME_DIR = os.path.join(os.path.dirname(HERE), "assets", "costumes")

# Scratch input primitive type codes
NUM = 4          # math_number
POS_NUM = 5      # math_positive_number
WHOLE_NUM = 6    # math_whole_number
INT = 7          # math_integer
ANGLE = 8        # math_angle
COLOR = 9        # colour_picker
TEXT = 10        # text
VAR = 12         # data_variable

# ---------------------------------------------------------------------------
# Block table
#
# Key   : normalized signature, every operand replaced by "%"
# Value : dict with
#           opcode    - Scratch 3 opcode
#           slots     - one descriptor per "%", in left-to-right order
#           substacks - names of C-shaped body inputs (structural, not in the line)
#           extension - extension id that must be declared in project.json
#           shape     - "hat" | "stack" | "cap" | "reporter" | "boolean"
#
# Slot descriptors:
#   ("input", NAME, TYPE)           - value slot with a shadow of that primitive type
#   ("bool",  NAME)                 - boolean-only slot (no shadow)
#   ("field", NAME)                 - plain dropdown stored as a field
#   ("varfield", NAME)              - variable dropdown, stored as [name, id]
#   ("menu", NAME, MENU_OPCODE, MENU_FIELD) - dropdown backed by a shadow menu block
# ---------------------------------------------------------------------------
BLOCKS = {
    # ---- Events ----------------------------------------------------------
    "when green flag clicked": {"opcode": "event_whenflagclicked", "shape": "hat"},
    "when % key pressed": {
        "opcode": "event_whenkeypressed", "shape": "hat",
        "slots": [("field", "KEY_OPTION")],
    },
    "when this sprite clicked": {"opcode": "event_whenthisspriteclicked", "shape": "hat"},
    "when i receive %": {
        "opcode": "event_whenbroadcastreceived", "shape": "hat",
        "slots": [("broadcastfield", "BROADCAST_OPTION")],
    },
    "broadcast %": {
        "opcode": "event_broadcast",
        "slots": [("broadcastinput", "BROADCAST_INPUT")],
    },

    # ---- Motion ----------------------------------------------------------
    "move % steps": {"opcode": "motion_movesteps", "slots": [("input", "STEPS", NUM)]},
    "turn cw % degrees": {"opcode": "motion_turnright", "slots": [("input", "DEGREES", NUM)]},
    "turn ccw % degrees": {"opcode": "motion_turnleft", "slots": [("input", "DEGREES", NUM)]},
    "go to x: % y: %": {
        "opcode": "motion_gotoxy",
        "slots": [("input", "X", NUM), ("input", "Y", NUM)],
    },
    "glide % secs to x: % y: %": {
        "opcode": "motion_glidesecstoxy",
        "slots": [("input", "SECS", NUM), ("input", "X", NUM), ("input", "Y", NUM)],
    },
    "point in direction %": {
        "opcode": "motion_pointindirection", "slots": [("input", "DIRECTION", ANGLE)],
    },
    "change x by %": {"opcode": "motion_changexby", "slots": [("input", "DX", NUM)]},
    "set x to %": {"opcode": "motion_setx", "slots": [("input", "X", NUM)]},
    "change y by %": {"opcode": "motion_changeyby", "slots": [("input", "DY", NUM)]},
    "set y to %": {"opcode": "motion_sety", "slots": [("input", "Y", NUM)]},
    "if on edge, bounce": {"opcode": "motion_ifonedgebounce"},
    "x position": {"opcode": "motion_xposition", "shape": "reporter"},
    "y position": {"opcode": "motion_yposition", "shape": "reporter"},
    "direction": {"opcode": "motion_direction", "shape": "reporter"},

    # ---- Pen (extension) -------------------------------------------------
    "erase all": {"opcode": "pen_clear", "extension": "pen"},
    "stamp": {"opcode": "pen_stamp", "extension": "pen"},
    "pen down": {"opcode": "pen_penDown", "extension": "pen"},
    "pen up": {"opcode": "pen_penUp", "extension": "pen"},
    "set pen color to %": {
        "opcode": "pen_setPenColorToColor", "extension": "pen",
        "slots": [("input", "COLOR", COLOR)],
    },
    "set pen size to %": {
        "opcode": "pen_setPenSizeTo", "extension": "pen",
        "slots": [("input", "SIZE", NUM)],
    },
    "change pen size by %": {
        "opcode": "pen_changePenSizeBy", "extension": "pen",
        "slots": [("input", "SIZE", NUM)],
    },
    "set pen % to %": {
        "opcode": "pen_setPenColorParamTo", "extension": "pen",
        "slots": [("menu", "COLOR_PARAM", "pen_menu_colorParam", "colorParam"),
                  ("input", "VALUE", NUM)],
    },
    "change pen % by %": {
        "opcode": "pen_changePenColorParamBy", "extension": "pen",
        "slots": [("menu", "COLOR_PARAM", "pen_menu_colorParam", "colorParam"),
                  ("input", "VALUE", NUM)],
    },

    # ---- Control ---------------------------------------------------------
    "wait % seconds": {"opcode": "control_wait", "slots": [("input", "DURATION", POS_NUM)]},
    "repeat %": {
        "opcode": "control_repeat",
        "slots": [("input", "TIMES", WHOLE_NUM)], "substacks": ["SUBSTACK"],
    },
    "forever": {"opcode": "control_forever", "substacks": ["SUBSTACK"], "shape": "cap"},
    "if % then": {
        "opcode": "control_if",
        "slots": [("bool", "CONDITION")], "substacks": ["SUBSTACK"],
    },
    "if % then else": {
        "opcode": "control_if_else",
        "slots": [("bool", "CONDITION")], "substacks": ["SUBSTACK", "SUBSTACK2"],
    },
    "repeat until %": {
        "opcode": "control_repeat_until",
        "slots": [("bool", "CONDITION")], "substacks": ["SUBSTACK"],
    },
    "wait until %": {"opcode": "control_wait_until", "slots": [("bool", "CONDITION")]},
    "stop %": {
        "opcode": "control_stop", "shape": "cap",
        "slots": [("field", "STOP_OPTION")],
    },

    # ---- Looks -----------------------------------------------------------
    "say %": {"opcode": "looks_say", "slots": [("input", "MESSAGE", TEXT)]},
    "say % for % seconds": {
        "opcode": "looks_sayforsecs",
        "slots": [("input", "MESSAGE", TEXT), ("input", "SECS", NUM)],
    },
    "think %": {"opcode": "looks_think", "slots": [("input", "MESSAGE", TEXT)]},
    "switch costume to %": {
        "opcode": "looks_switchcostumeto",
        "slots": [("menu", "COSTUME", "looks_costume", "COSTUME")],
    },
    "next costume": {"opcode": "looks_nextcostume"},
    "show": {"opcode": "looks_show"},
    "hide": {"opcode": "looks_hide"},
    "set size to % %": {"opcode": "looks_setsizeto", "slots": [("input", "SIZE", NUM)]},
    "change size by %": {"opcode": "looks_changesizeby", "slots": [("input", "CHANGE", NUM)]},

    # ---- Variables -------------------------------------------------------
    "set % to %": {
        "opcode": "data_setvariableto",
        "slots": [("varfield", "VARIABLE"), ("input", "VALUE", TEXT)],
    },
    "change % by %": {
        "opcode": "data_changevariableby",
        "slots": [("varfield", "VARIABLE"), ("input", "VALUE", NUM)],
    },
    "show variable %": {
        "opcode": "data_showvariable", "slots": [("varfield", "VARIABLE")],
    },
    "hide variable %": {
        "opcode": "data_hidevariable", "slots": [("varfield", "VARIABLE")],
    },

    # ---- Operators -------------------------------------------------------
    "% + %": {"opcode": "operator_add", "shape": "reporter",
              "slots": [("input", "NUM1", NUM), ("input", "NUM2", NUM)]},
    "% - %": {"opcode": "operator_subtract", "shape": "reporter",
              "slots": [("input", "NUM1", NUM), ("input", "NUM2", NUM)]},
    "% * %": {"opcode": "operator_multiply", "shape": "reporter",
              "slots": [("input", "NUM1", NUM), ("input", "NUM2", NUM)]},
    "% / %": {"opcode": "operator_divide", "shape": "reporter",
              "slots": [("input", "NUM1", NUM), ("input", "NUM2", NUM)]},
    "pick random % to %": {"opcode": "operator_random", "shape": "reporter",
                           "slots": [("input", "FROM", NUM), ("input", "TO", NUM)]},
    "% mod %": {"opcode": "operator_mod", "shape": "reporter",
                "slots": [("input", "NUM1", NUM), ("input", "NUM2", NUM)]},
    "round %": {"opcode": "operator_round", "shape": "reporter",
                "slots": [("input", "NUM", NUM)]},
    "join % %": {"opcode": "operator_join", "shape": "reporter",
                 "slots": [("input", "STRING1", TEXT), ("input", "STRING2", TEXT)]},
    "% > %": {"opcode": "operator_gt", "shape": "boolean",
              "slots": [("input", "OPERAND1", TEXT), ("input", "OPERAND2", TEXT)]},
    "% < %": {"opcode": "operator_lt", "shape": "boolean",
              "slots": [("input", "OPERAND1", TEXT), ("input", "OPERAND2", TEXT)]},
    "% = %": {"opcode": "operator_equals", "shape": "boolean",
              "slots": [("input", "OPERAND1", TEXT), ("input", "OPERAND2", TEXT)]},
    "% and %": {"opcode": "operator_and", "shape": "boolean",
                "slots": [("bool", "OPERAND1"), ("bool", "OPERAND2")]},
    "% or %": {"opcode": "operator_or", "shape": "boolean",
               "slots": [("bool", "OPERAND1"), ("bool", "OPERAND2")]},
    "not %": {"opcode": "operator_not", "shape": "boolean",
              "slots": [("bool", "OPERAND")]},

    # ---- Sensing ---------------------------------------------------------
    "touching %?": {
        "opcode": "sensing_touchingobject", "shape": "boolean",
        "slots": [("menu", "TOUCHINGOBJECTMENU", "sensing_touchingobjectmenu",
                   "TOUCHINGOBJECTMENU")],
    },
    "key % pressed?": {
        "opcode": "sensing_keypressed", "shape": "boolean",
        "slots": [("menu", "KEY_OPTION", "sensing_keyoptions", "KEY_OPTION")],
    },
    "mouse x": {"opcode": "sensing_mousex", "shape": "reporter"},
    "mouse y": {"opcode": "sensing_mousey", "shape": "reporter"},
    "timer": {"opcode": "sensing_timer", "shape": "reporter"},
    "reset timer": {"opcode": "sensing_resettimer"},
}

# Alternate spellings students and scratchblocks both accept.
ALIASES = {
    "when gf clicked": "when green flag clicked",
    "when flag clicked": "when green flag clicked",
    "when @greenflag clicked": "when green flag clicked",
    "turn right % degrees": "turn cw % degrees",
    "turn ↻ % degrees": "turn cw % degrees",
    "turn @turnright % degrees": "turn cw % degrees",
    "turn left % degrees": "turn ccw % degrees",
    "turn ↺ % degrees": "turn ccw % degrees",
    "turn @turnleft % degrees": "turn ccw % degrees",
    "clear": "erase all",
    "wait % secs": "wait % seconds",
    "say % for % secs": "say % for % seconds",
    "if % then, else": "if % then else",
}


class LabError(Exception):
    """A problem in the lab's block source, reported with the offending line."""


# ---------------------------------------------------------------------------
# Operand parsing
# ---------------------------------------------------------------------------

CLOSERS = {"(": ")", "[": "]", "<": ">"}


def is_opener(text, i):
    """True if text[i] opens an operand group.

    "<" is ambiguous: it opens a boolean group in `<(x) = (1)>` but is the
    less-than operator in `<(x) < (50)>`. Scratch's own convention decides it
    by spacing - an operator is written with a space after it.
    """
    ch = text[i]
    if ch not in CLOSERS:
        return False
    if ch == "<":
        return i + 1 < len(text) and text[i + 1] != " "
    return True


def is_closer(text, i):
    """True if text[i] closes an operand group.

    Mirror of is_opener: a ">" preceded by a space is the greater-than
    operator, as in `<(x) > (50)>`, not the end of the boolean.
    """
    ch = text[i]
    if ch not in CLOSERS.values():
        return False
    if ch == ">":
        return i > 0 and text[i - 1] != " "
    return True


def split_operands(text):
    """Split a line into literal words and bracketed operands.

    Returns a list of tokens: plain strings for literal text, and
    ("operand", kind, inner_text) tuples for ( ), [ ] and < > groups.
    Nesting is respected, so `((a) + (b))` comes back as one operand.
    """
    tokens, buf, i = [], "", 0
    while i < len(text):
        if not is_opener(text, i):
            buf += text[i]
            i += 1
            continue
        depth, j = 1, i + 1
        while j < len(text) and depth:
            if is_opener(text, j):
                depth += 1
            elif is_closer(text, j):
                depth -= 1
            j += 1
        if depth:
            raise LabError("unbalanced '%s' in: %s" % (text[i], text))
        if buf.strip():
            tokens.append(buf.strip())
        buf = ""
        tokens.append(("operand", text[i], text[i + 1:j - 1]))
        i = j
    if buf.strip():
        tokens.append(buf.strip())
    return tokens


def signature(tokens):
    parts = []
    for t in tokens:
        parts.append("%" if isinstance(t, tuple) else t)
    sig = re.sub(r"\s+", " ", " ".join(parts)).strip().lower()
    # A trailing "?" is part of the block label, not a separate word, so
    # `touching [edge v]?` and `touching [edge v] ?` mean the same block.
    return re.sub(r"\s+\?", "?", sig)


def lookup(sig):
    sig = ALIASES.get(sig, sig)
    return sig, BLOCKS.get(sig)


def suggest(sig):
    near = get_close_matches(sig, list(BLOCKS) + list(ALIASES), n=3, cutoff=0.5)
    return ("  Did you mean: " + ", ".join(repr(n) for n in near)) if near else ""


# ---------------------------------------------------------------------------
# Parsing source text into a tree
# ---------------------------------------------------------------------------

class Node:
    def __init__(self, sig, spec, operands, line_no, raw):
        self.sig = sig
        self.spec = spec
        self.operands = operands          # list of ("operand", kind, inner)
        self.bodies = []                  # list of lists of Node, one per substack
        self.line_no = line_no
        self.raw = raw


def parse_scripts(source):
    """Parse source text into a list of scripts, each a list of top-level Nodes."""
    lines = []
    for n, raw in enumerate(source.splitlines(), start=1):
        line = raw.split("//")[0].rstrip()
        lines.append((n, line))

    scripts, current, stack = [], [], []
    for n, line in lines:
        stripped = line.strip()
        if not stripped:
            if not stack and current:
                scripts.append(current)
                current = []
            continue

        low = stripped.lower()
        if low in ("end", "end }", "}"):
            if not stack:
                raise LabError("line %d: 'end' with no matching C-block" % n)
            stack.pop()
            continue
        if low == "else":
            if not stack:
                raise LabError("line %d: 'else' outside an if block" % n)
            node = stack[-1]
            if node.sig != "if % then":
                raise LabError("line %d: 'else' is only allowed after 'if <> then'" % n)
            # Promote the if into an if/else and start the second body.
            node.sig, node.spec = lookup("if % then else")[0], BLOCKS["if % then else"]
            node.bodies.append([])
            continue

        node = parse_line(stripped, n)
        target = stack[-1].bodies[-1] if stack else current
        target.append(node)
        if node.spec.get("substacks"):
            node.bodies = [[]]
            stack.append(node)

    if stack:
        raise LabError("line %d: missing 'end' for '%s'" % (stack[-1].line_no, stack[-1].raw))
    if current:
        scripts.append(current)
    return scripts


def parse_line(stripped, n):
    if stripped.lower().startswith("define "):
        return Node("define", {"opcode": "procedures_definition", "shape": "hat"},
                    [("operand", "define", stripped[len("define "):].strip())], n, stripped)

    tokens = split_operands(stripped)
    sig, spec = lookup(signature(tokens))
    if spec is None:
        # Not a built-in: treat it as a call to a custom block.
        return Node("__call__", {"opcode": "procedures_call"}, tokens, n, stripped)
    operands = [t for t in tokens if isinstance(t, tuple)]
    if len(operands) != len(spec.get("slots", [])):
        raise LabError(
            "line %d: '%s' expects %d value(s) but got %d"
            % (n, stripped, len(spec.get("slots", [])), len(operands)))
    return Node(sig, spec, operands, n, stripped)


# ---------------------------------------------------------------------------
# Serialization into project.json blocks
# ---------------------------------------------------------------------------

NUMBER_RE = re.compile(r"^-?\d+(\.\d+)?$")


class Builder:
    def __init__(self):
        self.blocks = {}
        self.variables = {}      # name -> id
        self.broadcasts = {}     # name -> id
        self.procs = {}          # proccode -> {"argids": [...], "names": [...]}
        self.extensions = []
        self._n = 0

    # -- ids ---------------------------------------------------------------
    def new_id(self, prefix="b"):
        self._n += 1
        return "%s%d" % (prefix, self._n)

    def var_id(self, name):
        if name not in self.variables:
            self.variables[name] = "var-" + re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")
        return self.variables[name]

    def broadcast_id(self, name):
        if name not in self.broadcasts:
            self.broadcasts[name] = "bc-" + re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-")
        return self.broadcasts[name]

    def note_extension(self, spec):
        ext = spec.get("extension")
        if ext and ext not in self.extensions:
            self.extensions.append(ext)

    # -- operands ----------------------------------------------------------
    @staticmethod
    def dropdown_value(inner):
        """Strip the trailing ' v' that marks a scratchblocks dropdown."""
        return re.sub(r"\s+v$", "", inner.strip())

    def value_input(self, operand, type_code, parent, params, line_no):
        """Serialize one value operand into an sb3 input array."""
        kind, inner = operand[1], operand[2]
        text = inner.strip()

        if kind == "<":
            if not text:
                return None
            sub = self.emit_expression(operand, parent, params, line_no)
            return [2, sub]

        if kind == "[":
            if text.startswith("#"):
                return [1, [COLOR, text]]
            return [1, [TEXT, self.dropdown_value(text)]]

        # kind == "("
        if text == "":
            return [1, [type_code, ""]]
        if NUMBER_RE.match(text):
            return [1, [type_code, text]]

        tokens = split_operands(text)
        sig, spec = lookup(signature(tokens))
        if spec is None and not text.endswith(" v"):
            name = text
            if name in params:
                arg = self.new_id()
                self.blocks[arg] = {
                    "opcode": params[name],
                    "next": None, "parent": parent,
                    "inputs": {}, "fields": {"VALUE": [name, None]},
                    "shadow": False, "topLevel": False,
                }
                return [3, arg, [type_code, ""]]
            # Anything else in round brackets is a variable reporter.
            return [3, [VAR, name, self.var_id(name)], [type_code, ""]]

        if spec is None:
            return [1, [type_code, self.dropdown_value(text)]]

        sub = self.emit_expression(operand, parent, params, line_no)
        return [3, sub, [type_code, ""]]

    def emit_expression(self, operand, parent, params, line_no):
        """Emit a nested reporter/boolean block and return its id."""
        tokens = split_operands(operand[2].strip())
        sig, spec = lookup(signature(tokens))
        if spec is None:
            raise LabError("line %d: unknown reporter '%s'.%s"
                           % (line_no, operand[2].strip(), suggest(signature(tokens))))
        node = Node(sig, spec, [t for t in tokens if isinstance(t, tuple)], line_no,
                    operand[2])
        return self.emit_block(node, parent, None, params)

    # -- blocks ------------------------------------------------------------
    def emit_block(self, node, parent, next_id, params):
        if node.sig == "define":
            return self.emit_define(node, next_id, params)
        if node.sig == "__call__":
            return self.emit_call(node, parent, next_id, params)

        spec = node.spec
        self.note_extension(spec)
        bid = self.new_id()
        inputs, fields = {}, {}

        for operand, slot in zip(node.operands, spec.get("slots", [])):
            kind = slot[0]
            if kind == "input":
                val = self.value_input(operand, slot[2], bid, params, node.line_no)
                if val is not None:
                    inputs[slot[1]] = val
            elif kind == "bool":
                if operand[2].strip():
                    inputs[slot[1]] = [2, self.emit_expression(operand, bid, params,
                                                               node.line_no)]
            elif kind == "field":
                fields[slot[1]] = [self.dropdown_value(operand[2]), None]
            elif kind == "varfield":
                name = self.dropdown_value(operand[2])
                fields[slot[1]] = [name, self.var_id(name)]
            elif kind == "broadcastfield":
                name = self.dropdown_value(operand[2])
                fields[slot[1]] = [name, self.broadcast_id(name)]
            elif kind == "broadcastinput":
                name = self.dropdown_value(operand[2])
                inputs[slot[1]] = [1, [11, name, self.broadcast_id(name)]]
            elif kind == "menu":
                mid = self.new_id()
                self.blocks[mid] = {
                    "opcode": slot[2], "next": None, "parent": bid,
                    "inputs": {}, "fields": {slot[3]: [self.dropdown_value(operand[2]), None]},
                    "shadow": True, "topLevel": False,
                }
                inputs[slot[1]] = [1, mid]

        for name, body in zip(spec.get("substacks", []), node.bodies):
            first = self.emit_stack(body, bid, params)
            if first:
                inputs[name] = [2, first]

        self.blocks[bid] = {
            "opcode": spec["opcode"], "next": next_id, "parent": parent,
            "inputs": inputs, "fields": fields,
            "shadow": False, "topLevel": False,
        }
        if spec["opcode"] == "control_stop":
            has_next = fields.get("STOP_OPTION", [""])[0] == "other scripts in sprite"
            self.blocks[bid]["mutation"] = {
                "tagName": "mutation", "children": [],
                "hasnext": "true" if has_next else "false",
            }
        return bid

    def emit_stack(self, nodes, parent, params):
        """Emit a chain of stacked blocks; returns the id of the first one."""
        if not nodes:
            return None
        ids = [None] * len(nodes)
        for i in range(len(nodes) - 1, -1, -1):
            nxt = ids[i + 1] if i + 1 < len(nodes) else None
            owner = parent if i == 0 else None
            ids[i] = self.emit_block(nodes[i], owner, nxt, params)
        # Non-first blocks are parented to their predecessor.
        for i in range(1, len(nodes)):
            self.blocks[ids[i]]["parent"] = ids[i - 1]
        return ids[0]

    # -- custom blocks -----------------------------------------------------
    @staticmethod
    def proc_parts(tokens):
        """Build proccode plus argument names/types from a define/call token list."""
        proccode, names, types = [], [], []
        for t in tokens:
            if isinstance(t, tuple):
                kind, inner = t[1], t[2].strip()
                if kind == "<":
                    proccode.append("%b")
                    types.append("%b")
                else:
                    proccode.append("%s")
                    types.append("%s")
                names.append(inner)
            else:
                proccode.append(t)
        return " ".join(proccode), names, types

    def emit_define(self, node, next_id, params):
        header = node.operands[0][2]
        tokens = split_operands(header)
        proccode, names, types = self.proc_parts(tokens)
        argids = ["arg-%s-%d" % (re.sub(r"[^A-Za-z0-9]+", "-", proccode).strip("-"), i)
                  for i in range(len(names))]
        self.procs[proccode] = {"argids": argids, "names": names, "types": types}

        def_id, proto_id = self.new_id(), self.new_id()
        proto_inputs = {}
        for argid, name, typ in zip(argids, names, types):
            rid = self.new_id()
            self.blocks[rid] = {
                "opcode": ("argument_reporter_boolean" if typ == "%b"
                           else "argument_reporter_string_number"),
                "next": None, "parent": proto_id,
                "inputs": {}, "fields": {"VALUE": [name, None]},
                "shadow": True, "topLevel": False,
            }
            proto_inputs[argid] = [1, rid]

        self.blocks[proto_id] = {
            "opcode": "procedures_prototype", "next": None, "parent": def_id,
            "inputs": proto_inputs, "fields": {}, "shadow": True, "topLevel": False,
            "mutation": {
                "tagName": "mutation", "children": [], "proccode": proccode,
                "argumentids": json.dumps(argids),
                "argumentnames": json.dumps(names),
                "argumentdefaults": json.dumps(
                    ["false" if t == "%b" else "" for t in types]),
                "warp": "false",
            },
        }
        self.blocks[def_id] = {
            "opcode": "procedures_definition", "next": next_id, "parent": None,
            "inputs": {"custom_block": [1, proto_id]}, "fields": {},
            "shadow": False, "topLevel": True, "x": 0, "y": 0,
        }
        return def_id

    def emit_call(self, node, parent, next_id, params):
        # For a call, node.operands holds the whole token list, literals included.
        proccode, _, _ = self.proc_parts(node.operands)
        known = self.procs.get(proccode)
        if known is None:
            raise LabError(
                "line %d: unknown block '%s'.%s\n"
                "  If this is a custom block, add its 'define %s' script first."
                % (node.line_no, node.raw, suggest(signature(node.operands)), proccode))
        bid = self.new_id()
        inputs = {}
        arg_operands = [t for t in node.operands if isinstance(t, tuple)]
        for argid, operand, typ in zip(known["argids"], arg_operands, known["types"]):
            if typ == "%b":
                if operand[2].strip():
                    inputs[argid] = [2, self.emit_expression(operand, bid, params,
                                                             node.line_no)]
            else:
                val = self.value_input(operand, TEXT, bid, params, node.line_no)
                if val is not None:
                    inputs[argid] = val
        self.blocks[bid] = {
            "opcode": "procedures_call", "next": next_id, "parent": parent,
            "inputs": inputs, "fields": {}, "shadow": False, "topLevel": False,
            "mutation": {
                "tagName": "mutation", "children": [], "proccode": proccode,
                "argumentids": json.dumps(known["argids"]), "warp": "false",
            },
        }
        return bid

    @staticmethod
    def scope_for(script):
        """Parameter names in scope for a script (its 'define' header, if any)."""
        if not script or script[0].sig != "define":
            return {}
        _, names, types = Builder.proc_parts(split_operands(script[0].operands[0][2]))
        return {name: ("argument_reporter_boolean" if typ == "%b"
                       else "argument_reporter_string_number")
                for name, typ in zip(names, types)}

    # -- whole file --------------------------------------------------------
    def build(self, scripts):
        # Custom-block definitions must be registered before any call to them.
        ordered = sorted(scripts, key=lambda s: 0 if s and s[0].sig == "define" else 1)
        x, y = 60, 60
        for script in ordered:
            params = self.scope_for(script)
            first = self.emit_stack(script, None, params)
            if first is None:
                continue
            head = self.blocks[first]
            head["topLevel"] = True
            head["parent"] = None
            head["x"], head["y"] = x, y
            y += 60 + 48 * sum(1 for _ in script)
            if y > 900:
                x, y = x + 340, 60
        return self.blocks


# ---------------------------------------------------------------------------
# project.json / .sb3 packaging
# ---------------------------------------------------------------------------

TURTLE_SVG = "00c7cc0dda5a3e305182918fce955957.svg"
BACKDROP_SVG = "cd21514d0531fdffb22204e0ec5ed84a.svg"


def costume_entry(path, name, rcx, rcy):
    data = open(path, "rb").read()
    md5 = hashlib.md5(data).hexdigest()
    return data, {
        "assetId": md5, "name": name, "bitmapResolution": 1,
        "md5ext": "%s.svg" % md5, "dataFormat": "svg",
        "rotationCenterX": rcx, "rotationCenterY": rcy,
    }


def build_project(builder, sprite_name, sprite_x, sprite_y, sprite_size):
    backdrop_data, backdrop = costume_entry(
        os.path.join(COSTUME_DIR, BACKDROP_SVG), "backdrop1", 240, 180)
    turtle_data, turtle = costume_entry(
        os.path.join(COSTUME_DIR, TURTLE_SVG), "coder-dojo-turtle-right", 158, 110.5)

    variables = {vid: [name, 0] for name, vid in builder.variables.items()}
    broadcasts = {bid: name for name, bid in builder.broadcasts.items()}

    stage = {
        "isStage": True, "name": "Stage", "variables": {}, "lists": {},
        "broadcasts": broadcasts, "blocks": {}, "comments": {},
        "currentCostume": 0, "costumes": [backdrop], "sounds": [],
        "volume": 100, "layerOrder": 0, "tempo": 60,
        "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None,
    }
    sprite = {
        "isStage": False, "name": sprite_name, "variables": variables, "lists": {},
        "broadcasts": {}, "blocks": builder.blocks, "comments": {},
        "currentCostume": 0, "costumes": [turtle], "sounds": [],
        "volume": 100, "layerOrder": 1, "visible": True,
        "x": sprite_x, "y": sprite_y, "size": sprite_size, "direction": 90,
        "draggable": False, "rotationStyle": "all around",
    }
    project = {
        "targets": [stage, sprite],
        "monitors": [],
        "extensions": builder.extensions,
        "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "scratch-lab-generator"},
    }
    return project, {backdrop["md5ext"]: backdrop_data, turtle["md5ext"]: turtle_data}


def main():
    ap = argparse.ArgumentParser(description="Compile scratchblocks text into an .sb3")
    ap.add_argument("input", help="scratchblocks .txt source file")
    ap.add_argument("-o", "--output", help="output .sb3 path")
    ap.add_argument("--json", action="store_true", help="print project.json and exit")
    ap.add_argument("--sprite-name", default="Cody")
    ap.add_argument("--sprite-x", type=float, default=0)
    ap.add_argument("--sprite-y", type=float, default=0)
    ap.add_argument("--sprite-size", type=float, default=20)
    args = ap.parse_args()

    source = open(args.input, encoding="utf-8").read()
    try:
        scripts = parse_scripts(source)
        builder = Builder()
        builder.build(scripts)
    except LabError as exc:
        sys.stderr.write("%s: %s\n" % (args.input, exc))
        return 1

    project, assets = build_project(builder, args.sprite_name, args.sprite_x,
                                    args.sprite_y, args.sprite_size)
    if args.json:
        print(json.dumps(project, indent=2))
        return 0

    out = args.output or os.path.splitext(args.input)[0] + ".sb3"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("project.json", json.dumps(project))
        for name, data in assets.items():
            z.writestr(name, data)
    n_blocks = sum(1 for b in builder.blocks.values() if not b.get("shadow"))
    print("%s: %d blocks, %d script(s), extensions=%s"
          % (out, n_blocks, len(scripts), builder.extensions or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
