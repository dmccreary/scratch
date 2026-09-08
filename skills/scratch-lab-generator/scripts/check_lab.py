#!/usr/bin/env python3
"""
check_lab.py - build and verify one generated Scratch lab.

Run this after generating a lab. It is the gate that keeps a lab honest:

  1. Compiles every *.txt block source in the lab into a real .sb3.
  2. Validates each project.json against the official Scratch 3 schema
     (bundled offline in assets/, so no network is needed).
  3. Checks index.md - required sections, mascot poses that actually exist on
     disk, download links that resolve, and <pre class="blocks"> diagrams that
     still match their .txt source.

Usage:
    python3 check_lab.py docs/labs/draw-a-square
    python3 check_lab.py docs/labs/draw-a-square --fix   # re-sync diagrams from .txt
"""

import argparse
import glob
import html
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
sys.path.insert(0, HERE)

import make_sb3  # noqa: E402

REQUIRED_SECTIONS = [
    "## What You Will Learn",
    "## The Starter Program",
    "## Your Task",
    "## Check Your Work",
    "## The Solution",
]

# Every lab opens with a challenge and closes with a celebration.
REQUIRED_POSES = ["welcome", "celebration"]

PRE_RE = re.compile(r'(?m)^([ \t]*)<pre class="blocks">\n(.*?)\n[ \t]*</pre>', re.DOTALL)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.notes = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def note(self, msg):
        self.notes.append(msg)

    def print_and_exit(self, lab):
        for n in self.notes:
            print("  ok    %s" % n)
        for w in self.warnings:
            print("  WARN  %s" % w)
        for e in self.errors:
            print("  ERROR %s" % e)
        print("%s: %d error(s), %d warning(s)" % (lab, len(self.errors), len(self.warnings)))
        return 1 if self.errors else 0


def load_validator():
    import warnings
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            from jsonschema import Draft7Validator, RefResolver
    except ImportError:
        return None
    schema = json.load(open(os.path.join(ASSETS, "sb3_schema.json")))
    defs = json.load(open(os.path.join(ASSETS, "sb3_definitions.json")))
    store = {
        "sb3_definitions.json": defs,
        "https://scratch.mit.edu/sb3_definitions.json": defs,
        schema["$id"]: schema,
    }
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        resolver = RefResolver(base_uri=schema["$id"], referrer=schema, store=store)
    return Draft7Validator(schema, resolver=resolver)


def build_programs(lab, report):
    """Compile each .txt into .sb3. Returns {basename: block source text}."""
    sources = {}
    txts = sorted(glob.glob(os.path.join(lab, "*.txt")))
    if not txts:
        report.error("no .txt block source files found - a lab needs at least solution.txt")
        return sources

    validator = load_validator()
    if validator is None:
        report.warn("jsonschema not installed; skipping sb3 schema validation "
                    "(pip install jsonschema)")

    for txt in txts:
        name = os.path.splitext(os.path.basename(txt))[0]
        source = open(txt, encoding="utf-8").read()
        sources[name] = source.strip("\n")
        try:
            scripts = make_sb3.parse_scripts(source)
            builder = make_sb3.Builder()
            builder.build(scripts)
        except make_sb3.LabError as exc:
            report.error("%s.txt: %s" % (name, exc))
            continue

        project, assets = make_sb3.build_project(builder, "Cody", 0, 0, 20)
        if validator is not None:
            errs = sorted(validator.iter_errors(project), key=lambda e: list(e.path))
            if errs:
                report.error("%s.sb3 fails the Scratch schema: %s" % (name, errs[0].message[:200]))
                continue

        out = os.path.join(lab, name + ".sb3")
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("project.json", json.dumps(project))
            for asset_name, data in assets.items():
                z.writestr(asset_name, data)
        n = sum(1 for b in builder.blocks.values() if not b.get("shadow"))
        report.note("%s.sb3 built and validated (%d blocks, %d script(s))"
                    % (name, n, len(scripts)))
    return sources


