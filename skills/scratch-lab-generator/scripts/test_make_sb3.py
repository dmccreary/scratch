#!/usr/bin/env python3
"""
test_make_sb3.py - regression tests for the scratchblocks -> .sb3 compiler.

Run after any change to make_sb3.py:

    python3 skills/scratch-lab-generator/scripts/test_make_sb3.py

Every case is checked structurally, and if `jsonschema` is installed each
generated project is also validated against the official Scratch 3 schema
bundled in assets/. These cases were verified end to end against Scratch's own
scratch-parser, so a regression here means a lab that will not open.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import make_sb3 as m  # noqa: E402

FAILURES = []


def compile_source(src):
    builder = m.Builder()
    builder.build(m.parse_scripts(src))
    project, _ = m.build_project(builder, "Cody", 0, 0, 20)
    return builder, project


def check(name, condition, detail=""):
    if condition:
        print("  pass  %s" % name)
    else:
        print("  FAIL  %s %s" % (name, detail))
        FAILURES.append(name)


def opcodes(builder):
    return [b["opcode"] for b in builder.blocks.values()]


def find(builder, opcode):
    return [b for b in builder.blocks.values() if b["opcode"] == opcode]


def test_linear_stack():
    b, _ = compile_source(
        "when green flag clicked\nerase all\npen down\nmove (100) steps\n")
    tops = [x for x in b.blocks.values() if x["topLevel"]]
    check("linear: one top-level hat", len(tops) == 1)
    check("linear: hat is the flag", tops[0]["opcode"] == "event_whenflagclicked")
    # Walk the chain and confirm every link is doubly consistent.
    seen, bid = [], [k for k, v in b.blocks.items() if v["topLevel"]][0]
    while bid:
        seen.append(b.blocks[bid]["opcode"])
        nxt = b.blocks[bid]["next"]
        if nxt:
            check("linear: %s parent link" % b.blocks[nxt]["opcode"],
                  b.blocks[nxt]["parent"] == bid)
        bid = nxt
    check("linear: chain order", seen == ["event_whenflagclicked", "pen_clear",
                                          "pen_penDown", "motion_movesteps"], seen)
    check("linear: input shadow type",
          find(b, "motion_movesteps")[0]["inputs"]["STEPS"] == [1, [4, "100"]])


def test_pen_extension():
    _, p = compile_source("when green flag clicked\npen down\n")
    check("pen: extension declared", p["extensions"] == ["pen"])
    _, p = compile_source("when green flag clicked\nmove (10) steps\n")
    check("pen: not declared when unused", p["extensions"] == [])


def test_c_block_nesting():
    b, _ = compile_source(
        "when green flag clicked\nrepeat (4)\n  move (100) steps\n"
        "  turn cw (90) degrees\nend\n")
    rep = find(b, "control_repeat")[0]
    check("repeat: TIMES uses whole-number shadow",
          rep["inputs"]["TIMES"] == [1, [6, "4"]])
    body = rep["inputs"]["SUBSTACK"]
    check("repeat: substack is a [2, id] input", body[0] == 2)
    first = b.blocks[body[1]]
    check("repeat: body starts with move", first["opcode"] == "motion_movesteps")
    check("repeat: body parent is the loop", first["parent"] == [
        k for k, v in b.blocks.items() if v is rep][0])
    check("repeat: body has two blocks",
          first["next"] is not None and b.blocks[first["next"]]["next"] is None)


def test_if_else():
    b, _ = compile_source(
        "when green flag clicked\nif <(1) = (1)> then\n  say [yes]\nelse\n"
        "  say [no]\nend\n")
    check("if/else: promoted to control_if_else", find(b, "control_if_else"))
    ie = find(b, "control_if_else")[0]
    check("if/else: both substacks present",
          "SUBSTACK" in ie["inputs"] and "SUBSTACK2" in ie["inputs"])
    check("if/else: condition is a boolean input", ie["inputs"]["CONDITION"][0] == 2)


def test_comparison_operators():
    """`>` and `<` as operators must not be mistaken for bracket delimiters."""
    b, _ = compile_source(
        "when green flag clicked\nwait until <<(x position) > (200)> or "
        "<(y position) < (50)>>\n")
    check("compare: greater-than parsed", find(b, "operator_gt"))
    check("compare: less-than parsed", find(b, "operator_lt"))
    check("compare: or parsed", find(b, "operator_or"))
    o = find(b, "operator_or")[0]
    check("compare: or has two boolean operands",
          o["inputs"]["OPERAND1"][0] == 2 and o["inputs"]["OPERAND2"][0] == 2)


def test_variables_autocreate():
    b, p = compile_source(
        "when green flag clicked\nset [angle v] to (90)\n"
        "turn cw (angle) degrees\nchange [angle v] by (10)\n")
    check("vars: created on the sprite", len(p["targets"][1]["variables"]) == 1)
    turn = find(b, "motion_turnright")[0]
    check("vars: reporter uses the [12, name, id] primitive",
          turn["inputs"]["DEGREES"][1][0] == 12,
          turn["inputs"]["DEGREES"])
    setv = find(b, "data_setvariableto")[0]
    check("vars: field carries name and id",
          setv["fields"]["VARIABLE"][0] == "angle" and setv["fields"]["VARIABLE"][1])


def test_custom_block():
    b, p = compile_source(
        "define polygon (sides) (size)\nrepeat (sides)\n  move (size) steps\nend\n\n"
        "when green flag clicked\npolygon (6) (80)\n")
    check("custom: definition emitted", find(b, "procedures_definition"))
    check("custom: prototype emitted", find(b, "procedures_prototype"))
    check("custom: call emitted", find(b, "procedures_call"))
    proto = find(b, "procedures_prototype")[0]
    check("custom: proccode has two %s args",
          proto["mutation"]["proccode"] == "polygon %s %s",
          proto["mutation"]["proccode"])
    call = find(b, "procedures_call")[0]
    check("custom: call argumentids match the prototype",
          call["mutation"]["argumentids"] == proto["mutation"]["argumentids"])
    # Parameters must be argument reporters, never variables.
    check("custom: parameters are not variables", p["targets"][1]["variables"] == {},
          p["targets"][1]["variables"])
    check("custom: parameter use compiles to an argument reporter",
          len(find(b, "argument_reporter_string_number")) >= 3)
    defn = find(b, "procedures_definition")[0]
    check("custom: definition body is attached", defn["next"] is not None)


def test_menus_and_broadcasts():
    b, p = compile_source(
        "when [space v] key pressed\nbroadcast [go v]\n\n"
        "when i receive [go v]\nset pen (color v) to (50)\n"
        "if <touching [edge v]?> then\n  stop [this script v]\nend\n")
    check("menu: pen colour param shadow", find(b, "pen_menu_colorParam"))
    check("menu: shadow flag set", find(b, "pen_menu_colorParam")[0]["shadow"] is True)
    check("menu: touching-object shadow", find(b, "sensing_touchingobjectmenu"))
    check("broadcast: registered on the stage", len(p["targets"][0]["broadcasts"]) == 1)
    check("broadcast: hat field carries the id",
          find(b, "event_whenbroadcastreceived")[0]["fields"]["BROADCAST_OPTION"][1])
    check("stop: mutation present", "mutation" in find(b, "control_stop")[0])


def test_aliases():
    for text in ("turn right (90) degrees", "turn cw (90) degrees",
                 "turn @turnright (90) degrees"):
        b, _ = compile_source("when green flag clicked\n%s\n" % text)
        check("alias: %r -> motion_turnright" % text, find(b, "motion_turnright"))
    b, _ = compile_source("when gf clicked\nclear\n")
    check("alias: 'when gf clicked'", find(b, "event_whenflagclicked"))
    check("alias: 'clear' -> pen_clear", find(b, "pen_clear"))


def test_multiple_scripts():
    b, _ = compile_source(
        "when green flag clicked\nmove (10) steps\n\n"
        "when this sprite clicked\nhide\n")
    tops = [x for x in b.blocks.values() if x["topLevel"]]
    check("scripts: two top-level stacks", len(tops) == 2)
    check("scripts: laid out at distinct positions",
          len({(t["x"], t["y"]) for t in tops}) == 2)


def test_errors_are_loud():
    for src, why in [
        ("when green flag clicked\nfly to the moon (3)\n", "unknown block"),
        ("when green flag clicked\nrepeat (4)\nmove (10) steps\n", "missing end"),
        ("when green flag clicked\nmove (10) steps (20)\n", "too many operands"),
        ("when green flag clicked\nelse\n", "stray else"),
    ]:
        try:
            compile_source(src)
            check("error: %s rejected" % why, False, "compiled without error")
        except m.LabError:
            check("error: %s rejected" % why, True)


def test_schema():
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from jsonschema import Draft7Validator, RefResolver
    except ImportError:
        print("  skip  schema validation (pip install jsonschema)")
        return
    assets = os.path.join(os.path.dirname(HERE), "assets")
    schema = json.load(open(os.path.join(assets, "sb3_schema.json")))
    defs = json.load(open(os.path.join(assets, "sb3_definitions.json")))
    store = {"sb3_definitions.json": defs,
             "https://scratch.mit.edu/sb3_definitions.json": defs,
             schema["$id"]: schema}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        resolver = RefResolver(base_uri=schema["$id"], referrer=schema, store=store)
    validator = Draft7Validator(schema, resolver=resolver)

    samples = [
        "when green flag clicked\nerase all\npen down\nrepeat (4)\n"
        "  move (100) steps\n  turn cw (90) degrees\nend\n",
        "define star (n)\nrepeat (n)\n  move (80) steps\n  turn cw (144) degrees\nend\n\n"
        "when green flag clicked\nstar (5)\n",
        "when [space v] key pressed\nif <<(x position) > (0)> and <(1) = (1)>> then\n"
        "  say [right side] for (1) seconds\nend\n",
    ]
    for i, src in enumerate(samples, 1):
        _, project = compile_source(src)
        errs = list(validator.iter_errors(project))
        check("schema: sample %d validates" % i, not errs,
              errs[0].message[:120] if errs else "")


def main():
    for fn in sorted(
            (v for k, v in globals().items() if k.startswith("test_")),
            key=lambda f: f.__code__.co_firstlineno):
        print("%s:" % fn.__name__)
        fn()
    print()
    if FAILURES:
        print("%d FAILURE(S): %s" % (len(FAILURES), ", ".join(FAILURES)))
        return 1
    print("all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