def check_index(lab, sources, report, fix):
    path = os.path.join(lab, "index.md")
    if not os.path.exists(path):
        report.error("index.md is missing")
        return
    text = open(path, encoding="utf-8").read()

    for section in REQUIRED_SECTIONS:
        if section not in text:
            report.error("index.md is missing the required section '%s'" % section)

    # Mascot poses must exist on disk at the path the page actually uses.
    poses = re.findall(r"!!!\s+mascot-(\w+)|\?\?\?\s+mascot-(\w+)", text)
    used = {a or b for a, b in poses}
    for pose in REQUIRED_POSES:
        cls = {"welcome": "welcome", "celebration": "celebration"}[pose]
        if cls not in used:
            report.warn("no mascot-%s admonition - every lab should open with a "
                        "challenge and close with a celebration" % cls)

    docs_root = os.path.abspath(os.path.join(lab, "..", ".."))
    for img in re.findall(r"!\[[^\]]*\]\((\.\./\.\./img/mascot/[^)]+)\)", text):
        target = os.path.normpath(os.path.join(lab, img))
        if not os.path.exists(target):
            report.error("mascot image not found: %s (expected at %s)"
                         % (img, os.path.relpath(target, docs_root)))
    if not re.search(r"!\[[^\]]*\]\(\.\./\.\./img/mascot/", text):
        report.warn("no mascot images found - check the ../../img/mascot/ path depth")

    for link in re.findall(r'href="([^"]+\.sb3)"', text):
        if not os.path.exists(os.path.join(lab, link)):
            report.error("download link points at a missing file: %s" % link)

    # Rendered diagrams must still match their .txt source.
    matches = list(PRE_RE.finditer(text))
    if not matches:
        report.error("index.md has no <pre class=\"blocks\"> block diagram")
    order = [n for n in ("starter", "solution") if n in sources]

    def normalize(block):
        return "\n".join(l.strip() for l in block.split("\n") if l.strip())

    if len(matches) == len(order):
        replacements = []
        for match, name in zip(matches, order):
            indent, rendered = match.group(1), match.group(2)
            expected = html.escape(sources[name], quote=False)
            if normalize(rendered) != normalize(expected):
                if fix:
                    # A diagram nested inside a ??? block carries the indentation
                    # that keeps it part of that block, so preserve it.
                    body = "\n".join(indent + l if l.strip() else ""
                                      for l in expected.split("\n"))
                    replacements.append((match.span(2), body))
                    report.note("re-synced the %s diagram from %s.txt" % (name, name))
                else:
                    report.error("the %s diagram in index.md no longer matches %s.txt "
                                 "(run with --fix to re-sync)" % (name, name))
        if replacements:
            for (start, end), body in reversed(replacements):
                text = text[:start] + body + text[end:]
            open(path, "w", encoding="utf-8").write(text)
    else:
        report.warn("index.md has %d diagram(s) but the lab has %d block source file(s)"
                    % (len(matches), len(order)))

    if "&lt;" not in text and re.search(r'<pre class="blocks">[^<]*\bif <', text):
        report.warn("angle brackets inside a block diagram should be written as "
                    "&lt; and &gt; so the browser does not eat them")


def main():
    ap = argparse.ArgumentParser(description="Build and verify a Scratch lab directory")
    ap.add_argument("lab", help="path to the lab directory, e.g. docs/labs/draw-a-square")
    ap.add_argument("--fix", action="store_true",
                    help="re-sync block diagrams in index.md from the .txt sources")
    args = ap.parse_args()

    lab = args.lab.rstrip("/")
    if not os.path.isdir(lab):
        sys.stderr.write("not a directory: %s\n" % lab)
        return 1

    print("checking %s" % lab)
    report = Report()
    sources = build_programs(lab, report)
    check_index(lab, sources, report, args.fix)
    return report.print_and_exit(lab)


if __name__ == "__main__":
    sys.exit(main())
